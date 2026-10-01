#!/usr/bin/env python3
"""fig_plastic_stool_topology.py — 依主人 1001 手稿 (Desktop/新备忘录.jpeg) 重绘。

手稿: 多个 slice (透视平面) 纵向叠放; 每片上有若干"拓扑"闭环; 同一拓扑以竖直波线
(worldline) 贯穿各片。主人令: **拓扑大小表示概率**; 塑胶凳与三摊子同属一个概念空间,
故 P(塑胶凳) 分配于各拓扑 (= 各摊)。

输出: docs/figs/plastic-stool-topology-{dark,light}.{svg,png}
"""
import os, math
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon, Ellipse

matplotlib.rcParams["font.family"] = ["Hiragino Sans GB", "Arial Unicode MS", "sans-serif"]
matplotlib.rcParams["axes.unicode_minus"] = False
OUT = os.path.join(os.path.dirname(__file__), "..", "docs", "figs")

TH = {
    "dark":  dict(bg="#0b0d10", ink="#e4dfd2", dim="#8d8a80", plane="#1b1f27",
                  plane_e="#39414f", gold="#c9a959", accent="#7fd1c8"),
    "light": dict(bg="#ffffff", ink="#1a1a1a", dim="#6b6b6b", plane="#f4f1e8",
                  plane_e="#c9c3b2", gold="#b8860b", accent="#2f7f77"),
}

W, H = 1150, 980
OY = [700, 470, 240]                     # 三片 (上=早, 中=午, 下=夜)
SLICE_LBL = [("t₋₁", "晨"), ("t₀", "午"), ("t₁", "夜")]
O = (120.0, 0.0)
A = np.array([650.0, -80.0])             # 平面长轴 (向右略降)
B = np.array([115.0, 72.0])              # 平面短轴 (向后略升)
U = [0.15, 0.37, 0.59, 0.88]             # 三摊聚集；便利店单独靠右
SEP = 3                                   # 便利店 = 单独的恒拓扑

STALLS = [
    ("肠粉店", "#e0913f", [0.92, 0.28, 0.08]),
    ("蒸饭店", "#5aa9d6", [0.18, 0.93, 0.14]),
    ("烧烤店", "#d1645c", [0.05, 0.12, 0.90]),
    ("便利店", "#6fb07a", [0.50, 0.50, 0.50]),
]


def pos(slice_k, u):
    """平面上某点 (u 沿长轴, 0.5 居中深度) 的屏幕坐标。"""
    o = np.array([O[0], OY[slice_k]])
    return o + u * A + 0.5 * B


def worldline(i, th, ax):
    """同一摊贯穿三片的波线。"""
    xs, ys = [], []
    for k in range(3):
        px, py = pos(k, U[i])
        xs.append(px); ys.append(py)
    # 手稿般微颤: 在相邻片间插值加正弦抖动
    t = np.linspace(0, 2, 120)
    x = np.interp(t, [0, 1, 2], xs); y = np.interp(t, [0, 1, 2], ys)
    x = x + 6.0 * np.sin(t * math.pi * 2.0 + i)
    if i == SEP:
        ax.plot(x, y, color=STALLS[i][1], lw=1.5, alpha=0.8, zorder=1,
                ls=(0, (5, 4)), solid_capstyle="round")
    else:
        ax.plot(x, y, color=th["dim"], lw=1.5, alpha=0.65, zorder=1,
                solid_capstyle="round")


def radius(p):
    return 10.0 + 46.0 * math.sqrt(p)     # 面积 ∝ 概率


