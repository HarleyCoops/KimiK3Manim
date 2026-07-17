"""Render-verified reward gate for Math-To-Manim repair tasks.

Executes the candidate Manim scene at draft quality and reports whether it
renders. Two backends:

    local_subprocess - runs ``python -m manim -q{quality}`` on the host
                       (dev/single-GPU workflows; Windows-safe)
    prime_sandbox    - Prime Intellect managed sandbox with a pre-baked
                       manim+PyAV+LaTeX image (training at scale)

Infra failures (manim missing, sandbox errors) are reported as
``infra_error`` so callers can mask instead of zero-scoring — the i3-code
pattern: never let infrastructure noise become reward noise.
"""

from __future__ import annotations

import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import time
from dataclasses import dataclass, field
from typing import Any


RENDER_STATUSES = {"rendered", "failed", "timeout", "infra_error"}


@dataclass(frozen=True)
class RenderResult:
    status: str
    scene_name: str
    mp4_path: str | None = None
    mp4_bytes: int = 0
    duration_s: float = 0.0
    stderr_tail: str = ""
    backend: str = "local_subprocess"
    wall_s: float = 0.0
    extra: dict[str, Any] = field(default_factory=dict)

    @property
    def rendered(self) -> bool:
        return self.status == "rendered" and self.mp4_bytes >= 1024

    @property
    def infra_error(self) -> bool:
        return self.status == "infra_error"


def resolve_manim_command() -> list[str] | None:
    """Prefer ``python -m manim`` from the current interpreter, else PATH."""

    try:
        probe = subprocess.run(
            [sys.executable, "-m", "manim", "--version"],
            capture_output=True,
            timeout=30,
        )
        if probe.returncode == 0:
            return [sys.executable, "-m", "manim"]
    except (OSError, subprocess.TimeoutExpired):
        pass
    if shutil.which("manim"):
        return ["manim"]
    return None


def render_scene(
    scene_name: str,
    code: str,
    quality: str = "ql",
    timeout_s: int = 120,
    backend: str = "local_subprocess",
    work_dir: str | Path | None = None,
    keep_artifacts: bool = False,
) -> RenderResult:
    """Render one candidate scene. Never raises; failures become statuses."""

    if backend == "prime_sandbox":
        return _render_prime_sandbox(scene_name, code, quality, timeout_s)
    if backend != "local_subprocess":
        raise ValueError(f"unknown render backend: {backend}")
    return _render_local(scene_name, code, quality, timeout_s, work_dir, keep_artifacts)


def _render_local(
    scene_name: str,
    code: str,
    quality: str,
    timeout_s: int,
    work_dir: str | Path | None,
    keep_artifacts: bool,
) -> RenderResult:
    command = resolve_manim_command()
    started = time.monotonic()
    if command is None:
        return RenderResult(
            status="infra_error",
            scene_name=scene_name,
            stderr_tail="manim not found (python -m manim and PATH both failed)",
        )

    tmp = Path(work_dir) if work_dir else Path(tempfile.mkdtemp(prefix="m2m2_render_"))
    tmp.mkdir(parents=True, exist_ok=True)
    media_dir = tmp / "media"
    scene_file = tmp / "candidate_scene.py"
    scene_file.write_text(code, encoding="utf-8")

    try:
        proc = subprocess.run(
            command + [f"-q{quality.lstrip('q')}", "--media_dir", str(media_dir), str(scene_file), scene_name],
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=timeout_s,
            cwd=str(tmp),
        )
    except subprocess.TimeoutExpired:
        return RenderResult(
            status="timeout",
            scene_name=scene_name,
            stderr_tail=f"render exceeded {timeout_s}s",
            wall_s=time.monotonic() - started,
        )
    except OSError as exc:
        return RenderResult(
            status="infra_error",
            scene_name=scene_name,
            stderr_tail=f"render subprocess failed: {exc}",
            wall_s=time.monotonic() - started,
        )

    wall_s = time.monotonic() - started
    mp4s = sorted(media_dir.rglob("*.mp4"), key=lambda p: p.stat().st_mtime) if media_dir.exists() else []
    stderr_tail = (proc.stderr or "")[-800:]
    if proc.returncode == 0 and mp4s:
        mp4 = mp4s[-1]
        size = mp4.stat().st_size
        result = RenderResult(
            status="rendered" if size >= 1024 else "failed",
            scene_name=scene_name,
            mp4_path=str(mp4),
            mp4_bytes=size,
            stderr_tail=stderr_tail,
            wall_s=wall_s,
        )
    else:
        result = RenderResult(
            status="failed",
            scene_name=scene_name,
            stderr_tail=stderr_tail or f"manim exited {proc.returncode} with no mp4",
            wall_s=wall_s,
        )
    if not keep_artifacts and not work_dir:
        if result.mp4_path:
            keep = Path(tempfile.mkdtemp(prefix="m2m2_mp4_")) / Path(result.mp4_path).name
            try:
                shutil.copy2(result.mp4_path, keep)
                result = RenderResult(**{**result.__dict__, "mp4_path": str(keep)})
            except OSError:
                pass
        shutil.rmtree(tmp, ignore_errors=True)
    return result


