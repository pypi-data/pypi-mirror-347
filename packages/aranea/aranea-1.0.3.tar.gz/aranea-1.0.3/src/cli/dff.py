"""CLI module for generating a diff between two architectures."""

import logging
from pathlib import Path
from typing import Optional

import click

from aranea.dff.build_diff_graph import build_diff_graph
from aranea.dff.export_dff_excel import export_dff_excel
from aranea.dff.get_graph_diff import GraphDiffResult, get_graph_diff
from aranea.models.graph_model import Graph, GraphCollection
from cli.lib.cli_context import EPILOG, CliContext
from cli.lib.export import export_options, export_outputs
from cli.lib.utils import check_valid_graph_index

logger: logging.Logger = logging.getLogger(__name__)


@click.command(epilog=EPILOG)
@click.argument(
    "graph_collection_1_json",
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
    "--graph-1-number",
    "graph_1_number",
    default=0,
    show_default=True,
    required=False,
    type=int,
    help="Defines the graph number of the first GraphCollection to use for the diffing.\
 Start counting from 0.",
)
@click.argument(
    "graph_collection_2_json",
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
    "--graph-2-number",
    "graph_2_number",
    default=0,
    show_default=True,
    required=False,
    type=int,
    help="Defines the graph number of the second GraphCollection to use for the diffing.\
 Start counting from 0.",
)
@click.option(
    "--dff-excel/--no-dff-excel",
    "dff_excel",
    is_flag=True,
    default=True,
    show_default=True,
    required=False,
    type=bool,
    help="If set, the results of the diffing will be exported to an Excel file.",
)
@export_options
@click.pass_obj
def dff(
    ctx: CliContext,
    graph_collection_1_json: Path,
    graph_1_number: int,
    graph_collection_2_json: Path,
    graph_2_number: int,
    dff_excel: bool,
    output_file_name: str,
    json_file: bool,
    drawio_file: bool,
    export_format: str | None,
    page_index: int,
) -> None:
    """Show the differences between two ``Graph``.

    Creates a ``GraphCollection`` that shows the differences between two ``Graph``.
    You need to specify which ``Graph`` from the ``GraphCollection`` you want to use for the
    diffing. Default is the first item (0) of the ``graphs`` list of the ``GraphCollection``.
    The provided JSON file must be a valid aranea ``GraphCollection``.

    The graph_1 is the graph which is to be considered as update of graph_2. (graph_1 = new,
    graph_2 = old). In the DrawIO output the first page contains the diff graph, the second page the
    graph from the first GraphCollection and the third page the graph from the second
    GraphCollection.
    """

    logger.debug("---Starting the dff command---")

    if not any([drawio_file, json_file, dff_excel]):
        logger.warning("If no output is set, aranea dff will not do anything.")
        return

    with open(graph_collection_1_json, "r", encoding="UTF-8") as f:
        graph_collection_1: GraphCollection[Graph] = GraphCollection.model_validate_json(f.read())
    check_valid_graph_index(graph_collection_1, graph_1_number)

    with open(graph_collection_2_json, "r", encoding="UTF-8") as f:
        graph_collection_2: GraphCollection[Graph] = GraphCollection.model_validate_json(f.read())
    check_valid_graph_index(graph_collection_2, graph_2_number)

    diff_result: GraphDiffResult = get_graph_diff(
        graph_collection_1.graphs[graph_1_number], graph_collection_2.graphs[graph_2_number]
    )

    if drawio_file:
        logger.debug("---Starting the generation of dff graph ---")
        diff_graph: Optional[Graph] = build_diff_graph(
            graph_collection_1.graphs[graph_1_number],
            graph_collection_2.graphs[graph_2_number],
            diff_result,
        )
        if diff_graph:
            result: GraphCollection[Graph] = GraphCollection(
                graphs=[
                    diff_graph,
                    graph_collection_1.graphs[graph_1_number],
                    graph_collection_2.graphs[graph_2_number],
                ]
            )

            export_outputs(
                ctx=ctx,
                graph_collection=result,
                output_file_name=output_file_name,
                json_file=json_file,
                drawio_file=drawio_file,
                export_format=export_format,
                page_index=page_index,
            )
        else:
            logger.warning("No differences found between the two graphs.")
            logger.warning("No output produced!")
        logger.debug("---Finished the generation of dff graph ---")

    if dff_excel:
        export_dff_excel(
            diff_result,
            graph_collection_1.graphs[graph_1_number],
            graph_collection_2.graphs[graph_2_number],
            ctx.user_config.output_dir,
            output_file_name,
        )

    logger.debug("---Finished the dff command---")
