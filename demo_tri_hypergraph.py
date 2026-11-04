"""
3-uniform hypergraph demo.

Every hyperedge joins exactly three vertices and is drawn as a rounded
triangle (TriEdge). Render with::

    .venv/bin/manim -ql --disable_caching demo_tri_hypergraph.py TriHyperGraphDemo
    .venv/bin/manim -qh demo_tri_hypergraph.py TriHyperGraphDemo
"""

from __future__ import annotations

import os
import sys

import numpy as np
from manim import *

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from graph_animation import TriHyperGraph


class TriHyperGraphDemo(Scene):
    def construct(self):
        self.camera.background_color = WHITE

        positions = {
            "1": np.array([-3.2,  1.6, 0]),
            "2": np.array([-1.2,  2.2, 0]),
            "3": np.array([-2.6, -0.6, 0]),
            "4": np.array([-0.4,  0.2, 0]),
            "5": np.array([ 1.8,  1.7, 0]),
            "6": np.array([ 2.6, -0.6, 0]),
            "7": np.array([ 0.6, -1.6, 0]),
        }

        # Every hyperedge has exactly three vertices (3-uniform).
        hyperedges = [
            ("1", "2", "3"),
            ("2", "3", "4"),
            ("4", "5", "6"),
            ("4", "6", "7"),
        ]

        hg = TriHyperGraph(
            vertices=list(positions.keys()),
            hyperedges=hyperedges,
            positions=positions,
        )

        hg.view.width = config.frame_width * 0.68
        hg.view.move_to(0.5 * DOWN)

        title = Text("3-uniform hypergraph", font_size=34, color=BLACK).to_edge(UP)
        caption = Text(
            "degree = number of incident triples",
            font_size=24, color=GREY_D,
        ).to_edge(DOWN)

        # 1. Bring in the vertices, then fade the triangles in around them.
        self.play(FadeIn(title))
        self.play(FadeIn(hg.vertex_group, lag_ratio=0.08), run_time=1.0)
        self.wait(0.3)
        self.play(hg.draw_hyperedges(lag_ratio=0.35), run_time=1.6)
        self.wait(0.5)

        # 2. Show incidence degrees.
        self.play(FadeIn(caption), hg.show_degrees(), run_time=0.8)
        self.wait(0.8)

        # 3. Gently light up each triangle in turn.
        for i in range(len(hyperedges)):
            self.play(hg.highlight_hyperedge(i), run_time=0.6)
            self.wait(0.4)
            self.play(hg.unhighlight_hyperedge(i), run_time=0.6)

        self.wait(0.3)

        # 4. Vertex "4" belongs to three triples — spotlight it together
        #    with the triangles that contain it.
        self.play(
            hg.select("4"),
            hg.show_halo("4"),
            *[hg.highlight_hyperedge(i) for i in hg.incidence["4"]],
            run_time=0.9,
        )
        self.wait(1.0)

        # 5. Release the spotlight.
        self.play(
            hg.deselect("4"),
            hg.hide_halo("4"),
            *[hg.unhighlight_hyperedge(i) for i in hg.incidence["4"]],
            run_time=0.9,
        )
        self.wait(1.0)
