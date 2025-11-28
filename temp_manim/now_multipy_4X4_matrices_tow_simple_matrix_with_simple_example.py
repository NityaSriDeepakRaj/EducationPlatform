from manim import *

class AutoTeach(Scene):
    def construct(self):
        title = Text("Multiply 4×4 Matrices").scale(1.2)
        self.play(Write(title))
        self.wait()
        self.play(title.animate.to_edge(UP))

        a = Matrix([[1, 0, 2, -1], [3, 1, 0, 2], [0, -1, 1, 0], [2, 0, 1, 1]])
        b = Matrix([[0, 1, 0, 1], [1, 0, -1, 2], [2, 1, 0, 1], [0, 1, 2, 0]])
        a.to_edge(LEFT).shift(UP)
        b.next_to(a, RIGHT, buff=1.5)

        times = Text("×").scale(2).next_to(a, RIGHT, buff=0.5)
        equals = Text("=").scale(2).next_to(b, RIGHT, buff=0.5)

        self.play(FadeIn(a), FadeIn(b), FadeIn(times))
        self.wait()
        self.play(FadeIn(equals))

        result = Matrix([[4, 2, -2, 3], [1, 5, 4, 5], [1, 1, 2, -1], [3, 3, 2, 3]])
        result.next_to(equals, RIGHT, buff=0.5)

        self.play(FadeIn(result))
        self.wait()

        arrow1 = Arrow(a.get_rows()[0].get_right() + 0.2*RIGHT,
                       result.get_rows()[0].get_left() + 0.2*LEFT,
                       color=YELLOW)
        arrow2 = Arrow(b.get_columns()[0].get_top() + 0.2*UP,
                       result.get_rows()[0].get_left() + 0.2*LEFT,
                       color=YELLOW)

        self.play(Create(arrow1), Create(arrow2))
        self.wait(2)
        self.play(FadeOut(arrow1), FadeOut(arrow2))

        step = Text("Dot row 1 of A with column 1 of B").scale(0.8).to_edge(DOWN)
        self.play(Write(step))
        self.wait(3)
        self.play(FadeOut(step))

        self.play(FadeOut(title), FadeOut(a), FadeOut(b), FadeOut(times), FadeOut(equals), FadeOut(result))
        self.wait()