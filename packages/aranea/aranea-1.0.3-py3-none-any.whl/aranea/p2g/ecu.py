"""
Module to extract Electronic Control Units from the PDF document.
"""

import re
from collections.abc import Generator
from typing import Annotated, Any, List, Tuple, cast

from pymupdf import Page, Rect
from rich.progress import track
from shapely import Polygon

from aranea.models.graph_model import ComponentNode, Text, get_default_text
from aranea.p2g.util import REM, DictTextBlock, gendocstring, is_horizontal

HORIZONTAL: tuple[float, float] = (1.0, 0.0)


def __remove_nested_ecus(
    ecus: List[ComponentNode] | Generator[ComponentNode],
) -> Generator[ComponentNode]:
    for ecu in ecus:
        for other_ecu in ecus:
            if ecu == other_ecu:
                continue
            if other_ecu.polygon().contains(ecu.polygon()):
                break
        else:
            yield ecu


def __get_inner_ecu_text(ecu: ComponentNode, page: Page, rem: REM) -> Text | None:
    rect = Rect(
        ecu.xRemFactor * rem,
        ecu.yRemFactor * rem,
        ecu.xRemFactor * rem + ecu.widthRemFactor * rem,
        ecu.yRemFactor * rem + ecu.heightRemFactor * rem,
    )

    word_blocks: list[DictTextBlock] = cast(
        list[DictTextBlock],
        page.get_text("dict", clip=rect)["blocks"],  # pyright: ignore
    )

    # cleanup the found text block and combine its lines into a single string
    size: float = 0.0
    seen: set[str] = set()
    lines: list[str] = []
    for block in word_blocks:
        if block.get("lines") is None:
            continue
        for line in block["lines"]:
            # only consider horizontal lines
            if line.get("dir") == HORIZONTAL:
                for span in line.get("spans", []):
                    text = str(span.get("text")).strip()
                    if text not in seen:
                        seen.add(text)
                        lines.append(text)
                    s: float = span.get("size")
                    size = max(size, s)

    ecu_text = " ".join(lines).strip()
    return get_default_text(ecu_text, rem_factor=size / rem)


def __get_outer_ecu_text(
    ecu: Annotated[ComponentNode, "The ECU for which to extract the outer text"],
    ecus: Annotated[List[ComponentNode], "List of all ECUs"],
    word_blocks: list[DictTextBlock],
    rem: REM,
) -> Tuple[Text, bool] | Tuple[None, bool]:
    # rectangle above the ecu
    rect = (
        ecu.xRemFactor * rem,
        ecu.yRemFactor * rem - 4,
        (ecu.xRemFactor + ecu.widthRemFactor) * rem,
        ecu.yRemFactor * rem - 1,
    )

    def __vert_distance2ecu(y1: float) -> float:
        return abs(y1 - ecu.yRemFactor * rem)

    def __bbox2poly(x1: float, y1: float, x2: float, y2: float) -> Polygon:
        _x1 = x1 / rem
        _y1 = y1 / rem
        _x2 = x2 / rem
        _y2 = y2 / rem
        return Polygon([(_x1, _y1), (_x2, _y1), (_x2, _y2), (_x1, _y2), (_x1, _y1)])

    blocks = [
        b
        for b in word_blocks
        if is_horizontal(*b["bbox"])
        and Rect(b.get("bbox")).intersects(rect)
        and all(not e.polygon().contains(__bbox2poly(*b["bbox"])) for e in ecus)
    ]

    def __cleanup(outer_text_block: Any) -> tuple[Text, bool]:
        seen: set[str] = set()
        lines: list[str] = []
        size = 0

        for line in outer_text_block.get("lines"):
            if Rect(line.get("bbox")).intersects(rect):
                for span in line.get("spans"):
                    text = span.get("text").strip()
                    if text not in seen:
                        seen.add(text)
                        lines.append(text)
                    size = max(size, span.get("size", 0))

        outer_text = " ".join(lines)
        amg_only = re.search(r"amg[\s_-]*only", outer_text, flags=re.IGNORECASE) is not None
        outer_text = re.sub(r"\(?amg[\s]*only\)?", "", outer_text, flags=re.IGNORECASE)
        outer_text = outer_text.replace("*", "").strip()

        return (
            get_default_text(outer_text, rem_factor=size / rem),
            amg_only,
        )

    if len(blocks) > 0:
        # remove used word blocks
        for block in blocks:
            word_blocks.remove(block)

        outer_text_block = min(
            blocks,
            key=lambda t: __vert_distance2ecu(
                t["bbox"][3],
            ),
        )
        return __cleanup(outer_text_block)
    return None, False


