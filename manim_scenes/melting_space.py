"""MELTING SPACE - Ricci Flow and the Poincare Conjecture.

A six-scene true-3D film, built to the approved verbose prompt
(prompts/RicciFlowFilm.tex). Every surface is a glowing wireframe of flat
polylines living at 3D coordinates (Cairo-fast); every morph interpolates
precomputed point arrays; every equation is real.

Scenes (render each, then concatenate):
    MS1Shapes      - the question of shapes, the rubber-band test, Poincare 1904
    MS2Curvature   - Gaussian curvature as a heat-map fingerprint
    MS3HeatFlow    - heat equation -> Ricci flow, the melt to a sphere
    MS4NeckPinch   - the neck pinches: |Rm| -> infinity in finite time
    MS5Surgery     - Perelman's cut and cap; the cascade to spheres
    MS6Theorem     - the conjecture becomes a theorem; finale

Render (1080p30):
    manim render -r 1920,1080 --fps 30 manim_scenes/melting_space.py MS1Shapes
"""

from __future__ import annotations

import numpy as np
from manim import (
    DEGREES, DOWN, LEFT, ORIGIN, OUT, PI, RIGHT, TAU, UP,
    Circle, DecimalNumber, Dot, FadeIn, FadeOut, MathTex, Tex, Text,
    ThreeDScene, VGroup, VMobject, ValueTracker, Write,
    linear, rush_from, rush_into, smooth, there_and_back,
    config,
)

# ----------------------------------------------------------------------
# palette - heat on void
# ----------------------------------------------------------------------
VOID = "#02020c"
GOLD = "#ffd166"        # the sphere / hero
CYAN = "#00e5ff"        # captions, loops, cool curvature
MAGENTA = "#ff2fb3"     # hot curvature
SADDLE = "#4d7cff"      # negative curvature
BLOOD = "#ff4040"       # surgery / warning
PAPER = "#f4f1ff"       # near-white
GHOST = "#3a3550"       # dim / ghost

CAM_PHI = 68 * DEGREES
CAM_THETA = -90 * DEGREES

config.background_color = VOID


# ----------------------------------------------------------------------
# generic helpers
# ----------------------------------------------------------------------
def face_camera(mob, phi=CAM_PHI):
    """Orient a flat mobject so it looks straight at the 3D camera."""
    mob.rotate(phi, axis=RIGHT)
    return mob


def hud(text, size=22, color=CYAN, **kwargs):
    return Text(text, font="Consolas", font_size=size, color=color, **kwargs)


def polyline(pts, color, width=1.3, opacity=1.0):
    c = VMobject(stroke_color=color, stroke_width=width,
                 stroke_opacity=opacity)
    c.set_points_as_corners([np.asarray(p, dtype=float) for p in pts])
    return c


def glow_ring(pts, color, width=2.5):
    """A polyline with a soft neon sheath (for hero curves only)."""
    core = polyline(pts, color, width=width)
    sheath = polyline(pts, color, width=width * 3.4)
    sheath.set_stroke(opacity=0.16)
    return VGroup(sheath, core)


def heat_color(t):
    """Cool cyan -> magenta -> white-hot gradient, t in [0, 1]."""
    t = float(np.clip(t, 0.0, 1.0))
    if t < 0.5:
        return _lerp_color(CYAN, MAGENTA, t * 2)
    return _lerp_color(MAGENTA, "#ffffff", (t - 0.5) * 2)


def _lerp_color(c1, c2, a):
    from manim import ManimColor
    x = np.array(ManimColor(c1).to_rgb())
    y = np.array(ManimColor(c2).to_rgb())
    return ManimColor(tuple(x * (1 - a) + y * a))


# ----------------------------------------------------------------------
# surface machinery - star-shaped radial surfaces and their wireframes
# ----------------------------------------------------------------------
def radial_point(r, u, v):
    """Point on a star-shaped surface: r(u,v) times the unit direction."""
    return r(u, v) * np.array(
        [np.sin(u) * np.cos(v), np.sin(u) * np.sin(v), np.cos(u)]
    )


def wireframe_arrays(r, n_lat=11, n_lon=14, n_pts=44):
    """Point arrays for a lat/long wireframe of a radial surface.

    Returns a list of point arrays (each N x 3) - the morphable currency.
    """
    arrays = []
    us = np.linspace(PI / (n_lat + 1), PI * n_lat / (n_lat + 1), n_lat)
    for u in us:
        vs = np.linspace(0, TAU, n_pts)
        arrays.append(np.array([radial_point(r, u, v) for v in vs]))
    for j in range(n_lon):
        v = TAU * j / n_lon
        us2 = np.linspace(0.02, PI - 0.02, n_pts)
        arrays.append(np.array([radial_point(r, u, v) for u in us2]))
    return arrays


def wireframe_from_arrays(arrays, color, width=1.2, opacity=0.95):
    return VGroup(*(polyline(a, color, width, opacity) for a in arrays))


def morph_play(curves, A0, A1, run_time=2.0, rate_func=smooth, **kwargs):
    """An animation interpolating every curve from A0[i] to A1[i]."""
    from manim import UpdateFromAlphaFunc

    def update(m, alpha):
        for c, a0, a1 in zip(curves, A0, A1):
            c.set_points_as_corners(a0 * (1 - alpha) + a1 * alpha)

    return UpdateFromAlphaFunc(curves, update, run_time=run_time,
                               rate_func=rate_func, **kwargs)


# --- the shapes of Scene 1 (all star-shaped about the origin) -----------
R0 = 1.9


def r_sphere(u, v):
    return R0 + 0.0 * np.asarray(u, dtype=float) * np.asarray(v, dtype=float)


def r_pear(u, v):
    return R0 * (1.0 - 0.28 * np.cos(u) + 0.06 * np.cos(2 * u))


