"""
Module to extract network line labels from the PDF document.
"""

import logging
from typing import Annotated, Any, cast
from uuid import UUID

from rich.progress import track
from shapely import LineString, Point, Polygon
from shapely.affinity import translate
from shapely.geometry.base import BaseGeometry

from aranea.models.graph_model import (ComponentNode, Edge, Network,
                                       NodeUnionType, Text, TextOrientation,
                                       WaypointNode, XorNode, get_default_text)
from aranea.p2g.util import REM, DictTextBlock, gendocstring

# ignore partially unknown type and ignore all formatting to keep the ignore
# comment where it is
#
# fmt: off
from shapely import convex_hull, unary_union  # pyright: ignore , isort: skip , pylint: disable=wrong-import-order,ungrouped-imports
# fmt: on

logger = logging.getLogger(__file__)

HORIZONTAL: tuple[float, float] = (1.0, 0.0)
TEXT_TO_IGNORE = ["xor", "...", ". . .", "m"]


def __is_horizontal(x0: float, y0: float, x1: float, y1: float) -> bool:
    return abs(x1 - x0) > abs(y1 - y0)


def __node_attachment2point(
    rem: REM, node: NodeUnionType, attach_x: float, attach_y: float
) -> Point:
    if isinstance(node, (ComponentNode, XorNode)):
        return Point(
            node.xRemFactor * rem + node.widthRemFactor * rem * attach_x,
            node.yRemFactor * rem + node.heightRemFactor * rem * attach_y,
        )
    if isinstance(node, WaypointNode):
        return Point(node.xRemFactor * rem, node.yRemFactor * rem)

    # we cannot correctly calculate the absolute point for a TextNode
    # attachment because TextNodes do miss height and width attributes.
    raise NotImplementedError(
        f"Cannot convert attachment point to absolute point for {node.__class__}"
    )


def __bbox2polygon(bbox: tuple[float, float, float, float]) -> Polygon:
    x1, y1, x2, y2 = bbox
    return Polygon(((x1, y1), (x2, y1), (x2, y2), (x1, y2), (x1, y1)))


def __is_text_line_to_be_ignored(line: dict[str, Any]) -> bool:
    for span in line["spans"]:
        if span["text"].lower().strip() in TEXT_TO_IGNORE:
            logger.debug('Skipping "%s" text span', span["text"])
            return True
    return False


# order edge candidates by orientation and distance to text span
def __sorting_key(
    line: LineString, span_poly: Polygon, text_orientation: TextOrientation
) -> tuple[bool, float]:
    p1, p2 = list(line.coords)
    line_is_horizontal = __is_horizontal(*p1, *p2)
    text_is_horizontal = text_orientation == TextOrientation.HORIZONTAL
    same_orientation = line_is_horizontal == text_is_horizontal

    # we prefer edges with same orientation so invert `same_orientation` bc False < True
    return not same_orientation, line.distance(span_poly)


# TODO: maybe prefer edge candidates that do not already have a text span associated with them
def __find_nearest_edge_to_text_line(
    text_line: dict[str, Any],
    max_label_to_line_distance: float,
    networks: list[Network],
    nodes: dict[UUID, NodeUnionType],
    waypoints: dict[UUID, WaypointNode],
    text_orientation: TextOrientation,
    rem: REM,
) -> Edge | None:
    text_line_poly = __bbox2polygon(text_line["bbox"])

    # Ensure that the text bbox does not intersect with any component node
    if not all(
        node.polygon(rem=rem).intersection(text_line_poly).is_empty
        for node in nodes.values()
        if isinstance(node, ComponentNode)
    ):
        return None

    text_line_poly_for_intersection = text_line_poly.buffer(max_label_to_line_distance)

    if text_orientation == TextOrientation.HORIZONTAL:
        text_bbox_height = abs(text_line["bbox"][2] - text_line["bbox"][0])
    else:
        text_bbox_height = abs(text_line["bbox"][1] - text_line["bbox"][3])

    dx, dy = cast(tuple[float, float], text_line.get("dir"))

    poly_for_intersection_below_text = convex_hull(
        unary_union(
            [
                text_line_poly,
                translate(text_line_poly, xoff=-dy * text_bbox_height, yoff=dx * text_bbox_height),
            ]
        )
    )

    def __find_edges_that_intersect_polygon(
        polygon_to_intersect: Polygon | BaseGeometry,
    ) -> list[tuple[Edge, LineString]]:
        candidates: list[tuple[Edge, LineString]] = []
        for network in networks:
            for edge in network.edges:
                source = nodes.get(edge.sourceId, waypoints.get(edge.sourceId))
                target = nodes.get(edge.targetId, waypoints.get(edge.targetId))

                if source is None:
                    raise ValueError("Edge source not found")
                if target is None:
                    raise ValueError("Edge target not found")

                p1 = __node_attachment2point(
                    rem,
                    source,
                    edge.sourceAttachmentPointX or 0,
                    edge.sourceAttachmentPointY or 0,
                )
                p2 = __node_attachment2point(
                    rem,
                    target,
                    edge.targetAttachmentPointX or 0,
                    edge.targetAttachmentPointY or 0,
                )
                edge_line = LineString((p1, p2))

                if edge_line.intersects(polygon_to_intersect):
                    candidates.append((edge, edge_line))
        return candidates

    edge_candidates = __find_edges_that_intersect_polygon(poly_for_intersection_below_text)
    if len(edge_candidates) == 0:
        edge_candidates = __find_edges_that_intersect_polygon(text_line_poly_for_intersection)

    if len(edge_candidates) > 0:
        return min(
            edge_candidates, key=lambda c: __sorting_key(c[1], text_line_poly, text_orientation)
        )[0]
    return None


