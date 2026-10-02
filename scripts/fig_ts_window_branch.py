#!/usr/bin/env python3
"""fig_ts_window_branch.py — 「时间切片＝交互窗口」分支树版（B）。

主人 1001 命题：token 大模型的概念空间线性组合 ＝ 真实世界切片的一个简化版本；
共通点＝**time-slice 就是智能体与世界（语言模型）交互的窗口**；经交互，**界（语言模型）获得信息，分支到新路径**。
复现之骨取 iPS 图（分支，不是回路）——但拉成**连锁**：每个切片一个窗口，交互把可选性抬回「界」，再长新枝（枝带上下文）。

输出: docs/figs/ts-window-branch-{dark,light}.{svg,png}
"""
import os
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, FancyArrowPatch

matplotlib.rcParams["font.family"] = ["Hiragino Sans GB", "Arial Unicode MS", "sans-serif"]
matplotlib.rcParams["axes.unicode_minus"] = False
OUT = os.path.join(os.path.dirname(__file__), "..", "docs", "figs")

TH = {
    "dark":  dict(bg="#0b0d10", ink="#e4dfd2", dim="#7f7c74", faint="#3a3d45",
                  gold="#c9a959", goldd="#e3c879", red="#c0705c"),
    "light": dict(bg="#ffffff", ink="#1a1a1a", dim="#6b6b6b", faint="#c9c3b2",
                  gold="#b8860b", goldd="#8a6f2e", red="#a0522d"),
}

W, H = 1340, 880
X0, X1 = 96, 1230
Y0, Y1 = 130, 690
BNY, BRY = 0.68, 0.585          # 界水位 / 新枝高度
WINDOWS = [0.255, 0.515, 0.775]
LN = ["①", "②", "③"]
TLBL = ["$T_{n-k}$", "$T_0$", "$T_1$"]


def xp(t):
    return X0 + (X1 - X0) * t


def yp(v):
    return Y0 + (Y1 - Y0) * v


def trunk_y(t):
    return 0.20 - 0.10 * t


