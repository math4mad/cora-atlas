#!/usr/bin/env python3
"""fig_time_slice_big.py — 「时间切片·大图」：把 time-slice-of-status 扩为一张大图。

依主人 1001 设想（据与 ima-Lola 的讨论）：
  · 曲线细化；slice 分 高 / 中 / 低 概率区；
  · 肠粉店、烧烤店 可见概率随时间涨落；
  · 中概率区留给 便利店 / KFC / 麦当劳 / 美宜佳 / 蜜雪冰城（常驻平稳）；
  · 人物入场：送外卖的小哥＝快变曲线；街边拄拐的老头＝慢变曲线。

输出: docs/figs/time-slice-of-status-big-{zh-dark,en-dark,en-light}.{svg,png}
"""
import os
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

matplotlib.rcParams["font.family"] = ["Hiragino Sans GB", "Arial Unicode MS", "sans-serif"]
matplotlib.rcParams["axes.unicode_minus"] = False
OUT = os.path.join(os.path.dirname(__file__), "..", "docs", "figs")

TH = {
    "dark":  dict(bg="#0e0f12", panel="#14161b", ink="#d8d4c8", dim="#8d8a80",
                  grid="#2a2d36", gold="#c9a959",
                  hi="#1e2a24", mid="#20222c", lo="#2a1e1e"),
    "light": dict(bg="#ffffff", panel="#faf8f3", ink="#1a1a1a", dim="#6b6b6b",
                  grid="#e2ded4", gold="#b8860b",
                  hi="#eef4ef", mid="#f1f1f4", lo="#f6eeec"),
}

T = np.linspace(0, 24, 1200)

def wave(mu, lo=0.06, hi=0.94):
    c = 0.5 + 0.5 * np.cos(2 * np.pi * (T - mu) / 24.0)
    return lo + (hi - lo) * c

# 三摊：各自高峰，涨落跨高/中/低区
SHOPS = [
    ("肠粉店", "#e0913f", wave(7.0)),
    ("蒸饭店", "#5aa9d6", wave(12.0)),
    ("烧烤店", "#d1645c", wave(21.0)),
]
# 中概率区常驻（平稳）
STABLE = [
    ("便利店",   "#6fb07a", 0.50 + 0.015 * np.sin(2 * np.pi * T / 24)),
    ("KFC",     "#b07aa8", 0.47 + 0.02 * np.sin(2 * np.pi * T / 12 + 1)),
    ("麦当劳",   "#c9a959", 0.53 + 0.018 * np.cos(2 * np.pi * T / 12)),
    ("美宜佳",   "#7fa0c0", 0.45 + 0.02 * np.sin(2 * np.pi * T / 10 + 2)),
    ("蜜雪冰城", "#8fbf9f", 0.55 + 0.02 * np.cos(2 * np.pi * T / 8)),
]
# 人物
PEOPLE = [
    ("外卖小哥", "#7fd1c8", 0.5 + 0.34 * np.sin(2 * np.pi * T / 2.0)),          # 快变
    ("拄拐老头", "#b9b1a2", 0.5 + 0.13 * np.cos(2 * np.pi * T / 24.0 + 0.6)),   # 慢变
]
SLICES = [(7, "T$_{n-k}$"), (12, "T$_0$"), (21, "T$_1$")]

TXT = {
    "zh": dict(title="时间切片 · 大图", sub="所见状态 ＝ 多条曲线在各时刻的剖面切片",
               hb="高概率区", mb="中概率区（常驻）", lb="低概率区",
               axis="时间 →（晨 · 午 · 夜）",
               stable="中概率区常驻：便利店 / KFC / 麦当劳 / 美宜佳 / 蜜雪冰城",
               foot="肠粉店（晨高峰）、烧烤店（夜高峰）概率随时间涨落；外卖小哥＝快变，拄拐老头＝慢变；中区常驻者近乎不随时刻变。"),
    "en": dict(title="The Time-Slice · Big Chart",
               sub="State = the cross-section (slice) of many curves at each t",
               hb="HIGH-prob region", mb="MID-prob region (persistent)", lb="LOW-prob region",
               axis="time → (morning · noon · night)",
               stable="Persistent mid band: convenience store / KFC / McDonald's / Meiyijia / Mixue",
               foot="Rice-roll shop peaks in the morning, BBQ stall at night (probabilities rise & fall with t); delivery rider = fast, old man on crutches = slow; mid-band dwellers barely vary with t."),
}


