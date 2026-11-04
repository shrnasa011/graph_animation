"""
Two versions of the demo1 scene at different sizes:

    GraphDemo60  ->  graph sized to 60% of the frame width
    GraphDemo30  ->  graph sized to 30% of the frame width

Render with::

    .venv/bin/manim -qh demo_sizes.py GraphDemo60
    .venv/bin/manim -qh demo_sizes.py GraphDemo30
    .venv/bin/manim -qh demo_sizes.py GraphDemo60 GraphDemo30   # both
"""

from __future__ import annotations

import os
import sys

import numpy as np
from manim import *

# Make the ``graph_animation`` package importable regardless of the cwd.
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from graph_animation.graph import Graph


class _BaseGraphDemo(Scene):
    """Shared scene; subclasses set ``width_fraction``."""

    width_fraction = 0.6

    def construct(self):
        self.camera.background_color = WHITE

        positions = {
            "a": np.array([-2, 1, 0]),
            "b": np.array([0, 2, 0]),
            "c": np.array([-2, -1, 0]),
            "d": np.array([1.5, 0, 0]),
            "e": np.array([3, 1.5, 0]),
        }

        graph = Graph(
            vertices=["a", "b", "c", "d", "e"],
            edges=[
                ("a", "b"),
                ("a", "c"),
                ("b", "d"),
                ("c", "d"),
                ("d", "e"),
            ],
            positions=positions,
        )

        # Size the graph to the requested fraction of the frame width,
        # then centre it. Assigning ``.width`` scales while preserving
        # aspect ratio (no deprecation warning).
        graph.view.width = config.frame_width * self.width_fraction
        graph.view.move_to(ORIGIN)

        # Small caption so the two renders are easy to tell apart.
        caption = Text(
            f"{int(self.width_fraction * 100)}% of frame width",
            font_size=28,
            color=BLACK,
        ).to_edge(DOWN)
        self.add(caption)

        self.wait(0.2)
        self.add(graph.view)
        self.wait(0.5)

        self.play(graph.show_degrees())
        self.wait(0.5)

        self.play(graph.show_halo("d"))
        self.wait(0.5)

        self.play(graph.select("d"))
        self.wait(0.5)

        self.play(graph.gray_vertices(["b", "c"]))
        self.wait(0.5)

        self.play(graph.update_degrees())
        self.wait(0.5)

        self.play(graph.hide_degrees())
        self.wait(0.5)

        self.play(graph.hide_halo("d"))
        self.wait()


class GraphDemo60(_BaseGraphDemo):
    width_fraction = 0.6


class GraphDemo30(_BaseGraphDemo):
    width_fraction = 0.3
