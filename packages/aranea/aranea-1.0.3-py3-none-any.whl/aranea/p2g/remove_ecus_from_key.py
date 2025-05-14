"""
Module to remove ECUs from the key of the diagram.
"""

from uuid import UUID

from typing_extensions import Annotated

from aranea.models.graph_model import Network, NodeType, NodeUnionType
from aranea.p2g.util import gendocstring


@gendocstring
def remove_ecus_from_key(
    nodes: Annotated[dict[UUID, NodeUnionType], "Dict of uuid and node"],
    networks: Annotated[list[Network], "The extracted networks."],
) -> Annotated[dict[UUID, NodeUnionType], "Dict of uuid and node"]:
    """
    Removes all ComponentNodes that are part of the key diagram.
    """
    nodes_to_remove: set[UUID] = {
        node_id
        for node_id, node in nodes.items()
        if node.type == NodeType.COMPONENT
        and not any(
            node_id in {edge.sourceId, edge.targetId}
            for network in networks
            for edge in network.edges
        )
    }

    for node_id in nodes_to_remove:
        del nodes[node_id]

    return nodes
