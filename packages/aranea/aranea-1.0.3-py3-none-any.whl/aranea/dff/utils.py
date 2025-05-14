"""
Module containing utility functions for diffing two Graphs conforming to the pydantic model.
"""

import logging
from enum import Enum
from typing import Optional
from uuid import UUID

import numpy as np
from shapely.geometry import LineString, Point, Polygon

from aranea.g2d.style_configs.get_default_style_config import \
    get_default_style_config
from aranea.g2d.text_node_constants import (
    TEXT_NODE_BOUNDING_BOX_HEIGHT_FACTOR, TEXT_NODE_BOUNDING_BOX_WIDTH_FACTOR)
from aranea.g2d.transform_waypoint_node_to_mx_cell import \
    DEFAULT_WAYPOINT_DIMENSION
from aranea.models.graph_model import (ComponentNode, Edge, Graph, Network,
                                       WaypointNode, XorNode)
from aranea.models.style_config_model import StyleConfig

logger = logging.getLogger(__name__)


# ------- Basic enums and types -------
class AttachmentPoint(Enum):
    """
    Valid attachment points for inserted edges.
    """

    TOP = 0.5, 0.0
    RIGHT = 1.0, 0.5
    BOTTOM = 0.5, 1.0
    LEFT = 0.0, 0.5


class EdgeDirection(Enum):
    """
    Possible directions of edges.
    """

    UP = "up"
    DOWN = "down"
    LEFT = "left"
    RIGHT = "right"


# ------- Geometric node operations -------
def get_waypoint_polygon(waypoint: WaypointNode) -> Polygon:
    """
    Generate a polygon representation of a WaypointNode.

    :param waypoint: The waypoint node to convert
    :type waypoint: WaypointNode
    :return: Polygon representing the waypoint's area
    :rtype: Polygon
    """
    center = Point(waypoint.xRemFactor, waypoint.yRemFactor)

    # Buffer radius is approximately half the waypoint dimension in rem units
    return center.buffer(DEFAULT_WAYPOINT_DIMENSION / get_default_style_config().rem_size / 2.0)


def get_graph_boundaries(graph: Graph) -> tuple[tuple[float, float], tuple[float, float]]:
    """
    Calculate the minimum and maximum coordinates of all nodes in the graph.

    :param graph: Graph to analyze
    :type graph: Graph

    :return: Tuple of ((min_x, min_y), (max_x, max_y)) in rem factors
    :rtype: tuple[tuple[float, float], tuple[float, float]]
    """
    if not graph.nodes:
        return (0.0, 0.0), (0.0, 0.0)

    min_x = float("inf")
    min_y = float("inf")
    max_x = -float("inf")
    max_y = -float("inf")

    default_rem_size = get_default_style_config().rem_size

    for node in graph.nodes.values():
        if isinstance(node, (ComponentNode, XorNode)):
            node_max_x = node.xRemFactor + node.widthRemFactor
            node_max_y = node.yRemFactor + node.heightRemFactor
        elif isinstance(node, WaypointNode):
            wp_size = DEFAULT_WAYPOINT_DIMENSION / default_rem_size
            node_max_x = node.xRemFactor + wp_size
            node_max_y = node.yRemFactor + wp_size
        else:  # TextNode
            node_max_x = node.xRemFactor + TEXT_NODE_BOUNDING_BOX_WIDTH_FACTOR / default_rem_size
            node_max_y = node.yRemFactor + TEXT_NODE_BOUNDING_BOX_HEIGHT_FACTOR / default_rem_size

        min_x = min(min_x, node.xRemFactor)
        min_y = min(min_y, node.yRemFactor)
        max_x = max(max_x, node_max_x)
        max_y = max(max_y, node_max_y)

    return (min_x, min_y), (max_x, max_y)


