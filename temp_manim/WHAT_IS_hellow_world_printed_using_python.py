from manim import *

class AutoTeach(Scene):
    def construct(self):
        title = Text("WHAT IS 'hello world' printed using Python?")
        title.scale(0.9)
        title.to_edge(UP)
        self.play(Write(title))
        self.wait(1)

        code = Text("print('hello world')", font="monospace", font_size=36)
        self.play(FadeIn(code))
        self.wait(1)

        arrow1 = Arrow(start=code.get_bottom(), end=code.get_bottom() + DOWN * 1.2, buff=0.2)
        self.play(GrowArrow(arrow1))
        self.wait(0.5)

        output = Text("hello world", font="monospace", font_size=36)
        output.next_to(arrow1, DOWN)
        self.play(FadeIn(output))
        self.wait(1)

        arrow2 = Arrow(start=output.get_right(), end=output.get_right() + RIGHT * 2, buff=0.2)
        self.play(GrowArrow(arrow2))
        self.wait(0.5)

        explanation = Text("Python sends the text to the console")
        explanation.scale(0.8)
        explanation.next_to(arrow2, RIGHT)
        self.play(Write(explanation))
        self.wait(1)

        self.play(
            FadeOut(title),
            FadeOut(code),
            FadeOut(arrow1),
            FadeOut(output),
            FadeOut(arrow2),
            FadeOut(explanation)
        )
        self.wait(0.5)