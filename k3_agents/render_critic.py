"""Stage 6: Render Critic - vision pass over actual rendered frames."""

from __future__ import annotations

import base64
from pathlib import Path
from typing import Any, List

try:
    from ..schemas import CritiqueReport, VisualSpec
except ImportError:
    from schemas import CritiqueReport, VisualSpec

from .base import K3Agent


class RenderCritic(K3Agent):
    name = "render-critic"
    output_model = CritiqueReport

    def system_prompt(self) -> str:
        return (
            "Role: Render Critic. You are shown frames sampled from a rendered "
            "Manim video plus the visual spec it was meant to satisfy. Judge "
            "composition, legibility of equations, color adherence, and whether "
            "the shots described actually appear. passed=true only if a viewer "
            "would call this polished. Issues must be concrete edits the coder "
            "can apply (name the scene class and the change)."
        )

    def critique(self, visual: VisualSpec, frames: List[Path]) -> CritiqueReport:
        content: List[Any] = [{
            "type": "text",
            "text": "Visual spec:\n" + visual.model_dump_json(indent=2),
        }]
        for frame in frames:
            b64 = base64.b64encode(frame.read_bytes()).decode()
            content.append({
                "type": "image_url",
                "image_url": {"url": f"data:image/png;base64,{b64}"},
            })
        return self.call(content)
