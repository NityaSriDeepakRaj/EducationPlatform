from manim import *

class AutoTeach(Scene):
    def construct(self):
        title = Text("Electromagnetic Waves", font_size=60)
        subtitle = Text("Self-propagating waves of electric & magnetic fields", font_size=30)
        subtitle.next_to(title, DOWN)
        self.play(Write(title))
        self.play(FadeIn(subtitle))
        self.wait(2)
        self.play(FadeOut(subtitle))

        charge = Dot(LEFT*4, color=YELLOW)
        charge_label = Text("wiggling charge", font_size=24).next_to(charge, DOWN)
        self.play(FadeIn(charge), Write(charge_label))
        self.wait()

        E_label = Text("Electric Field", font_size=28, color=BLUE).to_edge(UP).shift(LEFT*3)
        B_label = Text("Magnetic Field", font_size=28, color=RED).to_edge(UP).shift(RIGHT*3)
        self.play(Write(E_label), Write(B_label))

        E_wave = VGroup()
        B_wave = VGroup()
        for i in range(30):
            x = -6 + i*0.4
            y_E = 2*np.sin(i*0.4)
            y_B = 2*np.cos(i*0.4)
            E_vec = Arrow(start=np.array([x, 0, 0]), end=np.array([x, y_E, 0]), color=BLUE, buff=0)
            B_vec = Arrow(start=np.array([x, 0, 0]), end=np.array([x, 0, y_B]), color=RED, buff=0)
            E_wave.add(E_vec)
            B_wave.add(B_vec)

        self.play(Create(E_wave), Create(B_wave))
        self.wait()

        transverse = Text("Transverse: fields perpendicular to travel", font_size=28).to_edge(DOWN)
        self.play(Write(transverse))
        self.wait(2)

        self.play(
            E_wave.animate.shift(RIGHT*8),
            B_wave.animate.shift(RIGHT*8),
            rate_func=linear,
            run_time=4
        )
        self.wait()

        speed = Text("Speed in vacuum: 300,000 km/s", font_size=32).to_edge(DOWN)
        self.play(ReplacementTransform(transverse, speed))
        self.wait(2)

        spectrum = Text("Spectrum: radio → microwave → infrared → light → UV → X-ray → gamma", font_size=24).to_edge(DOWN*2)
        self.play(Write(spectrum))
        self.wait(2)

        self.play(FadeOut(VGroup(title, E_label, B_label, charge, charge_label, E_wave, B_wave, speed, spectrum)))