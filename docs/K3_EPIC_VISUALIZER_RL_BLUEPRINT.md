# K3 Epic Visualizer + Self-Improving Manim RL — Master Blueprint

Status: SYNTHESIS (2026-07-17). Consolidates inspection of three local
codebases + fresh research on Manim CE 0.19.x and the Prime Intellect RL
stack. Companion research files:
`research/manim_ce_3d_briefing.md`, `research/prime-intellect-rl-stack-briefing.md`.

---

## Part 0 — Ground truth: what we actually have

### Codebase inventory

| Codebase | Path | State |
|---|---|---|
| KimiK2Manim (this workspace) | `C:\Users\chris\KimiK2Manim` | **Live K3 agent swarm.** 6 specialist agents on `kimi-k3` (concept_scout, math_enricher, visual_designer, narrative_composer, manim_coder, render_critic), deterministic supervisor, strict json_schema artifacts (`schemas/artifacts.py`), e2b sandbox present, existing 3D scenes (`epic_rhombicosidodecahedron.py`, `bak_sneppen_3d.py`, `k3_harmonic_universe.py`). Latest commit: Euler's Identity hero film, Kosong removed. |
| Math-To-Manim | `C:\Users\chris\Math-To-Manim` | **v1.1.0 live** = `mythos/` (Claude Fable 5 film chain) + `sol/` (Codex CLI silo). The entire v1.0 RL pipeline (typed pipeline, Verifiers env, evals, Hermes agent) was **archived 2026-07-06** and is not installed. ~28 mythos run bundles exist; several 2026-07-08 bundles are empty (crashed runs). Zero Kimi references in code. |
| Math-To-Manim-prime-rl | `C:\Users\chris\Math-To-Manim-prime-rl` | **Git worktree of the same repo (broken gitlink)** holding the newest RL assets: Verifiers env `m2m2_visual_repair` **v0.1.13** (superset of the archived v1.0 copy — adds RLM mode with sandboxed REPL helpers), 9 prime-rl-style TOML configs, evidence of hosted launches (10 monitor scripts, `.prime/env-metadata.json`, published as `harleycooper/math-to-manim@0.1.1`, one claimed 25-step W&B pilot on `Qwen/Qwen3.5-35B-A3B`). verifiers pinned `==0.1.14`; no local torch/vllm/prime-rl. |

### Key corrections from research

1. **Manim "community .19" is superseded**: latest 0.19.x is **0.19.2** (2026-01-17); current stable is **0.20.1** (2026-02-27). 3D API unchanged between them. 0.19.2 bumps minimum Python to 3.11 — fine (this repo requires ≥3.13).
2. **The RL reward is 100% static** (AST/regex/text heuristics): nothing executes, renders, or judges visuals. It's gameable (stuff acceptance terms, sprinkle `scale_to_fit_width`). Designed-and-rejected in docs, now must be built.
3. **The dataset is a stub**: `repair_tasks.jsonl` = exactly **2 tasks**. The exporter was never run at scale.
4. **verifiers 0.1.14 pin is stale**: prime-rl 0.7.0 (current `main`) requires `verifiers>=0.2.0`; a v1 Taskset/Harness API now exists. Upgrading needs re-validation of the RLM harness and the renderer-pool monkeypatch (`rlm.py:484-509`).
5. **Config bug**: `repair_train.toml` says `Qwen/Qwen3-30B-A3B-Instruct-2507` while orch/infer say `Qwen/Qwen3.5-35B-A3B` — train/infer mismatch; `Qwen3.5-*` names must be verified against Prime before reuse.
6. **No live pipeline → RL bridge**: mythos bundle filenames (`01_intent.json…mythos_scene.py`) don't match the exporter's expected names (`request.json`, `generated_code.json`, …). An adapter is required.

---

## Part 1 — The Epic Visualizer: what makes it K3-native

Any LLM can be asked to write Manim. The K3 swarm's edge comes from four
properties no smaller pipeline combines — the design below exploits each.