def main(theme):
    th = TH[theme]
    fig = plt.figure(figsize=(13.4, 8.8), dpi=200)
    fig.patch.set_facecolor(th["bg"])
    ax = fig.add_axes([0.03, 0.03, 0.94, 0.94])
    ax.set_xlim(0, W); ax.set_ylim(0, H); ax.axis("off")
    ax.set_facecolor(th["bg"])

    # 窗口带
    for t, ln, tl in zip(WINDOWS, LN, TLBL):
        x = xp(t)
        ax.add_patch(Rectangle((x - 26, Y0 - 46), 52, (Y1 - Y0) + 96,
                               facecolor=th["gold"], alpha=0.08, edgecolor=th["gold"],
                               lw=1.2, ls=(0, (5, 5)), zorder=0))
        ax.text(x, Y1 + 62, f"窗口{ln} · {tl}", color=th["gold"], fontsize=12.5,
                ha="center", va="bottom")

    # 界（语言模型 · 可选性水位）
    yb = yp(BNY)
    ax.plot([X0 - 10, X1 + 10], [yb, yb], color=th["gold"], lw=1.4, ls=(0, (7, 5)),
            alpha=0.9, zorder=1)
    ax.text(X1 + 6, yb + 12, ll(theme, "boundary"), color=th["goldd"], fontsize=11,
            ha="right", va="bottom")

    # 未交互原路
    ts = np.linspace(0, 1, 200)
    ax.plot([xp(t) for t in ts], [yp(trunk_y(t)) for t in ts], color=th["faint"], lw=1.6, zorder=2)
    ax.text(xp(0.30), yp(trunk_y(0.30)) - 16, ll(theme, "trunk"), color=th["dim"],
            fontsize=10.5, ha="center", va="top")

    # 起点
    x0, y0 = xp(0.02), yp(trunk_y(0.02))
    ax.plot([x0], [y0], "o", ms=11, mfc=th["gold"], mec=th["goldd"], zorder=6)
    ax.text(x0 + 8, y0 + 30, ll(theme, "origin"), color=th["ink"], fontsize=12,
            ha="left", va="bottom")

    # 连锁：交互弧 + 新枝
    h = trunk_y(0.02)
    for i, t in enumerate(WINDOWS):
        px, py = xp(t), yp(h)
        ax.plot([px], [py], "o", ms=9, mfc=th["bg"], mec=th["red"], mew=2.2, zorder=6)
        arc_x = xp(t + 0.048)
        ax.add_patch(FancyArrowPatch((px + 2, py + 6), (arc_x - 6, yb - 5),
                     connectionstyle="arc3,rad=-0.28", arrowstyle="-|>",
                     mutation_scale=16, color=th["red"], lw=2.0, ls=(0, (5, 3)), zorder=4))
        ax.text(px - 40, py + 22, ll(theme, "interact"),
                color=th["red"], fontsize=10, ha="right", va="bottom")
        t_end = WINDOWS[i + 1] if i + 1 < len(WINDOWS) else 1.0
        bx = np.linspace(t + 0.048, t_end, 90)
        by = [BNY + (BRY - BNY) * ((xB - (t + 0.048)) / (t_end - (t + 0.048))) for xB in bx]
        ax.plot([xp(xB) for xB in bx], [yp(v) for v in by], color=th["gold"], lw=2.8,
                solid_capstyle="round", zorder=5)
        # 枝名（枝中下方）
        mx = xp((t + 0.048 + t_end) / 2)
        ax.text(mx, yp(BRY) - 20, ll(theme, "branch") + LN[i], color=th["goldd"],
                fontsize=10.5, ha="center", va="top")
        h = BRY

    # 末端 → 新路径
    ex, ey = xp(1.0), yp(BRY)
    ax.add_patch(FancyArrowPatch((ex - 6, ey), (ex + 30, ey), arrowstyle="-|>",
                                 mutation_scale=18, color=th["gold"], lw=2.6, zorder=5))
    ax.text(ex + 38, ey, ll(theme, "end"), color=th["goldd"], fontsize=11,
            ha="left", va="center")

    # 残留注
    ax.text(xp(0.40), yp(BRY) - 52, ll(theme, "resid"), color=th["dim"], fontsize=10,
            ha="center", va="top", style="italic")

    # 时间轴
    ay = Y0 - 66
    ax.add_patch(FancyArrowPatch((X0, ay), (X1 + 30, ay), arrowstyle="-|>",
                                 mutation_scale=18, color=th["dim"], lw=1.6))
    ax.text((X0 + X1) / 2, ay - 24, ll(theme, "axis"), color=th["dim"], fontsize=12,
            ha="center", va="top", style="italic")

    # 标题
    fig.text(0.045, 0.972, ll(theme, "title"), color=th["gold"], fontsize=21.5,
             fontweight="bold", va="top")
    fig.text(0.045, 0.935, ll(theme, "sub"), color=th["dim"], fontsize=11.5, va="top")
    fig.text(0.045, 0.026, ll(theme, "foot"), color=th["dim"], fontsize=10.5, va="top")

    tag = "dark" if theme == "dark" else "light"
    for ext in ("svg", "png"):
        fig.savefig(os.path.join(OUT, f"ts-window-branch-{tag}.{ext}"), facecolor=th["bg"])
    plt.close(fig)
    print(f"✔ ts-window-branch-{tag}.{{svg,png}}")


def ll(theme, k):
    zh = {
        "boundary": "界 · 语言模型（可选性水位）",
        "trunk": "未交互的原路（渐退场）",
        "origin": "起点 · 先验（未交互）",
        "interact": "交互",
        "branch": "新分支",
        "end": "→ 新路径",
        "resid": "枝带上下文（残留）",
        "axis": "时间  →",
        "title": "时间切片 ＝ 智能体 ↔ 世界的交互窗口（交互 → 分支）",
        "sub": "取 iPS 之骨：分支，不是回路。每个切片一个窗口；交互把可选性抬回「界」，再长出新枝，枝带上下文。",
        "foot": "token 大模型的概念空间线性组合 ＝ 真实世界切片的一个简化版本：同一根窗口、同一种分支。",
    }
    en = {
        "boundary": "the boundary · LM (optionality level)",
        "trunk": "uninteracted path (fading)", "origin": "start · prior (before interaction)",
        "interact": "interaction", "branch": "new branch", "end": "→ new path",
        "resid": "branch carries context (residue)", "axis": "time  →",
        "title": "A time-slice is the window where agent ↔ world interact",
        "sub": "The iPS backbone: a branch, not a loop. Each slice is a window; interaction lifts optionality back to the boundary, then a new branch grows, carrying context.",
        "foot": "An LLM's linear combination of concept spaces is a simplified world-slice: the same window, the same branch.",
    }
    return (en if theme.startswith("en-") else zh)[k]


if __name__ == "__main__":
    main("dark")
    main("light")
