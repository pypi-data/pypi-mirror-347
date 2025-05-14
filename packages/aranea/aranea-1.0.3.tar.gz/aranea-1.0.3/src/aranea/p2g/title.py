"""
Module to extract the PDF document title.
"""

from typing import Annotated, Any

import pymupdf

from aranea.p2g.util import gendocstring


@gendocstring
def get_title(
    page: pymupdf.Page,
    *,
    title_line_width_factor: Annotated[
        float, "The min width of line above title relative to page width"
    ] = 0.9,
    **_: Any  # Ignore all other keyword arguments
) -> Annotated[tuple[str | None, float], "The title and font size"]:
    """
    Gets the diagram's title and title size.

    It tries to find the long horizontal line above the title and then
    return the text span with the largest size.
    """

    # get all horizontal lines of a certain length
    lines = [
        item
        for path in page.get_drawings(extended=False)
        for item in path["items"]
        if item[0] == "l"
        and abs(item[2].y - item[1].y) < 0.5  # check that the line is (mostly) horizontal
        and abs(item[2].x - item[1].x) >= page.mediabox.width * title_line_width_factor
    ]

    if len(lines) == 0:
        return None, 0

    y: float
    if len(lines) > 0:
        title_line = max(lines, key=lambda l: (l[1].y, abs(l[2].x - l[1].x)))
        y = title_line[1].y
    else:
        y = page.mediabox.height - 36

    # get all texts below the title line as dictionaries
    texts: list[dict[str, Any]] = page.get_text(  # pyright: ignore
        "dict",
        clip=[
            (0, y),
            (page.mediabox.width, page.mediabox.height),
        ],
    )
    sspans: list[list[dict[str, Any]]] = [
        lines["spans"] for b in texts["blocks"] for lines in b["lines"]  # type: ignore
    ]
    spans: list[dict[str, Any]] = [s for span in sspans for s in span]
    title_text: str = ""
    title_size: float = 0
    if len(spans) > 0:
        # Get the upper most text span with the largest size
        title = max(spans, key=lambda s: (s["size"], -s["origin"][1]))
        title_text = title["text"]
        title_size = title["size"]
    return title_text, title_size