### 1.1 Whole-film single context (1M tokens)

K2-era pipelines lost coherence between per-node calls. K3 holds the
**entire knowledge graph + full screenplay + cinematography spec + every
prior scene's code** in one session. Consequence: leitmotifs (a color, a
camera move, a geometric motif) can recur and pay off across a 10-scene
film — impossible in per-node designs. This is the first uniqueness axis:
**films, not clips.**

### 1.2 The K3 House Style (signature 3D look)

Encode a repeatable visual grammar in `visual_designer` + a shared
`manim_utils` kit so output is recognizably "a K3 film":

- **Palette**: deep-space background (`#0A0E1A`), neon accents via HSV
  color space (0.19 feature), surface gradients with
  `Surface.set_fill_by_value(axes, colorscale=[(BLUE,-1),(TEAL,0),(GOLD,1)])`
  — the most underused epic-3D tool in CE.
- **Light**: `shade_in_3d=True`, deliberate `camera.light_source.move_to()`
  choreography; `set_sheen()` sweeps as cheap specular.
- **Camera**: never the default (phi=0, theta=-90° looks 2D — the #1
  failure). Signature moves: `move_camera(phi, theta, frame_center,
  focal_distance)` fly-throughs, `begin_ambient_camera_rotation(rate)`,
  `exponential_projection=True` for near-plane drama, short
  `focal_distance` (2–5) for wide-angle tension.
- **Glow without manimgl**: layered strokes (same path, growing
  `stroke_width`, shrinking `stroke_opacity`) + low-opacity scaled copies;
  fake contact shadows (flattened dark copies); distance-fog updaters
  (opacity vs camera distance).
- **Text discipline**: `MathTex` billboarded via
  `add_fixed_orientation_mobjects`, HUD via `add_fixed_in_frame_mobjects`
  — and every wide TeX gets `scale_to_fit_width` (this is exactly what the
  RL `layout_static` reward measures; house style and reward align).

### 1.3 A parameterized epic-3D template kit (new module)

Instead of asking the coder to invent 3D from scratch every time, give it
a composable kit — `manim_utils/epic3d.py` (new):

| Template | Core machinery | Use |
|---|---|---|
| `CosmicFlythrough` | `move_camera` spline + `exponential_projection` + fog updaters | scene transitions, reveals |
| `SurfaceMorph` | two `Surface`s, identical `resolution`, `Transform` | parametric → geometry narrative |
| `PolyhedronBuild` | `Polyhedron` subclasses / `ConvexHull3D` (0.19) + `GrowFromCenter` | Euler's identity, symmetry films |
| `GradientField` | `set_fill_by_value` + animated colorscale pivots via `ValueTracker` | potential/curvature viz |
| `NeonNetwork` | `Line3D`/`Dot3D` constellations + layered-stroke glow | SlowFastNetwork-style graphs in 3D |
| `BillboardHud` | fixed-orientation/in-frame text manager with guaranteed cleanup (`FadeOut` pairs) | all narration |

Budget rules baked in: `Surface.resolution` ≤ 32 while iterating (res 64
= 4096 faces ≈ linear Cairo cost), `-ql` for drafts, `-qh/-qk` only for
finals, `stroke_width=0` on dense surfaces to kill grid seams, no
interpenetrating surfaces (painter's algorithm sorts per-mobject —
intersection pops). These rules become **both** prompt scaffolding and RL
reward terms — one grammar, two consumers.

### 1.4 Vision-closed loop (the real differentiator)

`render_critic` is already a vision agent. Make the loop first-class:
render `-ql` → sample 6 frames → critic scores against the visual_spec →
targeted repair instructions → manim_coder fixes (max N rounds). This
produces, as a byproduct, **exactly the (prompt, code, evidence, verdict)
records the RL pipeline eats.** The visualizer and the RL program are the
same machine seen from two sides.

---

## Part 2 — Operationalizing the RL pipeline

