#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""fig_child_dev_poster.py — 儿童发展 · 概念演示海报（A 圆 / B 三维柱）

主人 1003 定调：要「A 圆 / B 三维柱」的整体观感/海报感；
**这是概念演示——主要演示"变化"与"轴趋势"，不为展示精确数据**。
故：去数字、放大形、加趋势线，长轴＝时间，月龄切片。

数据：本地 CHILDES（五指标 × 月龄切片），各指标自身 max 归一（仅作形状/高低）。
输出：docs/figs/child-dev-poster/v01/child-dev-poster-zh.{png,svg}
用法: .venv/bin/python scripts/fig_child_dev_poster.py
"""
import os, math, sys
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, FancyArrow

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from fig_child_dev_slices import collect, iso_bar, SLICES, METRICS, COLORS, BG, DIM  # noqa

D = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
VER = os.environ.get("VER", "v01")
OUT = os.path.join(D, "docs", "figs", "child-dev-poster", VER)
os.makedirs(OUT, exist_ok=True)
matplotlib.rcParams["font.family"] = ["Hiragino Sans GB", "Arial Unicode MS", "sans-serif"]
matplotlib.rcParams["axes.unicode_minus"] = False
INK = "#16211f"
XS = list(range(len(SLICES)))


def main():
    V = collect()
    fig = plt.figure(figsize=(16, 10), dpi=110)
    fig.patch.set_facecolor(BG)

    # ── 报头 ──────────────────────────────────────────────
    fig.text(0.045, 0.965, "儿童发展 · 切片柱阵", color=INK, fontsize=34, fontweight="bold", va="top")
    fig.text(0.045, 0.905, "长轴＝时间（月龄 12 → 42）；每片＝该月五指标的横截面　"
                           "——　概念演示：看「变化」与「轴趋势」（非精确数据）",
             color=DIM, fontsize=13.5, va="top")
    # 五指标图例
    lx = 0.045
    for mi, m in enumerate(METRICS):
        fig.text(lx, 0.860, "●", color=COLORS[mi], fontsize=13)
        fig.text(lx + 0.016, 0.862, m, color=DIM, fontsize=11.5)
        lx += 0.165

    # ── A · 圆簇（去数字，加趋势线）───────────────────────
    axA = fig.add_axes([0.05, 0.545, 0.90, 0.275]); axA.set_facecolor(BG); axA.axis("off")
    axA.set_xlim(-0.6, len(SLICES) - 0.4); axA.set_ylim(-0.95, 0.95)
    OFF = [(0.0, 0.40), (-0.255, 0.02), (0.255, 0.02), (-0.13, -0.36), (0.13, -0.36)]
    # 先画淡趋势线（以「词汇量」槽位贯穿 → 成长指引）
    axA.plot(XS, [0.40] * len(XS), color="#cfe0dc", lw=1.0, ls=(0, (4, 5)), zorder=1)
    for si, x in enumerate(XS):
        for mi in range(5):
            v = V[si, mi]; r = 0.045 + 0.135 * math.sqrt(v); ox, oy = OFF[mi]
            axA.add_patch(Circle((x + ox, oy), r, facecolor=COLORS[mi], edgecolor="white",
                                 lw=1.4, alpha=0.92, zorder=3))
        axA.text(x, -0.80, SLICES[si], color=INK, fontsize=12, ha="center")
    axA.text(len(SLICES) - 0.4, -0.80, " 月", color=DIM, fontsize=11, ha="left")
    axA.add_patch(FancyArrow(-0.55, -0.80, len(SLICES) - 0.55, 0, width=0.004,
                             head_width=0.05, head_length=0.18, color="#b9c8c4", zorder=2))
    axA.set_title("A · 圆簇（面积 ∝ 值，去数字，看生长与趋势）", color=INK, fontsize=14,
                  pad=6, loc="left")

    # ── B · 45° 三维柱（去数字，放大观感）─────────────────
    axB = fig.add_axes([0.05, 0.085, 0.90, 0.40]); axB.set_facecolor(BG); axB.axis("off")
    axB.set_xlim(-0.8, len(SLICES) - 0.2); axB.set_ylim(-0.95, 1.5)
    BARW, GAP, DX, DY = 0.15, 0.18, 0.115, 0.075
    for si, x in enumerate(XS):
        bx = x - 0.44
        axB.add_patch(plt.Polygon([(bx - 0.05, -0.60), (bx - 0.05 + 4 * GAP + BARW, -0.60),
                                   (bx - 0.05 + 4 * GAP + BARW + DX, -0.60 + DY),
                                   (bx - 0.05 + DX, -0.60 + DY)],
                                  closed=True, facecolor="#e7ecea", edgecolor="#cfd8d5", lw=0.6, zorder=1))
        for mi in range(5):
            iso_bar(axB, bx + mi * GAP, -0.58, 0.08 + 1.05 * V[si, mi], COLORS[mi],
                    w=BARW, d=(DX, DY), z=3 + si * 0.5 + mi * 0.05)
        axB.text(x, -0.9, SLICES[si], color=INK, fontsize=12, ha="center")
    axB.text(len(SLICES) - 0.25, -0.9, " 月", color=DIM, fontsize=11, ha="left")
    axB.set_title("B · 45° 三维柱（高矮 ∝ 值，去数字，看形与势）", color=INK, fontsize=14,
                  pad=6, loc="left")

    fig.text(0.045, 0.028,
             "读法：沿长轴（时间）从左到右＝发育推进；每片内五指标的高低/大小＝该月的横截面结构。"
             "本图为概念演示，只示变化与趋势，不作精确读数；数据＝本地 CHILDES（仅作形状）。",
             color=DIM, fontsize=10.5)
    fig.text(0.955, 0.028, f"ver {VER} · lola", color=DIM, fontsize=9, ha="right")

    for ext in ("png", "svg"):
        fig.savefig(os.path.join(OUT, f"child-dev-poster-zh.{ext}"), facecolor=BG)
    plt.close(fig)
    print("→", OUT)
    print("CHILD_DEV_POSTER_DONE")


if __name__ == "__main__":
    main()
