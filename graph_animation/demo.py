"""
Demo animation built on top of the ``graph_animation`` package.

Run it with::

    manim -pql demo.py GraphDemo      # quick preview (low quality)
    manim -qh demo.py GraphDemo       # high quality render

The scene walks a tiny greedy "cover" style animation:
    1.  fade the graph in
    2.  show every vertex degree
    3.  pick the highest-degree vertex, select it and light up its edges
    4.  gray out that vertex and its neighbours, then refresh the degrees
    5.  reset everything
"""

from __future__ import annotations

import os
import sys

import numpy as np
from manim import *

# Make the ``graph_animation`` package importable regardless of where
# manim is invoked from (the package uses relative imports internally).
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from graph_animation import Graph


class GraphDemo(Scene):
    def construct(self):
        # White canvas.
        self.camera.background_color = WHITE

        # ------------------------------------------------------------------
        # 1. Define the graph: vertices, edges and 2-D layout positions.
        # ------------------------------------------------------------------
        positions = {
            "A": np.array([-3.0,  1.5, 0.0]),
            "B": np.array([-1.0,  2.2, 0.0]),
            "C": np.array([ 1.0,  1.5, 0.0]),
            "D": np.array([ 3.0,  0.5, 0.0]),
            "E": np.array([-2.0, -0.5, 0.0]),
            "F": np.array([ 0.0,  0.2, 0.0]),
            "G": np.array([ 2.0, -1.2, 0.0]),
        }

        edges = [
            ("A", "B"),
            ("B", "C"),
            ("C", "D"),
            ("A", "E"),
            ("B", "F"),
            ("C", "F"),
            ("E", "F"),
            ("F", "G"),
            ("D", "G"),
        ]

        graph = Graph(
            vertices=list(positions.keys()),
            edges=edges,
            positions=positions,
        )

        # Scale the whole view down; the degree labels created later
        # will match this scale automatically.
        graph.scale(0.85)

        # ------------------------------------------------------------------
        # 2. Fade the graph in.
        # ------------------------------------------------------------------
        title = Text(
            "graph_animation demo",
            font_size=32,
            color=BLACK,
        ).to_edge(UP)
        graph.add_to_scene(self)   # add so edge updaters stay live
        self.play(FadeIn(title))
        self.play(FadeIn(graph.mobject))
        self.wait(0.5)

        # ------------------------------------------------------------------
        # 3. Reveal every vertex degree.
        # ------------------------------------------------------------------
        self.play(graph.show_degrees())
        self.wait(0.5)

        # ------------------------------------------------------------------
        # 3b. Scale the whole graph view up and back down.
        #     The degree labels (children of the view VGroup) scale
        #     right along with the vertices and edges.
        # ------------------------------------------------------------------
        self.play(graph.mobject.animate.scale(1.6), run_time=1.5)
        self.wait(0.5)
        self.play(graph.mobject.animate.scale(1 / 1.6), run_time=1.5)
        self.wait(0.5)

        # ------------------------------------------------------------------
        # 4. Greedily pick the highest-degree vertex.
        # ------------------------------------------------------------------
        chosen = max(graph, key=lambda v: graph.degree(v))

        self.play(graph.pulse(chosen))
        self.play(
            graph.show_halo(chosen),
            graph.select(chosen),
        )

        # Light up its incident edges one after another.
        self.play(
            AnimationGroup(
                *[
                    graph.highlight_edge(chosen, nbr)
                    for nbr in graph.neighbors(chosen)
                ],
                lag_ratio=0.25,
            )
        )
        self.wait(0.5)

        # ------------------------------------------------------------------
        # 5. "Cover" the chosen vertex + its neighbours, refresh degrees.
        # ------------------------------------------------------------------
        neighbours = list(graph.neighbors(chosen))

        self.play(
            graph.hide_halo(chosen),
            graph.gray(chosen),
            graph.gray_vertices(neighbours),
        )
        self.play(graph.update_degrees())
        self.wait(0.5)

        # ------------------------------------------------------------------
        # 6. Reset the graph back to its original state.
        # ------------------------------------------------------------------
        self.play(graph.hide_degrees())
        self.play(graph.reset())
        self.wait(1.0)
