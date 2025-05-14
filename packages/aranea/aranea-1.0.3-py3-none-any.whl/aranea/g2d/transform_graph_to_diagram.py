"""
This module provides a model transformation (Graph-Model->XML-Model) for graphs.
"""

from aranea.g2d.transform_networks_to_mx_cells import \
    transform_networks_to_mx_cells
from aranea.g2d.transform_nodes_to_mx_cells import transform_nodes_to_mx_cells
from aranea.g2d.utils.get_graph_boundaries import (Boundaries,
                                                   get_graph_boundaries)
from aranea.g2d.utils.get_graph_key import get_graph_key
from aranea.g2d.utils.get_graph_label import get_graph_label
from aranea.g2d.utils.get_graph_model_page_size import \
    get_graph_model_page_size
from aranea.models.graph_model import Graph
from aranea.models.style_config_model import StyleConfig
from aranea.models.xml_model import (Diagram, MxCellEdge, MxCellShape,
                                     MxGraphModel, Root, RootCells)
from aranea.models.xml_model_utils import get_xml_layer


def transform_graph_to_diagram(graph: Graph, style_config: StyleConfig) -> Diagram:
    """
    Function to transform graphs to Diagrams.

    :param graph: The graph to transform.
    :type graph: Graph
    :param style_config: The StyleConfig to use for the transformation.
    :type style_config: StyleConfig
    :return: The corresponding Diagram.
    :rtype: Diagram
    """
    networks_mx_cells: list[MxCellEdge] = transform_networks_to_mx_cells(
        graph.networks, style_config
    )
    nodes_mx_cells: list[MxCellShape] = transform_nodes_to_mx_cells(graph.nodes, style_config)

    graph_boundaries: Boundaries = get_graph_boundaries(nodes_mx_cells)
    key_mx_cells, key_outline_mx_cell = get_graph_key(style_config, graph_boundaries)
    label_mx_cell: MxCellShape = get_graph_label(
        graph.label, graph_boundaries, style_config.rem_size
    )

    boundaries: Boundaries = get_graph_boundaries(
        nodes_mx_cells + [label_mx_cell] + [key_outline_mx_cell]
    )
    page_size_width, page_size_height = get_graph_model_page_size(boundaries, style_config)

    layer_wrapped_cells: list[RootCells] = get_xml_layer(
        networks_mx_cells + nodes_mx_cells + [label_mx_cell] + key_mx_cells
    )

    root_element: Root = Root(
        cells=layer_wrapped_cells,
    )

    mx_graph_model: MxGraphModel = MxGraphModel(
        root=root_element,
        attr_page_width=page_size_width,
        attr_page_height=page_size_height,
    )

    diagram: Diagram = Diagram(
        attr_name=graph.label[0],
        graph_model=mx_graph_model,
    )

    return diagram
