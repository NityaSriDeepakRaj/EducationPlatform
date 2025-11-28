from manim import *

class AutoTeach(Scene):
    def construct(self):
        title = Text("Show Matrix", font_size=48)
        self.play(Write(title))
        self.wait()
        self.play(title.animate.to_edge(UP))

        mat = Matrix([[1, 2], [3, 4]])
        mat.scale(1.5)
        self.play(FadeIn(mat))
        self.wait()

        arrow = Arrow(start=LEFT, end=RIGHT, color=YELLOW)
        arrow.next_to(mat, RIGHT, buff=1)
        self.play(GrowArrow(arrow))
        self.wait()

        label = Text("2×2 matrix", font_size=36)
        label.next_to(arrow, RIGHT, buff=1)
        self.play(Write(label))
        self.wait()

        self.play(
            FadeOut(title),
            FadeOut(mat),
            FadeOut(arrow),
            FadeOut(label)
        )
        self.wait()