def draw(theme):
    th = TH[theme]
    fig = plt.figure(figsize=(11.5, 9.0), dpi=200)
    fig.patch.set_facecolor(th["bg"])
    ax = fig.add_axes([0.02, 0.02, 0.96, 0.96])
    ax.set_xlim(0, W); ax.set_ylim(0, H); ax.axis("off")
    ax.set_facecolor(th["bg"])

    # ---- 平面 (slice) ----
    for k in range(3):
        o = np.array([O[0], OY[k]])
        quad = [o, o + A, o + A + B, o + B]
        ax.add_patch(Polygon(quad, closed=True, facecolor=th["plane"],
                             edgecolor=th["plane_e"], lw=1.6, zorder=0))
        # 片标
        ax.text(o[0] - 24, o[1] - 26, SLICE_LBL[k][0], color=th["accent"],
                fontsize=15, fontstyle="italic", ha="right", va="center")
        ax.text(o[0] - 24, o[1] - 6, SLICE_LBL[k][1], color=th["dim"],
                fontsize=12, ha="right", va="top")

    # ---- worldlines ----
    for i in range(len(STALLS)):
        worldline(i, th, ax)

    # ---- 三摊 vs 便利店 分界 ----
    udiv = (U[2] + U[SEP]) / 2
    for k in range(3):
        o = np.array([O[0], OY[k]])
        p0 = o + udiv * A; p1 = p0 + B * 1.06
        ax.plot([p0[0], p1[0]], [p0[1], p1[1]], color=th["dim"], lw=1.0,
                alpha=0.5, ls=(0, (2, 4)), zorder=2)

    # ---- 拓扑闭环 (面积 ∝ 概率) ----
    for i, (name, col, probs) in enumerate(STALLS):
        dash = (0, (3, 2)) if i == SEP else "solid"
        for k in range(3):
            px, py = pos(k, U[i])
            r = radius(probs[k])
            ax.add_patch(Ellipse((px, py), r, 0.56 * r, facecolor=col,
                                 alpha=0.16, edgecolor=col, lw=2.4, zorder=3))
            ax.add_patch(Ellipse((px, py), 0.42 * r, 0.24 * r, facecolor="none",
                                 edgecolor=col, lw=1.0, alpha=0.75, zorder=3,
                                 ls=dash))
            ax.text(px, py, f"{probs[k]:.2f}", ha="center", va="center",
                    color=th["ink"], fontsize=9.5, zorder=4)
        # 摊名 (置顶, 留白)
        tx, ty = pos(0, U[i])
        ax.text(tx, OY[0] + 72 + 60, name, ha="center", va="bottom",
                color=col, fontsize=13.5, fontweight="bold")
        if i == SEP:
            ax.text(tx, OY[0] + 72 + 84, "（恒拓扑 · 面积不变）", ha="center",
                    va="bottom", color=th["dim"], fontsize=10.5)
    ax.text(pos(1, (U[0] + U[2]) / 2)[0], OY[1] + 96, "三摊：同一概念空间的变动拓扑",
            ha="center", va="bottom", color=th["dim"], fontsize=10.5)

    # ---- 概念空间名 (塑胶凳, 左侧竖排) ----
    ymid = (OY[0] + OY[2]) / 2 + 20
    ax.text(46, ymid, "塑胶凳 · 概念空间", color=th["gold"], fontsize=16,
            fontweight="bold", rotation=90, va="center", ha="center")

    fig.text(0.04, 0.968, "塑胶凳 · 每片切片上的拓扑（面积 ∝ 概率）", color=th["accent"],
             fontsize=21, fontweight="bold", va="top")
    fig.text(0.04, 0.933, "worldline 贯穿三片＝同一摊随时间；闭环大＝该片概率高。"
                          "便利店三者等大＝平稳轴。", color=th["dim"], fontsize=12, va="top")
    fig.text(0.04, 0.900, "世界（某片）＝ Σᵢ pᵢ · 空间ᵢ  —— 概念空间的线性组合；pᵢ 即各拓扑在该片的概率",
             color=th["gold"], fontsize=12.5, va="top")
    fig.text(0.04, 0.025, "同一概念空间横切三片；闭环＝各拓扑（摊），面积∝概率；"
                          "P(塑胶凳) 分配于诸拓扑（塑胶凳与三摊子同空间）。",
             color=th["dim"], fontsize=11)

    for ext in ("svg", "png"):
        fig.savefig(os.path.join(OUT, f"plastic-stool-topology-{theme}.{ext}"),
                    facecolor=th["bg"])
    plt.close(fig)
    print(f"✔ plastic-stool-topology-{theme}.{{svg,png}}")


if __name__ == "__main__":
    draw("dark")
    draw("light")
