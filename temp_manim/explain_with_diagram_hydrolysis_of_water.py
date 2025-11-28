from manim import *

class AutoTeach(Scene):
    def construct(self):
        title = Text("Hydrolysis of Water", font_size=48)
        self.play(Write(title))
        self.play(title.animate.to_edge(UP))

        h2o = Text("H₂O", font_size=36)
        plus1 = Text("+", font_size=36)
        h2o_copy = h2o.copy()
        self.play(FadeIn(h2o))
        self.wait(0.5)
        self.play(h2o.animate.shift(LEFT*3))
        self.play(FadeIn(plus1.next_to(h2o, RIGHT)))
        self.play(FadeIn(h2o_copy.next_to(plus1, RIGHT)))
        self.wait(0.5)

        arrow1 = Arrow(start=LEFT, end=RIGHT, color=YELLOW)
        self.play(GrowArrow(arrow1.move_to(h2o_copy.get_right() + RIGHT*1.5)))
        self.wait(0.5)

        h = Text("H", font_size=36)
        oh = Text("OH", font_size=36)
        h.next_to(arrow1, RIGHT).shift(UP*0.5)
        oh.next_to(arrow1, RIGHT).shift(DOWN*0.5)
        self.play(FadeIn(h), FadeIn(oh))
        self.wait(0.5)

        plus2 = Text("+", font_size=36)
        self.play(FadeIn(plus2.next_to(oh, RIGHT)))
        self.wait(0.5)

        arrow2 = Arrow(start=LEFT, end=RIGHT, color=YELLOW)
        self.play(GrowArrow(arrow2.next_to(plus2, RIGHT)))
        self.wait(0.5)

        h3o = Text("H₃O⁺", font_size=36, color=BLUE)
        oh_copy = oh.copy().set_color(RED)
        h3o.next_to(arrow2, RIGHT).shift(UP*0.5)
        oh_copy.next_to(arrow2, RIGHT).shift(DOWN*0.5)
        self.play(FadeIn(h3o), FadeIn(oh_copy))
        self.wait(0.5)

        self.play(
            FadeOut(h2o), FadeOut(plus1), FadeOut(h2o_copy),
            FadeOut(arrow1), FadeOut(h), FadeOut(oh),
            FadeOut(plus2), FadeOut(arrow2)
        )

        final_eq = VGroup(h3o, Text("and", font_size=28).next_to(h3o, DOWN), oh_copy.next_to(h3o, DOWN*2))
        self.play(
            h3o.animate.move_to(ORIGIN + UP*0.5),
            oh_copy.animate.move_to(ORIGIN + DOWN*0.5)
        )
        self.wait(0.5)

        self.play(
            FadeOut(title),
            FadeOut(final_eq),
            FadeOut(h3o),
            FadeOut(oh_copy)
        )
        self.wait()