# ------- Edge operations -------
def get_edge_line(edge: Edge, graph: Graph) -> LineString:
    """
    Create a LineString representing the path of an edge between nodes.

    :param edge: The edge to visualize
    :type edge: Edge
    :param graph: Graph containing the edge's nodes
    :type graph: Graph

    :return: Line from source to target node centers
    :rtype: LineString
    """
    if edge.sourceId not in graph.nodes or edge.targetId not in graph.nodes:
        raise ValueError(
            f"Edge from ID {edge.sourceId} to ID {edge.targetId} does not have valid "
            "source and target nodes in the given graph."
        )

    source = graph.nodes[edge.sourceId]
    target = graph.nodes[edge.targetId]

    if isinstance(source, (ComponentNode, XorNode)):
        source_coords = source.polygon().centroid
    elif isinstance(source, WaypointNode):
        source_coords = Point(source.xRemFactor, source.yRemFactor)
    else:
        raise ValueError(f"Node with ID {edge.sourceId} should not have edges connected to it.")

    if isinstance(target, (ComponentNode, XorNode)):
        target_coords = target.polygon().centroid
    elif isinstance(target, WaypointNode):
        target_coords = Point(target.xRemFactor, target.yRemFactor)
    else:
        raise ValueError(f"Node with ID {edge.targetId} should not have edges connected to it.")

    return LineString([source_coords, target_coords])


def get_edge_polygon_from_line(edge_line: LineString, stroke_width: float) -> Polygon:
    """
    Create a buffered polygon around an edge line for collision detection.

    :param edge_line: The edge's line representation
    :type edge_line: LineString
    :param stroke_width: Stroke width of the edge
    :type stroke_width: float

    :return: Buffered polygon
    :rtype: Polygon
    """
    # buffer dilates the line by the given value in every direction
    # here, half the stroke width in rem units needs to be used, same as in draw.io
    return edge_line.buffer(stroke_width / get_default_style_config().rem_size / 2.0)


def get_mean_edge_strokewidth_from_config(style_cfg: StyleConfig) -> float:
    """
    Calculate the average stroke width from network style configurations.

    :param style_cfg: Style configuration data
    :type style_cfg: StyleConfig

    :return: Average stroke width in rem
    :rtype: float
    """
    if style_cfg.network_protocol_type_style_attributes:
        stroke_widths = [
            attrs.stroke_width or 1.0
            for attrs in style_cfg.network_protocol_type_style_attributes.values()
        ]
        stroke_width = (
            float(
                np.mean(stroke_widths),  # pyright: ignore
            )
            if stroke_widths
            else 1.0
        )
    else:
        stroke_width = 1.0
    return stroke_width


def get_edge_direction(edge: Edge, attached_node_id: UUID, graph: Graph) -> EdgeDirection:
    """
    Determine the direction of an edge relative to an attached node.

    :param edge: The edge to analyze
    :type edge: Edge
    :param attached_node_id: UUID of the node to use as reference -
        needs to be either sourceId or targetId of the edge.
    :type attached_node: UUID
    :param graph: Graph containing the edge
    :type graph: Graph

    :return: Direction from the node's perspective
    :rtype: EdgeDirection
    """
    if attached_node_id not in (edge.sourceId, edge.targetId):
        raise ValueError(f"Node with ID {attached_node_id} is not attached to given edge.")

    source = graph.nodes[edge.sourceId]
    target = graph.nodes[edge.targetId]

    viewed_from_source = attached_node_id == edge.sourceId

    if isinstance(source, WaypointNode):
        source_point = Point(source.xRemFactor, source.yRemFactor)
    elif isinstance(source, (ComponentNode, XorNode)):
        source_point = source.polygon().centroid
    else:
        raise ValueError(f"Node with ID {edge.sourceId} should not have edges connected to it.")

    if isinstance(target, WaypointNode):
        target_point = Point(target.xRemFactor, target.yRemFactor)
    elif isinstance(target, (ComponentNode, XorNode)):
        target_point = target.polygon().centroid
    else:
        raise ValueError(f"Node with ID {edge.targetId} should not have edges connected to it.")

    # Calculate the difference in x and y coordinates, one of them should be 0
    dx = target_point.x - source_point.x
    dy = target_point.y - source_point.y

    if viewed_from_source:
        if abs(dx) > abs(dy):  # horizontal edge
            return EdgeDirection.RIGHT if dx > 0 else EdgeDirection.LEFT
        # vertical edge
        return EdgeDirection.DOWN if dy > 0 else EdgeDirection.UP
    # viewed from target
    if abs(dx) > abs(dy):
        return EdgeDirection.LEFT if dx > 0 else EdgeDirection.RIGHT
    return EdgeDirection.UP if dy > 0 else EdgeDirection.DOWN


