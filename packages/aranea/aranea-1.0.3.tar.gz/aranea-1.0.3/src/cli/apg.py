"""CLI module for generating attack paths for a provided architecture."""

import logging
import os
from pathlib import Path

import click
import pandas as pd
from rich import print as rich_print
from rich.table import Table

from aranea.apg import (apg_collection_to_statistics_df,
                        attack_path_collection_to_xsl_data_frame,
                        get_attack_paths)
from aranea.models.graph_model import AttackPathGraph, Graph, GraphCollection
from cli.lib.cli_context import EPILOG, CliContext
from cli.lib.export import export_options, export_outputs
from cli.lib.utils import check_valid_graph_index

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
@click.option(
    "-g",
    "--graph-number",
    "graph_number",
    default=0,
    show_default=True,
    required=False,
    type=int,
    help="Defines the graph number from the GraphCollection to generate the attack paths from.\
 Start counting from 0.",
)
@click.option(
    "--apg-table/--no-apg-table",
    "apg_table",
    is_flag=True,
    default=True,
    show_default=True,
    required=False,
    type=bool,
    help="If set, the results of the attack path generation will be printed to the terminal.\
 Up to 200 rows will be printed, adjusted to your current terminal size.",
)
@click.option(
    "--apg-excel/--no-apg-excel",
    "apg_excel",
    is_flag=True,
    default=True,
    show_default=True,
    required=False,
    type=bool,
    help="If set, the results of the attack path generation will be exported to an Excel file.",
)
@click.option(
    "--apg-excel-stats/--no-apg-excel-stats",
    "apg_excel_stats",
    is_flag=True,
    default=True,
    show_default=True,
    required=False,
    type=bool,
    help="If set, statistics about the attack paths gets exported to an Excel file.",
)
@export_options
@click.pass_obj
def apg(
    ctx: CliContext,
    graph_collection_json: Path,
    graph_number: int,
    apg_table: bool,
    apg_excel: bool,
    apg_excel_stats: bool,
    output_file_name: str,
    json_file: bool,
    drawio_file: bool,
    export_format: str | None,
    page_index: int,
) -> None:
    """Attack path generation for a provided ``Graph``.

    Creates a ``GraphCollection`` with several ``AttackPathGraph`` from an existing
    ``GraphCollection`` JSON file. You need to specify which ``Graph`` from the ``GraphCollection``
    you want to generate the attack paths from. Default is the first item (0) of the ``graphs``
    list of the ``GraphCollection``.

    The provided JSON file must be a valid aranea ``GraphCollection``.
    """

    logger.debug("---Starting the apg command---")

    with open(graph_collection_json, "r", encoding="UTF-8") as f:
        graph_collection: GraphCollection[Graph | AttackPathGraph] = (
            GraphCollection.model_validate_json(f.read())
        )

    check_valid_graph_index(graph_collection, graph_number)

    result: GraphCollection[AttackPathGraph] = get_attack_paths(
        graph_collection.graphs[graph_number],
        (
            ctx.user_config.apg.initial_x,
            ctx.user_config.apg.initial_y,
            ctx.user_config.apg.margin_x,
            ctx.user_config.apg.margin_y,
        ),
    )

    export_outputs(
        ctx=ctx,
        graph_collection=result,  # pyright: ignore
        output_file_name=output_file_name,
        json_file=json_file,
        drawio_file=drawio_file,
        export_format=export_format,
        page_index=page_index,
    )
    export_apg_table(ctx, result, output_file_name, apg_table, apg_excel, apg_excel_stats)

    logger.debug("---Finished the apg command---")


def export_apg_table(
    ctx: CliContext,
    graph_collection: GraphCollection[AttackPathGraph],
    output_file_name: str,
    terminal_output: bool,
    excel_file: bool,
    excel_stats_file: bool,
) -> None:
    """
    Can print the results of the attack path generation to the terminal (max 200 rows) or export
    them to an Excel file.

    :param ctx: The CLI context.
    :type ctx: CliContext
    :param graph_collection: The graph collection to export.
    :type graph_collection: GraphCollection[AttackPathGraph]
    :param output_file_name: The name of the output file.
    :type output_file_name: str
    :param terminal_output: If set, the results will be printed to the terminal.
    :type terminal_output: bool
    :param excel_file: If set, the results will be exported to an Excel file.
    :type excel_file: bool
    """
    if not any([terminal_output, excel_file]):
        return

    df_apg: pd.DataFrame = attack_path_collection_to_xsl_data_frame(graph_collection)

    if terminal_output:
        pd.set_option("display.max_rows", df_apg.shape[0])
        click.secho("The following attack paths were generated.")
        table = Table()
        for col in df_apg.columns:
            table.add_column(col, justify="left", style="cyan", no_wrap=False)
        for _, row in df_apg.iterrows():  # pyright: ignore
            table.add_row(
                *[str(v) for v in row],  # pyright: ignore
            )
            table.add_section()

        rich_print(table)

    if excel_file:
        excel_file_path: str = os.path.join(ctx.user_config.output_dir, output_file_name + ".xlsx")
        df_apg.to_excel(  # pyright: ignore
            excel_writer=excel_file_path,
            sheet_name="APG Results",
            engine="openpyxl",
        )
        logger.debug("The results were saved to: %s", excel_file_path)

    if excel_stats_file:
        ap_df = apg_collection_to_statistics_df(graph_collection)

        excel_file_path: str = os.path.join(
            ctx.user_config.output_dir, output_file_name + "_stats.xlsx"
        )
        writer = pd.ExcelWriter(excel_file_path, engine="xlsxwriter")
        ap_df.to_excel(  # pyright: ignore
            excel_writer=writer,
            sheet_name="Sheet1",
        )
        worksheet = writer.sheets["Sheet1"]
        max_row, max_col = ap_df.shape
        worksheet.conditional_format(2, 1, max_row, max_col, {"type": "3_color_scale"})
        writer.close()
        logger.debug("Wrote APG statistics to %s", excel_file_path)
