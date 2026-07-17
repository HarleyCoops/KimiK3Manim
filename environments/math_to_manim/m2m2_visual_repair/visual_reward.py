"""Visual-quality heuristics for rendered Manim videos (no model judge).

Deliberately hack-resistant proxies computed from decoded frames:

    non_black_ratio - fraction of non-near-black pixels across samples
                      (kills empty/black-scene reward hacks)
    motion          - mean absolute difference between consecutive samples
                      (kills static single-frame videos)
    color           - channel-variance colorfulness proxy
    duration        - clip length vs a minimum sensible duration

A VLM judge can replace this module later (blueprint Phase 2 v2); these
heuristics stay as the always-on, un-gameable-by-charm floor.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import numpy as np

MAX_DECODE_FRAMES = 900
BLACK_THRESHOLD = 12
MIN_DURATION_S = 2.0


@dataclass(frozen=True)
class VisualMetrics:
    non_black_ratio: float = 0.0
    motion: float = 0.0
    color: float = 0.0
    duration_s: float = 0.0
    width: int = 0
    height: int = 0
    frames_sampled: int = 0
    extra: dict[str, Any] = field(default_factory=dict)

    @property
    def duration_score(self) -> float:
        return min(1.0, self.duration_s / 5.0) if self.duration_s >= MIN_DURATION_S else 0.0


def visual_quality(mp4_path: str | Path, sample_count: int = 6) -> tuple[float, VisualMetrics]:
    """Score a rendered mp4 in [0, 1]. Returns (0.0, empty metrics) on failure."""

    mp4_path = Path(mp4_path)
    if not mp4_path.exists() or mp4_path.stat().st_size < 1024:
        return 0.0, VisualMetrics()
    try:
        import av
    except ImportError:
        return 0.0, VisualMetrics(extra={"error": "PyAV not installed"})

    try:
        container = av.open(str(mp4_path))
        stream = container.streams.video[0]
        duration_s = float(container.duration / 1_000_000) if container.duration else 0.0
        width, height = stream.width, stream.height
        frames = []
        for index, frame in enumerate(container.decode(stream)):
            if index >= MAX_DECODE_FRAMES:
                break
            frames.append(frame.to_ndarray(format="rgb24"))
        container.close()
    except Exception:
        return 0.0, VisualMetrics()

    if not frames:
        return 0.0, VisualMetrics(duration_s=duration_s, width=width, height=height)

    step = max(1, len(frames) // sample_count)
    samples = [np.asarray(frames[i], dtype=np.float32) for i in range(0, len(frames), step)][:sample_count]

    non_black = float(np.mean([np.mean(sample.max(axis=2) > BLACK_THRESHOLD) for sample in samples]))
    if len(samples) > 1:
        diffs = [
            float(np.mean(np.abs(samples[i + 1] - samples[i])) / 255.0)
            for i in range(len(samples) - 1)
        ]
        motion = float(np.clip(np.mean(diffs) * 6.0, 0.0, 1.0))
    else:
        motion = 0.0
    rg = samples[-1][:, :, 0].astype(np.float32) - samples[-1][:, :, 1].astype(np.float32)
    yb = 0.5 * (samples[-1][:, :, 0] + samples[-1][:, :, 1]) - samples[-1][:, :, 2]
    color = float(np.clip((rg.std() + yb.std()) / 60.0, 0.0, 1.0))

    metrics = VisualMetrics(
        non_black_ratio=round(non_black, 4),
        motion=round(motion, 4),
        color=round(color, 4),
        duration_s=round(duration_s, 2),
        width=width,
        height=height,
        frames_sampled=len(samples),
    )
    score = (
        0.35 * metrics.non_black_ratio
        + 0.35 * metrics.motion
        + 0.15 * metrics.color
        + 0.15 * metrics.duration_score
    )
    return round(float(np.clip(score, 0.0, 1.0)), 6), metrics
