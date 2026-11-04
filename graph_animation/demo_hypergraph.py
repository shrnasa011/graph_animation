"""
Hypergraph demo built on the graph_animation package.

Render with::

    .venv/bin/manim -ql --disable_caching demo_hypergraph.py HyperGraphDemo
    .venv/bin/manim -qh demo_hypergraph.py HyperGraphDemo

Each hyperedge is a translucent blob enclosing its member vertices;
the degree label on a vertex counts how many hyperedges it belongs to.
"""

from __future__ import annotations

import os
import sys

import numpy as np
from manim import *

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from graph_animation import HyperGraph


class HyperGraphDemo(Scene):
    def construct(self):
        self.camera.background_color = WHITE

        positions = {
            "a": np.array([-3.5,  1.4, 0]),
            "b": np.array([-1.8,  2.1, 0]),
            "c": np.array([-2.6, -0.4, 0]),
            "d": np.array([-0.3,  0.4, 0]),
            "e": np.array([ 1.8,  1.5, 0]),
            "f": np.array([ 2.2, -0.7, 0]),
            "g": np.array([ 3.8,  0.4, 0]),
        }

        hyperedges = [
            ("a", "b", "c", "d"),   # a 4-vertex hyperedge
            ("d", "e", "f"),        # a 3-vertex hyperedge
            ("f", "g"),             # an ordinary 2-vertex edge
            ("b", "e"),             # crossing pair
        ]

        hg = HyperGraph(
            vertices=list(positions.keys()),
            hyperedges=hyperedges,
            positions=positions,
        )

        hg.view.width = config.frame_width * 0.75
        hg.view.move_to(0.3 * UP)

        title = Text("Hypergraph", font_size=34, color=BLACK).to_edge(UP)
        caption = Text(
            "degree = number of incident hyperedges",
            font_size=24, color=GREY_D,
        ).to_edge(DOWN)

        # 1. Vertices first, then grow the hyperedge blobs around them.
        self.play(FadeIn(title), FadeIn(hg.vertex_group))
        self.wait(0.3)
        self.play(hg.draw_hyperedges())
        self.wait(0.4)

        # 2. Show incidence degrees.
        self.play(FadeIn(caption), hg.show_degrees())
        self.wait(0.6)

        # 3. Highlight the big 4-vertex hyperedge and pulse its members.
        self.play(hg.highlight_hyperedge(0))
        self.play(
            AnimationGroup(
                *[hg.pulse(v) for v in hg.membership[0]],
                lag_ratio=0.15,
            )
        )
        self.wait(0.3)
        self.play(hg.unhighlight_hyperedge(0))

        # 4. Vertex d is shared by two hyperedges — spotlight it.
        self.play(hg.show_halo("d"), hg.select("d"))
        self.play(
            AnimationGroup(
                *[hg.highlight_hyperedge(i) for i in hg.incidence["d"]],
                lag_ratio=0.2,
            )
        )
        self.wait(0.5)

        # 5. Deactivate one of d's hyperedges and refresh degrees.
        self.play(
            hg.deactivate_hyperedge(1),
            hg.unhighlight_hyperedge(0),
        )
        self.play(hg.update_degrees())
        self.wait(0.5)

        # 6. Reset.
        self.play(hg.hide_degrees(), hg.hide_halo("d"), hg.deselect("d"))
        self.play(hg.reset())
        self.wait(1.0)
