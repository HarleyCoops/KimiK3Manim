"""Stage 3: Visual Designer - plans the look of every segment.

K3 is natively multimodal: when still frames from a previous render are
supplied, they are attached as base64 image content for style continuity.
"""

from __future__ import annotations

import base64
from pathlib import Path
from typing import Any, List, Optional

try:
    from ..schemas import KnowledgeGraph, MathEnrichment, VisualSpec
except ImportError:
    from schemas import KnowledgeGraph, MathEnrichment, VisualSpec

from .base import K3Agent


class VisualDesigner(K3Agent):
    name = "visual-designer"
    output_model = VisualSpec

    def system_prompt(self) -> str:
        return (
            "Role: Visual Designer for Manim CE animations. Design a coherent "
            "global_style (palette from Manim color constants, typography, motion "
            "language) and a per-node shot plan: what draws, transforms, and "
            "morphs on screen, camera movement, and duration. Favor continuous "
            "visual metaphors that evolve across segments over disconnected "
            "illustrations. If reference frames are attached, match their style."
        )

    def design(
        self,
        graph: KnowledgeGraph,
        math: MathEnrichment,
        reference_frames: Optional[List[Path]] = None,
    ) -> VisualSpec:
        text = (
            "Knowledge graph:\n" + graph.model_dump_json(indent=2)
            + "\n\nMathematical enrichment:\n" + math.model_dump_json(indent=2)
        )
        if not reference_frames:
            return self.call(text)

        content: List[Any] = [{"type": "text", "text": text}]
        for frame in reference_frames:
            b64 = base64.b64encode(frame.read_bytes()).decode()
            content.append({
                "type": "image_url",
                "image_url": {"url": f"data:image/png;base64,{b64}"},
            })
        return self.call(content)
