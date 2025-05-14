"""
This module provides the functionality for generating and rating attack path graphs
based on attack feasibility.
"""

from uuid import UUID

import networkx as nx
import pandas as pd

from aranea.apg.compose_attack_path_graph import compose_attack_path_graph
from aranea.apg.get_networkx_graph import get_networkx_graph
from aranea.apg.get_reduced_graph import get_reduced_graph
from aranea.apg.get_shortest_path import get_shortest_path
from aranea.apg.utils.get_positioned_component_nodes import PositionalMargin
from aranea.models.graph_model import (AttackPathGraph, ComponentNode,
                                       EcuClassificationName, Graph,
                                       GraphCollection, NodeUnionType,
                                       TechnicalCapabilityName,
                                       get_default_text)


def get_attack_paths(
    graph: Graph, positional_margin: PositionalMargin = (15, 15, 0, 15)
) -> GraphCollection[AttackPathGraph]:
    """
    Function for generating a collection of attack path graphs.
    :param graph: The graph to generate paths from.
    :type graph: Graph
    :param positional_margin: The positional margin to use for each path.
    :type positional_margin: PositionalMargin
    :return: The generated paths in a collection.
    :rtype: GraphCollection[AttackPathGraph]
    """
    entry_point_nodes = {
        key: value
        for key, value in graph.nodes.items()
        if isinstance(value, ComponentNode)
        and EcuClassificationName.ENTRY_POINT
        in [classification.name for classification in value.classifications]
    }

    target_nodes: dict[UUID, ComponentNode] = {
        key: value
        for key, value in graph.nodes.items()
        if isinstance(value, ComponentNode)
        and EcuClassificationName.CRITICAL_ELEMENT
        in [classification.name for classification in value.classifications]
    }

    graph_collection: GraphCollection[AttackPathGraph] = GraphCollection(graphs=[])

    netx_graph: nx.MultiGraph[UUID] = get_networkx_graph(  # pylint: disable=unsubscriptable-object
        graph
    )
    weighted_graph: nx.Graph[UUID] = get_reduced_graph(  # pylint: disable=unsubscriptable-object
        netx_graph
    )

    for entry_uuid, entry_component in entry_point_nodes.items():
        for target_uuid in target_nodes:
            for technical_capability in entry_component.technical_capabilities:

                shortest_path = get_shortest_path(
                    weighted_graph, entry_uuid, target_uuid, technical_capability.name
                )

                if shortest_path:
                    graph_collection.graphs.append(
                        compose_attack_path_graph(
                            shortest_path[0],
                            shortest_path[1],
                            entry_uuid,
                            target_uuid,
                            technical_capability,
                            positional_margin,
                        )
                    )

    return graph_collection


def get_path_afr_and_length(graph: AttackPathGraph, x: float) -> tuple[float, int]:
    """
    Function for rating an attack path graph and getting the length of the path.

    :param graph: The graph to rate
    :type graph: AttackPathGraph
    :param x: A user given input for factoring the path length impact.
    :type x: float
    :return: The rating and the length of the path.
    :rtype: tuple[float, int]
    """
    if len(graph.nodes) == 0 or len(graph.networks) == 0:
        raise ValueError("Empty graph")

    if x <= 0:
        raise ValueError("x must be positive")

    raw_feasibility: float = 1

    raw_feasibility *= graph.entry_technical_capability.feasibility_rating

    for node in graph.nodes.values():
        if isinstance(node, ComponentNode):
            for classification in node.classifications:
                raw_feasibility *= classification.feasibility_rating

    for network in graph.networks:
        raw_feasibility *= network.protocol_type.feasibility_rating

    count_hops = len(graph.nodes) - 1
    omega_hops = count_hops * x
    afr_path = raw_feasibility / omega_hops

    return afr_path, count_hops


def attack_path_collection_to_xsl_data_frame(
    graph_collection: GraphCollection[AttackPathGraph],
) -> pd.DataFrame:
    """
    Function for generating a xsl ready data frame from an attack path collection.

    :param graph: The collection to generate a xsl ready data frame from.
    :type graph: GraphCollection[AttackPathGraph]
    :return: The generated xsl ready data frame
    :rtype: pd.DataFrame
    """
    dataframe = pd.DataFrame(
        columns=["Entry Point", "Used Technical Capability", "Path", "Amount Hops"],
        index=range(len(graph_collection.graphs)),
    )

    for index, graph in enumerate(graph_collection.graphs):
        path: list[str] = []

        prev_ecu_uuid: UUID = graph.entry_ecu
        running_ecu_uuid = graph.entry_ecu

        while running_ecu_uuid != graph.target_ecu:
            add_ecu_text_to_path(running_ecu_uuid, path, graph)

            used_reverse = False

            used_edge, used_network = next(
                (edge, network)
                for network in graph.networks
                for edge in network.edges
                if (
                    (edge.sourceId == running_ecu_uuid and edge.targetId != prev_ecu_uuid)
                    or (edge.targetId == running_ecu_uuid and edge.sourceId != prev_ecu_uuid)
                )
            )

            if used_edge.targetId == running_ecu_uuid:
                used_reverse = True

            network_label = next(
                (edge.text for edge in used_network.edges if edge.text is not None),
                get_default_text("Unnamed Network"),
            )
            path.append(network_label[0])

            prev_ecu_uuid = running_ecu_uuid
            running_ecu_uuid = used_edge.targetId if not used_reverse else used_edge.sourceId

        add_ecu_text_to_path(running_ecu_uuid, path, graph)

        entry_ecu = graph.nodes[graph.entry_ecu]

        if not isinstance(entry_ecu, ComponentNode):
            raise ValueError("Invalid ECU type")

        dataframe.loc[index] = [
            entry_ecu.innerText[0] if entry_ecu.innerText else "Unnamed Entry ECU",
            graph.entry_technical_capability.name.value,
            "\n  -> ".join([p.replace("\n", "") for p in path]),
            len(graph.nodes) - 1,
        ]

    return dataframe


