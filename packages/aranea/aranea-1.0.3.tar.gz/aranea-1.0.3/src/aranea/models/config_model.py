"""This module contains the configuration models for the aranea CLI."""

import shutil
from typing import Annotated, Any

from pydantic import BaseModel, ConfigDict, Field

from aranea.g2d.style_configs.get_default_style_config import \
    get_default_style_config
from aranea.models.graph_model import (EcuClassification,
                                       EcuClassificationName, ProtocolType,
                                       ProtocolTypeName, TechnicalCapability,
                                       TechnicalCapabilityName)
from aranea.models.style_config_model import StyleConfig
from aranea.p2g import parse_page


def get_default_technical_capabilities() -> list[TechnicalCapability]:
    """Returns a list of all valid technical capabilities with there default values.

    :return: List of all valid technical capabilities with there default values.
    :rtype: list[TechnicalCapability]
    """
    technical_capabilities: list[TechnicalCapability] = []

    for capability in TechnicalCapabilityName:
        technical_capabilities.append(TechnicalCapability(name=capability))

    return technical_capabilities


def get_default_ecu_classifications() -> list[EcuClassification]:
    """Returns a list of all valid ecu classifications with there default values.

    :return: List of all valid ecu classifications with there default values.
    :rtype: list[EcuClassification]
    """
    ecu_classifications: list[EcuClassification] = []

    for classification in EcuClassificationName:
        ecu_classifications.append(EcuClassification(name=classification))

    return ecu_classifications


def get_default_protocol_types() -> list[ProtocolType]:
    """Returns a list of all valid protocol types with there default values.

    :return: List of all valid protocol types with there default values.
    :rtype: list[ProtocolType]
    """
    protocol_types: list[ProtocolType] = []

    for protocol_type_name in ProtocolTypeName:
        protocol_types.append(ProtocolType(name=protocol_type_name))

    return protocol_types


class GeConfig(BaseModel):
    """Defines the configuration model for the graph enricher."""

    model_config = ConfigDict(extra="forbid", title="Graph enricher configuration.")

    technical_capabilities: list[TechnicalCapability] = get_default_technical_capabilities()
    ecu_classifications: list[EcuClassification] = get_default_ecu_classifications()
    protocol_types: list[ProtocolType] = get_default_protocol_types()


class ApgConfig(BaseModel):
    """Defines the configuration model for the attack path generator."""

    model_config = ConfigDict(extra="forbid", title="Attack path generator configuration.")

    initial_x: float = 30
    initial_y: float = 30
    margin_x: float = 30
    margin_y: float = 30


class AraneaConfig(BaseModel):
    """The global aranea configuration model which contains all configuration options
    This model is used by the aranea CLI and represents the config file.
    """

    model_config = ConfigDict(extra="forbid", title="Global aranea configuration.")

    output_dir: str = "./"
    drawio_path: str = shutil.which("drawio") or "/path/to/draw.io"
    log_level: Annotated[
        str,
        Field(
            pattern=r"^(NOTSET|DEBUG|INFO|WARNING|ERROR|CRITICAL)$",
            description="Set the log level regarding to the python logging module.",
        ),
    ] = "DEBUG"
    p2g: dict[str, Any] = parse_page.__kwdefaults__
    g2d: StyleConfig = get_default_style_config()
    ge: GeConfig = GeConfig()
    apg: ApgConfig = ApgConfig()
