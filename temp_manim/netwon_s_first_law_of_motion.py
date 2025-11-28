from manim import *

class AutoTeach(Scene):
    def construct(self):
        title = Text("Newton's First Law of Motion", font_size=48)
        title.to_edge(UP)
        self.play(Write(title))
        self.wait(1)

        law = Text("An object at rest stays at rest,\nand an object in motion stays in motion\nat constant velocity,\nunless acted upon by a net force.", font_size=30)
        law.next_to(title, DOWN, buff=0.5)
        self.play(Write(law))
        self.wait(2)

        box = Square(side_length=1.5, color=BLUE)
        box_label = Text("Object", font_size=24)
        box_label.next_to(box, DOWN)
        self.play(Create(box), Write(box_label))
        self.wait(1)

        arrow1 = Arrow(ORIGIN, 3*RIGHT, buff=0, color=GREEN)
        arrow1.next_to(box, RIGHT, buff=0.5)
        push_label = Text("Push", font_size=24)
        push_label.next_to(arrow1, UP)
        self.play(GrowArrow(arrow1), Write(push_label))
        self.wait(1)

        self.play(box.animate.shift(5*RIGHT), run_time=2)
        self.wait(1)

        arrow2 = Arrow(ORIGIN, 3*LEFT, buff=0, color=RED)
        arrow2.next_to(box, LEFT, buff=0.5)
        friction_label = Text("Friction", font_size=24)
        friction_label.next_to(arrow2, UP)
        self.play(GrowArrow(arrow2), Write(friction_label))
        self.wait(1)

        self.play(box.animate.shift(3*LEFT), run_time=2)
        self.wait(1)

        summary = Text("Without net force, motion continues unchanged.", font_size=30)
        summary.to_edge(DOWN)
        self.play(Write(summary))
        self.wait(2)