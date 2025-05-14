"""
PDF to Graph module (P2G) for extracting components, networks and metadata from
car architecture Visio PDF diagrams.
"""

import logging
from os.path import isfile
from typing import Annotated, Any, cast
from uuid import UUID, uuid4

import pymupdf
from numpy import median

from aranea.models.graph_model import Graph, NodeUnionType, get_default_text
from aranea.p2g.add_lin_connected_to_ecus import add_lin_connected_to_ecus
from aranea.p2g.ecu import get_ecus
from aranea.p2g.lines import get_networks
from aranea.p2g.obd import get_obd_connectors
from aranea.p2g.remove_ecus_from_key import remove_ecus_from_key
from aranea.p2g.title import get_title
from aranea.p2g.util import (REM, DictTextBlock, gendocstring,
                             take_annotation_from)
from aranea.p2g.xor import get_xor_nodes

logger = logging.getLogger(__name__)


@gendocstring
def calculate_rem(page: pymupdf.Page) -> REM:
    """
    Calculates the page's root element size by determining the median font size.
    """
    word_blocks = page.get_text("dict")["blocks"]  # pyright: ignore
    lines: list[dict[str, Any]] = [
        l for b in word_blocks if b.get("lines") for l in b["lines"]  # pyright: ignore
    ]
    text_sizes: list[float] = []
    for l in lines:
        text_sizes.extend([s.get("size") for s in l["spans"]])
    return float(median(text_sizes))  # pyright: ignore


@take_annotation_from(get_ecus, get_xor_nodes, get_obd_connectors, get_networks, get_title)
def parse_page(
    pdfpath: Annotated[str, "Path to the PDF file"],
    pagenumber: Annotated[int, "The page to parse"] = 0,
    rem: Annotated[float | None, "Optional Root Element Size"] = None,
    progress: Annotated[bool, "Enable printing progress bars"] = False,
    **kwargs: Any,
) -> Annotated[Graph, "A Graph representing all extracted information"]:
    """
    Tries to parse all necessary information from the PDF file.

    `**kwargs` captures the arguments for sub-functions. See `__doc__` for details.
    """

    if not isfile(pdfpath):
        raise IOError("Input is no file")
    with open(pdfpath, "rb") as inpf:
        if inpf.read(5) != b"%PDF-":
            raise IOError("Input is not a PDF file")
        doc = pymupdf.open(inpf, filetype="pdf")

    page: pymupdf.Page = doc.load_page(pagenumber)
    rem = rem or calculate_rem(page)

    word_blocks: list[DictTextBlock] = cast(
        list[DictTextBlock],
        page.get_text("dict")["blocks"],  # pyright: ignore
    )

    ecus = get_ecus(page, word_blocks, rem=rem, progress=progress, **kwargs)
    logger.info("Extracted %d ECUs", len(ecus))
    xors = get_xor_nodes(page, word_blocks=word_blocks, rem=rem, progress=progress, **kwargs)
    logger.info("Extracted %d XOR nodes", len(xors))
    obds = get_obd_connectors(page, word_blocks=word_blocks, rem=rem, progress=progress, **kwargs)
    logger.info("Extracted %d OBD connectors", len(obds))
    nodes: dict[UUID, NodeUnionType] = {uuid4(): node for node in ecus + xors + obds}
    networks, waypoints, text_nodes = get_networks(
        page, nodes=nodes, word_blocks=word_blocks, rem=rem, progress=progress, **kwargs
    )
    logger.info("Extracted %d networks", len(networks))
    logger.info("Created %d waypoints", len(waypoints))
    nodes.update(waypoints)
    nodes.update(text_nodes)
    nodes = remove_ecus_from_key(nodes, networks)
    nodes = add_lin_connected_to_ecus(nodes, networks)

    metadata = doc.metadata or {}  # pylint: disable=no-member
    title_str, title_size = get_title(page)
    title_str = title_str or metadata.get("title") or ""
    title = get_default_text(title_str, rem_factor=title_size / rem)
    logger.info('Extracted architecture title "%s"', title_str)

    return Graph(label=title, nodes=nodes, networks=networks)
