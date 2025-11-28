from manim import *

class AutoTeach(Scene):
    def construct(self):
        title = Text("Projectile Motion", font_size=48)
        subtitle = Text("A Visual Journey", font_size=28)
        title.to_edge(UP)
        subtitle.next_to(title, DOWN, buff=0.4)
        self.play(Write(title), Write(subtitle))
        self.wait(1)

        ground = Line(LEFT * 6, RIGHT * 6, color=GREEN)
        ground.shift(DOWN * 2.5)
        self.play(Create(ground))
        self.wait(0.5)

        launcher = Dot(LEFT * 4 + DOWN * 2.5, color=ORANGE)
        launcher_label = Text("Launch", font_size=20).next_to(launcher, DOWN, buff=0.2)
        self.play(FadeIn(launcher), Write(launcher_label))
        self.wait(0.5)

        traj = ParametricFunction(
            lambda t: np.array([t - 4, -0.2 * t * t + 1.5 * t - 2.5, 0]),
            t_range=[0, 7.5, 0.05],
            color=BLUE
        )
        self.play(Create(traj), run_time=3)
        self.wait(0.5)

        ball = Dot(color=RED)
        self.add(ball)
        self.play(MoveAlongPath(ball, traj), run_time=3)
        self.wait(0.5)

        vel_vec = Arrow(start=launcher.get_center(),
                        end=launcher.get_center() + np.array([1.2, 1.2, 0]),
                        buff=0,
                        color=YELLOW)
        vel_label = Text("v", font_size=24).next_to(vel_vec, UP, buff=0.1)
        self.play(GrowArrow(vel_vec), Write(vel_label))
        self.wait(0.5)

        grav_vec = Arrow(start=ball.get_center(),
                         end=ball.get_center() + np.array([0, -1, 0]),
                         buff=0,
                         color=PURPLE)
        grav_label = Text("g", font_size=24).next_to(grav_vec, RIGHT, buff=0.1)
        self.play(GrowArrow(grav_vec), Write(grav_label))
        self.wait(0.5)

        self.play(
            Transform(subtitle, Text("Gravity pulls down", font_size=28).next_to(title, DOWN, buff=0.4))
        )
        self.wait(1)

        x_axis = Line(LEFT * 5, RIGHT * 5, color=WHITE).shift(DOWN * 3.8)
        y_axis = Line(DOWN * 3.8, UP * 2, color=WHITE).shift(LEFT * 5)
        x_label = Text("Range", font_size=20).next_to(x_axis, RIGHT, buff=0.2)
        y_label = Text("Height", font_size=20).next_to(y_axis, UP, buff=0.2)
        self.play(Create(x_axis), Create(y_axis), Write(x_label), Write(y_label))
        self.wait(1)

        self.play(FadeOut(Group(title, subtitle, launcher_label, vel_vec, vel_label, grav_vec, grav_label, x_axis, y_axis, x_label, y_label)))
        self.wait(0.5)

        summary = Text("Path is a Parabola", font_size=36)
        summary.to_edge(UP)
        self.play(Write(summary))
        self.wait(2)
        self.play(FadeOut(summary), FadeOut(traj), FadeOut(ground), FadeOut(launcher), FadeOut(ball))