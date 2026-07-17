from manim import *


class EmptyStageStory(ThreeDScene):
    def construct(self):
        self.camera.background_color = "#0c0c0b"
        self.set_camera_orientation(phi=0, theta=-90 * DEGREES, zoom=1, frame_center=ORIGIN)

        headline = Text(
            "No mathematical story was supplied.",
            font_size=72,
            color="#faf9f5",
        ).move_to(ORIGIN)

        empty_stage_world = VGroup()

        caption = Text(
            "The stage is ready; no math was supplied.",
            font_size=30,
            color="#b0aea5",
            slant=ITALIC,
        ).move_to(DOWN * 3.2)

        self.add_fixed_in_frame_mobjects(headline)
        self.play(FadeIn(headline), run_time=1.0)
        self.wait(0.8)

        self.play(FadeOut(headline), run_time=0.5)
        self.remove(headline)
        self.add(empty_stage_world)
        self.wait(0.5)

        self.add_fixed_in_frame_mobjects(caption)
        self.play(FadeIn(caption), run_time=0.5)
        self.wait(1.2)
