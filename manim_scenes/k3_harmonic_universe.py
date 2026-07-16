"""The Harmonic Universe - demonstration scene for the Kimi K3 pipeline.

Three acts, one idea: every complex motion in mathematics and physics is
circles hiding inside circles. Fourier epicycles build a square wave from
pure rotation, standing waves quantize a vibrating string, and superposed
harmonics collapse into a localized wave packet - the seed of quantum
mechanics.

Render:
    manim -qh manim_scenes/k3_harmonic_universe.py K3HarmonicUniverse
"""

from __future__ import annotations

import numpy as np
from manim import (
    BLACK, WHITE, BLUE_B, BLUE_D, GOLD, TEAL_A, TEAL_B, PURPLE_A, RED_B,
    DOWN, LEFT, ORIGIN, PI, RIGHT, TAU, UP,
    Axes, Circle, Create, DashedLine, Dot, FadeIn, FadeOut, Line,
    MathTex, Scene, Text, Transform, ValueTracker, VGroup, VMobject,
    Write, always_redraw, rate_functions, config,
)

config.background_color = "#0b0e1a"

ACCENT = "#7dd3fc"     # ice blue
ACCENT2 = "#fbbf24"    # amber
ACCENT3 = "#c084fc"    # violet
DIM = "#334155"


