from manim import *

class AutoTeach(Scene):
    def construct(self):
        title = Text("What is gload?").scale(1.5)
        self.play(Write(title))
        self.wait()
        self.play(title.animate.to_edge(UP))

        line1 = Text("gload shows system load in a compact way").next_to(title, DOWN, buff=0.7)
        self.play(FadeIn(line1))
        self.wait()

        arrow = Arrow(start=UP, end=DOWN, color=YELLOW).next_to(line1, DOWN)
        self.play(GrowArrow(arrow))
        self.wait()

        line2 = Text("It averages CPU usage over 1, 5, and 15 minutes").next_to(arrow, DOWN)
        self.play(FadeIn(line2))
        self.wait()

        box = SurroundingRectangle(line2, color=BLUE, buff=0.2)
        self.play(Create(box))
        self.wait()

        line3 = Text("Three numbers: 1min  5min  15min").next_to(box, DOWN, buff=0.7)
        self.play(Write(line3))
        self.wait()

        numbers = Text("0.50  0.30  0.20").next_to(line3, DOWN, buff=0.5)
        self.play(FadeIn(numbers))
        self.wait()

        self.play(
            FadeOut(title),
            FadeOut(line1),
            FadeOut(arrow),
            FadeOut(line2),
            FadeOut(box),
            FadeOut(line3),
            FadeOut(numbers)
        )

        summary = Text("gload = quick glance at CPU load").scale(1.2)
        self.play(Write(summary))
        self.wait(2)
        self.play(FadeOut(summary))