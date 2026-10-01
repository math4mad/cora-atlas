#!/usr/bin/env python3
"""fig_plastic_stool_marginal.py — 依主人 1001 指路 (Lázaro Alonso / MPI-BGI 信息图语法) 重绘：
联合分布 (主图) ＋ 把边际密度投影到顶部/右侧 (marginal projection)。

参照: bgc-jena /en/bgi/gallery 之 precip_vpd (二维联合的柱阵, 色=值) +
      常见 jointplot 语法 (joint 主图 + 顶部/右侧 marginal)。

输出: docs/figs/plastic-stool-marginal-top-{dark,light}.{svg,png}
"""
import os
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
from matplotlib.gridspec import GridSpec

matplotlib.rcParams["font.family"] = ["Hiragino Sans GB", "Arial Unicode MS", "sans-serif"]
matplotlib.rcParams["axes.unicode_minus"] = False
OUT = os.path.join(os.path.dirname(__file__), "..", "docs", "figs")

THEMES = {
    "dark": dict(bg="#0b0d10", ink="#e2ddd0", dim="#8d8a80", grid="#23262d",
                 cmap=["#10131a", "#3a2a1c", "#8a6f2e", "#d8b552", "#fdf3cf"],
                 accent="#7fd1c8"),
    "light": dict(bg="#ffffff", ink="#1a1a1a", dim="#6b6b6b", grid="#e2e2e2",
                  cmap=["#f7f4ec", "#e7d9a8", "#c9a959", "#8a6f2e", "#3a2a1c"],
                  accent="#2f7f77"),
}

STALLS = ["肠粉店", "蒸饭店", "烧烤店", "便利店"]
TIMES = ["晨 t₋₁", "午 t₀", "夜 t₁"]

DENS = np.array([
    [0.92, 0.28, 0.08],
    [0.18, 0.93, 0.14],
    [0.05, 0.12, 0.90],
    [0.50, 0.50, 0.50],
])                                   # 联合 P(摊, t | 塑胶凳) 的密度核
col_marg = DENS.sum(axis=0)          # 投影到顶部: P(t)
row_marg = DENS.sum(axis=1)          # 投影到右侧: P(摊)


def draw(theme):
    th = THEMES[theme]
    cmap = LinearSegmentedColormap.from_list("density", th["cmap"])
    fig = plt.figure(figsize=(13.0, 8.2), dpi=200)
    fig.patch.set_facecolor(th["bg"])
    gs = GridSpec(2, 2, width_ratios=[3.1, 1.0], height_ratios=[1.0, 3.1],
                  left=0.11, right=0.90, bottom=0.10, top=0.82, wspace=0.06, hspace=0.06)

    axT = fig.add_subplot(gs[0, 0])   # 顶部边际
    axJ = fig.add_subplot(gs[1, 0])   # 联合主图
    axR = fig.add_subplot(gs[1, 1])   # 右侧边际

    # ---- 联合主图 ----
    im = axJ.imshow(DENS, cmap=cmap, aspect="auto", origin="upper",
                    vmin=0, vmax=DENS.max())
    for i in range(DENS.shape[0]):
        for j in range(DENS.shape[1]):
            v = DENS[i, j]
            axJ.text(j, i, f"{v:.2f}", ha="center", va="center", fontsize=12,
                     color="#141414" if v > 0.55 else th["dim"],
                     fontweight="bold" if v > 0.55 else "normal")
    axJ.set_xticks(range(len(TIMES)))
    axJ.set_xticklabels(TIMES, color=th["ink"], fontsize=13)
    axJ.set_yticks(range(len(STALLS)))
    axJ.set_yticklabels(STALLS, color=th["ink"], fontsize=13)
    axJ.tick_params(length=0)
    for s in axJ.spines.values():
        s.set_visible(False)
    axJ.set_xticks(np.arange(-.5, len(TIMES), 1), minor=True)
    axJ.set_yticks(np.arange(-.5, len(STALLS), 1), minor=True)
    axJ.grid(which="minor", color=th["bg"], lw=2.6)
    axJ.tick_params(which="minor", length=0)

    # ---- 顶部边际 (投影) ----
    xs = np.arange(len(TIMES))
    axT.fill_between(xs, col_marg, color=th["cmap"][3], alpha=0.85, zorder=2)
    axT.plot(xs, col_marg, color=stc(th, "hi"), lw=2.0, zorder=3)
    for x, v in zip(xs, col_marg):
        axT.text(x, v + 0.06, f"{v:.2f}", ha="center", va="bottom",
                 color=th["ink"], fontsize=10)
    axT.set_xlim(-0.5, len(TIMES) - 0.5)
    axT.set_ylim(0, col_marg.max() * 1.30)
    axT.axis("off")
    axT.text(0.0, 1.16, "↑ 边际密度投影  P(t) = Σ_摊 P(摊, t | 塑胶凳)",
             transform=axT.transAxes, color=th["accent"], fontsize=12, va="bottom")

    # ---- 右侧边际 (投影) ----
    ys = np.arange(len(STALLS))
    axR.barh(ys, row_marg, color=th["cmap"][3], alpha=0.8, zorder=2)
    for y, v in zip(ys, row_marg):
        axR.text(v + 0.05, y, f"{v:.2f}", va="center", ha="left",
                 color=th["ink"], fontsize=10)
    axR.set_ylim(len(STALLS) - 0.5, -0.5)
    axR.set_xlim(0, row_marg.max() * 1.42)
    axR.axis("off")
    axR.text(1.06, 1.0, "→ 边际  P(摊)", transform=axR.transAxes,
             color=th["accent"], fontsize=12, va="bottom", rotation=0)

    # ---- 标题/脚注 ----
    fig.text(0.11, 0.955, "塑胶凳 · 切片上的联合分布（边际投影到顶部）",
             color=th["accent"], fontsize=22, fontweight="bold", va="top")
    fig.text(0.11, 0.917, "主图＝联合 P(摊, t | 塑胶凳)；明暗＝密度；顶＝边际 P(t)；右＝边际 P(摊)。",
             color=th["dim"], fontsize=11.5, va="top")
    fig.text(0.11, 0.893, "便利店整行恒定 ＝ 平稳轴；顶部边际近乎水平 —— 故结构只在联合里。",
             color=th["dim"], fontsize=11.5, va="top")
    fig.text(0.11, 0.020, "效 Lázaro Alonso（MPI-BGI）信息图：二维联合的柱/热阵列 ＋ 边际投影于顶。"
                          "数据为示意，候主人勘定联合之第二轴。", color=th["dim"], fontsize=10.5)

    # 色标 (右上角)
    cax = fig.add_axes([0.685, 0.947, 0.215, 0.014])
    cb = fig.colorbar(im, cax=cax, orientation="horizontal")
    cb.set_label("概率密度  (brightness = density)", color=th["dim"], fontsize=10)
    cb.ax.tick_params(colors=th["dim"], labelsize=8, length=2)
    cb.outline.set_edgecolor(th["grid"])
    for lbl in cb.ax.get_xticklabels():
        lbl.set_color(th["dim"])

    tag = theme
    for ext in ("svg", "png"):
        fig.savefig(os.path.join(OUT, f"plastic-stool-marginal-top-{tag}.{ext}"),
                    facecolor=th["bg"])
    plt.close(fig)
    print(f"✔ plastic-stool-marginal-top-{tag}.{{svg,png}}")


def stc(th, k):
    return th["cmap"][4] if k == "hi" else th["ink"]


if __name__ == "__main__":
    draw("dark")
    draw("light")
