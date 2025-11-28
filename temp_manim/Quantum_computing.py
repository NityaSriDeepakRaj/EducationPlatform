from manim import *

class AutoTeach(Scene):
    def construct(self):
        title = Text("Quantum Computing", font_size=60)
        subtitle = Text("A new era of computation", font_size=30).next_to(title, DOWN)
        self.play(Write(title), FadeIn(subtitle))
        self.wait(2)
        self.play(FadeOut(title), FadeOut(subtitle))

        bit_text = Text("Classical Bit", font_size=40).to_edge(LEFT).shift(UP*2)
        qubit_text = Text("Qubit", font_size=40).to_edge(RIGHT).shift(UP*2)
        self.play(Write(bit_text), Write(qubit_text))

        zero = Text("0", font_size=50).move_to(bit_text.get_center()+DOWN*1.5)
        one = Text("1", font_size=50).next_to(zero, DOWN, buff=0.5)
        self.play(FadeIn(zero), FadeIn(one))

        arrow = Arrow(start=qubit_text.get_center()+DOWN*0.5, end=qubit_text.get_center()+DOWN*2, color=YELLOW)
        self.play(GrowArrow(arrow))
        superpos = Text("0 and 1 simultaneously", font_size=30).next_to(arrow, DOWN)
        self.play(Write(superpos))

        self.wait(2)
        self.play(FadeOut(bit_text), FadeOut(qubit_text), FadeOut(zero), FadeOut(one), FadeOut(arrow), FadeOut(superpos))

        gate_title = Text("Quantum Gates", font_size=50).to_edge(UP)
        self.play(Write(gate_title))

        x_gate = Text("X Gate", font_size=30).shift(LEFT*3)
        h_gate = Text("H Gate", font_size=30)
        z_gate = Text("Z Gate", font_size=30).shift(RIGHT*3)
        self.play(FadeIn(x_gate), FadeIn(h_gate), FadeIn(z_gate))

        desc = Text("Manipulate qubits", font_size=25).next_to(h_gate, DOWN*2)
        self.play(Write(desc))

        self.wait(2)
        self.play(FadeOut(gate_title), FadeOut(x_gate), FadeOut(h_gate), FadeOut(z_gate), FadeOut(desc))

        ent_title = Text("Entanglement", font_size=50).to_edge(UP)
        self.play(Write(ent_title))

        a = Text("A", font_size=40).shift(LEFT*3)
        b = Text("B", font_size=40).shift(RIGHT*3)
        self.play(FadeIn(a), FadeIn(b))

        link = DoubleArrow(a.get_right(), b.get_left(), color=BLUE)
        self.play(Create(link))

        ent_text = Text("Entangled qubits act as one", font_size=30).next_to(link, DOWN)
        self.play(Write(ent_text))

        self.wait(2)
        self.play(FadeOut(ent_title), FadeOut(a), FadeOut(b), FadeOut(link), FadeOut(ent_text))

        power = Text("Exponential Speed", font_size=50).to_edge(UP)
        self.play(Write(power))

        exp = Text("2^n states at once", font_size=40)
        self.play(Write(exp))

        self.wait(2)
        self.play(FadeOut(power), FadeOut(exp))

        final = Text("Quantum computing unlocks new possibilities", font_size=35)
        self.play(Write(final))
        self.wait(3)
        self.play(FadeOut(final))