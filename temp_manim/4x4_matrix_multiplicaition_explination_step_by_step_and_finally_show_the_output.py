from manim import *

class AutoTeach(Scene):
    def construct(self):
        title = Text("4x4 Matrix Multiplication", font_size=48)
        self.play(Write(title))
        self.play(title.animate.to_edge(UP))
        self.wait()

        a_vals = [[1, 2, 3, 4],
                  [5, 6, 7, 8],
                  [9, 10, 11, 12],
                  [13, 14, 15, 16]]
        b_vals = [[16, 15, 14, 13],
                  [12, 11, 10, 9],
                  [8, 7, 6, 5],
                  [4, 3, 2, 1]]
        c_vals = [[0 for _ in range(4)] for _ in range(4)]

        a_mob = Matrix(a_vals).scale(0.6).shift(3*LEFT)
        b_mob = Matrix(b_vals).scale(0.6).shift(3*RIGHT)
        times = Text("x", font_size=36).move_to(midpoint(a_mob.get_right(), b_mob.get_left()))
        self.play(FadeIn(a_mob), FadeIn(times), FadeIn(b_mob))
        self.wait()

        eq = Text("=", font_size=36).next_to(b_mob, RIGHT, buff=0.6)
        c_mob = Matrix(c_vals).scale(0.6).next_to(eq, RIGHT, buff=0.6)
        self.play(FadeIn(eq), FadeIn(c_mob))
        self.wait()

        highlight = Rectangle(color=YELLOW, width=1.2, height=0.4).set_stroke(width=3)

        for row in range(4):
            for col in range(4):
                self.play(highlight.animate.move_to(a_mob.get_entries()[row*4].get_center()), run_time=0.3)
                self.play(highlight.animate.move_to(b_mob.get_entries()[col].get_center()), run_time=0.3)

                sum_text = Text("0", font_size=24).move_to(c_mob.get_entries()[row*4 + col].get_center())
                self.play(Transform(c_mob.get_entries()[row*4 + col], sum_text))

                total = 0
                for k in range(4):
                    a_entry = a_vals[row][k]
                    b_entry = b_vals[k][col]
                    prod = a_entry * b_entry
                    total += prod

                    arrow1 = Arrow(start=a_mob.get_entries()[row*4 + k].get_center(),
                                   end=sum_text.get_center(), buff=0.2, stroke_width=2, color=BLUE)
                    arrow2 = Arrow(start=b_mob.get_entries()[k*4 + col].get_center(),
                                   end=sum_text.get_center(), buff=0.2, stroke_width=2, color=GREEN)
                    self.play(GrowArrow(arrow1), GrowArrow(arrow2), run_time=0.3)

                    new_sum_text = Text(str(total), font_size=24).move_to(sum_text.get_center())
                    self.play(Transform(sum_text, new_sum_text), run_time=0.3)
                    self.play(FadeOut(arrow1), FadeOut(arrow2), run_time=0.2)

                final_val = Text(str(total), font_size=24).move_to(c_mob.get_entries()[row*4 + col].get_center())
                self.play(Transform(c_mob.get_entries()[row*4 + col], final_val))

        self.wait(2)
        final_note = Text("Output 4x4 Matrix", font_size=36).next_to(c_mob, DOWN, buff=0.6)
        self.play(Write(final_note))
        self.wait(3)
        self.play(FadeOut(title), FadeOut(a_mob), FadeOut(times), FadeOut(b_mob), FadeOut(eq), FadeOut(c_mob), FadeOut(final_note), FadeOut(highlight))