def draw(lang, theme):
    th = TH[theme]; tx = TXT[lang]
    fig = plt.figure(figsize=(16, 10), dpi=180)
    fig.patch.set_facecolor(th["bg"])
    ax = fig.add_axes([0.075, 0.155, 0.855, 0.70])
    ax.set_facecolor(th["panel"])

    # 概率区（高/中/低）
    ax.add_patch(Rectangle((0, 0.66), 24, 0.34, facecolor=th["hi"], edgecolor="none", zorder=0))
    ax.add_patch(Rectangle((0, 0.33), 24, 0.33, facecolor=th["mid"], edgecolor="none", zorder=0))
    ax.add_patch(Rectangle((0, 0.00), 24, 0.33, facecolor=th["lo"], edgecolor="none", zorder=0))
    for y in (0.33, 0.66):
        ax.axhline(y, color=th["grid"], lw=1.2, ls=(0, (4, 5)), zorder=1)
    for y, lab in ((0.955, tx["hb"]), (0.625, tx["mb"]), (0.295, tx["lb"])):
        ax.text(0.18, y, lab, ha="left", va="center", color=th["dim"], fontsize=11)

    # slice 带
    for x, lab in SLICES:
        ax.add_patch(Rectangle((x - 0.42, 0), 0.84, 1.0, facecolor=th["gold"], alpha=0.10,
                               edgecolor=th["gold"], lw=1.5, ls=(0, (6, 5)), zorder=2))
        ax.text(x, 1.03, lab, ha="center", va="bottom", color=th["gold"], fontsize=15,
                fontstyle="italic")

    # 曲线
    for name, col, y in SHOPS + STABLE + PEOPLE:
        fw = 2.9 if name in ("外卖小哥", "拄拐老头") else 2.3
        ax.plot(T, y, color=col, lw=fw, zorder=4, solid_capstyle="round")
    # 交点小圈
    for x, _ in SLICES:
        for name, col, y in SHOPS + PEOPLE:
            ax.plot([x], [np.interp(x, T, y)], "o", ms=6, mfc=th["panel"], mec=col, mew=2, zorder=5)

    ax.set_xlim(0, 24); ax.set_ylim(0, 1)
    ax.set_xticks([]); ax.set_yticks([])
    for s in ax.spines.values():
        s.set_visible(False)

    # 左侧摊名/人名（错位）
    left_labels = []
    # 直接在曲线左端标名（ha=right）
    for name, col, y in SHOPS:
        ax.annotate(name, xy=(0, y[0]), xytext=(-0.6, y[0]), ha="right", va="center",
                    color=col, fontsize=12.5, fontweight="bold",
                    arrowprops=dict(arrowstyle="-", color=col, lw=1.0))
    for name, col, y in PEOPLE:
        ax.annotate(name, xy=(0, y[0]), xytext=(-0.6, y[0]), ha="right", va="center",
                    color=col, fontsize=12.5, fontweight="bold",
                    arrowprops=dict(arrowstyle="-", color=col, lw=1.0))
    # 中区常驻：右端聚成一束 + 括注
    endx = 24
    for name, col, y in STABLE:
        ax.annotate(name, xy=(endx, y[-1]), xytext=(endx + 0.7, y[-1]), ha="left", va="center",
                    color=col, fontsize=10.5,
                    arrowprops=dict(arrowstyle="-", color=col, lw=0.9))

    # 时间轴
    ax.annotate("", xy=(24, -0.055), xytext=(0, -0.055),
                arrowprops=dict(arrowstyle="-|>", color=th["gold"], lw=2.4))
    ax.text(12, -0.12, tx["axis"], ha="center", va="top", color=th["dim"], fontsize=12)

    # 标题/脚注
    fig.text(0.075, 0.965, tx["title"], color=th["gold"], fontsize=26, fontweight="bold", va="top")
    fig.text(0.075, 0.920, tx["sub"], color=th["dim"], fontsize=13.5, va="top")
    fig.text(0.075, 0.055, tx["stable"], color=th["ink"], fontsize=12, va="top")
    fig.text(0.075, 0.028, tx["foot"], color=th["dim"], fontsize=11, va="top")

    tag = f"{lang}-{'dark' if theme == 'dark' else 'light'}"
    for ext in ("svg", "png"):
        fig.savefig(os.path.join(OUT, f"time-slice-of-status-big-{tag}.{ext}"), facecolor=th["bg"])
    plt.close(fig)
    print(f"✔ time-slice-of-status-big-{tag}.{{svg,png}}")


if __name__ == "__main__":
    draw("zh", "dark")
    draw("en", "dark")
    draw("en", "light")
