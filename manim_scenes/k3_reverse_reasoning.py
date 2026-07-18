"""REVERSE REASONING - a Kimi K3 protocol film.

A ~30 second, five-act 3D short. Not a tutorial - a transmission from inside
the model. The film visualizes the reverse reasoning protocol: begin at the
goal, decompose backward into sufficient subgoals until every leaf is an
axiom, then run the forward verification pass as pulses of light travelling
up the proof tree while the K3 machinery (Kimi Delta Attention, Attention
Residuals, Stable LatentMoE) checks every link.

The mathematics on screen is real: Nicomachus' theorem

    sum_{k=1}^{n} k^3 = T_n^2,   T_n = n(n+1)/2

proved exactly the way the protocol works - backward from the goal G:
G <= g1 & tau & beta, g1 <= l & g2 & g3, g2 <= a1, g3 <= a2.

Render (five scenes, concatenated into one film):

    manim -r 1920,1080 --fps 30 manim_scenes/k3_reverse_reasoning.py RRGenesis
    manim -r 1920,1080 --fps 30 manim_scenes/k3_reverse_reasoning.py RRGoal
    manim -r 1920,1080 --fps 30 manim_scenes/k3_reverse_reasoning.py RRBackwardBloom
    manim -r 1920,1080 --fps 30 manim_scenes/k3_reverse_reasoning.py RRVerification
    manim -r 1920,1080 --fps 30 manim_scenes/k3_reverse_reasoning.py RRSigil
"""

from __future__ import annotations

import numpy as np
from manim import (
    DEGREES, DOWN, LEFT, ORIGIN, OUT, PI, RIGHT, UP,
    Circle, Dot, FadeIn, FadeOut, GrowFromPoint, Line, MathTex,
    Text, ThreeDScene, VGroup, VMobject, Write,
    linear, rush_from, rush_into, smooth, there_and_back,
    config,
)

# ----------------------------------------------------------------------
# palette - plasma on void (deliberately unlike the repo's navy/amber style)
# ----------------------------------------------------------------------
VOID = "#000004"
PLASMA = "#ff2fb3"      # magenta
VOLT = "#00e5ff"        # cyan
ULTRA = "#8a5cff"       # ultraviolet
GOLD = "#ffd166"        # the goal
AXIOM = "#39ff88"       # verified leaves
GHOST = "#3a3550"       # dormant experts / dim lattice
PAPER = "#f4f1ff"       # near-white

CAM_PHI = 64 * DEGREES
CAM_THETA = -90 * DEGREES

config.background_color = VOID


# ----------------------------------------------------------------------
# helpers
# ----------------------------------------------------------------------
def face_camera(mob, phi=CAM_PHI):
    """Orient a flat mobject so it looks straight at the 3D camera."""
    mob.rotate(phi, axis=RIGHT)
    return mob


def glow_dot(point, color, radius=0.07, halo=3.0):
    """A flat dot wrapped in a translucent halo - neon glow, Cairo-fast."""
    core = Dot(point=point, radius=radius, color=color)
    glow = Dot(point=point, radius=radius * halo, color=color)
    glow.set_opacity(0.18)
    return VGroup(glow, core)


def glow_edge(start, end, color, width=2.5):
    """A line with a soft outer sheath - neon fibre projected in 3D space."""
    core = Line(start, end, stroke_color=color, stroke_width=width)
    sheath = Line(start, end, stroke_color=color, stroke_width=width * 3.5)
    sheath.set_opacity(0.16)
    return VGroup(sheath, core)


def hud_line(text, size=22, color=VOLT, **kwargs):
    return Text(text, font="Consolas", font_size=size, color=color, **kwargs)


def starfield(n, spread=9.0, seed=7, color=GHOST):
    """Cheap 3D dust for depth (flat dots at 3D coordinates)."""
    rng = np.random.default_rng(seed)
    pts = rng.uniform(-spread, spread, size=(n, 3))
    pts[:, 2] = rng.uniform(-spread * 0.7, spread * 0.7, size=n)
    dots = VGroup(*(Dot(point=p, radius=0.028, color=color) for p in pts))
    for d in dots:
        d.set_opacity(float(rng.uniform(0.25, 0.8)))
    return dots


def fibonacci_sphere(n, radius=3.0):
    """Evenly spread n points on a sphere - the dormant expert lattice."""
    pts = []
    golden = PI * (3.0 - np.sqrt(5.0))
    for i in range(n):
        y = 1.0 - (i / float(n - 1)) * 2.0
        r = np.sqrt(max(0.0, 1.0 - y * y))
        theta = golden * i
        pts.append(radius * np.array([np.cos(theta) * r, y, np.sin(theta) * r]))
    return pts


