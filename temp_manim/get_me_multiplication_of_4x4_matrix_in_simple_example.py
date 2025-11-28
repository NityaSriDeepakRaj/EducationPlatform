from manim import *

class AutoTeach(Scene):
    def construct(self):
        title = Text("Multiplication of 4×4 Matrices", font_size=36)
        title.to_edge(UP)
        self.play(Write(title))
        self.wait()

        a_vals = [[1, 2, 0, 3],
                  [0, 1, 4, 1],
                  [2, 0, 1, 2],
                  [1, 3, 2, 0]]
        b_vals = [[2, 0, 1, 1],
                  [1, 1, 0, 2],
                  [0, 3, 2, 1],
                  [3, 1, 0, 2]]

        a_mob = Matrix(a_vals, h_buff=1.2).scale(0.7).shift(LEFT * 3)
        b_mob = Matrix(b_vals, h_buff=1.2).scale(0.7).shift(RIGHT * 3)
        times = Text("×", font_size=48).move_to((a_mob.get_right() + b_mob.get_left()) / 2)

        self.play(FadeIn(a_mob), FadeIn(b_mob), Write(times))
        self.wait()

        arrow = Arrow(b_mob.get_bottom() + DOWN * 0.5, b_mob.get_bottom() + DOWN * 1.5, buff=0.2)
        self.play(GrowArrow(arrow))
        self.wait()

        c_vals = [[11, 5, 1, 11],
                  [4, 13, 8, 4],
                  [10, 5, 4, 8],
                  [5, 9, 5, 9]]
        c_mob = Matrix(c_vals, h_buff=1.2).scale(0.7).next_to(arrow, DOWN)

        self.play(FadeIn(c_mob))
        self.wait()

        highlight = SurroundingRectangle(c_mob.get_rows()[0][0], color=YELLOW, buff=0.1)
        self.play(Create(highlight))
        self.wait()

        step = Text("Row 1 • Column 1 = 1·2 + 2·1 + 0·0 + 3·3 = 11",
                    font_size=24).next_to(c_mob, DOWN, buff=0.5)
        self.play(Write(step))
        self.wait()

        self.play(FadeOut(step), Uncreate(highlight))
        self.wait()

        box = SurroundingRectangle(c_mob, color=BLUE, buff=0.2, corner_radius=0.1)
        self.play(Create(box))
        self.wait()

        final = Text("Result is a new 4×4 matrix", font_size=28).next_to(box, DOWN, buff=0.4)
        self.play(Write(final))
        self.wait()

        self.play(FadeOut(title), FadeOut(a_mob), FadeOut(times), FadeOut(b_mob),
                  FadeOut(arrow), FadeOut(c_mob), FadeOut(box), FadeOut(final))
        self.wait()