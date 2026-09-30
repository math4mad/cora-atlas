#!/usr/bin/env python3
"""fig_time_slice_paper.py — 论文用「多线切片」插图 (浅底·英文·矢量).
输出: papers/expansive-interaction/figs/time-slice-en.pdf / .png
"""
import math, os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch

GOLD, INK, DIM, RED, GREEN = "#b8860b", "#1a1a1a", "#6b6b6b", "#a0522d", "#4f6f4a"
COLORS = [GOLD, INK, GREEN, DIM, RED, INK]
GEO = [
    (3.2, 0.46, 1.7, 0.0, 0.16, 4.3, 1.1),
    (3.9, 0.34, 2.1, 0.9, 0.12, 5.1, 0.3),
    (4.6, 0.52, 1.4, 1.8, 0.14, 3.7, 2.2),
    (5.3, 0.30, 2.5, 0.4, 0.10, 6.0, 1.5),
    (6.0, 0.44, 1.9, 2.6, 0.13, 4.7, 0.7),
    (6.7, 0.28, 2.3, 1.3, 0.09, 5.6, 2.9),
]
SLICE_X = [2.6, 6.4, 8.7]
SUBS = ["n-k", "0", "1"]

fig, ax = plt.subplots(figsize=(10.4, 5.9), dpi=200)
ax.set_xlim(0.6, 10.2); ax.set_ylim(0, 8.2); ax.axis("off")

xs = [0.6 + (10.2 - 0.6) * i / 300 for i in range(301)]
def ys(g, x):
    base, a1, f1, p1, a2, f2, p2 = g
    t = (x - 0.6) / (10.2 - 0.6)
    return base + a1 * math.sin(2 * math.pi * f1 * t + p1) + a2 * math.sin(2 * math.pi * f2 * t + p2)

for x, sub in zip(SLICE_X, SUBS):
    ax.add_patch(FancyBboxPatch((x - 0.20, 2.3), 0.40, 5.1, boxstyle="round,pad=0.02,rounding_size=0.15",
                                fc=GOLD, ec=GOLD, alpha=0.10, lw=1.4, ls=(0, (5, 4)), zorder=1))
    ax.text(x, 7.75, f"$T_{{{sub}}}$", color=GOLD, ha="center", va="bottom", fontsize=22, style="italic")
for g, col in zip(GEO, COLORS):
    ax.plot(xs, [ys(g, x) for x in xs], color=col, lw=1.8, solid_capstyle="round", zorder=3)
for x in SLICE_X:
    for g, col in zip(GEO, COLORS):
        ax.plot([x], [ys(g, x)], "o", ms=4.5, mfc="white", mec=col, mew=1.5, zorder=4)
ax.annotate("", xy=(10.1, 1.35), xytext=(0.6, 1.35),
            arrowprops=dict(arrowstyle="-|>", color=GOLD, lw=1.8))
ax.text(5.35, 0.75, "time", color=DIM, ha="center", fontsize=15, style="italic")
ax.text(0.6, 7.95, "The Multi-line Slice", color=GOLD, fontsize=19, style="italic")
ax.text(0.6, 7.55, "State = each curve's cross-section (slice) at $t$", color=DIM, fontsize=12)
ax.text(0.6, 0.25, r"$T_0$ is not a frozen point but a slice of many curves; $T_1$'s slice cannot determine $T_0$'s slice.",
        color=DIM, fontsize=10.5)

out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "papers", "expansive-interaction", "figs")
os.makedirs(out, exist_ok=True)
for ext in ("pdf", "png"):
    fig.savefig(os.path.join(out, f"time-slice-en.{ext}"), bbox_inches="tight", facecolor="white")
print("✔ papers/expansive-interaction/figs/time-slice-en.pdf / .png")
