#!/usr/bin/env python3
"""fig_plastic_stool.py — 「塑胶凳 · 切片上的联合分布」图。

主人 1001 亲述的模型：
  · 塑胶凳 = 一条随时间的曲线；早(t₋₁)/午(t₀)/夜(t₁) 三切片；
  · 三集合 = 肠粉店(晨) / 蒸饭店(午) / 烧烤店(夜)；明暗 = 概率密度；
  · 各摊位有各自的塑胶凳，独立分布；便利店概率密度基本平稳；
  · 关键：同一词在「某个切片上」给出一整张 **联合概率分布**（非一组独立标量）。

输出:
  docs/figs/plastic-stool-slice-dark.svg / .png
  docs/figs/plastic-stool-slice-light.svg / .png
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

PAL = {
    "dark":  dict(bg="#0e0f12", ink="#d8d4c8", dim="#8d8a80", grid="#2a2d36",
                  gold="#c9a959", gold_d="#8a6f2e", red="#b46a5a", green="#7fa07a"),
    "light": dict(bg="#ffffff", ink="#1a1a1a", dim="#6b6b6b", grid="#dcdcdc",
                  gold="#c9a959", gold_d="#b8860b", red="#a0522d", green="#4f6f4a"),
}

STALLS = ["肠粉店", "蒸饭店", "烧烤店", "便利店"]
SLICES = ["晨 t₋₁", "午 t₀", "夜 t₁"]

# 边际：P(摊 | 塑胶凳, t) —— 明暗即此值
DENS = np.array([
    [0.92, 0.28, 0.08],   # 肠粉店: 晨盛
    [0.18, 0.93, 0.14],   # 蒸饭店: 午盛
    [0.05, 0.12, 0.90],   # 烧烤店: 夜盛
    [0.50, 0.50, 0.50],   # 便利店: 平稳
])

STOOLS = ["红凳", "蓝凳", "方凳"]
STOOL_P = {                            # 各摊位自己的塑胶凳分布（独立分布）
    "肠粉店": [0.50, 0.30, 0.20],
    "蒸饭店": [0.20, 0.50, 0.30],
    "烧烤店": [0.40, 0.35, 0.25],
    "便利店": [0.34, 0.33, 0.33],
}
NOON = 1
JOINT = np.array([DENS[i, NOON] * np.array(STOOL_P[s]) for i, s in enumerate(STALLS)])


def heat(ax, M, col_labels, row_labels, p, norm_by_max=True, show_vals=True):
    nR, nC = M.shape
    mx = M.max() if norm_by_max else 1.0
    for i in range(nR):
        for j in range(nC):
            v = M[i, j]
            a = 0.06 + 0.94 * (v / mx)
            ax.add_patch(Rectangle((j, nR - 1 - i), 1, 1, facecolor=p["gold"],
                                   alpha=a, edgecolor=p["bg"], lw=2.4))
            if show_vals:
                dark = a > 0.62
                ax.text(j + 0.5, nR - 1 - i + 0.5, f"{v:.2f}", ha="center", va="center",
                        color="#141414" if dark else p["dim"], fontsize=10.5,
                        fontweight="bold" if dark else "normal")
    ax.set_xlim(-0.02, nC + 1.02)          # 右侧留白放注记
    ax.set_ylim(-0.02, nR + 0.02)
    ax.set_xticks([j + 0.5 for j in range(nC)])
    ax.set_xticklabels(col_labels, color=p["ink"], fontsize=12.5)
    ax.set_yticks([nR - 0.5 - i for i in range(nR)])
    ax.set_yticklabels(row_labels, color=p["ink"], fontsize=13)
    ax.tick_params(length=0)
    for sp in ax.spines.values():
        sp.set_visible(False)
    ax.set_facecolor(p["bg"])


def draw(theme):
    p = PAL[theme]
    fig = plt.figure(figsize=(13.6, 7.4), dpi=200)
    fig.patch.set_facecolor(p["bg"])
    axA = fig.add_axes([0.085, 0.24, 0.42, 0.56])
    axB = fig.add_axes([0.640, 0.24, 0.30, 0.56])

    fig.text(0.085, 0.965, "塑胶凳 · 切片上的联合分布", color=p["gold"],
             fontsize=25, fontweight="bold", va="top")
    fig.text(0.085, 0.905, "明暗 ＝ 概率密度；同一词在每一切片上给出一整张联合分布，"
                           "而非一组独立标量", color=p["dim"], fontsize=13, va="top")

    # ---------- 面板 A ----------
    heat(axA, DENS, SLICES, STALLS, p)
    axA.text(0, 1.055, "A · 时间切片上的边际密度   P(摊 | 塑胶凳, t)",
             transform=axA.transAxes, color=p["ink"], fontsize=13.5, va="bottom")
    nR = len(STALLS)
    axA.annotate("平稳轴：三切片等亮\n（time-invariant）",
                 xy=(3.02, 0.5), xytext=(3.22, 0.5), color=p["green"], fontsize=11,
                 va="center", ha="left",
                 arrowprops=dict(arrowstyle="-", color=p["green"], lw=1.3))
    axA.text(0, -0.125, "⊳ 晨盛肠粉 · 午盛蒸饭 · 夜盛烧烤 —— 同一个「塑胶凳」沿时间搬店",
             transform=axA.transAxes, color=p["dim"], fontsize=11, va="top")

    # ---------- 面板 B ----------
    heat(axB, JOINT, STOOLS, STALLS, p, norm_by_max=True)
    axB.text(0, 1.055, "B · 午间切片 (t₀) 上的联合分布   P(摊 × 凳型 | 塑胶凳)",
             transform=axB.transAxes, color=p["ink"], fontsize=13.5, va="bottom")
    axB.text(0, -0.125, "每摊位自有凳分布（独立分布）× 时间边际 → 整张联合表；\n"
                        "非对角／跨行结构 ＝ 摊与摊的关系（小区律）",
             transform=axB.transAxes, color=p["dim"], fontsize=11, va="top")

    fig.text(0.085, 0.022,
             "要点：先验/后验 ＝ 同一曲线两片切片（袜对）；每片切片是一张 联合 分布；"
             "便利店 ＝ 无斜率的不变轴。联合分布的第二轴候主人勘定。",
             color=p["dim"], fontsize=11.2)

    tag = "dark" if theme == "dark" else "light"
    for ext in ("svg", "png"):
        fig.savefig(os.path.join(OUT, f"plastic-stool-slice-{tag}.{ext}"),
                    facecolor=p["bg"])
    plt.close(fig)
    print(f"✔ plastic-stool-slice-{tag}.{{svg,png}}")


if __name__ == "__main__":
    draw("dark")
    draw("light")
