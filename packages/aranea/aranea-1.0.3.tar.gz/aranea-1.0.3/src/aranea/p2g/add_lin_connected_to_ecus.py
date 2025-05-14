"""
Module for adding LIN connected to ECUs.
"""

import logging
from uuid import UUID

from typing_extensions import Annotated

from aranea.models.graph_model import (ComponentNode, EcuClassification,
                                       EcuClassificationName, Network,
                                       NodeUnionType, ProtocolTypeName)
from aranea.p2g.util import gendocstring

logger = logging.getLogger(__file__)


@gendocstring
def add_lin_connected_to_ecus(
    nodes: Annotated[dict[UUID, NodeUnionType], "Dict of uuid and node"],
    networks: Annotated[list[Network], "The extracted networks."],
) -> Annotated[dict[UUID, NodeUnionType], "Dict of uuid and node"]:
    """
    Adds LIN connected to ECUs.
    """

    for network in networks:
        if network.protocol_type.name == ProtocolTypeName.LIN:
            for edge in network.edges:
                source_node = nodes[edge.sourceId]
                target_node = nodes[edge.targetId]

                if isinstance(source_node, ComponentNode):
                    source_node.classifications.add(
                        EcuClassification(name=EcuClassificationName.LIN_CONNECTED_ECU)
                    )

                if isinstance(target_node, ComponentNode):
                    target_node.classifications.add(
                        EcuClassification(name=EcuClassificationName.LIN_CONNECTED_ECU)
                    )

    return nodes
