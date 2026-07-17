from manim import *
import math


class FourConstantsVacuumWoundJourney(ThreeDScene):
    BG = "#0c0c0b"
    TEXT = "#faf9f5"
    CORAL = "#d97757"
    BLUE = "#6a9bcc"
    OLIVE = "#788c5d"
    GOLD = "#d4a27f"
    GRAY = "#b0aea5"

    FORMULAS = {
        "A1_four_dials": {
            "parts": [
                r"\text{rule dials}", ":", r"\quad", "c", r",\quad", "G", r",\quad", r"\hbar", r",\quad", r"\Lambda",
            ],
            "scale": 1.25,
            "colors": {3: BLUE, 5: OLIVE, 7: CORAL, 9: GOLD},
        },
        "A2_reachable_cone": {
            "parts": ["r", r"\le", "c", r"\Delta t"],
            "scale": 1.45,
            "colors": {0: OLIVE, 2: BLUE, 3: BLUE},
        },
        "A2_spacetime_interval": {
            "parts": [
                r"\Delta s^2", "=", r"c^2\Delta t^2", "-", r"\Delta x^2", "-", r"\Delta y^2", "-", r"\Delta z^2",
            ],
            "scale": 1.15,
            "colors": {2: BLUE, 4: OLIVE, 6: OLIVE, 8: OLIVE},
        },
        "A3_einstein_coupling": {
            "parts": [
                r"R_{\mu\nu}", "-", r"\frac{1}{2}R g_{\mu\nu}", "=", r"\frac{8\pi G}{c^4}", r"T_{\mu\nu}",
            ],
            "scale": 0.98,
            "colors": {0: OLIVE, 4: GRAY, 5: OLIVE},
        },
        "A4_schrodinger_clock": {
            "parts": ["i", r"\hbar", r"\frac{\partial}{\partial t}", r"\psi", "=", r"\hat{H}", r"\psi"],
            "scale": 1.15,
            "colors": {1: CORAL, 3: CORAL, 5: GOLD, 6: CORAL},
        },
        "A4_uncertainty_grain": {
            "parts": [r"\Delta x", r"\Delta p", r"\ge", r"\frac{\hbar}{2}"],
            "scale": 1.25,
            "colors": {0: CORAL, 1: CORAL, 3: CORAL},
        },
        "A5_bronstein_coordinates": {
            "parts": [r"\text{theory space}", ":", "(", r"c^{-1}", ",", "G", ",", r"\hbar", ")"],
            "scale": 1.15,
            "colors": {3: BLUE, 5: OLIVE, 7: CORAL},
        },
        "A5_quantum_gravity_corner": {
            "parts": [
                r"\text{far corner}", ":", r"c^{-1}", ",", "G", ",", r"\hbar", r"\ne 0", r"\Rightarrow", r"\text{quantum gravity?}",
            ],
            "scale": 1.0,
            "colors": {2: BLUE, 4: OLIVE, 6: CORAL, 9: GOLD},
        },
        "A6_planck_length": {
            "parts": [r"\ell_{\mathrm{P}}", "=", r"\sqrt{\frac{\hbar G}{c^3}}"],
            "scale": 1.25,
            "colors": {0: OLIVE, 2: GRAY},
        },
        "A6_planck_length_value": {
            "parts": [r"\ell_{\mathrm{P}}", r"\approx", "1.62", r"\times", r"10^{-35}\,\mathrm{m}"],
            "scale": 1.2,
            "colors": {0: OLIVE, 4: OLIVE},
        },
        "A7_lambda_in_geometry": {
            "parts": [
                r"R_{\mu\nu}", "-", r"\frac{1}{2}R g_{\mu\nu}", "+", r"\Lambda g_{\mu\nu}", "=", r"\frac{8\pi G}{c^4}", r"T_{\mu\nu}",
            ],
            "scale": 0.92,
            "colors": {4: GOLD, 6: GRAY, 7: OLIVE},
        },
        "A7_lambda_acceleration": {
            "parts": [r"\frac{\ddot a}{a}", "=", r"\frac{\Lambda c^2}{3}"],
            "scale": 1.25,
            "colors": {2: GOLD},
        },
        "A8_de_sitter_rate": {
            "parts": [r"H_{\Lambda}", "=", r"c\sqrt{\frac{\Lambda}{3}}"],
            "scale": 1.25,
            "colors": {0: GOLD, 2: GOLD},
        },
        "A8_de_sitter_horizon": {
            "parts": [r"R_{\Lambda}", "=", r"\frac{c}{H_{\Lambda}}", "=", r"\sqrt{\frac{3}{\Lambda}}"],
            "scale": 1.15,
            "colors": {0: GOLD, 2: BLUE, 4: GOLD},
        },
        "A9_length_hierarchy": {
            "parts": [
                r"\frac{R_{\Lambda}}{\ell_{\mathrm{P}}}", "=", r"\sqrt{\frac{3}{\Lambda}}", r"\sqrt{\frac{c^3}{\hbar G}}", r"\sim", r"10^{61}",
            ],
            "scale": 0.98,
            "colors": {0: OLIVE, 2: GOLD, 3: GRAY, 5: GOLD},
        },
        "A9_logarithmic_elevator": {
            "parts": [r"\log_{10}", "(", r"\frac{R_{\Lambda}}{\ell_{\mathrm{P}}}", ")", r"\approx", "61.0"],
            "scale": 1.15,
            "colors": {2: OLIVE, 5: GOLD},
        },
        "A10_vacuum_density_definition": {
            "parts": [r"\varepsilon_{\mathrm{vac}}", "=", r"\frac{E_{\mathrm{vac}}}{V}"],
            "scale": 1.25,
            "colors": {0: GOLD, 2: OLIVE},
        },
        "A10_lambda_energy_density": {
            "parts": [r"\varepsilon_{\Lambda}", "=", r"\frac{\Lambda c^4}{8\pi G}"],
            "scale": 1.15,
            "colors": {0: GOLD, 2: GOLD},
        },
        "A11_planck_density_estimate": {
            "parts": [
                r"\varepsilon_{\mathrm{P}}", r"\sim", r"\frac{E_{\mathrm{P}}}{\ell_{\mathrm{P}}^3}", r"\sim", r"\frac{c^7}{\hbar G^2}",
            ],
            "scale": 1.08,
            "colors": {0: CORAL, 2: OLIVE, 4: GRAY},
        },
        "A11_density_canyon": {
            "parts": [
                r"\frac{\varepsilon_{\mathrm{P}}}{\varepsilon_{\Lambda}}", r"\sim", "(", r"\frac{R_{\Lambda}}{\ell_{\mathrm{P}}}", r")^2", r"\sim", r"10^{122}",
            ],
            "scale": 1.0,
            "colors": {0: GOLD, 3: OLIVE, 6: GOLD},
        },
        "A12_four_constant_summary": {
            "parts": [
                "(", "c", ",", "G", ",", r"\hbar", ",", r"\Lambda", ")", r"\Rightarrow",
                r"\ell_{\mathrm{P}}", ",", r"R_{\Lambda}", ",", r"\frac{\varepsilon_{\mathrm{P}}}{\varepsilon_{\Lambda}}\sim10^{122}",
            ],
            "scale": 0.92,
            "colors": {1: BLUE, 3: OLIVE, 5: CORAL, 7: GOLD, 10: OLIVE, 12: GOLD, 14: GOLD},
        },
    }

    def construct(self):
        self.camera.background_color = self.BG
        self.set_camera_orientation(phi=0, theta=-90 * DEGREES)
        self.current_formula = None
        self.current_sets = VGroup()
        self.caption_mob = None
        self.glow = None

        self.headline("Four constants act like rule settings.", hold=1.2)
        self.pause(0.8)
        self.show_formula("A1_four_dials", run_time=1.0)
        self.caption("Constants are rule-settings, not just numbers.", hold=0.9)
        self.tour_sequence([
            (3, self.BLUE, "Speed limits which events can talk.", 2.25, 0.25, 1.4, 1.2, 0.9, 0.7),
            (5, self.OLIVE, "Gravity tells geometry how strongly to answer.", 2.25, 0.25, 1.3, 1.1, 0.9, 0.7),
            (7, self.CORAL, "Quantum grain turns points into waves.", 2.3, 0.25, 1.3, 1.1, 0.9, 0.7),
            (9, self.GOLD, "Lambda is empty space pushing back.", 2.35, 0.22, 1.5, 1.3, 1.0, 0.9),
        ])
        self.pause(1.0)

        self.headline("Light draws the map of what can happen.", hold=1.3)
        self.show_formula("A2_reachable_cone", run_time=1.0, support=self.causal_disk())
        self.caption("Signals reach only the cone light can cross.", hold=0.8)
        self.term_tour(2, self.BLUE, "c is the maximum speed for influence.", zoom=2.45, dim=0.24, run_time=1.5, hold=1.2)
        self.pull_back(run_time=0.9, hold=0.8)
        self.run_set_piece(self.light_cone_set(), "The inequality rises into a cone.", 60 * DEGREES, -45 * DEGREES, 1.1, 1.4, 3.0, 0.06, 1.0, 1.2, 1.2)

        self.headline("Space and time share one measuring rule.", hold=1.3)
        self.transform_formula("A2_spacetime_interval", run_time=1.2)
        self.caption("Time and space share one invariant separation.", hold=0.8)
        self.tour_sequence([
            (2, self.BLUE, "c translates time into distance language.", 2.35, 0.22, 1.4, 1.2, 0.9, 0.8),
            (4, self.OLIVE, "Space competes with the time part.", 2.2, 0.25, 1.3, 1.1, 0.9, 0.9),
        ])

        self.headline("Gravity is geometry answering matter.", hold=1.4)
        self.show_formula("A3_einstein_coupling", run_time=1.1)
        self.caption("Curvature listens to the energy inventory.", hold=0.9)
        self.tour_sequence([
            (4, self.OLIVE, "G makes geometry respond to energy.", 2.55, 0.2, 1.5, 1.2, 1.0, 0.8),
            (4, self.BLUE, "c to the fourth welds gravity to relativity.", 2.65, 0.2, 1.5, 1.3, 1.0, 0.8),
            (5, self.OLIVE, "Matter is energy, pressure, momentum, and stress.", 2.35, 0.22, 1.4, 1.2, 1.0, 0.8),
        ])
        self.run_set_piece(self.curved_geometry_set(), "A local packet bends the grid.", 58 * DEGREES, -38 * DEGREES, 1.05, 1.5, 3.0, 0.05, 1.0, 1.3, 1.2)

        self.headline("Quantum matter evolves like a phase clock.", hold=1.3)
        self.show_formula("A4_schrodinger_clock", run_time=1.0, support=self.wave_support())
        self.caption("Quantum waves tick with energy.", hold=0.8)
        self.tour_sequence([
            (1, self.CORAL, "hbar sets the quantum phase grain.", 2.5, 0.22, 1.4, 1.2, 0.9, 0.8),
            (3, self.CORAL, "psi is possibility, not a bead.", 2.45, 0.22, 1.4, 1.2, 0.9, 0.8),
        ])
        self.wave_packet_transform()

        self.headline("Certainty cannot be squeezed without cost.", hold=1.3)
        self.show_formula("A4_uncertainty_grain", run_time=1.0, support=self.narrow_packet())
        self.caption("Sharper position means blurrier momentum.", hold=0.8)
        self.term_tour(3, self.CORAL, "hbar sets the irreducible grain.", zoom=2.75, dim=0.18, run_time=1.6, hold=1.3)
        self.pull_back(run_time=1.0, hold=0.9)

        self.headline("The theories form a map of limits.", hold=1.3)
        self.show_formula("A5_bronstein_coordinates", run_time=1.0)
        self.caption("These axes are rule-directions, not space.", hold=0.9)
        self.tour_sequence([
            (3, self.BLUE, "Finite signal speed moves this axis.", 2.4, 0.23, 1.4, 1.1, 0.9, 0.8),
            (5, self.OLIVE, "Geometry responds when G is active.", 2.4, 0.23, 1.4, 1.1, 0.9, 0.8),
            (7, self.CORAL, "Matter becomes waves when hbar matters.", 2.4, 0.23, 1.4, 1.1, 0.9, 0.8),
        ])
        self.run_set_piece(self.bronstein_cube_set(), "The rule-directions become a cube.", 62 * DEGREES, -42 * DEGREES, 1.15, 1.6, 3.2, 0.055, 1.0, 1.4, 1.2)

        self.headline("The far corner names the unsolved meeting.", hold=1.3)
        self.show_formula("A5_quantum_gravity_corner", run_time=1.0)
        self.caption("The far corner keeps all three dials active.", hold=1.0)

        self.headline("Three deep dials build a tiny ruler.", hold=1.3)
        self.show_formula("A6_planck_length", run_time=1.1, support=self.tiny_ruler())
        self.caption("Three dials assemble a natural tiny ruler.", hold=0.9)
        self.tour_sequence([
            (0, self.OLIVE, "This is the three-dial ruler.", 2.35, 0.22, 1.4, 1.1, 0.9, 0.8),
            (2, self.CORAL, "hbar contributes quantum grain.", 2.45, 0.22, 1.4, 1.1, 0.9, 0.8),
            (2, self.OLIVE, "G contributes gravitational curvature.", 2.45, 0.22, 1.4, 1.1, 0.9, 0.8),
            (2, self.BLUE, "c cubed squeezes the scale down.", 2.6, 0.2, 1.5, 1.2, 1.0, 0.9),
        ])

        self.headline("The number is almost all exponent.", hold=1.3)
        self.transform_formula("A6_planck_length_value", run_time=1.2)
        self.caption("The exponent carries the scale.", hold=0.9)
        self.term_tour(4, self.OLIVE, "Thirty-five powers below a meter.", zoom=2.85, dim=0.16, run_time=1.8, hold=1.5)
        self.pull_back(run_time=1.1, hold=0.9)

        self.headline("Empty space can join the geometry.", hold=1.3)
        self.show_formula("A7_lambda_in_geometry", run_time=1.1)
        self.caption("Empty space can curve spacetime.", hold=0.9)
        self.term_tour(4, self.GOLD, "Lambda is curvature from empty space.", zoom=2.65, dim=0.18, run_time=1.6, hold=1.3)
        self.pull_back(run_time=1.0, hold=0.8)

        self.headline("Positive vacuum curvature makes expansion accelerate.", hold=1.3)
        self.transform_formula("A7_lambda_acceleration", run_time=1.2)
        self.caption("Positive vacuum curvature accelerates expansion.", hold=0.9)
        self.term_tour(2, self.GOLD, "Positive Lambda pushes the scale outward.", zoom=2.7, dim=0.18, run_time=1.6, hold=1.3)
        self.pull_back(run_time=1.0, hold=0.9)
        self.run_set_piece(self.expansion_grid_set(), "Everywhere stretches, not from one center.", 56 * DEGREES, -35 * DEGREES, 1.1, 1.5, 3.0, 0.045, 1.0, 1.3, 1.1)

        self.headline("A Lambda universe has its own clock.", hold=1.3)
        self.show_formula("A8_de_sitter_rate", run_time=1.0, support=self.expanding_ring())
        self.caption("Lambda sets the de Sitter expansion rate.", hold=0.9)
        self.term_tour(2, self.GOLD, "Lambda hides inside the rate.", zoom=2.65, dim=0.2, run_time=1.5, hold=1.2)
        self.pull_back(run_time=1.0, hold=0.8)

        self.headline("That clock defines a cosmic horizon.", hold=1.3)
        self.transform_formula("A8_de_sitter_horizon", run_time=1.2)
        self.caption("The horizon is the distance set by Lambda.", hold=0.9)
        self.tour_sequence([
            (0, self.GOLD, "R Lambda is dark energy's ruler.", 2.45, 0.22, 1.4, 1.1, 0.9, 0.8),
            (4, self.GOLD, "Smaller Lambda means a larger horizon.", 2.7, 0.18, 1.6, 1.3, 1.0, 0.9),
        ])

        self.headline("The smallest and largest rulers almost meet never.", hold=1.4)
        self.show_formula("A9_length_hierarchy", run_time=1.1, support=self.two_ruler_ticks())
        self.caption("The universe spans sixty-one decimal steps.", hold=0.9)
        self.tour_sequence([
            (0, self.OLIVE, "This compares outer and inner rulers.", 2.35, 0.22, 1.4, 1.1, 0.9, 0.8),
            (5, self.GOLD, "Sixty-one powers separate the rulers.", 2.9, 0.14, 1.9, 1.5, 1.1, 0.9),
        ])

        self.headline("A logarithm turns scale into steps.", hold=1.3)
        self.transform_formula("A9_logarithmic_elevator", run_time=1.2)
        self.caption("The log makes the jumps countable.", hold=0.9)
        self.tour_sequence([
            (2, self.OLIVE, "The same ratio becomes an elevator.", 2.4, 0.22, 1.4, 1.1, 0.9, 0.8),
            (5, self.GOLD, "Sixty-one is a step count.", 2.8, 0.16, 1.7, 1.4, 1.0, 0.8),
        ])
        self.run_set_piece(self.log_elevator_set(), "Equal steps mean equal powers of ten.", 60 * DEGREES, -30 * DEGREES, 1.15, 1.5, 3.0, 0.04, 1.0, 1.2, 1.1)

        self.headline("The crisis is energy per volume.", hold=1.3)
        self.show_formula("A10_vacuum_density_definition", run_time=1.0, support=self.density_box())
        self.caption("Density means energy per volume.", hold=0.9)
        self.tour_sequence([
            (0, self.GOLD, "Vacuum density assigns energy to space.", 2.45, 0.22, 1.4, 1.1, 0.9, 0.8),
            (2, self.OLIVE, "The question is energy per volume.", 2.5, 0.22, 1.4, 1.1, 0.9, 0.8),
        ])

        self.headline("Observed dark energy is thin but real.", hold=1.3)
        self.transform_formula("A10_lambda_energy_density", run_time=1.2)
        self.caption("Observed dark energy is very dilute.", hold=0.9)
        self.tour_sequence([
            (0, self.GOLD, "This is the observed lower plate.", 2.45, 0.22, 1.4, 1.1, 0.9, 0.8),
            (2, self.GOLD, "Lambda supplies measured vacuum curvature.", 2.55, 0.2, 1.5, 1.2, 1.0, 0.9),
        ])

        self.headline("A naive quantum estimate towers above it.", hold=1.3)
        self.show_formula("A11_planck_density_estimate", run_time=1.1, support=self.upper_density_plate())
        self.caption("Naive quantum density is enormous.", hold=0.9)
        self.tour_sequence([
            (0, self.CORAL, "This is a rough quantum estimate.", 2.45, 0.22, 1.4, 1.1, 0.9, 0.8),
            (2, self.OLIVE, "One Planck energy per Planck volume.", 2.65, 0.2, 1.5, 1.2, 1.0, 0.8),
        ])

        self.headline("The mismatch becomes the wound.", hold=1.4)
        self.transform_formula("A11_density_canyon", run_time=1.3)
        self.caption("The density canyon is squared length hierarchy.", hold=0.9)
        self.tour_sequence([
            (0, self.GOLD, "This compares estimate with observation.", 2.45, 0.2, 1.5, 1.2, 1.0, 0.8),
            (3, self.OLIVE, "The length gulf gets squared.", 2.65, 0.18, 1.6, 1.3, 1.0, 0.8),
        ])
        self.term_tour(6, self.GOLD, "One hundred twenty-two powers of mismatch.", zoom=3.0, dim=0.1, run_time=2.8, hold=1.6)
        self.pull_back(run_time=1.5, hold=1.0)
        self.run_set_piece(self.density_canyon_set(), "The gap is counted in powers.", 64 * DEGREES, -36 * DEGREES, 1.15, 1.7, 3.4, 0.035, 1.0, 1.4, 1.2)

        self.headline("The four dials make the wound precise.", hold=1.4)
        self.show_formula("A12_four_constant_summary", run_time=1.2)
        self.caption("The constants diagnose the wound.", hold=1.0)
        self.tour_sequence([
            (1, self.BLUE, "c marks causal boundaries.", 2.2, 0.25, 1.3, 1.0, 0.8, 0.7),
            (3, self.OLIVE, "G couples energy to curvature.", 2.2, 0.25, 1.3, 1.0, 0.8, 0.7),
            (5, self.CORAL, "hbar marks quantum grain.", 2.2, 0.25, 1.3, 1.0, 0.8, 0.7),
            (7, self.GOLD, "Lambda marks vacuum curvature.", 2.3, 0.23, 1.4, 1.1, 0.9, 0.8),
            (14, self.GOLD, "The map exposes the mismatch.", 2.75, 0.16, 1.7, 1.4, 1.2, 1.0),
        ])
        self.final_glows()
        self.pause(1.6)

    def pause(self, seconds):
        self.wait(max(0.6, min(1.6, seconds)))

    def break_headline(self, text):
        if len(text) <= 34:
            return text
        words = text.split()
        half = len(text) / 2
        best = 0
        best_gap = 999
        count = 0
        for i, word in enumerate(words[:-1]):
            count += len(word) + (1 if i else 0)
            gap = abs(count - half)
            if gap < best_gap:
                best = i + 1
                best_gap = gap
        return " ".join(words[:best]) + "\n" + " ".join(words[best:])

    def clear_scene(self):
        mobs = []
        if self.glow is not None:
            mobs.append(self.glow)
            self.glow = None
        if self.current_formula is not None:
            mobs.append(self.current_formula)
            self.current_formula = None
        if len(self.current_sets) > 0:
            mobs.append(self.current_sets)
            self.current_sets = VGroup()
        if self.caption_mob is not None:
            mobs.append(self.caption_mob)
            self.caption_mob = None
        if mobs:
            self.play(*[FadeOut(m) for m in mobs], run_time=0.35)

    def clear_sets(self, run_time=0.35):
        if len(self.current_sets) > 0:
            self.play(FadeOut(self.current_sets), run_time=run_time)
            self.current_sets = VGroup()

    def headline(self, text, hold=1.3, font_size=72):
        self.clear_scene()
        self.move_camera(phi=0, theta=-90 * DEGREES, zoom=1, frame_center=ORIGIN, run_time=0.8)
        headline = Text(
            self.break_headline(text),
            font_size=font_size,
            color=self.TEXT,
            weight=BOLD,
            line_spacing=0.85,
        ).move_to(ORIGIN)
        headline.set_stroke(self.BG, width=4, background=True)
        self.add_fixed_in_frame_mobjects(headline)
        self.play(FadeIn(headline, shift=0.1 * UP), run_time=0.8)
        self.pause(hold)
        self.play(FadeOut(headline), run_time=0.45)
        self.remove(headline)

    def caption(self, text, hold=0.9):
        new_caption = Text(text, font_size=30, color=self.TEXT, slant="ITALIC")
        if new_caption.width > config.frame_width - 1.0:
            new_caption.scale((config.frame_width - 1.0) / new_caption.width)
        new_caption.to_edge(DOWN, buff=0.55)
        new_caption.set_stroke(self.BG, width=5, background=True)
        new_caption.set_z_index(1000)
        self.add_fixed_in_frame_mobjects(new_caption)
        if self.caption_mob is None:
            self.play(FadeIn(new_caption, shift=0.08 * UP), run_time=0.35)
        else:
            old = self.caption_mob
            self.play(FadeOut(old), FadeIn(new_caption, shift=0.08 * UP), run_time=0.35)
            self.remove(old)
        self.caption_mob = new_caption
        self.pause(hold)

    def replace_caption_only(self, text):
        new_caption = Text(text, font_size=30, color=self.TEXT, slant="ITALIC")
        if new_caption.width > config.frame_width - 1.0:
            new_caption.scale((config.frame_width - 1.0) / new_caption.width)
        new_caption.to_edge(DOWN, buff=0.55)
        new_caption.set_stroke(self.BG, width=5, background=True)
        new_caption.set_z_index(1000)
        self.add_fixed_in_frame_mobjects(new_caption)
        if self.caption_mob is None:
            self.play(FadeIn(new_caption, shift=0.08 * UP), run_time=0.35)
        else:
            old = self.caption_mob
            self.play(FadeOut(old), FadeIn(new_caption, shift=0.08 * UP), run_time=0.35)
            self.remove(old)
        self.caption_mob = new_caption

    def make_formula(self, formula_id):
        spec = self.FORMULAS[formula_id]
        formula = MathTex(*spec["parts"], color=self.TEXT)
        formula.scale(spec["scale"])
        if formula.width > config.frame_width - 1.2:
            formula.scale((config.frame_width - 1.2) / formula.width)
        formula.move_to(ORIGIN)
        formula.set_z_index(20)
        for index, color in spec["colors"].items():
            if index < len(formula):
                formula[index].set_color(color)
        return formula

    def show_formula(self, formula_id, run_time=1.0, support=None):
        self.clear_sets()
        if self.current_formula is not None:
            self.play(FadeOut(self.current_formula), run_time=0.35)
            self.current_formula = None
        formula = self.make_formula(formula_id)
        if support is not None:
            support.set_z_index(-5)
            self.current_sets.add(support)
            self.play(LaggedStart(FadeIn(support), Write(formula), lag_ratio=0.25), run_time=run_time)
        else:
            self.play(Write(formula), run_time=run_time)
        self.current_formula = formula

    def transform_formula(self, formula_id, run_time=1.2):
        self.clear_sets()
        target = self.make_formula(formula_id)
        if self.current_formula is None:
            self.play(Write(target), run_time=run_time)
        else:
            old = self.current_formula
            self.play(ReplacementTransform(old, target), run_time=run_time)
        self.current_formula = target

    def term_tour(self, part_index, color, caption, zoom=2.4, dim=0.22, run_time=1.4, hold=1.1):
        formula = self.current_formula
        if formula is None or part_index >= len(formula):
            return
        self.replace_caption_only(caption)
        formula.save_state()
        target = formula[part_index]
        target.set_z_index(25)
        self.glow = target.copy()
        self.glow.set_color(color)
        self.glow.set_stroke(color, width=8, opacity=0.38)
        self.glow.set_fill(color, opacity=0.20)
        self.glow.set_z_index(18)
        dim_anims = []
        for i, part in enumerate(formula):
            if i != part_index:
                dim_anims.append(part.animate.set_opacity(dim))
        dim_anims.append(target.animate.set_opacity(1).set_color(color))
        self.play(FadeIn(self.glow, scale=1.08), *dim_anims, run_time=0.45)
        self.move_camera(phi=0, theta=-90 * DEGREES, frame_center=target.get_center(), zoom=zoom, run_time=run_time)
        self.pause(hold)

    def pull_back(self, run_time=0.9, hold=0.8):
        added = []
        if self.current_formula is not None and hasattr(self.current_formula, "saved_state"):
            added.append(Restore(self.current_formula))
        if self.glow is not None:
            added.append(FadeOut(self.glow))
        self.move_camera(
            phi=0,
            theta=-90 * DEGREES,
            frame_center=ORIGIN,
            zoom=1,
            run_time=run_time,
            added_anims=added,
        )
        self.glow = None
        self.pause(hold)

    def tour_sequence(self, tours):
        for part, color, caption, zoom, dim, move_time, hold, pull_time, pull_hold in tours:
            self.term_tour(part, color, caption, zoom=zoom, dim=dim, run_time=move_time, hold=hold)
            self.pull_back(run_time=pull_time, hold=pull_hold)

    def run_set_piece(self, group, caption, phi, theta, zoom, tilt_time, orbit_time, rate, tilt_hold, orbit_hold, return_time):
        self.current_sets.add(group)
        self.play(FadeIn(group), run_time=0.7)
        self.replace_caption_only(caption)
        self.move_camera(phi=phi, theta=theta, zoom=zoom, frame_center=ORIGIN, run_time=tilt_time)
        self.pause(tilt_hold)
        self.move_camera(
            phi=phi,
            theta=theta + rate * orbit_time * TAU,
            zoom=zoom,
            frame_center=ORIGIN,
            run_time=orbit_time,
            rate_func=linear,
        )
        self.pause(orbit_hold)
        self.move_camera(phi=0, theta=-90 * DEGREES, zoom=1, frame_center=ORIGIN, run_time=return_time)
        self.clear_sets(run_time=0.4)
        self.pause(0.8)

    def causal_disk(self):
        disk = Circle(radius=2.0, color=self.BLUE, stroke_width=2)
        disk.set_fill(self.BLUE, opacity=0.05)
        origin = Dot(ORIGIN, color=self.BLUE, radius=0.06)
        return VGroup(disk, origin)

    def wave_support(self):
        wave = ParametricFunction(
            lambda t: [t, 0.22 * math.sin(4 * t), 0],
            t_range=[-2.2, 2.2],
            color=self.CORAL,
            stroke_width=4,
        ).shift(DOWN * 1.35)
        haze = wave.copy().set_stroke(self.CORAL, width=12, opacity=0.18)
        return VGroup(haze, wave)

    def narrow_packet(self):
        packet = ParametricFunction(
            lambda t: [t, 0.45 * math.exp(-2.6 * t * t), 0],
            t_range=[-2.0, 2.0],
            color=self.CORAL,
            stroke_width=4,
        ).shift(UP * 1.25)
        base = Line(LEFT * 2, RIGHT * 2, color=self.GRAY, stroke_opacity=0.35).shift(UP * 1.25)
        return VGroup(base, packet)

    def tiny_ruler(self):
        line = Line(LEFT * 0.75, RIGHT * 0.75, color=self.OLIVE, stroke_width=4).shift(DOWN * 1.35)
        ticks = VGroup()
        for x in [-0.75, -0.35, 0, 0.35, 0.75]:
            ticks.add(Line([x, -1.48, 0], [x, -1.22, 0], color=self.OLIVE, stroke_width=2))
        return VGroup(line, ticks)

    def expanding_ring(self):
        rings = VGroup()
        for r, op in [(1.2, 0.25), (1.8, 0.16), (2.4, 0.10)]:
            rings.add(Circle(radius=r, color=self.GOLD, stroke_width=2, stroke_opacity=op))
        return rings.shift(DOWN * 0.05)

    def two_ruler_ticks(self):
        base = Line(LEFT * 4.8, RIGHT * 4.8, color=self.GRAY, stroke_width=2, stroke_opacity=0.55).shift(DOWN * 1.45)
        left_tick = Line([-4.6, -1.1, 0], [-4.6, -1.8, 0], color=self.OLIVE, stroke_width=5)
        right_tick = Line([4.6, -1.1, 0], [4.6, -1.8, 0], color=self.GOLD, stroke_width=5)
        labels = VGroup(
            Text("Planck", font_size=22, color=self.OLIVE).next_to(left_tick, DOWN, buff=0.15),
            Text("horizon", font_size=22, color=self.GOLD).next_to(right_tick, DOWN, buff=0.15),
        )
        return VGroup(base, left_tick, right_tick, labels)

    def density_box(self):
        box = Square(side_length=1.4, color=self.OLIVE, stroke_width=3).shift(DOWN * 1.35)
        fill = VGroup(*[
            Dot([0.45 * math.cos(k * TAU / 8), -1.35 + 0.45 * math.sin(k * TAU / 8), 0], radius=0.035, color=self.GOLD)
            for k in range(8)
        ])
        return VGroup(box, fill)

    def upper_density_plate(self):
        plate = Rectangle(width=4.2, height=0.38, color=self.CORAL, fill_color=self.CORAL, fill_opacity=0.16)
        plate.shift(UP * 1.3)
        sparks = VGroup(*[
            Dot([x, 1.3 + 0.12 * math.sin(5 * x), 0], radius=0.025, color=self.CORAL)
            for x in [-1.7, -1.2, -0.8, -0.3, 0.2, 0.7, 1.1, 1.6]
        ])
        return VGroup(plate, sparks)

    def light_cone_set(self):
        cone = Surface(
            lambda u, v: [v * math.cos(u), v * math.sin(u), 2.8 * (1 - v / 2.2)],
            u_range=[0, TAU],
            v_range=[0, 2.2],
            resolution=(32, 10),
            fill_opacity=0.14,
            checkerboard_colors=[self.BLUE, self.BLUE],
        )
        cone.set_stroke(self.BLUE, width=0.6, opacity=0.45)
        base = Circle(radius=2.2, color=self.BLUE, stroke_width=3, stroke_opacity=0.75)
        origin = Sphere(radius=0.09, resolution=(12, 6)).set_color(self.BLUE).move_to([0, 0, 0.05])
        points = VGroup()
        for k in range(18):
            angle = k * TAU / 18
            r = 2.75 + 0.22 * (k % 3)
            points.add(Dot([r * math.cos(angle), r * math.sin(angle), 0], radius=0.035, color=self.GRAY).set_opacity(0.22))
        return VGroup(cone, base, origin, points)

    def curved_geometry_set(self):
        surface = Surface(
            lambda u, v: [u, v, -0.85 * math.exp(-0.55 * (u * u + v * v))],
            u_range=[-3, 3],
            v_range=[-3, 3],
            resolution=(18, 18),
            fill_opacity=0.12,
            checkerboard_colors=[self.OLIVE, self.OLIVE],
        )
        surface.set_stroke(self.OLIVE, width=0.45, opacity=0.55)
        packet = Sphere(radius=0.25, resolution=(16, 8)).set_color(self.CORAL).move_to([0, 0, 0.35])
        orbit = ParametricFunction(
            lambda t: [1.7 * math.cos(t), 1.7 * math.sin(t), -0.25 * math.exp(-0.5)],
            t_range=[0, TAU],
            color=self.GRAY,
            stroke_width=2,
        )
        return VGroup(surface, orbit, packet)

    def bronstein_cube_set(self):
        cube = Cube(side_length=3.0, fill_opacity=0.035, stroke_width=1.5)
        cube.set_stroke(self.GRAY, opacity=0.45)
        x_axis = Line3D(start=[-1.5, -1.5, -1.5], end=[1.7, -1.5, -1.5], color=self.BLUE, thickness=0.025)
        y_axis = Line3D(start=[-1.5, -1.5, -1.5], end=[-1.5, 1.7, -1.5], color=self.OLIVE, thickness=0.025)
        z_axis = Line3D(start=[-1.5, -1.5, -1.5], end=[-1.5, -1.5, 1.7], color=self.CORAL, thickness=0.025)
        corner = Sphere(radius=0.14, resolution=(16, 8)).set_color(self.GOLD).move_to([1.5, 1.5, 1.5])
        halo = Sphere(radius=0.26, resolution=(16, 8)).set_color(self.GOLD).set_opacity(0.18).move_to([1.5, 1.5, 1.5])
        return VGroup(cube, x_axis, y_axis, z_axis, halo, corner)

    def expansion_grid_set(self):
        lines = VGroup()
        for p in [-3, -2, -1, 0, 1, 2, 3]:
            lines.add(Line([-3, p, 0], [3, p, 0], color=self.GRAY, stroke_width=1, stroke_opacity=0.35))
            lines.add(Line([p, -3, 0], [p, 3, 0], color=self.GRAY, stroke_width=1, stroke_opacity=0.35))
        points = VGroup()
        for x in [-2, -1, 0, 1, 2]:
            for y in [-2, -1, 0, 1, 2]:
                if x == 0 and y == 0:
                    continue
                points.add(Sphere(radius=0.045, resolution=(8, 4)).set_color(self.GOLD).move_to([1.18 * x, 1.18 * y, 0.04]))
        glow = Circle(radius=3.3, color=self.GOLD, stroke_width=8, stroke_opacity=0.18)
        return VGroup(lines, glow, points)

    def log_elevator_set(self):
        spine = Line3D(start=[0, 0, -3.0], end=[0, 0, 3.0], color=self.GRAY, thickness=0.018)
        ticks = VGroup()
        labels = VGroup()
        positions = [-3, -2, -1, 0, 1, 2, 3]
        label_texts = ["0", "10", "20", "30", "40", "50", "61"]
        for z, label in zip(positions, label_texts):
            color = self.GOLD if label in ["0", "61"] else self.GRAY
            ticks.add(Line3D(start=[-0.28, 0, z], end=[0.28, 0, z], color=color, thickness=0.012))
            labels.add(Text(label, font_size=20, color=color).move_to([0.65, 0, z]))
        lower = Text("Planck", font_size=22, color=self.OLIVE).move_to([-0.9, 0, -3.0])
        upper = Text("horizon", font_size=22, color=self.GOLD).move_to([-0.95, 0, 3.0])
        return VGroup(spine, ticks, labels, lower, upper)

    def density_canyon_set(self):
        upper = Rectangle(width=4.8, height=1.0, color=self.CORAL, fill_color=self.CORAL, fill_opacity=0.18).move_to([0, 0, 2.3])
        lower = Rectangle(width=4.8, height=1.0, color=self.GOLD, fill_color=self.GOLD, fill_opacity=0.12).move_to([0, 0, -2.3])
        rails = VGroup(
            Line3D(start=[-2.4, 0, -2.3], end=[-2.4, 0, 2.3], color=self.GRAY, thickness=0.012),
            Line3D(start=[2.4, 0, -2.3], end=[2.4, 0, 2.3], color=self.GRAY, thickness=0.012),
        )
        digits = VGroup()
        for k, z in enumerate([-1.6, -0.8, 0, 0.8, 1.6]):
            digits.add(Text("10", font_size=24, color=self.GOLD).move_to([0.0, -0.55, z]))
            digits.add(Text(str(24 * (k + 1)), font_size=16, color=self.GRAY).move_to([0.38, -0.55, z + 0.12]))
        upper_label = Text("naive Planck density", font_size=24, color=self.CORAL).move_to([0, -0.85, 2.3])
        lower_label = Text("observed dark energy", font_size=24, color=self.GOLD).move_to([0, -0.85, -2.3])
        return VGroup(upper, lower, rails, digits, upper_label, lower_label)

    def wave_packet_transform(self):
        dot = Dot(DOWN * 1.45, color=self.CORAL, radius=0.11)
        wave = ParametricFunction(
            lambda t: [t, -1.45 + 0.35 * math.exp(-0.55 * t * t) * math.cos(6 * t), 0],
            t_range=[-2.4, 2.4],
            color=self.CORAL,
            stroke_width=4,
        )
        haze = wave.copy().set_stroke(self.CORAL, width=14, opacity=0.16)
        packet = VGroup(haze, wave)
        self.current_sets.add(dot)
        self.play(FadeIn(dot), run_time=0.4)
        self.replace_caption_only("A point becomes a probability wave.")
        self.move_camera(phi=0, theta=-90 * DEGREES, frame_center=DOWN * 1.4, zoom=1, run_time=1.4)
        self.play(ReplacementTransform(dot, packet), run_time=1.0)
        self.current_sets.add(packet)
        self.pause(1.0)
        self.move_camera(phi=0, theta=-90 * DEGREES, frame_center=ORIGIN, zoom=1, run_time=0.8)

    def final_glows(self):
        if self.current_formula is None:
            return
        glows = VGroup()
        for index, color in [(1, self.BLUE), (3, self.OLIVE), (5, self.CORAL), (7, self.GOLD)]:
            if index < len(self.current_formula):
                glow = self.current_formula[index].copy()
                glow.set_color(color)
                glow.set_stroke(color, width=8, opacity=0.34)
                glow.set_fill(color, opacity=0.18)
                glow.set_z_index(18)
                glows.add(glow)
        self.play(LaggedStart(*[FadeIn(g, scale=1.08) for g in glows], lag_ratio=0.18), run_time=1.0)
        self.pause(0.8)
        self.play(glows.animate.set_opacity(0.45), run_time=0.6)