Goal restated: a continuously running loop that trains an open student
model to write/repair Manim code increasingly well, with K3 as
scout/designer/critic/teacher, on Prime Intellect infrastructure.

### Phase 0 — Consolidate the RL assets (1–2 days)

1. Choose the home: `Math-To-Manim-prime-rl`'s env is the superset
   (v0.1.13, RLM mode). Copy `environments/math_to_manim/` into a fresh
   repo or restore it into `Math-To-Manim` main (un-archive). Fix or
   abandon the broken git worktree link (files are intact; VCS is dead).
2. Upgrade `verifiers==0.1.14` → current 0.2.x; re-run the 14 unit tests;
   re-validate the RLM harness against the v1 Taskset API and re-check the
   `create_renderer_pool` monkeypatch.
3. Fix the train/infer model mismatch in `repair_*.toml`; verify all
   model IDs against Prime's current catalog.

### Phase 1 — Dataset at scale (week 1)

1. **Adapter** (new, ~100 lines): mythos bundle → `m2m2.pi_repair_task.v1`.
   Filename map: `01_intent.json`→`request.json`, `06_scene_spec.json`→
   `scene_spec.json`, `mythos_scene.py`→`generated_scene.py`, plus
   codegen/validation/review artifacts → `generated_code.json`,
   `validation_report.json`, `render_result.json`, `review_report.json`.
2. **K3 exporter** (new): `k3_agents` artifacts (`schemas/artifacts.py`)
   → same task schema. This makes the dataset K3-flavored from day one —
   every failed/hacked K3 run becomes training data.
3. **Synthetic mutation engine**: take passing scenes, programmatically
   break them in the ways the rubric measures (crowd text, drop
   `scale_to_fit_width`, remove `FadeOut` cleanups, over-dense
   `arrange(buff=)`, invalid imports, missing `construct`) → paired
   (broken, fixed) repair tasks. This scales 28 bundles → 1k–10k tasks.
4. Difficulty tagging (easy/normal/hard by validation outcome) for the
   online data filtering later. Publish to HF as a versioned dataset.

### Phase 2 — Reward v2: render-verified (week 2)

Keep the existing 7-component static rubric as a cheap pre-filter but
demote it; add execution truth:

```python
vf.Rubric(funcs=[
    static_gate,      # existing weighted bundle, collapsed  → weight 0.25
    renders,          # manim -ql in sandbox, timeout 120s   → weight 0.45
    visual_quality,   # heuristics first, VLM judge later    → weight 0.30
])
```

- `renders`: Prime Sandbox with a pre-baked `manim+ffmpeg+LaTeX` image
  (CPU-only sandboxes are fine — Cairo is CPU). Run
  `manim -ql --media_dir /tmp scene.py SceneName`; success = MP4 exists
  & ≥ threshold bytes (mirrors `sol/validation.py`). **Mask** (don't
  zero-score) on sandbox/infra failure, per the `i3-code` pattern.
- `visual_quality` v1 (hack-resistant heuristics, no model): non-black
  pixel ratio across sampled frames, inter-frame variance (kills static
  black-scene hacks), duration ≥ spec, mobject/scene-class count.
- `visual_quality` v2 (later): VLM judge on sampled frames — K3 vision or
  a Qwen-VL endpoint via `JudgeRubric`. Verify image-input support first
  (unverified in current verifiers).
- Anti-hacking stack from prime-rl: `gibberish`, `repetition`,
  `zero_advantage` rollout filters + linear `length_penalty`.

### Phase 3 — SFT warmup + smoke GRPO (weeks 2–3)

1. **Teacher traces (SYNTHETIC-1 pattern)**: run the existing K3 swarm on
   50–100 concepts; keep only render-verified successes; distill ~2–5k
   (prompt → working scene) traces. SFT **Qwen3-4B-Instruct-2507**
   (dense, cheap, prime-rl HF-fallback path).
