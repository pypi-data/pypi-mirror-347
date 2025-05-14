"""
Module containing the NodePlacer class for intelligent placement of ComponentNodes in a given 
Network, contained in a given Graph conforming to the pydantic model.
"""

from enum import Enum
from typing import Optional, TypedDict
from uuid import UUID, uuid4

from rtree import index
from shapely.geometry import LineString, Point, Polygon

from aranea.dff.utils import (AttachmentPoint, EdgeDirection,
                              create_edge_with_attachment_point,
                              get_connected_edges_of_node, get_edge_direction,
                              get_edge_line, get_edge_polygon_from_line,
                              get_graph_boundaries,
                              get_mean_edge_strokewidth_from_config,
                              get_network_element_ids, get_waypoint_polygon,
                              sort_network_edges_by_length)
from aranea.g2d.style_configs.get_default_style_config import \
    get_default_style_config
from aranea.models.graph_model import (ComponentNode, Edge, Graph, Network,
                                       WaypointNode)


class IntersectionType(Enum):
    """
    Possible types of intersections.
    """

    NODE = "node"
    EDGE = "edge"
    NONE = "none"


class PlacedElements(TypedDict):
    """
    Dictionary containing placed elements.
    """

    node_id: UUID
    waypoint_id: Optional[UUID]
    edges: Optional[list[Edge]]


