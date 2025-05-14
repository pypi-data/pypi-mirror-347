"""
Module for converting graph difference results to tabular format.
Provides functionality to transform the differences between two graphs
into a structured tabular format using pandas DataFrames.
"""

from enum import Enum
from typing import Optional
from uuid import UUID, uuid4

import pandas as pd

from aranea.dff.get_graph_diff import GraphDiffResult
from aranea.dff.utils import (check_networks_in_graph,
                              get_components_from_network, get_network_name)
from aranea.models.graph_model import ComponentNode, Graph, Network


class DiffClassification(Enum):
    """
    Enum containing the possible classifications for diffing in the tabular output.
    """

    ADDED = "added"
    REMOVED = "removed"
    CHANGED = "changed"


def build_tabular_diff_representation(
    graph_diff_result: GraphDiffResult, graph_1: Graph, graph_2: Graph
) -> Optional[pd.DataFrame]:
    """
    This function takes the return value of 'get_graph_diff()' and transforms it into a tabular
    representation in the form of a pandas dataframe.
    To differentiate between added networks, removed networks and changed networks the last column
    in the dataframe, called "nw_dff_class" contains either "added", "removed" or "changed". This
    may be used to differently format each classification for example.
    The same goes for components with the second to last column "comp_dff_class" and the categories
    "added" and "removed".

    :param graph_diff_result: The return value of 'get_graph_diff()', containing differences
                              between two graphs
    :type graph_diff_result: GraphDiffResult
    :param graph_1: The graph, which is viewed as the new graph in the diffing process.
    :type graph_1: Graph
    :param graph_2: The graph, which is viewed as the old graph in the diffing process.
    :type graph_2: Graph

    :return: A pandas dataframe containing a tabular processing of the differences between the
             graphs given to 'get_graph_diff()'.
    :rtype: Optional[pandas.DataFrame]
    """

    if not any(
        [
            graph_diff_result["added_networks"],
            graph_diff_result["network_component_changes"],
            graph_diff_result["removed_networks"],
        ]
    ):
        return None

    # check if networks are in the respective given graph - if not, throw error
    result = check_networks_in_graph(graph_diff_result["added_networks"], graph_1)
    if result is not None:
        nw_name, index = result
        raise ValueError(
            f"Network with index {index} and edge text {nw_name} in added_networks is not in "
            "graph_1 given to build_tabular_diff_representation()"
        )
    result = check_networks_in_graph(graph_diff_result["removed_networks"], graph_2)
    if result is not None:
        nw_name, index = result
        raise ValueError(
            f"Network with index {index} and edge text {nw_name} in removed_networks is not in "
            "graph_2 given to build_tabular_diff_representation()"
        )
    result = check_networks_in_graph(
        [change["changed_network"] for change in graph_diff_result["network_component_changes"]],
        graph_1,
    )
    if result is not None:
        nw_name, index = result
        raise ValueError(
            f"Network with index {index} and edge text {nw_name} in network_component_changes is "
            "not in the graph given to build_tabular_diff_representation()"
        )

    # real code below -----------------
    result_df = pd.DataFrame(
        columns=[
            "label",
            "network type",
            "outer text",
            "inner text",
            "security class",
            "classifications",
            "technical capabilities",
            "comp_diff_class",
            "nw_diff_class",
        ]
    )

    def add_networks_to_dataframe(
        networks: list[Network],
        nw_diff_class: DiffClassification,
        added_comps: Optional[list[UUID]] = None,
        removed_comps: Optional[list[ComponentNode]] = None,
    ) -> None:
        """
        Function to add networks and their connected components to the result dataframe with
        classification information.
        This function processes a list of networks and adds their components to a global
        dataframe with classification information indicating whether networks or components
        have been added, removed, or changed.

        :param networks: List of networks to be added to the dataframe.
        :type networks: list[Network]
        :param nw_diff_class: Classification of the networks (ADDED, REMOVED, or CHANGED).
        :type nw_diff_class: DiffClassification
        :param added_comps: List of component UUIDs that have been added to existing networks.
        :type added_comps: Optional[list[UUID]]
        :param removed_comps: List of component nodes that have been removed from existing networks.
        :type removed_comps: Optional[list[ComponentNode]]

        :return: The function modifies the global result_df variable.
        :rtype: None
        """
        old_component_ids: set[UUID] = set()  # needed to correctly classify components as added
        if nw_diff_class == DiffClassification.ADDED:
            # get all component node UUIDs which are connected to networks not classified as new
            # all these components are not new, even if they are connected to new networks
            for nw in graph_1.networks:
                if nw not in networks:
                    nw_comps = get_components_from_network(nw, graph_1)
                    old_component_ids.update(nw_comps.keys())

        for nw in networks:
            label = get_network_name(nw)
            label = "Unknown" if label is None else label
            if nw_diff_class == DiffClassification.REMOVED:
                connected_ecus = get_components_from_network(nw, graph_2)
            else:
                connected_ecus = get_components_from_network(nw, graph_1)
            if removed_comps:
                # add removed comps to connected ecus, just as would be done in the graph
                # this allows us to add the component to the dataframe in the following loop
                for comp in removed_comps:
                    if comp not in connected_ecus.values():
                        # Use random uuids as we don't have them and don't need them
                        connected_ecus[uuid4()] = comp
            for uuid, comp_node in connected_ecus.items():
                # only set components as added if they really are
                comp_diff_class: Optional[DiffClassification] = (
                    nw_diff_class if uuid not in old_component_ids else None
                )
                # for changed networks: set DiffClassification accordingly
                if added_comps and uuid in added_comps:
                    comp_diff_class = DiffClassification.ADDED
                if removed_comps and comp_node in removed_comps:
                    comp_diff_class = DiffClassification.REMOVED

                new_row = pd.DataFrame(
                    {
                        "label": [label],
                        "network type": [nw.protocol_type.name.value],
                        "outer text": [
                            comp_node.outerText[0] if comp_node.outerText else "Unknown"
                        ],
                        "inner text": [
                            comp_node.innerText[0] if comp_node.innerText else "Unknown"
                        ],
                        "security class": [
                            comp_node.security_class if comp_node.security_class else None
                        ],
                        "classifications": [
                            (
                                [
                                    classification.name.value
                                    for classification in comp_node.classifications
                                ]
                                if comp_node.classifications
                                else None
                            )
                        ],
                        "technical capabilities": [
                            (
                                [tc.name.value for tc in comp_node.technical_capabilities]
                                if comp_node.technical_capabilities
                                else None
                            )
                        ],
                        "comp_diff_class": [comp_diff_class.value if comp_diff_class else None],
                        "nw_diff_class": [nw_diff_class.value],
                    }
                )
                nonlocal result_df
                result_df = pd.concat([result_df, new_row], ignore_index=True)

    add_networks_to_dataframe(graph_diff_result["added_networks"], DiffClassification.ADDED)
    add_networks_to_dataframe(graph_diff_result["removed_networks"], DiffClassification.REMOVED)
    for change in graph_diff_result["network_component_changes"]:
        add_networks_to_dataframe(
            [change["changed_network"]],
            DiffClassification.CHANGED,
            change["added_components"],
            change["removed_components"],
        )

    return result_df
