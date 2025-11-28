from manim import *

class AutoTeach(Scene):
    def construct(self):
        title = Text("Gravitational Law", font_size=48)
        self.play(Write(title))
        self.wait()
        self.play(title.animate.to_edge(UP))

        stmt1 = Text("Every mass attracts every other mass", font_size=32)
        stmt1.next_to(title, DOWN, buff=0.7)
        self.play(FadeIn(stmt1))
        self.wait()

        stmt2 = Text("Force acts along the line joining centers", font_size=32)
        stmt2.next_to(stmt1, DOWN, buff=0.4)
        self.play(FadeIn(stmt2))
        self.wait()

        stmt3 = Text("Force is proportional to the product of masses", font_size=32)
        stmt3.next_to(stmt2, DOWN, buff=0.4)
        self.play(FadeIn(stmt3))
        self.wait()

        stmt4 = Text("Force is inversely proportional to distance squared", font_size=32)
        stmt4.next_to(stmt3, DOWN, buff=0.4)
        self.play(FadeIn(stmt4))
        self.wait()

        self.play(
            FadeOut(stmt1),
            FadeOut(stmt2),
            FadeOut(stmt3),
            FadeOut(stmt4),
        )

        m1 = Circle(radius=0.6, color=BLUE, fill_opacity=1).shift(3 * LEFT)
        m2 = Circle(radius=0.6, color=RED, fill_opacity=1).shift(3 * RIGHT)
        label1 = Text("m1", font_size=24).move_to(m1.get_center())
        label2 = Text("m2", font_size=24).move_to(m2.get_center())
        self.play(FadeIn(m1), FadeIn(label1), FadeIn(m2), FadeIn(label2))

        arrow = DoubleArrow(
            m1.get_right(),
            m2.get_left(),
            buff=0.1,
            color=YELLOW,
            stroke_width=4,
        )
        r_text = Text("r", font_size=30).next_to(arrow, DOWN, buff=0.2)
        self.play(GrowFromCenter(arrow), FadeIn(r_text))
        self.wait()

        force_text = Text("F = G m1 m2 / r^2", font_size=36)
        force_text.to_edge(DOWN, buff=1)
        self.play(Write(force_text))
        self.wait()

        self.play(
            Indicate(m1, scale_factor=1.2),
            Indicate(m2, scale_factor=1.2),
            Indicate(arrow, scale_factor=1.1),
            Indicate(force_text, scale_factor=1.1),
        )
        self.wait()

        self.play(
            FadeOut(title),
            FadeOut(m1),
            FadeOut(label1),
            FadeOut(m2),
            FadeOut(label2),
            FadeOut(arrow),
            FadeOut(r_text),
            FadeOut(force_text),
        )
        self.wait()