2. **Smoke GRPO**: single-file `rl.toml`, `type="grpo"`, `group_size=8`,
   `batch_size=128`, `max_tokens=4096`, 2 GPUs (marketplace 2×4090/A100
   or Hosted Training LoRA — Qwen3.5-4B at $0.10/$0.30/$0.30 per 1M
   tokens makes a smoke run cost dollars).
3. **Success gate before scaling**: reward climbs; held-out repair
   pass-rate up; sandbox render-success rate up; no divergence from the
   repetition/gibberish monitors.

### Phase 4 — Scale + the self-improvement flywheel (weeks 3–6)

1. Scale to **Qwen3-30B-A3B** (optimized MoE path in prime-rl) on a
   4–8×H100/H200 pod, or Hosted Training per-token ($0.25/$0.75/$1.00).
2. **Multi-turn repair** (`MultiTurnEnv`, feed render stderr back,
   `max_turns=3`) — compile-fix loops are where RL gains concentrate.
3. **Kimi K2/K3 as teacher, not student**: K2-Thinking open weights are
   1T params (not trainable on this budget; no optimized trainer path in
   prime-rl), but prime-rl ships `kimi-k2`/`kimi-k2.5` renderers and the
   algorithms layer supports **OPD (on-policy distillation) with an
   external OpenAI-compatible teacher** — K3 via `api.moonshot.ai` can be
   the teacher/judge while the Qwen student trains. **This is the
   Kimi-native core of the RL program.**
4. **The flywheel** (self-improvement, fully closed):
   student generates scenes → K3 render_critic scores frames → failures
   become new repair tasks (mutation engine + exporter) → difficulty
   pools refresh → next GRPO round. prime-rl's async continuous batching
   tolerates slow sandbox renders; `max_off_policy_steps` bounds
   staleness.
5. Publish env bump on the hub (`harleycooper/math-to-manim` → 0.2.0).

### Phase 5 — Productize: the student joins the swarm

Swap `manim_coder`'s backend: trained student does bulk codegen (cheap,
fast, Manim-specialized); K3 keeps scout/design/critique (where 1M
context and vision matter). Cost per film collapses; quality ratchets
because the critic that trains the student is the one grading its output.

---

## Part 3 — Risks & open questions

| Risk | Mitigation |
|---|---|
| verifiers 0.2.x API drift (RLM harness, monkeypatch) | Pin exactly; run env unit tests; prefer v0 SingleTurnEnv for first training, RLM later |
| Reward hacking (static-only terms) | Phase 2 render gate + heuristics + prime-rl filters; keep judge weight ≤0.3 |
| Render latency vs rollout throughput | `-ql`, 120 s timeouts, async continuous batching overlaps stragglers |
| K2 1T not trainable here | Student/teacher split (Qwen student, K3 teacher via OPD) |
| `Qwen3.5-*` / `poolside/Laguna-XS.2` IDs unverified | Verify against Prime catalog before reusing configs |
| RLM mode is POSIX-only (`fcntl`) | Train on Linux/Prime anyway; singleturn works on Windows for dev |
| LaTeX in sandboxes | Pre-bake TeXLive into the sandbox image |

## Cost sketch (order of magnitude)

- Smoke GRPO (4B, Hosted LoRA): **< $10**. Dataset build renders
  (1k × ~2 min @ $0.08/hr): **< $3**. 30B scale run: low hundreds of
  dollars at per-token pricing. K3 teacher/critic calls: ~$2–3 per film
  (existing repo model), reduced by prefix caching.

## Immediate next actions (in order)

1. Copy `environments/math_to_manim` v0.1.13 → canonical home; bump
   verifiers; green unit tests.
2. Write the mythos→`pi_repair_task.v1` adapter; export the ~28 bundles;
   run the mutation engine → dataset v1 on HF.
3. Add the `renders` sandbox component to `scoring.py`; smoke `vf-eval`.
4. Scaffold `manim_utils/epic3d.py` (template kit) and wire it into
   `visual_designer`/`manim_coder` prompts.
5. First Hosted-LoRA GRPO smoke on Qwen3.5-4B.
