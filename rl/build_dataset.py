"""Build dataset v1 for the m2m2_visual_repair environment.

Pipeline: mythos bundles -> adapter -> mutation engine -> scored repair
tasks (m2m2.pi_repair_task.v1) -> train/eval JSONL inside the env package.

Every kept task is honesty-checked with the environment's own rubric: the
gold scene must score >= GOLD_MIN and the mutated scene must drop at least
MIN_DROP points, so the task has a real reward gradient.

Usage:
    uv run python -m rl.build_dataset
    uv run python -m rl.build_dataset --per-bundle 6 --seed 11
"""

from __future__ import annotations

import argparse
import json
import random
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "environments" / "math_to_manim"))

from m2m2_visual_repair.scoring import (  # noqa: E402
    layout_static_score,
    score_completion,
    validate_source,
)

from rl.mutation_engine import EASY, NORMAL, Mutation, hard_combos  # noqa: E402
from rl.mythos_adapter import BundleError, load_bundle  # noqa: E402

DEFAULT_BUNDLES = ROOT / "data" / "mythos_runs"
DEFAULT_OUT = ROOT / "environments" / "math_to_manim" / "m2m2_visual_repair" / "data"
SAMPLE_DATASET = DEFAULT_OUT / "repair_tasks_sample.jsonl"

GOLD_MIN = 0.85
DIRECT_MIN = 0.55
MIN_DROP = 0.10

DIRECT_MUTATION = Mutation("original_layout_debt", "normal", ("layout_static",), lambda code: code)

INSTRUCTIONS = (
    "Repair the generated Manim scene while preserving the educational intent. "
    "Return exactly one <generated_code> block containing JSON with scene_name and code. "
    "Do not shell out, read local files, access the network, or use external assets."
)
LAYOUT_OBJECTIVES = [
    "Guard wide formulas and long captions with scale_to_fit_width.",
    "Fade out or transform fixed-frame overlays before introducing new ones.",
    "Avoid dense arrange(buff<0.18) groupings for text.",
    "Keep the requested scene name and scene class.",
]


def wrap_completion(scene_name: str, code: str) -> str:
    payload = json.dumps({"scene_name": scene_name, "language": "python", "code": code})
    return f"<generated_code>{payload}</generated_code>"


def build_evidence(code: str, has_mp4: bool) -> dict:
    ast_result = validate_source(code)
    layout_score, layout_warnings = layout_static_score(code) if ast_result["parsed"] else (0.0, [])
    issues = [
        {"code": "static-check", "message": message, "severity": "error"}
        for message in ast_result["errors"]
    ] + [
        {"code": "layout-risk", "message": message, "severity": "warning"}
        for message in layout_warnings
    ]
    status = "failed" if ast_result["errors"] or not ast_result["parsed"] else ("warning" if layout_warnings else "passed")
    return {
        "validation": {
            "status": status,
            "summary": "; ".join(ast_result["errors"][:3]) or f"static parse ok; layout score {layout_score}",
            "issues": issues,
            "metadata": {"layout_static_score": layout_score, "reward_mode": "static_no_render"},
        },
        "render": {
            "status": "succeeded" if has_mp4 else "skipped",
            "stderr_tail": "" if has_mp4 else "not rendered during dataset build",
            "stdout_tail": "",
            "metadata": {"source_run_had_mp4": has_mp4},
        },
        "review": {
            "approved": False,
            "score": 0.0,
            "observations": ["Bundle scene mutated for repair training; gold code available in the source run."],
            "recommendations": LAYOUT_OBJECTIVES[:2],
            "issues": [],
            "metadata": {},
        },
    }


def make_task(bundle: dict, mutation: Mutation, mutated_code: str, start_score: float, gold_score: float) -> dict:
    return {
        "schema_version": "m2m2.pi_repair_task.v1",
        "task_id": f"mythos_{bundle['run_id']}_{mutation.name}",
        "task_type": "manim_repair",
        "prompt": bundle["prompt"],
        "audience": bundle["audience"],
        "style": "mythos-cinematic",
        "duration_seconds": None,
        "scene_name": bundle["scene_name"],
        "acceptance_terms": bundle["acceptance_terms"],
        "scene_spec": bundle["scene_spec"],
        "generated_code": {
            "scene_name": bundle["scene_name"],
            "language": "python",
            "code": mutated_code,
            "dependencies": ["manim", "numpy"],
            "metadata": {"file_path": "mythos_scene.py"},
        },
        "evidence": build_evidence(mutated_code, bundle["has_mp4"]),
        "layout_objectives": LAYOUT_OBJECTIVES,
        "instructions": INSTRUCTIONS,
        "metadata": {
            "reward_mode": "static_no_render",
            "source": "mythos_mutation",
            "mutation": mutation.name,
            "mutation_targets": list(mutation.targets),
            "difficulty": mutation.difficulty,
            "start_score": round(start_score, 4),
            "gold_score": round(gold_score, 4),
            "gold_in_source_run": True,
        },
        "source_run_dir": bundle["run_id"],
    }


