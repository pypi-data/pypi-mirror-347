"""Module for enriching the graph."""

import fnmatch
import logging
import sys
from pathlib import Path
from typing import Any, Optional, cast

import pandas as pd

from aranea.ge.excel_names import (EXCEL_TECHNICAL_CAPABILITY_MAP,
                                   YES_NO_COLUMNS, ExcelColumnNames)
from aranea.models.config_model import GeConfig
from aranea.models.graph_model import (AttackPathGraph, ComponentNode,
                                       EcuClassification,
                                       EcuClassificationName, Graph,
                                       GraphCollection, Network, ProtocolType,
                                       TechnicalCapability,
                                       TechnicalCapabilityName)

logger = logging.getLogger(__name__)


class GraphCollectionEnricher:
    """Class for enriching the GraphCollection with ratings from Excel files."""

    def __init__(self, graph_collection: GraphCollection[Graph | AttackPathGraph]) -> None:
        """Constructor for the GraphCollectionEnricher class."""
        self.graph_collection: GraphCollection[Graph | AttackPathGraph] = graph_collection

    def to_bool(self, value: Any) -> bool:
        """Checks if a string starts with a 'y' or 'Y'.
        If is not a string, it returns False.

        :param value: The string to check.
        :type value: str
        :return: True if the string starts with 'y' or 'Y', otherwise False.
        :rtype: bool
        """
        if isinstance(value, str):
            return value.strip().lower().startswith("y")

        return False

    def transform_technical_capabilities(
        self, value: pd.StringDtype
    ) -> frozenset[TechnicalCapability] | frozenset[None]:
        """Transforms a ; separated string of ExcelTechnicalCapabilityNames
        to a frozenset of TechnicalCapability.

        :param value: The string to transform.
        :type value: pd.StringDtype
        :return: The frozenset of TechnicalCapability.
        :rtype: frozenset[TechnicalCapability]
        """

        if not isinstance(value, str):
            return frozenset()

        strings: list[str] = value.split(";")
        capabilities: set[TechnicalCapability] = set()

        for string in strings:
            string = string.strip()
            capability_name: TechnicalCapabilityName | None = EXCEL_TECHNICAL_CAPABILITY_MAP.get(
                string
            )
            if capability_name:
                capabilities.add(TechnicalCapability(name=capability_name))
            else:
                logger.warning(
                    "%s is not a valid value for the ``Technical Capability`` column!", string
                )
                logger.info(
                    "Please take a look at the valid values in the "
                    "ExcelTechnicalCapabilityNames Enum."
                )

        return frozenset(capabilities)

    def read_ecu_ratings(self, excel_file_path: Path) -> pd.DataFrame:
        """Converts the ECU ratings from an Excel file to a DataFrame.

        Duplicated rows in the Excel file will be removed.

        :param excel_file_path: The path to the Excel file containing the ECU ratings.
        :type excel_file_path: Path
        :return: The DataFrame containing the ECU ratings.
        :rtype: pd.DataFrame
        """
        # write excel file to DataFrame
        df: pd.DataFrame = pd.read_excel(  # pyright: ignore
            io=excel_file_path,
            sheet_name=0,
            header=0,
            index_col=None,
            dtype={
                ExcelColumnNames.ECU_NAME.value: str,
                ExcelColumnNames.SECURITY_CLASS.value: pd.UInt8Dtype(),
                ExcelColumnNames.EXTERNAL_INTERFACE.value: pd.StringDtype(),
                ExcelColumnNames.GATEWAY.value: pd.StringDtype(),
                ExcelColumnNames.LIN_SLAVE.value: pd.StringDtype(),
                ExcelColumnNames.DOMAIN.value: pd.StringDtype(),
                ExcelColumnNames.TECHNICAL_CAPABILITY.value: pd.StringDtype(),
                ExcelColumnNames.CRITICAL_ELEMENT.value: pd.StringDtype(),
            },
            engine="openpyxl",
        )

        required_columns = {name.value for name in ExcelColumnNames}
        missing_columns = required_columns - set(df.columns)
        if missing_columns:
            logger.error("Missing columns in Excel file: %s", missing_columns)
            sys.exit(1)

        # convert yes/no columns to bool
        for col in YES_NO_COLUMNS:
            df[col] = df[col].apply(self.to_bool)  # pyright: ignore

        # transform the ; separated technical capabilities to a frozenset of TechnicalCapability
        df[ExcelColumnNames.TECHNICAL_CAPABILITY.value] = df[
            ExcelColumnNames.TECHNICAL_CAPABILITY.value
        ].apply(  # pyright: ignore
            self.transform_technical_capabilities
        )

        df = df.drop_duplicates(keep="first")  # pyright: ignore
        # set the unique ECU name as the index of the DataFrame
        df.set_index(ExcelColumnNames.ECU_NAME.value, inplace=True)  # pyright: ignore

        logger.info("Imported the ECU ratings from: %s", excel_file_path)
        logger.debug("Imported ratings: \n%s", df)

        return df

    def find_ecu_pattern(self, ecu_name: str, ratings: pd.DataFrame) -> str | None:
        """Finds the pattern in the DataFrame that matches the ECU name.

        :param ecu_name: The name of the ECU.
        :type ecu_name: str
        :param ratings: The DataFrame containing the ECU ratings.
        :type ratings: pd.DataFrame
        :return: The pattern that matches the ECU name.
        :rtype: str | None
        """
        patterns: list[str] = []
        pattern: str | None = None

        # safe all patterns that match the ECU name
        for index, _ in ratings.iterrows():  # pyright: ignore
            ecu_pattern = str(index)
            if fnmatch.fnmatch(ecu_name, ecu_pattern):
                patterns.append(ecu_pattern)

        # return None or the longest pattern
        if len(patterns) == 0:
            logger.warning(
                "Found no rating for ECU '%s'.",
                ecu_name,
            )
        else:
            patterns = sorted(patterns, key=len, reverse=True)
            logger.debug(
                "Found %s patterns %s for ECU '%s'.",
                str(len(patterns)),
                str(patterns),
                ecu_name,
            )
            if len(patterns) > 1:
                logger.debug("Using the longest match: '%s'.", str(patterns[0]))
            pattern = patterns[0]

        return pattern

    def __set_security_class(
        self, node: ComponentNode, ratings: pd.DataFrame, pattern: str
    ) -> None:
        """Overwrites the security class of the ComponentNode based on the ratings DataFrame.

        :param node: The node to set the security class for.
        :type node: ComponentNode
        :param ratings: The DataFrame containing the ECU ratings.
        :type ratings: pd.DataFrame
        :param pattern: The pattern that matches the ECU name of the node.
        :type pattern: str
        """
        security_class: int | None = cast(
            Optional[int],
            ratings.at[pattern, ExcelColumnNames.SECURITY_CLASS.value],  # pyright: ignore
        )
        if not pd.isna(security_class):
            node.security_class = int(security_class)
        else:
            node.security_class = None

    def __update_technical_capability(
        self, node: ComponentNode, ratings: pd.DataFrame, pattern: str
    ) -> None:
        """Updates the TechnicalCapabilities of the ComponentNode based on the ratings DataFrame.
        Old TechnicalCapabilities are overwritten.

        :param node: The node to set the TechnicalCapability for.
        :type node: ComponentNode
        :param ratings: The DataFrame containing the ECU ratings.
        :type ratings: pd.DataFrame
        :param pattern: The pattern that matches the ECU name of the node.
        :type pattern: str
        """
        node.technical_capabilities = set(
            ratings.at[pattern, ExcelColumnNames.TECHNICAL_CAPABILITY.value]  # pyright: ignore
        )

    def __set_external_interface_classification(
        self, node: ComponentNode, ratings: pd.DataFrame, pattern: str
    ) -> None:
        """Sets or removes the EXTERNAL_INTERFACE classification of the ComponentNode
        based on the ratings DataFrame.

        If a ECU has an EXTERNAL_INTERFACE it is also an ENTRY_POINT, so the ENTRY_POINT
        classification will be also updated.

        :param node: The node to set the EXTERNAL_INTERFACE classification for.
        :type node: ComponentNode
        :param ratings: The DataFrame containing the ECU ratings.
        :type ratings: pd.DataFrame
        :param pattern: The pattern that matches the ECU name of the node.
        :type pattern: str
        """
        if ratings.at[pattern, ExcelColumnNames.EXTERNAL_INTERFACE.value]:  # pyright: ignore
            node.classifications.add(
                EcuClassification(name=EcuClassificationName.EXTERNAL_INTERFACE)
            )
            node.classifications.add(EcuClassification(name=EcuClassificationName.ENTRY_POINT))
        else:
            node.classifications.discard(
                EcuClassification(name=EcuClassificationName.EXTERNAL_INTERFACE)
            )
            node.classifications.discard(EcuClassification(name=EcuClassificationName.ENTRY_POINT))

    def __set_lin_connected_classification(
        self, node: ComponentNode, ratings: pd.DataFrame, pattern: str
    ) -> None:
        """Sets or removes the LIN_CONNECTED_ECU classification of the ComponentNode
        based on the ratings DataFrame.

        The LIN_CONNECTED_ECU classification should normally already be set during the
        PDF parsing process (g2d). This method will print a warning if the GraphCollection
        and the Excel file do not match. The classification will be set according to the
        Excel file.

        :param node: The node to set the LIN_CONNECTED_ECU classification for.
        :type node: ComponentNode
        :param ratings: The DataFrame containing the ECU ratings.
        :type ratings: pd.DataFrame
        :param pattern: The pattern that matches the ECU name of the node.
        :type pattern: str
        """
        lin_connected_excel: bool = ratings.at[  # pyright: ignore
            pattern, ExcelColumnNames.LIN_SLAVE.value
        ]
        lin_connected_node: bool = EcuClassificationName.LIN_CONNECTED_ECU in [
            classification.name for classification in node.classifications
        ]

        if lin_connected_node != lin_connected_excel:
            logger.warning(
                "Mismatch between the GraphCollection (from PDF) and Excel for LIN_CONNECTED_ECU "
                "classification for ECU '%s'.\n"
                "Classification 'LIN_CONNECTED_ECU' according to Excel: %s. (will be used)\n"
                "Classification 'LIN_CONNECTED_ECU' according to GraphCollection (from PDF): %s",
                (
                    node.innerText[0]
                    if node.innerText is not None
                    else node.outerText[0]  # type: ignore
                ),  # type ignore because outer text is how we match, can't be None
                str(lin_connected_excel),  # pyright: ignore
                str(lin_connected_node),
            )

        if lin_connected_excel:
            node.classifications.add(
                EcuClassification(name=EcuClassificationName.LIN_CONNECTED_ECU)
            )
        else:
            node.classifications.discard(
                EcuClassification(name=EcuClassificationName.LIN_CONNECTED_ECU)
            )

    def __set_gateway_classification(
        self, node: ComponentNode, ratings: pd.DataFrame, pattern: str
    ) -> None:
        """Sets the gateway classification of the ComponentNode based on the ratings DataFrame.

        :param node: The node to set the gateway classification for.
        :type node: ComponentNode
        :param ratings: The DataFrame containing the ECU ratings.
        :type ratings: pd.DataFrame
        :param pattern: The pattern that matches the ECU name of the node.
        :type pattern: str
        """
        domain: str | None = cast(
            Optional[str], ratings.at[pattern, ExcelColumnNames.DOMAIN.value]  # pyright: ignore
        )
        if (
            not pd.isna(domain)
            and ratings.at[pattern, ExcelColumnNames.GATEWAY.value]  # pyright: ignore
        ):
            node.classifications.discard(
                EcuClassification(name=EcuClassificationName.NON_DOMAIN_GATEWAY)
            )
            node.classifications.add(EcuClassification(name=EcuClassificationName.DOMAIN_GATEWAY))
        elif ratings.at[pattern, ExcelColumnNames.GATEWAY.value]:  # pyright: ignore
            node.classifications.discard(
                EcuClassification(name=EcuClassificationName.DOMAIN_GATEWAY)
            )
            node.classifications.add(
                EcuClassification(name=EcuClassificationName.NON_DOMAIN_GATEWAY)
            )
        else:
            node.classifications.discard(
                EcuClassification(name=EcuClassificationName.DOMAIN_GATEWAY)
            )
            node.classifications.discard(
                EcuClassification(name=EcuClassificationName.NON_DOMAIN_GATEWAY)
            )

    def __set_critical_element_classification(
        self, node: ComponentNode, ratings: pd.DataFrame, pattern: str
    ) -> None:
        """Sets or removes the CRITICAL_ELEMENT classification of the ComponentNode
        based on the ratings DataFrame.

        :param node: The node to set the CRITICAL_ELEMENT classification for.
        :type node: ComponentNode
        :param ratings: The DataFrame containing the ECU ratings.
        :type ratings: pd.DataFrame
        :param pattern: The pattern that matches the ECU name of the node.
        :type pattern: str
        """
        if ratings.at[pattern, ExcelColumnNames.CRITICAL_ELEMENT.value]:  # pyright: ignore
            node.classifications.add(EcuClassification(name=EcuClassificationName.CRITICAL_ELEMENT))
        else:
            node.classifications.discard(
                EcuClassification(name=EcuClassificationName.CRITICAL_ELEMENT)
            )

    def set_component_node_attributes(
        self, node: ComponentNode, ratings: pd.DataFrame, pattern: str
    ) -> None:
        """Sets the attributes of the node based on the ratings DataFrame.

        :param node: The node to set the attributes for.
        :type node: ComponentNode
        :param ratings: The DataFrame containing the ECU ratings.
        :type ratings: pd.DataFrame
        :param pattern: The pattern that matches the ECU name of the node.
        :type pattern: str
        """
        # Update security_class
        self.__set_security_class(node, ratings, pattern)

        # Update technical_capabilities
        self.__update_technical_capability(node, ratings, pattern)

        # Update classifications
        self.__set_external_interface_classification(node, ratings, pattern)
        self.__set_lin_connected_classification(node, ratings, pattern)
        self.__set_gateway_classification(node, ratings, pattern)
        self.__set_critical_element_classification(node, ratings, pattern)

    def enrich_technical_capabilities(
        self, node: ComponentNode, technical_capabilities: list[TechnicalCapability]
    ) -> None:
        """Overwrites the technical capabilities values of a node.

        Only for the TechnicalCapability the node already has.

        :param node: The ComponentNode to enrich.
        :type node: ComponentNode
        :param technical_capabilities: The technical capabilities to possible enrich the node with.
        :type technical_capabilities: list[TechnicalCapability]
        :return: The enriched ComponentNode.
        :rtype: ComponentNode
        """

        updated_capabilities: set[TechnicalCapability] = set()

        # Iterate over existing technical capabilities in the node
        for node_cap in node.technical_capabilities:
            # Check if there's a matching capability to enrich
            for cap in technical_capabilities:
                if node_cap.name == cap.name:
                    # Create an updated capability with enriched values
                    enriched_capability = TechnicalCapability(
                        name=cap.name,
                        attack_potential=cap.attack_potential,
                        feasibility_rating=cap.feasibility_rating,
                    )
                    updated_capabilities.add(enriched_capability)
                    break
            else:
                # If no match is found, keep the original capability
                updated_capabilities.add(node_cap)

        # Replace the node's technical capabilities with the updated set
        node.technical_capabilities = updated_capabilities

    def enrich_classifications(
        self, node: ComponentNode, classifications: list[EcuClassification]
    ) -> None:
        """Overwrites the classifications values of a node.

        Only for the EcuClassification the node already has.

        :param node: The ComponentNode to enrich.
        :type node: ComponentNode
        :param classifications: The classifications to possible enrich the node with.
        :type classifications: list[EcuClassification]
        :return: The enriched ComponentNode.
        :rtype: ComponentNode
        """
        updated_classifications: set[EcuClassification] = set()

        for node_classification in node.classifications:
            for classification in classifications:
                if node_classification.name == classification.name:
                    updated_classification = EcuClassification(
                        name=classification.name,
                        feasibility_rating=classification.feasibility_rating,
                    )
                    updated_classifications.add(updated_classification)
                    break
            else:
                updated_classifications.add(node_classification)

        node.classifications = updated_classifications

    def enrich_protocol_types(self, network: Network, protocol_types: list[ProtocolType]) -> None:
        """Updates the feasibility rating of the protocol types of a network.

        :param network: The network to enrich.
        :type network: Network
        :param protocol_types: The protocol types to possible enrich the network with.
        :type protocol_types: list[ProtocolType]
        """

        for protocol_type in protocol_types:
            if protocol_type.name == network.protocol_type.name:
                network.protocol_type.feasibility_rating = protocol_type.feasibility_rating
                break

    def get_ecu_name(self, node: ComponentNode) -> str:
        """Gets the ECU name from the node.

        If the 'outerText' attribute is not 'None', the ECU name is extracted from it.
        Otherwise, the 'innerText' attribute is used. If both are 'None', the default value
        'ECU_NAME_UNKNOWN' is returned.

        :param node: The node to get the ECU name from.
        :type node: ComponentNode
        :return: The ECU name.
        :rtype: str
        """

        ecu_name: str = "ECU_NAME_UNKNOWN"
        if node.outerText is not None:
            ecu_name = node.outerText[0]
        elif node.innerText is not None:
            logger.warning("The 'outerText' of Node is 'None': %s", str(node))
            logger.warning("Using the 'innerText' instead.")
            ecu_name = node.innerText[0]
        else:
            logger.error("The 'innerText' and 'outerText' of Node are 'None': %s", str(node))
            logger.error("Using the default value: %s.", ecu_name)

        return ecu_name

    def enrich(
        self,
        excel_file_path: Path,
        config: GeConfig,
    ) -> GraphCollection[Graph | AttackPathGraph]:
        """Reads the ECU ratings from an Excel file and uses the values from the config
        to enriches the graph with them.

        If a node has an 'outerText' attribute, the ECU name is extracted from it.
        The ECU name is then matched with the ratings DataFrame and
        the attributes of the node are set accordingly.

        For every network in the graph, the protocol type is enriched with the feasibility rating.

        :param excel_file_path: The path to the Excel file containing the ECU ratings.
        :type excel_file_path: Path
        :param config: Additional values to enrich the graph with.
        :type config: GeConfig
        :return: The enriched graph.
        :rtype: Graph
        """

        ratings: pd.DataFrame = self.read_ecu_ratings(excel_file_path)

        for graph in self.graph_collection.graphs:
            for node in graph.nodes.values():
                if not isinstance(node, ComponentNode):
                    continue

                ecu_name: str = self.get_ecu_name(node)
                pattern: str | None = self.find_ecu_pattern(ecu_name, ratings)
                if pattern is None:
                    continue

                self.set_component_node_attributes(node, ratings, pattern)
                self.enrich_technical_capabilities(node, config.technical_capabilities)
                self.enrich_classifications(node, config.ecu_classifications)

            for network in graph.networks:
                self.enrich_protocol_types(network, config.protocol_types)

        GraphCollection.model_validate(self.graph_collection)

        return self.graph_collection