def _render_prime_sandbox(scene_name: str, code: str, quality: str, timeout_s: int) -> RenderResult:
    """Render inside a Prime Intellect sandbox (pre-baked manim image).

    Requires the ``prime-sandboxes`` SDK and a Prime API key in the
    environment. Kept deliberately thin: the sandbox runs the same command
    as the local backend and returns the same RenderResult shape.
    """

    try:
        from prime_sandboxes import SandboxClient  # type: ignore
    except ImportError:
        return RenderResult(
            status="infra_error",
            scene_name=scene_name,
            backend="prime_sandbox",
            stderr_tail="prime-sandboxes SDK not installed",
        )
    image = os.environ.get("M2M2_SANDBOX_IMAGE", "manim-renderer:latest")
    try:
        client = SandboxClient()
        with client.create(image=image, cpu_cores=2, memory_gb=4, timeout_s=timeout_s + 60) as sandbox:
            sandbox.write_file("/workspace/candidate_scene.py", code)
            proc = sandbox.run(
                f"python -m manim -q{quality.lstrip('q')} --media_dir /workspace/media "
                f"/workspace/candidate_scene.py {scene_name}",
                timeout_s=timeout_s,
            )
            find = sandbox.run("find /workspace/media -name '*.mp4' | head -1", timeout_s=15)
            mp4_remote = (find.stdout or "").strip()
            payload: dict[str, Any] = {"proc_returncode": getattr(proc, "returncode", None)}
            if mp4_remote:
                data = sandbox.read_bytes(mp4_remote)
                local = Path(tempfile.mkdtemp(prefix="m2m2_mp4_")) / f"{scene_name}.mp4"
                local.write_bytes(data)
                return RenderResult(
                    status="rendered" if len(data) >= 1024 else "failed",
                    scene_name=scene_name,
                    mp4_path=str(local),
                    mp4_bytes=len(data),
                    stderr_tail=(getattr(proc, "stderr", "") or "")[-800:],
                    backend="prime_sandbox",
                    extra=payload,
                )
            return RenderResult(
                status="failed",
                scene_name=scene_name,
                stderr_tail=(getattr(proc, "stderr", "") or "")[-800:],
                backend="prime_sandbox",
                extra=payload,
            )
    except Exception as exc:  # sandbox API/infra failure -> mask, never score
        return RenderResult(
            status="infra_error",
            scene_name=scene_name,
            backend="prime_sandbox",
            stderr_tail=f"prime sandbox error: {exc}",
        )


def result_to_json(result: RenderResult) -> str:
    return json.dumps({**result.__dict__, "rendered": result.rendered, "infra_error": result.infra_error})
