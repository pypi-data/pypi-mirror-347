"""
Module for getting the key of a graph depending on the StyleConfig and the Boundaries of the graph.
"""

from aranea.g2d.transform_waypoint_node_to_mx_cell import \
    DEFAULT_WAYPOINT_DIMENSION
from aranea.g2d.utils.get_graph_boundaries import Boundaries
from aranea.models.custom_xml_shapes.icons import IconFactory, IconIdentifier
from aranea.models.graph_model import (EcuClassification,
                                       EcuClassificationName,
                                       NetworkDFFClassification, NodeType,
                                       ProtocolType, ProtocolTypeName)
from aranea.models.style_config_model import StyleConfig, map_color_descriptor
from aranea.models.xml_model import (MxCell, MxCellEdge, MxCellShape,
                                     MxCellStyle, MxCellStyleAlign,
                                     MxCellStyleArrow, MxCellStyleDefaultShape,
                                     MxCellStyleVerticalAlign,
                                     MxCellWhiteSpace, MxGeometryEdge,
                                     MxGeometryShape)

DEFAULT_OUTER_SPACING_MULTIPLIER = 4
DEFAULT_ITEM_WIDTH_MULTIPLIER = 8
DEFAULT_ITEM_HEIGHT_MULTIPLIER = 5
DEFAULT_HEADLINE_SIZE_MULTIPLIER = 3
ITEMS_PER_ROW = 4


def get_graph_key(
    style_config: StyleConfig, graph_boundaries: Boundaries
) -> tuple[list[MxCell], MxCellShape]:
    """
    Function to get the key of a graph.
    Key is set at the upper right corner of the graph.

    :param style_config: The StyleConfig to use for the key.
    :type style_config: StyleConfig
    :param graph_boundaries: The boundaries of the graph.
    :type graph_boundaries: Boundaries

    :return: The key of the graph and the outer MxCell for Boundary calculation.
    :rtype: tuple[list[MxCell], MxCellShape]
    """
    key_mx_cells: list[MxCell] = []

    # boundaries are [[min x, min y], [max x, max y]]
    key_boundaries: list[list[float]] = [
        [
            # max x + outer spacing
            graph_boundaries[1][0] + style_config.rem_size * DEFAULT_OUTER_SPACING_MULTIPLIER,
            # min y + outer spacing
            graph_boundaries[0][1] + style_config.rem_size * DEFAULT_OUTER_SPACING_MULTIPLIER,
        ],
        [
            # max x + outer spacing + width of items * number of items
            # + inner spacings * (number of items + 1)
            graph_boundaries[1][0]
            + style_config.rem_size * DEFAULT_OUTER_SPACING_MULTIPLIER
            + style_config.rem_size * DEFAULT_ITEM_WIDTH_MULTIPLIER * ITEMS_PER_ROW
            + style_config.rem_size * (ITEMS_PER_ROW + 1),
            0,  # calculated later
        ],
    ]
    key_width = key_boundaries[1][0] - key_boundaries[0][0]

    # headline, spanning the whole width of the key
    headline_mx_cell = MxCellShape(
        attr_value="Key",
        attr_style=MxCellStyle(
            shape=MxCellStyleDefaultShape.TEXT,
            fontSize=style_config.rem_size * DEFAULT_HEADLINE_SIZE_MULTIPLIER,
            align=MxCellStyleAlign.CENTER,
            strokeColor="none",
        ).to_semicolon_string(),
        geometry=MxGeometryShape(
            attr_x=key_boundaries[0][0] + style_config.rem_size,
            attr_y=key_boundaries[0][1] + style_config.rem_size,
            attr_width=key_width - style_config.rem_size * 2,  # small margin on both sides
            attr_height=style_config.rem_size * DEFAULT_HEADLINE_SIZE_MULTIPLIER,
        ),
    )
    key_mx_cells.append(headline_mx_cell)

    # Networks, on the left beneath the headline
    network_boundaries: list[list[float]] = [
        [
            key_boundaries[0][0] + style_config.rem_size,
            headline_mx_cell.geometry.attr_y
            + headline_mx_cell.geometry.attr_height
            + style_config.rem_size,
        ],
        [
            key_boundaries[1][0] - key_width / 2 - style_config.rem_size,
            0,  # calculated in get_networks_mx_cells
        ],
    ]
    key_mx_cells += get_networks_mx_cells(style_config, network_boundaries)

    # Icons, on the right beneath the headline
    icon_boundaries: list[list[float]] = [
        [network_boundaries[1][0] + style_config.rem_size, network_boundaries[0][1]],
        [key_boundaries[1][0] - style_config.rem_size, 0],  # calculated in get_icons_mx_cells
    ]
    key_mx_cells += get_icons_mx_cells(style_config, icon_boundaries)

    # get max height of networks and icons to know where to place components
    components_min_y = max(network_boundaries[1][1], icon_boundaries[1][1])

    # Components, beneath the networks and icons spanning the whole width
    components_boundaries: list[list[float]] = [
        [key_boundaries[0][0] + style_config.rem_size, components_min_y + style_config.rem_size],
        [key_boundaries[1][0] - style_config.rem_size, 0],  # calculated in get_components_mx_cells
    ]
    key_mx_cells += get_components_mx_cells(style_config, components_boundaries)

    key_boundaries[1][1] = components_boundaries[1][1] + style_config.rem_size

    # outer rectangle
    outer_rectangle_mx_cell = MxCellShape(
        attr_style=MxCellStyle(
            shape=MxCellStyleDefaultShape.RECTANGLE,
            fillColor="#FFFFFF",
            strokeColor="#000000",
        ).to_semicolon_string(),
        geometry=MxGeometryShape(
            attr_x=key_boundaries[0][0],
            attr_y=key_boundaries[0][1],
            attr_width=key_width,
            attr_height=key_boundaries[1][1] - key_boundaries[0][1],
        ),
    )
    key_mx_cells = [outer_rectangle_mx_cell] + key_mx_cells

    return (key_mx_cells, outer_rectangle_mx_cell)


