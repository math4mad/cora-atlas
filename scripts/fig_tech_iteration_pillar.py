#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""fig_tech_iteration_pillar.py —「技术迭代柱阵」（切片柱阵 · 图3）

母本＝今晨 ima 笔记《切片柱阵·三图提示词》doc 7511883443609699。
笔记云：图3 行＝NVIDIA GPU / AMD GPU / iPhone；横轴＝发布年份；
「两列 GPU 行左右并跑，形成**对决柱林**（呼应 PK／对决柱林），iPhone 行展示消费电子迭代节奏」。

数据：各代公开规格（TFLOPS FP32；iPhone 用相对性能指数），**近似取整·示意**，见 data/tech-iteration.csv。
各行内 max 归一（GPU 两行同为 TFLOPS 可比；iPhone 单位不同，仅示节奏）。
用法: .venv/bin/python scripts/fig_tech_iteration_pillar.py
"""
import os
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

D = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
VER = os.environ.get("VER", "v01")
OUT = os.path.join(D, "docs", "figs", "tech-iteration", VER)
os.makedirs(OUT, exist_ok=True)
matplotlib.rcParams["font.family"] = ["Hiragino Sans GB", "Arial Unicode MS", "sans-serif"]
matplotlib.rcParams["axes.unicode_minus"] = False

BG = "#f6f7f9"; INK = "#14181d"; DIM = "#6b7480"; GRID = "#dde1e7"
Y0, Y1 = 2009, 2026

# (name, 色, [(年, 值, 标签)])
ROWS = [
    ("NVIDIA", "#76b900", [(2010, 1.3, "GTX480"), (2013, 4.0, "GTX780"), (2016, 8.9, "GTX1080"),
                           (2018, 10.1, "RTX2080"), (2020, 35.6, "RTX3090"), (2022, 82.6, "RTX4090"),
                           (2025, 104.8, "RTX5090")]),
    ("AMD",    "#e2231a", [(2010, 2.7, "HD5870"), (2012, 3.8, "HD7970"), (2013, 5.6, "R9 290X"),
                           (2016, 5.8, "RX480"), (2019, 9.8, "RX5700XT"), (2020, 23.0, "RX6900XT"),
                           (2022, 61.4, "RX7900XTX"), (2025, 48.0, "RX9070XT")]),
    ("iPhone", "#8e8e93", [(2010, 0.25, "4"), (2014, 0.9, "6"), (2017, 2.1, "X"),
                           (2020, 4.5, "12"), (2024, 9.0, "16")]),
]


def draw():
    fig = plt.figure(figsize=(15.5, 8.2), dpi=110)
    fig.patch.set_facecolor(BG)
    fig.text(0.04, 0.965, "技术迭代柱阵", color=INK, fontsize=25, fontweight="bold", va="top")
    fig.text(0.04, 0.925, "切片柱阵 · 三行（NVIDIA ∥ AMD ∥ iPhone）× 发布年份切片 · "
                          "GPU 两行并跑＝对决柱林（接 PK／对决律）", color=DIM, fontsize=12.5, va="top")

    n = len(ROWS)
    ax = fig.add_axes([0.075, 0.13, 0.885, 0.72])
    ax.set_facecolor(BG)
    for sp in ax.spines.values():
        sp.set_visible(False)
    ax.set_xlim(Y0, Y1); ax.set_ylim(-0.45, n - 0.45)
    ax.set_yticks([]); ax.set_xticks([2010, 2013, 2016, 2019, 2022, 2025])
    ax.set_xticklabels(["2010", "2013", "2016", "2019", "2022", "2025"], color=INK, fontsize=11.5)
    ax.tick_params(length=0)
    for x in range(2010, Y1, 3):
        ax.plot([x, x], [-0.45, n - 0.45], color=GRID, lw=0.8, zorder=0)

    for ri, (name, col, pts) in enumerate(ROWS):
        y = n - 1 - ri
        ax.plot([Y0, Y1], [y, y], color=GRID, lw=0.8, zorder=0)
        ax.text(Y0 - 0.15, y + 0.06, name, color=INK, fontsize=14.5, ha="right",
                va="center", fontweight="bold")
        mx = max(v for _, v, _ in pts)
        for yr, v, lbl in pts:
            h = 0.72 * v / mx
            ax.add_patch(Rectangle((yr - 0.55, y - 0.36), 1.1, h,
                                   facecolor=col, edgecolor="white", lw=0.6, alpha=0.93, zorder=3))
            ax.text(yr, y - 0.36 + h + 0.03, f"{v:g}", color=DIM, fontsize=7.8,
                    ha="center", va="bottom", zorder=4)
            ax.text(yr, y - 0.42, lbl, color=DIM, fontsize=7.0, ha="center", va="top",
                    rotation=45, zorder=4)

    ax.set_xlabel("发布年份切片（共享切片轴）", color=DIM, fontsize=11.5, labelpad=6)
    fig.text(0.04, 0.052,
             "读：GPU 两行＝对决柱林——AMD 早年（HD5870）曾压 NVIDIA，2016 后 NVIDIA 反超并拉开（RTX 世代陡起）；"
             "iPhone 行＝消费电子迭代节奏。", color=INK, fontsize=11)
    fig.text(0.04, 0.026,
             "数据：各代公开规格（TFLOPS FP32；iPhone 为相对性能指数）· 近似取整·示意 · 各行 max 归一 "
             f"· 母本 ima doc 7511883443609699 · ver {VER} · lola", color=DIM, fontsize=9.5)

    for ext in ("png", "svg"):
        fig.savefig(os.path.join(OUT, f"tech-iteration-zh.{ext}"), facecolor=BG)
    plt.close(fig)
    print("→", OUT)
    print("TECH_ITER_DONE")


if __name__ == "__main__":
    draw()