class NodePlacer:
    """
    Intelligent placement handler for adding ComponentNodes to networks in a graph.

    Implements a three-stage placement strategy:
    1. Replace single-connection waypoints with new node
    2. Edge-adjacent placement with collision avoidance
    3. Grid-based fallback placement below existing graph
    """

    def __init__(self, graph: Graph):
        """
        Initialize the NodePlacer with a given graph and setup spatial indices.

        :param graph: The graph to place nodes into
        :type graph: Graph
        """
        self.graph = graph
        # Default style config used as I don't have the actual style config
        self.style_config = get_default_style_config()
        self.mean_edge_stroke_width = get_mean_edge_strokewidth_from_config(self.style_config)

        # Spatial indices for collision detection
        self.node_index = self._build_node_rtree()
        self.edge_index = self._build_edge_rtree()

        # Initialize (fallback) grid placement stage
        self._init_grid_placement_state()

        # Sort network edges by length for processing priority
        # Long edges should provide more placement opportunities
        for network in self.graph.networks:
            sort_network_edges_by_length(network, self.graph)

    def _init_grid_placement_state(self) -> None:
        """
        Initialize the grid placement state variables for stage 3 / fallback placement.

        Calculates the initial grid boundaries based on the current graph's nodes
        and sets up coordinates for grid-based node placement.

        :rtype: None
        """
        self.stage3_row_height = 0.0  # changed dynamically based on node heights
        # default spacing in rem units -
        # chosen as with the default style config nodes have a height of approximately 3 rem
        self.stage3_node_spacing = 2.0
        boundaries = get_graph_boundaries(self.graph)
        self.stage3_min_x = boundaries[0][0]
        self.stage3_current_x = self.stage3_min_x
        self.stage3_current_y = boundaries[1][1] + self.stage3_node_spacing
        self.original_width = boundaries[1][0] - boundaries[0][0]

    def _build_node_rtree(self) -> index.Index:
        """
        Build an R-tree index for all nodes in the graph.

        :return: R-tree index containing node bounding boxes
        :rtype: index.Index
        """
        idx = index.Index()
        for node_id, node in self.graph.nodes.items():
            if isinstance(node, WaypointNode):
                poly = get_waypoint_polygon(node)
            else:
                poly = node.polygon()
            idx.insert(int(node_id), poly.bounds)
        return idx

    def _build_edge_rtree(self) -> index.Index:
        """
        Build an R-tree index for all edges in the graph's networks.

        :return: R-tree index containing edge bounding boxes
        :rtype: index.Index
        """
        idx = index.Index()
        for network in self.graph.networks:
            for edge in network.edges:
                self._index_edge(edge, idx)
        return idx

    def _index_edge(self, edge: Edge, idx: index.Index) -> None:
        """
        Add a single edge to the spatial index.

        :param edge: Edge to index
        :type edge: Edge
        :param idx: R-tree index to modify
        :type idx: index.Index
        """
        edge_line = get_edge_line(edge, self.graph)
        edge_poly = get_edge_polygon_from_line(edge_line, self.mean_edge_stroke_width)
        idx.insert(int(edge.sourceId) + int(edge.targetId), edge_poly.bounds)

    def _check_collisions(self, geometry: Polygon) -> IntersectionType:
        """
        Check for collisions between a geometry and existing graph elements.

        :param geometry: Geometry to check for collisions
        :type geometry: Polygon
        :return: Type of detected collision
        :rtype: IntersectionType
        """
        if any(self.node_index.intersection(geometry.bounds)):
            return IntersectionType.NODE
        if any(self.edge_index.intersection(geometry.bounds)):
            return IntersectionType.EDGE
        return IntersectionType.NONE

    def _try_waypoint_replacement(
        self, network: Network, new_node: ComponentNode
    ) -> Optional[PlacedElements]:
        """
        Stage 1: Attempt to replace a single-connection waypoint with the new component node.

        Checks each waypoint in the network. If a waypoint has exactly one connected edge,
        calculates a position for the new node based on edge direction and checks for collisions.
        If no collision is found, replaces the waypoint with the new node and updates the graph
        inplace.

        :param network: Network to attempt replacement in, has to be in graph given to NodePlacer
        :type network: Network
        :param new_node: Component node to place in the network
        :type new_node: ComponentNode
        :return: Placement details if successful, None otherwise
        :rtype: Optional[PlacedElements]
        """
        for node_id in get_network_element_ids(network):
            node = self.graph.nodes.get(node_id)
            if not isinstance(node, WaypointNode):
                continue

            # rename for better readability
            waypoint_id = node_id

            connected_edges = get_connected_edges_of_node(waypoint_id, network)
            if len(connected_edges) != 1:
                continue

            edge = connected_edges.pop()
            edge_dir = get_edge_direction(edge, waypoint_id, self.graph)
            wp_center = Point(node.xRemFactor, node.yRemFactor)

            # Calculate new node position based on edge direction
            new_pos = self._calculate_replacement_position(wp_center, new_node, edge_dir)
            new_node.xRemFactor, new_node.yRemFactor = new_pos

            if self._validate_placement(new_node, waypoint_id, edge):
                return self._finalize_waypoint_replacement(waypoint_id, new_node, edge)

        return None

    def _calculate_replacement_position(
        self, wp_center: Point, new_node: ComponentNode, edge_dir: EdgeDirection
    ) -> tuple[float, float]:
        """
        Calculate the position for a new node to replace a waypoint based on edge direction.

        :param wp_center: Center of the waypoint being replaced
        :type wp_center: Point
        :param new_node: Component node to place
        :type new_node: ComponentNode
        :param edge_dir: Direction of the edge from the waypoint
        :type edge_dir: EdgeDirection

        :return: Calculated (x, y) position in rem factors
        :rtype: tuple[float, float]
        """
        match edge_dir:
            case EdgeDirection.UP:  # viewed from the waypoint/new node
                return wp_center.x - new_node.widthRemFactor / 2.0, wp_center.y
            case EdgeDirection.DOWN:
                return (
                    wp_center.x - new_node.widthRemFactor / 2.0,
                    wp_center.y - new_node.heightRemFactor,
                )
            case EdgeDirection.LEFT:
                return wp_center.x, wp_center.y - new_node.heightRemFactor / 2.0
            case EdgeDirection.RIGHT:
                return (
                    wp_center.x - new_node.widthRemFactor,
                    wp_center.y - new_node.heightRemFactor / 2.0,
                )

    def _validate_placement(
        self, new_node: ComponentNode, waypoint_node_id: UUID, connected_edge: Edge
    ) -> bool:
        """
        Validate that a new node placement doesn't cause collisions.

        :param new_node: Proposed new node
        :type new_node: ComponentNode
        :param old_node_id: UUID of node being replaced
        :type old_node_id: UUID
        :return: True if placement is valid, False otherwise
        :rtype: bool
        """
        new_poly = new_node.polygon()
        waypoint_node = self.graph.nodes[waypoint_node_id]
        if not isinstance(waypoint_node, WaypointNode):
            raise TypeError(f"Node with ID {waypoint_node_id} is not a WaypointNode")
        waypoint_poly = get_waypoint_polygon(waypoint_node)
        edge_line = get_edge_line(connected_edge, self.graph)
        edge_poly = get_edge_polygon_from_line(edge_line, self.mean_edge_stroke_width)
        edge_index_id = int(connected_edge.sourceId) + int(connected_edge.targetId)

        # Temporarily update index for collision check
        # Edge needs to be removed because the stroke width causes it to collide with new node
        self.node_index.delete(int(waypoint_node_id), waypoint_poly.bounds)
        self.edge_index.delete(edge_index_id, edge_poly.bounds)
        collision = self._check_collisions(new_poly)
        self.node_index.insert(int(waypoint_node_id), waypoint_poly.bounds)
        self.edge_index.insert(edge_index_id, edge_poly.bounds)

        return collision == IntersectionType.NONE

    def _finalize_waypoint_replacement(
        self, waypoint_id: UUID, new_node: ComponentNode, edge: Edge
    ) -> PlacedElements:
        """
        Finalize the replacement of a waypoint with a new component node.

        :param waypoint_id: UUID of the waypoint being replaced
        :type waypoint_id: UUID
        :param new_node: New component node which replaces the waypoint
        :type new_node: ComponentNode
        :param edge: Edge connected to the waypoint
        :type edge: Edge
        :return: Placement details
        :rtype: PlacedElements
        """
        new_node_id = uuid4()
        waypoint_node = self.graph.nodes[waypoint_id]
        if not isinstance(waypoint_node, WaypointNode):
            raise TypeError(f"Node with ID {waypoint_id} is not a WaypointNode")
        old_poly = get_waypoint_polygon(waypoint_node)

        # Update graph elements
        self.graph.nodes[new_node_id] = new_node
        del self.graph.nodes[waypoint_id]  # deleting waypoint_node does not work here

        # Update edge connections
        if edge.sourceId == waypoint_id:
            edge.sourceId = new_node_id
        else:
            edge.targetId = new_node_id

        # Update spatial index
        self.node_index.delete(int(waypoint_id), old_poly.bounds)
        self.node_index.insert(int(new_node_id), new_node.polygon().bounds)

        return {"node_id": new_node_id, "waypoint_id": None, "edges": None}

    def _try_placement_next_to_edge(
        self, edge: Edge, network: Network, new_node: ComponentNode
    ) -> Optional[PlacedElements]:
        """
        Stage 2: Attempt edge-adjacent placement with collision checks and backup strategy.

        Tries to place a new node next to an edge, avoiding collisions with existing nodes and
        edges. If no valid placement is found, a backup strategy is used to find the best
        possible placement. This is the placement where the new edge has the least intersections
        with existing edges while the new node is not allowed to intersect.
        Returns placement details if successful, None otherwise.

        :param edge: Target edge to place the new node next to, must be in the given network
        :type edge: Edge
        :param network: Network containing the given edge, must be in the graph given to NodePlacer
        :type network: Network
        :param new_node: Component node to place next to the edge and insert into the network
        :type new_node: ComponentNode
        :return: Placement details if successful, None otherwise
        :rtype: Optional[PlacedElements]
        """
        if edge not in network.edges:
            raise ValueError("Given edge is not in the given network.")

        edge_direction = get_edge_direction(edge, edge.sourceId, self.graph)
        edge_line = get_edge_line(edge, self.graph)

        backup_placement = None  # Placement where new edge has least edge intersections
        min_intersections = float("inf")

        # remove edge from spatial index during placement as it should be replaced
        edge_index_id = int(edge.sourceId) + int(edge.targetId)
        edge_poly = get_edge_polygon_from_line(edge_line, self.mean_edge_stroke_width)
        self.edge_index.delete(edge_index_id, edge_poly.bounds)

        for waypoint_center in self._generate_edge_points(edge_line, edge_direction, new_node):
            for pos, node_attachment_point in self._generate_candidate_positions(
                waypoint_center, new_node, edge_direction
            ):
                # Check node collisions
                new_node.xRemFactor, new_node.yRemFactor = pos.x, pos.y
                new_node_poly = new_node.polygon()
                if self._check_collisions(new_node_poly) != IntersectionType.NONE:
                    continue

                # Check edge collisions
                new_edge_line = LineString([new_node_poly.centroid, waypoint_center])
                new_edge_poly = get_edge_polygon_from_line(
                    new_edge_line, self.mean_edge_stroke_width
                )
                if (
                    edge_intersection_type := self._check_collisions(new_edge_poly)
                ) == IntersectionType.NONE:
                    return self._create_edge_connection(
                        new_node, waypoint_center, node_attachment_point, edge, network
                    )
                if edge_intersection_type == IntersectionType.EDGE:
                    edge_intersections = self._count_edge_intersections(new_edge_poly)
                    if edge_intersections < min_intersections:
                        backup_placement = pos, node_attachment_point, waypoint_center
                        min_intersections = edge_intersections
                else:
                    # Edge intersects with node -> skip this position
                    continue

        if backup_placement and min_intersections < float("inf"):
            pos, attachment, waypoint_center = backup_placement
            new_node.xRemFactor, new_node.yRemFactor = pos.x, pos.y
            return self._create_edge_connection(
                new_node, waypoint_center, attachment, edge, network
            )

        # No valid placement found -> restore edge index
        self.edge_index.insert(edge_index_id, edge_poly.bounds)
        return None

    def _count_edge_intersections(self, poly: Polygon) -> int:
        """
        Count intersections of given polygon with edges in the edge index.

        :param poly: Polygon to check for intersections
        :type poly: Polygon

        :return: Number of intersections
        :rtype: int
        """
        count: int = sum(1 for _ in self.edge_index.intersection(poly.bounds))
        return count

    def _generate_edge_points(
        self,
        edge_line: LineString,
        edge_direction: EdgeDirection,
        new_node: ComponentNode,
    ) -> list[Point]:
        """
        Generate potential connection points along an edge line.
        Takes the size of the new node into account to space the points.

        :param edge_line: Edge line to generate points along
        :type edge_line: LineString
        :param edge_direction: Direction of the edge viewed from a connected node
        :type edge_direction: EdgeDirection
        :param new_node: Component node to place next to the edge
        :type new_node: ComponentNode

        :return: List of sampled points
        :rtype: list[Point]
        """
        # Below constant determines how many times the node's size to space the points
        # Decided to use 0.5 as this feels like a good balance between hopping over potential points
        # and not missing any
        SPACING_FACTOR: float = 0.5  # pylint: disable=invalid-name

        if edge_direction in (EdgeDirection.UP, EdgeDirection.DOWN):  # vertical edge
            node_spacing = new_node.heightRemFactor * SPACING_FACTOR
        else:  # horizontal edge
            node_spacing = new_node.widthRemFactor * SPACING_FACTOR
        num_points = max(1, int(edge_line.length // node_spacing))
        # Don't include the 0-th and n-th point, as they are the connection points to nodes
        return [edge_line.interpolate(i * node_spacing) for i in range(1, num_points - 1)]

    def _generate_candidate_positions(
        self, point: Point, new_node: ComponentNode, edge_dir: EdgeDirection
    ) -> list[tuple[Point, AttachmentPoint]]:
        """
        Generate candidate positions for a ComponentNode relative to a given point on an edge.
        This point is intended to be the center of a waypoint.
        Takes the edge direction and the nodes size into account.
        Thus a candidate position is a tuple of a point and an attachment point where an edge could
        connect the new node to the given point.

        :param center: Point along edge, where the new node would be connected to the edge
        :type center: Point
        :param new_node: Component node to place
        :type new_node: ComponentNode
        :param edge_dir: Direction of the edge the given point is on, viewed from any connected node
        :type edge_dir: EdgeDirection

        :return: List of candidate (position, attachment point) tuples
        :rtype: list[tuple[Point, AttachmentPoint]]
        """
        spacing_to_edge: float = 2.0
        positions: list[tuple[Point, AttachmentPoint]] = []
        if edge_dir in (EdgeDirection.UP, EdgeDirection.DOWN):  # vertical edge
            positions.extend(
                [
                    (
                        Point(
                            point.x - new_node.widthRemFactor - spacing_to_edge,
                            point.y - new_node.heightRemFactor / 2.0,
                        ),
                        AttachmentPoint.RIGHT,
                    ),
                    (
                        Point(point.x + spacing_to_edge, point.y - new_node.heightRemFactor / 2.0),
                        AttachmentPoint.LEFT,
                    ),
                ]
            )
        else:  # horizontal edge
            positions.extend(
                [
                    (
                        Point(
                            point.x - new_node.widthRemFactor / 2.0,
                            point.y - new_node.heightRemFactor - spacing_to_edge,
                        ),
                        AttachmentPoint.BOTTOM,
                    ),
                    (
                        Point(point.x - new_node.widthRemFactor / 2.0, point.y + spacing_to_edge),
                        AttachmentPoint.TOP,
                    ),
                ]
            )
        return positions

    def _create_edge_connection(
        self,
        new_node: ComponentNode,
        new_waypoint_center: Point,
        new_node_attachment_point: AttachmentPoint,
        old_edge: Edge,
        network: Network,
    ) -> PlacedElements:
        """
        Create new edges and waypoint for a validated placement.

        :param new_node: New component node
        :type new_node: ComponentNode
        :param waypoint_center: Center point for new waypoint
        :type waypoint_center: Point
        :param node_attachment_point: Attachment point on new node
        :type node_attachment_point: AttachmentPoint
        :param old_edge: Original edge being split, has to be in the given network
        :type old_edge: Edge
        :param network: Network to connect new node to, has to be in the graph given to NodePlacer
        :type network: Network
        :return: Placement details
        :rtype: PlacedElements
        """
        if old_edge not in network.edges:
            raise ValueError("Given old_edge is not in the given network.")

        new_node_id = uuid4()
        waypoint_id = uuid4()

        # Create new elements
        self.graph.nodes[new_node_id] = new_node
        new_waypoint = WaypointNode(
            xRemFactor=new_waypoint_center.x, yRemFactor=new_waypoint_center.y
        )
        self.graph.nodes[waypoint_id] = new_waypoint

        # Create edges
        component_edge = create_edge_with_attachment_point(
            new_node_id, waypoint_id, new_node_attachment_point
        )
        # Split the old edge into two new edges, connecting to the new waypoint
        # keep the attachment points of the old edge
        split_edges = [
            old_edge.model_copy(deep=True),
            old_edge.model_copy(deep=True),
        ]
        split_edges[0].targetId = waypoint_id
        split_edges[1].sourceId = waypoint_id

        # Update network
        network.edges.remove(old_edge)
        network.edges.extend([component_edge] + split_edges)

        # Update spatial indices
        self._update_indices_for_placement(new_node_id, waypoint_id, [component_edge] + split_edges)

        return {
            "node_id": new_node_id,
            "waypoint_id": waypoint_id,
            "edges": [component_edge] + split_edges,
        }

    def _update_indices_for_placement(
        self, new_node_id: UUID, new_waypoint_id: UUID, new_edges: list[Edge]
    ) -> None:
        """
        Update spatial indices after successful node placement.

        :param new_node_id: UUID of new component node
        :type new_node_id: UUID
        :param waypoint_id: UUID of new waypoint
        :type waypoint_id: UUID
        :param edges: List of new edges to index
        :type edges: list[Edge]

        :rtype: None
        """
        new_node = self.graph.nodes[new_node_id]
        if not isinstance(new_node, ComponentNode):
            raise TypeError(f"Node with ID {new_node_id} is not a ComponentNode")
        new_waypoint = self.graph.nodes[new_waypoint_id]
        if not isinstance(new_waypoint, WaypointNode):
            raise TypeError(f"Node with ID {new_waypoint_id} is not a WaypointNode")

        self.node_index.insert(int(new_node_id), new_node.polygon().bounds)
        self.node_index.insert(int(new_waypoint_id), get_waypoint_polygon(new_waypoint).bounds)

        for edge in new_edges:
            self._index_edge(edge, self.edge_index)

    def _try_placement_below(
        self, network: Network, new_node: ComponentNode
    ) -> Optional[PlacedElements]:
        """
        Stage 3: Grid-based fallback placement below existing graph.

        :param network: Network to connect new node to, has to be in the graph given to NodePlacer
        :type network: Network
        :param new_node: ComponentNode to insert into network
        :type new_node: ComponentNode

        :return: Placement details if successful, None otherwise
        :rtype: Optional[PlacedElements]
        """
        self._update_grid_position(new_node)
        return self._connect_to_nearest_waypoint(network, new_node)

    def _update_grid_position(self, new_node: ComponentNode) -> None:
        """
        Get and update the grid-based position for a given new node in stage 3 placement.

        :param new_node: ComponentNode to place
        :type new_node: ComponentNode

        :rtype: None
        """
        if (self.stage3_current_x + new_node.widthRemFactor) > (
            self.stage3_min_x + self.original_width
        ):
            self.stage3_current_x = self.stage3_min_x  # pylint: disable=W0201
            self.stage3_current_y += self.stage3_row_height + self.stage3_node_spacing
            self.stage3_row_height = 0.0  # pylint: disable=attribute-defined-outside-init

        new_node.xRemFactor = self.stage3_current_x
        new_node.yRemFactor = self.stage3_current_y

        self.stage3_current_x += new_node.widthRemFactor + self.stage3_node_spacing
        self.stage3_row_height = max(  # pylint: disable=attribute-defined-outside-init
            self.stage3_row_height, new_node.heightRemFactor
        )

    def _connect_to_nearest_waypoint(
        self, network: Network, new_node: ComponentNode
    ) -> Optional[PlacedElements]:
        """
        Place a new node in the graph given to NodePlacer and connect it to the nearest waypoint of
        a given network.

        :param network: Network to connect new node to, has to be in the graph given to NodePlacer
        :type network: Network
        :param new_node: ComponentNode to insert into network
        :type new_node: ComponentNode

        :return: Placement details if successful, None otherwise
        :rtype: Optional[PlacedElements]
        """
        closest_waypoint_id, split_edges = self._get_or_create_closest_waypoint(new_node, network)

        new_node_id = uuid4()
        self.graph.nodes[new_node_id] = new_node

        new_edge = create_edge_with_attachment_point(
            new_node_id, closest_waypoint_id, AttachmentPoint.TOP
        )
        network.edges.append(new_edge)

        # Update only node spatial index as the edge would mess up the placement process
        # for further nodes
        self.node_index.insert(int(new_node_id), new_node.polygon().bounds)

        if split_edges:
            return {
                "node_id": new_node_id,
                "waypoint_id": closest_waypoint_id,
                "edges": [new_edge] + split_edges,
            }
        return {"node_id": new_node_id, "waypoint_id": None, "edges": [new_edge]}

    def _get_or_create_closest_waypoint(
        self, node: ComponentNode, network: Network
    ) -> tuple[UUID, Optional[list[Edge]]]:
        """
        Returns the ID of the waypoint inside the given network closest to the given node.
        If no waypoint exists in the given network, the closest edge gets split into two, connected
        by a new waypoint. The ID of this waypoint is then returned, with the new edges in the
        return value indicating that a new WaypointNode has been created.

        :param node: The ComponentNode from which the closest WaypointNode in the given Network
                     shall be found
        :type node: ComponentNode
        :param network: The Network in which the WaypointNode closest to the given ComponentNode
                        shall be found
        :type network: Network

        :return: The UUID of the WaypointNode in the Network closest to the given ComponentNode
                 The presence of edges in the return value indicates that a new WaypointNode has
                 been created. The edges are the ones added by splitting the closest edge.
        :rtype: tuple[UUID, Optional[list[Edge]]]
        """
        node_center = node.polygon().centroid
        closest_id = None
        min_distance = float("inf")

        nw_connected_nodes_ids = get_network_element_ids(network)
        for connected_node_id in nw_connected_nodes_ids:
            wp_node = self.graph.nodes[connected_node_id]
            if isinstance(wp_node, WaypointNode):
                wp_id = connected_node_id  # better readability
                wp_center = Point(wp_node.xRemFactor, wp_node.yRemFactor)
                distance = node_center.distance(wp_center)
                if distance < min_distance:
                    min_distance = distance
                    closest_id = wp_id

        if closest_id:
            return closest_id, None

        # No WaypointNode in the given network - split the closest edge and add new WaypointNode
        closest_edge = min(
            (edge for edge in network.edges),
            key=lambda e: node_center.distance(get_edge_line(e, self.graph).centroid),
            default=None,
        )
        if not closest_edge:
            raise ValueError(f"No edges in network {network}. This should not happen")
        closest_edge_line = get_edge_line(closest_edge, self.graph)
        closest_edge_center = closest_edge_line.centroid

        new_waypoint_id = uuid4()
        new_waypoint = WaypointNode(
            xRemFactor=closest_edge_center.x, yRemFactor=closest_edge_center.y
        )
        self.graph.nodes[new_waypoint_id] = new_waypoint

        # Split the closest edge into two new edges
        new_edges = [
            Edge(sourceId=closest_edge.sourceId, targetId=new_waypoint_id),
            Edge(sourceId=new_waypoint_id, targetId=closest_edge.targetId),
        ]

        # Update network
        network.edges.remove(closest_edge)
        network.edges.extend(new_edges)

        # Update spatial index
        self.edge_index.delete(
            int(closest_edge.sourceId) + int(closest_edge.targetId),
            get_edge_polygon_from_line(closest_edge_line, self.mean_edge_stroke_width).bounds,
        )
        for edge in new_edges:
            self._index_edge(edge, self.edge_index)
        self.node_index.insert(int(new_waypoint_id), get_waypoint_polygon(new_waypoint).bounds)

        closest_id = new_waypoint_id
        return closest_id, new_edges

    def add_component_to_network(
        self, network: Network, new_node: ComponentNode
    ) -> Optional[PlacedElements]:
        """
        Main entry point for adding a component to a network.

        Executes placement strategies in the following order:
        1. Waypoint replacement
        2. Edge-adjacent placement
        3. Grid-based placement (fallback)

        :param network: Network to connect new_node to, has to be in the graph given to NodePlacer,
                        can not be a copy of a network in the graph
        :type network: Network
        :param new_node: ComponentNode to insert into network
        :type new_node: ComponentNode

        :return: Placement details if successful, None otherwise
        :rtype: Optional[PlacedElements]
        """
        self._check_network_in_internal_graph(network)

        return (
            self._try_waypoint_replacement(network, new_node)
            or self._try_edge_adjacent_placement(network, new_node)
            or self._try_placement_below(network, new_node)
        )

    def _check_network_in_internal_graph(self, network: Network) -> None:
        """
        Checks if the given network is the same object as at least one of the networks in the  graph
        associated with node placer. If not, an error gets thrown.

        :param network: The network to check
        :type network: Network

        :rtype: None
        """
        is_copy: bool = False

        if network.edges == []:
            raise ValueError(
                "add_component_to_network was given a network with no edges. "
                f"No edges in network {network}. This should not happen."
            )

        # first naive check, does not identify copies of networks
        if network not in self.graph.networks:
            is_copy = True
        else:
            # remove all edges from the network,
            # if it is a copied network it won't get found in the internal graph anymore
            tmp_edges: list[Edge] = [edge.model_copy(deep=True) for edge in network.edges]
            network.edges.clear()

            if network not in self.graph.networks:
                is_copy = True

            # add edges back to network in any case
            network.edges = tmp_edges

        if is_copy:
            raise ValueError(
                f"Given network {network} is not in the graph associated with NodePlacer."
            )

    def _try_edge_adjacent_placement(
        self, network: Network, new_node: ComponentNode
    ) -> Optional[PlacedElements]:
        """
        Attempt Stage 2 placement for all edges in network

        :param network: Network to connect new node to, has to be in the graph given to NodePlacer
        :type network: Network
        :param new_node: ComponentNode to insert into network
        :type new_node: ComponentNode

        :return: Placement details if successful, None otherwise
        :rtype: Optional[PlacedElements]
        """
        for edge in network.edges:
            if result := self._try_placement_next_to_edge(edge, network, new_node):
                return result
        return None
