from manim import *

class AutoTeach(Scene):
    def construct(self):
        title = Text("4×4 Matrix Multiplication", font_size=48)
        self.play(Write(title))
        self.wait()
        self.play(title.animate.to_edge(UP))

        a_vals = [[1, 2, 3, 4],
                  [5, 6, 7, 8],
                  [9, 10, 11, 12],
                  [13, 14, 15, 16]]
        b_vals = [[16, 15, 14, 13],
                  [12, 11, 10, 9],
                  [8, 7, 6, 5],
                  [4, 3, 2, 1]]

        a_mob = Matrix(a_vals).scale(0.6).shift(LEFT * 3)
        b_mob = Matrix(b_vals).scale(0.6).shift(RIGHT * 3)
        times = Text("×", font_size=72).move_to((a_mob.get_right() + b_mob.get_left()) / 2)

        self.play(FadeIn(a_mob), FadeIn(b_mob), Write(times))
        self.wait()

        arrow = Arrow(b_mob.get_right() + RIGHT * 0.5, b_mob.get_right() + RIGHT * 1.5, buff=0.2)
        self.play(GrowArrow(arrow))

        c_vals = [[60, 50, 40, 30],
                  [172, 146, 120, 94],
                  [284, 242, 200, 158],
                  [396, 338, 280, 222]]
        c_mob = Matrix(c_vals).scale(0.6).next_to(arrow, RIGHT, buff=0.5)
        equals = Text("=", font_size=72).next_to(c_mob, LEFT, buff=0.3)
        self.play(FadeIn(c_mob), Write(equals))
        self.wait()

        highlight = SurroundingRectangle(c_mob.get_rows()[0][0], color=YELLOW, buff=0.1)
        self.play(Create(highlight))

        row0 = VGroup(*[a_mob.get_entries()[i] for i in range(4)])
        col0 = VGroup(*[b_mob.get_entries()[i * 4] for i in range(4)])
        row0_copy = row0.copy().set_color(YELLOW)
        col0_copy = col0.copy().set_color(YELLOW)

        self.play(row0_copy.animate.shift(DOWN * 2),
                  col0_copy.animate.shift(UP * 2))
        self.wait()

        calc = Text("1×16 + 2×12 + 3×8 + 4×4 = 60", font_size=28).to_edge(DOWN)
        self.play(Write(calc))
        self.wait()

        self.play(FadeOut(row0_copy), FadeOut(col0_copy), FadeOut(calc), Uncreate(highlight))

        self.play(
            a_mob.animate.scale(0.8).to_edge(LEFT),
            b_mob.animate.scale(0.8).next_to(a_mob, RIGHT, buff=0.8),
            times.animate.scale(0.8).next_to(a_mob, RIGHT, buff=0.3),
            equals.animate.scale(0.8).next_to(b_mob, RIGHT, buff=0.8),
            c_mob.animate.scale(0.8).next_to(equals, RIGHT, buff=0.8)
        )
        self.wait()

        final = Text("Final 4×4 Result", font_size=36).next_to(c_mob, DOWN, buff=0.6)
        self.play(Write(final))
        self.wait(2)