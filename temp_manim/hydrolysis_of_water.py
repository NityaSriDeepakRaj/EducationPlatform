from manim import *

class AutoTeach(Scene):
    def construct(self):
        title = Text("Hydrolysis of Water", font_size=48)
        self.play(Write(title))
        self.wait(1)
        self.play(title.animate.to_edge(UP))

        h2o = Text("H₂O", font_size=36)
        plus1 = Text("+", font_size=36)
        h2o2 = Text("H₂O", font_size=36)
        arrow1 = Text("→", font_size=36)
        h3o = Text("H₃O⁺", font_size=36)
        plus2 = Text("+", font_size=36)
        oh = Text("OH⁻", font_size=36)

        eq = VGroup(h2o, plus1, h2o2, arrow1, h3o, plus2, oh).arrange(RIGHT)
        eq.next_to(title, DOWN, buff=1)

        self.play(Write(h2o))
        self.play(Write(plus1))
        self.play(Write(h2o2))
        self.play(Write(arrow1))
        self.play(Write(h3o))
        self.play(Write(plus2))
        self.play(Write(oh))
        self.wait(2)

        label1 = Text("Water molecule 1", font_size=24).next_to(h2o, DOWN)
        label2 = Text("Water molecule 2", font_size=24).next_to(h2o2, DOWN)
        label3 = Text("Hydronium ion", font_size=24).next_to(h3o, DOWN)
        label4 = Text("Hydroxide ion", font_size=24).next_to(oh, DOWN)

        self.play(Write(label1), Write(label2))
        self.wait(1)
        self.play(Transform(label1, label3), Transform(label2, label4))
        self.wait(2)

        self.play(FadeOut(label1), FadeOut(label2), FadeOut(eq), FadeOut(title))

        summary = Text("Water reacts with itself to form H₃O⁺ and OH⁻", font_size=32)
        self.play(Write(summary))
        self.wait(2)
        self.play(FadeOut(summary))