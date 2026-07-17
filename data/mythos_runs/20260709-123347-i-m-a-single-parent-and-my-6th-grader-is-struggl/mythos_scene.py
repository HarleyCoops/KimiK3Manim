from manim import *

BG = "#0c0c0b"
TEXT_COLOR = "#faf9f5"
CORAL = "#d97757"
BLUE = "#6a9bcc"
OLIVE = "#788c5d"
GOLD = "#d4a27f"
GRAY = "#b0aea5"


class StructureFirstJourney(ThreeDScene):
    def construct(self):
        self.camera.background_color = BG
        self.caption = None
        self.set_camera_orientation(phi=0 * DEGREES, theta=-90 * DEGREES, zoom=1)

        self.headline("Multiplication builds equal groups\nyou can see.")
        visual = self.four_trays_two_each().move_to(UP * 1.0)
        self.play(LaggedStart(*[FadeIn(m) for m in visual], lag_ratio=0.06), run_time=1.3)
        self.wait(0.7)

        f = self.formula(["4", "\\times", "2", "=", "8"], 64, {0: OLIVE, 1: OLIVE, 2: CORAL, 3: GRAY, 4: GOLD}, DOWN * 1.55)
        self.show_formula(f, "Four groups of two counters make eight.")
        self.term_tour(f, [(0, "4 counts equal groups.", OLIVE), (2, "2 fills each group.", CORAL), (4, "8 is the total built.", GOLD)], zoom=2.2)
        self.pull_back()
        visual2 = self.grouped_counters(3, 4).move_to(UP * 1.0)
        self.play(FadeOut(f), ReplacementTransform(visual, visual2), run_time=1.2)
        visual = visual2
        self.wait(0.7)

        f = self.formula(["3", "\\times", "4", "=", "12"], 64, {0: OLIVE, 1: OLIVE, 2: CORAL, 3: GRAY, 4: GOLD}, DOWN * 1.55)
        self.show_formula(f, "Three groups of four counters make twelve.")
        self.term_tour(f, [(0, "3 names the groups.", OLIVE), (2, "4 fills each group.", CORAL), (4, "12 is the whole amount.", GOLD)], zoom=2.15)
        self.pull_back()
        visual2 = self.grouped_counters(2, 6).move_to(UP * 1.0)
        self.play(FadeOut(f), ReplacementTransform(visual, visual2), run_time=1.2)
        visual = visual2
        self.wait(0.7)

        f = self.formula(["2", "\\times", "6", "=", "12"], 64, {0: OLIVE, 1: OLIVE, 2: CORAL, 3: GRAY, 4: GOLD}, DOWN * 1.55)
        self.show_formula(f, "A different grouping can make the same twelve.")
        self.term_tour(f, [(0, "2 makes two equal groups.", OLIVE), (2, "6 counts each group.", CORAL), (4, "12 stays the same total.", GOLD)], zoom=2.1)
        self.pull_back()
        self.wait(0.9)

        self.headline("A number can open\nwithout changing.")
        block12 = self.number_block("12", OLIVE).move_to(UP * 0.6)
        self.play(FadeIn(block12, scale=0.92), run_time=0.9)
        self.wait(0.7)

        f12open = self.formula(["12", "=", "3", "\\times", "4"], 64, {0: OLIVE, 1: GRAY, 2: CORAL, 3: GOLD, 4: CORAL}, ORIGIN)
        split_lines = VGroup(
            Line(block12.get_center() + DOWN * 0.35, f12open[2].get_center() + UP * 0.35, color=GOLD, stroke_width=3),
            Line(block12.get_center() + DOWN * 0.35, f12open[4].get_center() + UP * 0.35, color=GOLD, stroke_width=3),
        )
        self.play(FadeOut(block12), Create(split_lines), Write(f12open), run_time=1.1)
        self.set_caption("The pieces still rebuild the same twelve.")
        self.wait(0.7)
        self.term_tour(f12open, [(0, "12 is the whole before opening.", OLIVE), (2, "3 is one piece.", CORAL), (4, "4 is the other piece.", CORAL)], zoom=2.25)
        self.pull_back()

        block18 = self.door_block("18").move_to(RIGHT * 3.1 + UP * 0.55)
        self.play(f12open.animate.scale(0.78).move_to(LEFT * 3.0 + UP * 0.4).set_opacity(0.42), FadeOut(split_lines), FadeIn(block18), run_time=0.9)
        f18hint = self.formula(["18", "=", "2", "\\times", "9"], 62, {0: OLIVE, 1: GRAY, 2: CORAL, 3: GOLD, 4: OLIVE}, RIGHT * 2.9 + DOWN * 0.75)
        self.show_formula(f18hint, "This is one honest opening of eighteen.")
        self.term_tour(f18hint, [(0, "18 is another whole.", OLIVE), (2, "2 is one piece.", CORAL), (4, "9 is still openable.", OLIVE)], zoom=2.15)
        self.pull_back()

        self.headline("A factor tree opens one honest\nbranch at a time.", font_size=66)
        tree12 = self.tree_12(first_only=True)
        f12a = self.formula(["12", "=", "2", "\\times", "6"], 58, {0: OLIVE, 1: GRAY, 2: BLUE, 3: GOLD, 4: OLIVE}, LEFT * 3.0 + DOWN * 2.05)
        self.play(Create(tree12), Write(f12a), run_time=0.9)
        self.set_caption("The first split only has to be honest.")
        self.wait(0.7)
        self.term_tour(f12a, [(0, "12 is the tree trunk.", OLIVE), (2, "2 is one factor leaf.", BLUE), (4, "6 is still openable.", OLIVE)], zoom=2.2)
        self.pull_back(LEFT * 2.2)

        tree12_full = self.tree_12(first_only=False)
        f12b = self.formula(["6", "=", "2", "\\times", "3"], 58, {0: OLIVE, 1: GRAY, 2: BLUE, 3: GOLD, 4: GOLD}, LEFT * 2.25 + DOWN * 2.15)
        self.play(ReplacementTransform(tree12, tree12_full), FadeOut(f12a), Write(f12b), run_time=1.0)
        self.set_caption("The six branch opens into two leaves.")
        self.wait(0.7)
        self.term_tour(f12b, [(0, "6 can open.", OLIVE), (2, "2 is one new leaf.", BLUE), (4, "3 is the final leaf.", GOLD)], zoom=2.2)
        self.pull_back(LEFT * 2.4)

        f12leaf = self.formula(["12", "=", "2", "\\times", "2", "\\times", "3"], 58, {0: OLIVE, 1: GRAY, 2: BLUE, 3: GOLD, 4: GRAY, 5: GOLD, 6: GOLD}, LEFT * 3.0 + UP * 0.1)
        self.play(FadeOut(tree12_full), FadeOut(f12b), Write(f12leaf), run_time=1.0)
        self.set_caption("Twelve is rebuilt by leaves 2, 2, and 3.")
        self.wait(0.7)
        self.term_tour(f12leaf, [(0, "12 is the original whole.", OLIVE), (2, "First 2 is one leaf.", BLUE), (4, "Second 2 is another copy.", GRAY), (6, "3 is the final leaf.", GOLD)], zoom=2.1)
        self.pull_back(LEFT * 3.0)

        self.headline("Open eighteen the same\npatient way.")
        f12leaf.scale(0.82).move_to(LEFT * 3.25 + UP * 1.65).set_opacity(0.38)
        self.add(f12leaf)
        tree18 = self.tree_18(first_only=True)
        f18a = self.formula(["18", "=", "2", "\\times", "9"], 58, {0: OLIVE, 1: GRAY, 2: BLUE, 3: GOLD, 4: OLIVE}, RIGHT * 3.0 + DOWN * 2.05)
        self.play(Create(tree18), Write(f18a), run_time=0.9)
        self.set_caption("Eighteen starts with a matching 2 and openable 9.")
        self.wait(0.7)
        self.term_tour(f18a, [(0, "18 is the second trunk.", OLIVE), (2, "2 might match.", BLUE), (4, "9 must keep opening.", OLIVE)], zoom=2.15)
        self.pull_back(RIGHT * 2.4)

        tree18_full = self.tree_18(first_only=False)
        f18b = self.formula(["9", "=", "3", "\\times", "3"], 58, {0: OLIVE, 1: GRAY, 2: GOLD, 3: GOLD, 4: GRAY}, RIGHT * 2.45 + DOWN * 2.15)
        self.play(ReplacementTransform(tree18, tree18_full), FadeOut(f18a), Write(f18b), run_time=1.0)
        self.set_caption("The nine branch opens into two separate threes.")
        self.wait(0.7)
        self.term_tour(f18b, [(0, "9 is a branch inside 18.", OLIVE), (2, "First 3 is one leaf.", GOLD), (4, "Second 3 is another leaf.", GRAY)], zoom=2.2)
        self.pull_back(RIGHT * 2.7)

        f18leaf = self.formula(["18", "=", "2", "\\times", "3", "\\times", "3"], 58, {0: OLIVE, 1: GRAY, 2: BLUE, 3: GOLD, 4: GOLD, 5: GOLD, 6: GRAY}, RIGHT * 3.0 + UP * 0.1)
        self.play(FadeOut(tree18_full), FadeOut(f18b), Write(f18leaf), run_time=1.0)
        self.set_caption("Eighteen is rebuilt by leaves 2, 3, and 3.")
        self.wait(0.7)
        self.term_tour(f18leaf, [(0, "18 is the original whole.", OLIVE), (2, "2 is one leaf.", BLUE), (4, "First 3 is one candidate.", GOLD), (6, "Second 3 is the extra copy.", GRAY)], zoom=2.1)
        self.pull_back()

        self.headline("A shared piece needs one copy\non each side.", font_size=66)
        fmatch2 = self.formula(
            ["12", "=", "2", "\\times", "2", "\\times", "3", "\\quad", "18", "=", "2", "\\times", "3", "\\times", "3"],
            48,
            {0: OLIVE, 1: GRAY, 2: BLUE, 3: GOLD, 4: GRAY, 5: GOLD, 6: GRAY, 8: OLIVE, 9: GRAY, 10: BLUE, 11: GOLD, 12: GRAY, 13: GOLD, 14: GRAY},
            UP * 0.45,
        )
        self.show_formula(fmatch2, "One visible 2 can only be used once.")
        self.term_tour(fmatch2, [(2, "The 2 in 12 matches once.", BLUE), (10, "The 2 in 18 matches it.", BLUE), (4, "The extra 2 stays quiet.", GRAY)], zoom=2.35)
        self.pull_back()
        blue_thread = ArcBetweenPoints(fmatch2[2].get_center() + UP * 0.2, fmatch2[10].get_center() + UP * 0.2, angle=-TAU / 5, color=BLUE, stroke_width=6)
        self.play(Create(blue_thread), run_time=0.6)
        self.wait(0.6)

        fmatch3 = self.formula(
            ["12", "=", "2", "\\times", "2", "\\times", "3", "\\quad", "18", "=", "2", "\\times", "3", "\\times", "3"],
            48,
            {0: OLIVE, 1: GRAY, 2: BLUE, 3: GOLD, 4: GRAY, 5: GOLD, 6: GOLD, 8: OLIVE, 9: GRAY, 10: BLUE, 11: GOLD, 12: GOLD, 13: GOLD, 14: GRAY},
            UP * 0.45,
        )
        self.play(ReplacementTransform(fmatch2, fmatch3), blue_thread.animate.set_opacity(0.35), run_time=0.9)
        self.set_caption("Sharing needs a matching copy on both sides.")
        self.wait(0.7)
        self.term_tour(fmatch3, [(6, "The 3 in 12 can match.", GOLD), (12, "The 3 in 18 matches it.", GOLD), (14, "The extra 3 is not shared.", GRAY)], zoom=2.35)
        self.pull_back()
        gold_thread = ArcBetweenPoints(fmatch3[6].get_center() + DOWN * 0.22, fmatch3[12].get_center() + DOWN * 0.22, angle=TAU / 5, color=GOLD, stroke_width=6)
        self.play(Create(gold_thread), run_time=0.6)
        self.wait(0.7)

        self.headline("Common means found in both\nopened numbers.", font_size=66)
        ghosts = self.match_ghosts()
        fcommon = self.formula(["\\text{common pieces}", "=", "2", "\\text{ and }", "3"], 58, {0: OLIVE, 1: GRAY, 2: BLUE, 3: TEXT_COLOR, 4: GOLD}, ORIGIN)
        self.play(FadeIn(ghosts), Write(fcommon), run_time=0.9)
        self.set_caption("Common pieces are leaves found in both numbers.")
        self.wait(0.7)
        self.term_tour(fcommon, [(0, "Common pieces are found in both.", OLIVE), (2, "2 is a shared copy.", BLUE), (4, "3 is a shared copy.", GOLD)], zoom=2.25)
        self.pull_back()

        self.headline("Now the picture gets\nits math name.")
        fdef = self.formula(["\\text{common factor}", "=", "\\text{a factor found in both numbers}"], 50, {0: OLIVE, 1: GRAY, 2: GOLD}, ORIGIN)
        self.show_formula(fdef, "A common factor has copies in both numbers.")
        self.term_tour(fdef, [(0, "Common factor is the math name.", OLIVE), (2, "Found in both means matching copies.", GOLD)], zoom=2.2)
        self.pull_back()

        self.headline("Shared leaves multiply into\none bundle.")
        leaves = VGroup(self.tile("2", BLUE), self.tile("3", GOLD)).arrange(RIGHT, buff=3.1).move_to(UP * 1.1)
        f236 = self.formula(["2", "\\times", "3", "=", "6"], 72, {0: BLUE, 1: GOLD, 2: GOLD, 3: GRAY, 4: OLIVE}, ORIGIN)
        self.play(LaggedStart(FadeIn(leaves[0]), FadeIn(leaves[1]), lag_ratio=0.25), run_time=0.8)
        self.play(leaves.animate.arrange(RIGHT, buff=0.35).move_to(UP * 1.15), Write(f236), run_time=1.0)
        self.set_caption("Factor leaves multiply; two and three make six.")
        self.wait(0.7)
        self.term_tour(f236, [(0, "2 is shared by both.", BLUE), (2, "3 is shared by both.", GOLD)], zoom=2.35)

        self.dim_except(f236, 4)
        glow6 = self.glow(f236[4], OLIVE)
        self.add(glow6)
        self.move_camera(frame_center=f236[4].get_center(), zoom=3.0, phi=0 * DEGREES, theta=-90 * DEGREES, run_time=2.4)
        self.set_caption("Together, the shared pieces become the bundle six.", run_time=0.3)
        self.wait(1.2)
        self.play(FadeOut(glow6), run_time=0.2)
        self.restore_formula(f236)
        self.pull_back()

        bundle = Prism(dimensions=[1.35, 0.85, 0.35], fill_color=OLIVE, fill_opacity=0.72, stroke_color=TEXT_COLOR, stroke_width=1.5)
        bundle.move_to(f236[4].get_center() + OUT * 0.18)
        bundle_label = MathTex("6", color=TEXT_COLOR, font_size=44).move_to(bundle.get_center() + OUT * 0.22)
        glints = VGroup(
            Line(bundle.get_center() + LEFT * 0.5 + OUT * 0.42, bundle.get_center() + LEFT * 0.05 + OUT * 0.42, color=BLUE, stroke_width=5),
            Line(bundle.get_center() + RIGHT * 0.05 + OUT * 0.42, bundle.get_center() + RIGHT * 0.5 + OUT * 0.42, color=GOLD, stroke_width=5),
        )
        self.play(FadeIn(bundle), FadeIn(bundle_label), FadeIn(glints), f236[4].animate.set_opacity(0.25), run_time=0.8)
        self.move_camera(frame_center=ORIGIN, zoom=1, phi=60 * DEGREES, theta=-45 * DEGREES, run_time=1.4)
        self.begin_ambient_camera_rotation(rate=0.06)
        self.wait(1.6)
        self.stop_ambient_camera_rotation()
        self.move_camera(frame_center=ORIGIN, zoom=1, phi=0 * DEGREES, theta=-90 * DEGREES, run_time=1.1)

        fplain = self.formula(
            ["\\text{biggest shared bundle of }", "12", "\\text{ and }", "18", "\\text{ is }", "6"],
            48,
            {0: OLIVE, 1: OLIVE, 2: TEXT_COLOR, 3: OLIVE, 4: TEXT_COLOR, 5: OLIVE},
            ORIGIN,
        )
        self.play(FadeOut(leaves), FadeOut(f236), FadeOut(bundle), FadeOut(bundle_label), FadeOut(glints), Write(fplain), run_time=1.0)
        self.set_caption("The biggest shared bundle of 12 and 18 is six.")
        self.wait(0.7)
        self.term_tour(fplain, [(1, "12 gives shared leaves.", OLIVE), (3, "18 gives matching leaves.", OLIVE), (5, "6 is the largest shared bundle.", OLIVE)], zoom=2.15)
        self.pull_back()

        self.headline("GCF is only the name\nfor that bundle.")
        fgcf = self.formula(["\\mathrm{GCF}", "(", "12", ",", "18", ")", "=", "6"], 72, {0: OLIVE, 2: OLIVE, 4: OLIVE, 7: OLIVE}, ORIGIN)
        self.show_formula(fgcf, "GCF names the biggest shared bundle already built.")
        self.term_tour(fgcf, [(0, "GCF means greatest common factor.", OLIVE), (2, "12 is the first opened number.", OLIVE), (4, "18 is the second opened number.", OLIVE), (7, "6 is the biggest shared factor.", OLIVE)], zoom=2.2)
        self.pull_back()

        self.headline("Each word points back\nto the picture.")
        fwords = self.formula(["\\text{Greatest}", "\\quad", "\\text{Common}", "\\quad", "\\text{Factor}"], 64, {0: OLIVE, 2: BLUE, 4: CORAL}, ORIGIN)
        self.show_formula(fwords, "Each word names a visible part of the picture.")
        self.term_tour(fwords, [(0, "Greatest means biggest bundle.", OLIVE), (2, "Common means belongs to both.", BLUE), (4, "Factor means multiplying piece.", CORAL)], zoom=2.3)
        self.pull_back()

        self.headline("Expressions also have\nvisible structure.")
        fexpr = self.formula(["3", "+", "4", "\\times", "2"], 72, {0: CORAL, 1: GOLD, 2: OLIVE, 3: OLIVE, 4: CORAL}, ORIGIN)
        cards = self.action_cards(fexpr)
        self.play(FadeIn(cards), Write(fexpr), run_time=0.9)
        self.set_caption("Build the multiplication group before plus acts.")
        self.wait(0.7)
        self.term_tour(fexpr, [(0, "3 waits for later.", CORAL), (1, "Plus combines finished totals.", GOLD), (2, "4 starts the groups.", OLIVE), (4, "2 fills the groups.", CORAL)], zoom=2.25)
        self.pull_back()
        bracket = Brace(VGroup(fexpr[2], fexpr[3], fexpr[4]), DOWN, color=OLIVE, buff=0.15)
        self.play(Create(bracket), run_time=0.5)
        self.wait(0.7)

        self.headline("Adding first is tempting,\nbut it changes the structure.", font_size=64)
        fexpr_ghost = self.formula(["3", "+", "4", "\\times", "2"], 54, {0: CORAL, 1: GOLD, 2: OLIVE, 3: OLIVE, 4: CORAL}, LEFT * 3.1 + UP * 0.4)
        fexpr_ghost.set_opacity(0.28)
        fwrong = self.formula(["(", "3+4", ")", "\\quad", "\\text{then}", "\\times 2", "=", "14"], 54, {1: GRAY, 5: GRAY, 7: GRAY}, RIGHT * 2.35 + UP * 0.35)
        route = DashedLine(fexpr_ghost.get_right(), fwrong.get_left(), color=GRAY, stroke_width=4, dash_length=0.12).set_opacity(0.55)
        self.play(FadeIn(fexpr_ghost), Create(route), Write(fwrong), run_time=0.9)
        self.set_caption("Adding first solves a different expression.")
        self.wait(0.7)
        self.term_tour(fwrong, [(1, "3 plus 4 tempts first.", GRAY), (5, "Times 2 skips the group.", GRAY), (7, "14 has different structure.", GRAY)], zoom=2.15)
        self.pull_back()

        self.headline("First finish the group\nthat is being built.", font_size=66)
        tray_ghosts = self.four_trays_two_each().scale(0.82).move_to(UP * 1.25).set_opacity(0.25)
        f48 = self.formula(["4", "\\times", "2", "=", "8"], 72, {0: OLIVE, 1: OLIVE, 2: CORAL, 3: GRAY, 4: OLIVE}, ORIGIN)
        self.play(FadeIn(tray_ghosts), Write(f48), run_time=0.9)
        self.set_caption("The group 4 times 2 finishes before addition.")
        self.wait(0.7)
        self.term_tour(f48, [(0, "4 builds four trays.", OLIVE), (2, "2 fills each tray.", CORAL), (4, "8 is the finished group.", OLIVE)], zoom=2.35)
        self.pull_back()

        f38 = self.formula(["3", "+", "8"], 72, {0: CORAL, 1: GOLD, 2: OLIVE}, ORIGIN)
        self.play(FadeOut(tray_ghosts), ReplacementTransform(f48, f38), run_time=1.0)
        self.set_caption("The 3 waited; now plus can combine totals.")
        self.wait(0.7)
        self.term_tour(f38, [(0, "3 is still unchanged.", CORAL), (1, "Plus combines now.", GOLD), (2, "8 is the completed group.", OLIVE)], zoom=2.25)
        self.pull_back()

        self.headline("The honest path keeps\nthe written structure.", font_size=66)
        fcorrect = self.formula(["3", "+", "4", "\\times", "2", "=", "3", "+", "8", "=", "11"], 50, {0: CORAL, 1: GOLD, 2: OLIVE, 3: OLIVE, 4: CORAL, 8: OLIVE, 10: GOLD}, ORIGIN)
        self.show_formula(fcorrect, "First build 8, then add 3 to reach 11.")
        self.term_tour(fcorrect, [(2, "4 starts group action.", OLIVE), (4, "2 fills the groups.", CORAL), (8, "8 is the group finished.", OLIVE), (10, "11 is the final total.", GOLD)], zoom=2.35)
        self.pull_back()

        self.headline("Same numbers do not guarantee\nthe same structure.", font_size=64)
        fcorrect_ref = self.formula(["3", "+", "4", "\\times", "2", "=", "3", "+", "8", "=", "11"], 38, {0: CORAL, 1: GOLD, 2: OLIVE, 3: OLIVE, 4: CORAL, 8: OLIVE, 10: GOLD}, LEFT * 3.0 + UP * 0.55)
        fwrong2 = self.formula(["3+4", "\\to", "7", "\\quad", "7", "\\times", "2", "\\quad", "=", "\\quad", "14"], 48, {0: GRAY, 4: GRAY, 10: GRAY}, RIGHT * 2.25 + UP * 0.35)
        fcorrect_ref.set_opacity(0.8)
        fwrong2.set_opacity(0.62)
        self.play(Write(fcorrect_ref), Write(fwrong2), run_time=0.9)
        self.set_caption("Same numbers, different structure, different answer.")
        self.wait(0.7)
        self.term_tour(fwrong2, [(0, "3 plus 4 starts too soon.", GRAY), (4, "7 changed the structure.", GRAY), (10, "14 is the dim answer.", GRAY)], zoom=2.15)
        self.pull_back()

        self.headline("Both lessons use\nthe same habit.")
        fleft = self.formula(["2", "\\times", "3", "=", "6"], 58, {0: BLUE, 2: GOLD, 4: OLIVE}, LEFT * 3.0 + UP * 0.35)
        self.show_formula(fleft, "The GCF answer came from shared leaves multiplying.")
        self.term_tour(fleft, [(0, "2 is the shared piece.", BLUE), (2, "3 is the shared piece.", GOLD), (4, "6 is named after structure.", OLIVE)], zoom=2.15)
        self.pull_back()

        fright = self.formula(["4", "\\times", "2", "=", "8", "\\quad", "\\text{then}", "\\quad", "3", "+", "8", "=", "11"], 46, {0: OLIVE, 2: CORAL, 4: OLIVE, 8: CORAL, 10: OLIVE, 12: GOLD}, RIGHT * 2.8 + UP * 0.35)
        self.play(Write(fright), run_time=1.0)
        self.set_caption("The expression answer came from building first.")
        self.wait(0.7)
        fleft.set_opacity(0.4)
        self.term_tour(fright, [(0, "4 times 2 finishes first.", OLIVE), (4, "8 is the completed group.", OLIVE), (8, "3 waits.", CORAL), (12, "11 is the final result.", GOLD)], zoom=2.15)
        fleft.set_opacity(1)
        self.pull_back()

        self.headline("Check the habit\non both questions.")
        q1 = Text("What's the GCF of 12 and 18?", font_size=34, color=TEXT_COLOR)
        fcheck1 = self.formula(["\\mathrm{GCF}", "(", "12", ",", "18", ")", "=", "6"], 58, {0: OLIVE, 2: OLIVE, 4: OLIVE, 7: OLIVE}, UP * 1.15)
        q1.move_to(UP * 2.15)
        self.play(FadeIn(q1), Write(fcheck1), run_time=0.9)
        self.set_caption("The greatest shared bundle uses both shared pieces.")
        self.wait(0.7)
        self.term_tour(fcheck1, [(0, "GCF is the biggest shared bundle.", OLIVE), (2, "12 opens to 2, 2, 3.", OLIVE), (4, "18 opens to 2, 3, 3.", OLIVE), (7, "6 multiplies the shared leaves.", OLIVE)], zoom=2.15)
        self.pull_back()

        q2 = Text("Which do you do first in 3+4×2?", font_size=34, color=TEXT_COLOR)
        fcheck2 = self.formula(["3", "+", "4", "\\times", "2", "=", "11"], 58, {0: CORAL, 1: GOLD, 2: OLIVE, 3: OLIVE, 4: CORAL, 6: GOLD}, DOWN * 1.15)
        q2.move_to(DOWN * 0.2)
        self.play(q1.animate.set_opacity(0.38), fcheck1.animate.set_opacity(0.38), FadeIn(q2), Write(fcheck2), run_time=0.9)
        self.set_caption("The written structure gives 11, not 14.")
        self.wait(0.7)
        self.term_tour(fcheck2, [(0, "3 waits.", CORAL), (2, "4 starts the groups.", OLIVE), (4, "2 fills the groups.", CORAL), (6, "11 is the final answer.", GOLD)], zoom=2.15)
        self.pull_back()

        self.headline("Structure first makes\nthe answer feel earned.", font_size=66)
        ffinal = self.formula(["\\text{structure first}", "\\quad", "\\Longrightarrow", "\\quad", "\\text{calmer math}"], 60, {0: OLIVE, 2: GOLD, 4: BLUE}, ORIGIN)
        self.show_formula(ffinal, "GCF used shared pieces; expressions used action order.")
        self.term_tour(ffinal, [(0, "Structure first sees what is built.", OLIVE), (2, "The arrow means less guessing.", GOLD), (4, "Calmer math follows the answer.", BLUE)], zoom=2.2)
        self.clear_caption()
        self.pull_back()
        self.wait(1.2)
        self.fade_all(run_time=1.2)

    def headline(self, text, font_size=68):
        self.fade_all(run_time=0.45)
        self.move_camera(frame_center=ORIGIN, zoom=1, phi=0 * DEGREES, theta=-90 * DEGREES, run_time=0.6)
        h = Text(text, font_size=font_size, color=TEXT_COLOR, line_spacing=0.85)
        if h.width > config.frame_width - 1.0:
            h.scale_to_fit_width(config.frame_width - 1.0)
        h.set_opacity(0)
        self.add_fixed_in_frame_mobjects(h)
        self.play(h.animate.set_opacity(1), run_time=0.8)
        self.wait(0.85)
        self.play(FadeOut(h), run_time=0.45)
        self.remove(h)

    def fade_all(self, run_time=0.5):
        mobs = list(self.mobjects)
        if mobs:
            self.play(*[FadeOut(m) for m in mobs], run_time=run_time)
        self.caption = None

    def clear_caption(self):
        if self.caption is not None:
            old = self.caption
            self.play(FadeOut(old), run_time=0.25)
            self.remove(old)
            self.caption = None

    def set_caption(self, text, run_time=0.35):
        new_caption = Text(text, font_size=30, color=TEXT_COLOR, slant=ITALIC)
        if new_caption.width > config.frame_width - 0.9:
            new_caption.scale_to_fit_width(config.frame_width - 0.9)
        new_caption.to_edge(DOWN, buff=0.42)
        new_caption.set_opacity(0)
        self.add_fixed_in_frame_mobjects(new_caption)
        if self.caption is not None:
            old = self.caption
            self.play(old.animate.set_opacity(0), new_caption.animate.set_opacity(1), run_time=run_time)
            self.remove(old)
        else:
            self.play(new_caption.animate.set_opacity(1), run_time=run_time)
        self.caption = new_caption

    def formula(self, parts, font_size, colors, position):
        m = MathTex(*parts, font_size=font_size, color=TEXT_COLOR)
        for index, color in colors.items():
            if 0 <= index < len(m):
                m[index].set_color(color)
        m.move_to(position)
        return m

    def show_formula(self, formula, caption):
        self.play(Write(formula), run_time=0.9)
        self.set_caption(caption)
        self.wait(0.7)

    def dim_except(self, formula, index):
        self.play(*[part.animate.set_opacity(1 if i == index else 0.22) for i, part in enumerate(formula)], run_time=0.25)

    def restore_formula(self, formula):
        self.play(*[part.animate.set_opacity(1) for part in formula], run_time=0.25)

    def glow(self, part, color):
        g = part.copy()
        g.set_fill(opacity=0)
        g.set_stroke(color=color, width=10, opacity=0.45)
        g.scale(1.04)
        return g

    def term_tour(self, formula, stops, zoom=2.2):
        for index, caption, color in stops:
            self.dim_except(formula, index)
            glow = self.glow(formula[index], color)
            self.add(glow)
            self.move_camera(frame_center=formula[index].get_center(), zoom=zoom, phi=0 * DEGREES, theta=-90 * DEGREES, run_time=0.8)
            self.set_caption(caption, run_time=0.25)
            self.wait(0.75)
            self.play(FadeOut(glow), run_time=0.2)
        self.restore_formula(formula)

    def pull_back(self, center=ORIGIN, run_time=0.85):
        self.move_camera(frame_center=center, zoom=1, phi=0 * DEGREES, theta=-90 * DEGREES, run_time=run_time)
        self.wait(0.65)

    def tile(self, label, color):
        box = RoundedRectangle(width=0.78, height=0.56, corner_radius=0.08, stroke_color=color, stroke_width=3, fill_color=color, fill_opacity=0.24)
        txt = MathTex(label, font_size=34, color=TEXT_COLOR).move_to(box.get_center())
        return VGroup(box, txt)

    def number_block(self, label, color):
        box = RoundedRectangle(width=1.55, height=1.05, corner_radius=0.08, stroke_color=color, stroke_width=3, fill_color=color, fill_opacity=0.45)
        txt = MathTex(label, font_size=52, color=TEXT_COLOR).move_to(box.get_center())
        return VGroup(box, txt)

    def door_block(self, label):
        body = self.number_block(label, OLIVE)
        hinge = Line(LEFT * 0.58 + DOWN * 0.46, LEFT * 0.58 + UP * 0.46, color=GOLD, stroke_width=4)
        door = Polygon(LEFT * 0.58 + DOWN * 0.46, RIGHT * 0.6 + DOWN * 0.3, RIGHT * 0.6 + UP * 0.3, LEFT * 0.58 + UP * 0.46, color=OLIVE, fill_color=OLIVE, fill_opacity=0.18, stroke_width=2)
        return VGroup(body, hinge, door)

    def four_trays_two_each(self):
        g = VGroup()
        centers = [LEFT * 0.9 + UP * 0.45, RIGHT * 0.9 + UP * 0.45, LEFT * 0.9 + DOWN * 0.55, RIGHT * 0.9 + DOWN * 0.55]
        for c in centers:
            tray = RoundedRectangle(width=1.25, height=0.74, corner_radius=0.08, stroke_color=GRAY, stroke_width=2.5)
            tray.move_to(c)
            dots = VGroup(Dot(c + LEFT * 0.23, radius=0.075, color=CORAL), Dot(c + RIGHT * 0.23, radius=0.075, color=CORAL))
            g.add(tray, dots)
        return g

    def grouped_counters(self, groups, per_group):
        g = VGroup()
        x_positions = [-2, 0, 2] if groups == 3 else [-1.45, 1.45]
        for x in x_positions:
            width = 1.35 if per_group == 4 else 2.25
            height = 1.05
            rect = RoundedRectangle(width=width, height=height, corner_radius=0.08, stroke_color=OLIVE, stroke_width=2.5)
            rect.move_to(RIGHT * x)
            dots = VGroup()
            cols = 2 if per_group == 4 else 3
            rows = 2
            for r in range(rows):
                for c in range(cols):
                    dx = (c - (cols - 1) / 2) * 0.38
                    dy = (r - 0.5) * 0.34
                    dots.add(Dot(rect.get_center() + RIGHT * dx + UP * dy, radius=0.07, color=CORAL))
            g.add(rect, dots)
        return g

    def tree_12(self, first_only=False):
        top = self.tile("12", OLIVE).move_to(LEFT * 3.0 + UP * 1.45)
        left = self.tile("2", BLUE).move_to(LEFT * 3.75 + UP * 0.35)
        right = self.tile("6", OLIVE).move_to(LEFT * 2.25 + UP * 0.35)
        lines = VGroup(Line(top.get_center(), left.get_center(), color=OLIVE, stroke_width=3), Line(top.get_center(), right.get_center(), color=OLIVE, stroke_width=3))
        if first_only:
            return VGroup(lines, top, left, right)
        low_left = self.tile("2", BLUE).move_to(LEFT * 2.75 + DOWN * 0.78)
        low_right = self.tile("3", GOLD).move_to(LEFT * 1.75 + DOWN * 0.78)
        low_lines = VGroup(Line(right.get_center(), low_left.get_center(), color=OLIVE, stroke_width=3), Line(right.get_center(), low_right.get_center(), color=OLIVE, stroke_width=3))
        return VGroup(lines, low_lines, top, left, right, low_left, low_right)

    def tree_18(self, first_only=False):
        top = self.tile("18", OLIVE).move_to(RIGHT * 3.0 + UP * 1.45)
        left = self.tile("2", BLUE).move_to(RIGHT * 2.25 + UP * 0.35)
        right = self.tile("9", OLIVE).move_to(RIGHT * 3.75 + UP * 0.35)
        lines = VGroup(Line(top.get_center(), left.get_center(), color=OLIVE, stroke_width=3), Line(top.get_center(), right.get_center(), color=OLIVE, stroke_width=3))
        if first_only:
            return VGroup(lines, top, left, right)
        low_left = self.tile("3", GOLD).move_to(RIGHT * 3.25 + DOWN * 0.78)
        low_right = self.tile("3", GRAY).move_to(RIGHT * 4.25 + DOWN * 0.78)
        low_lines = VGroup(Line(right.get_center(), low_left.get_center(), color=OLIVE, stroke_width=3), Line(right.get_center(), low_right.get_center(), color=OLIVE, stroke_width=3))
        return VGroup(lines, low_lines, top, left, right, low_left, low_right)

    def match_ghosts(self):
        blue = ArcBetweenPoints(LEFT * 2.5 + UP * 0.55, RIGHT * 2.5 + UP * 0.55, angle=-TAU / 5, color=BLUE, stroke_width=6)
        gold = ArcBetweenPoints(LEFT * 2.3 + DOWN * 0.25, RIGHT * 2.3 + DOWN * 0.25, angle=TAU / 5, color=GOLD, stroke_width=6)
        return VGroup(blue, gold).set_opacity(0.22)

    def action_cards(self, formula):
        c1 = SurroundingRectangle(formula[0], buff=0.18, color=CORAL, stroke_width=2, fill_color=CORAL, fill_opacity=0.06)
        c2 = SurroundingRectangle(formula[1], buff=0.18, color=GOLD, stroke_width=2, fill_color=GOLD, fill_opacity=0.06)
        c3 = SurroundingRectangle(VGroup(formula[2], formula[3], formula[4]), buff=0.18, color=OLIVE, stroke_width=2, fill_color=OLIVE, fill_opacity=0.08)
        return VGroup(c1, c2, c3)
