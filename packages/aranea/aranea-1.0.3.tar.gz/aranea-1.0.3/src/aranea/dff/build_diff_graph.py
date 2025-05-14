"""
Module for building a graph conforming to the pydantic model, containing the result of 
get_graph_diff.
"""

import logging
from typing import Optional
from uuid import UUID, uuid4

from aranea.dff.get_graph_diff import GraphDiffResult, NetworkComponentChanges
from aranea.dff.node_placer import NodePlacer
from aranea.dff.utils import (compare_networks, count_node_references_in_graph,
                              get_components_from_network,
                              get_graph_boundaries, get_network_name)
from aranea.models.graph_model import (ComponentNode, EcuClassification,
                                       EcuClassificationName, Edge, Graph,
                                       Network, NetworkDFFClassification,
                                       NodeUnionType, RemFactor, XorNode,
                                       get_default_text)

logger = logging.getLogger(__name__)


def process_added_networks(result_graph: Graph, added_networks: list[Network]) -> None:
    """
    In-place function that processes the added networks the given result graph.
    This is done by marking them as new.
    Components which are only connected to new networks also get marked as new.

    :param result_graph: The graph in which the added networks shall be marked as new
    :type result_graph: Graph
    :param added_networks: Networks that were added to result_graph when compared to the old graph
    :type added_networks: list[Network]

    :rtype: None
    """
    # Catch empty list of added networks
    if not added_networks:
        return

    added_components: set[ComponentNode] = set()  # for logging

    logger.info("build_diff_graph: Processing %d added networks", len(added_networks))
    logger.debug('Networks classified as "added":')

    for i, added_network in enumerate(added_networks):
        # Find matching network in result_graph
        network_name = get_network_name(added_network)
        network_name = "Unknown" if network_name is None else network_name
        matched = False
        for nw in result_graph.networks:
            if nw == added_network:
                nw.dff_classification = NetworkDFFClassification.NEW_NW
                matched = True
                logger.debug(
                    'Network "%s" containing %d component nodes',
                    network_name,
                    len(get_components_from_network(added_network, result_graph)),
                )
                break
        if not matched:
            raise ValueError(
                f"Network with index {i} and edge text {network_name} in added_networks is not in "
                "the graph associated with NodePlacer"
            )

    # mark components in added_components that are only part of added_networks as new
    for node_id, node in result_graph.nodes.items():
        if isinstance(node, ComponentNode):
            # Find all networks connected to this node.
            connected_networks = [
                network
                for network in result_graph.networks
                if any(node_id in (edge.sourceId, edge.targetId) for edge in network.edges)
            ]
            # If the node is connected to at least one network, and all of those networks are new...
            if connected_networks and all(
                network.dff_classification == NetworkDFFClassification.NEW_NW
                for network in connected_networks
            ):
                # Mark the component as new by adding a new ECU classification.
                node.classifications.add(EcuClassification(name=EcuClassificationName.NEW_ECU))
                added_components.add(node)

    logger.info("Classified %d components as new", len(added_components))
    logger.debug('Components classified as "added":')
    for added_component in added_components:
        logger.debug(
            'Component node "%s"',
            added_component.innerText[0] if added_component.innerText else "Unknown",
        )


