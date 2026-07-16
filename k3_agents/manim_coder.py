"""Stage 5: Manim Coder - turns the screenplay into runnable scenes.

Runs on the cheaper code-specialized model (kimi-k2.7-code by default).
The supervisor executes the emitted files and feeds tracebacks back here
for repair, so this agent also handles fix-up rounds.
"""

from __future__ import annotations

from typing import Optional

try:
    from ..config import KIMI_MODEL_CODE
    from ..schemas import Narrative, SceneBundle, VisualSpec
except ImportError:
    from config import KIMI_MODEL_CODE
    from schemas import Narrative, SceneBundle, VisualSpec

from .base import K3Agent


class ManimCoder(K3Agent):
    name = "manim-coder"
    output_model = SceneBundle

    def __init__(self, client=None, model: Optional[str] = None):
        super().__init__(client=client, model=model or KIMI_MODEL_CODE)

    def system_prompt(self) -> str:
        return (
            "Role: Manim Coder. Produce complete, runnable Manim CE (>=0.19) "
            "Python files implementing the screenplay and visual spec. Rules: "
            "import only from manim and the standard library; one Scene class "
            "per major segment or one master Scene; use .animate syntax and "
            "MathTex for equations; no external assets; every file must run "
            "under 'manim -pql <file> <SceneClass>' without edits. Fill "
            "render_command with the exact command for the final video."
        )

    def write_scenes(self, narrative: Narrative, visual: VisualSpec) -> SceneBundle:
        return self.call(
            "Screenplay:\n" + narrative.model_dump_json(indent=2)
            + "\n\nVisual spec:\n" + visual.model_dump_json(indent=2),
            max_tokens=65536,
        )

    def fix_scenes(self, bundle: SceneBundle, error_log: str) -> SceneBundle:
        return self.call(
            "Your previous scene bundle failed. Return a corrected FULL bundle "
            "(all files, complete content).\n\nPrevious bundle:\n"
            + bundle.model_dump_json(indent=2)
            + "\n\nError output:\n" + error_log[-8000:],
            max_tokens=65536,
        )