class K3HarmonicUniverse(Scene):
    def construct(self) -> None:
        self.act0_title()
        self.act1_epicycles()
        self.act2_standing_waves()
        self.act3_wave_packet()
        self.act4_outro()

    # ------------------------------------------------------------------
    def act0_title(self) -> None:
        title = Text("THE HARMONIC UNIVERSE", weight="BOLD", font_size=54)
        title.set_color_by_gradient(ACCENT, ACCENT3)
        sub = Text(
            "a Kimi K3 agent-pipeline demonstration",
            font_size=24, color=TEAL_A,
        ).next_to(title, DOWN, buff=0.4)
        rule = Line(LEFT * 3, RIGHT * 3, color=GOLD, stroke_width=2)
        rule.next_to(sub, DOWN, buff=0.35)

        self.play(Write(title), run_time=1.6)
        self.play(FadeIn(sub, shift=UP * 0.3), Create(rule), run_time=1.0)
        self.wait(1.2)
        self.play(FadeOut(VGroup(title, sub, rule)), run_time=0.8)

    # ------------------------------------------------------------------
    def act1_epicycles(self) -> None:
        """Fourier epicycles: rotation becomes a square wave."""
        heading = Text("I.  Circles hiding inside circles", font_size=30, color=ACCENT)
        heading.to_edge(UP, buff=0.4)
        self.play(FadeIn(heading, shift=DOWN * 0.2))

        eq = MathTex(
            r"f(t)=\frac{4}{\pi}\sum_{n=1,3,5,\dots}\frac{\sin(nt)}{n}",
            font_size=34,
        ).next_to(heading, DOWN, buff=0.3).set_color(WHITE)
        self.play(Write(eq), run_time=1.4)

        center = LEFT * 4 + DOWN * 0.8
        t = ValueTracker(0)
        harmonics = [1, 3, 5, 7, 9]
        radii = [4 / (PI * n) for n in harmonics]

        def chain() -> VGroup:
            group = VGroup()
            pos = np.array(center, dtype=float)
            angle = t.get_value()
            colors = [ACCENT, TEAL_B, ACCENT3, ACCENT2, RED_B]
            for r, n, col in zip(radii, harmonics, colors):
                circ = Circle(radius=r, color=col, stroke_width=1.6,
                              stroke_opacity=0.65).move_to(pos)
                tip = pos + r * np.array([np.cos(n * angle), np.sin(n * angle), 0])
                group.add(circ, Line(pos, tip, color=col, stroke_width=2))
                pos = tip
            group.add(Dot(pos, radius=0.05, color=WHITE))
            return group

        def tip_point() -> np.ndarray:
            pos = np.array(center, dtype=float)
            angle = t.get_value()
            for r, n in zip(radii, harmonics):
                pos = pos + r * np.array([np.cos(n * angle), np.sin(n * angle), 0])
            return pos

        def wave() -> VMobject:
            angle = t.get_value()
            xs = np.linspace(0, 5.4, 220)
            pts = []
            for x in xs:
                past = angle - x * 1.15
                y = sum(4 / (PI * n) * np.sin(n * past) for n in harmonics)
                pts.append(np.array([0.6 + x, -0.8 + y, 0]))
            curve = VMobject(color=ACCENT2, stroke_width=3)
            curve.set_points_smoothly(pts)
            return curve

        def connector() -> DashedLine:
            tip = tip_point()
            return DashedLine(
                tip, np.array([0.6, tip[1], 0]),
                color=DIM, stroke_width=1.5, dash_length=0.08,
            )

        rig = always_redraw(chain)
        trace = always_redraw(wave)
        link = always_redraw(connector)

        self.play(FadeIn(rig), run_time=0.8)
        self.add(link, trace)
        self.play(t.animate.set_value(3.5 * TAU), run_time=9.0,
                  rate_func=rate_functions.linear)
        self.wait(0.4)

        caption = Text(
            "pure rotation, summed, becomes a square wave",
            font_size=22, color=TEAL_A,
        ).to_edge(DOWN, buff=0.4)
        self.play(FadeIn(caption))
        self.play(t.animate.set_value(4.5 * TAU), run_time=2.5,
                  rate_func=rate_functions.linear)
        self.play(FadeOut(VGroup(rig, trace, link, caption, eq, heading)),
                  run_time=0.9)

    # ------------------------------------------------------------------
    def act2_standing_waves(self) -> None:
        """A vibrating string quantizes into harmonics."""
        heading = Text("II.  The string chooses its notes", font_size=30, color=ACCENT)
        heading.to_edge(UP, buff=0.4)
        self.play(FadeIn(heading, shift=DOWN * 0.2))

        eq = MathTex(
            r"y_n(x,t)=\sin\!\Big(\frac{n\pi x}{L}\Big)\cos(n\omega t)",
            font_size=34,
        ).next_to(heading, DOWN, buff=0.3)
        self.play(Write(eq), run_time=1.2)

        t = ValueTracker(0)
        mode = ValueTracker(1)
        L = 9.0

        def string() -> VMobject:
            n_float = mode.get_value()
            n_lo, n_hi = int(np.floor(n_float)), int(np.ceil(n_float))
            blend = n_float - n_lo
            xs = np.linspace(0, L, 200)
            pts = []
            for x in xs:
                y_lo = np.sin(n_lo * PI * x / L) * np.cos(n_lo * 2.4 * t.get_value())
                y_hi = np.sin(n_hi * PI * x / L) * np.cos(n_hi * 2.4 * t.get_value())
                y = (1 - blend) * y_lo + blend * y_hi
                pts.append(np.array([x - L / 2, -0.7 + 1.1 * y, 0]))
            curve = VMobject(stroke_width=4)
            curve.set_points_smoothly(pts)
            curve.set_color_by_gradient(ACCENT, ACCENT3, ACCENT2)
            return curve

        anchors = VGroup(
            Dot(np.array([-L / 2, -0.7, 0]), color=GOLD),
            Dot(np.array([L / 2, -0.7, 0]), color=GOLD),
        )
        wire = always_redraw(string)

        label = always_redraw(lambda: MathTex(
            f"n={max(1, round(mode.get_value()))}", font_size=36, color=ACCENT2,
        ).to_edge(DOWN, buff=0.5))

        self.play(FadeIn(anchors), FadeIn(wire), FadeIn(label))
        for target in (1, 2, 3, 5):
            self.play(
                mode.animate.set_value(target),
                t.animate.increment_value(4.5),
                run_time=2.4, rate_func=rate_functions.smooth,
            )
        caption = Text(
            "boundary conditions quantize the continuum",
            font_size=22, color=TEAL_A,
        ).next_to(label, UP, buff=0.35)
        self.play(FadeIn(caption))
        self.play(t.animate.increment_value(3.5), run_time=2.0,
                  rate_func=rate_functions.linear)
        self.play(FadeOut(VGroup(wire, anchors, label, caption, eq, heading)),
                  run_time=0.9)

    # ------------------------------------------------------------------
    def act3_wave_packet(self) -> None:
        """Superposed harmonics localize: the quantum wave packet."""
        heading = Text("III.  Many notes make a particle", font_size=30, color=ACCENT)
        heading.to_edge(UP, buff=0.4)
        self.play(FadeIn(heading, shift=DOWN * 0.2))

        eq = MathTex(
            r"\psi(x,t)=\sum_k A_k\, e^{i(kx-\omega_k t)}",
            font_size=34,
        ).next_to(heading, DOWN, buff=0.3)
        self.play(Write(eq), run_time=1.2)

        t = ValueTracker(0)
        spread = ValueTracker(0.35)   # k-space width: grows -> localizes in x

        ks = np.linspace(2.0, 9.0, 24)
        k0 = 5.5

        def packet() -> VMobject:
            sig = spread.get_value()
            weights = np.exp(-((ks - k0) ** 2) / (2 * sig ** 2))
            weights /= weights.sum()
            xs = np.linspace(-6.4, 6.4, 260)
            time = t.get_value()
            pts = []
            for x in xs:
                re = sum(w * np.cos(k * x - (k ** 2) * 0.12 * time)
                         for w, k in zip(weights, ks))
                pts.append(np.array([x, -0.9 + 2.2 * re, 0]))
            curve = VMobject(stroke_width=3.5)
            curve.set_points_smoothly(pts)
            curve.set_color_by_gradient(ACCENT3, ACCENT, TEAL_B)
            return curve

        def envelope() -> VMobject:
            sig = spread.get_value()
            weights = np.exp(-((ks - k0) ** 2) / (2 * sig ** 2))
            weights /= weights.sum()
            xs = np.linspace(-6.4, 6.4, 260)
            time = t.get_value()
            pts = []
            for x in xs:
                re = sum(w * np.cos(k * x - (k ** 2) * 0.12 * time)
                         for w, k in zip(weights, ks))
                im = sum(w * np.sin(k * x - (k ** 2) * 0.12 * time)
                         for w, k in zip(weights, ks))
                amp = np.sqrt(re ** 2 + im ** 2)
                pts.append(np.array([x, -0.9 + 2.2 * amp, 0]))
            curve = VMobject(stroke_width=2, stroke_opacity=0.75)
            curve.set_points_smoothly(pts)
            curve.set_color(ACCENT2)
            return curve

        wavefn = always_redraw(packet)
        env = always_redraw(envelope)

        self.play(FadeIn(wavefn), run_time=0.8)
        caption1 = Text("one frequency: everywhere at once",
                        font_size=22, color=TEAL_A).to_edge(DOWN, buff=0.4)
        self.play(FadeIn(caption1))
        self.play(t.animate.increment_value(6), run_time=3.0,
                  rate_func=rate_functions.linear)

        caption2 = Text("add harmonics: the wave becomes a place",
                        font_size=22, color=TEAL_A).to_edge(DOWN, buff=0.4)
        self.add(env)
        self.play(
            spread.animate.set_value(1.9),
            Transform(caption1, caption2),
            t.animate.increment_value(4),
            run_time=4.0, rate_func=rate_functions.smooth,
        )
        self.play(t.animate.increment_value(5), run_time=2.8,
                  rate_func=rate_functions.linear)
        self.play(FadeOut(VGroup(wavefn, env, caption1, eq, heading)),
                  run_time=0.9)

    # ------------------------------------------------------------------
    def act4_outro(self) -> None:
        line1 = Text("one idea, three physics", font_size=30, color=WHITE)
        line2 = Text(
            "concept -> math -> visuals -> narrative -> code -> critique",
            font_size=22, color=TEAL_A,
        ).next_to(line1, DOWN, buff=0.45)
        line3 = Text(
            "imagined end-to-end by six Kimi K3 agents",
            font_size=22, color=ACCENT2,
        ).next_to(line2, DOWN, buff=0.3)
        group = VGroup(line1, line2, line3).move_to(ORIGIN)
        self.play(FadeIn(line1, shift=UP * 0.2), run_time=0.9)
        self.play(FadeIn(line2), run_time=0.8)
        self.play(FadeIn(line3), run_time=0.8)
        self.wait(2.0)
        self.play(FadeOut(group), run_time=1.0)
