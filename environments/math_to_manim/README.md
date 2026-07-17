# Math-To-Manim Visual Repair

Math-To-Manim turns short educational text prompts into rendered Manim
animations: typed planning artifacts, generated Python scenes, validation
reports, and MP4/GIF outputs.

This Prime Intellect environment closes the improvement loop. Instead of
training on abstract coding tasks, it trains models on real Math-To-Manim run
bundles: the original prompt, scene specification, generated Manim code,
render/validation evidence, and review signals. The model's job is to repair or
improve the already-working output so future generations become more correct,
more readable, and more visually robust.

In short:

```text
text prompt
  -> Math-To-Manim pipeline
  -> generated Manim scene
  -> MP4/GIF output + validation evidence
  -> Prime RL repair task
  -> better generated animation code
```

The current environment has two repair surfaces:

- `mode="singleturn"`: the baseline task with compact prompt evidence.
- `mode="rlm"`: a Verifiers v1/RLM task where the full M2M2 run bundle is
  uploaded into the REPL filesystem and inspected programmatically.

Both modes reward valid `GeneratedCode` JSON, parseable and safe Manim Python,
expected scene structure, preserved math intent, and static layout improvements
that reduce crowded text and formulas before expensive render audits.

## Environment

- Hub ID: `harleycooper/math-to-manim`
- Package: `math-to-manim`
- Import package: `m2m2_visual_repair`
- Task: generated-code repair for text-prompt-to-animation run bundles
- Verifiers: `>=0.2.0` (bumped from `==0.1.14` on 2026-07-17; singleturn mode
  validated against 0.2.0, RLM mode still pinned to the v1 harness API)

In RLM mode, the prompt stays small. The run bundle lives at
`/workspace/run_bundle`, and the REPL preloads:

```python
list_artifacts()
load_artifact("scene_spec")
load_artifact("storyboard")
read_generated_scene()
search_trace("layout")
validate_candidate(code)
score_candidate(scene_name, code)
submit_generated_code(scene_name, code)
```

The model works on a candidate copy and submits only the repaired
`GeneratedCode`. The canonical run bundle and trace are evidence, not outputs to
mutate.

The default dataset includes a QED/Minkowski layout-repair task from the README
GIF. Its reward includes static text-crowding checks for long formulas without
`scale_to_fit_width`, dense text grouping, and excessive fixed-frame overlays.
Full rendering remains an eval/audit step, not the per-rollout reward.
Prime/orchestrator `create_renderer_pool` errors are from Verifiers' LLM
prompt-renderer dependency, not Manim rendering. The environment leaves Prime's
platform `renderers` package installed and patches Verifiers' client binding at
load time when needed.

## Local Use

```bash
uv pip install -e environments/math_to_manim
uv run python -c "from m2m2_visual_repair import load_environment; env = load_environment(mode='singleturn'); print(len(env.dataset))"
uv run python -c "from m2m2_visual_repair import load_environment; env = load_environment(mode='rlm'); print(env.taskset.taskset_id)"
uv run vf-eval math-to-manim -n 2
```

RLM mode targets Linux/WSL/Prime runtimes. The current Verifiers v1 RLM harness
imports POSIX `fcntl`, so native Windows can load the single-turn baseline but
should use WSL2 or hosted Prime for RLM rollouts.

## Export M2M2 Runs

From the Math-To-Manim repo:

```bash
python -m math_to_manim.cli pi-export-runs \
  --runs-dir runs \
  --output environments/math_to_manim/m2m2_visual_repair/data/repair_tasks.jsonl
```

## Publish

Run from an authenticated Prime environment:

```bash
prime env push --path environments/math_to_manim --name math-to-manim --visibility PUBLIC
```

Inside Codex's workspace sandbox, use the writable-home wrapper:

```bash
prime-codex env push --path environments/math_to_manim --name math-to-manim --visibility PUBLIC
```

## Training Templates

Config snippets are bundled under `m2m2_visual_repair/configs/`.

- Smoke: `Qwen/Qwen3.5-0.8B`
- Practical repair: `Qwen/Qwen3-30B-A3B-Instruct-2507`
- Follow-up: `Qwen/Qwen3.5-397B-A17B`
