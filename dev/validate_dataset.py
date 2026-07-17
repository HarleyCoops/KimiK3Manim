"""Validate dataset v1 end-to-end against the restored environment.

Checks:
  1. load_environment() works under verifiers 0.2.0 with the new train/eval files
  2. every task's mutated code re-scores to its recorded start_score
  3. mutated scenes still ast.parse (except intentional syntax_break)
  4. the question payload carries prompt + broken code + evidence
"""

from __future__ import annotations

import ast
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "environments" / "math_to_manim"))

from m2m2_visual_repair import load_environment  # noqa: E402
from m2m2_visual_repair.scoring import score_completion  # noqa: E402

DATA = ROOT / "environments" / "math_to_manim" / "m2m2_visual_repair" / "data"


def wrap(scene_name: str, code: str) -> str:
    payload = json.dumps({"scene_name": scene_name, "language": "python", "code": code})
    return f"<generated_code>{payload}</generated_code>"


def main() -> None:
    env = load_environment(max_examples=-1, eval_fraction=0.0)
    rows = [json.loads(line) for line in (DATA / "repair_tasks.jsonl").read_text(encoding="utf-8").splitlines() if line.strip()]
    eval_rows = [json.loads(line) for line in (DATA / "repair_tasks_eval.jsonl").read_text(encoding="utf-8").splitlines() if line.strip()]
    print(f"env train examples: {len(env.dataset)} | eval file rows: {len(eval_rows)}")

    failures = []
    parse_skips = 0
    for row in rows + eval_rows:
        task_id = row["task_id"]
        code = row["generated_code"]["code"]
        mutation = row["metadata"].get("mutation", "sample")
        result = score_completion(row, wrap(row["scene_name"], code))
        recorded = row["metadata"].get("start_score")
        if recorded is not None and abs(result.score - recorded) > 0.02:
            failures.append(f"{task_id}: rescored {result.score} != recorded {recorded}")
        if mutation != "syntax_break":
            try:
                ast.parse(code)
            except SyntaxError as exc:
                failures.append(f"{task_id}: mutated code does not parse: {exc}")
        else:
            parse_skips += 1

    sample = rows[0]
    question = None
    for i in range(len(env.dataset)):
        if env.dataset[i]["info"]["task_id"] == sample["task_id"]:
            question = env.dataset[i]["question"]
            break
    assert question and sample["prompt"][:60] in question, "question payload missing prompt"
    assert "current_generated_code" in question, "question payload missing broken code"
    assert "evidence" in question, "question payload missing evidence"

    print(f"rescored {len(rows) + len(eval_rows)} tasks | syntax_break rows skipped for parse: {parse_skips}")
    if failures:
        print("FAILURES:")
        for failure in failures:
            print(" -", failure)
        sys.exit(1)
    print("ALL CHECKS PASSED")


if __name__ == "__main__":
    main()
