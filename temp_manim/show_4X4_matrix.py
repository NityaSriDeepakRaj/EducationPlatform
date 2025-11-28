from manim import *

class AutoTeach(Scene):
    def construct(self):
        title = Text("4×4 Matrix").scale(1.5).to_edge(UP)
        self.play(Write(title))
        self.wait()

        mat = VGroup(
            *[Text(str(i)).scale(0.9) for i in range(1, 17)]
        )
        mat.arrange_in_grid(4, 4, buff=0.6).shift(DOWN*0.5)

        left_brace = Text("[", font_size=200).next_to(mat, LEFT, buff=0.1)
        right_brace = Text("]", font_size=200).next_to(mat, RIGHT, buff=0.1)

        self.play(FadeIn(left_brace), FadeIn(right_brace))
        for entry in mat:
            self.play(Write(entry), run_time=0.1)

        self.wait()

        arrow1 = Arrow(start=mat.get_corner(UL)+UP*0.5, end=mat.get_corner(UL)+UP*0.5+RIGHT*1.5, buff=0.2)
        label1 = Text("Rows").scale(0.7).next_to(arrow1, UP)
        self.play(GrowArrow(arrow1), Write(label1))
        self.wait()

        arrow2 = Arrow(start=mat.get_corner(UL)+LEFT*0.5, end=mat.get_corner(UL)+LEFT*0.5+DOWN*1.5, buff=0.2)
        label2 = Text("Columns").scale(0.7).next_to(arrow2, LEFT)
        self.play(GrowArrow(arrow2), Write(label2))
        self.wait()

        highlight = SurroundingRectangle(mat[0:4], color=YELLOW)
        self.play(Create(highlight))
        self.wait()

        highlight2 = SurroundingRectangle(VGroup(*[mat[i] for i in [0,4,8,12]]), color=BLUE)
        self.play(ReplacementTransform(highlight, highlight2))
        self.wait()

        self.play(FadeOut(highlight2), FadeOut(arrow1), FadeOut(label1), FadeOut(arrow2), FadeOut(label2))

        outro = Text("Order: 4×4").scale(1.2).next_to(mat, DOWN*1.5)
        self.play(Write(outro))
        self.wait()
        self.play(FadeOut(outro), FadeOut(mat), FadeOut(left_brace), FadeOut(right_brace), FadeOut(title))