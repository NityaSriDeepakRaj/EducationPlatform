from manim import *

class AutoTeach(Scene):
    def construct(self):
        title = Text("4×4 Matrix Multiplication").scale(1.2)
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

        a_mob = Matrix(a_vals).set_color(BLUE).shift(LEFT * 3)
        b_mob = Matrix(b_vals).set_color(GREEN).shift(RIGHT * 3)
        times = Text("×").scale(2).move_between(a_mob, b_mob)

        self.play(Create(a_mob), Create(b_mob), Write(times))
        self.wait()

        eq = Text("=").scale(2).next_to(b_mob, RIGHT * 2)
        self.play(Write(eq))

        c_vals = [[80, 70, 60, 50],
                  [240, 214, 188, 162],
                  [400, 358, 316, 274],
                  [560, 502, 444, 386]]
        c_mob = Matrix(c_vals).set_color(RED).next_to(eq, RIGHT * 2)
        self.play(Create(c_mob))
        self.wait()

        arrow1 = Arrow(a_mob.get_right(), c_mob.get_left(), color=BLUE)
        arrow2 = Arrow(b_mob.get_left(), c_mob.get_right(), color=GREEN)
        self.play(GrowArrow(arrow1), GrowArrow(arrow2))
        self.wait()

        highlight = Rectangle(width=2.5, height=0.8, color=YELLOW).move_to(a_mob.get_rows()[0])
        self.play(Create(highlight))
        self.wait()

        for i in range(4):
            new_highlight = Rectangle(width=2.5, height=0.8, color=YELLOW).move_to(a_mob.get_rows()[i])
            self.play(Transform(highlight, new_highlight))
            self.wait(0.5)

        self.play(FadeOut(highlight))
        self.wait()

        step_text = Text("Each row × each column").scale(0.8).next_to(c_mob, DOWN * 2)
        self.play(Write(step_text))
        self.wait()

        self.play(FadeOut(step_text), FadeOut(arrow1), FadeOut(arrow2))
        self.wait()

        final = Text("Result is 4×4 Matrix").scale(1.0).next_to(c_mob, DOWN * 2)
        self.play(Write(final))
        self.wait()

        self.play(FadeOut(title), FadeOut(a_mob), FadeOut(b_mob), FadeOut(times), FadeOut(eq), FadeOut(c_mob), FadeOut(final))
        self.wait()