def create_edge_with_attachment_point(
    source_id: UUID,
    target_id: UUID,
    source_attachment_point: Optional[AttachmentPoint] = None,
    target_attachment_point: Optional[AttachmentPoint] = None,
) -> Edge:
    """
    Create an edge with specified attachment points using the AttachmentPoint-Enum.

    :param source_id: Source node UUID
    :type source_id: UUID
    :param target_id: Target node UUID
    :type target_id: UUID
    :param source_attachment_point: Optional source attachment point
    :type source_attachment_point: Optional[AttachmentPoint]
    :param target_attachment_point: Optional target attachment point
    :type target_attachment_point: Optional[AttachmentPoint]

    :return: Configured Edge instance
    :rtype: Edge
    """
    sap_x, sap_y = source_attachment_point.value if source_attachment_point else (None, None)
    tap_x, tap_y = target_attachment_point.value if target_attachment_point else (None, None)

    return Edge(
        sourceId=source_id,
        targetId=target_id,
        sourceAttachmentPointX=sap_x,
        sourceAttachmentPointY=sap_y,
        targetAttachmentPointX=tap_x,
        targetAttachmentPointY=tap_y,
    )


def sort_network_edges_by_length(network: Network, graph: Graph) -> None:
    """
    Sort a network's edges in descending order of their geometric length.

    Operates in-place on the network's edges list.

    :param network: Network whose edges to sort
    :type network: Network
    :param graph: Graph containing edge nodes
    :type graph: Graph

    :rtype: None
    """
    if network not in graph.networks:
        raise ValueError("Network is not in the given graph.")

    network.edges.sort(key=lambda edge: get_edge_line(edge, graph).length, reverse=True)


# ------- Network-node relationship functions -------
def get_network_element_ids(network: Network) -> set[UUID]:
    """
    Extract all node IDs connected to a network's edges.

    :param network: Network to analyze
    :type network: Network
    :return: Set of connected node UUIDs
    :rtype: set[UUID]
    """
    node_ids: set[UUID] = set()
    for edge in network.edges:
        node_ids.add(edge.sourceId)
        node_ids.add(edge.targetId)
    return node_ids


def get_components_from_network(network: Network, graph: Graph) -> dict[UUID, ComponentNode]:
    """
    Extracts and returns a dict containing the ComponentNodes connected to the given network with
    their respective UUID.

    :param network: The Network to extract the components from
    :type network: Network
    :param graph: The Graph containing the network
    :type graph: Graph

    :return: The dictionary containing the ComponentNodes connected to the given network with
             their respective UUID
    :rtype: dict[UUID, ComponentNode]
    """

    comp_dict: dict[UUID, ComponentNode] = {}
    for edge in network.edges:
        source = graph.nodes.get(edge.sourceId)
        target = graph.nodes.get(edge.targetId)
        if source and isinstance(source, ComponentNode):
            comp_dict[edge.sourceId] = source
        if target and isinstance(target, ComponentNode):
            comp_dict[edge.targetId] = target

    return comp_dict


