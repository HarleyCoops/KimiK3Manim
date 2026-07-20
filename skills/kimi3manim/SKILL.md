---
name: kimi3manim
description: Turn math and physics concepts into rendered Manim films
version: 1.0.0
author: HarleyCoops
license: MIT
metadata:
  hermes:
    tags: [Education, Mathematics, Physics, Animation, Manim, Video]
    config:
      - key: kimi3manim.repo
        description: Path to a local KimiK3Manim checkout
        default: "~/KimiK3Manim"
        prompt: KimiK3Manim repository path
required_environment_variables:
  - name: MOONSHOT_API_KEY
    prompt: Moonshot/Kimi platform API key (optional)
    help: Create one at https://platform.kimi.ai - OR skip and run 'uv run kimi login' for subscription auth
    required_for: api-key auth mode and the vision Render Critic stage
---

# Kimi3Manim: concept to rendered film

Drive the Kimi3Manim six-agent pipeline (Concept Scout, Mathematical
Enricher, Visual Designer, Narrative Composer, Manim Coder, vision Render
Critic under a deterministic supervisor) to turn any math or physics
concept into a rendered 1080p Manim film.

## When to Use

- The user asks to animate, visualize, or make a video/film of a
  mathematical or physical concept, at any level from middle-school
  geometry to graduate physics.
- The user wants to resume or debug a failed animation run.
- The user wants an existing Manim scene re-rendered.

## Quick Reference

| Task | Command (run in the repo directory) |
|---|---|
| Full pipeline, concept to mp4 | `uv run python -m k3_agents.supervisor "<concept>" --quality qh` |
| Resume failed run at Stage 5 | `uv run python resume_pipeline.py [run_dir]` |
| Re-render a scene, no model calls | `uv run manim -qh <file.py> <SceneClass>` |
| One-time subscription login | `uv run kimi login` |
| Install deps | `uv sync` |

Quality flags: ql 480p (smoke test), qm 720p, qh 1080p, qk 4K.
`--max-repairs N` bounds coder/critic repair rounds (default 3).

## Procedure

1. Locate the repo (config `kimi3manim.repo`, default `~/KimiK3Manim`).
   Missing? `git clone https://github.com/HarleyCoops/KimiK3Manim.git`,
   then `uv sync` inside it. System deps: ffmpeg, texlive,
   texlive-latex-extra, dvisvgm.
2. Verify auth: either the user ran `uv run kimi login` once (Kimi Code
   OAuth subscription - the default), or `MOONSHOT_API_KEY` is set in
   `.env` (also enables the vision critic stage).
3. Warn the user that a full run takes minutes and spends Kimi quota
   (six kimi-k3 calls at max reasoning plus rendering); never launch
   runs in parallel.
4. Phrase the concept the way the intended audience would ask it - the
   Scout calibrates prerequisite depth from the phrasing. "why the
   Pythagorean theorem is true" is as valid as "the double cover of
   SO(3)".
5. Run the supervisor command. The built-in preflight aborts with exact
   instructions if the environment is broken - relay its message
   verbatim and fix the environment; do not retry the pipeline.
6. Outputs land in `output/k3_runs/<slug>/`: numbered JSON artifacts
   (01 knowledge graph ... 06 critique), generated scenes in `scenes/`,
   per-attempt `render_attemptN.log`, and the mp4 under `media/`.
   Deliver the mp4. `[[as_document]]`

## Pitfalls

- Environment failures (missing manim/latex/pango) are NOT code bugs:
  the supervisor aborts on them by design. Fix the environment; never
  feed them to the coder repair loop.
- Re-running the same concept reuses its run directory - move it aside
  first for a clean slate.
- Subscription-only auth cannot run the Stage 6 vision critic; the run
  stops after rendering with the mp4 already on disk. Ship it and note
  the critic was skipped, or set MOONSHOT_API_KEY to enable it.
- On WSL, keep the clone in the Linux filesystem (not /mnt/c) or uv and
  renders run slowly; `export UV_LINK_MODE=copy` silences the hardlink
  warning.

## Verification

- The run directory contains an mp4 under `media/` and artifacts 01-05.
- On failure, read the newest `render_attemptN.log` in the run dir
  BEFORE re-running; it contains the real traceback.
- Sample a few frames (`ffmpeg -ss <t> -i <mp4> -frames:v 1 f.png`) and
  confirm equations are legible and scenes match the visual spec before
  presenting the film as final.
