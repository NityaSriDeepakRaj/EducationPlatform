from manim import *

class AutoTeach(Scene):
    def construct(self):
        title = Text("Electromagnetic Waves", font_size=48)
        self.play(Write(title))
        self.wait(1)
        self.play(title.animate.to_edge(UP))

        intro = Text("Oscillating electric and magnetic fields", font_size=30)
        self.play(FadeIn(intro))
        self.wait(2)
        self.play(FadeOut(intro))

        axes = Axes(x_range=[0, 4 * PI, PI / 2], y_range=[-2, 2, 1], x_length=10, y_length=4)
        axes.shift(DOWN * 0.5)
        self.play(Create(axes))

        e_wave = axes.plot(lambda t: np.sin(t), color=BLUE)
        b_wave = axes.plot(lambda t: np.sin(t), color=RED)

        e_label = Text("Electric field", font_size=24).next_to(e_wave, UP, buff=0.5).set_color(BLUE)
        b_label = Text("Magnetic field", font_size=24).next_to(e_wave, DOWN, buff=0.5).set_color(RED)

        self.play(Create(e_wave), FadeIn(e_label))
        self.wait(1)
        self.play(Create(b_wave), FadeIn(b_label))
        self.wait(2)

        arrow_e = Arrow(start=ORIGIN, end=UP * 2, color=BLUE, buff=0)
        arrow_b = Arrow(start=ORIGIN, end=RIGHT * 2, color=RED, buff=0)
        arrow_k = Arrow(start=ORIGIN, end=OUT * 2, color=GREEN, buff=0)

        label_e = Text("E", font_size=24).next_to(arrow_e, UP).set_color(BLUE)
        label_b = Text("B", font_size=24).next_to(arrow_b, RIGHT).set_color(RED)
        label_k = Text("Direction", font_size=24).next_to(arrow_k, OUT).set_color(GREEN)

        self.play(
            FadeOut(axes), FadeOut(e_wave), FadeOut(b_wave), FadeOut(e_label), FadeOut(b_label),
            FadeIn(arrow_e), FadeIn(arrow_b), FadeIn(arrow_k),
            FadeIn(label_e), FadeIn(label_b), FadeIn(label_k)
        )
        self.wait(2)

        speed = Text("Speed in vacuum: 3 x 10^8 m/s", font_size=30)
        speed.to_edge(DOWN)
        self.play(Write(speed))
        self.wait(2)

        outro = Text("Transverse wave, no medium required", font_size=30)
        self.play(FadeOut(speed), FadeIn(outro))
        self.wait(2)

        self.play(FadeOut(outro), FadeOut(arrow_e), FadeOut(arrow_b), FadeOut(arrow_k),
                  FadeOut(label_e), FadeOut(label_b), FadeOut(label_k), FadeOut(title))