def r_dumbbell(u, v):
    return R0 * (1.0 + 0.42 * np.cos(2 * u))


def r_blob(u, v):
    return R0 * (1.0
                 + 0.16 * np.sin(3 * u) * np.cos(2 * v)
                 + 0.11 * np.cos(2 * u) * np.sin(3 * v)
                 + 0.07 * np.sin(5 * u + 1.3) * np.cos(v))


def r_round(mean_r):
    def f(u, v):
        return mean_r + 0.0 * u * v
    return f


# ----------------------------------------------------------------------
# revolution surfaces (Scene 4 dumbbell with a real neck)
# ----------------------------------------------------------------------
def revolution_arrays(profile, x_lo, x_hi, n_lat=22, n_lon=12, n_pts=40,
                      neck=1.0):
    """Surface of revolution about the x-axis.

    profile(x) gives the radius; `neck` squeezes x=0 by that factor.
    """
    arrays = []
    xs = np.linspace(x_lo, x_hi, n_lat)
    for x in xs:
        rad = profile(x)
        if abs(x) < 1e-9:
            rad *= 1.0
        rad = rad * (1 - (1 - neck) * np.exp(-((x / 0.55) ** 2)))
        th = np.linspace(0, TAU, n_pts)
        arrays.append(np.array([
            [x, rad * np.cos(t), rad * np.sin(t)] for t in th
        ]))
    for j in range(n_lon):
        t = TAU * j / n_lon
        xs2 = np.linspace(x_lo, x_hi, n_pts)
        rads = profile(xs2) * (1 - (1 - neck) * np.exp(-((xs2 / 0.55) ** 2)))
        arrays.append(np.array([
            [x, rad * np.cos(t), rad * np.sin(t)] for x, rad in zip(xs2, rads)
        ]))
    return arrays


def db_profile(x):
    """Dumbbell profile: two lobes at x = +/-1.5, neck at 0."""
    x = np.asarray(x, dtype=float)
    return 1.05 * (0.46 + 0.62 * (
        np.exp(-(((x - 1.5) / 0.85) ** 2)) + np.exp(-(((x + 1.5) / 0.85) ** 2))
    ))


# ----------------------------------------------------------------------
# numeric curvature on a radial surface (Scene 2)
# ----------------------------------------------------------------------
class RadialSurfaceGeometry:
    """First/second fundamental forms on a grid -> K and H fields."""

    def __init__(self, r, nu=40, nv=80):
        self.r = r
        self.nu, self.nv = nu, nv
        u = np.linspace(0.04, PI - 0.04, nu)
        v = np.linspace(0, TAU, nv, endpoint=False)
        self.U, self.V = np.meshgrid(u, v, indexing="ij")
        P = np.stack([radial_point(r, ui, vi)
                      for ui, vi in zip(self.U.ravel(), self.V.ravel())]
                     ).reshape(nu, nv, 3)
        du, dv = u[1] - u[0], v[1] - v[0]
        Pu = np.gradient(P, du, axis=0)
        Pv = np.gradient(P, dv, axis=1)
        Puu = np.gradient(Pu, du, axis=0)
        Puv = np.gradient(Pu, dv, axis=1)
        Pvv = np.gradient(Pv, dv, axis=1)
        E = np.einsum("ijk,ijk->ij", Pu, Pu)
        F = np.einsum("ijk,ijk->ij", Pu, Pv)
        G = np.einsum("ijk,ijk->ij", Pv, Pv)
        N = np.cross(Pu, Pv)
        Nn = np.linalg.norm(N, axis=-1, keepdims=True)
        Nn[Nn < 1e-9] = 1e-9
        N = N / Nn
        L = np.einsum("ijk,ijk->ij", Puu, N)
        M = np.einsum("ijk,ijk->ij", Puv, N)
        Nn2 = np.einsum("ijk,ijk->ij", Pvv, N)
        det1 = E * G - F * F
        det1[np.abs(det1) < 1e-9] = 1e-9
        self.K = (L * Nn2 - M * M) / det1
        self.H = (E * Nn2 - 2 * F * M + G * L) / (2 * det1)
        self.P = P
        self.N = N
        Tu = Pu / np.maximum(np.linalg.norm(Pu, axis=-1, keepdims=True), 1e-9)
        Tv = Pv / np.maximum(np.linalg.norm(Pv, axis=-1, keepdims=True), 1e-9)
        self.Tu, self.Tv = Tu, Tv

    def _idx(self, u, v):
        iu = int(np.clip((u - 0.04) / (PI - 0.08) * (self.nu - 1), 0, self.nu - 1))
        iv = int((v % TAU) / TAU * self.nv) % self.nv
        return iu, iv

    def k_at(self, u, v):
        """Principal curvatures at (u, v) via grid lookup."""
        iu, iv = self._idx(u, v)
        K = self.K[iu, iv]
        H = self.H[iu, iv]
        disc = max(H * H - K, 0.0)
        return H + np.sqrt(disc), H - np.sqrt(disc), self.P[iu, iv]

    def frame_at(self, u, v):
        """Position, normal, coordinate tangents and principal curvatures."""
        iu, iv = self._idx(u, v)
        K = self.K[iu, iv]
        H = self.H[iu, iv]
        disc = max(H * H - K, 0.0)
        k1, k2 = H + np.sqrt(disc), H - np.sqrt(disc)
        return (self.P[iu, iv], self.N[iu, iv], self.Tu[iu, iv],
                self.Tv[iu, iv], k1, k2)


