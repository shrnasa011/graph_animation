from __future__ import annotations

import numpy as np
from manim import *
from scipy.spatial import ConvexHull

from .constants import *


class HyperEdge(VMobject):
    """
    A hyperedge joining an arbitrary set of Vertex objects.

    It is drawn as a translucent rounded "blob" that encloses all of
    its member vertices. Like :class:`Edge`, it carries an updater so
    the blob follows the vertices whenever they move, and it scales
    with the surrounding graph view.

    Works for any number of members:
        1 member  -> a rounded disc around the vertex
        2 members -> a stadium/capsule
        3+        -> a rounded convex hull
    """

    def __init__(
        self,
        vertices,
        color=BLUE_D,
        pad=HYPEREDGE_PAD,
        samples=HYPEREDGE_SAMPLES,
        **kwargs,
    ):
        super().__init__(**kwargs)

        self.vertices = list(vertices)
        self.base_color = color
        self.pad = pad
        self.samples = samples
        self.active = True

        self.set_fill(color, opacity=HYPEREDGE_FILL_OPACITY)
        self.set_stroke(color, width=HYPEREDGE_STROKE_WIDTH, opacity=1)

        self.redraw()
        self.add_updater(lambda m: m.redraw())

    # -----------------------------------------------------
    # Membership
    # -----------------------------------------------------

    @property
    def members(self):
        return self.vertices

    def contains(self, vertex):
        return vertex in self.vertices

    # -----------------------------------------------------
    # Geometry
    # -----------------------------------------------------

    def _enclosing_points(self):
        """Point cloud: a ring of samples around each member vertex."""
        if not self.vertices:
            return None

        # Infer the view's current scale from a member circle so the
        # padding (and thus the blob) scales with the graph view.
        ref = self.vertices[0]
        view_scale = ref.circle.width / (2 * ref.radius)
        pad = self.pad * view_scale

        angles = np.linspace(0, TAU, self.samples, endpoint=False)
        cloud = []
        for v in self.vertices:
            center = v.point
            radius = v.circle.width / 2 + pad
            for a in angles:
                cloud.append(
                    [center[0] + radius * np.cos(a),
                     center[1] + radius * np.sin(a)]
                )

        return np.array(cloud)

    def redraw(self):
        cloud = self._enclosing_points()
        if cloud is None or len(cloud) < 3:
            return self

        try:
            hull = ConvexHull(cloud)
            ordered = cloud[hull.vertices]
        except Exception:
            # Degenerate (e.g. collinear) — fall back to raw cloud.
            ordered = cloud

        points = [np.array([x, y, 0.0]) for x, y in ordered]
        points.append(points[0])          # close the loop

        # The hull is convex and the per-vertex arcs are densely
        # sampled, so straight corners already read as a smooth,
        # rounded blob — and, unlike spline smoothing, never overshoot
        # into spikes at the corners.
        self.set_points_as_corners(points)
        return self

    # -----------------------------------------------------
    # Animations
    # -----------------------------------------------------

    def activate(self):
        self.active = True
        return (
            self.animate
            .set_fill(self.base_color, opacity=HYPEREDGE_FILL_OPACITY)
            .set_stroke(self.base_color, width=HYPEREDGE_STROKE_WIDTH, opacity=1)
        )

    def deactivate(self):
        self.active = False
        return (
            self.animate
            .set_fill(opacity=HYPEREDGE_INACTIVE_OPACITY * 0.4)
            .set_stroke(opacity=HYPEREDGE_INACTIVE_OPACITY)
        )

    def highlight(self):
        return (
            self.animate
            .set_fill(self.base_color, opacity=HYPEREDGE_HIGHLIGHT_FILL_OPACITY)
            .set_stroke(self.base_color, width=HYPEREDGE_STROKE_WIDTH + 2, opacity=1)
        )

    def unhighlight(self):
        return (
            self.animate
            .set_fill(self.base_color, opacity=HYPEREDGE_FILL_OPACITY)
            .set_stroke(self.base_color, width=HYPEREDGE_STROKE_WIDTH, opacity=1)
        )

    def pulse(self):
        return Succession(
            self.animate.set_stroke(width=HYPEREDGE_STROKE_WIDTH + 3),
            self.animate.set_stroke(width=HYPEREDGE_STROKE_WIDTH),
        )
