"""Stage 2: Mathematical Enricher - whole-graph math in one context."""

from __future__ import annotations

try:
    from ..schemas import KnowledgeGraph, MathEnrichment
except ImportError:
    from schemas import KnowledgeGraph, MathEnrichment

from .base import K3Agent


class MathEnricher(K3Agent):
    name = "math-enricher"
    output_model = MathEnrichment

    def system_prompt(self) -> str:
        return (
            "Role: Mathematical Enricher. For EVERY node in the knowledge graph "
            "provide the key LaTeX equations, a symbol table, one worked example, "
            "and cross_references to other node ids whose mathematics this "
            "connects to. Because you see the whole graph at once, make the "
            "cross-references genuinely illuminating rather than incidental."
        )

    def enrich(self, graph: KnowledgeGraph) -> MathEnrichment:
        return self.call(
            "Knowledge graph to enrich:\n" + graph.model_dump_json(indent=2)
        )