# ----------------------------------------------------------------------
# SCENE 1 - The Question of Shapes
# ----------------------------------------------------------------------
class MS1Shapes(ThreeDScene):
    def construct(self):
        self.set_camera_orientation(phi=CAM_PHI, theta=CAM_THETA)

        A_s = wireframe_arrays(r_sphere)
        A_p = wireframe_arrays(r_pear)
        A_d = wireframe_arrays(r_dumbbell)
        A_b = wireframe_arrays(r_blob)

        shape = wireframe_from_arrays(A_s, GOLD, width=1.4)
        shape.shift(LEFT * 0.0)

        # ambient dust
        rng = np.random.default_rng(3)
        dust = VGroup(*(Dot(point=p, radius=0.02, color=GHOST)
                        for p in rng.uniform(-7, 7, (70, 3))))
        dust.set_opacity(0.5)
        self.add(dust)

        # beat 1: the perfect sphere, slowly turning (0 - 2.2s)
        self.play(FadeIn(shape, run_time=1.2))
        self.play(shape.animate.rotate(PI / 6, axis=OUT), run_time=1.4,
                  rate_func=linear)

        # beat 2: deformations - pear, dumbbell, blob (2.2 - 6.4s)
        cap1 = hud("// to a topologist, these are all the same shape", size=22)
        cap1.to_edge(DOWN, buff=0.55)
        self.add_fixed_in_frame_mobjects(cap1)
        self.play(Write(cap1), run_time=0.7)
        for A in (A_p, A_d, A_b):
            self.play(morph_play(shape, A_s, A, run_time=1.3), rate_func=smooth)
            A_s = [a.copy() for a in A]

        # beat 3: the rubber-band test (6.4 - 11.5s)
        self.play(FadeOut(cap1), run_time=0.4)
        loop_g = glow_ring(self._loop_pts(PI / 2, 1.02), CYAN, width=2.5)
        self.play(FadeIn(loop_g, run_time=0.6))
        self.play(self._loop_slide(loop_g, final_u=0.06), run_time=2.2,
                  rate_func=smooth)
        self.play(FadeOut(loop_g, run_time=0.4))
        cap2 = hud("// on a sphere, every loop lets go", size=22, color=GOLD)
        cap2.to_edge(DOWN, buff=0.55)
        self.add_fixed_in_frame_mobjects(cap2)
        self.play(Write(cap2), run_time=0.7)

        # ghost donut with a stuck loop (11.5 - 15s)
        donut = self._ghost_torus()
        donut.shift(RIGHT * 4.2 + DOWN * 0.4)
        stuck = glow_ring(self._torus_loop_pts(1.0, 0.42), MAGENTA, width=2.2)
        stuck.shift(RIGHT * 4.2 + DOWN * 0.4)
        self.play(FadeIn(donut), FadeIn(stuck), run_time=1.0)
        cap3 = hud("// on a donut, some never can", size=22, color=MAGENTA)
        cap3.next_to(cap2, UP, buff=0.0).align_to(cap2, LEFT)
        self.add_fixed_in_frame_mobjects(cap3)
        self.play(Write(cap3), run_time=0.7)
        self.play(stuck.animate.scale(0.93), rate_func=there_and_back,
                  run_time=1.0)
        self.play(FadeOut(donut), FadeOut(stuck), FadeOut(cap2),
                  FadeOut(cap3), run_time=0.8)

        # beat 4: the question (15 - 20.5s)
        q = MathTex(
            r"\text{Poincar\'e 1904:}\quad \forall\,\gamma : S^1 \to M,\ "
            r"\gamma \simeq \text{point} \;\Rightarrow\; M \cong S^3\ ?",
            font_size=38, color=GOLD,
        )
        q.to_edge(UP, buff=0.6)
        self.add_fixed_in_frame_mobjects(q)
        self.play(Write(q), run_time=2.0)
        self.wait(1.6)
        self.play(*[FadeOut(m) for m in (shape, q, dust)], run_time=1.0)

    # -- rubber band helpers -------------------------------------------
    def _loop_pts(self, u, scale):
        th = np.linspace(0, TAU, 60)
        # loop on the current blob-ish surface; use blob radius * scale
        pts = []
        for t in th:
            r = r_blob(u, t) * scale
            pts.append(r * np.array([np.sin(u) * np.cos(t),
                                     np.sin(u) * np.sin(t), np.cos(u)]))
        return pts

    def _loop_slide(self, loop, final_u):
        from manim import UpdateFromAlphaFunc
        u0 = PI / 2

        def update(m, a):
            u = u0 + (final_u - u0) * a
            pts = self._loop_pts(u, 1.02)
            m[1].set_points_as_corners(pts)   # core
            m[0].set_points_as_corners(pts)   # sheath

        return UpdateFromAlphaFunc(loop, update)

    def _ghost_torus(self, R=1.0, r=0.42, n1=10, n2=8, n_pts=32):
        group = VGroup()
        for i in range(n1):
            u = TAU * i / n1
            pts = []
            for j in range(n_pts):
                w = TAU * j / n_pts
                x = (R + r * np.cos(w)) * np.cos(u)
                y = (R + r * np.cos(w)) * np.sin(u)
                z = r * np.sin(w)
                pts.append([x, y, z])
            group.add(polyline(pts, GHOST, 1.0, 0.6))
        for j in range(n2):
            w = TAU * j / n2
            pts = []
            for i in range(n_pts):
                u = TAU * i / n_pts
                x = (R + r * np.cos(w)) * np.cos(u)
                y = (R + r * np.cos(w)) * np.sin(u)
                z = r * np.sin(w)
                pts.append([x, y, z])
            group.add(polyline(pts, GHOST, 1.0, 0.6))
        return group

    def _torus_loop_pts(self, R, r):
        # loop through the hole, around the tube (the stuck direction)
        pts = []
        for j in range(60):
            w = TAU * j / 60
            pts.append([(R + r * np.cos(w)), 0.0, r * np.sin(w)])
        return pts


