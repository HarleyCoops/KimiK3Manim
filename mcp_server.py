"""Kimi3Manim MCP server.

Exposes the K3 agent-swarm animation pipeline as Model Context Protocol
tools, so any MCP client (Claude Code, Kimi Code, Claude Desktop, Zed...)
can turn a math or physics concept into a rendered film with one call.

Run (stdio transport):
    uv run python mcp_server.py

Register with Claude Code:
    claude mcp add kimi3manim -- uv --directory /path/to/KimiK3Manim run python mcp_server.py

Register with Kimi Code: add the same command under /mcp-config.
"""

from __future__ import annotations

import json
from pathlib import Path

from fastmcp import FastMCP

mcp = FastMCP(
    "kimi3manim",
    instructions=(
        "Turn math and physics concepts into rendered Manim films via a "
        "six-agent Kimi K3 pipeline. Start with check_environment once per "
        "session; use create_animation for new concepts (minutes-long, "
        "spends Kimi quota), resume_run to continue a failed run without "
        "re-paying for completed stages, and render_scene to re-render "
        "any existing scene file without model calls."
    ),
)

RUNS_ROOT = Path("output/k3_runs")


def _supervisor(quality: str = "qm", max_repairs: int = 3):
    from k3_agents.supervisor import Supervisor

    return Supervisor(max_repair_rounds=max_repairs,
                      render_quality=f"-{quality}")


@mcp.tool
def check_environment() -> str:
    """Verify the render environment (manim, ffmpeg, latex) and auth mode.

    Call this first in a session. Returns 'ready' plus the active auth
    mode, or the exact problems and how to fix them.
    """
    try:
        _supervisor().preflight()
    except RuntimeError as exc:
        return str(exc)
    try:
        from config import KIMI_AUTH_MODE, MOONSHOT_API_KEY
        from k3_agents.runtime import subscription_available

        ok, reason = subscription_available()
        auth = (
            f"subscription (CLI/SDK ready)" if ok and KIMI_AUTH_MODE == "subscription"
            else f"api-key" if MOONSHOT_API_KEY
            else f"NO AUTH: {reason}; run 'uv run kimi login' or set MOONSHOT_API_KEY"
        )
    except Exception as exc:  # pragma: no cover
        auth = f"auth check failed: {exc}"
    return f"ready; auth: {auth}"


@mcp.tool
def create_animation(concept: str, quality: str = "qm", max_repairs: int = 3) -> str:
    """Run the full six-agent pipeline: concept in, mp4 out.

    Takes minutes and spends Kimi quota (six kimi-k3 calls at max
    reasoning plus renders). quality: ql=480p, qm=720p, qh=1080p, qk=4K.
    Returns JSON with run_dir, video path, and critique result. Artifacts
    (knowledge graph, screenplay, scene code, render logs) persist in
    run_dir for inspection or resume.
    """
    result = _supervisor(quality, max_repairs).run(concept, verbose=False)
    return json.dumps({
        "run_dir": str(result.run_dir),
        "video": str(result.video_path) if result.video_path else None,
        "repair_rounds": result.repair_rounds,
        "critique": (
            {"passed": result.critique.passed, "score": result.critique.score}
            if result.critique else None
        ),
    })


@mcp.tool
def list_runs() -> str:
    """List pipeline runs with their furthest completed stage and video, if any.

    Use to find resumable runs (stage>=4, no video) for resume_run.
    """
    rows = []
    if RUNS_ROOT.exists():
        for d in sorted(RUNS_ROOT.iterdir(), key=lambda p: p.stat().st_mtime,
                        reverse=True):
            if not d.is_dir():
                continue
            stages = sorted(p.name[:2] for p in d.glob("0*_*.json"))
            mp4s = list(d.rglob("*.mp4"))
            rows.append({
                "run_dir": str(d),
                "furthest_stage": stages[-1] if stages else None,
                "video": str(mp4s[-1]) if mp4s else None,
            })
    return json.dumps(rows)


@mcp.tool
def resume_run(run_dir: str = "", quality: str = "qm", max_repairs: int = 3) -> str:
    """Resume a run at Stage 5 (coder) from saved stage 1-4 artifacts.

    Much cheaper than create_animation: skips scout/enricher/designer/
    composer. Empty run_dir picks the most recent resumable run. Returns
    JSON like create_animation.
    """
    from schemas import MathEnrichment, KnowledgeGraph, Narrative, VisualSpec
    from k3_agents.manim_coder import ManimCoder
    from k3_agents.render_critic import RenderCritic

    if run_dir:
        rd = Path(run_dir)
    else:
        candidates = [d for d in RUNS_ROOT.iterdir()
                      if d.is_dir() and (d / "04_narrative.json").exists()]
        if not candidates:
            return json.dumps({"error": "no resumable runs found"})
        rd = max(candidates, key=lambda d: d.stat().st_mtime)

    def load(name, cls):
        return cls.model_validate_json((rd / name).read_text(encoding="utf-8"))

    sup = _supervisor(quality, max_repairs)
    sup.preflight()
    visual = load("03_visual_spec.json", VisualSpec)
    narrative = load("04_narrative.json", Narrative)

    coder = ManimCoder()
    bundle = coder.write_scenes(narrative, visual)
    sup._save(rd, "05_scene_bundle", bundle)

    critique = None
    video = None
    rounds = 0
    while rounds <= sup.max_repair_rounds:
        sup._write_bundle(rd, bundle)
        ok, log, video = sup._render(rd, bundle, rounds + 1)
        if not ok:
            rounds += 1
            bundle = coder.fix_scenes(bundle, log)
            sup._save(rd, f"05_scene_bundle_fix{rounds}", bundle)
            continue
        try:
            frames = sup._sample_frames(rd, video)
            critique = RenderCritic().critique(visual, frames)
            sup._save(rd, f"06_critique_round{rounds}", critique)
        except RuntimeError:
            break  # vision stage unavailable on subscription-only auth
        if critique.passed:
            break
        rounds += 1
        if rounds > sup.max_repair_rounds:
            break
        bundle = coder.fix_scenes(bundle, "\n".join(critique.issues))
        sup._save(rd, f"05_scene_bundle_fix{rounds}", bundle)

    return json.dumps({
        "run_dir": str(rd),
        "video": str(video) if video else None,
        "repair_rounds": rounds,
        "critique": (
            {"passed": critique.passed, "score": critique.score}
            if critique else None
        ),
    })


@mcp.tool
def render_scene(file: str, scene_class: str, quality: str = "qh") -> str:
    """Render an existing Manim scene file to mp4 - no model calls, no quota.

    file: path to a .py scene (curated in manim_scenes/ or generated in a
    run dir). Returns JSON with the video path or the render error tail.
    """
    import subprocess
    import sys

    _supervisor().preflight()
    proc = subprocess.run(
        [sys.executable, "-m", "manim", f"-{quality}", file, scene_class],
        capture_output=True, text=True, timeout=3600,
    )
    if proc.returncode != 0:
        return json.dumps({"error": (proc.stdout + proc.stderr)[-2000:]})
    mp4s = sorted(Path("media").rglob(f"*{scene_class}.mp4"),
                  key=lambda p: p.stat().st_mtime)
    return json.dumps({"video": str(mp4s[-1]) if mp4s else None})


if __name__ == "__main__":
    mcp.run()
