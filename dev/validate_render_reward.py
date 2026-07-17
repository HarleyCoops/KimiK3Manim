"""Validate reward v2: render gate + visual heuristics (blueprint Phase 2).

Four probe completions plus one rubric-level pass:

    a) animated scene   -> rendered, visual clearly above the black probe
    b) black/static     -> rendered but low visual (discrimination check)
    c) runtime-broken   -> status failed, render component 0
    d) manim missing    -> status infra_error, ledger masked=True

Run from the repo root:

    .venv/Scripts/python.exe dev/validate_render_reward.py
"""

from __future__ import annotations

import json
from pathlib import Path
import sys
import time

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT))

from environments.math_to_manim.m2m2_visual_repair import render_reward as rr
from environments.math_to_manim.m2m2_visual_repair.environment import (
    M2M2RenderRubric,
    load_environment,
)
from environments.math_to_manim.m2m2_visual_repair.render_reward import render_scene
from environments.math_to_manim.m2m2_visual_repair.visual_reward import visual_quality


ANIMATED_SCENE = '''
from manim import *

class RewardWaveScene(Scene):
    def construct(self):
        squares = VGroup(*[
            Square(side_length=1.1, fill_opacity=0.9,
                   color=interpolate_color(BLUE, PINK, i / 24))
            for i in range(25)
        ]).arrange_in_grid(5, 5, buff=0.25)
        self.play(LaggedStart(*[FadeIn(s, scale=0.5) for s in squares],
                              lag_ratio=0.05), run_time=2)
        self.play(squares.animate.shift(UP * 0.5).set_color(GREEN), run_time=1)
        self.wait(0.3)
'''

BLACK_SCENE = '''
from manim import *

class RewardBlackScene(Scene):
    def construct(self):
        self.wait(2)
'''

BROKEN_SCENE = '''
from manim import *

class RewardBrokenScene(Scene):
    def construct(self):
        self.play(Create(UndefinedMobjectName()))
        self.wait(1)
'''


def probe(label: str, scene_name: str, code: str) -> tuple[rr.RenderResult, float]:
    started = time.monotonic()
    result = render_scene(scene_name, code, quality="ql", timeout_s=120)
    score, metrics = visual_quality(result.mp4_path) if result.rendered else (0.0, None)
    wall = time.monotonic() - started
    print(f"[{label}] status={result.status} bytes={result.mp4_bytes} "
          f"visual={score:.3f} wall={wall:.1f}s")
    if metrics is not None:
        print(f"    non_black={metrics.non_black_ratio} motion={metrics.motion} "
              f"color={metrics.color} duration_s={metrics.duration_s}")
    if result.status != "rendered":
        print(f"    stderr_tail: {result.stderr_tail[-200:]}")
    return result, score


def completion_for(scene_name: str, code: str) -> list[dict[str, str]]:
    payload = json.dumps({"scene_name": scene_name, "language": "python", "code": code})
    return [{"role": "assistant", "content": f"<generated_code>{payload}</generated_code>"}]


def main() -> int:
    failures: list[str] = []

    print("== probe renders ==")
    animated, animated_visual = probe("animated", "RewardWaveScene", ANIMATED_SCENE)
    black, black_visual = probe("black", "RewardBlackScene", BLACK_SCENE)
    broken, _ = probe("broken", "RewardBrokenScene", BROKEN_SCENE)

    if not animated.rendered:
        failures.append("animated scene did not render")
    if not black.rendered:
        failures.append("black scene did not render")
    if broken.status != "failed" or broken.rendered:
        failures.append(f"broken scene expected status=failed, got {broken.status}")
    if animated_visual <= black_visual + 0.1:
        failures.append(
            f"visual heuristics do not discriminate: animated={animated_visual:.3f} "
            f"black={black_visual:.3f}"
        )
    if black_visual >= 0.25:
        failures.append(f"black scene visual too high: {black_visual:.3f}")

    print("\n== infra mask ==")
    original = rr.resolve_manim_command
    rr.resolve_manim_command = lambda: None
    try:
        masked = render_scene("RewardWaveScene", ANIMATED_SCENE)
    finally:
        rr.resolve_manim_command = original
    print(f"[infra] status={masked.status} infra_error={masked.infra_error}")
    if masked.status != "infra_error" or not masked.infra_error:
        failures.append(f"infra mask expected infra_error, got {masked.status}")

    print("\n== rubric level (reward_mode=render) ==")
    env = load_environment(reward_mode="render", render_timeout_s=120)
    print(f"loaded env: {len(env.dataset)} train examples, rubric={type(env.rubric).__name__}")

    rubric = M2M2RenderRubric(timeout_s=120)
    answer = json.dumps({"task_id": "probe", "scene_name": "RewardWaveScene"})
    started = time.monotonic()
    score = rubric.score(completion_for("RewardWaveScene", ANIMATED_SCENE), answer)
    print(f"[rubric animated] score={score:.3f} wall={time.monotonic() - started:.1f}s")
    ledger = rubric.get_last_ledger()
    render_info = (ledger or {}).get("render", {})
    print(f"    render={render_info.get('status')} masked={render_info.get('masked')} "
          f"visual={ledger.get('visual_reward') if ledger else None}")
    if not (0.4 < score <= 1.0):
        failures.append(f"rubric animated score out of expected band: {score:.3f}")
    if render_info.get("status") != "rendered" or render_info.get("masked"):
        failures.append("rubric ledger did not record a clean render")

    rubric_broken = M2M2RenderRubric(timeout_s=120)
    score_broken = rubric_broken.score(completion_for("RewardBrokenScene", BROKEN_SCENE), answer)
    ledger_broken = rubric_broken.get_last_ledger() or {}
    print(f"[rubric broken] score={score_broken:.3f} "
          f"render_reward={ledger_broken.get('render_reward')}")
    if ledger_broken.get("render_reward") != 0.0:
        failures.append("broken completion should score 0 on the render gate")

    print("\n== summary ==")
    if failures:
        for failure in failures:
            print(f"FAIL: {failure}")
        return 1
    print("all render-reward validations passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