# ----------------------------------------------------------------------
# osculating ring for Scene 2
# ----------------------------------------------------------------------
def osculating_pts(P, N, T, k, n=26):
    """Arc of the best-fitting circle at point P, plane spanned by (T, N).

    Arc length is kept short (~0.9 units) so rings stay local on the surface.
    """
    kk = float(np.clip(k, -2.8, 2.8))
    if abs(kk) < 0.22:
        kk = 0.22 if kk >= 0 else -0.22
    rho = float(np.clip(1.0 / abs(kk), 0.3, 2.2))
    arc = min(1.9, 0.9 / rho)
    sgn = 1.0 if kk > 0 else -1.0
    c = P + N * rho * sgn
    a, b = -N * sgn, T
    return [c + rho * (np.cos(s) * a + np.sin(s) * b)
            for s in np.linspace(-arc, arc, n)]


# ----------------------------------------------------------------------
# SCENE 2 - Curvature: the Fingerprint of Shape
# ----------------------------------------------------------------------
class MS2Curvature(ThreeDScene):
    def construct(self):
        self.set_camera_orientation(phi=CAM_PHI, theta=CAM_THETA)
        geo = RadialSurfaceGeometry(r_blob)
        blob = wireframe_from_arrays(wireframe_arrays(r_blob), GOLD, 1.4)
        self.play(FadeIn(blob, run_time=1.0))

        # roaming probe with two principal rings
        tv = ValueTracker(0.0)
        probe = Dot(radius=0.075, color=PAPER)
        ring1 = polyline([[0, 0, 0], [0, 0, 0.01]], CYAN, 2.4)
        ring2 = polyline([[0, 0, 0], [0, 0, 0.01]], MAGENTA, 2.4)

        def path(tt):
            # meridian sweep over a cap, then around the waist
            if tt < 0.5:
                return 0.55 + 1.9 * (tt / 0.5), 0.6 + 0.35 * np.sin(TAU * tt)
            s = (tt - 0.5) / 0.5
            return 1.62 + 0.12 * np.sin(TAU * s), 0.95 + 2.4 * s

        def refresh():
            u, v = path(tv.get_value())
            P, N, Tu, Tv, k1, k2 = geo.frame_at(u, v)
            probe.move_to(P * 1.005)
            ring1.set_points_as_corners(osculating_pts(P, N, Tu, k1))
            ring2.set_points_as_corners(osculating_pts(P, N, Tv, k2))

        grp = VGroup(probe, ring1, ring2)
        grp.add_updater(lambda m: refresh())
        self.add(grp)
        refresh()

        eq1 = MathTex(r"k_i = \frac{1}{r_i}", font_size=40, color=PAPER)
        eq2 = MathTex(r"K = k_1 \cdot k_2", font_size=40, color=GOLD)
        eqs = VGroup(eq1, eq2).arrange(RIGHT, buff=0.8)
        eqs.to_edge(UP, buff=0.55)
        self.add_fixed_in_frame_mobjects(eqs)
        self.play(FadeIn(probe, scale=0.3), FadeIn(ring1), FadeIn(ring2),
                  run_time=0.8)
        self.play(Write(eq1), run_time=0.8)
        self.play(tv.animate.set_value(0.5), run_time=5.0, rate_func=smooth)
        self.play(Write(eq2), run_time=0.8)

        # heat map of Gaussian curvature - set once, fade in
        K = geo.K
        kmax = np.percentile(np.abs(K), 92) + 1e-9
        dots = VGroup()
        for iu in range(1, geo.nu - 1, 2):
            for iv in range(0, geo.nv, 2):
                kk = float(K[iu, iv] / kmax)
                if kk >= 0:
                    col = heat_color(0.15 + 0.85 * min(kk, 1.0))
                else:
                    col = _lerp_color(SADDLE, VOID, 1 - min(-kk, 1.0))
                dots.add(Dot(point=geo.P[iu, iv] * 1.004, radius=0.038,
                             color=col))
        cap = hud("// the shape's fingerprint, painted in fire", size=22,
                  color=GOLD)
        cap.to_edge(DOWN, buff=0.55)
        self.add_fixed_in_frame_mobjects(cap)
        self.play(FadeIn(dots, run_time=1.6, lag_ratio=0.06))
        self.play(Write(cap), run_time=0.8)

        # camera tour: hot cap, then cold saddle
        cap_pt = geo.P[6, int(0.6 / TAU * geo.nv)]
        saddle_pt = geo.P[int(1.62 / PI * geo.nu), int(2.2 / TAU * geo.nv)]
        self.move_camera(frame_center=cap_pt * 0.55, zoom=1.35, run_time=2.4)
        self.move_camera(frame_center=saddle_pt * 0.55, zoom=1.5, run_time=2.6)

        # Theorema Egregium
        theo = Tex(r"\textbf{Theorema Egregium:} $K$ is intrinsic",
                   font_size=32, color=PAPER)
        theo.to_edge(DOWN, buff=0.55)
        self.add_fixed_in_frame_mobjects(theo)
        self.play(FadeOut(cap), run_time=0.5)
        self.play(Write(theo), run_time=1.0)
        self.wait(1.4)
        grp.clear_updaters()
        self.play(*[FadeOut(m) for m in (blob, dots, grp, eqs, theo)],
                  run_time=1.0)


