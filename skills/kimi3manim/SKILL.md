---
name: kimi3manim
description: >
  Turn any math or physics concept into a rendered Manim film via the
  Kimi3Manim six-agent K3 pipeline. Use when the user asks to animate,
  visualize, or make a video/film of a mathematical or physical concept
  (from middle-school geometry to graduate physics), to resume or debug a
  failed animation run, or to re-render an existing Manim scene. Requires
  the Kimi3Manim repository and a Kimi subscription login or Moonshot API
  key.
---

# Kimi3Manim: concept to rendered film

This skill drives the six-agent Kimi K3 pipeline in the Kimi3Manim
repository (https://github.com/HarleyCoops/KimiK3Manim): Concept Scout,
Mathematical Enricher, Visual Designer, Narrative Composer, Manim Coder,
and a vision Render Critic in a closed repair loop, orchestrated by a
deterministic supervisor.

## Prerequisites (verify before first run)

1. Working directory is a Kimi3Manim checkout (`k3_agents/` exists). If
   not: `git clone https://github.com/HarleyCoops/KimiK3Manim.git`.
2. `uv sync` completes (installs manim and all Python deps).
3. System packages: ffmpeg, texlive, texlive-latex-extra, dvisvgm.
4. Auth, either:
   - Subscription (default): `uv run kimi login` once (Kimi Code OAuth), or
   - API key: `MOONSHOT_API_KEY=sk-...` in `.env` (also enables the
     vision critic stage, which subscription-only auth cannot run yet).

The supervisor runs a preflight and aborts with instructions if the
environment is broken - surface its message to the user verbatim.

## Creating an animation

```bash
uv run python -m k3_agents.supervisor "<concept>" --quality qh
```

- Quality: ql 480p (fast smoke test), qm 720p, qh 1080p, qk 4K.
- `--max-repairs N` bounds coder/critic repair rounds (default 3).
- Phrase the concept the way the intended audience would ask the
  question; the Scout calibrates prerequisite depth from the phrasing.
  Works at every level - "why the Pythagorean theorem is true" is as
  valid as "the double cover of SO(3)".
- A run takes minutes (six kimi-k3 calls at max reasoning, plus
  rendering) and spends Kimi quota; warn the user before starting and do
  not launch runs in parallel.

Outputs land in `output/k3_runs/<slug>/`: numbered JSON artifacts
(01 knowledge graph through 06 critique), generated scenes in `scenes/`,
per-attempt `render_attemptN.log`, and the mp4 under `media/`.

## Resuming and debugging

- Resume a run whose stages 1-4 succeeded (cheap - skips straight to the
  coder): `uv run python resume_pipeline.py [run_dir]`; with no argument
  it picks the latest resumable run.
- Render failures: read the newest `render_attemptN.log` in the run dir
  BEFORE re-running. Environment-signature failures (missing manim,
  latex, pango) abort immediately by design - fix the environment, do
  not retry the pipeline.
- Re-render any scene without model calls:
  `uv run manim -qh <file.py> <SceneClass>`.
- Re-running the same concept reuses its run directory; move it aside
  first for a clean slate.

## MCP alternative

The same operations are exposed as MCP tools (check_environment,
create_animation, resume_run, list_runs, render_scene) by
`mcp_server.py` in the repo root:

```bash
claude mcp add kimi3manim -- uv --directory <repo> run python mcp_server.py
```

Prefer the CLI commands when working inside the repo; prefer the MCP
server when animating from another project or client.

## Conventions

- Never send environment errors to the coder repair loop.
- Ship the mp4 to the user even if the critic stage was unavailable.
- Artifacts are plain JSON and scenes are plain Manim: the user can stop
  at any stage and hand-edit - offer that when a run partially fails.
