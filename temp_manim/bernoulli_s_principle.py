from manim import *

class AutoTeach(Scene):
    def construct(self):
        title = Text("Bernoulli's Principle", font_size=48)
        subtitle = Text("Fast air, low pressure", font_size=32).next_to(title, DOWN)
        self.play(Write(title))
        self.play(FadeIn(subtitle))
        self.wait(1)
        self.play(FadeOut(title), FadeOut(subtitle))

        tube = Rectangle(width=6, height=1.5, color=WHITE)
        left = Rectangle(width=1, height=2, color=WHITE).next_to(tube, LEFT, buff=0)
        right = Rectangle(width=1, height=2, color=WHITE).next_to(tube, RIGHT, buff=0)
        pipe = VGroup(left, tube, right)
        self.play(Create(pipe))
        self.wait(0.5)

        narrow = Rectangle(width=2, height=0.6, color=WHITE).move_to(tube)
        self.play(Transform(tube, narrow))
        self.wait(0.5)

        label_wide = Text("Wide", font_size=24).next_to(left, DOWN)
        label_narrow = Text("Narrow", font_size=24).next_to(right, DOWN)
        self.play(Write(label_wide), Write(label_narrow))
        self.wait(0.5)

        arrow1 = Arrow(start=left.get_edge_center(LEFT), end=left.get_edge_center(RIGHT), buff=0.2, color=BLUE)
        arrow2 = Arrow(start=right.get_edge_center(LEFT), end=right.get_edge_center(RIGHT), buff=0.2, color=RED)
        self.play(GrowArrow(arrow1))
        self.play(GrowArrow(arrow2))
        self.wait(0.5)

        speed1 = Text("Slow", font_size=24).next_to(arrow1, UP)
        speed2 = Text("Fast", font_size=24).next_to(arrow2, UP)
        self.play(Write(speed1), Write(speed2))
        self.wait(0.5)

        press1 = Text("High Pressure", font_size=24).next_to(left, DOWN*2.5)
        press2 = Text("Low Pressure", font_size=24).next_to(right, DOWN*2.5)
        self.play(Write(press1), Write(press2))
        self.wait(1)

        lift_arrow = Arrow(start=ORIGIN, end=UP*2, color=YELLOW).shift(RIGHT*4)
        lift_label = Text("Lift!", font_size=32).next_to(lift_arrow, UP)
        self.play(GrowArrow(lift_arrow), Write(lift_label))
        self.wait(2)

        self.play(FadeOut(pipe), FadeOut(label_wide), FadeOut(label_narrow),
                  FadeOut(arrow1), FadeOut(arrow2), FadeOut(speed1), FadeOut(speed2),
                  FadeOut(press1), FadeOut(press2), FadeOut(lift_arrow), FadeOut(lift_label))

        summary = Text("Bernoulli: Speed up air → pressure drops", font_size=36)
        self.play(Write(summary))
        self.wait(3)
        self.play(FadeOut(summary))