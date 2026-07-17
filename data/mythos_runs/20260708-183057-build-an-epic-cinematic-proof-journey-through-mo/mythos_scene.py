from manim import *


class MythosOfflineScene(ThreeDScene):
    """Offline rehearsal scene: proves the harness plumbing end to end."""

    def construct(self):
        self.camera.background_color = "#0c0c0b"
        self.set_camera_orientation(phi=0 * DEGREES, theta=-90 * DEGREES)
        title = Text("Mythos harness: offline rehearsal", font_size=40, color="#faf9f5")
        formula = MathTex(r"e^{i\pi} + 1 = 0", font_size=64, color="#d97757")
        self.play(FadeIn(title))
        self.wait(0.6)
        self.play(title.animate.scale(0.5).to_edge(UP), FadeIn(formula))
        self.move_camera(frame_center=formula.get_center(), zoom=2.2, run_time=1.2)
        self.wait(0.6)
        self.move_camera(frame_center=ORIGIN, zoom=1.0, run_time=1.0)
        self.play(FadeOut(formula), FadeOut(title))