def __edge_text_lines2text(
    text_lines: list[tuple[dict[str, Any], TextOrientation]], rem: REM
) -> Text:
    if text_lines[0][1] == TextOrientation.HORIZONTAL:
        text_lines = sorted(text_lines, key=lambda line: line[0]["bbox"][:1:-1])
    elif text_lines[0][1] == TextOrientation.VERTICAL:
        text_lines = sorted(text_lines, key=lambda line: line[0]["bbox"][:1])

    edge_label_text = "\n".join(
        ["".join([s["text"] for s in line[0]["spans"]]) for line in text_lines]
    )

    if len({line[1] for line in text_lines}) > 1:
        logger.warning('Multiple text orientations in edge label "%s"', edge_label_text)

    o = text_lines[0][1]
    s = text_lines[0][0]["spans"][0]["size"]
    return get_default_text(edge_label_text, text_orientation=o, rem_factor=s / rem)


@gendocstring
def add_labels_to_networks(
    rem: REM,
    word_blocks: Annotated[list[DictTextBlock], "The current page's word blocks"],
    networks: Annotated[list[Network], "The list of networks"],
    nodes: Annotated[dict[UUID, NodeUnionType], "A dictionary of nodes"],
    waypoints: Annotated[dict[UUID, WaypointNode], "A dictionary of waypoints"],
    max_label_to_line_distance: Annotated[
        float, "The maximum distance between a network label and network line segment"
    ],
    progress: Annotated[bool, "Enable printing progress bars"] = False,
) -> Annotated[list[Network], "The list of networks with labels"]:
    """
    Finds network labels and assigns them to network edges.
    """
    # keep track of all spans to assign to an edge
    edge2text_lines: dict[Edge, list[tuple[dict[str, Any], TextOrientation]]] = {}
    word_blocks_to_remove: list[DictTextBlock] = []
    for block in track(word_blocks, description="Assigning network labels", disable=not progress):
        if "lines" not in block:
            continue
        for line in block["lines"]:
            if "spans" not in line:
                continue

            text_orientation: TextOrientation = (
                TextOrientation.HORIZONTAL
                if line.get("dir") == HORIZONTAL
                else TextOrientation.VERTICAL
            )
            if __is_text_line_to_be_ignored(line):
                continue

            nearest_edge = __find_nearest_edge_to_text_line(
                line,
                max_label_to_line_distance,
                networks,
                nodes,
                waypoints,
                text_orientation,
                rem,
            )
            if nearest_edge is None:
                continue
            if nearest_edge not in edge2text_lines:
                edge2text_lines[nearest_edge] = []
            edge2text_lines[nearest_edge].append((line, text_orientation))
            word_blocks_to_remove.append(block)

    for edge, lines in edge2text_lines.items():
        lines = [(line[0], line[1]) for line in lines]
        if len(lines) > 0:
            edge.text = __edge_text_lines2text(lines, rem)

    for block in word_blocks_to_remove:
        try:
            word_blocks.remove(block)
        except ValueError:
            pass

    return networks