def get_components_mx_cells(
    style_config: StyleConfig, components_boundaries: list[list[float]]
) -> list[MxCellShape]:
    """
    Function to get the components in the key.

    :param style_config: The StyleConfig to use for the components.
    :type style_config: StyleConfig
    :param components_boundaries: The boundaries of the components, margins already factored in.
    :type components_boundaries: list[list[float]]

    :return: The components of the graph.
    :rtype: list[MxCellShape]
    """
    components_mx_cells: list[MxCellShape] = []

    component_values: list[tuple[EcuClassification, str]] = [
        (EcuClassification(name=EcuClassificationName.NEW_ECU), "New ECU"),
        (EcuClassification(name=EcuClassificationName.ECU), "ECU"),
        (EcuClassification(name=EcuClassificationName.DOMAIN_GATEWAY), "Domain Gateway"),
        (EcuClassification(name=EcuClassificationName.ENTRY_POINT), "Entry Point"),
        (EcuClassification(name=EcuClassificationName.ECU_ONLY_IN_BR), "ECU only in previous BR"),
        (EcuClassification(name=EcuClassificationName.LIN_CONNECTED_ECU), "LIN connected ECU"),
        (EcuClassification(name=EcuClassificationName.NON_DOMAIN_GATEWAY), "Non-Domain Gateway"),
        (EcuClassification(name=EcuClassificationName.CRITICAL_ELEMENT), "Critical Element"),
    ]

    # fill in components from top left to bottom right
    current_x = components_boundaries[0][0]
    current_y = components_boundaries[0][1] + style_config.rem_size
    for classification, text in component_values:
        component = MxCellShape(
            attr_value=text,
            attr_style=style_config.get_mx_cell_style(
                node_type=NodeType.COMPONENT, node_classifications=[classification]
            ).to_semicolon_string(),
            geometry=MxGeometryShape(
                attr_x=current_x,
                attr_y=current_y,
                attr_width=style_config.rem_size * DEFAULT_ITEM_WIDTH_MULTIPLIER,
                attr_height=style_config.rem_size * DEFAULT_ITEM_HEIGHT_MULTIPLIER,
            ),
        )
        components_mx_cells.append(component)

        # calculate position of next component
        current_x += style_config.rem_size * DEFAULT_ITEM_WIDTH_MULTIPLIER + style_config.rem_size
        if current_x >= components_boundaries[1][0]:
            current_x = components_boundaries[0][0]
            current_y += style_config.rem_size * (DEFAULT_ITEM_HEIGHT_MULTIPLIER + 1)

    if current_x == components_boundaries[0][0]:
        components_boundaries[1][1] = current_y
    else:
        components_boundaries[1][1] = current_y + style_config.rem_size * (
            DEFAULT_ITEM_HEIGHT_MULTIPLIER + 1
        )
    return components_mx_cells


