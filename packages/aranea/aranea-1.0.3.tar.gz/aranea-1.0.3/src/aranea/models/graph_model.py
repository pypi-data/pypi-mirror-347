"""
This module provides the pydantic model for working with graph data.
"""

from __future__ import annotations

import logging
import re
from enum import Enum
from typing import Annotated, Any, Generic, TypeVar, Union
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field
from pydantic.types import UuidVersion
from shapely import Point, Polygon, affinity

from aranea.g2d.text_node_constants import (
    TEXT_NODE_BOUNDING_BOX_HEIGHT_FACTOR, TEXT_NODE_BOUNDING_BOX_WIDTH_FACTOR)

logger = logging.getLogger(__name__)


class TextOrientation(Enum):
    """Enum for the orientation of the text."""

    VERTICAL = "VERTICAL"
    HORIZONTAL = "HORIZONTAL"


RemFactor = float
Text = tuple[str, TextOrientation, RemFactor]


def get_default_text(
    text: str,
    *,
    text_orientation: TextOrientation = TextOrientation.HORIZONTAL,
    rem_factor: RemFactor = 1,
) -> Text:
    """
    Function for creating a default text tuple.

    :param text: The corresponding text
    :type text: str
    :param text_orientation: The orientation of the text
    :type text_orientation: TextOrientation
    :param rem_factor: The rem factor of the text
    :type rem_factor: RemFactor
    :return: The default text tuple
    :rtype: Text
    """
    return text, text_orientation, rem_factor


class NodeType(Enum):
    """Enum for the type of the node."""

    COMPONENT = "COMPONENT"
    XOR = "XOR"
    TEXT = "TEXT"
    WAYPOINT = "WAYPOINT"


class Node(BaseModel):
    """Base class for all nodes."""

    model_config = ConfigDict(extra="forbid")

    type: NodeType
    xRemFactor: RemFactor = Field(
        description="Origin is in upper left corner of the document, x increases to the right. \
Factor orients itself on the respective Root Element Size used in the document.",
    )
    yRemFactor: RemFactor = Field(
        description="Origin is in upper left corner of the document, y increases downwards. \
Factor orients itself on the respective Root Element Size used in the document.",
    )


class TechnicalCapabilityName(Enum):
    """Enum for the supported technical capabilities.

    The comment behind the enum value is the corresponding string that the graph enricher
    is looking for in the Excel file. Documented in docs/source/user_guide.rst
    """

    ANALOG_BROADCAST = "ANALOG_BROADCAST"  # Radio
    BACKEND = "BACKEND"  # Cloud
    BLUETOOTH = "BLUETOOTH"  # BT
    CAR_CHARGER = "CAR_CHARGER"  # PLC
    CELLULAR = "CELLULAR"  # 5G
    DIGITAL_BROADCAST = "DIGITAL_BROADCAST"  # DVB
    NETWORK_SWITCH = "NETWORK_SWITCH"  # Switch
    NFC = "NFC"  # NFC
    OBD = "OBD"  # OBD
    SATELLITE = "SATELLITE"  # GNSS
    USB = "USB"  # USB
    WIFI = "WIFI"  # Wifi


class TechnicalCapability(BaseModel):
    """Model for the technical capabilities."""

    name: TechnicalCapabilityName
    attack_potential: int = 0
    feasibility_rating: Annotated[
        float,
        Field(
            ge=0.0,
            le=1.0,
            description="Evaluates how practical or likely it is for a specific \
                attack to succeed. Higher means more practical/likely.",
        ),
    ] = 1.0

    def __hash__(self) -> int:
        return hash((self.name, self.attack_potential, self.feasibility_rating))

    def __eq__(self, other: Any) -> bool:
        if isinstance(other, TechnicalCapability):
            return (
                self.name == other.name
                and self.attack_potential == other.attack_potential
                and self.feasibility_rating == other.feasibility_rating
            )
        return False