# ----------------------------------------------------------------------
# SCENE 3 - The Heat Equation for Shape
# ----------------------------------------------------------------------
class MS3HeatFlow(ThreeDScene):
    def construct(self):
        self.set_camera_orientation(phi=CAM_PHI, theta=CAM_THETA)

        # ---- beat 1: the heat plate (0 - 7.5s) -------------------------
        n = 18
        side = 5.0
        grid = VGroup()
        for i in range(n + 1):
            t = -side / 2 + side * i / n
            grid.add(polyline([[t, -side / 2, -1.2], [t, side / 2, -1.2]],
                              GHOST, 0.8, 0.6))
            grid.add(polyline([[-side / 2, t, -1.2], [side / 2, t, -1.2]],
                              GHOST, 0.8, 0.6))
        xs = np.linspace(-side / 2, side / 2, n)
        dots = VGroup(*(
            Dot(point=[x, y, -1.15], radius=0.075, color=VOID)
            for x in xs for y in xs
        ))

        eq_heat = MathTex(r"\partial_t u = \Delta u", font_size=44,
                          color=PAPER)
        eq_heat.to_edge(UP, buff=0.55)
        cap1 = hud("// heat spreads until every point equals its neighbors",
                   size=22)
        cap1.to_edge(DOWN, buff=0.55)
        for m in (eq_heat, cap1):
            self.add_fixed_in_frame_mobjects(m)

        self.play(FadeIn(grid), Write(eq_heat), run_time=1.0)

        t_heat = ValueTracker(0.0)

        def heat_refresh():
            tt = t_heat.get_value()
            s2 = 0.12 + 0.55 * tt
            amp = 1.0 / (1.0 + 2.2 * tt)
            for d in dots:
                x, y = d.get_center()[0], d.get_center()[1]
                u = amp * np.exp(-(x * x + y * y) / (2 * s2 * side))
                base = 0.12 + 0.5 * tt
                d.set_color(heat_color(min(base + u, 1.0)))

        heat_grp = VGroup(dots)
        heat_grp.add_updater(lambda m: heat_refresh())
        self.add(dots)
        heat_refresh()
        self.play(FadeIn(dots, run_time=0.8))
        self.play(t_heat.animate.set_value(1.0), run_time=4.6,
                  rate_func=linear)
        heat_grp.clear_updaters()
        self.play(Write(cap1), run_time=0.8)
        self.play(FadeOut(grid), FadeOut(dots), FadeOut(eq_heat),
                  FadeOut(cap1), run_time=0.8)

        # ---- beat 2: Ricci flow equation + colored dumbbell (7.5 - 10s) --
        eq_ricci = MathTex(
            r"\frac{\partial g}{\partial t} = -2\,\mathrm{Ric}(g)",
            font_size=48, color=GOLD)
        eq_ricci.to_edge(UP, buff=0.55)
        ham = hud("Hamilton, 1982 - do the same to shape itself", size=22,
                  color=PAPER)
        ham.next_to(eq_ricci, DOWN, buff=0.3)
        for m in (eq_ricci, ham):
            self.add_fixed_in_frame_mobjects(m)
        self.play(Write(eq_ricci), Write(ham), run_time=1.4)

        geo = RadialSurfaceGeometry(r_dumbbell)
        A0 = wireframe_arrays(r_dumbbell)
        mean_r = float(np.mean([r_dumbbell(u, v)
                                for u in np.linspace(0.1, PI - 0.1, 40)
                                for v in np.linspace(0, TAU, 40)]))
        A1 = wireframe_arrays(r_round(mean_r))

        dumb = wireframe_from_arrays(A0, GOLD, 1.4)
        # per-curve curvature colors (one-time): mean |K| per curve
        curve_cols = self._curve_curvature_colors(geo, A0)
        for c, col in zip(dumb, curve_cols):
            c.set_stroke(color=col)
        self.play(FadeIn(dumb, run_time=1.0))

        # ---- beat 3: the melt (10 - 18s) --------------------------------
        cap2 = hud("// curvature spreads until every point equals its neighbors",
                   size=22, color=GOLD)
        cap2.to_edge(DOWN, buff=0.55)
        self.add_fixed_in_frame_mobjects(cap2)

        from manim import UpdateFromAlphaFunc

        def melt(m, alpha):
            for c, a0, a1, col0 in zip(dumb, A0, A1, curve_cols):
                c.set_points_as_corners(a0 * (1 - alpha) + a1 * alpha)
                c.set_stroke(color=_lerp_color_obj(col0, GOLD, alpha),
                             width=1.4 + 0.3 * alpha)

        self.play(UpdateFromAlphaFunc(dumb, melt, run_time=6.0,
                                      rate_func=smooth))
        self.play(Write(cap2), run_time=0.8)
        self.wait(0.6)
        self.play(FadeOut(cap2), run_time=0.5)

        # ---- beat 4: the cliffhanger waist (18 - 24s) -------------------
        self.play(FadeOut(dumb), FadeOut(eq_ricci), FadeOut(ham),
                  run_time=0.6)
        db_arrays = revolution_arrays(db_profile, -2.8, 2.8, neck=0.85)
        db = wireframe_from_arrays(db_arrays, GOLD, 1.3)
        db.scale(0.9)
        warn = glow_ring(self._neck_ring_pts(0.55 * 0.9), BLOOD, width=3.0)
        self.play(FadeIn(db, run_time=0.8))
        self.play(FadeIn(warn, scale=0.5), run_time=0.6)
        self.play(warn.animate.scale(1.35), rate_func=there_and_back,
                  run_time=1.0)
        self.move_camera(zoom=2.1, frame_center=ORIGIN, run_time=2.4,
                         rate_func=smooth)
        self.play(warn.animate.scale(1.5).set_stroke(opacity=0.9),
                  rate_func=there_and_back, run_time=1.2)
        self.play(FadeOut(db), FadeOut(warn), run_time=0.7)

    # -- helpers ---------------------------------------------------------
    def _curve_curvature_colors(self, geo, arrays):
        """Mean |K| per wireframe curve -> heat colors; blue if K < 0."""
        cols = []
        kmax = np.percentile(np.abs(geo.K), 90) + 1e-9
        for arr in arrays:
            ks, sgn = [], 0.0
            for p in arr[::4]:
                u = np.arccos(np.clip(p[2] / (np.linalg.norm(p) + 1e-9), -1, 1))
                v = np.arctan2(p[1], p[0]) % TAU
                iu, iv = geo._idx(u, v)
                ks.append(abs(geo.K[iu, iv]))
                sgn += geo.K[iu, iv]
            m = min(np.mean(ks) / kmax, 1.0)
            cols.append(heat_color(0.1 + 0.9 * m) if sgn >= 0 else
                        _lerp_color(SADDLE, "#9fc0ff", m * 0.5))
        return cols

    def _neck_ring_pts(self, rad):
        th = np.linspace(0, TAU, 60)
        return [[0.0, rad * np.cos(t), rad * np.sin(t)] for t in th]


