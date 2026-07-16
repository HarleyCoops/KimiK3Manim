"""Kimi K3 agent swarm for math/physics animation generation.

Six specialist agents plus a deterministic supervisor rebuild the original
4-stage K2 enrichment pipeline as whole-graph, single-context K3 sessions
with strict structured output, ending in a closed render/critique loop.

    from k3_agents import Supervisor
    result = Supervisor().run("gauge invariance in electromagnetism")
"""

from .base import K3Agent
from .concept_scout import ConceptScout
from .math_enricher import MathEnricher
from .visual_designer import VisualDesigner
from .narrative_composer import NarrativeComposer
from .manim_coder import ManimCoder
from .render_critic import RenderCritic
from .supervisor import Supervisor

__all__ = [
    "K3Agent",
    "ConceptScout",
    "MathEnricher",
    "VisualDesigner",
    "NarrativeComposer",
    "ManimCoder",
    "RenderCritic",
    "Supervisor",
]
