"""CLI module for executing p2g and g2d."""

import logging
from pathlib import Path

import click

from aranea.models.graph_model import AttackPathGraph, Graph, GraphCollection
from aranea.p2g import parse_page
from cli.lib.cli_context import EPILOG, CliContext
from cli.lib.export import export_options, export_outputs

logger: logging.Logger = logging.getLogger(__name__)


@click.command(epilog=EPILOG)
@click.argument(
    "architecture_pdf_path",
    nargs=1,
    required=True,
    type=click.Path(
        exists=True,
        file_okay=True,
        dir_okay=False,
        readable=True,
        resolve_path=True,
        path_type=Path,
    ),
)
@click.option(
    "--progress/--no-progress",
    "progress",
    is_flag=True,
    default=True,
    show_default=True,
    required=False,
    type=bool,
    help="If set, progress bars get displayed.",
)
@export_options
@click.pass_obj
def run(
    ctx: CliContext,
    architecture_pdf_path: Path,
    output_file_name: str,
    json_file: bool,
    drawio_file: bool,
    export_format: str | None,
    page_index: int,
    progress: bool,
) -> None:
    """Detect an architecture of a PDF file.

    Run aranea to detect an architecture on a given PDF file."""

    logger.debug("---Starting the run command---")

    logger.debug("Starting the parsing process of the PDF file.")
    graph: Graph = parse_page(
        pdfpath=str(architecture_pdf_path),
        progress=progress,
        ecu_min_height=ctx.user_config.p2g["ecu_min_height"],
        ecu_max_height=ctx.user_config.p2g["ecu_max_height"],
        xor_min_height=ctx.user_config.p2g["xor_min_height"],
        obd_min_height=ctx.user_config.p2g["obd_min_height"],
        obd_max_height=ctx.user_config.p2g["obd_max_height"],
        obd_min_width=ctx.user_config.p2g["obd_min_width"],
        obd_max_width=ctx.user_config.p2g["obd_max_width"],
        obd_color=ctx.user_config.p2g["obd_color"],
    )
    graph_collection: GraphCollection[Graph | AttackPathGraph] = GraphCollection(graphs=[graph])

    export_outputs(
        ctx=ctx,
        graph_collection=graph_collection,
        output_file_name=output_file_name,
        json_file=json_file,
        drawio_file=drawio_file,
        export_format=export_format,
        page_index=page_index,
    )
