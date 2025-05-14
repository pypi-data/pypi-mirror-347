"""
Module to extract XOR nodes from the PDF document.
"""

from dataclasses import dataclass
from math import isclose, sqrt
from typing import Annotated, Any

from pymupdf.pymupdf import Page, Rect
from rich.progress import track

from aranea.models.graph_model import XorNode, get_default_text
from aranea.p2g.util import REM, DictTextBlock, gendocstring


def __calculate_distance(p1: tuple[float, float], p2: tuple[float, float]) -> float:
    """
    Calculates the Euclidean distance between two points.

    :param p1: The first point, as a tuple of (x, y) coordinates.
    :type p1: tuple[float, float]
    :param p2: The second point, as a tuple of (x, y) coordinates.
    :type p2: tuple[float, float]
    :return: The distance between the two points.
    :rtype: float
    """
    return sqrt((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2)


def __is_diamond(points: list[tuple[float, float]], tolerance: float = 5) -> bool:
    """
    Checks if the given points form a diamond shape by verifying that all side lengths are
    nearly equal.

    :param points: A list of four points (tuples of x, y coordinates) representing the vertices
                   of the shape.
    :type points: list[tuple[float, float]]
    :param tolerance: The tolerance for comparing side lengths, default is 0.1.
    :type tolerance: float
    :return: True if the points form a diamond (all sides are nearly equal within the
             tolerance), False otherwise.
    :rtype: bool
    """
    if len(points) != 4:
        return False

    # calculate side lengths
    d1 = __calculate_distance(points[0], points[1])
    d2 = __calculate_distance(points[1], points[2])
    d3 = __calculate_distance(points[2], points[3])
    d4 = __calculate_distance(points[3], points[0])

    # checks if all sides are nearly the same length
    return (
        isclose(d1, d2, abs_tol=tolerance)
        and isclose(d2, d3, abs_tol=tolerance)
        and isclose(d3, d4, abs_tol=tolerance)
    )


def __is_overlapping(
    bbox1: tuple[float, float, float, float],
    bbox2: tuple[float, float, float, float],
    threshold: float = 0.3,
) -> bool:
    """
    Checks if two bounding boxes overlap by more than the specified threshold.

    The overlap is calculated as a percentage of the area of the smaller bounding box.

    :param bbox1: Bounding box of the first text (x0, y0, x1, y1).
    :param bbox2: Bounding box of the second text (x0, y0, x1, y1).
    :param threshold: The overlap threshold (default is 0.3 for 30%).
    :return: True if the overlap is greater than the threshold; otherwise, False.
    """
    # Calculate the area of intersection
    x_overlap = max(0, min(bbox1[2], bbox2[2]) - max(bbox1[0], bbox2[0]))
    y_overlap = max(0, min(bbox1[3], bbox2[3]) - max(bbox1[1], bbox2[1]))
    intersection_area = x_overlap * y_overlap

    # Calculate the area of the smaller box
    bbox1_area = (bbox1[2] - bbox1[0]) * (bbox1[3] - bbox1[1])
    bbox2_area = (bbox2[2] - bbox2[0]) * (bbox2[3] - bbox2[1])
    smaller_area = min(bbox1_area, bbox2_area)

    # Determine if overlap is greater than the threshold
    return (intersection_area / smaller_area) > threshold


def __get_text_in_diamond(rect: Rect, word_blocks: list[DictTextBlock]) -> tuple[str, float]:
    """
    Extracts and concatenates text within a given diamond area.

    This function iterates over text blocks and collects texts that fall within
    the specified rectangle (rect). It sorts the texts from top to bottom,
    left to right, and removes any overlapping texts that have more than 30%
    overlap with an already included text (keeping the last-encountered text).

    :param rect: The bounding rectangle of the diamond.
    :param texts: All text blocks on the page.
    :return: A concatenated string of text within the diamond.
    """

    @dataclass
    class _DiamondText:
        text: str
        bbox: tuple[float, float, float, float]
        size: float

    diamond_texts: list[_DiamondText] = []

    for block in word_blocks:
        if block["type"] == 0:  # Only text blocks
            if rect.intersects(block["bbox"]):
                for line in block["lines"]:
                    for span in line["spans"]:
                        text: str = span["text"]
                        text_bbox: tuple[float, float, float, float] = span["bbox"]
                        size: float = span["size"]
                        diamond_texts.append(_DiamondText(text=text, bbox=text_bbox, size=size))

    # Sort texts by y (top to bottom), then by x (left to right)
    diamond_texts = sorted(diamond_texts, key=lambda t: (t.bbox[1], t.bbox[0]))

    # Filter overlapping texts by keeping only the "topmost" in the stack (last in list order)
    filtered_texts: list[_DiamondText] = []
    for current_text in reversed(diamond_texts):  # Process from the last element to the first
        if len(current_text.bbox) != 4 or not all(
            isinstance(coord, float) for coord in current_text.bbox
        ):
            raise ValueError("current_text['bbox'] must be a tuple of four floats")
        overlapping: bool = False
        for other_text in filtered_texts:
            if __is_overlapping(current_text.bbox, other_text.bbox):
                overlapping = True
                break
        if not overlapping:
            filtered_texts.append(current_text)

    # Reverse filtered_texts to maintain original order in output
    filtered_texts.reverse()

    # Concatenate texts
    concatenated_text = " ".join(t.text for t in filtered_texts)
    size = max(filtered_texts, key=lambda t: t.size).size
    return concatenated_text, size


def __get_points_and_rect(drawing: dict[str, Any]) -> tuple[list[tuple[float, float]], Rect | None]:
    """
    Extracts points and rectangle information from a drawing element based on its type.

    :param drawing: The drawing element to process, containing shape or line data.
    :type drawing: dict
    :return: A tuple with a list of points and a rectangle (rect) if available, otherwise
    False.
    :rtype: tuple[list[tuple[float, float]], Rect | None]
    """
    points: list[tuple[float, float]] = []
    rect: Rect | None = None
    if not "items" in drawing or drawing["type"] not in ["s", "fs"]:
        return [], None

    if drawing["type"] == "s":
        for item in reversed(drawing["items"]):
            if item[0] == "qu":
                quad = item[1]
                points = [(point.x, point.y) for point in quad]
                rect = drawing["rect"]
                return points, rect

    elif drawing["type"] == "fs":
        points = [(item[1].x, item[1].y) for item in drawing["items"] if item[0] == "l"]
        rect = drawing["rect"]
        return points, rect

    return [], None


@gendocstring
def get_xor_nodes(
    page: Page,
    word_blocks: list[DictTextBlock],
    rem: REM,
    progress: Annotated[bool, "Enable printing progress bars"] = False,
    *,
    xor_min_height: Annotated[float, "Minimum height of XOR diamond shapes"] = 10,
    **_: Any  # Ignore all other keyword arguments
) -> Annotated[list[XorNode], "A list of XorNodes"]:
    """
    Extracts diamond shapes in the pdf

    This method iterates through the drawings on the page, identifies diamond shapes.
    It then creates Diamond and returns a list of XorNodes.
    """

    seen_diamonds: set[tuple[tuple[float, float], ...]] = (
        set()
    )  # Set for monitoring diamonds that have already been found
    diamonds: list[XorNode] = []

    drawings: list[dict[str, Any]] = page.get_drawings()

    for drawing in track(drawings, description="Extracting XOR nodes", disable=not progress):
        points: list[tuple[float, float]]
        rect: Rect | None
        points, rect = __get_points_and_rect(drawing)
        if rect is None or len(points) == 0:
            continue

        if len(points) > 0:
            if rect.height >= xor_min_height:

                # Check if the line points form a diamond
                if __is_diamond(points):
                    diamond_str, diamond_size = __get_text_in_diamond(
                        rect,
                        word_blocks=word_blocks,
                    )
                    diamond_text = get_default_text(diamond_str, rem_factor=diamond_size / rem)
                    # Convert points to tuple
                    points_tuple = tuple(sorted(points))  # sort tuples to find duplicates
                    if points_tuple not in seen_diamonds:
                        if not isinstance(rect.x0, float):
                            raise ValueError("rect.x0 must be a float")
                        if not isinstance(rect.y0, float):
                            raise ValueError("rect.y0 must be a float")
                        if not isinstance(rect.width, float):
                            raise ValueError("rect.width must be a float")
                        diamond = XorNode(
                            xRemFactor=rect.x0 / rem,
                            yRemFactor=rect.y0 / rem,
                            widthRemFactor=rect.height / rem,
                            heightRemFactor=rect.width / rem,
                            innerText=diamond_text,
                        )

                        seen_diamonds.add(points_tuple)  # add tuple for duplicate check
                        diamonds.append(diamond)

    return diamonds