class EcuClassificationName(Enum):
    """Enum for the supported classification name of the ECUs."""

    ECU = "ECU"
    NEW_ECU = "NEW_ECU"
    ECU_ONLY_IN_BR = "ECU_ONLY_IN_BR"
    DOMAIN_GATEWAY = "DOMAIN_GATEWAY"
    NON_DOMAIN_GATEWAY = "NON_DOMAIN_GATEWAY"
    LIN_CONNECTED_ECU = "LIN_CONNECTED_ECU"
    ENTRY_POINT = "ENTRY_POINT"
    CRITICAL_ELEMENT = "CRITICAL_ELEMENT"
    EXTERNAL_INTERFACE = "EXTERNAL_INTERFACE"


class EcuClassification(BaseModel):
    """Model for the enum classification"""

    name: EcuClassificationName
    feasibility_rating: Annotated[
        float,
        Field(
            ge=0.0,
            le=1.0,
            description="Evaluates how practical or likely it is for a specific \
                attack to succeed. Higher means more practical/likely.",
        ),
    ] = 1.0

    def __hash__(self) -> int:
        return hash((self.name, self.feasibility_rating))

    def __eq__(self, other: Any) -> bool:
        if isinstance(other, EcuClassification):
            return self.name == other.name and self.feasibility_rating == other.feasibility_rating
        return False


class ComponentNode(Node):
    """Model for the component nodes."""

    type: NodeType = NodeType.COMPONENT
    heightRemFactor: RemFactor
    widthRemFactor: RemFactor
    innerText: Text | None = None
    outerText: Text | None = None
    amg_only: bool = False
    security_class: int | None = None
    technical_capabilities: set[TechnicalCapability] = Field(default=set())
    classifications: set[EcuClassification] = Field(
        default={EcuClassification(name=EcuClassificationName.ECU)},
    )

    def __hash__(self) -> int:
        return hash(
            (
                self.type,
                self.xRemFactor,
                self.yRemFactor,
                self.heightRemFactor,
                self.widthRemFactor,
                self.innerText,
                self.outerText,
                self.amg_only,
                self.security_class,
                frozenset(self.technical_capabilities),
                frozenset(self.classifications),
            )
        )

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, self.__class__):
            return NotImplemented
        return hash(self) == hash(other)

    def polygon(self, *, rem: float = 1, buffer: float = 0.0) -> Polygon:
        """
        Returns the polygon representation of the component's rectangle

        :param rem: The Root Element Size
        :type rem: float
        :param buffer: Increase the rectangle's dimensions by `buffer` in all directions
        :type buffer: float
        :return: The polygon representation of the rectangle
        :rtype: Polygon
        """
        _x_rem_factor = self.xRemFactor * rem
        _y_rem_factor = self.yRemFactor * rem
        _width_rem_factor = self.widthRemFactor * rem
        _height_rem_factor = self.heightRemFactor * rem

        return Polygon(
            (
                (_x_rem_factor - buffer, _y_rem_factor - buffer),
                (_x_rem_factor - buffer, _y_rem_factor + _height_rem_factor + buffer),
                (
                    _x_rem_factor + _width_rem_factor + buffer,
                    _y_rem_factor + _height_rem_factor + buffer,
                ),
                (_x_rem_factor + _width_rem_factor + buffer, _y_rem_factor - buffer),
                (_x_rem_factor - buffer, _y_rem_factor - buffer),
            )
        )


class XorNode(Node):
    """Model for the XOR nodes."""

    type: NodeType = NodeType.XOR
    heightRemFactor: RemFactor
    widthRemFactor: RemFactor
    innerText: Text | None = get_default_text("XOR")

    def __hash__(self) -> int:
        return hash(
            (
                self.type,
                self.xRemFactor,
                self.yRemFactor,
                self.heightRemFactor,
                self.widthRemFactor,
                self.innerText,
            )
        )

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, self.__class__):
            return NotImplemented
        return hash(self) == hash(other)

    def polygon(self, *, buffer: float = 0.0) -> Polygon:
        """
        Returns the polygon (ellipse) representation of the XOR's rectangle

        :param buffer: Increase the rectangle's dimensions by `buffer` in all directions
        :type buffer: float
        :return: The polygon representation of the ellipse
        :rtype: Polygon
        """
        _x_rem_factor = self.xRemFactor
        _y_rem_factor = self.yRemFactor
        _width_rem_factor = self.widthRemFactor
        _height_rem_factor = self.heightRemFactor

        center = Point(
            _x_rem_factor + _width_rem_factor / 2, _y_rem_factor + _height_rem_factor / 2
        )
        circle = center.buffer(_width_rem_factor / 2 + buffer)
        ellipse = affinity.scale(circle, xfact=1, yfact=_height_rem_factor / _width_rem_factor)
        return ellipse