def process_changed_networks(
    result_graph: Graph, network_component_changes: list[NetworkComponentChanges]
) -> None:
    """
    In-place function that marks added components as new in networks of the result_graph
    and adds removed components to the network they were removed from in the result_graph.
    The removed components are marked as removed.

    :param result_graph: The graph in which the network changes occurred
    :type result_graph: Graph
    :param network_component_changes: Added and removed components with their respective network
    :type network_component_changes: NetworkComponentChanges

    :rtype: None
    """
    # Catch empty list of network component changes
    if not network_component_changes:
        return

    logger.info("build_diff_graph: Processing %d changed networks", len(network_component_changes))

    node_placer = NodePlacer(result_graph)
    new_node_occurrences: dict[UUID, int] = {}
    removed_components: set[ComponentNode] = set()  # for logging

    for i, network_changes in enumerate(network_component_changes):
        network_name = get_network_name(network_changes["changed_network"])
        network_name = "Unknown" if network_name is None else network_name
        logger.debug(
            'Processing network "%s", containing %d component nodes',
            network_name,
            len(get_components_from_network(network_changes["changed_network"], result_graph))
            + len(network_changes["removed_components"]),
        )

        # get the network of the graph that corresponds to the one in NetworkComponentChanges
        # this is necessary as the network in NetworkComponentChanges is only a copy and changing
        # it doesn't change the network in the result_graph
        internal_network = None
        for network in node_placer.graph.networks:
            if compare_networks(network, network_changes["changed_network"]):
                internal_network = network
                break

        if internal_network is None:
            raise ValueError(
                f"Network with index {i} and edge text {network_name} in NetworkComponentChanges "
                "is not in the graph associated with NodePlacer"
            )

        # added components
        logger.debug("Added components:")
        for added_component_id in network_changes["added_components"]:
            node = result_graph.nodes.get(added_component_id)
            if isinstance(node, ComponentNode):
                logger.debug(
                    'Component node "%s"', node.innerText[0] if node.innerText else "Unknown"
                )
                node.classifications.add(EcuClassification(name=EcuClassificationName.NEW_ECU))
                # count occurrences of added component
                # these have to match the number of occurrences in graph to be considered as new
                # if they do not, the component might not be new and a warning should be displayed
                if added_component_id not in new_node_occurrences:
                    new_node_occurrences[added_component_id] = 1
                else:
                    new_node_occurrences[added_component_id] += 1
            else:
                raise ValueError(
                    f"Node with ID {added_component_id} is not a ComponentNode. "
                    "Something went seriously wrong."
                )
        # removed components
        logger.debug("Removed components:")
        for removed_component in network_changes["removed_components"]:
            removed_components.add(removed_component)
            logger.debug(
                'Component node "%s"',
                removed_component.innerText[0] if removed_component.innerText else "Unknown",
            )
            # Objects in graph_diff_result are deepcopies of the originals, so we can modify them
            removed_component.classifications.add(
                EcuClassification(name=EcuClassificationName.ECU_ONLY_IN_BR)
            )
            node_placer.add_component_to_network(internal_network, removed_component)

    # compare occurrences of each component in new_node_occurrences to
    # number of references in result_graph: They should be the same if matching went right
    # if they aren't  the same, the component might not be new -> warning
    # (Wrong matching can occur even if get_graph_diff runs without errors as sometimes information
    # is missing)
    for node_id, count in new_node_occurrences.items():
        if count != count_node_references_in_graph(node_id, result_graph):
            if not isinstance(result_graph.nodes[node_id], ComponentNode):
                raise ValueError(
                    f"Node with ID {node_id} is not a ComponentNode. "
                    "Something went seriously wrong."
                )

            node = result_graph.nodes[node_id]
            inner_text = "Unknown"
            if node.innerText is not None:  # type: ignore - node is a ComponentNode
                inner_text = node.innerText[0]  # type: ignore
            logger.warning(
                'Node with id %s and inner text "%s" might not be new. Make sure to check!',
                node_id,
                inner_text,  # type: ignore
            )

    logger.info(
        "%d component nodes were classified as added, %d as removed",
        len(new_node_occurrences),
        len(removed_components),
    )


