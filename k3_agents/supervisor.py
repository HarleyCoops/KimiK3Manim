"""Deterministic supervisor: sequencing, validation, and the render loop.

The supervisor is intentionally NOT a model. It runs the six agents in
order, validates every artifact against its schema (Pydantic re-validation
on load), persists artifacts to a run directory, renders with real Manim,
and drives the coder/critic repair loop until the critic passes or the
budget is exhausted.
"""

from __future__ import annotations

import json
import subprocess
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import List, Optional

try:
    from ..schemas import (
        CritiqueReport,
        KnowledgeGraph,
        MathEnrichment,
        Narrative,
        SceneBundle,
        VisualSpec,
    )
except ImportError:
    from schemas import (
        CritiqueReport,
        KnowledgeGraph,
        MathEnrichment,
        Narrative,
        SceneBundle,
        VisualSpec,
    )

from .concept_scout import ConceptScout
from .math_enricher import MathEnricher
from .visual_designer import VisualDesigner
from .narrative_composer import NarrativeComposer
from .manim_coder import ManimCoder
from .render_critic import RenderCritic


@dataclass
class RunResult:
    run_dir: Path
    video_path: Optional[Path]
    critique: Optional[CritiqueReport]
    repair_rounds: int
    artifacts: dict = field(default_factory=dict)


