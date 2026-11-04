from __future__ import annotations

import numpy as np
import contourpy
from scipy.spatial import ConvexHull as SciPyConvexHull

from manim import *


class ContainerBlob(VGroup):
    """A padded container drawn around a collection of vertices.

    ``shape=\"convex\"`` creates a conventional convex hull.
    ``shape=\"connected\"`` creates one smooth, non-convex outline around a
    minimum-spanning-tree neighbourhood of the vertices.  This keeps inactive
    vertices outside the boundary whenever the geometry allows it.
    """

    def __init__(
        self,
        vertices,
        padding: float = 0.35,
        color=GREEN,
        samples: int = 20,
        shape: str = "convex",
        **kwargs,
    ):
        super().__init__(**kwargs)
        self.padding = padding
        self.color = color
        self.samples = samples
        if shape not in {"convex", "connected"}:
            raise ValueError("shape must be either 'convex' or 'connected'.")
        self.shape = shape
        self.update_boundary(vertices)

    def _convex_boundary(self, vertices):
        """Return a padded convex-hull outline as a single VMobject."""
        angles = np.linspace(0, TAU, self.samples, endpoint=False)
        cloud = []
        for vertex in vertices:
            centre = np.array(vertex.point, dtype=float)
            radius = vertex.circle.width / 2 + self.padding
            cloud.extend(
                centre + radius * np.array([np.cos(angle), np.sin(angle), 0])
                for angle in angles
            )

        points = np.array([point[:2] for point in cloud])
        try:
            # ``manim`` also exports a ``ConvexHull`` symbol, so use the
            # explicitly aliased SciPy implementation here.
            hull = SciPyConvexHull(points)
            boundary = [cloud[index] for index in hull.vertices]
        except Exception:
            boundary = cloud[: self.samples]

        outline = VMobject()
        outline.set_points_as_corners([*boundary, boundary[0]])
        outline.set_stroke(color=self.color, width=3, opacity=1)
        outline.set_fill(color=self.color, opacity=0.15)
        return outline

    def _connected_boundary(self, vertices):
        """Return one outer contour around a rounded spanning-tree region."""
        radius = max(vertex.circle.width / 2 + self.padding for vertex in vertices)
        centres = [np.array(vertex.point, dtype=float) for vertex in vertices]

        # Prim's algorithm gives the least intrusive set of connections, so
        # it avoids the broad diagonal chord produced by a convex hull.
        tree_edges = []
        reached = {0}
        while len(reached) < len(vertices):
            _, source, target = min(
                (
                    np.linalg.norm(centres[source] - centres[target]),
                    source,
                    target,
                )
                for source in reached
                for target in range(len(vertices))
                if target not in reached
            )
            tree_edges.append((source, target))
            reached.add(target)

        # Rasterise the union of padded vertex disks and padded tree segments,
        # then extract its *single outer contour*.  Unlike rendering disks and
        # corridors separately, this gives one continuous blob boundary.
        # A sub-pixel grid at low quality keeps the extracted outline smooth.
        step = min(0.015, radius / 20)
        min_x = min(point[0] for point in centres) - radius - step
        max_x = max(point[0] for point in centres) + radius + step
        min_y = min(point[1] for point in centres) - radius - step
        max_y = max(point[1] for point in centres) + radius + step
        xs = np.arange(min_x, max_x + step, step)
        ys = np.arange(min_y, max_y + step, step)
        x_grid, y_grid = np.meshgrid(xs, ys)
        inside = np.zeros_like(x_grid, dtype=bool)

        for centre in centres:
            inside |= (x_grid - centre[0]) ** 2 + (y_grid - centre[1]) ** 2 <= radius**2

        for source, target in tree_edges:
            start, end = centres[source], centres[target]
            direction = end[:2] - start[:2]
            length_squared = np.dot(direction, direction)
            projection = np.clip(
                ((x_grid - start[0]) * direction[0] + (y_grid - start[1]) * direction[1])
                / length_squared,
                0,
                1,
            )
            nearest_x = start[0] + projection * direction[0]
            nearest_y = start[1] + projection * direction[1]
            inside |= (x_grid - nearest_x) ** 2 + (y_grid - nearest_y) ** 2 <= radius**2

        paths = contourpy.contour_generator(x=xs, y=ys, z=inside.astype(float)).lines(0.5)
        boundary_2d = max(
            paths,
            key=lambda path: abs(
                np.dot(path[:, 0], np.roll(path[:, 1], -1))
                - np.dot(path[:, 1], np.roll(path[:, 0], -1))
            ),
        )
        boundary = [np.array([x, y, 0]) for x, y in boundary_2d]
        # Keep only regularly spaced anchors before spline interpolation; the
        # raw marching-squares contour has many nearly identical grid points.
        boundary = boundary[::20]
        outline = VMobject()
        # ``contourpy`` returns a staircase of short grid segments.  Convert
        # it to a closed cubic path so it reads as one organic blob instead
        # of a collection of tiny straight pieces.
        outline.set_points_smoothly([*boundary, boundary[0]])
        outline.set_stroke(color=self.color, width=3, opacity=1)
        outline.set_fill(color=self.color, opacity=0.15)
        return outline

    def update_boundary(self, vertices):
        """Replace the boundary with one enclosing ``vertices``."""
        vertices = list(vertices)
        if not vertices:
            raise ValueError("ContainerBlob requires at least one vertex.")

        self.remove(*self.submobjects)
        if self.shape == "connected":
            self.add(self._connected_boundary(vertices))
        else:
            self.add(self._convex_boundary(vertices))
        return self

    def animate_to(self, vertices, shape: str | None = None):
        """Return an animation that morphs the blob around ``vertices``.

        An empty container has no boundary, so it is represented by fading
        the current blob out.  This makes terminal containers such as
        ``C_k = \\varnothing`` straightforward to animate.
        """
        vertices = list(vertices)
        if not vertices:
            return FadeOut(self)

        target_shape = self.shape if shape is None else shape
        if target_shape not in {"convex", "connected"}:
            raise ValueError("shape must be either 'convex' or 'connected'.")
        # Keep later transitions in the requested geometry mode after this
        # animation has finished.
        self.shape = target_shape

        target = ContainerBlob(
            vertices,
            padding=self.padding,
            color=self.color,
            samples=self.samples,
            shape=target_shape,
        )
        return Transform(self, target)