def process_removed_networks(
    old_graph: Graph, result_graph: Graph, removed_networks: list[Network]
) -> None:
    """
    In-place function that adds the removed networks to the left of the existing nodes in the given
    result graph.
    Copies of old_graph objects are used to avoid modifying the original graph.

    :param old_graph: The graph considered as the old version, from which the removed networks stem
    :type old_graph: Graph
    :param result_graph: The graph to which the removed networks shall be added
    :type result_graph: Graph
    :param removed_networks: Networks that were removed from old_graph when compared to result_graph
    :type removed_networks: list[Network]

    :rtype: None
    """
    # Spacing between removed nodes and existing content
    SPACING: float = 5.0  # pylint: disable=C0103

    # Catch empty list of removed networks
    if not removed_networks:
        return

    logger.info("build_diff_graph: Processing %d removed networks", len(removed_networks))
    logger.debug("Removed Networks:")
    for i, removed_nw in enumerate(removed_networks):
        nw_name = get_network_name(removed_nw)
        nw_name = "Unknown" if nw_name is None else nw_name
        matched = False
        for network in old_graph.networks:
            if network == removed_nw:
                matched = True
                logger.debug(
                    'Network "%s" containing %d component nodes',
                    nw_name,
                    len(get_components_from_network(removed_nw, old_graph)),
                )
                break
        if not matched:
            raise ValueError(
                f"Network with index {i} and edge text {nw_name} in removed_networks does not exist"
                " in old_graph."
            )

    # Collect all nodes from removed networks
    removed_nodes: dict[UUID, NodeUnionType] = {
        node_id: node
        for network in removed_networks
        for edge in network.edges
        for node_id in (edge.sourceId, edge.targetId)
        if (node := old_graph.nodes.get(node_id))
    }

    if not removed_nodes:
        return

    # Calculate collective bounding box of removed nodes
    removed_nodes_min_y = min(node.yRemFactor for node in removed_nodes.values())
    removed_nodes_max_x = max(
        node.xRemFactor
        + (node.widthRemFactor if isinstance(node, (ComponentNode, XorNode)) else 0.0)
        for node in removed_nodes.values()
    )

    # Get boundaries of the result graph
    result_graph_boundaries = get_graph_boundaries(result_graph)
    result_graph_min_x, result_graph_min_y = result_graph_boundaries[0]

    # Calculate offset to top-left of existing content
    delta_x = result_graph_min_x - removed_nodes_max_x - SPACING
    delta_y = result_graph_min_y - removed_nodes_min_y - SPACING

    # Clone removed nodes and add them to the result graph
    node_id_map: dict[UUID, UUID] = {}
    for removed_node_id, removed_node in removed_nodes.items():
        node_to_add = removed_node.model_copy(deep=True)
        node_to_add.xRemFactor += delta_x
        node_to_add.yRemFactor += delta_y
        if isinstance(node_to_add, ComponentNode):
            node_to_add.classifications.add(
                EcuClassification(name=EcuClassificationName.ECU_ONLY_IN_BR)
            )
        node_to_add_id = uuid4()
        node_id_map[removed_node_id] = node_to_add_id
        result_graph.nodes[node_to_add_id] = node_to_add

    # Create new edges with cloned nodes
    for removed_network in removed_networks:
        edges_to_add: list[Edge] = []
        for removed_edge in removed_network.edges:
            new_source = node_id_map.get(removed_edge.sourceId)
            new_target = node_id_map.get(removed_edge.targetId)

            edge_to_add = removed_edge.model_copy(
                update={"sourceId": new_source, "targetId": new_target}
            )
            edges_to_add.append(edge_to_add)

        # Add cloned network with classification
        cloned_network = removed_network.model_copy(update={"edges": edges_to_add})
        cloned_network.dff_classification = NetworkDFFClassification.NW_ONLY_IN_BR
        result_graph.networks.append(cloned_network)

    logger.info(
        "build_diff_graph: Processed %d removed networks, containing %d nodes",
        len(removed_networks),
        len(removed_nodes),
    )


def build_diff_graph(
    graph_1: Graph, graph_2: Graph, graph_diff_result: GraphDiffResult, label_size: RemFactor = 3.0
) -> Optional[Graph]:
    """
    Adds the information of graph_diff_result to graph_1.
    This means that added networks and components are marked as new
    and removed networks and components are added to graph_1 while being marked as removed.

    :param graph_1: The graph considered as the new version.
    :type graph_1: Graph
    :param graph_2: The graph considered as the old version.
    :type graph_2: Graph
    :param graph_diff_result: The result of get_graph_diff().
    :type graph_diff_result: GraphDiffResult
    :param label_size: The RemFactor of the result graph label, if it is not set in graph_1,
                       default is from Architecture1_Collection.json
    :type label_size: RemFactor

    :return: Copy of graph_1 with the changes from graph_diff_result applied.
    :rtype: Graph | None
    """

    if not any(
        [
            graph_diff_result["added_networks"],
            graph_diff_result["network_component_changes"],
            graph_diff_result["removed_networks"],
        ]
    ):
        return None

    result_graph = graph_1.model_copy(deep=True)

    # Process added networks
    process_added_networks(result_graph, graph_diff_result["added_networks"])

    # Process network component changes
    process_changed_networks(result_graph, graph_diff_result["network_component_changes"])

    # Process removed networks
    process_removed_networks(graph_2, result_graph, graph_diff_result["removed_networks"])

    # set name of result_graph
    if result_graph.label:
        label_size = result_graph.label[2]
    result_graph.label = get_default_text("Diff Result", rem_factor=label_size)

    return result_graph
