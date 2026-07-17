"""Adapt Math-To-Manim mythos run bundles into m2m2.pi_repair_task.v1 building blocks.

A mythos bundle (copied into data/mythos_runs/) contains:
    01_intent.json, 06_scene_spec.json, manifest.json, mythos_scene.py,
    render_sidecar.json ({"has_mp4": bool}), optionally prompt.txt

The adapter extracts the pieces a repair task needs: prompt, audience,
scene_name, original (gold) code, compacted scene spec, and acceptance
terms derived from the prompt plus layout idioms present in the gold code.
"""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any

MAX_AUDIENCE_CHARS = 240
MAX_PROMPT_TERMS = 8
LAYOUT_TERMS = ("scale_to_fit_width", "FadeOut")

STOP_WORDS = {
    "about", "above", "across", "after", "again", "against", "also", "animation",
    "another", "around", "before", "being", "below", "between", "build", "called",
    "cinematic", "create", "each", "epic", "every", "explain", "explaining", "film",
    "from", "have", "into", "journey", "just", "like", "make", "manim", "more",
    "most", "movie", "must", "only", "other", "over", "proof", "render", "scene",
    "should", "show", "spectacular", "start", "than", "that", "the", "their", "them",
    "then", "theorem", "there", "these", "they", "this", "through", "true", "under",
    "use", "using", "very", "video", "what", "when", "where", "which", "while",
    "will", "with", "would", "your",
}
WORD_RE = re.compile(r"[A-Za-z][A-Za-z\-]{3,}")


class BundleError(Exception):
    """Raised when a bundle lacks the artifacts needed for a repair task."""


def load_bundle(bundle_dir: str | Path) -> dict[str, Any]:
    """Load one mythos bundle into adapter-normalized pieces."""

    bundle_dir = Path(bundle_dir)
    scene_path = bundle_dir / "mythos_scene.py"
    spec_path = bundle_dir / "06_scene_spec.json"
    manifest_path = bundle_dir / "manifest.json"
    intent_path = bundle_dir / "01_intent.json"
    if not scene_path.exists():
        raise BundleError(f"{bundle_dir.name}: missing mythos_scene.py")
    if not spec_path.exists():
        raise BundleError(f"{bundle_dir.name}: missing 06_scene_spec.json")

    code = scene_path.read_text(encoding="utf-8")
    spec = _read_json(spec_path)
    manifest = _read_json(manifest_path) if manifest_path.exists() else {}
    intent = _read_json(intent_path) if intent_path.exists() else {}
    sidecar = _read_json(bundle_dir / "render_sidecar.json") if (bundle_dir / "render_sidecar.json").exists() else {}

    scene_name = (
        manifest.get("scene_name")
        or spec.get("scene_name")
        or _discover_scene_name(code)
    )
    if not scene_name:
        raise BundleError(f"{bundle_dir.name}: could not determine scene_name")

    prompt = str(manifest.get("prompt") or "").strip()
    if not prompt and (bundle_dir / "prompt.txt").exists():
        prompt = (bundle_dir / "prompt.txt").read_text(encoding="utf-8").strip()
    if not prompt:
        raise BundleError(f"{bundle_dir.name}: no prompt found")

    audience = str(intent.get("audience") or "").strip() or None
    if audience and len(audience) > MAX_AUDIENCE_CHARS:
        audience = audience[:MAX_AUDIENCE_CHARS].rstrip() + "..."

    static_check = manifest.get("static_check") if isinstance(manifest.get("static_check"), dict) else {}

    return {
        "run_id": bundle_dir.name,
        "scene_name": scene_name,
        "code": code,
        "prompt": prompt,
        "audience": audience,
        "has_mp4": bool(sidecar.get("has_mp4")),
        "static_passed": bool(static_check.get("passed", True)),
        "scene_spec": compact_spec(spec, prompt),
        "acceptance_terms": acceptance_terms(prompt, code),
    }


def compact_spec(spec: dict[str, Any], prompt: str) -> dict[str, Any]:
    """Reduce a mythos 06_scene_spec to the env's compact scene_spec shape."""

    objects = spec.get("objects") if isinstance(spec.get("objects"), list) else []
    compact_objects = [
        {"id": obj.get("id"), "type": obj.get("kind") or obj.get("type")}
        for obj in objects
        if isinstance(obj, dict)
    ][:40]
    animations = spec.get("animations") if isinstance(spec.get("animations"), list) else []
    compact_animations = [
        {"target": anim.get("target"), "action": anim.get("action")}
        for anim in animations
        if isinstance(anim, dict)
    ][:40]
    return {
        "scene_name": spec.get("scene_name"),
        "scene_class": spec.get("scene_class"),
        "camera": spec.get("camera"),
        "objects": compact_objects,
        "animations": compact_animations,
        "code_requirements": spec.get("code_requirements") or [],
        "metadata": {
            "original_prompt": prompt[:400],
            "requested_style": "mythos-cinematic",
        },
    }


def acceptance_terms(prompt: str, code: str) -> list[str]:
    """Prompt content words (rubric-matchable) + layout idioms present in gold code."""

    counts: dict[str, int] = {}
    order: list[str] = []
    for match in WORD_RE.finditer(prompt):
        word = match.group(0).casefold().strip("-")
        if len(word) < 4 or word in STOP_WORDS:
            continue
        if word not in counts:
            order.append(word)
        counts[word] = counts.get(word, 0) + 1
    ranked = sorted(order, key=lambda w: (-counts[w], order.index(w)))
    terms = ranked[:MAX_PROMPT_TERMS]
    for term in LAYOUT_TERMS:
        if term in code and term not in terms:
            terms.append(term)
    return terms


def _discover_scene_name(code: str) -> str | None:
    match = re.search(r"class\s+(\w+)\s*\(\s*\w*Scene\w*\s*\)", code)
    return match.group(1) if match else None


def _read_json(path: Path) -> dict[str, Any]:
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return {}
    return payload if isinstance(payload, dict) else {}