def _lerp_color_obj(c1, c2, a):
    return _lerp_color(c1, c2, float(np.clip(a, 0, 1)))


# ----------------------------------------------------------------------
# SCENE 4 - The Neck Pinches
# ----------------------------------------------------------------------
class MS4NeckPinch(ThreeDScene):
    def construct(self):
        self.set_camera_orientation(phi=72 * DEGREES, theta=CAM_THETA,
                                    zoom=1.1)
        n_lat = 22
        xs = np.linspace(-2.8, 2.8, n_lat)
        A0 = revolution_arrays(db_profile, -2.8, 2.8, n_lat=n_lat, neck=1.0)
        A1 = revolution_arrays(db_profile, -2.8, 2.8, n_lat=n_lat, neck=0.35)
        A2 = revolution_arrays(db_profile, -2.8, 2.8, n_lat=n_lat, neck=0.05)
        db = wireframe_from_arrays(A0, GOLD, 1.3)

        # curvature gauge (fixed frame): label + filling bar meter
        glabel = MathTex(r"|\mathrm{Rm}|_{\mathrm{neck}}", font_size=30,
                         color=PAPER)
        glabel.to_corner(UP + LEFT, buff=0.45)
        from manim import Rectangle
        bar_bg = Rectangle(width=2.6, height=0.22, stroke_color=GHOST,
                           stroke_width=1.2, fill_opacity=0)
        bar_bg.next_to(glabel, DOWN, buff=0.25, aligned_edge=LEFT)
        bar = Rectangle(width=0.02, height=0.22, stroke_opacity=0,
                        fill_color=GOLD, fill_opacity=1)
        bar.next_to(glabel, DOWN, buff=0.25, aligned_edge=LEFT)
        self.add_fixed_in_frame_mobjects(glabel, bar_bg, bar)

        state = {"neck": 1.0}

        def gauge_refresh():
            heat = float(np.clip((1 - state["neck"]) * 1.18, 0.02, 1))
            bar.set(fill_color=heat_color(heat))
            bar.stretch_to_fit_width(2.6 * heat)
            bar.next_to(glabel, DOWN, buff=0.25, aligned_edge=LEFT)

        bar.add_updater(lambda m: gauge_refresh())

        self.play(FadeIn(db, run_time=0.9), FadeIn(glabel), FadeIn(bar_bg),
                  FadeIn(bar))

        from manim import UpdateFromAlphaFunc

        def pinch(A_start, A_end):
            def update(m, alpha):
                neck = np.sqrt(
                    (1 - alpha) * state["n0"] ** 2 + alpha * state["n1"] ** 2)
                state["neck"] = neck
                for i, (c, a0, a1) in enumerate(zip(db, A_start, A_end)):
                    c.set_points_as_corners(a0 * (1 - alpha) + a1 * alpha)
                    if i < n_lat:
                        x = xs[i]
                        hot = float(np.clip(
                            np.exp(-((x / 0.6) ** 2)) * (1 - neck) ** 1.3
                            * 1.35, 0, 1))
                        if hot > 0.04:
                            c.set_stroke(color=heat_color(hot), width=1.6)
            return UpdateFromAlphaFunc(db, update)

        state["n0"], state["n1"] = 1.0, 0.35
        self.play(pinch(A0, A1), run_time=3.6, rate_func=linear)
        state["n0"], state["n1"] = 0.35, 0.05
        self.play(pinch(A1, A2), run_time=3.4, rate_func=rush_into)

        # the snap: two lobes drift apart; a dying-star flare at the pinch
        left_A = revolution_arrays(db_profile, -2.8, -0.07, n_lat=11,
                                   neck=0.05)
        right_A = revolution_arrays(db_profile, 0.07, 2.8, n_lat=11,
                                    neck=0.05)
        left = wireframe_from_arrays(left_A, GOLD, 1.3)
        right = wireframe_from_arrays(right_A, GOLD, 1.3)
        flare = VGroup(
            Dot(point=ORIGIN, radius=0.5, color="#ffffff"),
            Dot(point=ORIGIN, radius=0.16, color=GOLD),
        )
        flare[0].set_opacity(0.35)
        self.remove(db)
        self.add(left, right, flare)
        self.play(
            left.animate.shift(LEFT * 1.3).rotate(0.35, axis=UP),
            right.animate.shift(RIGHT * 1.3).rotate(-0.35, axis=UP),
            flare.animate.scale(2.6).set_opacity(0),
            run_time=1.8, rate_func=rush_from,
        )

        eq = MathTex(r"|\mathrm{Rm}| \to \infty \quad \text{as} \quad "
                     r"t \to T < \infty", font_size=44, color=BLOOD)
        eq.to_edge(UP, buff=0.55)
        cap = hud("// the flow has died in finite time", size=22, color=BLOOD)
        cap.to_edge(DOWN, buff=0.55)
        for m in (eq, cap):
            self.add_fixed_in_frame_mobjects(m)
        self.play(Write(eq), Write(cap), run_time=1.2)
        bar.clear_updaters()
        self.play(FadeOut(left), FadeOut(right), FadeOut(glabel),
                  FadeOut(bar_bg), FadeOut(bar), FadeOut(eq), FadeOut(cap),
                  run_time=0.8)
        self.wait(1.2)  # two beats of black silence


