"""CLI module for creating a DrawIO file from a aranea GraphCollection JSON file."""

import logging
from pathlib import Path

import click

from aranea.models.graph_model import AttackPathGraph, Graph, GraphCollection
from cli.lib.cli_context import EPILOG, CliContext
from cli.lib.export import export_options, export_outputs

logger: logging.Logger = logging.getLogger(__name__)


@click.command(epilog=EPILOG)
@click.argument(
    "graph_collection_json",
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
@export_options
@click.pass_obj
def json_to_drawio(
    ctx: CliContext,
    graph_collection_json: Path,
    output_file_name: str,
    json_file: bool,
    drawio_file: bool,
    export_format: str | None,
    page_index: int,
) -> None:
    """Create a DrawIO file from a ``GraphCollection``.

    The provided JSON file must be a valid aranea ``GraphCollection``.
    """

    logger.debug("---Starting the json-to-drawio command---")

    with open(graph_collection_json, "r", encoding="UTF-8") as f:
        graph_collection: GraphCollection[Graph | AttackPathGraph] = (
            GraphCollection.model_validate_json(f.read())
        )

    export_outputs(
        ctx=ctx,
        graph_collection=graph_collection,
        output_file_name=output_file_name,
        json_file=json_file,
        drawio_file=drawio_file,
        export_format=export_format,
        page_index=page_index,
    )
