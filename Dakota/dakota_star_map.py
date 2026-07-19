"""The Grammar That Trains the Machine - a Dakota star map, 1890.

Built the native Math-To-Manim way: implemented directly from the
imagined verbose prompt in Dakota/imagined_prompt.md. Grammar content
follows Riggs, "Dakota Grammar, Texts, and Ethnography" (1893).

Render:
    manim -qh --fps 30 Dakota/dakota_star_map.py DakotaStarMap
"""

from __future__ import annotations

import math

import numpy as np
from manim import (
    BLACK, WHITE,
    DOWN, LEFT, ORIGIN, PI, RIGHT, TAU, UP,
    Arrow, Circle, Create, Dot, FadeIn, FadeOut, Flash, GrowArrow,
    LaggedStart, Line, MathTex, MoveAlongPath, Scene, Text, Transform,
    VGroup, VMobject, Write, config, rate_functions,
)

config.background_color = "#0b0e1a"

ICE = "#7dd3fc"      # morphology
GOLD = "#fbbf24"     # syntax
EMBER = "#f87171"    # phonology
MIST = "#94a3b8"
FAINT = "#334155"

RULES = [
    ("-pi plural", ICE), ("wa- absolutive", ICE), ("ki- dative", ICE),
    ("uŋk- we", ICE), ("ma- me", ICE), ("ni- you", ICE),
    ("-kte future", ICE), ("waŋ article", GOLD), ("SOV order", GOLD),
    ("postpositions", GOLD), ("čha connective", GOLD), ("relative last", GOLD),
    ("topic first", GOLD), ("reduplication", EMBER), ("ablaut a/e", EMBER),
    ("nasal vowels", EMBER), ("aspiration", EMBER), ("stress 2nd", EMBER),
]


def spiral_layout(n: int, scale: float = 3.1) -> list[np.ndarray]:
    pts = []
    for i in range(n):
        t = i / n
        ang = 2.6 * TAU * t
        r = 0.55 + scale * t
        pts.append(np.array([r * math.cos(ang), 0.82 * r * math.sin(ang) - 0.2, 0]))
    return pts


