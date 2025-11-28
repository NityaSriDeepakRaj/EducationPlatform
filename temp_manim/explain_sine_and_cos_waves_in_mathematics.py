from manim import *

class AutoTeach(Scene):
    def construct(self):
        title = Text("Sine & Cosine Waves", font_size=48).to_edge(UP)
        self.play(Write(title))
        self.wait(0.5)

        unit_circle = Circle(radius=2, color=WHITE).shift(LEFT*3)
        self.play(Create(unit_circle))

        dot = Dot(unit_circle.point_at_angle(0), color=YELLOW)
        self.play(FadeIn(dot))

        h_line = Line(dot.get_center(), np.array([dot.get_x(), -2, 0]), color=BLUE)
        v_line = Line(dot.get_center(), np.array([-5, dot.get_y(), 0]), color=RED)
        self.play(Create(h_line), Create(v_line))

        cos_label = Text("cos", font_size=24, color=BLUE).next_to(h_line, DOWN)
        sin_label = Text("sin", font_size=24, color=RED).next_to(v_line, LEFT)
        self.play(Write(cos_label), Write(sin_label))

        axes = Axes(x_range=[0, 4*np.pi, np.pi/2], y_range=[-1.5, 1.5, 1],
                    x_length=6, y_length=3, axis_config={"color": GRAY}).shift(RIGHT*3)
        self.play(Create(axes))

        sine_curve = axes.plot(lambda x: np.sin(x), color=RED)
        cos_curve = axes.plot(lambda x: np.cos(x), color=BLUE)
        self.play(Create(sine_curve), Create(cos_curve))

        sine_tag = Text("sine wave", font_size=24, color=RED).next_to(axes, DOWN)
        cos_tag = Text("cosine wave", font_size=24, color=BLUE).next_to(sine_tag, DOWN)
        self.play(Write(sine_tag), Write(cos_tag))

        arrow1 = Arrow(dot.get_center(), axes.coords_to_point(0, 0), buff=0.1, color=YELLOW)
        self.play(GrowArrow(arrow1))
        self.wait(0.5)

        tracker = ValueTracker(0)
        dot.add_updater(lambda m: m.move_to(unit_circle.point_at_angle(tracker.get_value())))
        h_line.add_updater(lambda l: l.put_start_and_end_on(
            dot.get_center(), np.array([dot.get_x(), -2, 0])))
        v_line.add_updater(lambda l: l.put_start_and_end_on(
            dot.get_center(), np.array([-5, dot.get_y(), 0])))
        arrow1.add_updater(lambda a: a.put_start_and_end_on(
            dot.get_center(), axes.coords_to_point(tracker.get_value(), np.sin(tracker.get_value()))))

        self.play(tracker.animate.set_value(4*np.pi), run_time=6, rate_func=linear)

        summary = Text("Sine = vertical motion, Cosine = horizontal motion", font_size=30).to_edge(DOWN)
        self.play(Write(summary))
        self.wait(2)
        self.play(*[FadeOut(m) for m in self.mobjects])