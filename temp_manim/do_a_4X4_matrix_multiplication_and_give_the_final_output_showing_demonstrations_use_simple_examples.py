from manim import *

class AutoTeach(Scene):
    def construct(self):
        title = Text("4×4 Matrix Multiplication").scale(1.2)
        self.play(Write(title))
        self.wait(1)
        self.play(title.animate.to_edge(UP))

        a_vals = [[1, 2, 0, 1],
                  [0, 3, 1, 2],
                  [2, 0, 1, 1],
                  [1, 1, 2, 0]]
        b_vals = [[2, 0, 1, 1],
                  [1, 1, 0, 2],
                  [0, 2, 1, 0],
                  [1, 0, 2, 1]]
        c_vals = [[4, 2, 3, 6],
                  [5, 5, 5, 8],
                  [5, 2, 5, 4],
                  [3, 3, 3, 3]]

        mA = self.matrix_mob(a_vals).scale(0.6).shift(3*LEFT)
        mB = self.matrix_mob(b_vals).scale(0.6).shift(3*RIGHT)
        times = Text("×").scale(1.5).move_to(ORIGIN)
        equals = Text("=").scale(1.5).move_to(ORIGIN)

        self.play(FadeIn(mA), FadeIn(mB), Write(times))
        self.wait(1)
        self.play(Transform(times, equals))
        mC = self.matrix_mob(c_vals).scale(0.6).shift(3*RIGHT)
        self.play(Transform(mB, mC))
        self.wait(2)

        highlight = SurroundingRectangle(mC, color=YELLOW, buff=0.2)
        self.play(Create(highlight))
        self.wait(1)

        step_txt = Text("Step-by-step for element (0,0)").scale(0.8).to_edge(DOWN)
        self.play(Write(step_txt))
        self.wait(2)

        self.play(FadeOut(title), FadeOut(mA), FadeOut(times), FadeOut(mB), FadeOut(highlight), FadeOut(step_txt))

        row = Text("Row 0 of A: [1 2 0 1]").scale(0.7).shift(2*UP)
        col = Text("Col 0 of B: [2 1 0 1]").scale(0.7).next_to(row, DOWN)
        self.play(Write(row))
        self.play(Write(col))
        self.wait(1)

        calc = Text("1·2 + 2·1 + 0·0 + 1·1 = 2+2+0+1 = 5").scale(0.7).next_to(col, DOWN)
        self.play(Write(calc))
        self.wait(2)

        self.play(FadeOut(row), FadeOut(col), FadeOut(calc))

        final = Text("Final Result:").scale(0.9).to_edge(UP)
        self.play(Write(final))
        result = self.matrix_mob(c_vals).scale(0.8)
        self.play(FadeIn(result))
        self.wait(3)

    def matrix_mob(self, values):
        rows = len(values)
        cols = len(values[0])
        group = VGroup()
        for i in range(rows):
            for j in range(cols):
                t = Text(str(values[i][j])).scale(0.7)
                t.shift((j - cols/2 + 0.5)*RIGHT + (rows/2 - i - 0.5)*DOWN)
                group.add(t)
        bracket_left = Text("[").scale(2.5).shift((cols/2)*LEFT)
        bracket_right = Text("]").scale(2.5).shift((cols/2)*RIGHT)
        group.add(bracket_left, bracket_right)
        return group