def get_networks_mx_cells(
    style_config: StyleConfig, network_boundaries: list[list[float]]
) -> list[MxCell]:
    """
    Function to get the networks in the key.

    :param style_config: The StyleConfig to use for the networks.
    :type style_config: StyleConfig
    :param network_boundaries: The boundaries of the networks, margins already factored in.
    :type network_boundaries: list[list[float]]

    :return: The networks of the graph.
    :rtype: list[MxCell]
    """
    networks_mx_cells: list[MxCell] = []

    network_height = style_config.rem_size * DEFAULT_ITEM_HEIGHT_MULTIPLIER / 2

    network_values: list[tuple[ProtocolType | NetworkDFFClassification, str]] = [
        (ProtocolType(name=ProtocolTypeName.CAN_250), "CAN 250"),
        (ProtocolType(name=ProtocolTypeName.CAN_500), "CAN 500"),
        (ProtocolType(name=ProtocolTypeName.CAN_800), "CAN 800"),
        (ProtocolType(name=ProtocolTypeName.CAN_FD), "CAN FD"),
        (ProtocolType(name=ProtocolTypeName.FLEX_RAY), "FlexRay"),
        (ProtocolType(name=ProtocolTypeName.ETHERNET), "Ethernet"),
        (ProtocolType(name=ProtocolTypeName.MOST_ELECTRIC), "MOST electric"),
        (ProtocolType(name=ProtocolTypeName.LIN), "LIN"),
        (NetworkDFFClassification.NEW_NW, "New Network"),
        (NetworkDFFClassification.NW_ONLY_IN_BR, "Network only in previous BR"),
    ]

    # fill in networks from top to bottom
    current_y = network_boundaries[0][1] + style_config.rem_size
    for nw_type, text in network_values:
        # generate waypoints for edge
        waypoints: list[MxCellShape] = []  # temporary list for current edge
        for i in range(2):
            waypoint_mx_cell = MxCellShape(
                attr_style=style_config.get_mx_cell_style(
                    node_type=NodeType.WAYPOINT
                ).to_semicolon_string(),
                geometry=MxGeometryShape(
                    attr_x=network_boundaries[0][0] - DEFAULT_WAYPOINT_DIMENSION / 2,
                    attr_y=current_y + network_height / 2 - DEFAULT_WAYPOINT_DIMENSION / 2,
                    attr_height=DEFAULT_WAYPOINT_DIMENSION,
                    attr_width=DEFAULT_WAYPOINT_DIMENSION,
                ),
            )
            if i == 1:
                waypoint_mx_cell.geometry.attr_x += (
                    DEFAULT_ITEM_WIDTH_MULTIPLIER * style_config.rem_size
                )
            waypoints.append(waypoint_mx_cell)
            networks_mx_cells.append(waypoint_mx_cell)

        # generate edge
        if isinstance(nw_type, ProtocolType):
            edge_style = style_config.get_mx_cell_style(
                protocol_type=nw_type,
            )
        else:
            edge_style = style_config.get_mx_cell_style(
                network_dff_classification=nw_type,
            )
            edge_style.startArrow = MxCellStyleArrow.NONE
            edge_style.endArrow = MxCellStyleArrow.NONE

        edge_mx_cell = MxCellEdge(
            attr_style=edge_style.to_semicolon_string(),
            attr_source=waypoints[0].attr_id,
            attr_target=waypoints[1].attr_id,
            geometry=MxGeometryEdge(),
        )
        networks_mx_cells.append(edge_mx_cell)

        # generate text next to edge
        font_color = None
        protocol = None
        if style_config.network_protocol_type_style_attributes:
            protocol = (
                style_config.network_protocol_type_style_attributes.get(nw_type.name, None)
                if isinstance(nw_type, ProtocolType)
                else None
            )
        if protocol:
            font_color = map_color_descriptor(protocol.stroke_color)

        text_mx_cell = MxCellShape(
            attr_value=text,
            attr_style=MxCellStyle(
                shape=MxCellStyleDefaultShape.TEXT,
                fontSize=style_config.rem_size,
                fontColor=font_color,
                align=MxCellStyleAlign.CENTER,
                verticalAlign=MxCellStyleVerticalAlign.MIDDLE,
                strokeColor="none",
                whiteSpace=MxCellWhiteSpace.WRAP,
            ).to_semicolon_string(),
            geometry=MxGeometryShape(
                attr_x=network_boundaries[0][0]
                + style_config.rem_size * (DEFAULT_ITEM_WIDTH_MULTIPLIER + 1),
                attr_y=current_y,
                attr_width=style_config.rem_size * DEFAULT_ITEM_WIDTH_MULTIPLIER,
                attr_height=network_height,
            ),
        )
        networks_mx_cells.append(text_mx_cell)

        # set current_y to next line
        current_y += network_height + style_config.rem_size

    network_boundaries[1][1] = current_y
    return networks_mx_cells