class TextNode(Node):
    """Model for the text nodes."""

    type: NodeType = NodeType.TEXT
    innerText: Text | None = None

    def __hash__(self) -> int:
        return hash(
            (
                self.type,
                self.xRemFactor,
                self.yRemFactor,
                self.innerText,
            )
        )

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, self.__class__):
            return NotImplemented
        return hash(self) == hash(other)

    def polygon(self, *, buffer: float = 0.0) -> Polygon:
        """
        Returns the polygon representation of the text's rectangle

        :param buffer: Increase the rectangle's dimensions by `buffer` in all directions
        :type buffer: float
        :return: The polygon representation of the rectangle
        :rtype: Polygon
        """
        _x_rem_factor = self.xRemFactor
        _y_rem_factor = self.yRemFactor
        if self.innerText is not None:
            _width_rem_factor = self.innerText[2] * TEXT_NODE_BOUNDING_BOX_WIDTH_FACTOR
            _height_rem_factor = self.innerText[2] * TEXT_NODE_BOUNDING_BOX_HEIGHT_FACTOR
        else:
            _width_rem_factor = 0.0
            _height_rem_factor = 0.0

        return Polygon(
            (
                (_x_rem_factor - buffer, _y_rem_factor - buffer),  # top left corner
                (
                    _x_rem_factor - buffer,
                    _y_rem_factor + _height_rem_factor + buffer,
                ),  # bottom left corner
                (
                    _x_rem_factor + _width_rem_factor + buffer,
                    _y_rem_factor + _height_rem_factor + buffer,
                ),  # bottom right corner
                (
                    _x_rem_factor + _width_rem_factor + buffer,
                    _y_rem_factor - buffer,
                ),  # top right corner
                (_x_rem_factor - buffer, _y_rem_factor - buffer),  # top left corner
            )
        )


class WaypointNode(Node):
    """Model for the waypoint nodes."""

    type: NodeType = NodeType.WAYPOINT

    def __hash__(self) -> int:
        return hash(
            (
                self.type,
                self.xRemFactor,
                self.yRemFactor,
            )
        )

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, self.__class__):
            return NotImplemented
        return hash(self) == hash(other)


class ProtocolTypeName(Enum):
    """Enum for the supported protocol type names"""

    CAN = "CAN"
    CAN_250 = "CAN_250"
    CAN_500 = "CAN_500"
    CAN_800 = "CAN_800"
    CAN_FD = "CAN_FD"
    FLEX_RAY = "FLEX_RAY"
    ETHERNET = "ETHERNET"
    MOST_ELECTRIC = "MOST_ELECTRIC"
    LIN = "LIN"
    UNKNOWN = "UNKNOWN"
    OTHER = "OTHER"


