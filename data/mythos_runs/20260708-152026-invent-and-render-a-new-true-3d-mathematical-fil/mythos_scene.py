from manim import *
import numpy as np


class CausticProjectionJourney(ThreeDScene):
    BG = "#0c0c0b"
    TEXT = "#faf9f5"
    CORAL = "#d97757"
    BLUE = "#6a9bcc"
    OLIVE = "#788c5d"
    GOLD = "#d4a27f"
    GRAY = "#b0aea5"

    def construct(self):
        self.camera.background_color = self.BG
        self.set_camera_orientation(phi=0, theta=-90 * DEGREES, zoom=1)

        self.caption = None
        self.current = VGroup()
        self.stage = VGroup()

        self.act(
            "Projection sends one point to one visible mark.",
            MathTex("p", "\\mapsto", "F(p)"),
            {0: self.OLIVE, 1: self.GOLD, 2: self.BLUE},
            "A projection sends one source point to one image mark.",
            [
                (0, "The original point lives upstairs.", self.OLIVE, 2.15),
                (1, "The arrow is the sending rule.", self.GOLD, 2.35),
                (2, "The mark is that point's image.", self.BLUE, 2.2),
            ],
            diagram=self.point_to_mark_diagram(),
            after="The mark is the image of the point, not new geometry.",
        )

        self.headline("A caustic needs two stages: source sheet and receiving plane.", 70)
        sheet, plane = self.surfaces()
        self.stage = VGroup(sheet, plane)
        self.play(FadeIn(plane), FadeIn(sheet), run_time=0.8)
        self.move_camera(phi=60 * DEGREES, theta=-45 * DEGREES, zoom=1, run_time=1.4)
        self.move_camera(phi=60 * DEGREES, theta=-38.1 * DEGREES, zoom=1, run_time=2.0, rate_func=linear)
        self.move_camera(phi=0, theta=-90 * DEGREES, zoom=1, run_time=1.2)
        self.act(
            None,
            MathTex("\\Sigma", "\\subset", "\\mathbb{R}^{3}", "\\quad", "\\Pi", "\\cong", "\\mathbb{R}^{2}"),
            {0: self.OLIVE, 2: self.OLIVE, 4: self.BLUE, 6: self.BLUE},
            "Two surfaces set the stage: source above, image below.",
            [
                (0, "The source sheet holds original points.", self.OLIVE, 2.35),
                (4, "The receiving plane holds the images.", self.BLUE, 2.35),
            ],
            keep_stage=True,
            after="The sheet is placed in space; the image plane is flat.",
        )

        self.act(
            "The same event has two coordinate names.",
            MathTex("p", "=", "(u,v)", "\\in", "\\Sigma", "\\quad", "F(p)", "=", "(X,Y)", "\\in", "\\Pi"),
            {0: self.OLIVE, 2: self.OLIVE, 4: self.OLIVE, 6: self.GOLD, 8: self.BLUE, 10: self.BLUE},
            "Lowercase coordinates start upstairs; uppercase coordinates land downstairs.",
            [
                (2, "u and v name the source point.", self.OLIVE, 2.45),
                (6, "F of p is the projected point.", self.GOLD, 2.35),
                (8, "X and Y name the landing point.", self.BLUE, 2.45),
            ],
            after="These are different locations, connected by projection.",
        )

        self.act(
            "F is the rule that connects the two stages.",
            MathTex("F", ":", "\\Sigma", "\\longrightarrow", "\\Pi", "\\quad", "F(p)", "=", "(X(u,v),Y(u,v))"),
            {0: self.GOLD, 2: self.OLIVE, 3: self.GOLD, 4: self.BLUE, 6: self.GOLD, 8: self.BLUE},
            "F is the map from the sheet to the plane.",
            [
                (0, "F is the projection rule.", self.GOLD, 2.55),
                (2, "The input side is the source sheet.", self.OLIVE, 2.3),
                (4, "The output side is the receiving plane.", self.BLUE, 2.3),
                (8, "X and Y depend on u and v.", self.BLUE, 2.55),
            ],
            after="F is geometric: it is not force or brightness.",
        )

        self.headline("Near one point, projection becomes a local linear machine.", 68)
        patch = self.local_patch()
        self.stage = VGroup(sheet.copy(), plane.copy(), patch)
        self.play(FadeIn(self.stage), run_time=0.8)
        self.move_camera(phi=58 * DEGREES, theta=-45 * DEGREES, zoom=1.15, run_time=1.4)
        self.move_camera(phi=58 * DEGREES, theta=-39.8 * DEGREES, zoom=1.15, run_time=1.8, rate_func=linear)
        self.move_camera(phi=0, theta=-90 * DEGREES, zoom=1, run_time=1.1)
        self.act(
            None,
            MathTex("F(p+\\Delta p)", "\\approx", "F(p)", "+", "dF_p", "\\begin{pmatrix}\\Delta u\\\\ \\Delta v\\end{pmatrix}"),
            {0: self.OLIVE, 1: self.GRAY, 2: self.GOLD, 4: self.GOLD, 5: self.OLIVE},
            "Nearby behavior is captured by the differential dF.",
            [
                (0, "The nearby point is a tiny step away.", self.OLIVE, 2.35),
                (4, "dF sends tiny moves to tiny image moves.", self.GOLD, 2.7),
                (5, "The column is the tiny source step.", self.OLIVE, 2.35),
            ],
            keep_stage=True,
            after="The closer the patch, the better this linear picture.",
        )

        self.act(
            "Area reveals when projection is squeezing the image.",
            MathTex("dA_{\\mathrm{image}}", "=", "|J(u,v)|", "dA_{\\mathrm{source}}"),
            {0: self.BLUE, 2: self.OLIVE, 3: self.OLIVE},
            "Image area is source area times local scale.",
            [
                (0, "The image patch is the projected tiny area.", self.BLUE, 2.4),
                (2, "The absolute Jacobian is the local area multiplier.", self.OLIVE, 2.75),
                (3, "The source patch is the original tiny area.", self.OLIVE, 2.4),
            ],
            diagram=self.area_motif(),
            after="Use absolute value because visible area is never negative.",
        )

        self.headline("The Jacobian is a determinant of local coordinate change.", 68)
        jac = self.formula(
            MathTex("J", "(u,v)", "=", "\\det", "\\left(", "\\frac{\\partial(X,Y)}{\\partial(u,v)}", "\\right)"),
            {0: self.OLIVE, 1: self.OLIVE, 3: self.OLIVE, 5: self.GOLD},
        )
        self.show_formula(jac, "J records signed local area change.")
        self.term_tour(
            jac,
            [
                (0, "J is the area diagnostic.", self.OLIVE, 2.45),
                (1, "J depends on the inspected source point.", self.OLIVE, 2.35),
                (3, "The determinant turns coordinate change into area scale.", self.OLIVE, 2.55),
                (5, "This derivative compares image and source coordinates.", self.GOLD, 2.75),
            ],
        )
        self.pull_back(jac)
        self.replace_caption("The fraction is shorthand, not ordinary division.")
        expanded = self.formula(
            MathTex(
                "J(u,v)",
                "=",
                "\\det",
                "\\begin{pmatrix}\\frac{\\partial X}{\\partial u} & \\frac{\\partial X}{\\partial v}\\\\ \\frac{\\partial Y}{\\partial u} & \\frac{\\partial Y}{\\partial v}\\end{pmatrix}",
            ),
            {0: self.OLIVE, 2: self.OLIVE, 3: self.GOLD},
        )
        self.play(TransformMatchingShapes(jac, expanded), run_time=1.4)
        jac = expanded
        self.current = VGroup(jac)
        self.replace_caption("The shorthand opens into four partial rates.")
        self.term_tour(
            jac,
            [
                (0, "J is read at the same source point.", self.OLIVE, 2.25),
                (2, "The determinant measures the tiny image area.", self.OLIVE, 2.45),
                (3, "The matrix lists how X and Y respond.", self.GOLD, 2.8),
            ],
        )
        self.pull_back(jac)
        self.replace_caption("Together, the four rates describe one local map.")
        self.wait(1.0)

        self.act(
            "A caustic begins where local area collapses to zero.",
            MathTex("J(u,v)", "=", "0", "\\Longleftrightarrow", "\\operatorname{rank}", "(dF_p)", "\\,", "<2"),
            {0: self.OLIVE, 2: self.OLIVE, 4: self.OLIVE, 5: self.GOLD, 7: self.OLIVE},
            "Zero Jacobian means local two-dimensional area collapses.",
            [
                (2, "Zero marks the area collapse.", self.OLIVE, 2.8),
                (4, "Rank counts surviving independent directions.", self.OLIVE, 2.45),
                (5, "dF is the local direction-sending map.", self.GOLD, 2.55),
                (7, "Less than two means full rank is gone.", self.OLIVE, 2.8),
            ],
            after="The point remains; the local two-direction behavior fails.",
        )

        self.act(
            "At collapse, one real source direction can vanish downstairs.",
            MathTex("dF_p", "w", "=", "\\mathbf{0}", "\\quad", "w", "\\ne", "\\mathbf{0}"),
            {0: self.GOLD, 1: self.OLIVE, 3: self.BLUE, 5: self.OLIVE, 7: self.OLIVE},
            "A nonzero source direction can have zero image motion.",
            [
                (0, "dF tests one source direction.", self.GOLD, 2.45),
                (1, "w is a real source direction.", self.OLIVE, 2.45),
                (3, "The zero vector means no image motion.", self.BLUE, 2.65),
                (7, "The direction was nonzero before projection.", self.OLIVE, 2.45),
            ],
            diagram=self.lost_direction_motif(),
            after="Only one direction must be lost in the generic case.",
        )

        self.headline("The zero-J points form a hidden critical curve.", 70)
        critical_stage = VGroup(sheet.copy(), plane.copy().set_opacity(0.08), self.source_critical_curve())
        self.stage = critical_stage
        self.play(FadeIn(critical_stage), run_time=0.8)
        self.move_camera(phi=58 * DEGREES, theta=-50 * DEGREES, zoom=1.1, run_time=1.4)
        self.move_camera(phi=58 * DEGREES, theta=-44.8 * DEGREES, zoom=1.1, run_time=1.8, rate_func=linear)
        self.move_camera(phi=0, theta=-90 * DEGREES, zoom=1, run_time=1.1)
        self.act(
            None,
            MathTex("C", "=", "\\{", "(u,v)", "\\in", "\\Sigma", ":", "J(u,v)=0", "\\}"),
            {0: self.OLIVE, 3: self.OLIVE, 5: self.OLIVE, 7: self.OLIVE},
            "The critical curve lives upstairs before projection.",
            [
                (0, "C is the source-side warning curve.", self.OLIVE, 2.6),
                (3, "These source coordinates are being tested.", self.OLIVE, 2.35),
                (5, "The curve lives on the source sheet.", self.OLIVE, 2.35),
                (7, "Only zero-J source points belong.", self.OLIVE, 2.8),
            ],
            keep_stage=True,
            after="This is not the visible caustic yet.",
        )

        self.headline("The caustic is the projected critical curve.", 72)
        caustic_stage = self.caustic_projection_stage()
        self.stage = caustic_stage
        self.play(FadeIn(caustic_stage), run_time=1.0)
        self.move_camera(phi=62 * DEGREES, theta=-45 * DEGREES, zoom=1.05, run_time=1.8)
        self.move_camera(phi=62 * DEGREES, theta=-39 * DEGREES, zoom=1.08, run_time=2.6, rate_func=linear)
        self.move_camera(phi=0, theta=-90 * DEGREES, zoom=1, run_time=1.3)
        payoff = self.formula(
            MathTex(
                "K",
                "=",
                "F",
                "(",
                "C",
                ")",
                "=",
                "\\{",
                "F",
                "(",
                "(u,v)",
                ")",
                "\\mid (u,v)\\in\\Sigma",
                ",",
                "J(u,v)=0",
                "\\}",
                "\\subset \\Pi",
            ),
            {0: self.GOLD, 2: self.GOLD, 4: self.OLIVE, 8: self.GOLD, 10: self.OLIVE, 12: self.OLIVE, 14: self.OLIVE, 16: self.BLUE},
            scale=0.78,
        )
        self.show_formula(payoff, "First find the hidden curve, then project it.", keep_stage=True)
        self.term_tour(
            payoff,
            [
                (0, "K is the visible caustic curve.", self.GOLD, 3.0),
                (2, "F pushes the critical curve downstairs.", self.GOLD, 2.7),
                (4, "C is the hidden rank-drop curve.", self.OLIVE, 2.65),
                (10, "These are the tested source coordinates.", self.OLIVE, 2.55),
                (14, "J equals zero selects the curve.", self.OLIVE, 3.0),
            ],
        )
        self.pull_back(payoff, run_time=1.5)
        self.replace_caption("Only rank-dropping source points make the caustic.")
        self.wait(1.2)

        self.act(
            "Every visible caustic point remembers an upstairs point.",
            MathTex("P", "=", "F(p)", ",", "p", "\\in", "C", "\\quad\\Rightarrow\\quad", "P", "\\in", "K", "\\subset", "\\Pi"),
            {0: self.BLUE, 2: self.GOLD, 4: self.OLIVE, 6: self.OLIVE, 8: self.BLUE, 10: self.GOLD, 12: self.BLUE},
            "A caustic point is the image of a critical point.",
            [
                (0, "P is the visible footprint point.", self.BLUE, 2.45),
                (2, "F of p makes the visible point.", self.GOLD, 2.55),
                (6, "p comes from the critical curve.", self.OLIVE, 2.45),
                (10, "The landing point belongs to the caustic.", self.GOLD, 2.55),
            ],
            diagram=self.footprint_motif(),
            after="The bright trace is anchored on the receiving plane.",
        )

        self.act(
            "Brightness grows where projection crowds existing light together.",
            MathTex("I(P)", "\\propto", "\\sum_{p:\\ F(p)=P}", "\\frac{1}{|J(p)|}"),
            {0: self.BLUE, 1: self.GOLD, 2: self.OLIVE, 3: self.OLIVE},
            "Brightness rises when many source points crowd together.",
            [
                (0, "I is measured brightness on the image plane.", self.BLUE, 2.55),
                (2, "The sum counts source points landing here.", self.OLIVE, 2.8),
                (3, "Small area scale makes each contribution larger.", self.OLIVE, 2.95),
            ],
            diagram=self.crowding_motif(),
            after="No new light is created; existing light is concentrated.",
            final=True,
        )
        self.wait(1.6)

    def headline(self, text, size):
        self.clear_stage()
        self.move_camera(phi=0, theta=-90 * DEGREES, zoom=1, frame_center=ORIGIN, run_time=0.4)
        h = Text(text, font_size=size, color=self.TEXT)
        h.set_width(min(h.width, 12.6))
        self.add_fixed_in_frame_mobjects(h)
        self.play(FadeIn(h, shift=0.15 * UP), run_time=0.7)
        self.wait(1.0)
        self.play(FadeOut(h), run_time=0.7)
        self.remove(h)

    def act(self, headline_text, formula, colors, caption, stops, diagram=None, keep_stage=False, after=None, final=False):
        if headline_text:
            self.headline(headline_text, 66 if len(headline_text) > 56 else 72)
        f = self.formula(formula, colors)
        self.show_formula(f, caption, diagram=diagram, keep_stage=keep_stage)
        self.term_tour(f, stops)
        self.pull_back(f)
        if after:
            self.replace_caption(after)
            self.wait(1.0)
        if not final:
            self.wait(0.8)

    def formula(self, mob, colors, scale=1.0):
        mob.set_color(self.TEXT)
        mob.scale(scale)
        mob.move_to([0, 0.35, 0])
        for index, color in colors.items():
            if index < len(mob):
                mob[index].set_color(color)
        return mob

    def show_formula(self, formula, caption, diagram=None, keep_stage=False):
        if not keep_stage:
            self.clear_stage()
        items = VGroup()
        if keep_stage and len(self.stage) > 0:
            self.stage.set_opacity(0.22)
            items.add(self.stage)
        if diagram is not None:
            diagram.set_z_index(-2)
            items.add(diagram)
            self.play(FadeIn(diagram), run_time=0.5)
        self.play(Write(formula), run_time=1.0)
        items.add(formula)
        self.current = items
        self.replace_caption(caption)
        self.wait(0.8)

    def replace_caption(self, text):
        new_caption = Text(text, font_size=30, color=self.TEXT, slant=ITALIC)
        new_caption.set_width(min(new_caption.width, 11.4))
        new_caption.to_edge(DOWN, buff=0.35)
        self.add_fixed_in_frame_mobjects(new_caption)
        if self.caption is None:
            self.play(FadeIn(new_caption), run_time=0.35)
        else:
            self.play(ReplacementTransform(self.caption, new_caption), run_time=0.35)
            self.remove(self.caption)
        self.caption = new_caption

    def term_tour(self, formula, stops):
        for index, caption, color, zoom in stops:
            part = formula[index]
            glows = self.glow(part, color)
            animations = []
            for i, item in enumerate(formula):
                animations.append(item.animate.set_opacity(1.0 if i == index else 0.22))
            animations.append(part.animate.set_color(color))
            self.play(*animations, FadeIn(glows), run_time=0.35)
            self.replace_caption(caption)
            self.move_camera(frame_center=part.get_center(), phi=0, theta=-90 * DEGREES, zoom=zoom, run_time=1.1)
            self.wait(0.85 if zoom < 3 else 1.6)
            self.play(FadeOut(glows), run_time=0.25)

    def pull_back(self, formula, run_time=1.0):
        self.move_camera(frame_center=ORIGIN, phi=0, theta=-90 * DEGREES, zoom=1, run_time=run_time)
        self.play(*[part.animate.set_opacity(1) for part in formula], run_time=0.35)

    def glow(self, mob, color):
        g1 = mob.copy().set_color(color).set_stroke(color, width=12, opacity=0.24)
        g2 = mob.copy().set_color(color).set_stroke(color, width=5, opacity=0.34)
        return VGroup(g1, g2)

    def clear_stage(self):
        if self.current:
            self.play(FadeOut(self.current), run_time=0.45)
            self.current = VGroup()
        if self.stage:
            self.play(FadeOut(self.stage), run_time=0.35)
            self.stage = VGroup()
        if self.caption is not None:
            self.play(FadeOut(self.caption), run_time=0.25)
            self.remove(self.caption)
            self.caption = None

    def point_to_mark_diagram(self):
        source = Dot([-1.65, 1.15, 0], radius=0.07, color=self.OLIVE)
        mark = Dot([1.65, -1.0, 0], radius=0.08, color=self.BLUE)
        arrow = Arrow(source.get_center(), mark.get_center(), buff=0.16, color=self.GOLD, stroke_width=3, max_tip_length_to_length_ratio=0.08).set_opacity(0.65)
        return VGroup(source, mark, arrow)

    def surfaces(self):
        sheet = Surface(
            lambda u, v: np.array([u, v, 1.15 + 0.16 * np.sin(1.2 * u) * np.cos(1.1 * v)]),
            u_range=[-2.4, 2.4],
            v_range=[-1.45, 1.45],
            resolution=(18, 10),
            fill_color=self.OLIVE,
            fill_opacity=0.18,
            checkerboard_colors=[self.OLIVE, self.OLIVE],
            stroke_color=self.OLIVE,
            stroke_opacity=0.35,
        )
        plane = Surface(
            lambda u, v: np.array([u, v, -1.05]),
            u_range=[-2.7, 2.7],
            v_range=[-1.6, 1.6],
            resolution=(2, 2),
            fill_color=self.BLUE,
            fill_opacity=0.14,
            checkerboard_colors=[self.BLUE, self.BLUE],
            stroke_color=self.BLUE,
            stroke_opacity=0.28,
        )
        return sheet, plane

    def local_patch(self):
        s = Square(0.55, color=self.OLIVE, stroke_width=5).move_to([-0.55, 0.2, 1.22])
        p = Polygon([0.35, -0.15, -1.02], [1.0, -0.05, -1.02], [1.18, 0.35, -1.02], [0.52, 0.24, -1.02], color=self.BLUE, stroke_width=5)
        rays = VGroup(*[Line(s.get_vertices()[i], p.get_vertices()[i], color=self.GOLD, stroke_width=1.5).set_opacity(0.35) for i in range(4)])
        return VGroup(s, p, rays)

    def area_motif(self):
        source = Polygon([-2.3, -0.9, 0], [-1.55, -0.9, 0], [-1.55, -0.15, 0], [-2.3, -0.15, 0], color=self.OLIVE, fill_opacity=0.18, stroke_width=4)
        image = Polygon([1.35, -0.95, 0], [2.25, -0.78, 0], [2.05, -0.25, 0], [1.18, -0.42, 0], color=self.BLUE, fill_opacity=0.18, stroke_width=4)
        thin = Polygon([1.35, -1.35, 0], [2.25, -1.28, 0], [2.2, -1.22, 0], [1.31, -1.29, 0], color=self.CORAL, fill_opacity=0.15, stroke_width=3)
        return VGroup(source, image, thin).set_opacity(0.6)

    def lost_direction_motif(self):
        vec = Arrow([-1.35, -1.15, 0], [-0.35, -1.15, 0], buff=0, color=self.OLIVE, stroke_width=5)
        zero = Dot([0.85, -1.15, 0], radius=0.07, color=self.BLUE)
        ray = Arrow([-0.1, -1.15, 0], [0.7, -1.15, 0], buff=0.1, color=self.GOLD, stroke_width=3).set_opacity(0.55)
        return VGroup(vec, ray, zero)

    def source_critical_curve(self):
        curve = ParametricFunction(
            lambda t: np.array([1.2 * np.cos(t), 0.58 * np.sin(2 * t), 1.15 + 0.08 * np.sin(t)]),
            t_range=[0, TAU],
            color=self.OLIVE,
            stroke_width=5,
        )
        return VGroup(curve.copy().set_stroke(self.OLIVE, 12, opacity=0.24), curve)

    def projected_caustic_curve(self):
        curve = ParametricFunction(
            lambda t: np.array([1.2 * np.cos(t) + 0.38 * np.cos(2 * t), 0.46 * np.sin(2 * t), -1.04]),
            t_range=[0, TAU],
            color=self.GOLD,
            stroke_width=5,
        )
        return VGroup(curve.copy().set_stroke(self.CORAL, 15, opacity=0.28), curve)

    def caustic_projection_stage(self):
        sheet, plane = self.surfaces()
        c = self.source_critical_curve()
        k = self.projected_caustic_curve()
        rays = VGroup()
        for t in np.linspace(0, TAU, 16, endpoint=False):
            a = np.array([1.2 * np.cos(t), 0.58 * np.sin(2 * t), 1.15 + 0.08 * np.sin(t)])
            b = np.array([1.2 * np.cos(t) + 0.38 * np.cos(2 * t), 0.46 * np.sin(2 * t), -1.04])
            rays.add(Line(a, b, color=self.GOLD, stroke_width=2).set_opacity(0.35))
        return VGroup(sheet, plane, c, k, rays)

    def footprint_motif(self):
        p = Dot([-1.1, 0.95, 0], radius=0.06, color=self.OLIVE)
        P = Dot([1.15, -0.85, 0], radius=0.075, color=self.GOLD)
        glow = P.copy().set_stroke(self.CORAL, width=12, opacity=0.3)
        ray = Arrow(p.get_center(), P.get_center(), buff=0.12, color=self.GOLD, stroke_width=3).set_opacity(0.55)
        return VGroup(p, glow, P, ray)

    def crowding_motif(self):
        k = self.projected_caustic_curve().move_to([0, -1.2, 0]).scale(0.7).set_opacity(0.7)
        point = Dot([1.15, -0.85, 0], radius=0.07, color=self.BLUE)
        threads = VGroup()
        for i, y in enumerate(np.linspace(1.3, 0.1, 7)):
            start = np.array([-2.3 + 0.25 * i, y, 0])
            mid = np.array([-0.5 + 0.08 * i, -0.1 + 0.04 * i, 0])
            end = point.get_center()
            threads.add(CubicBezier(start, mid, mid + np.array([0.5, -0.25, 0]), end, color=self.OLIVE, stroke_width=2).set_opacity(0.32))
        return VGroup(k, threads, point)
