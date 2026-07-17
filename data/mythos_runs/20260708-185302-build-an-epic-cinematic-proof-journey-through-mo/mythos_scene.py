from manim import *
import numpy as np


class EvidenceToFieldsJourney(ThreeDScene):
    BG = "#0c0c0b"
    TEXT = "#faf9f5"
    MATTER = "#d97757"
    LIGHT = "#6a9bcc"
    STRUCTURE = "#788c5d"
    INTERACTION = "#d4a27f"
    SECONDARY = "#b0aea5"

    def construct(self):
        self.camera.background_color = self.BG
        self.current_caption = None
        self.current_glow = None
        self.live = VGroup()
        self.set_camera_orientation(phi=0, theta=-90 * DEGREES, zoom=1)

        self.headline("Physics first gives motion a push.", 72)
        self.wait(0.8)
        f = self.show_formula("newton_second_law_anchor")
        self.caption("Force changes motion; it does not explain steady motion.")
        self.wait(1.0)
        self.clear_all()

        self.headline("Mass and energy are two accounts of one content.", 72)
        f = self.show_formula("mass_energy_anchor")
        self.caption("Mass and energy are two accounts of conserved content.")
        self.wait(1.2)
        self.clear_all()

        self.headline("Newton's gravity nearly carries the sky.", 74)
        f = self.show_formula("newton_inverse_square_gravity")
        self.caption("Gravity weakens by the square of distance.")
        self.wait(0.9)
        self.term_tour(f, 5, "Farther apart means weaker by a squared rule.", 2.6, self.STRUCTURE, 0.25, 2.2)
        self.pull_back(f, 1.2)
        self.caption("One distance rule organizes apples and planets.")
        self.wait(0.7)
        self.distance_set_piece(f)
        self.clear_all()

        self.headline("A tiny leftover refuses to go away.", 74)
        f = self.show_formula("mercury_residual")
        self.caption("Mercury's tiny leftover repeats for a century.")
        self.term_tour(f, 4, "Tiny is not ignorable when it keeps returning.", 2.8, self.INTERACTION, 0.22, 2.5)
        self.pull_back(f, 1.3)
        self.caption("The mismatch is small, precise, and stubborn.")
        self.wait(0.8)
        self.clear_all()

        self.headline("Curved spacetime predicts the missing advance.", 72)
        f = self.show_formula("relativistic_perihelion_correction")
        self.caption("Relativity supplies the missing orbit advance.")
        self.term_tour(f, 6, "Light speed in the denominator marks relativity.", 2.5, self.LIGHT, 0.25, 2.0)
        self.pull_back(f, 1.2)
        self.caption("This is not a patch; it comes from geometry.")
        self.wait(1.1)
        self.clear_all()

        self.headline("An event has a time-place address.", 74)
        f = self.show_formula("event_coordinates")
        self.caption("An event is one address in spacetime.")
        self.term_tour(f, 2, "Time is measured in light-travel distance here.", 2.4, self.LIGHT, 0.25, 2.0)
        self.pull_back(f, 1.1)
        self.caption("Space and time are linked, not identical.")
        self.wait(0.8)
        self.clear_all()

        self.headline("Spacetime measures separations with a special ruler.", 68)
        f = self.show_formula("flat_spacetime_interval")
        self.caption("All observers agree on this spacetime separation.")
        self.term_tour(f, 2, "Time contributes differently from space.", 2.6, self.LIGHT, 0.25, 2.1)
        self.pull_back(f, 1.1)
        self.caption("This is the flat ruler before gravity curves it.")
        self.wait(1.0)
        self.clear_all()

        self.headline("Gravity changes the ruler itself.", 74)
        grid = self.metric_grid()
        self.add(grid)
        self.live.add(grid)
        f = self.show_formula("metric_interval")
        self.caption("The metric is spacetime's local measuring rule.")
        self.term_tour(f, 2, "The ruler itself decides length, time, and straightness.", 2.7, self.STRUCTURE, 0.22, 2.3)
        self.pull_back(f, 1.2)
        self.caption("The flat ruler can now vary from place to place.")
        self.metric_set_piece(f)
        self.clear_all()

        self.headline("Free fall follows the straightest curved path.", 70)
        f = self.show_formula("geodesic_equation")
        self.caption("Free fall follows geometry, not an unseen push.")
        self.term_tour(f, 2, "Gamma tells the path how local directions steer.", 2.6, self.INTERACTION, 0.22, 2.2)
        self.pull_back(f, 1.2)
        self.term_tour(f, 6, "Zero means free motion needs no extra push.", 2.35, self.STRUCTURE, 0.25, 1.8)
        self.pull_back(f, 1.1)
        self.caption("The path is straight by the curved rule.")
        self.wait(1.1)
        self.clear_all()

        self.headline("Matter and geometry must agree locally.", 72)
        f = self.show_formula("einstein_field_equation_texture")
        self.caption("Curvature and stress-energy must balance locally.")
        self.curvature_set_piece(f)
        self.clear_all()

        self.headline("Now we ask where the steering lives.", 74)
        f = self.show_formula("geodesic_gamma_focus")
        self.caption("The whole equation still describes free motion.")
        self.caption("Gamma is the local steering rule.")
        self.big_gamma_zoom(f)
        self.pull_back(f, 1.6)
        self.caption("The steering term belongs to the whole path.")
        self.wait(0.8)
        self.clear_all()

        self.headline("Gamma is built from the changing metric.", 72)
        f = self.show_formula("christoffel_connection_from_metric")
        self.caption("The connection is built from the metric.")
        self.term_tour(f, 0, "Gamma names the steering rule to be explained.", 2.5, self.INTERACTION, 0.24, 2.0)
        self.pull_back(f, 1.1)
        self.term_tour(f, 4, "Metric changes create the local steering instructions.", 2.7, self.STRUCTURE, 0.22, 2.4)
        self.pull_back(f, 1.2)
        self.caption("The changing ruler becomes path guidance.")
        self.wait(1.2)
        self.clear_all()

        self.headline("A repeated mismatch can rewrite the stage.", 72)
        f = self.show_formula("evidence_crisis_structure_pattern")
        self.caption("A mismatch can force a deeper rule.")
        self.term_tour(f, 4, "The new rule keeps the old successes.", 2.1, self.STRUCTURE, 0.35, 1.8)
        self.pull_back(f, 1.0)
        self.wait(1.0)
        self.clear_all()

        self.headline("Quantum alternatives interfere before probabilities appear.", 68)
        slit = self.double_slit_set_piece()
        self.add(slit)
        self.live.add(slit)
        self.play(FadeIn(slit), run_time=1.1)
        f = self.show_formula("double_slit_probability_with_interference", position=DOWN * 2.05)
        self.caption("Detections form probabilities with interference.")
        self.term_tour(f, 6, "The cross term makes bright and dark bands.", 2.8, self.LIGHT, 0.20, 2.6)
        self.pull_back(f, 1.3, center=ORIGIN)
        self.caption("Quantum paths combine before probabilities are counted.")
        self.wait(1.2)
        self.clear_all()

        self.headline("Quantum motion is wave evolution.", 74)
        f = self.show_formula("schrodinger_wave_milestone")
        self.caption("Quantum waves evolve by an energy rule.")
        self.wait(1.0)
        self.clear_all()

        self.headline("Relativity turns matter into fields.", 74)
        f = self.show_formula("dirac_relativistic_field_milestone")
        self.caption("Relativistic matter balances spacetime change against mass.")
        self.wait(1.0)
        self.clear_all()

        self.headline("A particle is a stable field excitation.", 72)
        f = self.show_formula("one_particle_as_field_excitation")
        self.caption("One field quantum appears from the vacuum.")
        self.term_tour(f, 0, "The creation operator makes a one-particle state.", 2.6, self.MATTER, 0.24, 2.1)
        self.pull_back(f, 1.1)
        self.caption("Particles are quantized excitations, not hidden beads.")
        self.wait(1.1)
        self.clear_all()

        self.headline("QED makes interaction local.", 74)
        f = self.show_formula("qed_interaction_lagrangian")
        self.caption("QED couples charged matter to the light field.")
        self.term_tour(f, 2, "Charge sets how strongly the fields meet.", 2.4, self.INTERACTION, 0.25, 1.8)
        self.pull_back(f, 1.0)
        self.term_tour(f, 3, "The matter current becomes a local source.", 2.5, self.MATTER, 0.25, 2.0)
        self.pull_back(f, 1.0)
        self.term_tour(f, 4, "The light field meets the charged matter.", 2.5, self.LIGHT, 0.25, 2.0)
        self.pull_back(f, 1.1)
        self.caption("The vertex is a local field interaction.")
        self.wait(0.8)
        self.clear_all()

        self.headline("One pure number sets the strength.", 74)
        f = self.show_formula("fine_structure_constant")
        self.caption("Alpha is electromagnetic strength without units.")
        self.term_tour(f, 0, "Alpha is electromagnetic strength without units.", 2.6, self.INTERACTION, 0.24, 2.1)
        self.pull_back(f, 1.1)
        self.term_tour(f, 4, "Alpha is small, but not exactly one over 137.", 2.7, self.INTERACTION, 0.22, 2.4)
        self.pull_back(f, 1.2)
        self.caption("The small coupling makes QED delicate and precise.")
        self.wait(1.3)
        self.clear_all()

        self.headline("The equations changed because the evidence demanded it.", 70)
        self.move_camera(phi=0, theta=-90 * DEGREES, zoom=1, frame_center=ORIGIN, run_time=0.1)
        self.wait(1.2)

    def wrap_headline(self, text, max_chars=38):
        words = text.split()
        lines = []
        line = ""
        for word in words:
            candidate = word if not line else line + " " + word
            if len(candidate) <= max_chars:
                line = candidate
            else:
                lines.append(line)
                line = word
        if line:
            lines.append(line)
        return "\n".join(lines)

    def headline(self, text, font_size=72):
        self.move_camera(phi=0, theta=-90 * DEGREES, zoom=1, frame_center=ORIGIN, run_time=0.1)
        headline = Text(
            self.wrap_headline(text),
            font_size=font_size,
            color=self.TEXT,
            line_spacing=0.9,
        )
        headline.move_to(ORIGIN)
        self.add_fixed_in_frame_mobjects(headline)
        self.play(FadeIn(headline), run_time=0.45)
        self.wait(0.95)
        self.play(FadeOut(headline), run_time=0.45)
        self.remove(headline)

    def caption(self, text):
        if self.current_caption is not None:
            self.play(FadeOut(self.current_caption), run_time=0.18)
            self.remove(self.current_caption)
        caption = Text(
            text,
            font_size=30,
            color=self.SECONDARY,
            slant=ITALIC,
        )
        caption.to_edge(DOWN, buff=0.45)
        if caption.width > config.frame_width - 1.0:
            caption.scale_to_fit_width(config.frame_width - 1.0)
        self.add_fixed_in_frame_mobjects(caption)
        self.play(FadeIn(caption), run_time=0.28)
        self.current_caption = caption

    def clear_all(self, run_time=0.55):
        mobs = list(self.live)
        if self.current_glow is not None:
            mobs.append(self.current_glow)
        if self.current_caption is not None:
            mobs.append(self.current_caption)
        if mobs:
            self.play(*[FadeOut(m) for m in mobs], run_time=run_time)
            self.remove(*mobs)
        self.live = VGroup()
        self.current_glow = None
        self.current_caption = None
        self.move_camera(phi=0, theta=-90 * DEGREES, zoom=1, frame_center=ORIGIN, run_time=0.1)

    def show_formula(self, key, position=ORIGIN, run_time=1.15):
        formula = self.make_formula(key)
        formula.move_to(position)
        formula.set_z_index(5)
        if formula.width > config.frame_width - 1.2:
            formula.scale_to_fit_width(config.frame_width - 1.2)
        self.move_camera(phi=0, theta=-90 * DEGREES, zoom=1, frame_center=ORIGIN, run_time=0.1)
        self.play(Write(formula), run_time=run_time)
        self.live.add(formula)
        return formula

    def make_formula(self, key):
        specs = {
            "newton_second_law_anchor": (
                ["F", "=", "m", "\\mathbf{a}"],
                78,
                {0: self.INTERACTION, 1: self.TEXT, 2: self.STRUCTURE, 3: self.STRUCTURE},
            ),
            "mass_energy_anchor": (
                ["E", "=", "m", "c^2"],
                78,
                {0: self.STRUCTURE, 1: self.TEXT, 2: self.STRUCTURE, 3: self.LIGHT},
            ),
            "newton_inverse_square_gravity": (
                ["F_g", "=", "G", "m_1", "m_2", "r^{-2}"],
                72,
                {0: self.INTERACTION, 1: self.TEXT, 2: self.INTERACTION, 3: self.STRUCTURE, 4: self.STRUCTURE, 5: self.STRUCTURE},
            ),
            "mercury_residual": (
                ["\\Delta\\varpi_{\\mathrm{obs}}", "-", "\\Delta\\varpi_{\\mathrm{Newt}}", "\\approx", "43^{\\prime\\prime}/\\mathrm{century}"],
                66,
                {0: self.STRUCTURE, 1: self.TEXT, 2: self.STRUCTURE, 3: self.TEXT, 4: self.INTERACTION},
            ),
            "relativistic_perihelion_correction": (
                ["\\Delta\\varpi_{\\mathrm{GR}}", "=", "6\\pi", "G M", "a^{-1}", "(1-\\epsilon^2)^{-1}", "c^{-2}"],
                58,
                {0: self.STRUCTURE, 1: self.TEXT, 2: self.TEXT, 3: self.STRUCTURE, 4: self.STRUCTURE, 5: self.STRUCTURE, 6: self.LIGHT},
            ),
            "event_coordinates": (
                ["x^\\mu", "=", "(ct,\\,x,\\,y,\\,z)"],
                70,
                {0: self.STRUCTURE, 1: self.TEXT, 2: self.LIGHT},
            ),
            "flat_spacetime_interval": (
                ["\\Delta s^2", "=", "-c^2\\Delta t^2", "+", "\\Delta x^2+\\Delta y^2+\\Delta z^2"],
                60,
                {0: self.STRUCTURE, 1: self.TEXT, 2: self.LIGHT, 3: self.TEXT, 4: self.STRUCTURE},
            ),
            "metric_interval": (
                ["ds^2", "=", "g_{\\mu\\nu}", "dx^\\mu", "dx^\\nu"],
                70,
                {0: self.STRUCTURE, 1: self.TEXT, 2: self.STRUCTURE, 3: self.STRUCTURE, 4: self.STRUCTURE},
            ),
            "geodesic_equation": (
                ["\\frac{d^2x^\\mu}{d\\lambda^2}", "+", "\\Gamma^\\mu_{\\alpha\\beta}", "\\frac{dx^\\alpha}{d\\lambda}", "\\frac{dx^\\beta}{d\\lambda}", "=", "0"],
                54,
                {0: self.TEXT, 1: self.TEXT, 2: self.INTERACTION, 3: self.STRUCTURE, 4: self.STRUCTURE, 5: self.TEXT, 6: self.TEXT},
            ),
            "einstein_field_equation_texture": (
                ["G_{\\mu\\nu}", "=", "\\frac{8\\pi G}{c^4}", "T_{\\mu\\nu}"],
                62,
                {0: self.STRUCTURE, 1: self.TEXT, 2: self.INTERACTION, 3: self.MATTER},
            ),
            "geodesic_gamma_focus": (
                ["\\frac{d^2x^\\mu}{d\\lambda^2}", "+", "\\Gamma^\\mu_{\\alpha\\beta}", "\\frac{dx^\\alpha}{d\\lambda}", "\\frac{dx^\\beta}{d\\lambda}", "=", "0"],
                54,
                {0: self.TEXT, 1: self.TEXT, 2: "#e0ad86", 3: self.STRUCTURE, 4: self.STRUCTURE, 5: self.TEXT, 6: self.TEXT},
            ),
            "christoffel_connection_from_metric": (
                ["\\Gamma^\\rho_{\\mu\\nu}", "=", "\\frac{1}{2}", "g^{\\rho\\sigma}", "\\left(\\partial_\\mu g_{\\nu\\sigma}+\\partial_\\nu g_{\\mu\\sigma}-\\partial_\\sigma g_{\\mu\\nu}\\right)"],
                48,
                {0: self.INTERACTION, 1: self.TEXT, 2: self.TEXT, 3: self.STRUCTURE, 4: self.STRUCTURE},
            ),
            "evidence_crisis_structure_pattern": (
                ["\\text{mismatch}", "\\Rightarrow", "\\text{crisis}", "\\Rightarrow", "\\text{deeper rule}", "\\Rightarrow", "\\text{new structure}"],
                42,
                {0: self.TEXT, 1: self.SECONDARY, 2: self.INTERACTION, 3: self.SECONDARY, 4: self.STRUCTURE, 5: self.SECONDARY, 6: self.STRUCTURE},
            ),
            "double_slit_probability_with_interference": (
                ["P(x)", "=", "|\\psi_1+\\psi_2|^2", "=", "|\\psi_1|^2", "+|\\psi_2|^2", "+2\\operatorname{Re}(\\psi_1^*\\psi_2)"],
                44,
                {0: self.TEXT, 1: self.TEXT, 2: self.MATTER, 3: self.TEXT, 4: self.MATTER, 5: self.MATTER, 6: self.LIGHT},
            ),
            "schrodinger_wave_milestone": (
                ["i\\hbar", "\\partial_t", "\\psi", "=", "\\hat H", "\\psi"],
                64,
                {0: self.STRUCTURE, 1: self.TEXT, 2: self.MATTER, 3: self.TEXT, 4: self.STRUCTURE, 5: self.MATTER},
            ),
            "dirac_relativistic_field_milestone": (
                ["(", "i\\gamma^\\mu\\partial_\\mu", "-", "m", ")", "\\psi", "=", "0"],
                60,
                {0: self.TEXT, 1: self.STRUCTURE, 2: self.TEXT, 3: self.STRUCTURE, 4: self.TEXT, 5: self.MATTER, 6: self.TEXT, 7: self.TEXT},
            ),
            "one_particle_as_field_excitation": (
                ["a^\\dagger_{\\mathbf p}|0\\rangle", "=", "|\\mathbf p\\rangle"],
                66,
                {0: self.MATTER, 1: self.TEXT, 2: self.MATTER},
            ),
            "qed_interaction_lagrangian": (
                ["\\mathcal L_{\\mathrm{int}}", "=", "-e", "\\bar\\psi\\gamma^\\mu\\psi", "A_\\mu"],
                60,
                {0: self.INTERACTION, 1: self.TEXT, 2: self.INTERACTION, 3: self.MATTER, 4: self.LIGHT},
            ),
            "fine_structure_constant": (
                ["\\alpha", "=", "\\frac{e^2}{4\\pi\\varepsilon_0\\hbar c}", "\\approx", "\\frac{1}{137.035999}"],
                52,
                {0: self.INTERACTION, 1: self.TEXT, 2: self.INTERACTION, 3: self.TEXT, 4: self.INTERACTION},
            ),
        }
        parts, font_size, colors = specs[key]
        formula = MathTex(*parts, font_size=font_size)
        formula.set_color(self.TEXT)
        for index, color in colors.items():
            if index < len(formula):
                formula[index].set_color(color)
        return formula

    def make_glow(self, part, color, wide=False):
        widths = (10, 18) if wide else (8, 14)
        opacities = (0.36, 0.16)
        glow = VGroup()
        for width, opacity in zip(widths, opacities):
            layer = part.copy()
            layer.set_fill(opacity=0)
            layer.set_stroke(color=color, width=width, opacity=opacity)
            layer.set_z_index(part.z_index - 1)
            glow.add(layer)
        return glow

    def term_tour(self, formula, part_index, caption, zoom, glow_color, dim, run_time):
        self.caption(caption)
        part = formula[part_index]
        glow = self.make_glow(part, glow_color)
        self.current_glow = glow
        anims = []
        for i, item in enumerate(formula):
            anims.append(item.animate.set_opacity(1 if i == part_index else dim))
        self.play(*anims, FadeIn(glow), run_time=0.45)
        self.move_camera(
            phi=0,
            theta=-90 * DEGREES,
            zoom=zoom,
            frame_center=part.get_center(),
            run_time=run_time,
        )
        self.wait(0.6)

    def big_gamma_zoom(self, formula):
        part = formula[2]
        glow = self.make_glow(part, self.INTERACTION, wide=True)
        self.current_glow = glow
        anims = []
        for i, item in enumerate(formula):
            anims.append(item.animate.set_opacity(1 if i == 2 else 0.16))
        self.play(*anims, FadeIn(glow), run_time=0.5)
        self.move_camera(
            phi=0,
            theta=-90 * DEGREES,
            zoom=3.0,
            frame_center=part.get_center(),
            run_time=3.8,
        )
        self.wait(1.6)

    def pull_back(self, formula, run_time=1.2, center=None):
        if center is None:
            center = formula.get_center()
        self.move_camera(
            phi=0,
            theta=-90 * DEGREES,
            zoom=1,
            frame_center=center,
            run_time=run_time,
        )
        anims = [part.animate.set_opacity(1) for part in formula]
        if self.current_glow is not None:
            anims.append(FadeOut(self.current_glow))
        self.play(*anims, run_time=0.35)
        if self.current_glow is not None:
            self.remove(self.current_glow)
        self.current_glow = None

    def metric_grid(self):
        grid = VGroup()
        for x in np.linspace(-4.2, 4.2, 17):
            grid.add(Line([x, -2.6, -0.05], [x, 2.6, -0.05], color=self.SECONDARY, stroke_width=1).set_opacity(0.18))
        for y in np.linspace(-2.6, 2.6, 11):
            grid.add(Line([-4.2, y, -0.05], [4.2, y, -0.05], color=self.SECONDARY, stroke_width=1).set_opacity(0.18))
        grid.set_z_index(-3)
        return grid

    def distance_set_piece(self, formula):
        sun = Dot([-2.2, 0, 0], radius=0.22, color=self.STRUCTURE)
        planet = Dot([2.2, 0, 0], radius=0.12, color=self.STRUCTURE)
        shells = VGroup(*[
            Circle(radius=r, color=self.SECONDARY, stroke_width=1).move_to(sun.get_center()).set_opacity(0.18)
            for r in (0.9, 1.55, 2.2, 2.85)
        ])
        force = VGroup(
            Line([-1.9, 0, 0.02], [0.2, 0, 0.02], color=self.INTERACTION, stroke_width=6),
            Line([0.2, 0, 0.02], [1.35, 0, 0.02], color=self.INTERACTION, stroke_width=4).set_opacity(0.75),
            Arrow([1.35, 0, 0.02], [2.02, 0, 0.02], buff=0, color=self.INTERACTION, stroke_width=2, max_tip_length_to_length_ratio=0.22).set_opacity(0.6),
        )
        piece = VGroup(shells, sun, planet, force)
        self.live.add(piece)
        self.play(formula.animate.set_opacity(0.18).shift(UP * 1.2), FadeIn(piece), run_time=0.8)
        self.move_camera(phi=55 * DEGREES, theta=-55 * DEGREES, zoom=1.12, frame_center=ORIGIN, run_time=1.8)
        self.move_camera(phi=55 * DEGREES, theta=-70 * DEGREES, zoom=1.12, frame_center=ORIGIN, run_time=2.0)
        self.move_camera(phi=0, theta=-90 * DEGREES, zoom=1, frame_center=ORIGIN, run_time=1.2)

    def warped_grid(self, depression):
        grid = VGroup()
        xs = np.linspace(-3.2, 3.2, 15)
        ys = np.linspace(-3.2, 3.2, 15)
        for x in xs:
            grid.add(ParametricFunction(
                lambda t, x=x: np.array([x, t, depression(x, t)]),
                t_range=[-3.2, 3.2],
                color=self.SECONDARY,
                stroke_width=1.2,
            ).set_opacity(0.55))
        for y in ys:
            grid.add(ParametricFunction(
                lambda t, y=y: np.array([t, y, depression(t, y)]),
                t_range=[-3.2, 3.2],
                color=self.SECONDARY,
                stroke_width=1.2,
            ).set_opacity(0.55))
        return grid

    def metric_set_piece(self, formula):
        grid = self.warped_grid(lambda u, v: -0.55 * np.exp(-0.35 * (u * u + v * v)))
        grid.set_color(self.STRUCTURE)
        self.live.add(grid)
        self.play(formula.animate.set_opacity(0.20).scale(0.82), FadeIn(grid), run_time=0.8)
        self.move_camera(phi=60 * DEGREES, theta=-55 * DEGREES, zoom=1.15, frame_center=ORIGIN, run_time=1.8)
        self.move_camera(phi=60 * DEGREES, theta=-70 * DEGREES, zoom=1.15, frame_center=ORIGIN, run_time=2.0)
        self.move_camera(phi=0, theta=-90 * DEGREES, zoom=1, frame_center=ORIGIN, run_time=1.2)

    def curvature_set_piece(self, formula):
        def depression(u, v):
            left = -0.38 * np.exp(-((u + 1.1) ** 2 + (v - 0.45) ** 2))
            right = -0.28 * np.exp(-((u - 1.2) ** 2 + (v + 0.35) ** 2))
            return left + right

        grid = self.warped_grid(depression)
        grid.set_color(self.STRUCTURE)
        nodes = VGroup()
        for point in [[-1.1, 0.45, 0.16], [1.2, -0.35, 0.16]]:
            core = Dot(point, radius=0.13, color=self.MATTER)
            halo = Dot(point, radius=0.28, color=self.MATTER).set_opacity(0.18)
            nodes.add(halo, core)
        piece = VGroup(grid, nodes)
        self.live.add(piece)
        self.play(formula.animate.set_opacity(0.18).shift(UP * 1.1), FadeIn(piece), run_time=0.8)
        self.move_camera(phi=62 * DEGREES, theta=-50 * DEGREES, zoom=1.18, frame_center=ORIGIN, run_time=1.8)
        self.move_camera(phi=62 * DEGREES, theta=-66 * DEGREES, zoom=1.18, frame_center=ORIGIN, run_time=2.0)
        self.move_camera(phi=0, theta=-90 * DEGREES, zoom=1, frame_center=ORIGIN, run_time=1.3)

    def double_slit_set_piece(self):
        barrier = VGroup(
            Line([-1.7, -1.3, 0], [-1.7, -0.55, 0], color=self.SECONDARY, stroke_width=5),
            Line([-1.7, -0.18, 0], [-1.7, 0.18, 0], color=self.SECONDARY, stroke_width=5),
            Line([-1.7, 0.55, 0], [-1.7, 1.3, 0], color=self.SECONDARY, stroke_width=5),
        )
        source = Dot([-3.2, 0, 0], radius=0.09, color=self.MATTER)
        incoming = VGroup(
            Line([-3.1, 0, 0], [-1.9, -0.35, 0], color=self.MATTER, stroke_width=2).set_opacity(0.55),
            Line([-3.1, 0, 0], [-1.9, 0.35, 0], color=self.MATTER, stroke_width=2).set_opacity(0.55),
        )
        waves = VGroup()
        for slit_y in (-0.35, 0.35):
            for r in np.linspace(0.45, 2.55, 6):
                arc = Arc(
                    radius=r,
                    start_angle=-50 * DEGREES,
                    angle=100 * DEGREES,
                    color=self.MATTER,
                    stroke_width=2,
                )
                arc.move_arc_center_to(np.array([-1.7, slit_y, 0]))
                arc.set_opacity(0.62)
                waves.add(arc)
        screen = Line([3.0, -1.35, 0], [3.0, 1.35, 0], color=self.SECONDARY, stroke_width=4).set_opacity(0.65)
        bands = VGroup()
        for i, y in enumerate(np.linspace(-1.1, 1.1, 9)):
            opacity = 0.9 if i % 2 == 0 else 0.28
            bands.add(Line([3.05, y - 0.08, 0], [3.05, y + 0.08, 0], color=self.LIGHT, stroke_width=8).set_opacity(opacity))
        dots = VGroup(*[
            Dot([3.15, y, 0], radius=0.035, color=self.LIGHT).set_opacity(0.75)
            for y in np.linspace(-1.0, 1.0, 17)
        ])
        return VGroup(source, incoming, barrier, waves, screen, bands, dots).shift(UP * 1.25)
