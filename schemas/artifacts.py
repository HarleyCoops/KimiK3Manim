"""Pydantic models for every artifact in the K3 agent pipeline.

The pipeline is a chain of typed hand-offs:

    ConceptScout        -> KnowledgeGraph
    MathEnricher        -> MathEnrichment
    VisualDesigner      -> VisualSpec
    NarrativeComposer   -> Narrative
    ManimCoder          -> SceneBundle
    RenderCritic        -> CritiqueReport

kimi-k3 supports strict json_schema structured output, so each agent is
forced to emit exactly one of these shapes - no text-parsing fallbacks.
"""

from __future__ import annotations

from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field


def k3_response_format(model: type[BaseModel]) -> Dict[str, Any]:
    """Build a kimi-k3 response_format dict from a Pydantic model."""
    schema = model.model_json_schema()
    return {
        "type": "json_schema",
        "json_schema": {
            "name": model.__name__,
            "schema": schema,
            "strict": True,
        },
    }


# --------------------------------------------------------------------------
# Stage 1: Concept Scout
# --------------------------------------------------------------------------

class KnowledgeNode(BaseModel):
    """One concept in the prerequisite graph."""

    id: str = Field(description="Stable slug, e.g. 'pythagorean-theorem'")
    concept: str = Field(description="Human-readable concept name")
    depth: int = Field(description="0 = target concept, increasing toward foundations")
    summary: str = Field(description="One-paragraph orientation for this concept")
    prerequisite_ids: List[str] = Field(
        default_factory=list,
        description="ids of concepts that must be understood first",
    )


class KnowledgeGraph(BaseModel):
    """Full prerequisite graph for a target concept (whole-graph, not a tree:
    shared prerequisites appear once and are referenced by id)."""

    target_id: str
    nodes: List[KnowledgeNode]

    def node(self, node_id: str) -> KnowledgeNode:
        for n in self.nodes:
            if n.id == node_id:
                return n
        raise KeyError(node_id)

    def topological_order(self) -> List[KnowledgeNode]:
        """Foundations first, target last. Raises on cycles."""
        order: List[KnowledgeNode] = []
        seen: set[str] = set()
        visiting: set[str] = set()

        def visit(node_id: str) -> None:
            if node_id in seen:
                return
            if node_id in visiting:
                raise ValueError(f"Cycle in knowledge graph at {node_id}")
            visiting.add(node_id)
            for dep in self.node(node_id).prerequisite_ids:
                visit(dep)
            visiting.discard(node_id)
            seen.add(node_id)
            order.append(self.node(node_id))

        for n in self.nodes:
            visit(n.id)
        return order


# --------------------------------------------------------------------------
# Stage 2: Mathematical Enricher
# --------------------------------------------------------------------------

class NodeMath(BaseModel):
    node_id: str
    equations: List[str] = Field(description="LaTeX equations, most important first")
    definitions: Dict[str, str] = Field(
        default_factory=dict, description="symbol -> meaning"
    )
    worked_example: str = Field(description="One concrete worked example")
    cross_references: List[str] = Field(
        default_factory=list,
        description="ids of other nodes whose math this connects to",
    )


class MathEnrichment(BaseModel):
    target_id: str
    nodes: List[NodeMath]


# --------------------------------------------------------------------------
# Stage 3: Visual Designer
# --------------------------------------------------------------------------

class NodeVisual(BaseModel):
    node_id: str
    color_scheme: str = Field(description="Manim color constants, e.g. 'BLUE, GOLD'")
    animation_description: str = Field(
        description="Shot-by-shot description of the animation for this concept"
    )
    camera_notes: str = Field(default="", description="Camera movement/frame notes")
    duration_seconds: int = Field(description="Target duration for this segment")
    style_continuity: str = Field(
        default="",
        description="How this segment visually echoes earlier segments",
    )


class VisualSpec(BaseModel):
    target_id: str
    global_style: str = Field(description="Palette, typography, motion language")
    nodes: List[NodeVisual]


# --------------------------------------------------------------------------
# Stage 4: Narrative Composer
# --------------------------------------------------------------------------

class Narrative(BaseModel):
    target_id: str
    title: str
    logline: str = Field(description="One-sentence promise of the video")
    screenplay: str = Field(
        description="Scene-by-scene screenplay integrating math, visuals, narration"
    )
    scene_order: List[str] = Field(description="node ids in presentation order")


# --------------------------------------------------------------------------
# Stage 5: Manim Coder
# --------------------------------------------------------------------------

class SceneFile(BaseModel):
    path: str = Field(description="Relative path of the generated .py file")
    scene_class: str = Field(description="Manim Scene class name to render")
    covers_node_ids: List[str]
    content: str = Field(description="Complete Python source of the scene file")


class SceneBundle(BaseModel):
    target_id: str
    files: List[SceneFile]
    render_command: str = Field(
        description="Exact manim command that renders the full video"
    )
    notes: str = Field(default="", description="Coder notes: risks, todos")


# --------------------------------------------------------------------------
# Stage 6: Render Critic
# --------------------------------------------------------------------------

class CritiqueReport(BaseModel):
    target_id: str
    passed: bool = Field(description="True if the render meets the visual spec")
    score: int = Field(description="0-100 against the visual spec")
    issues: List[str] = Field(
        default_factory=list,
        description="Specific, actionable fixes for the Manim Coder",
    )
