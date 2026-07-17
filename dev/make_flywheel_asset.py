"""Render the K3 x Prime RL self-improvement flywheel as a README asset.

Outputs assets/k3_rl_flywheel.png (dark house-style card, 2000x2000).
Mirrors the Blueprint widget geometry: six nodes on a clockwise loop,
K3 swarm teacher feed in, verified scenes out to epic films.
"""

from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import FancyBboxPatch, Polygon

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "assets" / "k3_rl_flywheel.png"

# --- palette (K3 house style) ---
BG = "#0A0E1A"
PANEL = "#141A2E"
EDGE = "#3A4666"
TEXT = "#E8ECF5"
SUB = "#9AA6C4"
DIM = "#5E6C8F"
ARC = "#8B9BC0"
ACCENT = "#4C8DFF"
TEAL = "#39D0C4"

CX, CY, R = 50.0, 47.0, 27.0
GAP = 22.0

NODES = [
    ("Student", "Qwen3 4B → 30B", 0, True),
    ("Render gate", "sandbox · manim -ql", 60, False),
    ("K3 critic", "frames vs spec", 120, False),
    ("Harvester", "failures → tasks", 180, False),
    ("Dataset", "HF difficulty pools", 240, False),
    ("GRPO", "prime-rl · DPPO+KL", 300, False),
]
LINKS = ["code", "frames+stderr", "score", "broken pairs", "batches", "Δweights"]

SWARM = (13.0, 53.0, "K3 swarm", "teacher + judge")
FILMS = (88.0, 45.0, "Epic films", "epic3d kit")


def pos(a, r=R):
    """Angle a: 0=top, increasing clockwise (y-up data coords)."""
    a = np.deg2rad(a)
    return CX + r * np.sin(a), CY + r * np.cos(a)


