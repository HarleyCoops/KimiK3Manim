from manim import *
import numpy as np

BG = "#0c0c0b"
TEXT = "#faf9f5"
CORAL = "#d97757"
BLUE = "#6a9bcc"
OLIVE = "#788c5d"
GOLD = "#d4a27f"
GRAY = "#b0aea5"


class CausticFootprintJourney(ThreeDScene):
    def construct(self):
        self.camera.background_color = BG
        self.caption = None
        self.active_glow = None
        self.formula_specs = self.get_formula_specs()
        self.set_camera_orientation(phi=0, theta=-90 * DEGREES, zoom=1)

        self.play_projection_opening()
        self.play_sheet_addresses()
        self.play_source_image_split()
        self.play_projection_map()
        self.play_normal_separation()
        self.play_differential_patch()
        self.play_jacobian_area()
        self.play_determinant_formula()
        self.play_zero_collapse()
        self.play_critical_curve()
        self.play_image_of_critical_curve()
        self.play_caustic_definition()
        self.play_brightness_pileup()
        self.play_rank_loss()
        self.play_final_footprint()

    def get_formula_specs(self):
        return {
            "projection_flattens_space": {
                "parts": [
                    r"\pi", ":", r"\mathbb{R}^{3}", r"\to", r"\mathbb{R}^{2}",
                    r",\quad", r"\pi(x,y,z)", "=", r"(x,y)"
                ],
                "colors": {0: BLUE, 2: OLIVE, 4: BLUE, 8: BLUE},
                "font_size": 62,
            },
            "smooth_sheet_parameterization": {
                "parts": [
                    r"\mathbf{s}", "(", "u", ",", "v", ")", "=",
                    r"(x(u,v),\,y(u,v),\,z(u,v))"
                ],
                "colors": {0: OLIVE, 2: OLIVE, 4: OLIVE, 7: OLIVE},
                "font_size": 58,
            },
            "source_and_image_coordinates": {
                "parts": [
                    r"(u,v)", r"\in", r"\Sigma", r"\quad\longmapsto\quad",
                    r"(X,Y)", r"\in", r"\Omega"
                ],
                "colors": {0: OLIVE, 2: OLIVE, 4: BLUE, 6: BLUE},
                "font_size": 60,
            },
            "projection_map": {
                "parts": [
                    "F", "(", "u", ",", "v", ")", r"=\bigl(",
                    r"X(u,v)", ",", r"Y(u,v)", r"\bigr)"
                ],
                "colors": {0: GOLD, 2: OLIVE, 4: OLIVE, 7: BLUE, 9: BLUE},
                "font_size": 60,
            },
            "nearby_points_stay_separate": {
                "parts": [
                    r"p_{1}", r"\neq", r"p_{2}", r"\quad\Longrightarrow\quad",
                    r"\text{usually}", r"F(p_{1})", r"\neq", r"F(p_{2})"
                ],
                "colors": {0: OLIVE, 2: OLIVE, 5: BLUE, 7: BLUE},
                "font_size": 54,
            },
            "differential_sends_tiny_displacements": {
                "parts": [
                    r"D F_{(u,v)}",
                    r"\begin{pmatrix} du \\ dv \end{pmatrix}",
                    "=",
                    r"\begin{pmatrix} dX \\ dY \end{pmatrix}",
                ],
                "colors": {0: GOLD, 1: OLIVE, 3: BLUE},
                "font_size": 58,
            },
            "jacobian_as_area_scale": {
                "parts": [
                    r"dA_{\mathrm{image}}", "=", r"|J(u,v)|",
                    r"dA_{\mathrm{source}}"
                ],
                "colors": {0: BLUE, 2: GOLD, 3: OLIVE},
                "font_size": 60,
            },
            "jacobian_determinant_formula": {
                "parts": [
                    r"J(u,v)", "=", r"\det",
                    r"\frac{\partial(X,Y)}{\partial(u,v)}",
                    "=",
                    r"\det\begin{pmatrix} \partial_u X & \partial_v X \\ \partial_u Y & \partial_v Y \end{pmatrix}",
                ],
                "colors": {0: GOLD, 2: GOLD, 3: BLUE, 5: GOLD},
                "font_size": 48,
                "width": 0.90,
            },
            "zero_jacobian_condition": {
                "parts": [r"J(u,v)", "=", "0"],
                "colors": {0: GOLD, 2: GOLD},
                "font_size": 86,
            },
            "critical_curve_on_sheet": {
                "parts": [
                    r"\Gamma_{\mathrm{crit}}", "=", r"\{(u,v)\in\Sigma",
                    ":", r"J(u,v)=0", r"\}"
                ],
                "colors": {0: OLIVE, 2: OLIVE, 4: GOLD},
                "font_size": 58,
            },
            "image_of_critical_curve": {
                "parts": ["F", "(", r"\Gamma_{\mathrm{crit}}", ")", r"\subset", r"\Omega"],
                "colors": {0: GOLD, 2: OLIVE, 5: BLUE},
                "font_size": 64,
            },
            "caustic_definition": {
                "parts": [r"\mathcal{K}", "=", "F", "(", r"\Gamma_{\mathrm{crit}}", ")"],
                "colors": {0: GOLD, 2: GOLD, 4: OLIVE},
                "font_size": 72,
            },
            "brightness_from_preimage_pileup": {
                "parts": [
                    r"I(X,Y)", "=", r"\sum_{(u,v):\,F(u,v)=(X,Y)}",
                    r"\frac{I_{0}(u,v)}{|J(u,v)|}",
                ],
                "colors": {0: BLUE, 2: OLIVE, 3: GOLD},
                "font_size": 48,
                "width": 0.88,
            },
            "rank_loss_condition": {
                "parts": [
                    r"\operatorname{rank}", r"D F_{(u,v)}", "<", "2",
                    r"\quad\Longleftrightarrow\quad", r"J(u,v)=0"
                ],
                "colors": {0: GOLD, 1: GOLD, 3: BLUE, 5: GOLD},
                "font_size": 58,
            },
            "caustic_as_rank_loss_footprint": {
                "parts": [
                    r"\mathcal{K}", "=", "F", r"\bigl(\{(u,v)\in",
                    r"\Sigma", ":", r"\operatorname{rank}D F_{(u,v)}<2",
                    r"\}\bigr)"
                ],
                "colors": {0: GOLD, 2: GOLD, 4: OLIVE, 6: GOLD},
                "font_size": 46,
                "width": 0.92,
            },
        }

    def top_down(self, center=ORIGIN, zoom=1, run_time=0.01):
        self.move_camera(
            phi=0,
            theta=-90 * DEGREES,
            zoom=zoom,
            frame_center=center,
            run_time=run_time,
        )

    def headline(self, text, font_size=70):
        self.clear_caption()
        self.top_down(ORIGIN, zoom=1, run_time=0.01)
        title = Text(text, font_size=font_size, color=TEXT)
        if title.width > 12:
            title.set_width(12)
        title.move_to(ORIGIN)
        self.add_fixed_in_frame_mobjects(title)
        self.play(FadeIn(title), run_time=1.0)
        self.wait(0.8)
        self.play(FadeOut(title), run_time=0.45)
        self.remove(title)
        self.wait(0.2)

    def set_caption(self, text, wait_time=0.6):
        new_caption = Text(text, font_size=30, slant=ITALIC, color=TEXT)
        if new_caption.width > 11.5:
            new_caption.set_width(11.5)
        new_caption.to_edge(DOWN, buff=0.42)
        self.add_fixed_in_frame_mobjects(new_caption)
        if self.caption is None:
            self.play(FadeIn(new_caption), run_time=0.2)
        else:
            self.play(ReplacementTransform(self.caption, new_caption), run_time=0.2)
            self.remove(self.caption)
        self.caption = new_caption
        if wait_time:
            self.wait(wait_time)

    def clear_caption(self):
        if self.caption is not None:
            self.play(FadeOut(self.caption), run_time=0.2)
            self.remove(self.caption)
            self.caption = None

    def make_formula(self, key, y=0):
        spec = self.formula_specs[key]
        formula = MathTex(*spec["parts"], color=TEXT, font_size=spec.get("font_size", 60))
        formula.move_to([0, y, 0])
        if "width" in spec and formula.width > config.frame_width * spec["width"]:
            formula.set_width(config.frame_width * spec["width"])
        formula.formula_key = key
        self.restore_formula(formula)
        return formula

    def restore_formula(self, formula):
        colors = self.formula_specs[formula.formula_key]["colors"]
        formula.set_opacity(1)
        for i, part in enumerate(formula):
            part.set_color(colors.get(i, TEXT))
            part.set_opacity(1)

    def write_formula(self, formula, run_time=1.1):
        self.top_down(formula.get_center(), zoom=1, run_time=0.01)
        anims = [FadeIn(formula[i], shift=0.05 * RIGHT) for i in range(len(formula))]
        self.play(LaggedStart(*anims, lag_ratio=0.08), run_time=run_time)
        self.add(formula)

    def make_glow(self, part, color, width=12, opacity=0.48):
        glow = part.copy()
        glow.set_color(color)
        glow.set_stroke(color=color, width=width, opacity=opacity)
        glow.set_fill(color=color, opacity=0.06)
        return glow

    def remove_glow(self):
        if self.active_glow is not None:
            self.play(FadeOut(self.active_glow), run_time=0.15)
            self.remove(self.active_glow)
            self.active_glow = None

    def highlight_part(self, formula, part_index, color, dim=0.24, width=12):
        self.remove_glow()
        self.restore_formula(formula)
        formula.set_opacity(dim)
        part = formula[part_index]
        part.set_opacity(1)
        part.set_color(color)
        self.active_glow = self.make_glow(part, color, width=width)
        self.add(self.active_glow)
        self.bring_to_front(formula)

    def tour_formula(self, formula, stops, dim=0.24):
        for part_index, zoom, color, caption, run_time in stops:
            self.highlight_part(formula, part_index, color, dim=dim)
            self.set_caption(caption, wait_time=0)
            self.move_camera(
                frame_center=formula[part_index].get_center(),
                zoom=zoom,
                phi=0,
                theta=-90 * DEGREES,
                run_time=run_time,
            )
            self.wait(0.6)
        self.remove_glow()
        self.restore_formula(formula)
        self.move_camera(
            frame_center=formula.get_center(),
            zoom=1,
            phi=0,
            theta=-90 * DEGREES,
            run_time=1.0,
        )
        self.wait(0.6)

    def fade_group(self, *mobjects, clear_caption=True):
        mobs = [m for m in mobjects if m is not None]
        if mobs:
            self.play(*[FadeOut(m) for m in mobs], run_time=0.5)
        self.remove_glow()
        if clear_caption:
            self.clear_caption()

    def sheet_point(self, u, v, lift=0.72):
        return np.array([u, v, lift + 0.33 * np.sin(1.2 * u) * np.cos(1.1 * v)])

    def folded_point(self, u, v, lift=0.72):
        return np.array([u, v, lift + 0.36 * np.tanh(1.2 * v) + 0.18 * np.sin(1.3 * u)])

    def make_smooth_sheet(self):
        surface = Surface(
            lambda u, v: self.sheet_point(u, v),
            u_range=[-3, 3],
            v_range=[-2, 2],
            resolution=(18, 12),
        )
        surface.set_style(
            fill_color=OLIVE,
            fill_opacity=0.22,
            stroke_color=OLIVE,
            stroke_opacity=0.25,
            stroke_width=0.5,
        )

        grid_u = VGroup()
        for u in np.linspace(-2.7, 2.7, 7):
            curve = ParametricFunction(
                lambda t, u=u: self.sheet_point(u, t) + np.array([0, 0, 0.015]),
                t_range=[-1.85, 1.85],
                color=OLIVE,
                stroke_width=1.3,
            )
            grid_u.add(curve)

        grid_v = VGroup()
        for v in np.linspace(-1.8, 1.8, 7):
            curve = ParametricFunction(
                lambda t, v=v: self.sheet_point(t, v) + np.array([0, 0, 0.018]),
                t_range=[-2.85, 2.85],
                color=GRAY,
                stroke_width=1.0,
                stroke_opacity=0.85,
            )
            grid_v.add(curve)

        return Group(surface, grid_u, grid_v)

    def make_split_domain(self):
        left_outline = RoundedRectangle(
            width=3.3,
            height=2.25,
            corner_radius=0.18,
            color=OLIVE,
            fill_color=OLIVE,
            fill_opacity=0.10,
            stroke_width=2,
        ).move_to(LEFT * 3.2)

        left_grid = VGroup()
        for x in np.linspace(-4.45, -1.95, 5):
            left_grid.add(Line([x, -1.0, 0], [x, 1.0, 0], color=OLIVE, stroke_width=0.8, stroke_opacity=0.45))
        for y in np.linspace(-0.75, 0.75, 4):
            left_grid.add(Line([-4.65, y, 0], [-1.75, y, 0], color=GRAY, stroke_width=0.7, stroke_opacity=0.38))

        right_plane = Rectangle(
            width=3.3,
            height=2.25,
            color=BLUE,
            fill_color=BLUE,
            fill_opacity=0.10,
            stroke_width=2,
        ).move_to(RIGHT * 3.2)

        axes = VGroup(
            Line(RIGHT * 1.85, RIGHT * 4.55, color=BLUE, stroke_width=1, stroke_opacity=0.55),
            Line(RIGHT * 3.2 + DOWN, RIGHT * 3.2 + UP, color=BLUE, stroke_width=1, stroke_opacity=0.55),
        )

        sigma = MathTex(r"\Sigma", color=OLIVE, font_size=44).next_to(left_outline, UP, buff=0.2)
        omega = MathTex(r"\Omega", color=BLUE, font_size=44).next_to(right_plane, UP, buff=0.2)
        return VGroup(left_outline, left_grid, right_plane, axes, sigma, omega)

    def make_point_projection(self):
        src = Dot(LEFT * 3.2 + UP * 0.35, color=OLIVE, radius=0.08)
        dst = Dot(RIGHT * 3.2 + DOWN * 0.15, color=BLUE, radius=0.08)
        path = Line(src.get_center(), dst.get_center(), color=GOLD, stroke_width=3)
        traveling = Dot(src.get_center(), color=OLIVE, radius=0.07)
        group = VGroup(path, src, dst, traveling)
        return group, traveling, path, dst

    def make_nearby_points_piece(self):
        sources = [LEFT * 3.2 + UP * 1.75 + RIGHT * dx for dx in [-0.22, 0.22]]
        images = [RIGHT * 3.0 + UP * 1.48 + RIGHT * dx for dx in [-0.35, 0.35]]
        src_dots = VGroup(*[Dot(p, color=OLIVE, radius=0.065) for p in sources])
        img_dots = VGroup(*[Dot(p, color=BLUE, radius=0.065) for p in images])
        paths = VGroup(*[Line(s, e, color=GOLD, stroke_width=2, stroke_opacity=0.65) for s, e in zip(sources, images)])
        source_patch = RoundedRectangle(width=1.1, height=0.55, corner_radius=0.12, color=OLIVE, stroke_width=1.4)
        source_patch.move_to(LEFT * 3.2 + UP * 1.75)
        image_patch = RoundedRectangle(width=1.3, height=0.55, corner_radius=0.12, color=BLUE, stroke_width=1.4)
        image_patch.move_to(RIGHT * 3.0 + UP * 1.48)
        return VGroup(source_patch, image_patch, paths, src_dots, img_dots)

    def make_patch_piece(self):
        source = Polygon(
            [-1.25, -0.45, 0.85],
            [-0.55, -0.45, 0.95],
            [-0.55, 0.25, 0.90],
            [-1.25, 0.25, 0.78],
            color=OLIVE,
            fill_color=OLIVE,
            fill_opacity=0.24,
            stroke_width=3,
        )
        image = Polygon(
            [0.35, -0.65, -0.65],
            [1.45, -0.42, -0.65],
            [1.25, 0.18, -0.65],
            [0.18, -0.08, -0.65],
            color=BLUE,
            fill_color=BLUE,
            fill_opacity=0.24,
            stroke_width=3,
        )
        lines = VGroup()
        for s, e in zip(source.get_vertices(), image.get_vertices()):
            lines.add(Line(s, e, color=GOLD, stroke_width=1.6, stroke_opacity=0.65))
        return VGroup(source, image, lines).scale(1.35)

    def make_area_piece(self):
        source = Square(side_length=0.78, color=OLIVE, fill_color=OLIVE, fill_opacity=0.18, stroke_width=2.2)
        source.move_to(LEFT * 2.65 + UP * 1.55)
        image = Polygon(
            RIGHT * 1.8 + UP * 1.22,
            RIGHT * 2.95 + UP * 1.38,
            RIGHT * 3.18 + UP * 1.95,
            RIGHT * 2.02 + UP * 1.78,
            color=BLUE,
            fill_color=BLUE,
            fill_opacity=0.18,
            stroke_width=2.2,
        )
        arrow = Line(source.get_right() + RIGHT * 0.25, image.get_left() + LEFT * 0.25, color=GOLD, stroke_width=3)
        dial = Arc(radius=0.42, start_angle=210 * DEGREES, angle=115 * DEGREES, color=GOLD, stroke_width=3)
        dial.move_to(UP * 1.57)
        needle = Line(dial.get_center(), dial.get_center() + 0.38 * (0.35 * RIGHT + 0.94 * UP), color=GOLD, stroke_width=3)
        label = MathTex("J", color=GOLD, font_size=34).next_to(dial, DOWN, buff=0.05)
        return VGroup(source, image, arrow, dial, needle, label)

    def make_collapse_piece(self):
        patch = Polygon(
            [-1.25, -0.55, 0.78],
            [-0.35, -0.35, 0.92],
            [-0.50, 0.42, 0.82],
            [-1.40, 0.18, 0.72],
            color=OLIVE,
            fill_color=OLIVE,
            fill_opacity=0.25,
            stroke_width=3,
        )
        line = Line([0.25, -0.12, -0.65], [1.75, 0.08, -0.65], color=GOLD, stroke_width=9)
        glow = line.copy().set_stroke(GOLD, width=18, opacity=0.28)
        guides = VGroup()
        target_points = [line.point_from_proportion(t) for t in [0.15, 0.38, 0.62, 0.85]]
        for s, e in zip(patch.get_vertices(), target_points):
            guides.add(Line(s, e, color=GOLD, stroke_width=1.8, stroke_opacity=0.55))
        return VGroup(patch, glow, line, guides).scale(1.35)

    def make_critical_sheet(self):
        surface = Surface(
            lambda u, v: self.folded_point(u, v),
            u_range=[-3, 3],
            v_range=[-1.75, 1.75],
            resolution=(18, 12),
        )
        surface.set_style(
            fill_color=OLIVE,
            fill_opacity=0.20,
            stroke_color=OLIVE,
            stroke_opacity=0.24,
            stroke_width=0.5,
        )
        curve = ParametricFunction(
            lambda t: self.folded_point(t, 0.18 * np.sin(1.3 * t)) + np.array([0, 0, 0.035]),
            t_range=[-2.65, 2.65],
            color=GOLD,
            stroke_width=9,
        )
        glow = curve.copy().set_stroke(GOLD, width=18, opacity=0.25)
        return Group(surface, glow, curve)

    def make_projected_critical_piece(self):
        plane = Rectangle(
            width=6.2,
            height=3.5,
            color=BLUE,
            fill_color=BLUE,
            fill_opacity=0.10,
            stroke_width=1.6,
        ).move_to([0, 0, -0.7])

        source_curve = ParametricFunction(
            lambda t: np.array([t, 0.38 * np.sin(1.25 * t), 0.85 + 0.25 * np.cos(1.1 * t)]),
            t_range=[-2.65, 2.65],
            color=OLIVE,
            stroke_width=7,
        )
        image_curve = ParametricFunction(
            lambda t: np.array([t, 0.38 * np.sin(1.25 * t), -0.68]),
            t_range=[-2.65, 2.65],
            color=GOLD,
            stroke_width=9,
        )
        image_glow = image_curve.copy().set_stroke(GOLD, width=18, opacity=0.25)

        rays = VGroup()
        for t in np.linspace(-2.4, 2.4, 9):
            start = np.array([t, 0.38 * np.sin(1.25 * t), 0.85 + 0.25 * np.cos(1.1 * t)])
            end = np.array([t, 0.38 * np.sin(1.25 * t), -0.68])
            rays.add(Line(start, end, color=GOLD, stroke_width=1.4, stroke_opacity=0.55))
        return Group(plane, rays, source_curve, image_glow, image_curve)

    def make_caustic_trace_label(self):
        trace = ParametricFunction(
            lambda t: np.array([1.0 * np.sin(t), 0.42 * np.sin(2 * t), 0]),
            t_range=[-PI, PI],
            color=GOLD,
            stroke_width=8,
        ).scale(0.95).shift(UP * 1.25)
        glow = trace.copy().set_stroke(GOLD, width=17, opacity=0.24)
        label = MathTex(r"\mathcal{K}", color=GOLD, font_size=48).next_to(trace, RIGHT, buff=0.25)
        return VGroup(glow, trace, label)

    def make_brightness_piece(self):
        image_point = Dot(RIGHT * 2.6 + UP * 1.48, color=BLUE, radius=0.10)
        source_positions = [
            LEFT * 3.0 + UP * 1.85,
            LEFT * 2.55 + UP * 1.48,
            LEFT * 3.25 + UP * 1.20,
            LEFT * 2.80 + UP * 2.15,
            LEFT * 3.48 + UP * 1.62,
        ]
        dots = VGroup(*[Dot(p, color=OLIVE, radius=0.058) for p in source_positions])
        paths = VGroup(*[Line(p, image_point.get_center(), color=GOLD, stroke_width=1.8, stroke_opacity=0.72) for p in source_positions])
        ridge = Line(RIGHT * 2.15 + UP * 1.25, RIGHT * 3.05 + UP * 1.72, color=GOLD, stroke_width=7)
        glow = ridge.copy().set_stroke(GOLD, width=18, opacity=0.26)
        return VGroup(paths, dots, glow, ridge, image_point)

    def play_projection_opening(self):
        self.headline("Looking can erase depth.", 76)
        formula = self.make_formula("projection_flattens_space")
        self.write_formula(formula)
        self.set_caption("Projection is a rule sending source points to observed points.")
        self.tour_formula(
            formula,
            [
                (0, 2.25, BLUE, "Pi names the flattening view.", 1.4),
                (2, 2.35, OLIVE, "The source begins in three dimensions.", 1.5),
                (4, 2.25, BLUE, "The observed image lives on a plane.", 1.4),
            ],
        )
        self.fade_group(formula)

    def play_sheet_addresses(self):
        self.headline("A curved sheet still has two addresses.", 70)
        sheet = self.make_smooth_sheet()
        self.play(FadeIn(sheet[0]), run_time=0.8)
        self.move_camera(phi=60 * DEGREES, theta=-45 * DEGREES, zoom=1, frame_center=ORIGIN, run_time=1.4)
        self.play(LaggedStart(Create(sheet[1]), Create(sheet[2]), lag_ratio=0.25), run_time=1.0)
        self.set_caption("The sheet bends, but its address grid stays smooth.")
        self.move_camera(phi=60 * DEGREES, theta=-41 * DEGREES, zoom=1, frame_center=ORIGIN, run_time=1.2)
        self.wait(0.6)
        self.move_camera(phi=0, theta=-90 * DEGREES, zoom=1, frame_center=ORIGIN, run_time=1.0)
        self.play(FadeOut(sheet), run_time=0.5)
        self.clear_caption()

        formula = self.make_formula("smooth_sheet_parameterization")
        self.write_formula(formula)
        self.set_caption("Two source addresses name each point on the curved sheet.")
        self.tour_formula(
            formula,
            [
                (0, 2.25, OLIVE, "s turns addresses into spatial points.", 1.4),
                (2, 2.2, OLIVE, "u moves along one grid family.", 1.3),
                (4, 2.2, OLIVE, "v moves along the crossing family.", 1.3),
            ],
        )
        self.fade_group(formula)

    def play_source_image_split(self):
        self.headline("Do not confuse the source with the image.", 70)
        split = self.make_split_domain()
        self.play(FadeIn(split), run_time=1.0)

        formula = self.make_formula("source_and_image_coordinates", y=-0.35)
        self.write_formula(formula)
        self.set_caption("Sheet addresses and image coordinates live in different spaces.")
        self.tour_formula(
            formula,
            [
                (0, 2.25, OLIVE, "u and v name a source position.", 1.3),
                (2, 2.35, OLIVE, "Sigma is the upstairs source sheet.", 1.4),
                (4, 2.25, BLUE, "X,Y name the observed landing point.", 1.3),
                (6, 2.35, BLUE, "Omega is the downstairs image plane.", 1.4),
            ],
        )
        self.fade_group(split, formula)

    def play_projection_map(self):
        self.headline("The map tells where each source point lands.", 68)
        formula = self.make_formula("projection_map")
        self.write_formula(formula)
        self.set_caption("F sends a sheet address to its observed landing point.")
        self.tour_formula(
            formula,
            [
                (0, 2.5, GOLD, "F is the active projection rule.", 1.5),
                (7, 2.25, BLUE, "X is the observed horizontal landing coordinate.", 1.3),
                (9, 2.25, BLUE, "Y is the observed vertical landing coordinate.", 1.3),
            ],
        )

        projection, traveler, path, dst = self.make_point_projection()
        formula.generate_target()
        formula.target.scale(0.72).to_edge(UP, buff=0.55).set_opacity(0.32)
        self.play(MoveToTarget(formula), FadeIn(projection[:-1]), run_time=0.8)
        self.play(MoveAlongPath(traveler, path), run_time=1.1)
        self.play(traveler.animate.set_color(BLUE).move_to(dst.get_center()), run_time=0.4)
        self.wait(0.6)
        self.fade_group(formula, projection)

    def play_normal_separation(self):
        self.headline("Normally, nearby source points stay separate.", 68)
        visual = self.make_nearby_points_piece()
        formula = self.make_formula("nearby_points_stay_separate", y=-0.75)
        self.play(FadeIn(visual), run_time=0.7)
        self.write_formula(formula)
        self.set_caption("Nearby, a healthy projection keeps distinct points distinct.")
        self.tour_formula(
            formula,
            [
                (5, 2.35, BLUE, "F(p1) is one observed landing point.", 1.4),
                (7, 2.35, BLUE, "F(p2) remains a separate landing point.", 1.4),
            ],
        )
        self.fade_group(visual, formula)

    def play_differential_patch(self):
        self.headline("Up close, the map acts on tiny motions.", 68)
        patch = self.make_patch_piece()
        self.play(FadeIn(patch), run_time=0.8)
        self.move_camera(phi=58 * DEGREES, theta=-42 * DEGREES, zoom=1.05, frame_center=ORIGIN, run_time=1.3)
        self.wait(0.6)
        self.move_camera(phi=58 * DEGREES, theta=-39 * DEGREES, zoom=1.05, frame_center=ORIGIN, run_time=1.0)
        self.move_camera(phi=0, theta=-90 * DEGREES, zoom=1, frame_center=ORIGIN, run_time=1.0)
        self.play(FadeOut(patch), run_time=0.5)

        formula = self.make_formula("differential_sends_tiny_displacements")
        self.write_formula(formula)
        self.set_caption("DF turns a tiny source motion into a tiny image motion.")
        self.tour_formula(
            formula,
            [
                (0, 2.5, GOLD, "DF is F seen close-up.", 1.5),
                (1, 2.35, OLIVE, "du,dv is the tiny source step.", 1.3),
                (3, 2.35, BLUE, "dX,dY is the tiny image step.", 1.3),
            ],
        )
        self.fade_group(formula)

    def play_jacobian_area(self):
        self.headline("The Jacobian is the local area dial.", 70)
        visual = self.make_area_piece()
        formula = self.make_formula("jacobian_as_area_scale", y=-0.75)
        self.play(FadeIn(visual), run_time=0.7)
        self.write_formula(formula)
        self.set_caption("J measures spread: large footprint or collapsed footprint.")
        self.tour_formula(
            formula,
            [
                (0, 2.3, BLUE, "This is the observed footprint area.", 1.3),
                (2, 2.55, GOLD, "J is the local area multiplier.", 1.5),
                (3, 2.3, OLIVE, "This is the original patch area.", 1.3),
            ],
        )
        self.fade_group(visual, formula)

    def play_determinant_formula(self):
        self.headline("The area dial has a coordinate test.", 70)
        formula = self.make_formula("jacobian_determinant_formula")
        self.write_formula(formula, run_time=1.2)
        self.set_caption("The determinant computes the tiny footprint area scale.")
        self.tour_formula(
            formula,
            [
                (0, 2.25, GOLD, "J records area scale at this address.", 1.3),
                (2, 2.35, GOLD, "det is the area test.", 1.4),
                (3, 2.2, BLUE, "This compares image coordinates to source addresses.", 1.4),
                (5, 2.35, GOLD, "The matrix records all tiny coordinate changes.", 1.5),
            ],
            dim=0.22,
        )
        self.fade_group(formula)

    def play_zero_collapse(self):
        self.headline("The decisive event is zero area.", 76)
        collapse = self.make_collapse_piece()
        self.play(FadeIn(collapse), run_time=0.8)
        self.move_camera(phi=62 * DEGREES, theta=-42 * DEGREES, zoom=1.05, frame_center=ORIGIN, run_time=1.5)
        self.set_caption("The footprint still appears, but its area vanishes.")
        self.move_camera(phi=62 * DEGREES, theta=-38.8 * DEGREES, zoom=1.05, frame_center=collapse.get_center(), run_time=1.4)
        self.wait(0.6)
        self.move_camera(phi=0, theta=-90 * DEGREES, zoom=1, frame_center=ORIGIN, run_time=1.0)
        self.play(FadeOut(collapse), run_time=0.5)
        self.clear_caption()

        formula = self.make_formula("zero_jacobian_condition")
        self.write_formula(formula, run_time=1.0)
        zero_glow = self.make_glow(formula[2], GOLD, width=18, opacity=0.35)
        self.add(zero_glow)
        self.bring_to_front(formula)
        self.play(FadeIn(zero_glow), run_time=0.25)
        self.set_caption("Zero area means collapse, not disappearance.")

        self.set_caption("J is the area dial being tested.", wait_time=0.4)
        self.highlight_part(formula, 0, GOLD, dim=0.22, width=14)
        self.move_camera(
            frame_center=formula[0].get_center(),
            zoom=2.4,
            phi=0,
            theta=-90 * DEGREES,
            run_time=1.5,
        )
        self.wait(0.6)
        self.remove_glow()
        self.restore_formula(formula)
        self.move_camera(
            frame_center=formula.get_center(),
            zoom=1,
            phi=0,
            theta=-90 * DEGREES,
            run_time=1.0,
        )
        self.wait(0.6)

        self.set_caption("Exactly zero marks the collapse threshold.", wait_time=0.4)
        self.highlight_part(formula, 2, GOLD, dim=0.16, width=20)
        self.move_camera(
            frame_center=formula[2].get_center(),
            zoom=3.0,
            phi=0,
            theta=-90 * DEGREES,
            run_time=3.2,
        )
        self.wait(1.6)
        self.remove_glow()
        self.restore_formula(formula)
        self.move_camera(
            frame_center=formula.get_center(),
            zoom=1,
            phi=0,
            theta=-90 * DEGREES,
            run_time=1.4,
        )
        self.wait(0.6)
        self.remove(zero_glow)
        self.fade_group(formula)

    def play_critical_curve(self):
        self.headline("The zero set forms a hidden curve.", 70)
        sheet = self.make_critical_sheet()
        self.play(FadeIn(sheet), run_time=0.8)
        self.move_camera(phi=60 * DEGREES, theta=-45 * DEGREES, zoom=1.05, frame_center=ORIGIN, run_time=1.3)
        self.set_caption("The failing places live upstream on the sheet.")
        self.move_camera(phi=60 * DEGREES, theta=-42.1 * DEGREES, zoom=1.05, frame_center=ORIGIN, run_time=1.0)
        self.wait(0.6)
        self.move_camera(phi=0, theta=-90 * DEGREES, zoom=1, frame_center=ORIGIN, run_time=1.0)
        self.play(FadeOut(sheet), run_time=0.5)
        self.clear_caption()

        formula = self.make_formula("critical_curve_on_sheet")
        self.write_formula(formula)
        self.set_caption("The critical curve selects sheet addresses where J is zero.")
        self.tour_formula(
            formula,
            [
                (0, 2.5, OLIVE, "Gamma crit is the hidden failing curve.", 1.5),
                (2, 2.25, OLIVE, "These are selected source-sheet addresses.", 1.3),
                (4, 2.45, GOLD, "J equals zero is the selection rule.", 1.5),
            ],
        )
        self.fade_group(formula)

    def play_image_of_critical_curve(self):
        self.headline("Projection carries that hidden curve into view.", 68)
        piece = self.make_projected_critical_piece()
        self.play(FadeIn(piece), run_time=0.8)
        self.move_camera(phi=60 * DEGREES, theta=-40 * DEGREES, zoom=1.05, frame_center=ORIGIN, run_time=1.4)
        self.set_caption("Every visible trace point comes from the hidden curve.")
        self.move_camera(phi=60 * DEGREES, theta=-36.8 * DEGREES, zoom=1.05, frame_center=ORIGIN, run_time=1.1)
        self.wait(0.6)
        self.move_camera(phi=0, theta=-90 * DEGREES, zoom=1, frame_center=ORIGIN, run_time=1.0)
        self.play(FadeOut(piece), run_time=0.5)
        self.clear_caption()

        formula = self.make_formula("image_of_critical_curve")
        self.write_formula(formula, run_time=1.0)
        self.set_caption("The projected critical curve lies on the observation plane.")
        self.tour_formula(
            formula,
            [
                (0, 2.45, GOLD, "F carries the hidden curve downward.", 1.4),
                (2, 2.4, OLIVE, "Gamma crit is the source curve.", 1.4),
                (5, 2.3, BLUE, "Omega is the observation plane.", 1.3),
            ],
        )
        self.fade_group(formula)

    def play_caustic_definition(self):
        self.headline("The visible image curve is the caustic.", 72)
        formula = self.make_formula("caustic_definition")
        self.write_formula(formula)
        self.set_caption("A caustic is the image of the critical curve.")

        trace = self.make_caustic_trace_label()
        self.play(FadeIn(trace), run_time=1.2)
        self.wait(0.6)

        self.tour_formula(
            formula,
            [
                (0, 2.55, GOLD, "K names the visible caustic.", 1.5),
                (2, 2.35, GOLD, "F performs the projection.", 1.3),
                (4, 2.45, OLIVE, "Gamma crit is the upstream failure curve.", 1.5),
            ],
            dim=0.23,
        )
        self.fade_group(trace, formula)

    def play_brightness_pileup(self):
        self.headline("Brightness rises because source points pile up.", 68)
        visual = self.make_brightness_piece()
        formula = self.make_formula("brightness_from_preimage_pileup", y=-0.82)
        self.play(FadeIn(visual), run_time=0.8)
        self.write_formula(formula, run_time=1.3)
        self.set_caption("Light is concentrated, not created.")
        self.tour_formula(
            formula,
            [
                (0, 2.35, BLUE, "I is brightness at an image point.", 1.4),
                (2, 2.2, OLIVE, "The sum gathers all source addresses landing there.", 1.5),
                (3, 2.45, GOLD, "Small J makes each contribution large.", 1.6),
            ],
            dim=0.22,
        )
        self.fade_group(visual, formula)

    def play_rank_loss(self):
        self.headline("Rank counts surviving local directions.", 70)
        formula = self.make_formula("rank_loss_condition")
        self.write_formula(formula, run_time=1.2)
        self.set_caption("Rank loss and zero Jacobian describe the same collapse.")
        self.tour_formula(
            formula,
            [
                (0, 2.35, GOLD, "Rank counts surviving image directions.", 1.4),
                (1, 2.4, GOLD, "DF is the local projection machine.", 1.4),
                (3, 2.25, BLUE, "Two is full sheet-to-plane rank.", 1.3),
                (5, 2.45, GOLD, "J equals zero is the area version.", 1.5),
            ],
            dim=0.22,
        )
        self.fade_group(formula)

    def play_final_footprint(self):
        self.headline("The whole story is one footprint.", 72)
        formula = self.make_formula("caustic_as_rank_loss_footprint")
        self.write_formula(formula, run_time=1.3)
        self.set_caption("The caustic is the visible footprint of rank loss.")
        self.tour_formula(
            formula,
            [
                (0, 2.45, GOLD, "K is the visible footprint.", 1.5),
                (2, 2.3, GOLD, "F projects the rank-loss set.", 1.4),
                (4, 2.15, OLIVE, "The hidden set lives on Sigma.", 1.5),
                (6, 2.5, GOLD, "Rank below two means one direction collapsed.", 1.6),
            ],
            dim=0.20,
        )
        self.move_camera(
            frame_center=formula.get_center(),
            zoom=1,
            phi=0,
            theta=-90 * DEGREES,
            run_time=1.4,
        )
        self.wait(1.4)
