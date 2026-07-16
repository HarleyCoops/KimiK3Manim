"""Stage 4: Narrative Composer - the screenplay that binds it together."""

from __future__ import annotations

try:
    from ..schemas import KnowledgeGraph, MathEnrichment, Narrative, VisualSpec
except ImportError:
    from schemas import KnowledgeGraph, MathEnrichment, Narrative, VisualSpec

from .base import K3Agent


class NarrativeComposer(K3Agent):
    name = "narrative-composer"
    output_model = Narrative

    def system_prompt(self) -> str:
        return (
            "Role: Narrative Composer. Write a scene-by-scene screenplay for the "
            "animation: narration lines, what appears on screen and when, and the "
            "emotional arc from wonder through understanding. Every equation from "
            "the enrichment that appears on screen must be introduced by the "
            "narration before it lands. scene_order lists node ids foundations "
            "first, target concept as the finale."
        )

    def compose(
        self, graph: KnowledgeGraph, math: MathEnrichment, visual: VisualSpec
    ) -> Narrative:
        return self.call(
            "Knowledge graph:\n" + graph.model_dump_json(indent=2)
            + "\n\nMath:\n" + math.model_dump_json(indent=2)
            + "\n\nVisual spec:\n" + visual.model_dump_json(indent=2),
            max_tokens=65536,
        )
