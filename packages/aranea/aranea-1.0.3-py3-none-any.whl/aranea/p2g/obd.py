"""
Module to extract OBD connectors from the PDF document.
"""

from typing import Annotated, Any

import pymupdf
from rich.progress import track

from aranea.models.graph_model import (ComponentNode, EcuClassification,
                                       EcuClassificationName, get_default_text)
from aranea.p2g.util import (REM, DictTextBlock, color2str, gendocstring,
                             is_horizontal)


@gendocstring
def get_obd_connectors(
    page: pymupdf.Page,
    word_blocks: list[DictTextBlock],
    rem: REM,
    progress: Annotated[bool, "Enable printing progress bars"] = False,
    *,
    obd_min_height: Annotated[float, "Minimum height of OBD connectors"] = 8,
    obd_max_height: Annotated[float, "Maximum height of OBD connectors"] = 9,
    obd_min_width: Annotated[float, "Minimum width of OBD connectors"] = 27,
    obd_max_width: Annotated[float, "Maximum width of OBD connectors"] = 28,
    obd_color: Annotated[str, "Color of the underlying rectangle of the OBD connector"] = "#99ccff",
    **_: Any  # Ignore all other keyword arguments
) -> Annotated[list[ComponentNode], "A list of obd connectors"]:
    """
    Extracts all OBD connectors from the page. There will probably be only
    one OBD connector most of the time.
    """

    obds: list[ComponentNode] = []
    for path in track(
        page.get_drawings(extended=False),
        description="Extracting OBD connectors",
        disable=not progress,
    ):
        if not "items" in path or not "fill" in path:
            continue

        # ignore drawings without full fill opacity
        if path.get("fill_opacity") != 1.0:
            continue

        # filter by fill color
        if isinstance(path.get("fill"), tuple) and color2str(path.get("fill")) != obd_color.lower():
            continue

        for item in [i for i in path["items"] if i[0] == "re"]:
            if item[0] != "re":
                continue
            rect = item[1]

            # filter by rectangle size
            if (
                rect.height >= obd_min_height
                and rect.height <= obd_max_height
                and rect.width >= obd_min_width
                and rect.width <= obd_max_width
            ):
                obd = ComponentNode(
                    xRemFactor=rect.x0 / rem,
                    yRemFactor=rect.y0 / rem,
                    widthRemFactor=(rect.x1 - rect.x0) / rem,
                    heightRemFactor=(rect.y1 - rect.y0) / rem,
                    classifications={
                        EcuClassification(name=EcuClassificationName.EXTERNAL_INTERFACE)
                    },
                )
                obds.append(obd)

                rect = (
                    obd.xRemFactor * rem,
                    obd.yRemFactor * rem - 8,
                    obd.xRemFactor * rem + obd.widthRemFactor * rem,
                    obd.yRemFactor * rem - 1,
                )

                blocks: list[DictTextBlock] = [  # pyright: ignore
                    b
                    for b in word_blocks  # pyright: ignore
                    if is_horizontal(*b["bbox"])  # pyright: ignore
                    and pymupdf.Rect(b["bbox"]).intersects(rect)  # pyright: ignore
                ]
                outer_text_words: list[str] = []
                spans_list: list[list[dict[str, Any]]] = [
                    l["spans"] for b in blocks for l in b["lines"]
                ]
                size = 0
                for spans in spans_list:
                    outer_text_words.extend([s["text"] for s in spans])
                    s = max(s["size"] for s in spans)
                    size = max(size, s)
                outer_text = "".join(outer_text_words).replace("\n", "")
                obd.outerText = get_default_text(outer_text, rem_factor=size / rem)

                # remove used word blocks
                for block in blocks:
                    word_blocks.remove(block)
    return obds