def build_reasoning_tree():
    """The proof DAG for Nicomachus' theorem, laid out in 3D.

    Returns (nodes, edges, meta) where edges are (parent, child) pairs and
    reasoning flows child -> parent (verification) while search draws
    parent -> child (backward decomposition).
    """
    spec = {
        "G":   (r"\mathcal{G}:\ \sum_{k=1}^{n} k^3 = T_n^2", (0.0, 0.0, 3.1), GOLD, 44),
        "g1":  (r"T_n^2 - T_{n-1}^2 = n^3", (-3.4, 0.0, 1.55), VOLT, 34),
        "tau": (r"\sum_{k=1}^{n}\!\left(T_k^2 - T_{k-1}^2\right) = T_n^2", (1.6, 0.4, 1.55), ULTRA, 30),
        "beta":(r"1^3 = 1^2", (4.6, 0.0, 1.55), AXIOM, 34),
        "ell": (r"x^2 - y^2 = (x-y)(x+y)", (-4.9, 0.2, -0.05), ULTRA, 30),
        "g2":  (r"T_n - T_{n-1} = n", (-2.1, -0.3, -0.05), VOLT, 30),
        "g3":  (r"T_n + T_{n-1} = n^2", (0.2, 0.2, -0.05), VOLT, 30),
        "a1":  (r"T_n = T_{n-1} + n", (-2.9, 0.0, -1.75), AXIOM, 30),
        "a2":  (r"2T_n = n(n+1)", (0.8, 0.0, -1.75), AXIOM, 30),
    }
    edge_keys = [
        ("G", "g1"), ("G", "tau"), ("G", "beta"),
        ("g1", "ell"), ("g1", "g2"), ("g1", "g3"),
        ("g2", "a1"), ("g3", "a2"),
    ]
    nodes, pos = {}, {}
    for key, (tex, p, col, size) in spec.items():
        m = MathTex(tex, font_size=size, color=col)
        m.move_to(p)
        face_camera(m)
        halo = MathTex(tex, font_size=size, color=col)
        halo.move_to(p).rotate(CAM_PHI, axis=RIGHT)
        halo.set_stroke(width=6, opacity=0.25)
        halo.set_fill(opacity=0.0)
        nodes[key] = VGroup(halo, m)
        pos[key] = np.array(p, dtype=float)
    edges = {}
    for parent, child in edge_keys:
        col = PAPER if parent == "G" else GHOST
        edges[(parent, child)] = glow_edge(pos[parent], pos[child], col)
    return nodes, edges, pos


def dim_tree(nodes, edges, opacity=0.35):
    for key, node in nodes.items():
        if key != "G":
            node.set_opacity(opacity)
    for e in edges.values():
        e.set_opacity(opacity)


# ----------------------------------------------------------------------
# ACT I - GENESIS: 896 sleep, 16 wake
# ----------------------------------------------------------------------
class RRGenesis(ThreeDScene):
    def construct(self):
        self.set_camera_orientation(phi=CAM_PHI, theta=CAM_THETA)

        dust = starfield(90, seed=11)
        self.add(dust)

        # dormant expert lattice
        pts = fibonacci_sphere(220, radius=3.1)
        lattice = VGroup(*(
            Dot(point=p, radius=0.062, color=GHOST) for p in pts
        ))
        lattice.set_opacity(0.9)
        self.play(FadeIn(lattice, run_time=1.2))
        self.play(lattice.animate.rotate(PI / 5, axis=OUT, about_point=ORIGIN),
                  run_time=6.0, rate_func=linear)

        # 16 experts ignite
        awake_idx = np.linspace(0, 219, 16, dtype=int)
        awake = VGroup(*(lattice[i] for i in awake_idx))
        halos = VGroup(*(
            glow_dot(lattice[i].get_center(), PLASMA if k % 2 else VOLT,
                     radius=0.06, halo=2.6)
            for k, i in enumerate(awake_idx)
        ))
        self.play(
            *[dot.animate.set_color(PLASMA if k % 2 else VOLT).scale(1.9)
              for k, dot in enumerate(awake)],
            *[FadeIn(h, scale=0.4) for h in halos],
            run_time=1.6, lag_ratio=0.12,
        )

        # HUD
        term = VGroup(
            hud_line("> stable_latent_moe.online()"),
            hud_line("> experts: 896  |  active: 16", color=PLASMA),
            hud_line("> protocol: reverse_reasoning", color=GOLD),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.18)
        term.to_corner(DOWN + LEFT, buff=0.5)
        moe = MathTex(
            r"y=\sum_{i\in\mathcal{T}} g_i(x)\,E_i(x)"
            r"\qquad |\mathcal{T}|=16,\ N_E=896",
            font_size=30, color=PAPER,
        ).to_corner(UP + RIGHT, buff=0.5)
        for mob in (term, moe):
            self.add_fixed_in_frame_mobjects(mob)
        self.play(Write(term[0]), run_time=0.7)
        self.play(Write(term[1]), Write(term[2]), run_time=0.9)
        self.play(Write(moe), run_time=1.2)
        self.wait(1.0)
        self.play(*[FadeOut(m) for m in (term, moe, lattice, halos, dust)],
                  run_time=0.8)


