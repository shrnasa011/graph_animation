from __future__ import annotations

from collections import defaultdict
from typing import Dict, Iterable, List

import numpy as np
from manim import *

from .primitives import Vertex, HyperEdge, TriEdge
from .primitives.constants import HYPEREDGE_PALETTE


class HyperGraph:
    """
    Animated hypergraph built from Vertex and HyperEdge primitives.

    A hyperedge connects an arbitrary set of vertices and is drawn as a
    translucent blob enclosing them. Like :class:`Graph`, this class is
    agnostic to any algorithm; it manages geometry and returns Manim
    animations.

    Parameters
    ----------
    vertices   : list of vertex names
    hyperedges : list of iterables of vertex names, e.g.
                 [("a", "b", "c"), ("c", "d"), ("d", "e", "f")]
    positions  : dict name -> np.ndarray
    colors     : optional list of colours, one per hyperedge
    """

    def __init__(
        self,
        vertices: List[str],
        hyperedges: List[Iterable[str]],
        positions: Dict[str, np.ndarray],
        colors: List = None,
    ):

        self.positions = positions

        ####################################################
        # Vertices
        ####################################################

        self.vertices: Dict[str, Vertex] = {}
        for v in vertices:
            self.vertices[v] = Vertex(name=v, position=positions[v])

        ####################################################
        # Hyperedges
        ####################################################

        self.hyperedges: List[HyperEdge] = []
        self.membership: List[frozenset] = []

        # vertex name -> list of hyperedge indices it belongs to
        self.incidence = defaultdict(list)

        for i, members in enumerate(hyperedges):
            members = list(members)
            color = (
                colors[i] if colors is not None
                else HYPEREDGE_PALETTE[i % len(HYPEREDGE_PALETTE)]
            )

            he = self._make_hyperedge(
                [self.vertices[m] for m in members],
                color,
            )

            self.hyperedges.append(he)
            self.membership.append(frozenset(members))

            for m in members:
                self.incidence[m].append(i)

        ####################################################
        # Degree labels (number of incident hyperedges)
        ####################################################

        for name, vertex in self.vertices.items():
            vertex.set_degree(self.degree(name))

        ####################################################
        # View  (hyperedges behind the vertices)
        ####################################################

        self.hyperedge_group = VGroup(*self.hyperedges)
        self.vertex_group = VGroup(*self.vertices.values())

        self.view = VGroup(
            self.hyperedge_group,
            self.vertex_group,
        )
        self._fade_state_saved = False

    ########################################################
    # Hyperedge factory (overridable)
    ########################################################

    def _make_hyperedge(self, vertices, color):
        """Build the primitive for one hyperedge. Subclasses may override."""
        return HyperEdge(vertices, color=color)

    ########################################################
    # Convenience
    ########################################################

    def __getitem__(self, vertex: str):
        return self.vertices[vertex]

    def __iter__(self):
        return iter(self.vertices)

    @property
    def mobject(self):
        return self.view

    def add_to_scene(self, scene):
        scene.add(self.view)

    def move_to(self, point):
        self.view.move_to(point)
        return self

    def shift(self, vector):
        self.view.shift(vector)
        return self

    def scale(self, factor):
        self.view.scale(factor)
        return self

    ########################################################
    # Queries
    ########################################################

    def hyperedge(self, index: int) -> HyperEdge:
        return self.hyperedges[index]

    def incident_hyperedges(self, vertex: str) -> List[HyperEdge]:
        return [self.hyperedges[i] for i in self.incidence[vertex]]

    def degree(self, vertex: str, active_only: bool = True) -> int:
        """Number of hyperedges incident to ``vertex``."""
        if not active_only:
            return len(self.incidence[vertex])

        return sum(
            self.hyperedges[i].active
            for i in self.incidence[vertex]
        )

    def neighbors(self, vertex: str):
        """Vertices sharing at least one hyperedge with ``vertex``."""
        result = set()
        for i in self.incidence[vertex]:
            result |= self.membership[i]
        result.discard(vertex)
        return result

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

    def gray_vertices(self, vertices: Iterable[str]):
        animations = [self.gray(v) for v in vertices]
        return AnimationGroup(*animations) if animations else Wait(0)

    def activate_vertices(self, vertices: Iterable[str]):
        animations = [self.activate(v) for v in vertices]
        return AnimationGroup(*animations) if animations else Wait(0)

    def remove_vertices(self, vertices: Iterable[str]):
        """Deactivate vertices and every active hyperedge incident to them.

        The hyperedges remain in the drawing at their inactive opacity, so
        the original geometry stays available to the animation.  Subsequent
        calls to :meth:`degree` and :meth:`update_degrees` then ignore them.
        """
        vertices = list(dict.fromkeys(vertices))
        unknown = set(vertices) - self.vertices.keys()
        if unknown:
            raise KeyError(f"Unknown vertices: {sorted(unknown)!r}")

        incident = {
            index
            for vertex in vertices
            for index in self.incidence[vertex]
            if self.hyperedges[index].active
        }
        return AnimationGroup(
            *[self.gray(vertex) for vertex in vertices],
            *[self.deactivate_hyperedge(index) for index in incident],
        )

    ########################################################
    # Degree labels
    ########################################################

    def show_degrees(self):
        animations = [
            vertex.degree_label.animate.set_opacity(1)
            for vertex in self.vertices.values()
            if vertex.is_active()
        ]
        return AnimationGroup(*animations, lag_ratio=0) if animations else Wait(0)

    def update_degrees(self):
        return AnimationGroup(
            *[
                (
                    vertex.degree_label.animate.become(
                        vertex.degree_target(self.degree(name))
                    )
                    if vertex.is_active()
                    else vertex.degree_label.animate.set_opacity(0)
                )
                for name, vertex in self.vertices.items()
            ],
            lag_ratio=0,
        )

    def hide_degrees(self):
        return AnimationGroup(
            *[
                FadeOut(vertex.degree_label)
                for vertex in self.vertices.values()
            ],
            lag_ratio=0,
        )

    ########################################################
    # Whole-hypergraph visibility
    ########################################################

    def fade(self, opacity: float = 0.1):
        """Dim the hyperedges and vertices without changing their base state.

        This is useful when a derived object, such as a link graph, is
        temporarily drawn over the same vertex layout.  The current visual
        state is saved so :meth:`unfade` restores the original individual
        fill, stroke, and label opacities exactly.
        """
        self.view.save_state()
        self._fade_state_saved = True
        return self.view.animate.set_opacity(opacity)

    def unfade(self):
        """Restore the exact visual state saved by :meth:`fade`."""
        if not self._fade_state_saved:
            return Wait(0)
        self._fade_state_saved = False
        return Restore(self.view)

    ########################################################
    # Hyperedge animations
    ########################################################

    def draw_hyperedges(self, lag_ratio: float = 0.3):
        """Fade/create every hyperedge in one animation."""
        return AnimationGroup(
            *[FadeIn(he) for he in self.hyperedges],
            lag_ratio=lag_ratio,
        )

    def highlight_hyperedge(self, index):
        return self.hyperedges[index].highlight()

    def unhighlight_hyperedge(self, index):
        return self.hyperedges[index].unhighlight()

    def activate_hyperedge(self, index):
        return self.hyperedges[index].activate()

    def deactivate_hyperedge(self, index):
        return self.hyperedges[index].deactivate()

    def pulse_hyperedge(self, index):
        return self.hyperedges[index].pulse()

    ########################################################
    # Utility
    ########################################################

    def reset(self):
        animations = [self.activate(v) for v in self.vertices]
        animations += [he.activate() for he in self.hyperedges]
        return AnimationGroup(*animations)


