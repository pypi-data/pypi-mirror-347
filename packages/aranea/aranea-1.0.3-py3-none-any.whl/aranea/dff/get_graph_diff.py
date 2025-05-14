"""
Module for getting the difference between 2 graphs of the pydantic model.
"""

from collections import defaultdict
from dataclasses import dataclass
from typing import Optional, TypedDict
from uuid import UUID

from aranea.dff.utils import get_components_from_network, get_network_name
from aranea.models.graph_model import (ComponentNode, EcuClassificationName,
                                       Graph, Network, ProtocolTypeName,
                                       TechnicalCapabilityName)


@dataclass(frozen=True)
class ComparableAttributesComponent:
    """
    A dataclass containing comparable attributes of a component.
    """

    inner_text: Optional[str]
    outer_text: Optional[str]
    amg_only: bool
    technical_caps: frozenset[TechnicalCapabilityName]
    classifications: frozenset[EcuClassificationName]


class ComparableAttributesNetwork(TypedDict):
    """
    A dictionary type containing comparable attributes of a network.
    """

    protocol_type: ProtocolTypeName
    edge_text: Optional[str]
    amg_only: bool


@dataclass
class EnrichedNetwork:
    """
    A dataclass containing a network and a dict of component attributes of the components in the
    network.
    """

    nw: Network
    component_attributes: dict[ComparableAttributesComponent, set[UUID]]
    # UUID of the components with ComparableAttributesComponent in the network


class NetworkComponentChanges(TypedDict):
    """
    A dictionary type containing a network and the changes in components in the network.
    The Network is intended to be from the graph which is considered as newer version.
    """

    changed_network: Network
    added_components: list[UUID]  # UUIDs used as these are only marked new in the diff graph
    removed_components: list[ComponentNode]  # Components which are removed in the diff graph
    # These are added in the diff graph


class GraphDiffResult(TypedDict):
    """
    A dictionary type containing the result of a graph comparison.
    This includes added and removed networks and changes in components for matching networks.
    It is intended to be viewed from the perspective of the graph which is considered as newer.
    Contained objects should be deep copies of the original objects.
    """

    added_networks: list[Network]
    removed_networks: list[Network]
    network_component_changes: list[NetworkComponentChanges]


# data preparation functions -----------------------------------------------------------------------


def get_comparable_attributes_component(component: ComponentNode) -> ComparableAttributesComponent:
    """
    Extracts and returns the comparable attributes of a given component.

    :param component: The ComponentNode to extract the attributes from
    :type component: ComponentNode

    :return: The comparable attributes of the component
    :rtype: ComparableAttributesComponent
    """

    inner_text = component.innerText[0] if component.innerText else None
    outer_text = component.outerText[0] if component.outerText else None

    return ComparableAttributesComponent(
        inner_text=inner_text,
        outer_text=outer_text,
        amg_only=component.amg_only,
        technical_caps=frozenset(tc.name for tc in component.technical_capabilities),
        classifications=frozenset(clas.name for clas in component.classifications),
    )


def get_comparable_attributes_network(enriched_nw: EnrichedNetwork) -> ComparableAttributesNetwork:
    """
    Extracts and returns the comparable attributes of the network in a given EnrichedNetwork.
    These are the protocol type, edge text and AMG-only flag.

    :param enriched_nw: The EnrichedNetwork to extract the attributes from
    :type network: EnrichedNetwork

    :return: The comparable attributes of the network
    :rtype: ComparableAttributesNetwork
    """

    edge_text = get_network_name(enriched_nw.nw)

    return ComparableAttributesNetwork(
        protocol_type=enriched_nw.nw.protocol_type.name,
        edge_text=edge_text,
        amg_only=enriched_nw.nw.amg_only,
    )


def get_enriched_nws_from_graph(graph: Graph) -> list[EnrichedNetwork]:
    """
    Extracts and returns a list of EnrichedNetwork objects from the given graph.

    :param graph: The Graph to extract the networks from
    :type graph: Graph

    :return: A list of EnrichedNetwork objects
    :rtype: list[EnrichedNetwork]
    """
    comparable_nws: list[EnrichedNetwork] = []

    for nw in graph.networks:
        component_attributes: defaultdict[ComparableAttributesComponent, set[UUID]] = defaultdict(
            set
        )
        component_dict = get_components_from_network(nw, graph)
        for component_id, component in component_dict.items():
            component_attributes[get_comparable_attributes_component(component)].add(component_id)

        comparable_nws.append(EnrichedNetwork(nw, component_attributes))

    return comparable_nws


# Actual diffing below -----------------------------------------------------------------------------


def count_nw_component_differences(nw_1: EnrichedNetwork, nw_2: EnrichedNetwork) -> int:
    """
    Count the number of differences between the components of two networks.

    :param nw_1: The first network to compare
    :type nw_1: Network
    :param nw_2: The second network to compare
    :type nw_2: Network

    :return: Number of differences between the two given Networks based on the contained components
    :rtype: int
    """
    total_diff: int = 0

    # create a set of all comparable attributes
    all_attributes = set(nw_1.component_attributes.keys()) | set(nw_2.component_attributes.keys())

    # Count the difference in the number of components with the same set of comparable attributes
    for attributes in all_attributes:
        comp_ids_1 = nw_1.component_attributes.get(attributes, set())
        comp_ids_2 = nw_2.component_attributes.get(attributes, set())
        total_diff += abs(len(comp_ids_1) - len(comp_ids_2))

    return total_diff