def get_icons_mx_cells(
    style_config: StyleConfig, icons_boundaries: list[list[float]]
) -> list[MxCellShape]:
    """
    Function to get the icons in the key.

    :param style_config: The StyleConfig to use for the icons.
    :type style_config: StyleConfig
    :param icons_boundaries: The boundaries for the icons, margins already factored in.
    :type icons_boundaries: list[list[float]]

    :return: The icons of the graph.
    :rtype: list[MxCellShape]
    """
    icons_mx_cells: list[MxCellShape] = []

    icon_height = style_config.rem_size * DEFAULT_ITEM_HEIGHT_MULTIPLIER / 2

    icon_values: list[tuple[IconIdentifier, str]] = [
        (IconIdentifier.AMG, "AMG"),
        (IconIdentifier.NETWORK_SWITCH, "Switch"),
        (IconIdentifier.BACKEND, "Backend"),
        (IconIdentifier.CELLULAR, "2/3/4/5G"),
        (IconIdentifier.WIFI, "WLAN"),
        (IconIdentifier.BLUETOOTH, "Bluetooth"),
        (IconIdentifier.USB, "USB"),
        (IconIdentifier.SATELLITE, "GNSS"),
        (IconIdentifier.CAR_CHARGER, "PLC, GBT, ..."),
        (IconIdentifier.DIGITAL_BROADCAST, "DVB-C, DVB-T, DAB"),
        (IconIdentifier.ANALOG_BROADCAST, "Radio, UWB"),
        (IconIdentifier.NFC, "NFC"),
    ]

    # fill in icons from top to bottom
    icon_factory = IconFactory()
    current_y = icons_boundaries[0][1] + style_config.rem_size
    for icon_identifier, text in icon_values:
        # generate icon
        icon_mx_cell = MxCellShape(
            attr_style=MxCellStyle(
                shape=MxCellStyleDefaultShape.IMAGE,
                image=icon_factory.get_icon_str(icon_identifier),
            ).to_semicolon_string(),
            geometry=MxGeometryShape(
                attr_x=icons_boundaries[0][0]
                + style_config.rem_size * DEFAULT_ITEM_WIDTH_MULTIPLIER / 2
                - icon_height / 2,
                attr_y=current_y,
                attr_height=icon_height,
                attr_width=icon_height,
            ),
        )
        icons_mx_cells.append(icon_mx_cell)

        # generate text next to icon
        text_mx_cell = MxCellShape(
            attr_value=text,
            attr_style=MxCellStyle(
                shape=MxCellStyleDefaultShape.TEXT,
                fontSize=style_config.rem_size,
                align=MxCellStyleAlign.CENTER,
                verticalAlign=MxCellStyleVerticalAlign.MIDDLE,
                strokeColor="none",
                whiteSpace=MxCellWhiteSpace.WRAP,
            ).to_semicolon_string(),
            geometry=MxGeometryShape(
                attr_x=icons_boundaries[0][0]
                + style_config.rem_size * (DEFAULT_ITEM_WIDTH_MULTIPLIER + 1),
                attr_y=current_y,
                attr_width=style_config.rem_size * DEFAULT_ITEM_WIDTH_MULTIPLIER,
                attr_height=icon_height,
            ),
        )
        icons_mx_cells.append(text_mx_cell)

        # set current_y to next line
        current_y += icon_height + style_config.rem_size

    icons_boundaries[1][1] = current_y
    return icons_mx_cells
