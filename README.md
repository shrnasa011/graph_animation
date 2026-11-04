# Graph Animation

Graph Animation is a small [Manim](https://www.manim.community/) library for
building animated graphs and hypergraphs. It provides reusable vertex, edge,
and graph objects, plus example scenes you can render and adapt.

## Setup

Use Python 3.10 or newer. Create and activate a virtual environment, then
install Manim and NumPy:

```bash
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
python -m pip install manim numpy
```

The graph labels use Manim's `MathTex`, so rendering also needs a LaTeX installation and `dvisvgm`. On Debian/Ubuntu (including Colab), install `texlive-latex-extra`, `texlive-fonts-recommended`, `cm-super`, and `dvisvgm`. The Colab setup cell in `Demos.ipynb` installs these automatically.

Run commands from this directory. For example, render the basic graph scene:

```bash
manim -pql demo.py GraphDemo
```

`-pql` renders a quick low-quality preview and opens it when finished. Use
`-qh` for a high-quality render without the preview window.

## Examples

```bash
manim -pql demo_hypergraph.py HyperGraphDemo
manim -pql demo_tri_hypergraph.py TriHyperGraphDemo
manim -pql demo_sizes.py GraphDemo60 GraphDemo30
```

The Jupyter notebooks contain exploratory animations and simulations. The
standalone Python scenes are the easiest place to start when creating a new
animation.

## Build a graph

```python
import numpy as np
from manim import Scene, WHITE
from graph_animation import Graph


class Example(Scene):
    def construct(self):
        self.camera.background_color = WHITE
        positions = {
            "a": np.array([-1, 0, 0]),
            "b": np.array([1, 0, 0]),
        }
        graph = Graph(
            vertices=["a", "b"],
            edges=[("a", "b")],
            positions=positions,
        )
        self.add(graph.view)
        self.play(graph.show_degrees())
```

`Graph` takes vertex names, edge pairs, and a 3D position for each vertex.
`HyperGraph` accepts hyperedges containing any number of vertices, while
`TriHyperGraph` draws three-vertex hyperedges. Each object exposes animation
helpers such as `select`, `show_halo`, `gray_vertices`, and `update_degrees`.

## Package overview

- `graph_animation/graph.py`: ordinary graph model and animation helpers.
- `graph_animation/hypergraph.py`: general and 3-uniform hypergraphs.
- `graph_animation/primitives/`: vertices, edges, and drawing primitives.
- `demo*.py`: runnable Manim scenes.
