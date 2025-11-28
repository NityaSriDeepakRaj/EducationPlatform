from manim import *

class AutoTeach(Scene):
    def construct(self):
        title = Text("Projectile Motion", font_size=48)
        self.play(Write(title))
        self.wait()
        self.play(title.animate.to_edge(UP))

        ax = Axes(x_range=[0, 10, 1], y_range=[0, 5, 1], x_length=10, y_length=5)
        self.play(Create(ax))
        self.wait()

        g = -9.8
        v0 = 8
        ang = 50 * DEGREES
        vx = v0 * np.cos(ang)
        vy = v0 * np.sin(ang)

        def pos(t):
            x = vx * t
            y = vy * t + 0.5 * g * t * t
            return ax.coords_to_point(x, max(y, 0))

        trail = VMobject()
        trail.set_points_as_corners([pos(0), pos(0)])
        trail.set_stroke(BLUE, 3)
        self.add(trail)

        ball = Dot(point=pos(0), color=RED, radius=0.1)
        self.add(ball)

        dt = 0.05
        t = 0
        while pos(t)[1] > -10:
            t += dt
            new = pos(t)
            trail.add_line_to(new)
            ball.move_to(new)
            self.wait(dt)

        vtxt = Text("Velocity", font_size=24).next_to(ball, UR)
        varrow = Arrow(ball.get_center(), ball.get_center() + 0.5 * np.array([vx, vy, 0]), buff=0, color=YELLOW)
        self.play(Create(varrow), Write(vtxt))

        self.wait()
        self.play(FadeOut(vtxt), FadeOut(varrow))

        ctxt = Text("Gravity", font_size=24).next_to(ball, DOWN)
        carrow = Arrow(ball.get_center(), ball.get_center() + 0.3 * DOWN, buff=0, color=GREEN)
        self.play(Create(carrow), Write(ctxt))

        self.wait()
        self.play(FadeOut(ctxt), FadeOut(carrow))

        end = Text("Parabolic Path", font_size=36).to_edge(DOWN)
        self.play(Write(end))
        self.wait(2)