#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""fig_time_spine.py —「生物体 time-spine · 生命尺度柱阵」(切片柱阵 · 图2)

母本＝今晨 ima 笔记《切片柱阵·三图提示词》doc 7511883443609699。
笔记云：图2 目的是「先把**跨尺度 lifespan 怎么同框**讲清楚，是 **切片轴律** 的现场教学」；
并警告「勿用等距年龄轴，否则昆虫被压成一条线、大象溢出」。

故本图把这一课做正：**同一批物种，两种切片轴并置**——
  Panel A · **等距年龄轴**（0–80 年线性）：小/短物种被压成一条线。
  Panel B · **生命阶段轴**（卵/幼体/亚成体/成体/老年，各物种自归一）：跨尺度同框。
= 切片轴律之现场：**切片怎么 bin，柱阵就讲什么故事。**

数据：概念图（示意值），各物种 lifespan 与里程碑取公开常识量级，**非精确数据**。
用法: .venv/bin/python scripts/fig_time_spine.py
"""
import os
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

D = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
VER = os.environ.get("VER", "v01")
OUT = os.path.join(D, "docs", "figs", "time-spine", VER)
os.makedirs(OUT, exist_ok=True)
matplotlib.rcParams["font.family"] = ["Hiragino Sans GB", "Arial Unicode MS", "sans-serif"]
matplotlib.rcParams["axes.unicode_minus"] = False

BG = "#f4f7f6"; INK = "#1d2b2a"; DIM = "#6b7b79"; GRID = "#d6e0dd"
STAGES = ["卵", "幼体", "亚成体", "成体", "老年"]

# 物种（示意）：name, 色, 里程碑年龄（年）, 各阶段强度(0..1)
SPECIES = [
    ("果蝇", "#c98b48", [0.0, 0.008, 0.02, 0.05, 0.12], [0.30, 0.60, 0.55, 0.60, 0.30]),
    ("小鼠", "#8a9b6e", [0.0, 0.12, 0.35, 1.00, 2.60], [0.30, 0.55, 0.50, 0.45, 0.25]),
    ("龟",   "#4e8f7a", [0.0, 1.0, 6.0, 25.0, 45.0], [0.25, 0.35, 0.45, 0.70, 0.85]),
    ("人",   "#3f7fb3", [0.0, 1.2, 13.0, 40.0, 75.0], [0.20, 0.40, 0.60, 0.90, 0.70]),
    ("大象", "#9a5b52", [0.0, 2.0, 13.0, 35.0, 60.0], [0.40, 0.60, 0.80, 1.00, 0.90]),
]


def draw():
    fig = plt.figure(figsize=(15.5, 8.2), dpi=110)
    fig.patch.set_facecolor(BG)
    fig.text(0.04, 0.965, "生物体 time-spine · 生命尺度柱阵", color=INK,
             fontsize=25, fontweight="bold", va="top")
    fig.text(0.04, 0.925, "同一批物种，两种切片轴并置 —— 切片轴律之现场：切片怎么 bin，柱阵就讲什么故事",
             color=DIM, fontsize=12.5, va="top")

    n = len(SPECIES)
    axA = fig.add_axes([0.075, 0.115, 0.42, 0.74])
    axB = fig.add_axes([0.565, 0.115, 0.40, 0.74])

    # ---------- Panel A · 等距年龄轴 ----------
    axA.set_facecolor(BG)
    for sp in axA.spines.values():
        sp.set_visible(False)
    axA.set_xlim(-2, 82); axA.set_ylim(-0.4, n - 0.4)
    axA.set_yticks([]); axA.set_xticks([0, 20, 40, 60, 80])
    axA.set_xticklabels(["0", "20", "40", "60", "80"], color=INK, fontsize=11)
    axA.tick_params(length=0)
    for x in range(0, 81, 20):
        axA.plot([x, x], [-0.4, n - 0.4], color=GRID, lw=0.8, zorder=0)
    for ri, (name, col, ages, hh) in enumerate(SPECIES):
        y = n - 1 - ri
        axA.plot([-0.5, 81], [y, y], color=GRID, lw=0.8, zorder=0)
        axA.text(-2.5, y + 0.05, name, color=INK, fontsize=13, ha="right", va="center")
        for a, h in zip(ages, hh):
            axA.add_patch(Rectangle((a - 0.7, y - 0.34), 1.4, 0.68 * h,
                                    facecolor=col, edgecolor="white", lw=0.5, alpha=0.92, zorder=3))
    axA.set_title("A · 等距年龄轴（0–80 年 线性）—— 短命小物种被压成一条线", color=INK,
                  fontsize=13.5, pad=10)
    axA.set_xlabel("年龄（年，等距）", color=DIM, fontsize=11)

    # ---------- Panel B · 生命阶段轴 ----------
    axB.set_facecolor(BG)
    for sp in axB.spines.values():
        sp.set_visible(False)
    axB.set_xlim(-0.6, 4.6); axB.set_ylim(-0.4, n - 0.4)
    axB.set_yticks([]); axB.set_xticks(range(5)); axB.set_xticklabels(STAGES, color=INK, fontsize=12)
    axB.tick_params(length=0)
    for x in range(5):
        axB.plot([x, x], [-0.4, n - 0.4], color=GRID, lw=0.8, zorder=0)
    for ri, (name, col, ages, hh) in enumerate(SPECIES):
        y = n - 1 - ri
        axB.plot([-0.6, 4.6], [y, y], color=GRID, lw=0.8, zorder=0)
        axB.text(-0.7, y + 0.05, name, color=INK, fontsize=13, ha="right", va="center")
        for ci, h in enumerate(hh):
            axB.add_patch(Rectangle((ci - 0.34, y - 0.34), 0.68, 0.68 * h,
                                    facecolor=col, edgecolor="white", lw=0.6, alpha=0.92, zorder=3))
    axB.set_title("B · 生命阶段轴（卵/幼/亚成/成/老，各物种自归一）—— 跨尺度同框", color=INK,
                  fontsize=13.5, pad=10)
    axB.set_xlabel("生命阶段切片（共享切片轴）", color=DIM, fontsize=11)

    fig.text(0.04, 0.052,
             "读：同一批物种——A 轴上果蝇/小鼠挤在原点（被压成一条线），大象铺满；B 轴上换成生命阶段切片，"
             "各尺度同框可比。", color=INK, fontsize=11)
    fig.text(0.04, 0.026,
             "示意 · 概念图（lifespan 与里程碑取公开常识量级，非精确数据）· 母本 ima doc 7511883443609699 · "
             f"ver {VER} · lola", color=DIM, fontsize=9.5)

    for ext in ("png", "svg"):
        fig.savefig(os.path.join(OUT, f"time-spine-zh.{ext}"), facecolor=BG)
    plt.close(fig)
    print("→", OUT)
    print("TIME_SPINE_DONE")


if __name__ == "__main__":
    draw()
