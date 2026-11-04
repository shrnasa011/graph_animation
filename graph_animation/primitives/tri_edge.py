from __future__ import annotations

import numpy as np
from manim import *

from .constants import *
from .hyperedge import HyperEdge


class TriEdge(HyperEdge):
    """
    A 3-uniform hyperedge: a rounded triangle joining exactly three
    Vertex objects.

    The outline is built from three genuine circular arcs — one per
    vertex, of radius ``circle + pad`` centred on the vertex — joined by
    the outer tangent sides. Every member vertex therefore lies fully
    inside its rounded corner, the corners are true arcs (not facets),
    and the shape follows / scales with the graph view via the inherited
    updater.
    """

    def __init__(
        self,
        vertices,
        color=BLUE_D,
        pad=TRIEDGE_PAD,
        arc_samples=24,
        **kwargs,
    ):
        if len(vertices) != 3:
            raise ValueError(
                "TriEdge connects exactly three vertices "
                f"(got {len(vertices)})."
            )

        self.arc_samples = arc_samples
        super().__init__(vertices, color=color, pad=pad, **kwargs)

    def redraw(self):
        vs = self.vertices
        if len(vs) != 3:
            return self

        ref = vs[0]
        view_scale = ref.circle.width / (2 * ref.radius)
        pad = self.pad * view_scale

        centers = [np.array(v.point, dtype=float) for v in vs]
        radii = [v.circle.width / 2.0 + pad for v in vs]
        centroid = sum(centers) / 3.0

        # Traverse the corners counter-clockwise.
        if self._signed_area(centers) < 0:
            order = [0, 2, 1]
        else:
            order = [0, 1, 2]
        C = [centers[i] for i in order]
        R = [radii[i] for i in order]

        # Outward unit normal of each edge C[k] -> C[k+1].
        normals = []
        for k in range(3):
            u = C[(k + 1) % 3] - C[k]
            u = u / np.linalg.norm(u)
            perp = np.array([-u[1], u[0], 0.0])
            mid = 0.5 * (C[k] + C[(k + 1) % 3])
            if np.dot(perp, mid - centroid) < 0:
                perp = -perp
            normals.append(perp)

        # Corner i: arc from the incoming edge's tangent direction to the
        # outgoing edge's tangent direction, swept CCW around the vertex.
        # Connecting consecutive arcs yields the straight sides for free.
        pts = []
        for i in range(3):
            n_in = normals[(i - 1) % 3]
            n_out = normals[i]
            a0 = np.arctan2(n_in[1], n_in[0])
            a1 = np.arctan2(n_out[1], n_out[0])
            while a1 < a0:
                a1 += TAU
            for a in np.linspace(a0, a1, self.arc_samples):
                pts.append(C[i] + R[i] * np.array([np.cos(a), np.sin(a), 0.0]))

        pts.append(pts[0])
        self.set_points_as_corners(pts)
        return self

    @staticmethod
    def _signed_area(centers):
        s = 0.0
        for i in range(len(centers)):
            x1, y1 = centers[i][0], centers[i][1]
            x2, y2 = centers[(i + 1) % len(centers)][0], centers[(i + 1) % len(centers)][1]
            s += x1 * y2 - x2 * y1
        return 0.5 * s
