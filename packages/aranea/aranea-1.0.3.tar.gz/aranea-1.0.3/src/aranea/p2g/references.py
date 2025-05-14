"""
This module extracts all references from the word blocks and creates TextNodes for them.
"""

import logging
from typing import Annotated, Dict, List, Tuple, TypedDict
from uuid import UUID, uuid4

from pymupdf import Rect

from aranea.models.graph_model import TextNode, TextOrientation
from aranea.p2g.util import REM, DictTextBlock, gendocstring

logger = logging.getLogger(__name__)

HORIZONTAL: Tuple[float, float] = (1.0, 0.0)


class Span(TypedDict):
    """Represents a text span with bounding box information."""

    text: str
    bbox: Tuple[float, float, float, float]


class Line(TypedDict, total=False):
    """Represents a line with optional text direction and spans."""

    spans: List[Span]
    dir: Tuple[float, float]


@gendocstring
def get_references_as_text_nodes(
    rem: REM, word_blocks: Annotated[List[DictTextBlock], "The word blocks to process"]
) -> Annotated[Dict[UUID, TextNode], "A dictionary of nodes with their geometry data"]:
    """
    Extracts the references from the word blocks.
    """
    references: Dict[UUID, TextNode] = {}
    word_blocks_to_remove: List[DictTextBlock] = []
    counter: int = 0

    for block in word_blocks:
        if "lines" not in block:
            logger.debug("No lines in block %s", block)
            continue

        for line in block["lines"]:
            for span in line["spans"]:
                if span["text"].startswith(("à", "→")):
                    counter += 1
                    _process_reference_span(
                        rem, span, word_blocks, references, word_blocks_to_remove
                    )

    _remove_blocks(word_blocks, word_blocks_to_remove)

    logger.debug("Found %d references", counter)

    return references


def _process_reference_span(
    rem: REM,
    span: Span,
    word_blocks: List[DictTextBlock],
    references: Dict[UUID, TextNode],
    word_blocks_to_remove: List[DictTextBlock],
) -> None:
    """
    Process a reference span and add matching text nodes.
    """
    rect: Rect = _normalize_bbox(span["bbox"], rem)

    for other_block in word_blocks:
        if "lines" not in other_block:
            continue

        for other_line in other_block["lines"]:
            for other_span in other_line["spans"]:
                if other_span["text"].startswith(("à", "→")):
                    continue

                other_rect: Rect = _normalize_bbox(other_span["bbox"], rem)

                if _is_adjacent(rect, other_rect):
                    text_orientation = _get_text_orientation(other_line)
                    node_id = uuid4()
                    references[node_id] = TextNode(
                        # Use a non-breaking space to instruct drawio to keep
                        # the arrow and reference in one line
                        innerText=(f"→\u00a0{other_span['text'].strip()}", text_orientation, 1.0),
                        xRemFactor=other_rect.x0,
                        yRemFactor=other_rect.y0,
                    )
                    word_blocks_to_remove.append(other_block)


def _normalize_bbox(bbox: Tuple[float, float, float, float], rem: REM) -> Rect:
    """
    Normalize the bounding box values relative to REM.
    """
    x1, y1, x2, y2 = bbox
    return Rect(x1 / rem, y1 / rem, x2 / rem, y2 / rem)


def _is_adjacent(rect: Rect, other_rect: Rect) -> bool:
    """
    Check if the other span is next to or overlapping the reference span.
    """
    return (abs(other_rect.x0 - rect.x1) < 2 and abs(other_rect.y0 - rect.y0) < 2) or (
        abs(other_rect.y0 - rect.y1) < 2 and (other_rect.x0 < rect.x1 and other_rect.x1 > rect.x0)
    )


def _get_text_orientation(line: Line) -> TextOrientation:
    """
    Determine the text orientation based on the line direction.
    """
    return TextOrientation.HORIZONTAL if line.get("dir") == HORIZONTAL else TextOrientation.VERTICAL


def _remove_blocks(
    word_blocks: List[DictTextBlock], word_blocks_to_remove: List[DictTextBlock]
) -> None:
    """
    Remove processed blocks from the word blocks list.
    """
    for block in word_blocks_to_remove:
        try:
            word_blocks.remove(block)
        except ValueError:
            pass
