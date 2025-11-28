from manim import *

class AutoTeach(Scene):
    def construct(self):
        title = Text("Newton's Third Law of Motion", font_size=48)
        self.play(Write(title))
        self.wait(1)
        self.play(title.animate.to_edge(UP))

        law = Text("For every action, there is an equal and opposite reaction.", font_size=32)
        law.next_to(title, DOWN, buff=0.5)
        self.play(Write(law))
        self.wait(2)

        box = Square(side_length=1.5, color=BLUE).shift(LEFT*3)
        box_label = Text("Box", font_size=24).next_to(box, DOWN)
        ground = Line(LEFT*5, RIGHT*5, color=GRAY).shift(DOWN*2)
        ground_label = Text("Ground", font_size=24).next_to(ground, DOWN)

        self.play(Create(box), Write(box_label), Create(ground), Write(ground_label))
        self.wait(1)

        action_arrow = Arrow(box.get_right(), box.get_right()+RIGHT*2, buff=0, color=RED)
        action_label = Text("Action", font_size=24).next_to(action_arrow, UP)
        self.play(GrowArrow(action_arrow), Write(action_label))
        self.wait(1)

        reaction_arrow = Arrow(box.get_left(), box.get_left()+LEFT*2, buff=0, color=GREEN)
        reaction_label = Text("Reaction", font_size=24).next_to(reaction_arrow, UP)
        self.play(GrowArrow(reaction_arrow), Write(reaction_label))
        self.wait(1)

        force_pair = Text("Action and Reaction Forces", font_size=32).to_edge(DOWN)
        self.play(Write(force_pair))
        self.wait(2)

        self.play(
            FadeOut(action_arrow),
            FadeOut(action_label),
            FadeOut(reaction_arrow),
            FadeOut(reaction_label),
            FadeOut(force_pair),
            FadeOut(box),
            FadeOut(box_label),
            FadeOut(ground),
            FadeOut(ground_label),
            FadeOut(law)
        )

        example = Text("Example: When you jump, you push the Earth down, and the Earth pushes you up!", font_size=28)
        self.play(Write(example))
        self.wait(2)
        self.play(FadeOut(example))

        summary = Text("Remember: Forces always come in pairs!", font_size=36)
        self.play(Write(summary))
        self.wait(2)
        self.play(FadeOut(summary), FadeOut(title))