class DakotaStarMap(Scene):
    def construct(self) -> None:
        self.opening()
        stars, labels = self.act1_constellation()
        self.act2_closeups(stars)
        self.act3_gradient(stars)
        self.coda(stars)

    # ------------------------------------------------------------------
    def opening(self) -> None:
        star = Dot(ORIGIN, radius=0.06, color=WHITE)
        word = Text("wičháȟpi", font_size=34, color=ICE).next_to(star, DOWN, buff=0.3)
        gloss = Text("star", font_size=20, color=MIST).next_to(word, DOWN, buff=0.12)
        self.play(FadeIn(star), Flash(star, color=ICE, line_length=0.25))
        self.play(FadeIn(word, shift=UP * 0.2), FadeIn(gloss))

        title = Text("The Grammar That Trains the Machine",
                     weight="BOLD", font_size=40)
        title.set_color_by_gradient(ICE, GOLD)
        title.to_edge(UP, buff=1.1)
        sub = Text("a Dakota star map, 1890", font_size=24,
                   color=MIST).next_to(title, DOWN, buff=0.3)
        self.play(Write(title), run_time=1.6)
        self.play(FadeIn(sub))
        self.wait(1.2)
        self.play(
            FadeOut(title, shift=UP * 0.5), FadeOut(sub, shift=UP * 0.4),
            FadeOut(word), FadeOut(gloss), FadeOut(star),
            run_time=0.9,
        )

    # ------------------------------------------------------------------
    def act1_constellation(self) -> tuple[VGroup, VGroup]:
        pts = spiral_layout(len(RULES))
        stars = VGroup(*[
            Dot(p, radius=0.075, color=c).set_glow_factor(1.5)
            if hasattr(Dot, "set_glow_factor")
            else Dot(p, radius=0.075, color=c)
            for p, (_, c) in zip(pts, RULES)
        ])
        labels = VGroup(*[
            Text(name, font_size=16, color=c).next_to(s, UP, buff=0.12)
            for s, (name, c) in zip(stars, RULES)
        ])

        # rivers of light: connect stars that share a morphological theme
        edges = VGroup()
        for i in range(len(RULES)):
            for j in (i + 1, i + 2):
                if j < len(RULES):
                    edges.add(Line(pts[i], pts[j], color=FAINT,
                                   stroke_width=1.2, stroke_opacity=0.5))

        self.play(LaggedStart(*[
            FadeIn(s, scale=0.2) for s in stars
        ], lag_ratio=0.08), run_time=3.2)
        self.play(LaggedStart(*[
            FadeIn(l) for l in labels
        ], lag_ratio=0.05), run_time=2.2)
        self.play(LaggedStart(*[
            Create(e) for e in edges
        ], lag_ratio=0.02), run_time=2.4)

        caption = Text("18 rules, one language: every star constrains its neighbors",
                       font_size=22, color=MIST).to_edge(DOWN, buff=0.4)
        self.play(FadeIn(caption))
        self.wait(1.6)
        self.play(FadeOut(caption), FadeOut(edges), FadeOut(labels), run_time=0.8)
        self.stars_home = VGroup(*stars)
        return stars, labels

    # ------------------------------------------------------------------
    def act2_closeups(self, stars: VGroup) -> None:
        dimmed = stars.copy().set_opacity(0.18)
        self.play(Transform(stars, dimmed), run_time=0.7)

        # -- closeup 1: morphology, the -pi plural --------------------------
        head = Text("morphology: the plural  -pi", font_size=26, color=ICE)
        head.to_edge(UP, buff=0.5)
        self.play(FadeIn(head, shift=DOWN * 0.2))

        woman = Text("wíŋyaŋ", font_size=44, color=WHITE)
        gloss1 = Text("woman", font_size=20, color=MIST).next_to(woman, DOWN, buff=0.15)
        pi = Text("-pi", font_size=40, color=GOLD).move_to(RIGHT * 5 + UP * 1.5)
        self.play(FadeIn(woman), FadeIn(gloss1))
        self.play(pi.animate.next_to(woman, RIGHT, buff=0.05), run_time=1.4,
                  rate_func=rate_functions.ease_in_out_sine)
        women = Text("wíŋyaŋpi", font_size=44, color=WHITE)
        gloss2 = Text("women", font_size=20, color=MIST).next_to(women, DOWN, buff=0.15)
        self.play(Transform(woman, women), Transform(gloss1, gloss2), FadeOut(pi))

        s1 = Text("Wíŋyaŋ máni.", font_size=28, color=MIST)
        g1 = Text("the woman walks", font_size=18, color=FAINT)
        s2 = Text("Wíŋyaŋ mánipi.", font_size=28, color=WHITE)
        g2 = Text("the women walk", font_size=18, color=MIST)
        VGroup(VGroup(s1, g1).arrange(DOWN, buff=0.1),
               ).arrange(DOWN).shift(DOWN * 1.9)
        g1.next_to(s1, DOWN, buff=0.1)
        s2.move_to(s1)
        g2.next_to(s2, DOWN, buff=0.1)
        self.play(FadeIn(s1), FadeIn(g1))
        self.wait(0.6)
        self.play(Transform(s1, s2), Transform(g1, g2))
        rule = MathTex(r"\mathrm{plural}(x) = x + \text{``-pi''}",
                       font_size=30, color=ICE).to_edge(DOWN, buff=0.45)
        self.play(Write(rule))
        self.wait(1.4)
        self.play(FadeOut(VGroup(head, woman, gloss1, s1, g1, rule)), run_time=0.7)

        # -- closeup 2: phonology, reduplication ---------------------------
        head = Text("phonology: reduplication", font_size=26, color=EMBER)
        head.to_edge(UP, buff=0.5)
        self.play(FadeIn(head, shift=DOWN * 0.2))

        sapa = Text("sápa", font_size=46, color=WHITE)
        glossa = Text("black", font_size=20, color=MIST).next_to(sapa, DOWN, buff=0.15)
        self.play(FadeIn(sapa), FadeIn(glossa))
        self.wait(0.5)
        sapsapa = Text("sapsápa", font_size=46, color=WHITE)
        glossb = Text("black, here and there", font_size=20,
                      color=MIST).next_to(sapsapa, DOWN, buff=0.15)
        self.play(Transform(sapa, sapsapa), Transform(glossa, glossb), run_time=1.2)

        drops = VGroup(*[
            Dot(np.array([x, -1.7, 0]), radius=r, color=BLACK,
                stroke_color=EMBER, stroke_width=1.5)
            for x, r in [(-2.4, 0.12), (-0.6, 0.09), (1.1, 0.14), (2.7, 0.1)]
        ])
        self.play(LaggedStart(*[FadeIn(d, scale=0.3) for d in drops],
                              lag_ratio=0.2))
        rule = MathTex(r"\mathrm{red}(x) = \sigma_1(x) + x",
                       font_size=30, color=EMBER).to_edge(DOWN, buff=0.45)
        self.play(Write(rule))
        self.wait(1.3)
        self.play(FadeOut(VGroup(head, sapa, glossa, drops, rule)), run_time=0.7)

        # -- closeup 3: syntax, SOV ---------------------------------------
        head = Text("syntax: the verb comes last", font_size=26, color=GOLD)
        head.to_edge(UP, buff=0.5)
        self.play(FadeIn(head, shift=DOWN * 0.2))

        w1 = Text("Wičhášta", font_size=36, color=WHITE)
        w2 = Text("šúŋka", font_size=36, color=WHITE)
        w3 = Text("waŋyáŋke.", font_size=36, color=WHITE)
        sent = VGroup(w1, w2, w3).arrange(RIGHT, buff=0.55).shift(UP * 0.4)
        gl = VGroup(
            Text("man", font_size=18, color=MIST),
            Text("dog", font_size=18, color=MIST),
            Text("sees", font_size=18, color=MIST),
        )
        for g, w in zip(gl, sent):
            g.next_to(w, DOWN, buff=0.12)
        self.play(LaggedStart(*[
            FadeIn(VGroup(w, g), shift=UP * 0.2) for w, g in zip(sent, gl)
        ], lag_ratio=0.35), run_time=2.0)

        a1 = Arrow(w1.get_bottom() + DOWN * 0.5, w3.get_bottom() + DOWN * 0.5,
                   color=GOLD, stroke_width=3, buff=0.1,
                   path_arc=-1.1)
        a2 = Arrow(w2.get_bottom() + DOWN * 0.35, w3.get_bottom() + DOWN * 0.35,
                   color=ICE, stroke_width=3, buff=0.1, path_arc=-0.9)
        t1 = Text("agent", font_size=16, color=GOLD).next_to(a1, DOWN, buff=0.1)
        t2 = Text("patient", font_size=16, color=ICE).next_to(a2, UP, buff=0.05)
        self.play(GrowArrow(a1), FadeIn(t1))
        self.play(GrowArrow(a2), FadeIn(t2))
        cap = Text("the sentence flows into its verb like rivers into a lake",
                   font_size=20, color=MIST).to_edge(DOWN, buff=0.45)
        self.play(FadeIn(cap))
        self.wait(1.6)
        self.play(FadeOut(VGroup(head, sent, gl, a1, a2, t1, t2, cap)),
                  run_time=0.8)

    # ------------------------------------------------------------------
    def act3_gradient(self, stars: VGroup) -> None:
        bright = stars.copy().set_opacity(1.0)
        self.play(Transform(stars, bright), run_time=0.9)

        obj = MathTex(
            r"J(\theta)=\mathbb{E}_{x\sim\mathcal{D}_{1890}}"
            r"\Big[\sum_{r}w_r\,\log p_\theta(r\ \text{satisfied}\mid x)\Big]",
            font_size=30,
        ).to_edge(UP, buff=0.45)
        step = MathTex(
            r"\theta_{t+1}=\theta_t+\eta\,\nabla_\theta J(\theta_t)",
            font_size=28, color=GOLD,
        ).next_to(obj, DOWN, buff=0.25)
        self.play(Write(obj), run_time=2.0)
        self.play(Write(step), run_time=1.4)

        # the model particle and its learning trajectory
        path = VMobject()
        path.set_points_smoothly([
            np.array([-6.2, -2.6, 0]), np.array([-3.4, 0.6, 0]),
            np.array([-0.8, -1.8, 0]), np.array([1.8, 0.9, 0]),
            np.array([3.6, -1.2, 0]), np.array([1.2, -0.4, 0]),
        ])
        particle = Dot(path.get_start(), radius=0.09, color=WHITE)
        trail = VMobject(stroke_color=GOLD, stroke_width=2.5,
                         stroke_opacity=0.85)
        trail.set_points_smoothly([path.get_start(), path.get_start()])

        pulls = VGroup(*[
            Line(particle.get_center(), s.get_center(), color=FAINT,
                 stroke_width=1, stroke_opacity=0.5)
            for s in stars[:9]
        ])

        def update_pulls(group: VGroup) -> None:
            for line, s in zip(group, stars[:9]):
                line.put_start_and_end_on(particle.get_center(),
                                          s.get_center())

        pulls.add_updater(update_pulls)
        traced = []

        def update_trail(m: VMobject) -> None:
            traced.append(particle.get_center().copy())
            if len(traced) > 2:
                m.set_points_smoothly(traced)

        trail.add_updater(update_trail)

        self.play(FadeIn(particle), FadeIn(pulls))
        self.add(trail)
        self.play(MoveAlongPath(particle, path), run_time=6.5,
                  rate_func=rate_functions.ease_in_out_sine)
        pulls.clear_updaters()
        trail.clear_updaters()

        cap = Text("every rule is a gradient; the grammar pulls the model toward the language",
                   font_size=21, color=MIST).to_edge(DOWN, buff=0.4)
        self.play(FadeIn(cap))
        self.wait(1.6)
        self.play(FadeOut(VGroup(obj, step, particle, pulls, trail, cap)),
                  run_time=0.9)

    # ------------------------------------------------------------------
    def coda(self, stars: VGroup) -> None:
        self.play(LaggedStart(*[
            Flash(s, color=s.get_color(), line_length=0.15, flash_radius=0.25)
            for s in stars
        ], lag_ratio=0.04), run_time=2.2)
        dim = stars.copy().set_opacity(0.25)
        self.play(Transform(stars, dim), run_time=1.4)

        end1 = Text("Dakhóta iápi - the Dakota language", font_size=28, color=WHITE)
        end2 = Text("Documented 1890. Still spoken. Still teaching.",
                    font_size=22, color=MIST).next_to(end1, DOWN, buff=0.3)
        card = VGroup(end1, end2).move_to(ORIGIN)
        self.play(FadeIn(card, shift=UP * 0.2), run_time=1.2)
        self.wait(3.0)
        self.play(FadeOut(card), FadeOut(stars), run_time=1.4)