def main():
    rng = np.random.default_rng(11)
    fig = plt.figure(figsize=(10, 10), dpi=200, facecolor=BG)
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    ax.axis("off")
    ax.set_facecolor(BG)

    # star field
    n = 170
    xs = rng.uniform(1, 99, n)
    ys = rng.uniform(1, 99, n)
    ss = rng.uniform(0.4, 2.6, n)
    al = rng.uniform(0.10, 0.45, n)
    ax.scatter(xs, ys, s=ss, c="#AFC3FF", alpha=al, linewidths=0)

    # soft glows
    for gx, gy, gr, gc, ga in [(50, 47, 40, ACCENT, 0.05), (50, 47, 26, TEAL, 0.04)]:
        glow = plt.Circle((gx, gy), gr, color=gc, alpha=ga, lw=0)
        ax.add_patch(glow)

    # loop arcs with arrowheads
    angles = [n[2] for n in NODES]
    for i, a_start in enumerate(angles):
        a_end = angles[(i + 1) % 6] + (360 if i == 5 else 0)
        t0, t1 = a_start + GAP, a_end - GAP
        accent = i == 5
        tt = np.linspace(t0, t1, 120)
        pts = np.array([pos(t) for t in tt])
        color = ACCENT if accent else ARC
        if accent:
            ax.plot(pts[:, 0], pts[:, 1], color=color, lw=5.5, alpha=0.22, solid_capstyle="round", zorder=2)
        ax.plot(pts[:, 0], pts[:, 1], color=color, lw=2.0 if accent else 1.3,
                alpha=0.95 if accent else 0.75, dashes=(1, 0) if accent else (4, 3),
                solid_capstyle="round", zorder=3)
        # arrowhead at end, tangent = (cos a, -sin a) for clockwise motion
        a1 = np.deg2rad(t1)
        tx, ty = np.cos(a1), -np.sin(a1)
        px, py = pos(t1)
        bx, by = px - tx * 3.0, py - ty * 3.0
        nx, ny = -ty, tx
        tri = Polygon([(px, py), (bx + nx * 1.6, by + ny * 1.6), (bx - nx * 1.6, by - ny * 1.6)],
                      closed=True, facecolor=color, edgecolor="none", alpha=0.95, zorder=4)
        ax.add_patch(tri)
        # link label inside the loop
        lx, ly = pos((t0 + t1) / 2, 20.5)
        ax.text(lx, ly, LINKS[i], ha="center", va="center", fontsize=7.6,
                family="DejaVu Sans Mono", color=ACCENT if accent else DIM, zorder=5)

    # center label
    ax.text(CX, CY + 1.8, "RENDER =", ha="center", va="center", fontsize=8.6,
            family="DejaVu Sans Mono", color=SUB, zorder=5)
    ax.text(CX, CY - 2.2, "TRAINING DATA", ha="center", va="center", fontsize=8.6,
            family="DejaVu Sans Mono", color=SUB, zorder=5)

    # external feeds
    def ext_arrow(p0, p1, label, lpos, lrot=0):
        ax.annotate("", xy=p1, xytext=p0,
                    arrowprops=dict(arrowstyle="-|>", color=DIM, lw=1.1,
                                    linestyle=(0, (3, 3)), mutation_scale=11),
                    zorder=3)
        ax.text(lpos[0], lpos[1], label, ha="center", va="center", fontsize=7.2,
                family="DejaVu Sans Mono", color=DIM, rotation=lrot, zorder=5)

    ext_arrow((20.0, 57.5), (42.0, 70.5), "SFT/OPD traces", (27.0, 67.5), lrot=32)
    ext_arrow((80.0, 56.0), (85.0, 49.5), "verified\nscenes", (89.0, 53.5))

    # node chips
    def chip(x, y, title, sub, accent=False, dashed=False, w=19.5):
        h = 8.2
        if accent:
            glow = FancyBboxPatch((x - w / 2 - 0.9, y - h / 2 - 0.9), w + 1.8, h + 1.8,
                                  boxstyle="round,pad=0,rounding_size=2.2",
                                  facecolor=ACCENT, edgecolor="none", alpha=0.20, zorder=5)
            ax.add_patch(glow)
        box = FancyBboxPatch((x - w / 2, y - h / 2), w, h,
                             boxstyle="round,pad=0,rounding_size=1.8",
                             facecolor=PANEL if not dashed else "none",
                             edgecolor=ACCENT if accent else (DIM if dashed else EDGE),
                             lw=1.6 if accent else 1.1,
                             linestyle=(0, (3, 2)) if dashed else "solid", zorder=6)
        ax.add_patch(box)
        ax.text(x, y + 1.5, title, ha="center", va="center", fontsize=10.5,
                weight="bold", color=TEXT, zorder=7)
        ax.text(x, y - 2.1, sub, ha="center", va="center", fontsize=6.8,
                family="DejaVu Sans Mono", color=SUB, zorder=7)

    for name, sub, ang, accent in NODES:
        x, y = pos(ang)
        chip(x, y, name, sub, accent=accent)
    chip(*SWARM[:2], SWARM[2], SWARM[3], dashed=True, w=18.0)
    chip(*FILMS[:2], FILMS[2], FILMS[3], dashed=True, w=18.0)

    # header / footer
    ax.text(50, 95.5, "THE SELF-IMPROVEMENT FLYWHEEL", ha="center", va="center",
            fontsize=15.5, weight="bold", color=TEXT)
    ax.text(50, 91.8, "K3 epic visualizer × Prime Intellect RL — every render becomes training data",
            ha="center", va="center", fontsize=8.8, color=SUB)
    ax.text(50, 6.4, "KimiK2Manim · k3_agents swarm + render critic     |     Math-To-Manim · m2m2 repair env v0.1.13     |     Prime Intellect · sandboxes + prime-rl GRPO",
            ha="center", va="center", fontsize=7.0, family="DejaVu Sans Mono", color=DIM)

    OUT.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(OUT, facecolor=BG)
    plt.close(fig)
    print(f"wrote {OUT} ({OUT.stat().st_size} bytes)")


if __name__ == "__main__":
    main()
