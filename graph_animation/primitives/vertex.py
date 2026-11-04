from __future__ import annotations

from manim import *

from .constants import *

class Vertex(VGroup):
    """
    A reusable graph vertex.

    Components
    ----------
    circle
    label
    degree_label

    Public API
    ----------
    select()
    deselect()
    gray()
    activate()
    pulse()
    show_degree()
    hide_degree()
    """

    def __init__(
        self,
        name: str,
        position=ORIGIN,
        radius=0.18,
        fill_color=WHITE,
        stroke_color=BLACK,
        label_color=BLACK,
        **kwargs,
    ):

        super().__init__(**kwargs)

        self.name = name
        self.radius = radius
        self.active = True
        self.selected = False

        self.halo = Circle(
            radius=radius + 0.08,
            stroke_color=HALO_COLOR,
            stroke_width=4,
        )
        self.halo.set_opacity(0)


        self.circle = Circle(
            radius=radius,
            fill_color=fill_color,
            fill_opacity=1,
            stroke_color=stroke_color,
            stroke_width=2,
        )

        self.label = MathTex(name)
        self.label.set_color(label_color)
        self.label.scale(LABEL_SCALE)

        # The degree label lives *inside* the vertex, so it is part of
        # the graph view and scales with it automatically. Its content
        # is set once (set_degree) while the graph is still at base
        # scale; afterwards it just rides along with the view. It starts
        # invisible until show_degree() reveals it.
        self.degree_label = MathTex("", color=DARK_BLUE)
        self.degree_label.set_opacity(0)

        self.add(
            self.halo,
            self.circle,
            self.label,
            self.degree_label,
        )

        self.move_to(position)

    # -------------------------------------------------
    # Convenience properties
    # -------------------------------------------------

    @property
    def point(self):
        return self.circle.get_center()

    # -------------------------------------------------
    # Degree label
    # -------------------------------------------------

    def set_degree(self, value):
        """
        Fill in the degree label at base scale. Call this once, before
        the graph view is scaled: the label then scales with the view
        like any other child, so it never has to be re-sized by hand.
        The same LABEL_SCALE as the vertex name keeps the two in sync.
        """
        self.degree_label.become(
            MathTex(f"({value})", color=DARK_BLUE)
            .scale(LABEL_SCALE)
            .next_to(self.circle, UP, buff=0.12)
        )
        self.degree_label.set_opacity(0)
        return self

    def degree_target(self, value):
        """
        A new degree label for an updated value, matched to the current
        on-screen size and position of the existing one — so an update
        reuses the label's scale instead of recomputing it.
        """
        target = MathTex(f"({value})", color=DARK_BLUE)
        target.match_height(self.degree_label)
        target.move_to(self.degree_label)
        return target

    # -------------------------------------------------
    # Animations
    # -------------------------------------------------

    def show_halo(self):
        self.halo.scale(0.85)
        return AnimationGroup(
            self.halo.animate
                .set_opacity(1)
                .scale(1 / 0.85)
        )

    def hide_halo(self):
        return self.halo.animate.set_opacity(0)
    
    def pulse(self, scale=1.15):
        return AnimationGroup(
            self.animate.scale(scale),
            rate_func=there_and_back,
        )

    def flash(self):
        return Flash(
            self.circle,
            color=YELLOW,
            line_length=0.15,
        )

    def select(self):
        self.selected = True
    
        return AnimationGroup(
            self.circle.animate.set_fill(
                GREEN,
                opacity=1,
            ),
            self.label.animate.set_color(WHITE),
        )

    def is_active(self):
        return self.active
        
        
    def deselect(self):

        self.selected = False
    
        return AnimationGroup(
            self.circle.animate.set_fill(
                WHITE,
                opacity=1,
            ),
            self.label.animate.set_color(BLACK),
        )

    def gray(self):

        self.active = False
    
        return AnimationGroup(
            self.circle.animate.set_fill(
                GRAY,
                opacity=1,
            ),
            self.label.animate.set_color(WHITE),
            self.degree_label.animate.set_opacity(0),
        )

    def activate(self):

        self.active = True
        self.selected = False
    
        return AnimationGroup(
            self.circle.animate.set_fill(
                WHITE,
                opacity=1,
            ),
            self.circle.animate.set_stroke(
                BLACK,
                width=2,
            ),
            self.label.animate.set_color(BLACK),
        )

    def move_to(self, point):

        super().move_to(point)
    
        return self