# ----------------------------------------------------------------------
# ACT II - THE GOAL crystallizes over a manifold of conjectures
# ----------------------------------------------------------------------
class RRGoal(ThreeDScene):
    def construct(self):
        self.set_camera_orientation(phi=CAM_PHI, theta=CAM_THETA)

        # wireframe ripple manifold - flat polylines living at 3D coordinates
        xs = np.linspace(-7, 7, 15)
        ripples = VGroup()
        for x in xs:
            seg_pts = []
            for y in np.linspace(-6, 6, 26):
                z = -2.6 + 0.35 * np.sin(0.9 * y + 1.7 * x) * np.cos(0.6 * x)
                seg_pts.append(np.array([x, y, z]))
            curve = VMobject(stroke_color=ULTRA, stroke_width=1.5)
            curve.set_points_as_corners(seg_pts)
            ripples.add(curve)
        ripples.set_opacity(0.45)
        self.play(FadeIn(ripples, run_time=1.0))

        # the goal monolith
        goal_tex = r"\mathcal{G}:\ \ \sum_{k=1}^{n} k^3 \;=\; \left(\frac{n(n+1)}{2}\right)^2"
        goal = MathTex(goal_tex, font_size=52, color=GOLD)
        face_camera(goal)
        glow = MathTex(goal_tex, font_size=52, color=GOLD)
        face_camera(glow)
        glow.set_stroke(width=9, opacity=0.30)
        glow.set_fill(opacity=0.0)
        monolith = VGroup(glow, goal)

        note = MathTex(r"T_n = \tfrac{n(n+1)}{2}", font_size=28, color=PAPER)
        note.move_to(np.array([4.4, -0.2, 0.6]))
        face_camera(note)

        self.play(Write(goal), run_time=1.8)
        self.play(FadeIn(glow, scale=1.03), Write(note), run_time=1.0)

        caption = hud_line("// the protocol begins at the end", size=24,
                           color=GOLD)
        caption.to_edge(DOWN, buff=0.6)
        self.add_fixed_in_frame_mobjects(caption)
        self.play(Write(caption), run_time=0.8)

        # heartbeat pulse on the goal
        self.play(monolith.animate.scale(1.06), rate_func=there_and_back,
                  run_time=1.2)
        self.move_camera(zoom=1.22, run_time=2.4, rate_func=smooth)
        self.wait(0.4)
        self.play(*[FadeOut(m) for m in (monolith, note, caption, ripples)],
                  run_time=0.8)


