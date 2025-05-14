"""This module contains functions to parse and write TOML files."""

from pathlib import Path
from typing import Any, cast

import tomli
import tomli_w


def parse_toml(toml_path: Path | str) -> dict[str, Any]:
    """
    Parse a TOML file and return the content as a dictionary.

    :param toml_path: Path to the TOML file
    :type toml_path: Path | str
    :return: The content of the TOML file as a dictionary
    :rtype: dict
    """
    with open(toml_path, "rb") as f:
        toml: dict[str, Any] = tomli.load(f)
    return toml


def write_toml(toml_path: Path, toml: dict[str, Any]) -> None:
    """Write a dictionary to a TOML file.

    :param toml_path: Path to the TOML file
    :type toml_path: Path
    :param toml: Dictionary to write
    :type toml: dict
    """
    cleaned_toml = remove_none_entries(toml)
    with open(toml_path, "wb") as f:
        tomli_w.dump(cleaned_toml, f)


def aranea_config_available(toml_path: Path) -> bool:
    """Checks if a aranea section is available in the config file.

    :param toml_path: Path to the TOML file
    :type toml_path: str
    :return: True if aranea section is available
    :rtype: bool
    """
    with open(toml_path, "rb") as f:
        toml: dict[str, Any] = tomli.load(f)
    return "tool" in toml and "aranea" in toml["tool"]


def remove_none_entries(data: dict[str, Any]) -> dict[str, Any]:
    """
    Remove None entries from a dictionary.

    :param data: Dictionary to clean
    :return: Cleaned dictionary
    """

    cleaned_data: dict[str, Any] = {}
    for key, value in data.items():
        if value is None:
            continue
        if isinstance(value, dict):
            cleaned_nested = remove_none_entries(cast(dict[str, Any], value))
            if cleaned_nested:
                cleaned_data[key] = cleaned_nested
        else:
            cleaned_data[key] = value
    return cleaned_data
