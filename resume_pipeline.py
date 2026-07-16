"""Resume the K3 pipeline at Stage 5 from saved artifacts 01-04.

Stages 1-4 completed and were persisted to the run directory; the original
run died because the default code model (kimi-k2.7-code) was discontinued.
This script reuses Supervisor's render/critic machinery without re-paying
for stages 1-4.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from k3_agents.supervisor import Supervisor
from k3_agents.manim_coder import ManimCoder
from k3_agents.render_critic import RenderCritic
from schemas import (
    KnowledgeGraph,
    MathEnrichment,
    Narrative,
    VisualSpec,
)

RUN_DIR = Path(
    "output/k3_runs/animate-an-epic--rigorous-derivation-of-the-euler-identity-e"
)


def load(name, cls):
    return cls.model_validate_json((RUN_DIR / name).read_text(encoding="utf-8"))


def say(msg: str) -> None:
    print(f"[supervisor] {msg}", flush=True)


def main() -> None:
    graph = load("01_knowledge_graph.json", KnowledgeGraph)
    math = load("02_math_enrichment.json", MathEnrichment)
    visual = load("03_visual_spec.json", VisualSpec)
    narrative = load("04_narrative.json", Narrative)
    say(f"Resumed artifacts: graph={len(graph.nodes)} nodes, "
        f"math={len(math.nodes) if hasattr(math, 'nodes') else 'ok'}")

    sup = Supervisor()

    say("Stage 5/6 Manim Coder (resume)")
    coder = ManimCoder()
    bundle = coder.write_scenes(narrative, visual)
    sup._save(RUN_DIR, "05_scene_bundle", bundle)

    critic = RenderCritic()
    critique = None
    video = None
    rounds = 0
    while rounds <= sup.max_repair_rounds:
        sup._write_bundle(RUN_DIR, bundle)
        say(f"Render attempt {rounds + 1}")
        ok, log, video = sup._render(RUN_DIR, bundle)
        if not ok:
            say("Render failed; sending traceback to coder")
            (RUN_DIR / f"render_log_round{rounds}.txt").write_text(
                log, encoding="utf-8"
            )
            rounds += 1
            bundle = coder.fix_scenes(bundle, log)
            sup._save(RUN_DIR, f"05_scene_bundle_fix{rounds}", bundle)
            continue

        say("Stage 6/6 Render Critic")
        frames = sup._sample_frames(RUN_DIR, video)
        critique = critic.critique(visual, frames)
        sup._save(RUN_DIR, f"06_critique_round{rounds}", critique)
        if critique.passed:
            say(f"Critic passed (score {critique.score})")
            break
        rounds += 1
        if rounds > sup.max_repair_rounds:
            say("Budget exhausted; shipping best effort")
            break
        say(f"Critic score {critique.score}; issues -> coder")
        bundle = coder.fix_scenes(bundle, "\n".join(critique.issues))
        sup._save(RUN_DIR, f"05_scene_bundle_fix{rounds}", bundle)

    print(f"VIDEO: {video}")
    if critique:
        print(f"CRITIQUE: score={critique.score} passed={critique.passed}")


if __name__ == "__main__":
    main()