def __get_ecu_labels(
    page: Page, ecus: List[ComponentNode], word_blocks: list[DictTextBlock], rem: REM
) -> Generator[ComponentNode]:
    """
    Extracts the ECU labels from the page for the all ECUs of `ecus`

    :param ecus: The ecus to process.
    :type ecus: List[ComponentNode] | Generator[ComponentNode]
    :return: A generator for ComponentNode with the extracted labels
    :rtype: Generator[ComponentNode]
    """

    for ecu in ecus:
        ecu.innerText = __get_inner_ecu_text(ecu, page=page, rem=rem)
        ecu.outerText, ecu.amg_only = __get_outer_ecu_text(
            ecu, ecus=ecus, word_blocks=word_blocks, rem=rem
        )

        yield ecu


@gendocstring
def __remove_double_ecus(
    ecus: Annotated[List[ComponentNode], "List of all found ECUs"],
    ecu_overlapping_tolerance: Annotated[float, "The tolerance for overlapping ECUs"],
) -> Annotated[List[ComponentNode], "List of all found ECUs without duplicates"]:
    """
    Removes ECUs that are too similar to each other
    """
    new_ecus: list[ComponentNode] = []
    reversed_ecus = ecus[::-1]
    for ecu in reversed_ecus:
        for other_ecu in new_ecus:
            if ecu == other_ecu:
                continue
            if (
                ecu.polygon().intersection(other_ecu.polygon()).area
                / min(ecu.polygon().area, other_ecu.polygon().area)
                > ecu_overlapping_tolerance
            ):
                break
        else:
            new_ecus.append(ecu)

    return new_ecus


@gendocstring
def get_ecus(
    page: Page,
    word_blocks: list[DictTextBlock],
    rem: REM,
    progress: Annotated[bool, "Enable printing progress bars"] = False,
    *,
    ecu_min_height: Annotated[
        float, "Minimum height of the rectangle to be considered as an ECU"
    ] = 15,
    ecu_max_height: Annotated[
        float, "Maximum height of the rectangle to be considered as an ECU"
    ] = 21,
    ecu_overlapping_tolerance: Annotated[float, "The tolerance for overlapping ECUs"] = 0.8,
    **_: Any  # Ignore all other keyword arguments
) -> Annotated[List[ComponentNode], "A generator of unique ECUs"]:
    """
    Extracts the ``ComponentNode`` of all Electronic
    Control Units (ECUs) from the page drawings based on their height.
    """

    ecu_rects: dict[Polygon, ComponentNode] = {}
    for path in page.get_drawings(extended=False):
        if not "items" in path:
            continue

        for item in path["items"]:
            # Process all rectangles
            if item[0] == "re":
                rect = item[1]

                # Filter rectangles by height
                if rect.height >= ecu_min_height and rect.height <= ecu_max_height:
                    ecu_rect = ComponentNode(
                        xRemFactor=rect.x0 / rem,
                        yRemFactor=rect.y0 / rem,
                        widthRemFactor=(rect.x1 - rect.x0) / rem,
                        heightRemFactor=(rect.y1 - rect.y0) / rem,
                    )
                    ecu_rects[ecu_rect.polygon()] = ecu_rect

    ecus: list[ComponentNode] = list(
        track(
            __get_ecu_labels(
                page, list(__remove_nested_ecus(list(ecu_rects.values()))), word_blocks, rem
            ),
            description="Extracting ECUs",
            disable=not progress,
        )
    )

    ecus = __remove_double_ecus(ecus, ecu_overlapping_tolerance)
    return ecus
