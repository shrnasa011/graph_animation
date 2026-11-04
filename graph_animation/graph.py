from __future__ import annotations

from collections import defaultdict
from typing import Iterable

import numpy as np
from manim import *

from .primitives import Edge, Vertex


class Graph:
    """An animated graph built from reusable vertex and edge primitives."""

    def __init__(
        self,
        vertices: list[str],
        edges: list[tuple[str, str]],
        positions: dict[str, np.ndarray],
    ) -> None:

        self.positions = positions
        self.edge_list = edges

        ####################################################
        # Vertices
        ####################################################

        self.vertices: dict[str, Vertex] = {}

        for v in vertices:
            self.vertices[v] = Vertex(
                name=v,
                position=positions[v],
            )

        ####################################################
        # Edges
        ####################################################

        self.edges: dict[frozenset[str], Edge] = {}

        for u, v in edges:
            self.edges[frozenset((u, v))] = Edge(
                self.vertices[u],
                self.vertices[v],
            )

        ####################################################
        # Adjacency
        ####################################################

        self.adjacency = defaultdict(set)

        for u, v in edges:
            self.adjacency[u].add(v)
            self.adjacency[v].add(u)

        ####################################################
        # Degree labels
        ####################################################

        # Fill in each vertex's degree label now, at base scale. From
        # here on it scales with the view automatically — no rescaling.
        for name, vertex in self.vertices.items():
            vertex.set_degree(self.degree(name))

        ####################################################
        # View
        ####################################################

        self.edge_group = VGroup(*self.edges.values())
        self.vertex_group = VGroup(*self.vertices.values())

        # Degree labels now live inside their vertices, so the vertex
        # group already contains them — no separate annotation group.
        self.view = VGroup(
            self.edge_group,
            self.vertex_group,
        )



    ########################################################
    # Convenience
    ########################################################

    def __getitem__(self, vertex: str) -> Vertex:
        """Return the visual vertex with the given name."""
        return self.vertices[vertex]

    def __iter__(self):
        """Iterate over vertex names."""
        return iter(self.vertices)

    @property
    def mobject(self):
        """The Manim group containing all graph visuals."""
        return self.view

    ########################################################
    # Queries
    ########################################################

    def neighbors(self, vertex: str) -> set[str]:
        """Return the names of vertices adjacent to ``vertex``."""
        return self.adjacency[vertex]

    def degree(
        self,
        vertex: str,
        active_only: bool = True,
    ) -> int:
        """Return degree, optionally counting only active neighbors."""

        if not active_only:
            return len(self.adjacency[vertex])

        return sum(
            self.vertices[u].active
            for u in self.adjacency[vertex]
        )

    def is_active(self, vertex: str) -> bool:
        """Return whether the named vertex is active."""
        return self.vertices[vertex].is_active()

    def edge(self, u: str, v: str) -> Edge:
        """Return the edge joining ``u`` and ``v``."""
        return self.edges[frozenset((u, v))]

    def incident_edges(self, vertex: str) -> list[Edge]:
        """Return all edges touching ``vertex``."""
        return [self.edge(vertex, neighbor) for neighbor in self.neighbors(vertex)]

    ########################################################
    # Vertex animations
    ########################################################

    def select(self, vertex):

        return self[vertex].select()

    def deselect(self, vertex):

        return self[vertex].deselect()

    def gray(self, vertex):

        return self[vertex].gray()

    def activate(self, vertex):

        return self[vertex].activate()

    def pulse(self, vertex):

        return self[vertex].pulse()

    def show_halo(self, vertex):

        return self[vertex].show_halo()

    def hide_halo(self, vertex):

        return self[vertex].hide_halo()

    ########################################################
    # Batch vertex animations
    ########################################################

    def gray_vertices(
        self,
        vertices: Iterable[str],
    ):
        animations = [self.gray(v) for v in vertices]
        return AnimationGroup(*animations) if animations else Wait(0)

    def activate_vertices(
        self,
        vertices: Iterable[str],
    ):
        animations = [self.activate(v) for v in vertices]
        return AnimationGroup(*animations) if animations else Wait(0)

    ########################################################
    # Degree labels
    ########################################################

    def show_degrees(self):
        # The labels already exist at the right size (set at construction
        # and scaled with the view); revealing them is just a fade-in.
        animations = [
            vertex.degree_label.animate.set_opacity(1)
            for vertex in self.vertices.values()
            if vertex.is_active()
        ]
        return AnimationGroup(*animations, lag_ratio=0) if animations else Wait(0)

    def update_degrees(self):
        animations = [
            vertex.degree_label.animate.become(
                vertex.degree_target(self.degree(name))
            )
            for name, vertex in self.vertices.items()
            if vertex.is_active()
        ]
        return AnimationGroup(*animations, lag_ratio=0) if animations else Wait(0)

    def hide_degrees(self):

        return AnimationGroup(
            *[
                FadeOut(vertex.degree_label)
                for vertex in self.vertices.values()
            ],
            lag_ratio=0,
        )

    ########################################################
    # Edge animations
    ########################################################

    def highlight_edge(
        self,
        u,
        v,
    ):

        return self.edge(u, v).highlight()

    def unhighlight_edge(
        self,
        u,
        v,
    ):

        return self.edge(u, v).unhighlight()

    def gray_edges(
        self,
        edges,
    ):

        return AnimationGroup(
            *[
                self.edge(u, v).deactivate()
                for u, v in edges
            ]
        )

    def activate_edges(
        self,
        edges,
    ):

        return AnimationGroup(
            *[
                self.edge(u, v).activate()
                for u, v in edges
            ]
        )

    ########################################################
    # Utility
    ########################################################

    def add_to_scene(self, scene):

        scene.add(self.view)

    def reset(self):

        animations = []
    
        for v in self.vertices:
            animations.append(self.activate(v))
    
        for edge in self.edges.values():
            animations.append(edge.activate())
    
        return AnimationGroup(*animations)

    def move_to(self, point):

        self.view.move_to(point)
        return self
    
    def shift(self, vector):
    
        self.view.shift(vector)
        return self
    
    def scale(self, factor):

        self.view.scale(factor)
        return self
