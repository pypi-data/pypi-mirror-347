"""CLI module for creating a configuration file for aranea."""

import json
import logging
from pathlib import Path
from typing import Any

import click

from aranea.models.config_model import AraneaConfig
from cli.lib.cli_context import EPILOG, CliContext
from cli.lib.toml_tools import parse_toml, write_toml

logger: logging.Logger = logging.getLogger(__name__)


@click.command(epilog=EPILOG)
@click.argument(
    "new_config_file_path",
    nargs=1,
    required=True,
    type=click.Path(
        dir_okay=False,
        resolve_path=True,
        path_type=Path,
    ),
)
@click.option(
    "--overwrite/--no-overwrite",
    "overwrite",
    is_flag=True,
    show_default=True,
    default=False,
    required=False,
    type=bool,
    help="If set, the configuration section in the provided file will be overwritten if it already \
exists.",
)
@click.pass_obj
def create_config(ctx: CliContext, new_config_file_path: Path, overwrite: bool) -> None:
    """Default configuration file creation for aranea.

    Creates an initial configuration section for aranea in the CONFIG_FILE_PATH with all default
    values.

    Aranea checks for the existence of the CONFIG_FILE_PATH file and creates a new one if it does
    not exist. The config file needs to be a TOML file.
    """

    logger.debug("---Starting the create-config command---")

    if new_config_file_path.suffix != ".toml":
        logger.info("The suffix '%s' is not '.toml'.", new_config_file_path.suffix)
        new_config_file_path = new_config_file_path.with_suffix(".toml")
        logger.info("Changed the suffix to '.toml'.")

    if new_config_file_path.is_file():
        logger.debug("%s already exists.", new_config_file_path)
        existing_config: dict[str, Any] = parse_toml(new_config_file_path)

        if "tool" in existing_config and "aranea" in existing_config["tool"]:
            logger.debug("An aranea configuration section already exists.")

            if not overwrite:
                logger.warning("Will not overwrite the existing configuration!")
            else:
                existing_config["tool"]["aranea"] = json.loads(AraneaConfig().model_dump_json())
                logger.info("Old aranea configuration was deleted!")
                write_toml(new_config_file_path, existing_config)
                logger.info("New default aranea configuration was written!")

        else:
            logger.info("No existing aranea configuration found.")
            existing_config["tool"]["aranea"] = json.loads(AraneaConfig().model_dump_json())
            write_toml(new_config_file_path, existing_config)
            logger.info("New default aranea configuration added.")

    else:
        Path(new_config_file_path).touch()
        logger.info("Created a new configuration file: %s", new_config_file_path)
        write_toml(
            new_config_file_path,
            {"tool": {"aranea": json.loads(AraneaConfig().model_dump_json())}},
        )
