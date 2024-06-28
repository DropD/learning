"""The example scene from the quickstart section of the tutorial."""

from manim import (
    Scene,
    Circle,
    Square,
    Create,
    Transform,
    ReplacementTransform,
    FadeOut,
    PINK,
    BLUE,
    PI,
    RIGHT,
)


class CreateCircle(Scene):
    """Animate creation of a circle."""

    def construct(self):
        """Construct the scene."""
        circle = Circle()
        circle.set_fill(PINK, opacity=0.5)
        self.play(Create(circle))


class SquareToCircle(Scene):
    """Transform a square into a circle."""

    def construct(self):
        """Construct the scene."""
        circle = Circle()
        circle.set_fill(PINK, opacity=0.5)

        square = Square()
        square.rotate(PI / 4)

        self.play(Create(square))
        self.play(Transform(square, circle))
        self.play(FadeOut(square))


class SquareAndCircle(Scene):
    """Position the square next to the circle."""

    def construct(self):
        """Construct the scene."""
        circle = Circle()
        circle.set_fill(PINK, opacity=0.5)

        square = Square()
        square.set_fill(BLUE, opacity=0.5)

        square.next_to(circle, RIGHT, buff=0.5)
        self.play(Create(circle), Create(square))


class AnimatedSquareToCircle(Scene):
    """Transform the square into a circle using .animate syntax."""

    def construct(self):
        """Construct the scene."""
        circle = Circle()
        square = Square()

        self.play(Create(square))
        self.play(square.animate.rotate(PI / 4))
        self.play(ReplacementTransform(square, circle))
        self.play(circle.animate.set_fill(PINK, opacity=0.5))
