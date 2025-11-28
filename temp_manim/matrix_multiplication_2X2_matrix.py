from manim import *

class AutoTeach(Scene):
    def construct(self):
        title = Text("Matrix Multiplication 2×2").scale(1.2).to_edge(UP)
        self.play(Write(title))
        self.wait()

        a = [[1, 2], [3, 4]]
        b = [[5, 6], [7, 8]]
        c = [[a[0][0]*b[0][0]+a[0][1]*b[1][0], a[0][0]*b[0][1]+a[0][1]*b[1][1]],
             [a[1][0]*b[0][0]+a[1][1]*b[1][0], a[1][0]*b[0][1]+a[1][1]*b[1][1]]]

        mata = VGroup(
            Text("1 2").set_color(BLUE),
            Text("3 4").set_color(BLUE)
        ).arrange(DOWN, buff=0.2).shift(LEFT*4)

        matb = VGroup(
            Text("5 6").set_color(GREEN),
            Text("7 8").set_color(GREEN)
        ).arrange(DOWN, buff=0.2).shift(LEFT*1)

        times = Text("×").next_to(mata, RIGHT, buff=0.5)
        equals = Text("=").next_to(matb, RIGHT, buff=0.5)

        matc = VGroup(
            Text(str(c[0][0])+" "+str(c[0][1])).set_color(YELLOW),
            Text(str(c[1][0])+" "+str(c[1][1])).set_color(YELLOW)
        ).arrange(DOWN, buff=0.2).shift(RIGHT*2.5)

        self.play(Write(mata), Write(times), Write(matb), Write(equals), Write(matc))
        self.wait()

        arrow1 = Arrow(mata[0].get_center()+DOWN*0.5, matb[0].get_center()+UP*0.5, buff=0.1, color=WHITE)
        arrow2 = Arrow(mata[0].get_center()+DOWN*0.5, matb[1].get_center()+UP*0.5, buff=0.1, color=WHITE)
        self.play(GrowArrow(arrow1), GrowArrow(arrow2))
        self.wait()

        step1 = Text("Top-left: 1×5 + 2×7 = 19").scale(0.6).to_edge(DOWN)
        self.play(Write(step1))
        self.wait()
        self.play(FadeOut(step1))

        step2 = Text("Top-right: 1×6 + 2×8 = 22").scale(0.6).to_edge(DOWN)
        self.play(Write(step2))
        self.wait()
        self.play(FadeOut(step2))

        step3 = Text("Bottom-left: 3×5 + 4×7 = 43").scale(0.6).to_edge(DOWN)
        self.play(Write(step3))
        self.wait()
        self.play(FadeOut(step3))

        step4 = Text("Bottom-right: 3×6 + 4×8 = 50").scale(0.6).to_edge(DOWN)
        self.play(Write(step4))
        self.wait()
        self.play(FadeOut(step4))

        final = Text("Result is").scale(0.8).next_to(matc, DOWN, buff=0.5)
        self.play(Write(final))
        self.wait()

        self.play(FadeOut(title), FadeOut(mata), FadeOut(times), FadeOut(matb), FadeOut(equals), FadeOut(matc),
                  FadeOut(arrow1), FadeOut(arrow2), FadeOut(final))
        self.wait()