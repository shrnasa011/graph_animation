"""
Local (.py) version of the scene in demo1.ipynb.

Render with::

    .venv/bin/manim -ql --disable_caching demo1.py GraphDemo   # quick
    .venv/bin/manim -qh demo1.py GraphDemo                      # high quality
"""

from __future__ import annotations

import os
import sys

import numpy as np
from manim import *

# Make the ``graph_animation`` package importable regardless of the cwd
# (the package uses relative imports internally).
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from graph_animation.graph import Graph


class GraphDemo(Scene):
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

        graph.view.set_width(config.frame_width * 0.7)
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
