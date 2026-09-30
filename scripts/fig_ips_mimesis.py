#!/usr/bin/env python3
"""fig_ips_mimesis.py — 「iPS 拟态」图：受精卵→组织分化序列 ＋ iPS 作为 T_k 处的分支 (非回路)。
输出 docs/figs/ips-mimesis-dark.{svg,png} (+ light 供信)。
"""
import os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch

BG, INK, DIM, GOLD, GOLD_D, RED, GREEN = "#ffffff", "#1a1a1a", "#9a968c", "#c9a959", "#b8860b", "#b46a5a", "#7fa07a"

TISSUES = [(8.75, "neuron"), (7.55, "cardiomyocyte"), (6.35, "hepatocyte"),
           (3.45, "fibroblast"), (2.25, "blood"), (1.15, "skin")]
ZYG = (1.15, 5.15)
XEND = 12.0
TK_X = 8.2
IPS = (10.9, 5.15)


def curve(yt, x):
    t = max(0.0, min(1.0, (x - ZYG[0]) / (XEND - ZYG[0])))
    return ZYG[1] + (yt - ZYG[1]) * (t ** 1.25)


def box(**kw):
    return dict(boxstyle="round,pad=0.25", fc=BG, ec="none")


fig, ax = plt.subplots(figsize=(12.0, 6.4), dpi=200)
ax.set_xlim(0, 13.6); ax.set_ylim(-1.1, 10.2); ax.axis("off")
fig.patch.set_facecolor(BG); ax.set_facecolor(BG)

xs = [ZYG[0] + (XEND - ZYG[0]) * i / 220 for i in range(221)]
for yt, nm in TISSUES:
    hi = nm == "fibroblast"
    ax.plot(xs, [curve(yt, x) for x in xs], color=RED if hi else DIM, lw=2.7 if hi else 1.3,
            solid_capstyle="round", zorder=2)
    ax.text(XEND + 0.18, curve(yt, XEND), nm, color=RED if hi else DIM, fontsize=11, va="center")

# 多能性水平线
ax.plot([ZYG[0], 13.3], [ZYG[1], ZYG[1]], color=GOLD, lw=1.2, ls=(0, (6, 5)), alpha=0.85, zorder=1)

# 受精卵 / T0
ax.plot([ZYG[0]], [ZYG[1]], "o", ms=11, mfc=GOLD, mec=GOLD_D, zorder=5)
ax.text(ZYG[0] - 0.05, ZYG[1] + 0.5, "zygote · $T_0$", color=INK, fontsize=12.5, ha="left", va="bottom", bbox=box())

# T_k
yk = curve(3.45, TK_X)
ax.plot([TK_X], [yk], "o", ms=9, mfc="white", mec=RED, mew=2.2, zorder=6)
ax.text(TK_X, yk - 0.55, "somatic cell at $T_k$", color=RED, fontsize=11, ha="center", va="top", bbox=box())

# 重编程弧
ax.add_patch(FancyArrowPatch((TK_X + 0.1, yk + 0.15), (IPS[0] - 0.42, IPS[1] - 0.05),
             connectionstyle="arc3,rad=-0.32", arrowstyle="-|>", mutation_scale=22,
             color=RED, lw=2.2, ls=(0, (5, 3)), zorder=4))
ax.text(9.35, 6.55, "reprogramming · OSKM (2006)", color=RED, fontsize=11, ha="center", bbox=box(), zorder=7)

# iPS 集落 + 分支
ax.add_patch(FancyBboxPatch((IPS[0] - 0.5, IPS[1] - 0.4), 1.1, 0.8,
             boxstyle="round,pad=0.02,rounding_size=0.2", fc=GOLD, ec=GOLD_D, lw=1.6, alpha=0.28, zorder=5))
ax.plot([IPS[0]], [IPS[1]], "o", ms=11, mfc=GOLD, mec=GOLD_D, zorder=6)
ax.plot([IPS[0] + 0.55, 13.25], [IPS[1], IPS[1] - 0.05], color=GOLD, lw=2.6, zorder=5)
ax.text(IPS[0], IPS[1] + 0.62, "iPS colony", color=GOLD_D, fontsize=13, ha="center", va="bottom", weight="bold", bbox=box())
ax.text(12.35, 4.15, "a branch,\nnot a loop", color=GOLD_D, fontsize=11, ha="center", va="center", style="italic", bbox=box())

# 图例注: pluripotency
ax.text(13.32, ZYG[1] + 0.02, "  =  pluripotency level ($T_0$)", color=GOLD_D, fontsize=10, va="center", style="italic")

# 时间轴
ay = 0.7
ax.add_patch(FancyArrowPatch((ZYG[0], ay), (XEND + 1.1, ay), arrowstyle="-|>", mutation_scale=18, color=DIM, lw=1.6))
ax.text(6.5, ay + 0.28, "time  →", color=DIM, fontsize=11.5, ha="center", style="italic")

# 标题 + 脚注
ax.text(0.0, 9.8, "iPS mimesis: reprogramming is a branch, not a loop", color=INK, fontsize=17, style="italic")
ax.text(0.0, 9.35, "Differentiation runs forward from the zygote ($T_0$): the iPS colony is a branch that arises at a later point $T_k$ and mimics $T_0$.",
        color=DIM, fontsize=10.5)
ax.text(0.0, -0.85, "The iPS colony resembles $T_0$ but is downstream of $T_k$, carrying residual epigenetic memory (Daley & Hochedlinger 2010) — irreversibility is confirmed, not reversed.",
        color=DIM, fontsize=9.5, style="italic")

out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "docs", "figs")
os.makedirs(out, exist_ok=True)
for ext in ("svg", "png"):
    fig.savefig(os.path.join(out, f"ips-mimesis-dark.{ext}"), bbox_inches="tight", facecolor=BG)
plt.close(fig)
print("✔ docs/figs/ips-mimesis-dark.svg / .png")
