"""Input graph and induced random-sample illustration.

Render with::

    manim -pqh random_sample_graph.py RandomSampleGraph
"""

from manim import *

from graph_animation import Graph


SAMPLE_FILL = "#4B4BFF"
SAMPLE_STROKE = "#1D1DB8"
INACTIVE_FILL = "#E6E6E6"
INACTIVE_STROKE = "#A9A9A9"
EDGE_COLOR = "#ACACAC"
TEXT_COLOR = "#263D42"


class RandomSampleGraph(Scene):
    """Show a highlighted random sample and the graph it induces."""

    def construct(self):
        self.camera.background_color = WHITE

        # The four blue vertices are the sampled vertices.  The other names
        # are deliberately hidden: they only provide the surrounding input
        # graph structure.
        positions = {
            "a": [-6.1, 2.2, 0], "b": [-4.6, 2.45, 0],
            "c": [-3.05, 1.8, 0], "d": [-1.65, 0.75, 0],
            "e": [-6.55, -0.4, 0], "f": [-5.1, 0.15, 0],
            "g": [-5.8, -2.05, 0], "h": [-4.15, -2.05, 0],
            "i": [-3.25, -0.25, 0], "j": [-2.35, -1.3, 0],
            "l": [-2.15, -0.95, 0], "k": [-2.7, 1.75, 0],
            "m": [-1.55, -1.65, 0],
        }
        edges = [
            ("a", "b"), ("a", "e"), ("b", "f"), ("b", "k"),
            ("e", "f"), ("e", "g"), ("e", "h"), ("f", "h"),
            ("f", "i"), ("k", "i"), ("k", "d"), ("i", "d"),
            ("i", "l"), ("d", "j"), ("h", "g"), ("h", "l"),
            ("g", "h"), ("l", "j"), ("j", "m"),
        ]
        input_graph = Graph(list(positions), edges, positions)
        self._style_input_graph(input_graph, sample={"e", "f", "k", "m"})

        # The induced graph retains exactly the sample vertices and edges
        # from the input graph: e--f--k and f--m.
        sample_positions = {
            "e": [4.25, -2.05, 0], "f": [5.65, -0.95, 0],
            "k": [4.95, 0.8, 0], "m": [6.85, -1.45, 0],
        }
        sample_graph = Graph(
            vertices=list(sample_positions),
            edges=[("e", "f"), ("f", "k"), ("f", "m")],
            positions=sample_positions,
        )
        self._style_sample_graph(sample_graph)

        arrow = Arrow(
            start=[-0.95, -0.45, 0], end=[3.55, -0.45, 0],
            color=TEXT_COLOR, stroke_width=3, buff=0.05,
        )
        arrow_label = Text("Random Sample", font_size=27, color=TEXT_COLOR)
        arrow_label.next_to(arrow, UP, buff=0.42)

        input_label = Text("Input Graph", font_size=25, color=TEXT_COLOR)
        input_label.move_to([-4.0, -3.2, 0])
        sample_label = Text("Induced Sample", font_size=25, color=TEXT_COLOR)
        sample_label.move_to([5.6, -3.2, 0])

        self.add(
            input_graph.view,
            arrow,
            arrow_label,
            sample_graph.view,
            input_label,
            sample_label,
        )

    @staticmethod
    def _style_input_graph(graph: Graph, sample: set[str]):
        for edge in graph.edges.values():
            edge.set_stroke(EDGE_COLOR, width=2)

        for name, vertex in graph.vertices.items():
            vertex.circle.set_fill(INACTIVE_FILL, opacity=1)
            vertex.circle.set_stroke(INACTIVE_STROKE, width=1.5)
            vertex.label.set_opacity(0)
            if name in sample:
                vertex.circle.set_fill(SAMPLE_FILL, opacity=1)
                vertex.circle.set_stroke(SAMPLE_STROKE, width=1.5)
                vertex.label.set_color(WHITE).set_opacity(1)

    @staticmethod
    def _style_sample_graph(graph: Graph):
        for edge in graph.edges.values():
            edge.set_stroke(EDGE_COLOR, width=2)
        for vertex in graph.vertices.values():
            vertex.circle.set_fill(SAMPLE_FILL, opacity=1)
            vertex.circle.set_stroke(SAMPLE_STROKE, width=1.5)
            vertex.label.set_color(WHITE).set_opacity(1)
