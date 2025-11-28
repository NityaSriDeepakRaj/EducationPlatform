from manim import *

class AutoTeach(Scene):
    def construct(self):
        title = Text("Hydrolysis of Water", font_size=48)
        self.play(Write(title))
        self.wait()
        self.play(title.animate.to_edge(UP))

        reactants = Text("2 H₂O", font_size=36).shift(LEFT * 3)
        arrow = Arrow(LEFT, RIGHT, buff=0.5)
        products = Text("2 H₂ + O₂", font_size=36).shift(RIGHT * 3)

        self.play(FadeIn(reactants))
        self.play(GrowArrow(arrow))
        self.play(FadeIn(products))

        self.wait()

        step1 = Text("Step 1: Electric current passes", font_size=28).shift(DOWN * 1.5)
        self.play(Write(step1))
        self.wait()

        step2 = Text("Step 2: Water splits", font_size=28).next_to(step1, DOWN)
        self.play(Write(step2))
        self.wait()

        step3 = Text("Step 3: Gases form", font_size=28).next_to(step2, DOWN)
        self.play(Write(step3))
        self.wait()

        self.play(
            FadeOut(step1),
            FadeOut(step2),
            FadeOut(step3),
            FadeOut(reactants),
            FadeOut(arrow),
            FadeOut(products)
        )

        summary = Text("Water → Hydrogen + Oxygen", font_size=36)
        self.play(Write(summary))
        self.wait()

        self.play(FadeOut(summary), FadeOut(title))