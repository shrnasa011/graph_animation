# primitives/constants.py

from manim import *

VERTEX_FILL = WHITE
VERTEX_SELECTED = "#145A32"
VERTEX_GRAY = "#BBBBBB"

VERTEX_BORDER = BLACK

EDGE_COLOR = GRAY_D
EDGE_WIDTH = 2
EDGE_HIGHLIGHT = YELLOW
EDGE_INACTIVE_OPACITY = 0.25

HALO_COLOR = GOLD
DEGREE_COLOR = BLUE

# Scale applied to the LaTeX inside a vertex. The degree labels reuse
# this so both read at the same font size.
LABEL_SCALE = 0.6

# ---------------------------------------------------------------
# Hyperedges
# ---------------------------------------------------------------

# Padding (in base units) between a member vertex circle and the
# enclosing blob outline.
HYPEREDGE_PAD = 0.30

HYPEREDGE_STROKE_WIDTH = 3
HYPEREDGE_FILL_OPACITY = 0.16
HYPEREDGE_HIGHLIGHT_FILL_OPACITY = 0.34
HYPEREDGE_INACTIVE_OPACITY = 0.10

# Number of sample points placed around each member vertex when
# building the enclosing hull (higher = smoother blob).
HYPEREDGE_SAMPLES = 16

# Default colour cycle assigned to hyperedges.
HYPEREDGE_PALETTE = [
    BLUE_D,
    RED_D,
    GREEN_D,
    PURPLE_D,
    ORANGE,
    TEAL_D,
    MAROON_D,
]

# ---------------------------------------------------------------
# 3-uniform hyperedges (rounded triangles)
# ---------------------------------------------------------------

# Gap (base units) between each member vertex circle and the triangle
# outline that wraps around it. Any positive value guarantees the
# vertices are fully covered by the triangle.
TRIEDGE_PAD = 0.16