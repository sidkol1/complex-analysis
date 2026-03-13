from manim import *


class AvgRateOfChange(Scene):
    def construct(self):
        x0 = 1

        number_line = NumberLine(
            x_range=[-2, 4, 1],
            length=10,
            include_numbers=True,
            include_tip=True,
        )

        x0_dot = Dot(number_line.n2p(x0), color=YELLOW, z_index=1)
        x0_label = MathTex("x_0", color=YELLOW).next_to(x0_dot, DOWN + LEFT * 0.5)

        self.play(Create(number_line))
        self.play(FadeIn(x0_dot), FadeIn(x0_label))

        t_val = ValueTracker(3)

        t_dot = always_redraw(
            lambda: Dot(number_line.n2p(t_val.get_value()), color=RED, z_index=1)
        )
        t_label = always_redraw(
            lambda: MathTex("x", color=RED).next_to(
                number_line.n2p(t_val.get_value()), DOWN + LEFT * 0.5
            )
        )

        # f(x) = x^2, so (f(t) - f(x0)) / (t - x0) = t + x0
        rate_label = always_redraw(lambda: MathTex(
            r"\frac{\Delta f}{\Delta x} = " + f"{t_val.get_value() + x0:.2f}",
            color=WHITE,
        ).to_corner(UR))

        self.play(FadeIn(t_dot), FadeIn(t_label), FadeIn(rate_label))
        self.wait(0.5)

        self.play(t_val.animate.set_value(1.2), run_time=4, rate_func=smooth)
        self.wait(0.5)
        self.play(t_val.animate.set_value(-1), run_time=3, rate_func=smooth)
        self.wait(0.5)
        self.play(t_val.animate.set_value(1.05), run_time=3, rate_func=smooth)
        self.wait()