class ProtocolType(BaseModel):
    """Model for the protocol types"""

    name: ProtocolTypeName
    feasibility_rating: Annotated[
        float,
        Field(
            ge=0.0,
            le=1.0,
            description="Evaluates how practical or likely it is for a specific \
                attack to succeed. Higher means more practical/likely.",
        ),
    ] = 1.0

    @staticmethod
    def lookup_by_color(
        color: Annotated[
            tuple[int, int, int], "The network's line color to resolve to a protocol type"
        ],
        color2protocol_type_map: Annotated[
            dict[tuple[int, int, int], ProtocolTypeName] | None,
            "Optional parameter to override default color map",
        ] = None,
    ) -> ProtocolType:
        """
        Looks ``ProtocolTypeName`` up for the provided ``color`` and generates
        matching ``ProtocolType``.
        """
        default_c2pt_map: dict[tuple[int, int, int], ProtocolTypeName] = {
            (255, 0, 0): ProtocolTypeName.CAN,
            (0, 0, 255): ProtocolTypeName.CAN_FD,
            (255, 153, 204): ProtocolTypeName.FLEX_RAY,
            (0, 153, 153): ProtocolTypeName.ETHERNET,
            (0, 255, 0): ProtocolTypeName.LIN,
            (255, 153, 0): ProtocolTypeName.MOST_ELECTRIC,
        }
        if not color2protocol_type_map:
            color2protocol_type_map = default_c2pt_map

        name = color2protocol_type_map.get(color, ProtocolTypeName.UNKNOWN)

        if name == ProtocolTypeName.UNKNOWN:
            logger.warning("Unknown network color %s", str(color))
        return ProtocolType(name=name)

    @staticmethod
    def lookup_by_label(
        label: Annotated[str, "The network label to resolve to a protocol type"],
        protocol_type_regexes: Annotated[
            dict[tuple[str, re.RegexFlag], ProtocolTypeName] | None,
            "Optional parameter to override default protocol type keywords",
        ] = None,
    ) -> ProtocolType:
        """
        Looks ``ProtocolTypeName`` up for the provided network ``label`` and
        generates matching ``ProtocolType``.
        """
        default_regexes: dict[tuple[str, re.RegexFlag], ProtocolTypeName] = {
            (r"\bCAN\b", re.IGNORECASE): ProtocolTypeName.CAN,
            (r"\bCAN\s+250\b", re.IGNORECASE): ProtocolTypeName.CAN_250,
            (r"\bCAN\s+500\b", re.IGNORECASE): ProtocolTypeName.CAN_500,
            (r"\bCAN\s+800\b", re.IGNORECASE): ProtocolTypeName.CAN_800,
            (r"\bCAN\s+\d+\s*\/\s*\d+\b", re.IGNORECASE): ProtocolTypeName.CAN_FD,
            (r"\bFlexRay\b", re.IGNORECASE): ProtocolTypeName.FLEX_RAY,
            (r"\bETHERNET\b", re.IGNORECASE): ProtocolTypeName.ETHERNET,
            (r"\bMOST\b", re.IGNORECASE): ProtocolTypeName.MOST_ELECTRIC,
            (r"\bLIN\b", re.IGNORECASE): ProtocolTypeName.LIN,
        }

        if not protocol_type_regexes:
            protocol_type_regexes = default_regexes

        max_length_match: tuple[int, ProtocolTypeName] = 0, ProtocolTypeName.UNKNOWN
        for r, proto in protocol_type_regexes.items():
            matches = (
                sum(len(m) for m in re.findall(pattern=r[0], string=label, flags=r[1])),
                proto,
            )
            max_length_match = max(max_length_match, matches, key=lambda x: x[0])

        if max_length_match[0] == 0 and len(label.strip()) > 0:
            max_length_match = 0, ProtocolTypeName.OTHER

        return ProtocolType(name=max_length_match[1])

    def __hash__(self) -> int:
        return hash((self.name, self.feasibility_rating))

    def __eq__(self, other: Any) -> bool:
        if isinstance(other, ProtocolType):
            return self.name == other.name and self.feasibility_rating == other.feasibility_rating
        return False


class NetworkDFFClassification(Enum):
    """Enum for the supported network classifications."""

    NEW_NW = "NEW_NW"
    NW_ONLY_IN_BR = "NW_ONLY_IN_BR"


class Network(BaseModel):
    """Model for the networks."""

    model_config = ConfigDict(extra="forbid")

    protocol_type: ProtocolType
    amg_only: bool = False
    dff_classification: NetworkDFFClassification | None = None
    edges: list[Edge]

    def __hash__(self) -> int:
        return hash((self.protocol_type, self.amg_only, self.dff_classification))