# ----------------------------------------------------------------------
# surgery helpers
# ----------------------------------------------------------------------
def hemi_arrays(cut_x, rad, sign, n_lat=5, n_lon=8, n_pts=32):
    """Wireframe dome closing a wound of radius `rad` at x = cut_x."""
    arrays = []
    for k in range(1, n_lat + 1):
        phi = (PI / 2) * k / (n_lat + 1)
        rr = rad * np.cos(phi)
        x = cut_x + sign * rad * np.sin(phi)
        th = np.linspace(0, TAU, n_pts)
        arrays.append(np.array([[x, rr * np.cos(t), rr * np.sin(t)]
                                for t in th]))
    for j in range(n_lon):
        t = TAU * j / n_lon
        phis = np.linspace(0.02, PI / 2, n_pts)
        arrays.append(np.array([
            [cut_x + sign * rad * np.sin(p),
             rad * np.cos(p) * np.cos(t), rad * np.cos(p) * np.sin(t)]
            for p in phis
        ]))
    return arrays


def sphere_arrays(center, radius, n_lat=11, n_lon=12, n_pts=40):
    arrs = wireframe_arrays(r_round(radius), n_lat=n_lat, n_lon=n_lon,
                            n_pts=n_pts)
    c = np.asarray(center, dtype=float)
    return [a + c for a in arrs]


def tri_profile(x):
    """Three-lobed profile for the surgery cascade."""
    x = np.asarray(x, dtype=float)
    return 0.95 * (0.34 + 0.62 * (
        np.exp(-(((x - 2.1) / 0.8) ** 2))
        + np.exp(-((x / 0.8) ** 2))
        + np.exp(-(((x + 2.1) / 0.8) ** 2))
    ))


# ----------------------------------------------------------------------
# SCENE 5 - Perelman's Surgery
# ----------------------------------------------------------------------
class MS5Surgery(ThreeDScene):
    def construct(self):
        self.set_camera_orientation(phi=CAM_PHI, theta=CAM_THETA)

        # rewind: the almost-pinched dumbbell returns
        A = revolution_arrays(db_profile, -2.8, 2.8, n_lat=22, neck=0.3)
        db = wireframe_from_arrays(A, GOLD, 1.3)
        self.play(FadeIn(db, run_time=0.8))

        # the incision
        neck_rad = float(db_profile(0)) * 0.3 * 1.1
        ring = glow_ring([[0.0, neck_rad * np.cos(t), neck_rad * np.sin(t)]
                          for t in np.linspace(0, TAU, 60)], BLOOD, 3.0)
        self.play(FadeIn(ring, scale=0.6), run_time=0.5)
        self.play(ring.animate.scale(1.3), rate_func=there_and_back,
                  run_time=0.7)

        # cut: halves drift apart
        left_A = revolution_arrays(db_profile, -2.8, -0.12, n_lat=11,
                                   neck=0.3)
        right_A = revolution_arrays(db_profile, 0.12, 2.8, n_lat=11,
                                    neck=0.3)
        left = wireframe_from_arrays(left_A, GOLD, 1.3)
        right = wireframe_from_arrays(right_A, GOLD, 1.3)
        self.remove(db)
        self.add(left, right)
        self.play(FadeOut(ring),
                  left.animate.shift(LEFT * 0.45),
                  right.animate.shift(RIGHT * 0.45),
                  run_time=0.9)

        # caps graft onto the wounds
        end_rad = float(db_profile(0.12)) * (1 - 0.7 * np.exp(-((0.12 / 0.55) ** 2)))
        capL = wireframe_from_arrays(hemi_arrays(-0.12, end_rad, 1), GOLD,
                                     1.2, 0.9)
        capR = wireframe_from_arrays(hemi_arrays(0.12, end_rad, -1), GOLD,
                                     1.2, 0.9)
        capL.shift(LEFT * 0.45)
        capR.shift(RIGHT * 0.45)
        self.play(FadeIn(capL), FadeIn(capR), run_time=0.8)

        # both pieces melt into their own spheres
        lc = np.array([-1.85, 0, 0]) + LEFT * 0.45
        rc = np.array([1.85, 0, 0]) + RIGHT * 0.45
        sphL = sphere_arrays(lc, 1.15)
        sphR = sphere_arrays(rc, 1.15)

        from manim import UpdateFromAlphaFunc

        def melt(m, alpha):
            for grp, A_start, A_end in ((left, left_A, sphL),
                                        (right, right_A, sphR)):
                for c, a0, a1 in zip(grp, A_start, A_end):
                    a0s = a0 + (LEFT * 0.45 if grp is left else RIGHT * 0.45)
                    c.set_points_as_corners(a0s * (1 - alpha) + a1 * alpha)
            for cap in (capL, capR):
                cap.set_stroke(opacity=0.9 * (1 - alpha))

        Went = MathTex(r"\mathcal{W}(g, f, \tau) \uparrow", font_size=34,
                       color=CYAN)
        Went.to_edge(UP, buff=0.6)
        self.add_fixed_in_frame_mobjects(Went)
        self.play(FadeIn(Went), run_time=0.5)
        self.play(UpdateFromAlphaFunc(VGroup(left, right, capL, capR), melt,
                                      run_time=3.6, rate_func=smooth),
                  FadeOut(Went, run_time=3.0))

        # equations of the operation
        eq1 = MathTex(r"M \cong M_1 \,\#\, M_2", font_size=42, color=PAPER)
        eq2 = MathTex(r"\text{cut } S^2 \times (-\varepsilon, \varepsilon)"
                      r"\text{, cap with } D^3", font_size=30, color=CYAN)
        per = hud("Perelman, 2002-2003", size=24, color=GOLD)
        eqs = VGroup(eq1, eq2, per).arrange(DOWN, buff=0.3)
        eqs.to_edge(DOWN, buff=0.5)
        for m in (eqs,):
            self.add_fixed_in_frame_mobjects(m)
        self.play(Write(eq1), Write(eq2), FadeIn(per), run_time=1.4)
        self.wait(0.8)
        self.play(FadeOut(left), FadeOut(right), FadeOut(capL),
                  FadeOut(capR), FadeOut(eqs), run_time=0.7)

        # the cascade: a three-lobed blob dissolves into little spheres
        blobA = revolution_arrays(tri_profile, -3.2, 3.2, n_lat=16, neck=0.55)
        blob = wireframe_from_arrays(blobA, GOLD, 1.2, 0.9)
        self.play(FadeIn(blob, run_time=0.7))
        flash = Dot(point=ORIGIN, radius=4.5, color="#ffffff")
        flash.set_opacity(0.0)
        self.add(flash)
        self.play(flash.animate.set_opacity(0.5), run_time=0.25)
        self.play(flash.animate.set_opacity(0.0), FadeOut(blob), run_time=0.4)
        centers = [-2.9, 0.0, 2.9]
        spheres = VGroup(*(
            wireframe_from_arrays(sphere_arrays([c, 0, 0], 0.85, n_lat=7,
                                                n_lon=8, n_pts=28),
                                  GOLD, 1.3)
            for c in centers
        ))
        cap2 = hud("// after finitely many cuts, only spheres remain",
                   size=22, color=GOLD)
        cap2.to_edge(DOWN, buff=0.55)
        self.add_fixed_in_frame_mobjects(cap2)
        self.play(FadeIn(spheres, lag_ratio=0.4), run_time=1.6)
        self.play(Write(cap2), run_time=0.8)
        self.play(spheres.animate.shift(UP * 0.4), run_time=1.2,
                  rate_func=there_and_back)
        self.play(FadeOut(spheres), FadeOut(cap2), run_time=0.8)