# ----------------------------------------------------------------------
# ACT III - BACKWARD BLOOM: the goal decomposes into sufficient subgoals
# ----------------------------------------------------------------------
class RRBackwardBloom(ThreeDScene):
    def construct(self):
        self.set_camera_orientation(phi=CAM_PHI, theta=CAM_THETA, zoom=1.05)
        nodes, edges, pos = build_reasoning_tree()

        caption = hud_line("// step 1 - reason backward: what would suffice?",
                           size=24, color=VOLT)
        caption.to_edge(DOWN, buff=0.55)
        rule = MathTex(r"\mathcal{G} \;\Longleftarrow\; g_1 \wedge \tau \wedge \beta",
                       font_size=30, color=GOLD)
        rule.to_corner(UP + LEFT, buff=0.45)
        for mob in (caption, rule):
            self.add_fixed_in_frame_mobjects(mob)

        # the goal descends
        self.play(FadeIn(nodes["G"], shift=UP * 0.6), Write(caption),
                  run_time=1.0)
        self.play(Write(rule), run_time=0.8)

        # level 1 bloom: g1, tau, beta
        level1 = [("G", "g1"), ("G", "tau"), ("G", "beta")]
        self.play(
            *[GrowFromPoint(edges[k], pos[k[0]]) for k in level1],
            run_time=0.9, lag_ratio=0.25,
        )
        self.play(
            *[Write(nodes[k[1]]) for k in level1],
            run_time=1.3, lag_ratio=0.3,
        )

        # level 2 bloom under g1: ell, g2, g3
        level2 = [("g1", "ell"), ("g1", "g2"), ("g1", "g3")]
        self.play(
            *[GrowFromPoint(edges[k], pos[k[0]]) for k in level2],
            run_time=0.9, lag_ratio=0.25,
        )
        self.play(
            *[Write(nodes[k[1]]) for k in level2],
            run_time=1.3, lag_ratio=0.3,
        )

        # level 3: the axioms ignite green
        level3 = [("g2", "a1"), ("g3", "a2")]
        self.play(
            *[GrowFromPoint(edges[k], pos[k[0]]) for k in level3],
            run_time=0.8,
        )
        self.play(
            *[Write(nodes[k[1]]) for k in level3],
            run_time=1.1,
        )
        self.play(
            nodes["a1"].animate.scale(1.12),
            nodes["a2"].animate.scale(1.12),
            nodes["beta"].animate.scale(1.12),
            rate_func=there_and_back, run_time=0.9,
        )

        # slow pull-back to take in the whole tree
        self.move_camera(zoom=0.78, run_time=2.2, rate_func=smooth)
        self.wait(0.3)
        everything = list(nodes.values()) + list(edges.values()) + [caption, rule]
        self.play(*[FadeOut(m) for m in everything], run_time=0.8)


# ----------------------------------------------------------------------
# ACT IV - VERIFICATION: light runs the tree forward; KDA / AttnRes check
# ----------------------------------------------------------------------
class RRVerification(ThreeDScene):
    def construct(self):
        self.set_camera_orientation(phi=CAM_PHI, theta=CAM_THETA, zoom=0.78)
        nodes, edges, pos = build_reasoning_tree()
        dim_tree(nodes, edges)
        self.add(*edges.values(), *nodes.values())

        caption = hud_line("// step 2 - verify forward: every link checked",
                           size=24, color=AXIOM)
        caption.to_edge(DOWN, buff=0.55)
        self.add_fixed_in_frame_mobjects(caption)
        self.play(Write(caption), run_time=0.7)

        # verification pulses climb the tree, leaves -> goal
        wave1 = [("g2", "a1"), ("g3", "a2")]          # axioms fire first
        wave2 = [("g1", "ell"), ("g1", "g2"), ("g1", "g3")]
        wave3 = [("G", "g1"), ("G", "tau"), ("G", "beta")]

        def pulse(edge_key, color):
            parent, child = edge_key
            p = glow_dot(pos[child], color, radius=0.09, halo=2.8)
            self.add(p)
            return p, p.animate.move_to(pos[parent])

        # axioms ignite
        self.play(
            nodes["a1"].animate.set_opacity(1).scale(1.15),
            nodes["a2"].animate.set_opacity(1).scale(1.15),
            nodes["beta"].animate.set_opacity(1).scale(1.15),
            nodes["ell"].animate.set_opacity(1),
            nodes["tau"].animate.set_opacity(1),
            run_time=0.8,
        )

        pulses1 = [pulse(k, AXIOM) for k in wave1]
        self.play(*[anim for _, anim in pulses1],
                  edges[("g2", "a1")].animate.set_opacity(1),
                  edges[("g3", "a2")].animate.set_opacity(1),
                  run_time=0.9, rate_func=rush_into)
        self.remove(*[p for p, _ in pulses1])
        self.play(nodes["g2"].animate.set_opacity(1),
                  nodes["g3"].animate.set_opacity(1), run_time=0.4)

        pulses2 = [pulse(k, VOLT) for k in wave2]
        self.play(*[anim for _, anim in pulses2],
                  *[edges[k].animate.set_opacity(1) for k in wave2],
                  run_time=0.9, rate_func=rush_into)
        self.remove(*[p for p, _ in pulses2])
        self.play(nodes["g1"].animate.set_opacity(1).scale(1.1),
                  run_time=0.4)

        pulses3 = [pulse(k, GOLD) for k in wave3]
        self.play(*[anim for _, anim in pulses3],
                  *[edges[k].animate.set_opacity(1) for k in wave3],
                  run_time=1.0, rate_func=rush_into)
        self.remove(*[p for p, _ in pulses3])

        # the goal blazes; shockwave rings
        self.play(nodes["G"].animate.set_opacity(1).scale(1.25), run_time=0.5)
        rings = VGroup()
        for r, op in ((0.3, 0.9), (0.5, 0.6), (0.7, 0.4)):
            ring = Circle(radius=r, color=GOLD, stroke_width=3)
            ring.set_opacity(op)
            face_camera(ring)
            ring.move_to(pos["G"])
            rings.add(ring)
        self.play(
            *[ring.animate.scale(6.5).set_opacity(0) for ring in rings],
            run_time=1.3, lag_ratio=0.15, rate_func=rush_from,
        )
        self.remove(rings)

        # the machinery that checked the proof: KDA + AttnRes plates
        kda = MathTex(
            r"\mathrm{KDA}:\ S_t = S_{t-1}\,\Gamma_t"
            r" + \beta_t\, k_t\,(v_t - S_{t-1}k_t)^{\top}",
            font_size=26, color=VOLT,
        )
        att = MathTex(
            r"\mathrm{AttnRes}:\ h_{\ell} = \sum_{i<\ell} w_i\, h_i",
            font_size=26, color=PLASMA,
        )
        kda.to_corner(DOWN + LEFT, buff=0.45).shift(UP * 0.9)
        att.to_corner(DOWN + RIGHT, buff=0.45).shift(UP * 0.9)
        self.add_fixed_in_frame_mobjects(kda, att)
        self.play(Write(kda), Write(att), run_time=1.2)
        self.wait(0.5)

        # collapse into the goal star
        keep = nodes["G"]
        rest = [m for k, m in nodes.items() if k != "G"] + list(edges.values())
        self.play(
            *[m.animate.move_to(pos["G"]).scale(0.05).set_opacity(0)
              for m in rest],
            FadeOut(caption), FadeOut(kda), FadeOut(att),
            keep.animate.scale(1.4),
            run_time=1.4, rate_func=rush_into,
        )
        self.play(FadeOut(keep), run_time=0.5)


