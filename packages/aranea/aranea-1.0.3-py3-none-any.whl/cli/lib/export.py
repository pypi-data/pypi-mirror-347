"""Module for export utilities in the CLI."""

import logging
import os
from typing import Any, Callable

import click

from aranea.models.graph_model import AttackPathGraph, Graph, GraphCollection
from cli.lib.cli_context import CliContext
from cli.lib.utils import (export_drawio_file, graph_collection_to_drawio_file,
                           graph_collection_to_json_file)

logger: logging.Logger = logging.getLogger(__name__)


def export_options(function: Callable[..., Any]) -> Callable[..., Any]:
    """A decorator for the click options to export the outputs."""
    function = click.option(
        "-n",
        "--output-file-name",
        "output_file_name",
        default="aranea_result",
        show_default=True,
        type=str,
        help="You can specify a custom name for the output files/artifacts. Note: The output\
 directory is specified in another option. The required suffix is added automatically.",
    )(function)
    function = click.option(
        "--json-file/--no-json-file",
        "json_file",
        is_flag=True,
        default=True,
        show_default=True,
        required=False,
        type=bool,
        help="If set, a JSON file (GraphCollection[Graph | AttackPathGraph]) will be created for\
the generated result and will be saved in the output folder.",
    )(function)
    function = click.option(
        "--drawio-file/--no-drawio-file",
        "drawio_file",
        is_flag=True,
        default=True,
        show_default=True,
        required=False,
        type=bool,
        help="If set, a DrawIO file will be created for the generated result and will be saved in\
 the output folder.",
    )(function)

    function = click.option(
        "-f",
        "--export-format",
        "export_format",
        show_default=True,
        required=False,
        type=click.Choice(["pdf", "png", "jpg", "svg", "vsdx", "xml"], case_sensitive=False),
        help="If set, the generated DrawIO file is exported to the specified format. The export\
 will be disabled if the drawio_path is not set or the '--no-drawio-file' flag is set.\
 If you are using ``--export-format`` under Linux and EUID is 0 (root), drawio will be\
 run with ``--no-sandbox``. If the environment variable ``CI`` is also set to ``true`` it will\
 be run with ``xvfb-run``. This requires that ``xvfb`` is installed on the system.",
    )(function)
    function = click.option(
        "-p",
        "--page-index",
        "page_index",
        default=0,
        show_default=True,
        required=False,
        type=int,
        help="You can specify which page of the generated DrawIO file should be exported. Start\
 counting at 0. The export will be disabled if the drawio_path is not set or the '--no-drawio-file'\
 flag is set.",
    )(function)
    return function


def export_outputs(
    ctx: CliContext,
    graph_collection: GraphCollection[Graph | AttackPathGraph],
    output_file_name: str,
    json_file: bool,
    drawio_file: bool,
    export_format: str | None,
    page_index: int,
) -> None:
    """
    Exports the given graph collection to JSON and DrawIO files.

    :param ctx: The CLI context.
    :type ctx: CliContext
    :param graph_collection: The graph collection to export.
    :type graph_collection: GraphCollection[Graph | AttackPathGraph]
    :param output_file_name: The name of the output files.
    :type output_file_name: str
    :param json_file: If set, a JSON file will be created.
    :type json_file: bool
    :param drawio_file: If set, a DrawIO file will be created.
    :type drawio_file: bool
    :param export_format: The format to export the DrawIO file to.
    :type export_format: str | None
    :param page_index: The page index to export.
    :type page_index: int
    """

    output_dir: str = ctx.user_config.output_dir

    if json_file:
        json_file_path: str = os.path.join(output_dir, output_file_name + ".json")
        graph_collection_to_json_file(graph_collection, json_file_path)

    if drawio_file:
        drawio_file_path: str = os.path.join(output_dir, output_file_name + ".drawio")
        graph_collection_to_drawio_file(graph_collection, ctx.user_config.g2d, drawio_file_path)

        if export_format:
            export_drawio_file(
                drawio_path=ctx.user_config.drawio_path,
                drawio_file_path=drawio_file_path,
                page_index=page_index,
                export_format=export_format,
                output_dir=ctx.user_config.output_dir,
                output_file_name=output_file_name,
            )