# ----------------------------------------------------------------------
# SCENE 6 - The Conjecture Becomes a Theorem
# ----------------------------------------------------------------------
class MS6Theorem(ThreeDScene):
    def construct(self):
        self.set_camera_orientation(phi=CAM_PHI, theta=CAM_THETA)

        # the constellation of resolved questions
        specs = [([-3.6, 0.7, -1.0], 0.72), ([-1.5, -0.9, 0.4], 0.9),
                 ([0.2, 0.9, -0.5], 1.05), ([2.2, -0.5, 0.3], 0.82),
                 ([4.0, 0.8, -0.9], 0.68)]
        spheres = VGroup(*(
            wireframe_from_arrays(
                sphere_arrays(c, r, n_lat=8, n_lon=9, n_pts=30),
                GOLD, 1.2, 0.9)
            for c, r in specs
        ))
        self.play(FadeIn(spheres, lag_ratio=0.35), run_time=2.2)

        thm = MathTex(
            r"M\ \text{closed, simply connected} \;\Longrightarrow\; "
            r"M \cong S^3", font_size=38, color=GOLD)
        thm.to_edge(UP, buff=0.6)
        lineage = hud("Poincaré 1904  →  Hamilton 1982  →  Perelman 2002",
                      size=24, color=PAPER)
        lineage.next_to(thm, DOWN, buff=0.3)
        prizes = hud("Millennium Prize, 2010 - declined.   "
                     "Fields Medal, 2006 - declined.", size=19, color=GHOST)
        prizes.to_edge(DOWN, buff=0.55)
        for m in (thm, lineage, prizes):
            self.add_fixed_in_frame_mobjects(m)
        self.play(Write(thm), run_time=1.8)
        self.play(FadeIn(lineage), FadeIn(prizes), run_time=1.0)
        self.play(FadeOut(thm), FadeOut(lineage), run_time=0.7)

        # one sphere remains
        others = VGroup(*(s for i, s in enumerate(spheres) if i != 2))
        hero = spheres[2]
        self.play(FadeOut(others), hero.animate.move_to(ORIGIN).scale(1.25),
                  run_time=1.4)

        # the rubber band lets go one last time
        R = 1.05 * 1.25 * 1.03

        def loop_pts(u):
            th = np.linspace(0, TAU, 60)
            return [[R * np.sin(u) * np.cos(t), R * np.sin(u) * np.sin(t),
                     R * np.cos(u)] for t in th]

        loop = glow_ring(loop_pts(PI / 2), CYAN, 2.5)
        self.play(FadeIn(loop, run_time=0.5))

        from manim import UpdateFromAlphaFunc

        def slide(m, a):
            pts = loop_pts(PI / 2 + (0.07 - PI / 2) * a)
            m[1].set_points_as_corners(pts)
            m[0].set_points_as_corners(pts)

        self.play(UpdateFromAlphaFunc(loop, slide, run_time=2.0,
                                      rate_func=smooth))
        spark = Dot(point=[0, 0, R], radius=0.3, color="#ffffff")
        spark.set_opacity(0.0)
        self.add(spark, loop)
        self.play(FadeOut(loop), spark.animate.set_opacity(0.9), run_time=0.3)
        self.play(spark.animate.set_opacity(0).scale(3), FadeOut(prizes),
                  run_time=0.6)
        self.play(FadeOut(hero), run_time=0.6)

        # the final card
        l1 = Tex("If every loop can let go,", font_size=44)
        l2 = Tex("the shape was always a sphere.", font_size=44)
        card = VGroup(l1, l2).arrange(DOWN, buff=0.3)
        card.set_color_by_gradient(GOLD, CYAN)
        eq = MathTex(r"\text{Ricci flow: } \partial_t g = -2\,\mathrm{Ric}"
                     r"\ \text{ --- melt the shape, and the truth remains.}",
                     font_size=26, color=PAPER)
        eq.next_to(card, DOWN, buff=0.5)
        for m in (card, eq):
            self.add_fixed_in_frame_mobjects(m)
        self.play(Write(card), run_time=1.6)
        self.play(Write(eq), run_time=1.2)
        self.wait(1.2)
        self.play(FadeOut(card), FadeOut(eq), run_time=1.0)