# ----------------------------------------------------------------------
# ACT V - SIGIL: the halo of the protocol, then the K3 signature
# ----------------------------------------------------------------------
class RRSigil(ThreeDScene):
    def construct(self):
        self.set_camera_orientation(phi=78 * DEGREES, theta=CAM_THETA,
                                    zoom=1.05)
        glyphs_tex = [
            r"\sum k^3", r"T_n^2", r"\Longleftarrow", r"\Gamma_t",
            r"k_t", r"v_t", r"h_\ell", r"\tfrac{16}{896}",
            r"10^6\,\mathrm{tok}", r"2.8\mathrm{T}", r"\mathcal{G}",
            r"\checkmark",
        ]
        colors = [VOLT, GOLD, PLASMA, ULTRA, VOLT, PLASMA, ULTRA, GOLD,
                  VOLT, PLASMA, GOLD, AXIOM]
        ring = VGroup()
        R = 3.4
        for k, (tex, col) in enumerate(zip(glyphs_tex, colors)):
            g = MathTex(tex, font_size=34, color=col)
            ang = 2 * PI * k / len(glyphs_tex)
            p = R * np.array([np.cos(ang), np.sin(ang), 0.0])
            g.move_to(p)
            g.rotate(78 * DEGREES, axis=RIGHT)
            ring.add(g)
        self.play(FadeIn(ring, run_time=1.0))
        spin = ring.animate.rotate(2 * PI / 3, axis=OUT, about_point=ORIGIN)

        # the goal star burns at the center (kept facing the camera)
        star = glow_dot(ORIGIN, GOLD, radius=0.22, halo=4.5)
        face_camera(star, phi=78 * DEGREES)
        self.play(FadeIn(star, scale=0.2), run_time=0.8)
        self.play(spin, run_time=3.4, rate_func=linear)

        # signature card
        title = Text("KIMI K3", font="Consolas", font_size=84, color=PAPER,
                     weight="BOLD")
        title.set_color_by_gradient(VOLT, PLASMA)
        sub = hud_line("reason backward  ·  verify forward", size=26,
                       color=GOLD)
        micro = hud_line("k3 swarm × manim ce  ·  30 s transmission", size=18,
                         color=GHOST)
        card = VGroup(title, sub, micro).arrange(DOWN, buff=0.35)
        self.add_fixed_in_frame_mobjects(card)
        self.play(
            ring.animate.set_opacity(0.3),
            star.animate.set_opacity(0.25),
            Write(title), run_time=1.2,
        )
        self.play(FadeIn(sub, shift=UP * 0.2), FadeIn(micro), run_time=0.9)
        self.wait(0.6)
        self.play(*[FadeOut(m) for m in (card, ring, star)], run_time=0.9)
