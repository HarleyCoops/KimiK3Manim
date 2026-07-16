"""Typed artifacts exchanged between K3 pipeline agents.

Each model doubles as the strict json_schema for kimi-k3 structured output
(via .k3_response_format()) and as the validator the supervisor runs on
every artifact before handing it to the next agent.
"""

from .artifacts import (
    KnowledgeGraph,
    KnowledgeNode,
    MathEnrichment,
    NodeMath,
    NodeVisual,
    VisualSpec,
    Narrative,
    SceneBundle,
    SceneFile,
    CritiqueReport,
    k3_response_format,
)

__all__ = [
    "KnowledgeGraph",
    "KnowledgeNode",
    "MathEnrichment",
    "NodeMath",
    "NodeVisual",
    "VisualSpec",
    "Narrative",
    "SceneBundle",
    "SceneFile",
    "CritiqueReport",
    "k3_response_format",
]