class Edge(BaseModel):
    """Model for the edges/links between ECUS."""

    model_config = ConfigDict(extra="forbid")

    sourceId: Annotated[UUID, UuidVersion(4)]
    targetId: Annotated[UUID, UuidVersion(4)]
    sourceAttachmentPointX: float | None = Field(
        default=None,
        ge=0.0,
        le=1.0,
        description="Origin is in upper left corner of the respective element, \
x increases to the right.",
    )
    sourceAttachmentPointY: float | None = Field(
        default=None,
        ge=0.0,
        le=1.0,
        description="Origin is in upper left corner of the respective element, \
y increases downwards.",
    )
    targetAttachmentPointX: float | None = Field(
        default=None,
        ge=0.0,
        le=1.0,
        description="Origin is in upper left corner of the respective element, \
x increases to the right.",
    )
    targetAttachmentPointY: float | None = Field(
        default=None,
        ge=0.0,
        le=1.0,
        description="Origin is in upper left corner of the respective element, \
y increases downwards.",
    )

    text: Text | None = None

    def __hash__(self) -> int:
        return hash(
            (
                self.sourceAttachmentPointX,
                self.sourceAttachmentPointY,
                self.targetAttachmentPointX,
                self.targetAttachmentPointY,
                self.text,
            )
        )


NodeUnionType = Union[WaypointNode, TextNode, XorNode, ComponentNode]


class Graph(BaseModel):
    """Model for the graphs of a car architecture."""

    model_config = ConfigDict(extra="forbid")

    label: Text
    nodes: dict[Annotated[UUID, UuidVersion(4)], NodeUnionType]
    networks: list[Network]

    @classmethod
    def get_network_tuple(cls, network: Network, graph: Graph) -> tuple[Network, tuple[Any, ...]]:
        """
        Get a tuple of (network, network_master, tuple[tuple[edge, source, target]])
        """
        nw_edges: set[tuple[Edge, Node, Node]] = set()
        for edge in network.edges:
            edge_source = graph.nodes.get(edge.sourceId)
            if edge_source is None:
                raise ReferenceError(f"Could not find source node {edge.sourceId}")
            edge_target = graph.nodes.get(edge.targetId)
            if edge_target is None:
                raise ReferenceError(f"Could not find target node {edge.targetId}")
            nw_edges.add((edge, edge_source, edge_target))

        return network, tuple(nw_edges)

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, self.__class__):
            return NotImplemented

        if not self.label == other.label:
            return False

        node_occurrences: dict[NodeUnionType, int] = {}

        # count all node_occurrences in self.nodes
        for node in self.nodes.values():
            if node in node_occurrences:
                node_occurrences[node] += 1
            else:
                node_occurrences[node] = 1

        # count all node_occurrences other.nodes
        for other_node in other.nodes.values():
            if other_node in node_occurrences:
                node_occurrences[other_node] -= 1
            else:
                return False

        if any(item != 0 for item in node_occurrences.values()):
            return False

        # count tuples of (network, network_master, list[tuple[edge, source, target]])
        network_occurences: dict[
            tuple[Network, tuple[tuple[Edge, Node, Node]]],
            int,
        ] = {}

        for network in self.networks:
            nw_tuple = self.get_network_tuple(network, self)
            if nw_tuple in network_occurences:
                network_occurences[nw_tuple] += 1
            else:
                network_occurences[nw_tuple] = 1

        for network in other.networks:
            nw_tuple = self.get_network_tuple(network, other)
            if nw_tuple in network_occurences:
                network_occurences[nw_tuple] -= 1
            else:
                return False

        if any(item != 0 for item in network_occurences.values()):
            return False

        return True


class AttackPathGraph(Graph):
    """Model for an attack path graph with corresponding entry point."""

    entry_technical_capability: TechnicalCapability
    entry_ecu: UUID
    target_ecu: UUID

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, self.__class__):
            return NotImplemented

        if self.entry_technical_capability != other.entry_technical_capability:
            return False

        if self.entry_ecu != other.entry_ecu:
            return False

        if self.target_ecu != other.target_ecu:
            return False

        return super().__eq__(other)


GraphType = TypeVar("GraphType", Graph, AttackPathGraph)


class GraphCollection(BaseModel, Generic[GraphType]):
    """Model for the collection of graphs."""

    model_config = ConfigDict(
        extra="forbid",
        title="Graph Schema",
    )

    graphs: list[GraphType]

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, self.__class__):
            return NotImplemented
        return self.graphs == other.graphs
