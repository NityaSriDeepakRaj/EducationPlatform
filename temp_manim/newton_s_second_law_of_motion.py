from manim import *

class AutoTeach(Scene):
    def construct(self):
        title = Text("Newton's Second Law", font_size=48)
        self.play(Write(title))
        self.wait()
        self.play(title.animate.to_edge(UP))

        stmt = Text("Force equals mass times acceleration", font_size=32)
        self.play(FadeIn(stmt))
        self.wait()
        self.play(stmt.animate.next_to(title, DOWN, buff=0.5))

        box = Rectangle(width=2, height=1, color=BLUE, fill_opacity=0.5)
        box_label = Text("m", font_size=24).move_to(box.get_center())
        mass = VGroup(box, box_label)
        mass.to_edge(LEFT, buff=2)
        self.play(Create(box), Write(box_label))
        self.wait()

        arrow = Arrow(start=mass.get_right(), end=mass.get_right() + 3*RIGHT, buff=0.2, color=YELLOW)
        arrow_label = Text("F", font_size=24).next_to(arrow, UP)
        self.play(GrowArrow(arrow), Write(arrow_label))
        self.wait()

        accel = Text("a", font_size=36).next_to(mass, DOWN, buff=0.7)
        accel_arrow = Arrow(start=mass.get_bottom(), end=mass.get_bottom() + 2*DOWN, buff=0.2, color=RED)
        accel_group = VGroup(accel, accel_arrow)
        self.play(Create(accel_arrow), Write(accel))
        self.wait()

        formula = Text("F = m a", font_size=40, color=GREEN)
        formula.to_edge(RIGHT, buff=2)
        self.play(TransformFromCopy(arrow_label[0], formula[0]))
        self.play(TransformFromCopy(box_label[0], formula[2]))
        self.play(Write(formula[1]), Write(formula[3]))
        self.wait()

        self.play(
            mass.animate.shift(4*RIGHT),
            accel_group.animate.shift(4*RIGHT),
            run_time=2
        )
        self.wait()

        summary = Text("Greater force → Greater acceleration", font_size=28)
        summary.next_to(stmt, DOWN, buff=0.8)
        self.play(Write(summary))
        self.wait(2)

        self.play(FadeOut(title), FadeOut(stmt), FadeOut(summary), FadeOut(formula),
                  FadeOut(arrow), FadeOut(arrow_label), FadeOut(mass), FadeOut(accel_group))
        self.wait()