def find_best_network_match(
    network_1: EnrichedNetwork, unmatched_networks: list[EnrichedNetwork]
) -> Optional[EnrichedNetwork]:
    """
    Find the best match of network_1 in unmatched_networks based on component similarity.
    Returns the best matching network or None if no match was found.

    :param network_1: The network to find a match for
    :type network_1: EnrichedNetwork
    :param unmatched_networks: The list of umatched networks to match against
    :type unmatched_networks: list[EnrichedNetwork]

    :return: The best matching network from unmatched_networks or None if no match was found
    :rtype: Optional[EnrichedNetwork]
    """
    best_match: Optional[EnrichedNetwork] = None
    min_differences = float("inf")

    for unmatched_network in unmatched_networks:
        if get_comparable_attributes_network(network_1) != get_comparable_attributes_network(
            unmatched_network
        ):
            continue

        differences = count_nw_component_differences(network_1, unmatched_network)
        if differences < min_differences:
            min_differences = differences
            best_match = unmatched_network

    return best_match


def diff_nw_components(
    nw_1: EnrichedNetwork, nw_2: EnrichedNetwork, graph_2: Graph
) -> NetworkComponentChanges:
    """
    Extracts and returns the changes in components between two networks.
    Returns a dictionary containing lists of removed ComponentNodes and added UUIDs of components.
    Added means not in nw_2, removed means missing in nw_1.

    :param nw_1: The network which is considered as newer version
    :type nw_1: EnrichedNetwork
    :param nw_2: The network which is considered as older version
    :type nw_2: EnrichedNetwork
    :param graph_2: The graph containing nw_2
    :type graph_2: Graph

    :return: A dictionary containing the changed network and the added and removed components
    :rtype: NetworkComponentChanges
    """

    result: NetworkComponentChanges = {
        "changed_network": nw_1.nw.model_copy(deep=True),
        "added_components": [],
        "removed_components": [],
    }

    # create a set of all comparable attributes
    all_attributes = set(nw_1.component_attributes.keys()) | set(nw_2.component_attributes.keys())

    for attributes in all_attributes:
        # Get the component ids for the current attributes
        comp_ids_1: set[UUID] = nw_1.component_attributes.get(attributes, set())
        comp_ids_2: set[UUID] = nw_2.component_attributes.get(attributes, set())

        # Get the counts of components with the same attributes
        attr_count_1 = len(comp_ids_1)
        attr_count_2 = len(comp_ids_2)

        if attr_count_1 > attr_count_2:
            # More components in comps_1 / nw_1 - these were added
            # Add attr_count_1 - attr_count_2 random UUIDs from comp_ids_1 to added
            # This works because all the components are indistinguishable by their comparable
            # attributes
            result["added_components"].extend(list(comp_ids_1)[attr_count_2:])
        elif attr_count_2 > attr_count_1:
            # More components in comps_2 / nw_2 - these were removed
            # Find the actual components with these ids
            comps_2: list[ComponentNode] = [
                comp
                for comp_id in comp_ids_2
                if (comp := graph_2.nodes.get(comp_id)) and isinstance(comp, ComponentNode)
            ]

            copied_comps_2 = [comp.model_copy(deep=True) for comp in comps_2]

            # Add attr_count_2 - attr_count_1 random components from comps_2 to removed
            result["removed_components"].extend(copied_comps_2[attr_count_1:])

    return result


def get_graph_diff(graph_1: Graph, graph_2: Graph) -> GraphDiffResult:
    """
    Compares two graphs and identifies added and removed networks and components.

    The comparison preserves multiple networks/components with identical comparable attributes
    and matches them based on both network attributes and component compositions.

    In the result dictionary, 'added_networks' contains networks that are new in graph_1,
    'removed_networks' contains networks that are missing in graph_1, and
    'network_component_changes' contains changes in components for networks that are present in both
    graphs.
    So to sum up, the result is intended to be viewed from the perspective of graph_1.
    All objects in the result are deep copies of the original objects so that they can be modified
    without affecting the original graphs.

    :param graph_1: The graph which is to be considered as update of graph_2
    :type graph_new: Graph
    :param graph_old: The graph which is to be considered as older version of graph_1
    :type graph_old: Graph

    :return: A dictionary containing deepcopies unmatched networks and components
    :rtype: GraphDiffResult
    """
    result: GraphDiffResult = {
        "added_networks": [],
        "removed_networks": [],
        "network_component_changes": [],
    }

    nws_1: list[EnrichedNetwork] = get_enriched_nws_from_graph(graph_1)
    unmatched_nws: list[EnrichedNetwork] = get_enriched_nws_from_graph(graph_2)

    # For each network in graph_1, find its best match among unmatched networks in graph_2
    for currrent_nw in nws_1:
        best_match = find_best_network_match(currrent_nw, unmatched_nws)

        if best_match is None:
            # No matching network found - this is an added network
            result["added_networks"].append(currrent_nw.nw.model_copy(deep=True))
            continue

        # Remove the matched network from available networks
        unmatched_nws.remove(best_match)

        # Compare components of the matched networks
        nw_component_changes: NetworkComponentChanges = diff_nw_components(
            currrent_nw, best_match, graph_2
        )

        if nw_component_changes["added_components"] or nw_component_changes["removed_components"]:
            # only add the network if there are changes in components
            # unchanged networks are not added to the result
            result["network_component_changes"].append(nw_component_changes)

    # Any remaining networks in unmatched_nws (originating from graph_2) are removed networks
    result["removed_networks"] = list(
        unmatched_nw.nw.model_copy(deep=True) for unmatched_nw in unmatched_nws
    )

    return result