def get_connected_edges_of_node(node_id: UUID, network: Network) -> set[Edge]:
    """
    Retrieve all edges in a network connected to a specific node.

    :param node_id: UUID of the node to check
    :type node_id: UUID
    :param network: Network to search
    :type network: Network
    :return: Set of connected edges
    :rtype: set[Edge]
    """
    connected_edges: set[Edge] = set()
    for edge in network.edges:
        if node_id in (edge.sourceId, edge.targetId):
            connected_edges.add(edge)
    return connected_edges


def count_node_references_in_graph(node_id: UUID, graph: Graph) -> int:
    """
    Count the number of edges connected to a specific node across all networks in a graph.

    :param node_id: The unique identifier of the node to count references for
    :type node_id: UUID
    :param graph: The graph to count references to the node in
    :type graph: Graph

    :return: The total number of edges connected to the specified node across all networks
    :rtype: int
    """
    count = 0
    for network in graph.networks:
        count += len(get_connected_edges_of_node(node_id, network))

    return count


# ------- High-level network operations -------
def compare_networks(nw1: Network, nw2: Network) -> bool:
    """
    Function to compare two networks that does not care for the order its edges are in.
    This is needed to compare networks contained in the graph associated with a NodePlacer object,
    as the edges in these networks get sorted by size.

    :param nw1: The first Network to compare
    :type nw1: Network
    :param nw2: The second Network to compare
    :type nw2: Network

    :return: True if networks are the same (excluding edge order), False otherwise
    :rtype: bool
    """
    # Compare high-level network attributes first
    if nw1.protocol_type != nw2.protocol_type:
        return False
    if nw1.amg_only != nw2.amg_only:
        return False
    if nw1.dff_classification != nw2.dff_classification:
        return False

    # Compare edges regardless of their order.
    if len(nw1.edges) != len(nw2.edges):
        return False

    # Convert each edge to a frozenset of its dictionary items for order-independent comparison.
    edges1 = {frozenset(edge.model_dump().items()) for edge in nw1.edges}
    edges2 = {frozenset(edge.model_dump().items()) for edge in nw2.edges}

    return edges1 == edges2


seen_networks: set[Network] = (
    set()
)  # used to store the networks for which a warning has been issued


def get_network_name(nw: Network) -> Optional[str]:
    """
    Returns the text that is most prevalent on the edges of the given network or None if no text is
    present.

    :param nw: The network to get the name of
    :type nw: Network

    :return: The text that is most prevalent on the edges of the given network or None if no text is
             present.
    :rtype: Optional[str]
    """
    # Dictionary to count occurrences of each edge text
    text_counts: dict[str, int] = {}

    # Iterate through all edges in the network
    for edge in nw.edges:
        if edge.text:
            text_counts[edge.text[0]] = text_counts.get(edge.text[0], 0) + 1

    # If no text was found on any edge
    if not text_counts:
        return None

    if len(text_counts) > 1 and nw not in seen_networks:
        seen_networks.add(nw)
        logger.warning("There are %d different texts on an edge. The texts are:", len(text_counts))
        for text, count in text_counts.items():
            logger.warning('"%s" for %d times', text, count)
        logger.warning("This may cause errors in diffing")

    # Return the text with the highest count
    return max(text_counts.items(), key=lambda x: x[1])[0]


def check_networks_in_graph(networks: list[Network], graph: Graph) -> Optional[tuple[str, int]]:
    """
    Check if a list of networks is present in a given graph.
    Returns the most prevalent text on the edges of the first network and its index, if it is not
    present in the graph. Otherwise, returns None.

    :param network: The network to check
    :type network: Network
    :param graph: The graph to check in
    :type graph: Graph

    :return: The most prevalent text on the edges of the first network and its index, if it is not
             present in the graph. Otherwise, returns None.
    :rtype: Optional[tuple[str, int]]
    """
    if len(graph.networks) == 0:
        raise ValueError("Graph given to check_networks_in_graph contains no networks")

    for i, nw in enumerate(networks):
        nw_name = get_network_name(nw)
        nw_name = "Unknown" if nw_name is None else nw_name
        if nw not in graph.networks:
            return nw_name, i
    return None
