"""Module for the context class of CLI."""

import json
import logging
from pathlib import Path
from typing import Any

import click

from aranea.models.config_model import AraneaConfig
from cli.lib.toml_tools import aranea_config_available, parse_toml

logger: logging.Logger = logging.getLogger(__name__)

EPILOG: str = (
    "Docs: https://gitlab.uni-ulm.de/api/v4/projects/6351/jobs/artifacts/main/download?\
job=build-html"
)


class CliContext:
    """Configuration class containing configuration settings for other commands."""

    user_config: AraneaConfig

    def __init__(self, config_file_path: Path) -> None:
        """Constructor for the Config class.

        Checks if a config file exists and reads it if it does. If the config file or aranea
        section does not exist, the default configuration is used. If the config file exists
        and the aranea section is present, the default configuration is overwritten and
        validated with the user configuration.
        """

        if config_file_path.exists() and aranea_config_available(config_file_path):
            logger.info("Reading the config file: %s", str(config_file_path))
            config_file: dict[str, Any] = parse_toml(config_file_path)

            if "tool" in config_file and "aranea" in config_file["tool"]:
                logger.debug("Found an aranea config section in: %s", str(config_file_path))
                self.toml_config: dict[str, Any] = config_file["tool"]["aranea"]

                logger.debug("Start overwriting the default values with the user values.")
                self.user_config: AraneaConfig = AraneaConfig.model_validate(
                    self.merge_aranea_config_dicts(
                        json.loads(AraneaConfig().model_dump_json()),
                        self.toml_config,
                    )
                )

                return

            logger.info("No aranea config section found in: %s", str(config_file_path))

        else:
            logger.info("No config file found for: %s", str(config_file_path))

        logger.info("Using the default aranea configuration.")
        self.user_config = AraneaConfig()

    def merge_aranea_config_dicts(
        self, dict_a: dict[str, Any], dict_b: dict[str, Any]
    ) -> dict[str, Any]:
        """Merge two aranea config dictionaries.

        The dict_a is the base dictionary (the default config). If a key from dict_a is also in
        dict_b, the value of dict_b is used. New keys from dict_b will not be added to dict_a.
        The function returns a new dictionary. Nested dictionaries are also merged.

        For lists, the function tries to merge the elements of the list. If a list element has a
        "name" key, the function tries to find a matching element in the other list. If a match is
        found, the elements are merged. If no match is found, the element from the first list is
        used.

        :param dict_a: The base dictionary.
        :type dict_a: dict[str, Any]
        :param dict_b: The dictionary with the new values.
        :type dict_b: dict[str, Any]
        :return: The new merged dictionary.
        :rtype: dict[str, Any]
        """

        merged: dict[str, Any] = {}

        # Iterate over keys that exist in both dictionaries
        for first_level_key in dict_a.keys() & dict_b.keys():
            value_a = dict_a[first_level_key]
            value_b = dict_b[first_level_key]

            # If both values are dictionaries, merge them recursively
            if isinstance(value_a, dict) and isinstance(value_b, dict):
                merged[first_level_key] = self.merge_aranea_config_dicts(
                    value_a, value_b  # pyright: ignore
                )

            # If both values are lists, attempt to merge list elements
            elif isinstance(value_a, list) and isinstance(value_b, list):
                merged[first_level_key] = self.merge_aranea_config_lists(
                    value_a, value_b  # pyright: ignore
                )

            # Otherwise, take the value from dict_b
            else:
                merged[first_level_key] = value_b

        # Add keys that are only present in dict_a (they are unchanged)
        for first_level_key in dict_a.keys() - dict_b.keys():
            merged[first_level_key] = dict_a[first_level_key]

        return merged

    def merge_aranea_config_lists(self, list_a: list[Any], list_b: list[Any]) -> list[Any]:
        """Merge two aranea config lists.

        The function tries to merge the elements of the list, which have to be dicts.
        If a list element/dict has a "name" key, the function tries to find a matching element in
        the other list. If a match is found, the elements are merged. If no match is found, the
        element from the first list is used.

        :param list_a: The base list.
        :type list_a: list[Any]
        :param list_b: The list with the new values.
        :type list_b: list[Any]
        :return: The new merged list.
        :rtype: list[Any]
        """

        merged_list: list[Any] = []

        # Iterate through the first list
        for item_a in list_a:

            # Check if the item is a dictionary and has a name key
            if not isinstance(item_a, dict):
                logger.error("List item is not a dictionary: %s", str(item_a))
                raise ValueError("Not a valid aranea configuration!")
            if "name" not in item_a:
                logger.error("Item %s has no 'name' key!", str(item_a))  # pyright: ignore
                raise ValueError("Not a valid aranea configuration!")

            found_match: bool = False
            for item_b in list_b:

                # Check if the item is a dictionary and has a name key
                if not isinstance(item_b, dict):
                    logger.error("List item is not a dictionary: %s", str(item_b))
                    raise ValueError("Not a valid aranea configuration!")
                if "name" not in item_b:
                    logger.warning("Item %s has no 'name' key!", str(item_b))  # pyright: ignore
                    logger.warning("Skipping this item.")
                    continue

                if item_a["name"] == item_b["name"]:
                    merged_list.append(
                        self.merge_aranea_config_dicts(item_a, item_b)  # pyright: ignore
                    )
                    found_match = True
                    break
            if not found_match:
                merged_list.append(item_a)

        return merged_list

    def print_default_aranea_config(self) -> None:
        """Prints the default configuration of aranea to the terminal."""
        click.secho("The default configuration of aranea is:")
        click.secho(json.dumps(json.loads(AraneaConfig().model_dump_json()), indent=4))

    def print_current_aranea_config(self) -> None:
        """Prints the current configuration of aranea to the terminal.

        This configuration was loaded from the config file and will be now used for aranea.
        """
        click.secho("Aranea is currently using this configuration:")
        click.secho(json.dumps(json.loads(self.user_config.model_dump_json()), indent=4))
