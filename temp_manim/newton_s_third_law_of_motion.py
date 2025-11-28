from manim import *

class AutoTeach(Scene):
    def construct(self):
        title = Text("Newton's Third Law of Motion", font_size=48)
        self.play(Write(title))
        self.wait(1)
        self.play(title.animate.to_edge(UP))

        line1 = Text("For every action,", font_size=36)
        line2 = Text("there is an equal and opposite reaction.", font_size=36)
        statement = VGroup(line1, line2).arrange(DOWN)
        self.play(Write(line1))
        self.play(Write(line2))
        self.wait(2)
        self.play(FadeOut(statement))

        box1 = Rectangle(width=2, height=1, color=BLUE).shift(3*LEFT)
        box2 = Rectangle(width=2, height=1, color=RED).shift(3*RIGHT)
        label1 = Text("Box A", font_size=24).move_to(box1.get_center())
        label2 = Text("Box B", font_size=24).move_to(box2.get_center())
        self.play(Create(box1), Create(box2), Write(label1), Write(label2))

        arrow1 = Arrow(box1.get_right(), box2.get_left(), buff=0.1, color=YELLOW)
        arrow2 = Arrow(box2.get_left(), box1.get_right(), buff=0.1, color=GREEN)
        self.play(GrowArrow(arrow1), GrowArrow(arrow2))
        self.wait(2)

        action_text = Text("Action", font_size=28).next_to(arrow1, UP)
        reaction_text = Text("Reaction", font_size=28).next_to(arrow2, DOWN)
        self.play(Write(action_text), Write(reaction_text))
        self.wait(2)

        self.play(
            FadeOut(box1), FadeOut(box2),
            FadeOut(label1), FadeOut(label2),
            FadeOut(arrow1), FadeOut(arrow2),
            FadeOut(action_text), FadeOut(reaction_text)
        )

        summary = Text("Equal forces, opposite directions", font_size=36)
        self.play(Write(summary))
        self.wait(2)
        self.play(FadeOut(summary), FadeOut(title))