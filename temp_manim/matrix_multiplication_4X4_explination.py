from manim import *

class AutoTeach(Scene):
    def construct(self):
        title = Text("Matrix Multiplication 4x4", font_size=48)
        self.play(Write(title))
        self.wait()
        self.play(title.animate.to_edge(UP))

        a_labels = VGroup(*[Text(f"A row {i+1}", font_size=24) for i in range(4)]).arrange(DOWN, buff=0.6).shift(4*LEFT)
        b_labels = VGroup(*[Text(f"B col {j+1}", font_size=24) for j in range(4)]).arrange(RIGHT, buff=0.6).shift(4*RIGHT)

        self.play(FadeIn(a_labels, b_labels))
        self.wait()

        a_mat = Matrix([[1,2,3,4],[5,6,7,8],[9,10,11,12],[13,14,15,16]], element_to_mobject=Text)
        a_mat.scale(0.6).shift(2.5*LEFT)
        b_mat = Matrix([[16,15,14,13],[12,11,10,9],[8,7,6,5],[4,3,2,1]], element_to_mobject=Text)
        b_mat.scale(0.6).shift(2.5*RIGHT)

        self.play(Create(a_mat), Create(b_mat))
        self.wait()

        eq = Text("=", font_size=36).next_to(b_mat, RIGHT, buff=0.4)
        self.play(Write(eq))

        c_mat = Matrix([[80,70,60,50],[240,214,188,162],[400,358,316,274],[560,502,444,386]], element_to_mobject=Text)
        c_mat.scale(0.6).next_to(eq, RIGHT, buff=0.4)

        self.play(Create(c_mat))
        self.wait()

        row_rect = SurroundingRectangle(a_mat.get_rows()[0], color=YELLOW, buff=0.1)
        col_rect = SurroundingRectangle(b_mat.get_columns()[0], color=YELLOW, buff=0.1)
        cell_rect = SurroundingRectangle(c_mat.get_entries()[0], color=RED, buff=0.1)

        self.play(Create(row_rect), Create(col_rect), Create(cell_rect))
        self.wait()

        arrow1 = Arrow(row_rect.get_right(), col_rect.get_left(), buff=0.1, color=YELLOW)
        self.play(GrowArrow(arrow1))
        self.wait()

        calc = Text("1*16 + 2*12 + 3*8 + 4*4 = 80", font_size=24).to_edge(DOWN)
        self.play(Write(calc))
        self.wait()

        for i in range(4):
            for j in range(4):
                new_row_rect = SurroundingRectangle(a_mat.get_rows()[i], color=YELLOW, buff=0.1)
                new_col_rect = SurroundingRectangle(b_mat.get_columns()[j], color=YELLOW, buff=0.1)
                new_cell_rect = SurroundingRectangle(c_mat.get_entries()[i*4+j], color=RED, buff=0.1)

                self.play(
                    Transform(row_rect, new_row_rect),
                    Transform(col_rect, new_col_rect),
                    Transform(cell_rect, new_cell_rect)
                )

                a_vals = a_mat.get_rows()[i]
                b_vals = b_mat.get_columns()[j]
                dot = sum(int(a_vals[k].text) * int(b_vals[k].text) for k in range(4))
                new_calc = Text(f"{'+'.join([f'{a_vals[k].text}*{b_vals[k].text}' for k in range(4)])} = {dot}", font_size=24).to_edge(DOWN)
                self.play(Transform(calc, new_calc))
                self.wait()

        self.play(
            FadeOut(row_rect), FadeOut(col_rect), FadeOut(cell_rect),
            FadeOut(arrow1), FadeOut(calc)
        )

        final_text = Text("Each entry is dot product of row and column", font_size=28)
        final_text.next_to(c_mat, DOWN, buff=0.6)
        self.play(Write(final_text))
        self.wait()

        self.play(FadeOut(title), FadeOut(a_labels), FadeOut(b_labels),
                  FadeOut(a_mat), FadeOut(b_mat), FadeOut(eq), FadeOut(c_mat), FadeOut(final_text))

        self.wait()