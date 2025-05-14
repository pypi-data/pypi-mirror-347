"""CLI module for enriching an GraphCollection JSON file with data from an Excel file."""

import logging
from pathlib import Path

import click

from aranea.ge.graph_collection_enricher import GraphCollectionEnricher
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
@click.argument(
    "excel_path",
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
def ge(
    ctx: CliContext,
    graph_collection_json: Path,
    excel_path: Path,
    output_file_name: str,
    json_file: bool,
    drawio_file: bool,
    export_format: str | None,
    page_index: int,
) -> None:
    """Enrich a GraphCollection with additional data.

    Creates an enriched ``GraphCollection`` from an existing ``GraphCollection``
    JSON file. The attributes from the excel file and the ratings from the config file
    will be added to every ``Graph`` in the ``GraphCollection``.

    The provided JSON file must be a valid aranea ``GraphCollection``.
    The required layout of the excel file is documented in the user guide.
    """

    logger.debug("---Starting the ge command---")

    with open(graph_collection_json, "r", encoding="UTF-8") as f:
        graph_collection: GraphCollection[Graph | AttackPathGraph] = (
            GraphCollection.model_validate_json(f.read())
        )

    enricher: GraphCollectionEnricher = GraphCollectionEnricher(graph_collection)
    enricher.enrich(excel_path, ctx.user_config.ge)

    export_outputs(
        ctx=ctx,
        graph_collection=graph_collection,
        output_file_name=output_file_name,
        json_file=json_file,
        drawio_file=drawio_file,
        export_format=export_format,
        page_index=page_index,
    )

    logger.debug("---Finished the ge command---")