def add_ecu_text_to_path(ecu_uuid: UUID, path: list[str], graph: AttackPathGraph):
    """
    Function for get the inner text of an ECU

    :param ecu_uuid: The ECU UUID
    :type ecu_uuid: UUID
    :param path: The created path
    :type path: list[str]
    :param graph: The graph to get the name from
    :type graph: Graph
    :return: The ECU text
    :rtype: str
    """
    running_ecu: NodeUnionType = graph.nodes[ecu_uuid]

    if not isinstance(running_ecu, ComponentNode):
        raise ValueError("Invalid ECU type")

    if running_ecu.innerText:
        path.append(running_ecu.innerText[0])
    else:
        path.append("Unnamed ECU")


def __get_apg_statistics_skeleton(
    graph_collection: GraphCollection[AttackPathGraph],
) -> pd.DataFrame:
    tech_caps: set[tuple[str, float]] = set()
    target_nodes: set[ComponentNode] = set()
    tc2entry_nodes: dict[str, set[str]] = {tc.name: set() for tc in TechnicalCapabilityName}

    for graph in graph_collection.graphs:
        entry_tc = graph.entry_technical_capability
        entry_ecu = graph.nodes[graph.entry_ecu]
        target_ecu = graph.nodes[graph.target_ecu]

        if not isinstance(entry_ecu, ComponentNode):
            raise ValueError("Invalid entry ECU type")
        if not isinstance(target_ecu, ComponentNode):
            raise ValueError("Invalid target ECU type")

        tech_caps.add((entry_tc.name.name, entry_tc.feasibility_rating))
        target_nodes.add(target_ecu)

        if entry_ecu.outerText:
            tc2entry_nodes[entry_tc.name.name].add(entry_ecu.outerText[0])
        elif entry_ecu.innerText:
            tc2entry_nodes[entry_tc.name.name].add(entry_ecu.innerText[0])
        else:
            tc2entry_nodes[entry_tc.name.name].add(str(graph.entry_ecu))

    columns = [tc[0] for tc in sorted(tech_caps, key=lambda t: -t[1])]

    sorted_target_nodes = sorted(
        target_nodes, key=lambda n: (-(n.security_class or 0), (n.outerText or [""])[0])
    )
    index = ["Entrypoints"] + list(
        {node.outerText[0] for node in sorted_target_nodes if node.outerText is not None}
    )

    df = pd.DataFrame(index=index, columns=columns)
    df.loc["Entrypoints"] = [",".join(tc2entry_nodes[c]) for c in df.columns]
    return df


def __fill_apg_statistics_skeleton(
    graph_collection: GraphCollection[AttackPathGraph], skeleton: pd.DataFrame
) -> pd.DataFrame:
    for graph in graph_collection.graphs:
        entry_tc = graph.entry_technical_capability
        target_ecu = graph.nodes[graph.target_ecu]

        if not isinstance(target_ecu, ComponentNode):
            raise ValueError("Invalid target ECU type")

        if target_ecu.outerText:
            target_name = target_ecu.outerText[0]
            tc_name = entry_tc.name.name
            prev_hop_count = skeleton.loc[target_name, tc_name]
            if isinstance(prev_hop_count, int):
                hop_count = min(prev_hop_count, len(graph.nodes) - 1)
            else:
                hop_count = len(graph.nodes) - 1
            skeleton.loc[target_ecu.outerText[0], tc_name] = hop_count
    return skeleton


def apg_collection_to_statistics_df(
    graph_collection: GraphCollection[AttackPathGraph],
) -> pd.DataFrame:
    """
    Function for generating an attack path statistics / overview DataFrame.

    The cells contain the minimum hop count for an attack path from an ECU with
    a specific technical capability (columns) to a specific target ECU (rows).

    :param graph: The collection to generate a statistics DataFrame jor.
    :type graph: GraphCollection[AttackPathGraph]
    :return: The statistics DataFrame.
    :rtype: pd.DataFrame
    """

    skeleton_df = __get_apg_statistics_skeleton(graph_collection)
    df = __fill_apg_statistics_skeleton(graph_collection, skeleton_df)

    df.dropna(  # pyright: ignore
        how="all",
        axis="columns",
        inplace=True,
    )

    return df