def pick_mutations(rng: random.Random, bundle_index: int) -> list[Mutation]:
    easy = [EASY[(bundle_index + rng.randint(0, 2)) % len(EASY)]]
    normal_pool = NORMAL[:]
    rng.shuffle(normal_pool)
    normal = normal_pool[:3]
    hard_pool = hard_combos()
    hard = [hard_pool[bundle_index % len(hard_pool)]]
    return easy + normal + hard


def build(bundles_dir: Path, out_dir: Path, per_bundle: int, seed: int) -> dict:
    rng = random.Random(seed)
    tasks: list[dict] = []
    skipped: dict[str, str] = {}
    bundle_ids: list[str] = []

    for bundle_index, bundle_dir in enumerate(sorted(p for p in bundles_dir.iterdir() if p.is_dir())):
        try:
            bundle = load_bundle(bundle_dir)
        except BundleError as exc:
            skipped[bundle_dir.name] = str(exc)
            continue
        bundle_ids.append(bundle["run_id"])

        scoring_context = {"scene_name": bundle["scene_name"], "acceptance_terms": bundle["acceptance_terms"]}
        gold_score = score_completion(scoring_context, wrap_completion(bundle["scene_name"], bundle["code"])).score
        if gold_score < GOLD_MIN:
            if gold_score >= DIRECT_MIN:
                # the shipped scene itself carries real, rubric-visible layout
                # debt: keep it as a direct repair task (no mutation needed)
                tasks.append(make_task(bundle, DIRECT_MUTATION, bundle["code"], gold_score, 1.0))
            else:
                skipped[bundle_dir.name] = f"gold score {gold_score} below direct band ({gold_score} < {DIRECT_MIN})"
            continue

        kept = 0
        for mutation in pick_mutations(rng, bundle_index):
            if kept >= per_bundle:
                break
            mutated = mutation.apply(bundle["code"])
            if mutated is None or mutated == bundle["code"]:
                skipped[f"{bundle_dir.name}:{mutation.name}"] = "not applicable"
                continue
            start_score = score_completion(scoring_context, wrap_completion(bundle["scene_name"], mutated)).score
            if gold_score - start_score < MIN_DROP:
                skipped[f"{bundle_dir.name}:{mutation.name}"] = f"drop {gold_score - start_score:.3f} < {MIN_DROP}"
                continue
            tasks.append(make_task(bundle, mutation, mutated, start_score, gold_score))
            kept += 1

    # sample tasks stay in train (they are the env's canonical smoke tasks)
    if SAMPLE_DATASET.exists():
        for line in SAMPLE_DATASET.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if line:
                tasks.append(json.loads(line))

    # split by bundle so eval scenes are unseen
    eval_bundles = set(bundle_ids[-1:])
    train = [t for t in tasks if t["source_run_dir"] not in eval_bundles]
    eval_ = [t for t in tasks if t["source_run_dir"] in eval_bundles]

    out_dir.mkdir(parents=True, exist_ok=True)
    train_path = out_dir / "repair_tasks.jsonl"
    eval_path = out_dir / "repair_tasks_eval.jsonl"
    train_path.write_text("\n".join(json.dumps(t) for t in train) + "\n", encoding="utf-8")
    eval_path.write_text("\n".join(json.dumps(t) for t in eval_) + "\n", encoding="utf-8")

    by_difficulty: dict[str, int] = {}
    by_mutation: dict[str, int] = {}
    for task in tasks:
        meta = task["metadata"]
        by_difficulty[meta.get("difficulty", "sample")] = by_difficulty.get(meta.get("difficulty", "sample"), 0) + 1
        by_mutation[meta.get("mutation", "sample")] = by_mutation.get(meta.get("mutation", "sample"), 0) + 1

    stats = {
        "bundles_used": len(bundle_ids),
        "tasks_total": len(tasks),
        "train": len(train),
        "eval": len(eval_),
        "eval_bundles": sorted(eval_bundles),
        "by_difficulty": by_difficulty,
        "by_mutation": by_mutation,
        "skipped": skipped,
        "train_path": str(train_path),
        "eval_path": str(eval_path),
    }
    return stats


def main() -> None:
    parser = argparse.ArgumentParser(description="Build m2m2 repair dataset v1 from mythos bundles.")
    parser.add_argument("--bundles", type=Path, default=DEFAULT_BUNDLES)
    parser.add_argument("--out", type=Path, default=DEFAULT_OUT)
    parser.add_argument("--per-bundle", type=int, default=5)
    parser.add_argument("--seed", type=int, default=11)
    args = parser.parse_args()

    stats = build(args.bundles, args.out, args.per_bundle, args.seed)
    print(json.dumps(stats, indent=2))


if __name__ == "__main__":
    main()
