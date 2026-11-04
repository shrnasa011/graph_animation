from __future__ import annotations

import numpy as np
from manim import *

from .constants import *

class Edge(VMobject):
    """
    Edge joining two Vertex objects.

    The edge automatically follows its endpoints whenever
    either vertex moves.
    """

    def __init__(
        self,
        u,
        v,
        color=EDGE_COLOR,
        stroke_width=EDGE_WIDTH,
        **kwargs,
    ):
        super().__init__(**kwargs)

        self.u = u
        self.v = v

        self.color = color
        self.width = stroke_width

        self.active = True

        self.set_stroke(
            color=color,
            width=stroke_width,
        )

        self.redraw()

        self.add_updater(
            lambda m: m.redraw()
        )

    # -----------------------------------------------------
    # Geometry
    # -----------------------------------------------------

    @property
    def endpoints(self):
        return (self.u, self.v)

    def contains(self, vertex):
        return vertex is self.u or vertex is self.v

    def other(self, vertex):
        if vertex is self.u:
            return self.v
        if vertex is self.v:
            return self.u
        raise ValueError("Vertex not incident to edge.")

    def redraw(self):
        """
        Recompute the edge so that it touches the
        boundaries of the endpoint circles instead of
        passing through their centers.
        """

        start = self.u.point
        end = self.v.point

        direction = end - start
        length = np.linalg.norm(direction)

        if length < 1e-8:
            return self

        direction /= length

        start += direction * self.u.radius
        end -= direction * self.v.radius

        self.set_points_as_corners([start, end])

        return self

    # -----------------------------------------------------
    # Animations
    # -----------------------------------------------------

    def activate(self):
        self.active = True

        return self.animate.set_stroke(
            color=self.color,
            width=self.width,
            opacity=1,
        )

    def deactivate(self):
        self.active = False

        return self.animate.set_stroke(
            opacity=EDGE_INACTIVE_OPACITY,
        )

    def highlight(self):
        return self.animate.set_stroke(
            color=EDGE_HIGHLIGHT,
            width=self.width + 2,
            opacity=1,
        )

    def unhighlight(self):
        return self.animate.set_stroke(
            color=self.color,
            width=self.width,
            opacity=1,
        )

    def pulse(self):
        return Succession(
            self.animate.set_stroke(width=self.width + 3),
            self.animate.set_stroke(width=self.width),
        )

    def incident_to(self, vertices):
        return self.u in vertices or self.v in vertices

    @property
    def point(self):
        return self.circle.get_center()