class TriHyperGraph(HyperGraph):
    """
    A 3-uniform hypergraph: every hyperedge connects exactly three
    vertices and is drawn as a rounded triangle (:class:`TriEdge`).

    Identical API to :class:`HyperGraph`; only the hyperedge primitive
    and the 3-uniform validation differ.
    """

    def _make_hyperedge(self, vertices, color):
        if len(vertices) != 3:
            raise ValueError(
                "TriHyperGraph is 3-uniform: every hyperedge must have "
                f"exactly 3 vertices (got {len(vertices)})."
            )
        return TriEdge(vertices, color=color)

    def link_graph_edges(
        self,
        vertex: str,
        active_only: bool = True,
    ) -> List[tuple[int, tuple[str, str]]]:
        """Return the 2-edge projection of triples incident to ``vertex``.

        Each returned item contains the source hyperedge index followed by
        the two remaining endpoints.  Keeping the source index lets an
        animation reveal the original 3-edge and its projected 2-edge in
        the same step.
        """
        if vertex not in self.vertices:
            raise KeyError(f"Unknown vertex: {vertex!r}")

        edges = []
        for index in self.incidence[vertex]:
            if active_only and not self.hyperedges[index].active:
                continue

            endpoints = tuple(sorted(self.membership[index] - {vertex}))
            # _make_hyperedge enforces this invariant, but the explicit
            # check makes an invalid subclass implementation easier to spot.
            if len(endpoints) != 2:
                raise ValueError(
                    "The link graph is defined only for 3-uniform "
                    "hyperedges."
                )
            edges.append((index, endpoints))

        return edges

    def link_graph_degrees(
        self,
        vertex: str,
        active_only: bool = True,
    ) -> Dict[str, int]:
        """Return degrees in the link graph formed from ``vertex``'s triples.

        A link edge is counted once per incident triple, matching the visual
        construction in :meth:`link_graph_edges` even if two triples project
        to the same pair of vertices.
        """
        degrees = defaultdict(int)
        for _, (u, v) in self.link_graph_edges(vertex, active_only):
            degrees[u] += 1
            degrees[v] += 1
        return dict(degrees)
