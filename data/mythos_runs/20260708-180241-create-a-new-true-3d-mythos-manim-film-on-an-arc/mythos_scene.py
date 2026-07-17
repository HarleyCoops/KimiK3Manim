from manim import *
import numpy as np


class ExceptionalPointMonodromyJourney(ThreeDScene):
    def construct(self):
        self.BG = "#f3ead7"
        self.TEXT = "#211a14"
        self.CORAL = "#a94f36"
        self.BLUE = "#285f87"
        self.OLIVE = "#4f6239"
        self.GOLD = "#9a6738"
        self.GRAY = "#6f685f"

        self.camera.background_color = self.BG
        self.set_camera_orientation(phi=0 * DEGREES, theta=-90 * DEGREES, zoom=1)

        self.caption_mob = None
        self.world_mobjects = []
        self.formula_specs = {}

        self.headline("A moving point will drive the whole story.", 72)
        self.wait(0.7)
        plane = self.track(self.make_complex_plane())
        self.play(Create(plane), run_time=1.0)
        f = self.show_formula("act1_cartesian_parameter", UP * 2.25, 8.8, 0.8)
        self.caption("z is the moving input, not an eigenvalue yet.", 0.8)
        self.term_tour(f, [
            (0, self.CORAL, 2.4, "z is the actor whose path drives the story.", 1.2),
            (2, self.OLIVE, 2.0, "x measures real motion across the plane.", 1.2),
            (4, self.GRAY, 2.0, "i y measures imaginary motion up the plane.", 1.2),
        ])
        self.pull_back(1.0)
        self.wait(0.9)

        self.headline("The same point can be described by distance and turn.", 70)
        polar = self.track(self.make_polar_loop())
        self.play(Create(polar), run_time=1.0)
        f = self.show_formula("act2_polar_form", RIGHT * 3.0 + UP * 0.25, 5.4, 0.8)
        self.caption("Radius stays fixed; the phase records the turn.", 0.8)
        self.term_tour(f, [
            (2, self.OLIVE, 2.2, "r holds the distance while the loop runs.", 1.35),
            (3, self.GOLD, 2.4, "The exponential is the rotating direction.", 1.35),
        ])
        self.pull_back(0.9)

        self.headline("One circuit changes the angle's memory.", 70)
        faint_loop = self.track(self.make_faint_loop())
        self.play(FadeIn(faint_loop), run_time=0.4)
        f = self.show_formula("act2_one_full_loop", ORIGIN, 9.8, 1.0)
        self.caption("Position returns, but theta has gained one full turn.", 0.8)
        self.term_tour(f, [
            (0, self.GOLD, 2.3, "Theta is the clock for accumulated turning.", 1.35),
            (2, self.GOLD, 2.6, "Adding 2 pi means one complete circuit.", 1.35),
        ])
        self.pull_back(1.0)
        self.wait(1.0)

        self.headline("Now the point enters one matrix slot.", 72)
        f = self.show_formula("act3_matrix_family", ORIGIN, 8.8, 0.9)
        self.caption("Only one matrix entry listens to z.", 0.8)
        self.term_tour(f, [
            (0, self.OLIVE, 2.2, "A of z is a family, not one matrix.", 1.45),
            (2, self.OLIVE, 2.5, "The lower-left slot is the only moving slot.", 1.45),
        ])
        self.pull_back(0.9)

        self.headline("The same matrix can expose its moving slot.", 68)
        f = self.show_formula("act3_moving_entry_decomposition", ORIGIN, 12.0, 1.2)
        self.caption("The same matrix is rewritten to isolate the moving entry.", 0.8)
        self.term_tour(f, [
            (4, self.CORAL, 2.5, "z is the only changing amount.", 1.45),
            (5, self.OLIVE, 2.4, "The selector places z in one slot.", 1.45),
        ])
        self.pull_back(0.9)
        self.wait(0.9)

        self.headline("Eigenvalues appear when a shifted matrix collapses.", 68)
        f = self.show_formula("act4_shifted_matrix", ORIGIN, 9.8, 0.9)
        self.caption("Lambda is the output value being tested.", 0.8)
        self.term_tour(f, [
            (0, self.OLIVE, 2.4, "Subtracting lambda prepares the eigenvalue test.", 1.5),
            (2, self.BLUE, 2.5, "The diagonal changes; the z slot stays put.", 1.5),
        ])
        self.pull_back(0.9)

        self.headline("Collapse is tested by determinant zero.", 70)
        f = self.show_formula("act4_characteristic_equation", ORIGIN, 9.5, 1.0)
        self.caption("Eigenvalues make the shifted matrix collapse.", 0.8)
        self.term_tour(f, [
            (0, self.OLIVE, 2.5, "The determinant detects rank collapse.", 1.45),
            (2, self.OLIVE, 2.4, "Zero marks the allowed eigenvalue test.", 1.45),
        ])
        self.pull_back(0.9)
        self.wait(0.9)

        self.headline("The calculation leaves a square minus the input.", 68)
        f = self.show_formula("act5_determinant_expansion", ORIGIN, 12.0, 1.0)
        self.caption("Diagonal product minus off-diagonal product leaves lambda squared minus z.", 0.8)
        self.term_tour(f, [
            (2, self.BLUE, 2.5, "Two negative lambdas multiply to positive lambda squared.", 1.5),
            (4, self.CORAL, 2.5, "The off-diagonal product subtracts the moving z.", 1.5),
            (6, self.OLIVE, 2.6, "The determinant simplifies to lambda squared minus z.", 1.5),
        ])
        self.pull_back(0.9)

        self.headline("The algebraic heart is lambda squared equals z.", 68)
        f = self.show_formula("act5_square_equation", ORIGIN, 10.8, 1.1)
        self.caption("The square of lambda, not lambda, equals z.", 0.8)
        self.term_tour(f, [
            (0, self.OLIVE, 2.3, "The characteristic equation must vanish.", 1.45),
            (4, self.BLUE, 2.6, "The eigenvalue is being squared.", 1.45),
            (6, self.CORAL, 2.6, "z is what that square must equal.", 1.45),
        ])
        self.pull_back(1.0)
        self.wait(1.1)

        self.headline("A square has two opposite roots.", 72)
        f = self.show_formula("act6_two_roots", ORIGIN, 10.5, 1.0)
        self.caption("Every nonzero z gives two opposite square-root choices.", 0.8)
        self.term_tour(f, [
            (0, self.BLUE, 2.4, "The plus name chooses one local root.", 1.35),
            (2, self.BLUE, 2.5, "A square root squares back to z.", 1.35),
            (4, self.BLUE, 2.4, "The minus name chooses the opposite root.", 1.35),
            (6, self.BLUE, 2.5, "Opposite signs share one square-root relation.", 1.35),
        ])
        self.pull_back(0.9)

        self.headline("At the origin, the two roots pinch together.", 68)
        f = self.show_formula("act6_origin_collapse", ORIGIN, 9.8, 1.1)
        self.caption("At z equals zero, the two roots collapse.", 0.8)
        self.term_tour(f, [
            (0, self.CORAL, 2.5, "The input sits exactly at the origin.", 1.5),
            (2, self.BLUE, 2.7, "Both branch values collapse to zero.", 1.5),
        ])
        self.pull_back(0.9)
        self.wait(1.0)

        self.headline("The square root cuts angle in half.", 74)
        f = self.show_formula("act7_square_root_half_angle", ORIGIN, 11.2, 1.0)
        self.caption("Square roots keep radius square-rooted and halve angle.", 0.8)
        self.term_tour(f, [
            (2, self.GOLD, 2.4, "z carries radius r and angle theta.", 1.35),
            (4, self.BLUE, 2.4, "lambda is the square-root output.", 1.35),
        ])
        self.caption("The output angle is only half the input angle.", 0.7)
        self.focus_part(f, 6, self.GOLD, 3.0, 3.2, hold=1.6, pull_time=2.1)
        self.run_half_angle_set_piece(f)
        f2 = self.transform_formula(f, "act7_argument_relation", ORIGIN, 8.8, 1.0)
        self.caption("Angle of lambda is half the angle of z.", 0.8)
        self.term_tour(f2, [
            (0, self.BLUE, 2.4, "arg lambda means the eigenvalue angle.", 1.4),
            (2, self.GOLD, 2.9, "One half is the mechanism.", 1.4),
            (3, self.CORAL, 2.4, "arg z means the parameter angle.", 1.4),
        ])
        self.pull_back(1.0)
        self.wait(1.1)

        self.headline("One loop swaps the eigenvalue names.", 72)
        f = self.show_formula("act8_one_loop_swap", ORIGIN, 11.8, 1.0)
        self.caption("One parameter loop forces plus to land on minus.", 0.8)
        self.term_tour(f, [
            (2, self.GOLD, 2.5, "The downstairs angle adds one complete turn.", 1.45),
            (4, self.BLUE, 2.4, "Start by following the plus branch.", 1.45),
            (6, self.BLUE, 2.8, "The lifted value becomes its opposite.", 1.45),
            (8, self.BLUE, 2.6, "That opposite is the local minus branch.", 1.45),
        ])
        self.pull_back(0.9)
        self.run_branch_surface_set_piece(f)

        self.headline("The second loop brings the name home.", 70)
        f = self.show_formula("act8_two_loop_return", ORIGIN, 10.8, 1.0)
        self.caption("Two input loops are needed for closure.", 0.8)
        self.term_tour(f, [
            (2, self.GOLD, 2.6, "Two circuits add four pi downstairs.", 1.5),
            (6, self.BLUE, 2.7, "After two loops, the branch name returns.", 1.5),
        ])
        self.pull_back(1.0)
        self.wait(1.0)

        self.headline("Ordinary crossings keep their labels.", 72)
        f = self.show_formula("act9_ordinary_crossing_labels", ORIGIN, 11.5, 1.0)
        self.caption("Ordinary crossings preserve labels through the meeting.", 0.8)
        self.term_tour(f, [
            (0, self.GRAY, 2.4, "The first label remains itself.", 1.35),
            (4, self.GRAY, 2.4, "The second label also remains itself.", 1.35),
            (6, self.OLIVE, 2.5, "No loop-induced exchange occurs here.", 1.35),
        ])
        self.pull_back(0.9)

        self.headline("A branch point fails that label test.", 70)
        f = self.show_formula("act9_branch_point_label_exchange", ORIGIN, 10.6, 1.1)
        self.caption("Branch points are revealed by identity exchange.", 0.8)
        self.term_tour(f, [
            (0, self.BLUE, 2.5, "Plus is only a local name.", 1.45),
            (1, self.GOLD, 2.7, "The loop around zero performs the test.", 1.45),
            (2, self.BLUE, 2.5, "The same path now has the minus name.", 1.45),
        ])
        self.pull_back(1.0)
        self.wait(1.0)

        self.headline("At zero, the matrix is defective.", 72)
        f = self.show_formula("act10_exceptional_matrix_at_origin", ORIGIN, 10.8, 1.0)
        self.caption("At zero, the matrix becomes algebraically defective.", 0.8)
        self.term_tour(f, [
            (0, self.OLIVE, 2.4, "A of zero is the pinched matrix.", 1.35),
            (2, self.OLIVE, 2.5, "The fixed one prevents diagonalization.", 1.35),
            (4, self.BLUE, 2.5, "The equation collapses to lambda squared zero.", 1.35),
            (6, self.OLIVE, 2.4, "Both eigenvalue branches meet at zero.", 1.35),
        ])
        self.pull_back(0.9)

        self.headline("Exceptional means one direction is missing.", 70)
        f = self.show_formula("act10_defective_eigenvector_count", ORIGIN, 11.3, 1.1)
        self.caption("One eigenvector direction cannot serve two algebraic counts.", 0.8)
        self.term_tour(f, [
            (0, self.OLIVE, 2.5, "The eigenspace has one direction.", 1.35),
            (2, self.OLIVE, 2.5, "Only one eigenvector direction remains.", 1.35),
            (4, self.BLUE, 2.5, "Algebraic multiplicity counts repeated roots.", 1.35),
            (6, self.BLUE, 2.5, "Zero is counted twice algebraically.", 1.35),
        ])
        self.pull_back(0.9)

        self.headline("The film closes with the loop test.", 70)
        f = self.show_formula("act10_monodromy_summary", ORIGIN, 11.6, 1.1)
        self.caption("Exceptional means one loop exchanges eigenvalue identity.", 0.8)
        self.term_tour(f, [
            (0, self.GOLD, 2.5, "One loop performs the swap.", 1.35),
            (2, self.BLUE, 2.7, "Plus and minus exchange local names.", 1.35),
            (4, self.GOLD, 2.5, "Two loops complete the cycle.", 1.35),
            (6, self.BLUE, 2.7, "The original name returns after two circuits.", 1.35),
        ])
        self.pull_back(1.2)
        self.wait(1.6)

    def headline(self, text, font_size):
        self.clear_world(0.45)
        self.set_camera_orientation(phi=0 * DEGREES, theta=-90 * DEGREES, zoom=1)
        mob = Text(text, font_size=font_size, color=self.TEXT)
        if mob.width > 12.2:
            mob.scale_to_fit_width(12.2)
        mob.move_to(ORIGIN)
        mob.set_opacity(0)
        self.add_fixed_in_frame_mobjects(mob)
        self.play(mob.animate.set_opacity(1), run_time=0.45)
        self.wait(0.75)
        self.play(FadeOut(mob), run_time=0.45)
        self.remove(mob)

    def caption(self, text, hold=0.0):
        if self.caption_mob is not None:
            self.play(FadeOut(self.caption_mob), run_time=0.16)
            self.remove(self.caption_mob)
            self.caption_mob = None
        mob = Text(text, font_size=30, slant=ITALIC, color=self.TEXT)
        if mob.width > 12.2:
            mob.scale_to_fit_width(12.2)
        mob.to_edge(DOWN, buff=0.33)
        mob.set_opacity(0)
        self.add_fixed_in_frame_mobjects(mob)
        self.caption_mob = mob
        self.play(mob.animate.set_opacity(1), run_time=0.25)
        if hold:
            self.wait(hold)

    def clear_world(self, run_time=0.45):
        anims = [FadeOut(m) for m in self.world_mobjects]
        if self.caption_mob is not None:
            anims.append(FadeOut(self.caption_mob))
        if anims:
            self.play(*anims, run_time=run_time)
        self.world_mobjects = []
        if self.caption_mob is not None:
            self.remove(self.caption_mob)
            self.caption_mob = None

    def track(self, mob):
        self.world_mobjects.append(mob)
        return mob

    def show_formula(self, name, position, max_width, run_time):
        mob = self.make_formula(name, position, max_width)
        self.track(mob)
        self.play(Write(mob), run_time=run_time)
        return mob

    def transform_formula(self, old, name, position, max_width, run_time):
        new = self.make_formula(name, position, max_width)
        self.play(ReplacementTransform(old, new), run_time=run_time)
        if old in self.world_mobjects:
            self.world_mobjects.remove(old)
        self.track(new)
        return new

    def pull_back(self, run_time=0.8):
        self.move_camera(
            phi=0 * DEGREES,
            theta=-90 * DEGREES,
            zoom=1,
            frame_center=ORIGIN,
            run_time=run_time,
        )

    def term_tour(self, formula, stops):
        for part_index, color, zoom, text, run_time in stops:
            self.caption(text, 0.0)
            self.focus_part(formula, part_index, color, zoom, run_time, hold=0.45, pull_time=0.65)

    def focus_part(self, formula, part_index, color, zoom, run_time, hold=0.45, pull_time=0.65):
        self.restore_formula_colors(formula)
        active = formula[part_index]
        dim_anims = []
        for i, part in enumerate(formula):
            if i == part_index:
                dim_anims.append(part.animate.set_opacity(1).set_color(color))
            else:
                dim_anims.append(part.animate.set_opacity(0.4).set_color(self.GRAY))
        self.play(*dim_anims, run_time=0.25)

        glow = active.copy()
        glow.set_color(color)
        glow.set_stroke(color=color, width=10, opacity=0.38)
        glow.set_fill(color=color, opacity=0.12)
        box = SurroundingRectangle(active, buff=0.08, color=color, stroke_width=2)
        box.set_opacity(0.72)
        halo = VGroup(glow, box)
        self.add(halo)
        self.add(formula)
        self.play(FadeIn(glow), Create(box), run_time=0.2)

        self.move_camera(
            phi=0 * DEGREES,
            theta=-90 * DEGREES,
            frame_center=active.get_center(),
            zoom=zoom,
            run_time=run_time,
        )
        self.wait(hold)
        self.move_camera(
            phi=0 * DEGREES,
            theta=-90 * DEGREES,
            frame_center=ORIGIN,
            zoom=1,
            run_time=pull_time,
        )
        self.play(FadeOut(halo), run_time=0.18)
        self.restore_formula_colors(formula)
        self.wait(0.18)

    def make_formula(self, name, position, max_width):
        data = {
            "act1_cartesian_parameter": (
                [r"z", "=", r"x", "+", r"\mathrm{i}y"],
                {0: self.CORAL, 2: self.OLIVE, 4: self.GRAY},
                []
            ),
            "act2_polar_form": (
                [r"z", "=", r"r", r"e^{\mathrm{i}\theta}"],
                {0: self.CORAL, 2: self.OLIVE, 3: self.GOLD},
                []
            ),
            "act2_one_full_loop": (
                [r"\theta", r"\mapsto", r"\theta+2\pi", r"\quad", r"z", r"\mapsto", r"z"],
                {0: self.GOLD, 2: self.GOLD, 4: self.CORAL, 6: self.CORAL},
                []
            ),
            "act3_matrix_family": (
                [r"A(z)", "=", r"\begin{pmatrix}0&1\\z&0\end{pmatrix}"],
                {0: self.OLIVE, 2: self.OLIVE},
                [(r"z", self.CORAL)]
            ),
            "act3_moving_entry_decomposition": (
                [r"A(z)", "=", r"\begin{pmatrix}0&1\\0&0\end{pmatrix}", "+", r"z", r"\begin{pmatrix}0&0\\1&0\end{pmatrix}"],
                {0: self.OLIVE, 2: self.GRAY, 4: self.CORAL, 5: self.OLIVE},
                []
            ),
            "act4_shifted_matrix": (
                [r"A(z)-\lambda I", "=", r"\begin{pmatrix}-\lambda&1\\z&-\lambda\end{pmatrix}"],
                {0: self.OLIVE, 2: self.OLIVE},
                [(r"\lambda", self.BLUE), (r"z", self.CORAL)]
            ),
            "act4_characteristic_equation": (
                [r"\det(A(z)-\lambda I)", "=", "0"],
                {0: self.OLIVE, 2: self.OLIVE},
                [(r"\lambda", self.BLUE), (r"z", self.CORAL)]
            ),
            "act5_determinant_expansion": (
                [r"\det\begin{pmatrix}-\lambda&1\\z&-\lambda\end{pmatrix}", "=", r"(-\lambda)(-\lambda)", "-", r"(1)(z)", "=", r"\lambda^2-z"],
                {0: self.OLIVE, 2: self.BLUE, 4: self.CORAL, 6: self.OLIVE},
                [(r"\lambda", self.BLUE), (r"z", self.CORAL)]
            ),
            "act5_square_equation": (
                [r"\lambda^2-z", "=", "0", r"\Longleftrightarrow", r"\lambda^2", "=", r"z"],
                {0: self.OLIVE, 4: self.BLUE, 6: self.CORAL},
                [(r"\lambda", self.BLUE), (r"z", self.CORAL)]
            ),
            "act6_two_roots": (
                [r"\lambda_+", "=", r"\sqrt{z}", r"\quad", r"\lambda_-", "=", r"-\sqrt{z}"],
                {0: self.BLUE, 2: self.BLUE, 4: self.BLUE, 6: self.BLUE},
                [(r"z", self.CORAL)]
            ),
            "act6_origin_collapse": (
                [r"z=0", r"\Longrightarrow", r"\lambda_+=\lambda_-=0"],
                {0: self.CORAL, 2: self.BLUE},
                []
            ),
            "act7_square_root_half_angle": (
                [r"z", "=", r"r e^{\mathrm{i}\theta}", r"\Longrightarrow", r"\lambda", "=", r"\sqrt{r}e^{\mathrm{i}\theta/2}"],
                {0: self.CORAL, 2: self.GOLD, 4: self.BLUE, 6: self.GOLD},
                [(r"r", self.OLIVE), (r"\theta", self.GOLD)]
            ),
            "act7_argument_relation": (
                [r"\arg(\lambda)", "=", r"\frac{1}{2}", r"\arg(z)"],
                {0: self.BLUE, 2: self.GOLD, 3: self.CORAL},
                []
            ),
            "act8_one_loop_swap": (
                [r"\theta", r"\mapsto", r"\theta+2\pi", r"\Longrightarrow", r"\lambda_+", r"\mapsto", r"-\lambda_+", "=", r"\lambda_-"],
                {0: self.GOLD, 2: self.GOLD, 4: self.BLUE, 6: self.BLUE, 8: self.BLUE},
                []
            ),
            "act8_two_loop_return": (
                [r"\theta", r"\mapsto", r"\theta+4\pi", r"\Longrightarrow", r"\lambda_+", r"\mapsto", r"\lambda_+"],
                {0: self.GOLD, 2: self.GOLD, 4: self.BLUE, 6: self.BLUE},
                []
            ),
            "act9_ordinary_crossing_labels": (
                [r"\mu_1", r"\longrightarrow", r"\mu_1", r"\quad", r"\mu_2", r"\longrightarrow", r"\mu_2\;\text{preserved}"],
                {0: self.GRAY, 2: self.GRAY, 4: self.GRAY, 6: self.OLIVE},
                []
            ),
            "act9_branch_point_label_exchange": (
                [r"\lambda_+", r"\xrightarrow{\text{loop around }z=0}", r"\lambda_-"],
                {0: self.BLUE, 1: self.GOLD, 2: self.BLUE},
                [(r"z=0", self.CORAL)]
            ),
            "act10_exceptional_matrix_at_origin": (
                [r"A(0)", "=", r"\begin{pmatrix}0&1\\0&0\end{pmatrix}", r"\quad", r"\lambda^2", "=", "0"],
                {0: self.OLIVE, 2: self.OLIVE, 4: self.BLUE, 6: self.OLIVE},
                []
            ),
            "act10_defective_eigenvector_count": (
                [r"\dim\ker A(0)", "=", "1", r"\quad", r"\operatorname{algmult}(0)", "=", "2"],
                {0: self.OLIVE, 2: self.OLIVE, 4: self.BLUE, 6: self.BLUE},
                []
            ),
            "act10_monodromy_summary": (
                [r"1\text{ loop}", r"\Rightarrow", r"\lambda_+\leftrightarrow\lambda_-", r"\quad", r"2\text{ loops}", r"\Rightarrow", r"\lambda_+\to\lambda_+"],
                {0: self.GOLD, 2: self.BLUE, 4: self.GOLD, 6: self.BLUE},
                []
            ),
        }
        parts, colors, nested = data[name]
        mob = MathTex(*parts, color=self.TEXT, font_size=58)
        if mob.width > max_width:
            mob.scale_to_fit_width(max_width)
        mob.move_to(position)
        self.formula_specs[id(mob)] = (colors, nested)
        self.restore_formula_colors(mob)
        return mob

    def restore_formula_colors(self, formula):
        formula.set_opacity(1)
        for part in formula:
            part.set_opacity(1)
            part.set_color(self.TEXT)
        colors, nested = self.formula_specs.get(id(formula), ({}, []))
        for index, color in colors.items():
            if index < len(formula):
                formula[index].set_color(color)
                formula[index].set_opacity(1)
        for tex, color in nested:
            formula.set_color_by_tex(tex, color)

    def make_complex_plane(self):
        x_axis = Line(LEFT * 4.2, RIGHT * 4.2, color=self.OLIVE, stroke_width=3)
        y_axis = Line(DOWN * 2.2, UP * 2.2, color=self.OLIVE, stroke_width=3)
        origin = Dot(ORIGIN, radius=0.045, color=self.GRAY)
        z_dot = Dot(RIGHT * 1.6 + UP * 1.0, radius=0.09, color=self.CORAL)
        z_label = Text("z", font_size=30, color=self.CORAL).next_to(z_dot, UR, buff=0.12)
        x_label = Text("Re z", font_size=25, color=self.OLIVE).next_to(x_axis, RIGHT, buff=0.18)
        y_label = Text("Im z", font_size=25, color=self.OLIVE).next_to(y_axis, UP, buff=0.18)
        i_label = Text("i", font_size=28, color=self.GRAY).next_to(y_axis, LEFT, buff=0.22).shift(UP * 0.75)
        grid = VGroup()
        for x in np.linspace(-4, 4, 9):
            grid.add(Line(DOWN * 2.2 + RIGHT * x, UP * 2.2 + RIGHT * x, color=self.GRAY, stroke_width=0.6, stroke_opacity=0.18))
        for y in np.linspace(-2, 2, 5):
            grid.add(Line(LEFT * 4.2 + UP * y, RIGHT * 4.2 + UP * y, color=self.GRAY, stroke_width=0.6, stroke_opacity=0.18))
        return VGroup(grid, x_axis, y_axis, origin, z_dot, z_label, x_label, y_label, i_label).shift(DOWN * 0.75)

    def make_polar_loop(self):
        center = LEFT * 2.8 + DOWN * 0.15
        radius = 1.45
        circle = Circle(radius=radius, color=self.GRAY, stroke_width=2, stroke_opacity=0.45).move_to(center)
        arm = Line(center, center + radius * RIGHT, color=self.OLIVE, stroke_width=5)
        dot = Dot(center + radius * RIGHT, radius=0.09, color=self.CORAL)
        arc = Arc(radius=0.58, start_angle=0, angle=70 * DEGREES, arc_center=center, color=self.GOLD, stroke_width=5)
        origin = Dot(center, radius=0.05, color=self.GRAY)
        theta = Text("theta", font_size=24, color=self.GOLD).move_to(center + 0.78 * RIGHT + 0.28 * UP)
        r_label = Text("r", font_size=25, color=self.OLIVE).move_to(center + 0.78 * RIGHT + 0.16 * DOWN)
        z_label = Text("z", font_size=28, color=self.CORAL).next_to(dot, UR, buff=0.1)
        return VGroup(circle, arm, dot, arc, origin, theta, r_label, z_label)

    def make_faint_loop(self):
        circle = Circle(radius=1.45, color=self.GRAY, stroke_width=2, stroke_opacity=0.28)
        dot = Dot(circle.point_from_proportion(0), radius=0.08, color=self.CORAL)
        angle = Arc(radius=0.7, start_angle=0, angle=TAU - 0.2, color=self.GOLD, stroke_width=4, stroke_opacity=0.55)
        return VGroup(circle, dot, angle).shift(DOWN * 0.55)

    def run_half_angle_set_piece(self, formula):
        saved = formula.copy()
        self.play(formula.animate.scale(0.55).to_edge(UP, buff=0.35), run_time=0.45)

        group, z_path, lambda_path, z_dot, lambda_dot = self.make_half_angle_lift()
        self.play(FadeIn(group), run_time=0.8)
        self.move_camera(
            phi=60 * DEGREES,
            theta=-55 * DEGREES,
            zoom=1.2,
            frame_center=ORIGIN,
            run_time=1.6,
        )
        self.caption("One downstairs turn becomes a half upstairs turn.", 0.8)
        self.move_camera(
            phi=60 * DEGREES,
            theta=-55 * DEGREES + 0.40,
            zoom=1.2,
            frame_center=ORIGIN,
            run_time=5.0,
            rate_func=linear,
            added_anims=[
                MoveAlongPath(z_dot, z_path),
                MoveAlongPath(lambda_dot, lambda_path),
            ],
        )
        self.move_camera(
            phi=0 * DEGREES,
            theta=-90 * DEGREES,
            zoom=1,
            frame_center=ORIGIN,
            run_time=1.4,
            added_anims=[FadeOut(group)],
        )
        self.play(Transform(formula, saved), run_time=0.5)
        self.restore_formula_colors(formula)

    def make_half_angle_lift(self):
        radius = 1.55
        z_path = ParametricFunction(
            lambda t: np.array([radius * np.cos(t), radius * np.sin(t), -0.9]),
            t_range=[0, TAU],
            color=self.CORAL,
            stroke_width=5,
        )
        lambda_path = ParametricFunction(
            lambda t: np.array([1.25 * np.cos(t / 2), 1.25 * np.sin(t / 2), 0.95]),
            t_range=[0, TAU],
            color=self.BLUE,
            stroke_width=6,
        )
        base_circle = Circle(radius=radius, color=self.CORAL, stroke_width=2, stroke_opacity=0.45).shift(OUT * -0.9)
        z_dot = Dot3D(point=z_path.point_from_proportion(0), radius=0.06, color=self.CORAL)
        lambda_dot = Dot3D(point=lambda_path.point_from_proportion(0), radius=0.07, color=self.BLUE)
        guides = VGroup()
        for alpha in [0, 0.25, 0.5, 0.75, 1.0]:
            guides.add(Line(
                z_path.point_from_proportion(alpha),
                lambda_path.point_from_proportion(alpha),
                color=self.GRAY,
                stroke_width=1,
                stroke_opacity=0.25,
            ))
        return VGroup(base_circle, z_path, lambda_path, guides, z_dot, lambda_dot).shift(DOWN * 0.15), z_path, lambda_path, z_dot, lambda_dot

    def run_branch_surface_set_piece(self, formula):
        saved = formula.copy()
        self.play(formula.animate.scale(0.55).to_edge(UP, buff=0.35), run_time=0.45)

        group, lifted_path, lifted_dot = self.make_branch_surface()
        self.play(FadeIn(group), run_time=0.9)
        self.move_camera(
            phi=62 * DEGREES,
            theta=-50 * DEGREES,
            zoom=1.25,
            frame_center=ORIGIN,
            run_time=1.5,
        )
        self.caption("The surface connects plus to minus after one loop.", 0.8)
        self.move_camera(
            phi=62 * DEGREES,
            theta=-50 * DEGREES + 0.345,
            zoom=1.25,
            frame_center=ORIGIN,
            run_time=4.6,
            rate_func=linear,
            added_anims=[MoveAlongPath(lifted_dot, lifted_path)],
        )
        self.move_camera(
            phi=0 * DEGREES,
            theta=-90 * DEGREES,
            zoom=1,
            frame_center=ORIGIN,
            run_time=1.3,
            added_anims=[FadeOut(group)],
        )
        self.play(Transform(formula, saved), run_time=0.5)
        self.restore_formula_colors(formula)

    def make_branch_surface(self):
        rmax = 2.05
        sheet_plus = Surface(
            lambda r, t: np.array([
                r * np.cos(t),
                r * np.sin(t),
                0.62 * np.sqrt(r) * np.cos(t / 2),
            ]),
            u_range=[0.03, rmax],
            v_range=[0, TAU],
            resolution=(12, 48),
        )
        sheet_minus = Surface(
            lambda r, t: np.array([
                r * np.cos(t),
                r * np.sin(t),
                -0.62 * np.sqrt(r) * np.cos(t / 2),
            ]),
            u_range=[0.03, rmax],
            v_range=[0, TAU],
            resolution=(12, 48),
        )
        for sheet in (sheet_plus, sheet_minus):
            sheet.set_fill(self.BLUE, opacity=0.16)
            sheet.set_stroke(self.BLUE, width=0.35, opacity=0.32)

        base = ParametricFunction(
            lambda t: np.array([1.55 * np.cos(t), 1.55 * np.sin(t), -1.05]),
            t_range=[0, TAU],
            color=self.CORAL,
            stroke_width=4,
        )
        zero = Dot3D(point=np.array([0, 0, -1.05]), radius=0.06, color=self.CORAL)
        lifted = ParametricFunction(
            lambda t: np.array([
                1.55 * np.cos(t),
                1.55 * np.sin(t),
                0.62 * np.sqrt(1.55) * np.cos(t / 2),
            ]),
            t_range=[0, TAU],
            color=self.BLUE,
            stroke_width=7,
        )
        lifted_dot = Dot3D(point=lifted.point_from_proportion(0), radius=0.075, color=self.BLUE)
        arrow = CurvedArrow(
            start_point=RIGHT * 0.95 + DOWN * 0.2 + OUT * -1.02,
            end_point=LEFT * 0.95 + UP * 0.18 + OUT * -1.02,
            angle=TAU * 0.65,
            color=self.GOLD,
            stroke_width=4,
        )
        guides = VGroup()
        for alpha in [0, 0.25, 0.5, 0.75, 1.0]:
            p = base.point_from_proportion(alpha)
            q = lifted.point_from_proportion(alpha)
            guides.add(Line(p, q, color=self.GRAY, stroke_width=1, stroke_opacity=0.22))
        return VGroup(sheet_plus, sheet_minus, base, zero, arrow, guides, lifted, lifted_dot), lifted, lifted_dot
