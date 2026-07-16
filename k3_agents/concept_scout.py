"""Stage 1: Concept Scout - whole-graph prerequisite exploration.

Replaces the depth-limited recursive explorer: with K3's 1M context the
full prerequisite graph is produced in a single reasoning pass.
"""

from __future__ import annotations

try:
    from ..schemas import KnowledgeGraph
except ImportError:
    from schemas import KnowledgeGraph

from .base import K3Agent


class ConceptScout(K3Agent):
    name = "concept-scout"
    output_model = KnowledgeGraph

    def system_prompt(self) -> str:
        return (
            "Role: Concept Scout. Given a target math/physics concept, map the "
            "COMPLETE prerequisite graph a motivated viewer needs, from true "
            "foundations up to the target. Emit a graph, not a tree: shared "
            "prerequisites appear once and are referenced by id. Keep it tight - "
            "every node must earn its screen time in a video. 4 to 12 nodes. "
            "depth 0 is the target concept; higher depth is more foundational."
        )

    def explore(self, concept: str) -> KnowledgeGraph:
        return self.call(f"Target concept: {concept}")