class Supervisor:
    def __init__(
        self,
        output_root: Path = Path("output/k3_runs"),
        max_repair_rounds: int = 3,
        render_quality: str = "-qm",
    ):
        self.output_root = Path(output_root)
        self.max_repair_rounds = max_repair_rounds
        self.render_quality = render_quality

    # -- artifact persistence ------------------------------------------------

    def _save(self, run_dir: Path, name: str, artifact) -> None:
        (run_dir / f"{name}.json").write_text(
            artifact.model_dump_json(indent=2), encoding="utf-8"
        )

    # -- rendering -----------------------------------------------------------

    def _write_bundle(self, run_dir: Path, bundle: SceneBundle) -> None:
        for f in bundle.files:
            target = run_dir / "scenes" / f.path
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text(f.content, encoding="utf-8")

    # Failures caused by the environment, not the generated code. Sending
    # these to the coder wastes repair rounds on something it cannot fix.
    _ENV_FAILURES = (
        "No module named manim",
        "No module named 'manim'",
        "latex error converting to dvi",
        "latex: not found",
        "FileNotFoundError: [Errno 2] No such file or directory: 'latex'",
        "libpango",
    )

    def preflight(self) -> None:
        """Fail fast, with instructions, if the render environment is broken."""
        import importlib.util
        import shutil as _shutil

        problems = []
        if importlib.util.find_spec("manim") is None:
            problems.append(
                "manim is not installed in this environment. Run 'uv sync' "
                "(manim is now a project dependency) or 'uv pip install manim'."
            )
        if _shutil.which("ffmpeg") is None:
            problems.append("ffmpeg is not on PATH (sudo apt install ffmpeg).")
        if _shutil.which("latex") is None:
            problems.append(
                "latex is not on PATH; MathTex will fail "
                "(sudo apt install texlive texlive-latex-extra dvisvgm)."
            )
        if problems:
            raise RuntimeError(
                "Render environment is not ready:\n- " + "\n- ".join(problems)
            )

    def _render(
        self, run_dir: Path, bundle: SceneBundle, attempt: int
    ) -> tuple[bool, str, Optional[Path]]:
        """Render every scene file; returns (ok, combined_log, video_path)."""
        log_parts: List[str] = []
        video: Optional[Path] = None
        ok = True
        for f in bundle.files:
            cmd = [
                sys.executable, "-m", "manim", self.render_quality,
                str(run_dir / "scenes" / f.path), f.scene_class,
                "--media_dir", str(run_dir / "media"),
            ]
            proc = subprocess.run(
                cmd, capture_output=True, text=True, timeout=1800
            )
            log_parts.append(proc.stdout + proc.stderr)
            if proc.returncode != 0:
                ok = False
                break
        log = "\n".join(log_parts)
        # Always persist the log so failed runs are diagnosable after the fact
        (run_dir / f"render_attempt{attempt}.log").write_text(
            log, encoding="utf-8"
        )
        if not ok:
            for marker in self._ENV_FAILURES:
                if marker in log:
                    raise RuntimeError(
                        f"Render failed due to the ENVIRONMENT, not the "
                        f"generated code (matched: {marker!r}). Fix the "
                        f"environment and re-run; see "
                        f"{run_dir}/render_attempt{attempt}.log. Not sending "
                        f"to the coder - it cannot repair this."
                    )
            return False, log, None
        mp4s = sorted((run_dir / "media").rglob("*.mp4"), key=lambda p: p.stat().st_mtime)
        video = mp4s[-1] if mp4s else None
        return video is not None, log, video

    def _sample_frames(self, run_dir: Path, video: Path, count: int = 6) -> List[Path]:
        frames_dir = run_dir / "frames"
        frames_dir.mkdir(exist_ok=True)
        subprocess.run(
            [
                "ffmpeg", "-y", "-i", str(video),
                "-vf", f"thumbnail,select=not(mod(n\\,60))",
                "-frames:v", str(count), "-vsync", "vfr",
                str(frames_dir / "frame_%02d.png"),
            ],
            capture_output=True, timeout=300,
        )
        return sorted(frames_dir.glob("frame_*.png"))

    # -- the pipeline ----------------------------------------------------------

    def run(self, concept: str, verbose: bool = True) -> RunResult:
        slug = "".join(c if c.isalnum() else "-" for c in concept.lower())[:60]
        run_dir = self.output_root / slug
        run_dir.mkdir(parents=True, exist_ok=True)

        def say(msg: str) -> None:
            if verbose:
                print(f"[supervisor] {msg}")

        # Fail fast on a broken render environment BEFORE paying for any
        # model calls - a missing manim/latex cannot be fixed by the coder.
        self.preflight()

        say(f"Stage 1/6 Concept Scout: {concept}")
        graph: KnowledgeGraph = ConceptScout().explore(concept)
        graph.topological_order()  # validates acyclicity
        self._save(run_dir, "01_knowledge_graph", graph)

        say(f"Stage 2/6 Math Enricher ({len(graph.nodes)} nodes)")
        math: MathEnrichment = MathEnricher().enrich(graph)
        self._save(run_dir, "02_math_enrichment", math)

        say("Stage 3/6 Visual Designer")
        visual: VisualSpec = VisualDesigner().design(graph, math)
        self._save(run_dir, "03_visual_spec", visual)

        say("Stage 4/6 Narrative Composer")
        narrative: Narrative = NarrativeComposer().compose(graph, math, visual)
        self._save(run_dir, "04_narrative", narrative)

        say("Stage 5/6 Manim Coder")
        coder = ManimCoder()
        bundle: SceneBundle = coder.write_scenes(narrative, visual)
        self._save(run_dir, "05_scene_bundle", bundle)

        critic = RenderCritic()
        critique: Optional[CritiqueReport] = None
        video: Optional[Path] = None

        rounds = 0
        while rounds <= self.max_repair_rounds:
            self._write_bundle(run_dir, bundle)
            say(f"Render attempt {rounds + 1}")
            ok, log, video = self._render(run_dir, bundle, rounds + 1)
            if not ok:
                say("Render failed; sending traceback to coder")
                rounds += 1
                bundle = coder.fix_scenes(bundle, log)
                self._save(run_dir, f"05_scene_bundle_fix{rounds}", bundle)
                continue

            say("Stage 6/6 Render Critic")
            frames = self._sample_frames(run_dir, video)
            critique = critic.critique(visual, frames)
            self._save(run_dir, f"06_critique_round{rounds}", critique)
            if critique.passed:
                say(f"Critic passed (score {critique.score})")
                break
            rounds += 1
            if rounds > self.max_repair_rounds:
                say("Budget exhausted; shipping best effort")
                break
            say(f"Critic score {critique.score}; issues -> coder")
            bundle = coder.fix_scenes(bundle, "\n".join(critique.issues))
            self._save(run_dir, f"05_scene_bundle_fix{rounds}", bundle)

        return RunResult(
            run_dir=run_dir,
            video_path=video,
            critique=critique,
            repair_rounds=rounds,
            artifacts={
                "graph": graph, "math": math, "visual": visual,
                "narrative": narrative, "bundle": bundle,
            },
        )


def main() -> None:
    import argparse

    parser = argparse.ArgumentParser(description="Run the K3 animation pipeline")
    parser.add_argument("concept", help="Math/physics concept to animate")
    parser.add_argument("--max-repairs", type=int, default=3)
    parser.add_argument(
        "--quality",
        default="qm",
        choices=["ql", "qm", "qh", "qk"],
        help="Manim render quality: ql (480p), qm (720p), qh (1080p), qk (4K)",
    )
    args = parser.parse_args()

    result = Supervisor(
        max_repair_rounds=args.max_repairs, render_quality=f"-{args.quality}"
    ).run(args.concept)
    print(f"\nRun dir: {result.run_dir}")
    print(f"Video:   {result.video_path}")
    if result.critique:
        print(f"Critic:  passed={result.critique.passed} score={result.critique.score}")


if __name__ == "__main__":
    main()
