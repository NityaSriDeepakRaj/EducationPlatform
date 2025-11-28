from manim import *

class AutoTeach(Scene):
    def construct(self):
        title = Text("Oscillatory Motion", font_size=48)
        self.play(Write(title))
        self.wait()
        self.play(title.animate.to_edge(UP))

        line = NumberLine(x_range=[-4, 4, 1], length=8, include_tip=True)
        self.play(Create(line))
        self.wait()

        dot = Dot(color=YELLOW).move_to(line.number_to_point(0))
        self.play(FadeIn(dot))
        self.wait()

        arrow = Arrow(ORIGIN, RIGHT, buff=0, color=RED)
        arrow.next_to(dot, UP)
        self.play(GrowArrow(arrow))
        self.wait()

        label = Text("Displacement", font_size=24).next_to(arrow, UP)
        self.play(Write(label))
        self.wait()

        def update_dot(mob, alpha):
            mob.move_to(line.number_to_point(3 * np.sin(4 * PI * alpha)))

        def update_arrow(mob, alpha):
            x = 3 * np.sin(4 * PI * alpha)
            mob.put_start_and_end_on(
                line.number_to_point(x) + UP * 0.3,
                line.number_to_point(x) + RIGHT * 0.5 + UP * 0.3
            )

        self.play(
            UpdateFromAlphaFunc(dot, update_dot),
            UpdateFromAlphaFunc(arrow, update_arrow),
            run_time=4
        )
        self.wait()

        self.play(FadeOut(label), FadeOut(arrow))
        self.wait()

        center_text = Text("Equilibrium", font_size=24).next_to(line.number_to_point(0), DOWN)
        self.play(Write(center_text))
        self.wait()

        left_text = Text("Maximum left", font_size=20).move_to(line.number_to_point(-3) + DOWN * 0.5)
        right_text = Text("Maximum right", font_size=20).move_to(line.number_to_point(3) + DOWN * 0.5)
        self.play(Write(left_text), Write(right_text))
        self.wait()

        self.play(
            UpdateFromAlphaFunc(dot, update_dot),
            run_time=4
        )
        self.wait()

        summary = Text("Back-and-forth around equilibrium", font_size=30).to_edge(DOWN)
        self.play(Write(summary))
        self.wait(2)

        self.play(*[FadeOut(m) for m in self.mobjects])