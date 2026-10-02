#!/usr/bin/env python3
"""fig_seq_skeleton.py — 「共现 / 序 / 骨架」三层 ＋ 「序位」第三轴。

主人 1001 问：肠粉店一片可切（元素同现于晨）；NBA 选秀榜应跨多片。
对岸 ima-Lola 信二十一裁定：
  · 共现 = 片上的支撑（一列系数）——  天气
  · 序   = 片与片之间的有向边（轨迹）—— 骨架上的路径
  · 骨架 = 二者共用的地板
  · 序 = PK 的时间展开；序位 = 第三轴（大图 → 纤维丛「维×概率×序位」）

输出: docs/figs/coexistence-order-skeleton-{dark,light}.{svg,png}
"""
import os, math
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, FancyArrowPatch, Ellipse

matplotlib.rcParams["font.family"] = ["Hiragino Sans GB", "Arial Unicode MS", "sans-serif"]
matplotlib.rcParams["axes.unicode_minus"] = False
OUT = os.path.join(os.path.dirname(__file__), "..", "docs", "figs")

TH = {
    "dark":  dict(bg="#0b0d10", ink="#e4dfd2", dim="#8f8b82", faint="#3a3d45",
                  gold="#c9a959", goldd="#e3c879", red="#c0705c", blue="#6fa8c8", panel="#14161b"),
    "light": dict(bg="#ffffff", ink="#1a1a1a", dim="#6b6b6b", faint="#d8d2c4",
                  gold="#b8860b", goldd="#8a6f2e", red="#a0522d", blue="#3f7f9f", panel="#faf8f3"),
}

W, H = 1340, 820


def ll(theme, k):
    zh = dict(title="共现 · 序 · 骨架：三层不可混",
              sub="肠粉店一片可切（元素同现）；选秀榜须跨片（有向的序）。序位＝第三轴。",
              slice="切片 t", coexist="共现（一列系数）＝天气", order="序（片间的边）＝骨架上的轨迹",
              skeleton="骨架 ＝ 二者共用的地板", pos="序位（第三轴）", axis="时间 →",
              foot="序不是新物种，是 PK 换了一根轴；序只能「重放」，不能「读」。")
    en = dict(title="Coexistence · Order · Skeleton",
              sub="A rice-roll shop fits one slice; a draft list spans slices. Ordinal position = the third axis.",
              slice="slice t", coexist="coexistence (a column) = weather", order="order (edges between slices) = trajectory on skeleton",
              skeleton="skeleton = the shared floor", pos="ordinal position (3rd axis)", axis="time →",
              foot="Order is not a new species; it is PK with a new axis — order can only be replayed, not read.")
    return (en if theme.startswith("en-") else zh)[k]


def main(theme):
    th = TH[theme]
    fig = plt.figure(figsize=(13.4, 8.2), dpi=200)
    fig.patch.set_facecolor(th["bg"])
    ax = fig.add_axes([0.03, 0.03, 0.94, 0.94]); ax.set_xlim(0, W); ax.set_ylim(0, H); ax.axis("off")
    ax.set_facecolor(th["bg"])

    # ---- 骨架：地板 ----
    sx0, sx1, sy = 120, 1200, 210
    ax.add_patch(Rectangle((sx0, sy - 26), sx1 - sx0, 52, facecolor=th["panel"],
                           edgecolor=th["faint"], lw=1.4, zorder=1))
    ax.text(sx0, sy + 46, ll(theme, "skeleton"), color=th["dim"], fontsize=12, ha="left", va="bottom")

    # ---- 三片切片 ----
    SL = [0.14, 0.42, 0.72, 0.94]
    for i, t in enumerate(SL):
        x = sx0 + (sx1 - sx0) * t
        ax.plot([x, x], [sy - 24, 620], color=th["gold"], lw=1.1, ls=(0, (5, 5)), alpha=0.5, zorder=2)
        ax.text(x, 628, f"{ll(theme,'slice')}{i+1}", color=th["gold"], fontsize=11, ha="center", va="bottom")

    # ---- 共现：每片一列系数（柱） ----
    vals = [0.30, 0.85, 0.55, 0.20]           # 一点"维"上的系数（例）
    for i, (t, v) in enumerate(zip(SL, vals)):
        x = sx0 + (sx1 - sx0) * t
        h = 60 + 300 * v
        ax.add_patch(Rectangle((x - 16, sy + 26), 32, h, facecolor=th["blue"], alpha=0.22,
                               edgecolor=th["blue"], lw=1.6, zorder=3))
        ax.text(x, sy + 26 + h + 8, f"{v:.2f}", color=th["blue"], fontsize=9.5, ha="center", va="bottom")
    ax.text(sx0 - 8, sy + 26 + 300, ll(theme, "coexist"), color=th["blue"], fontsize=12,
            ha="left", va="center")

    # ---- 序：片与片之间的有向边（弧） ----
    pts = [(sx0 + (sx1 - sx0) * t, sy + 26 + 60 + 300 * v) for t, v in zip(SL, vals)]
    for a, b in zip(pts, pts[1:]):
        ax.add_patch(FancyArrowPatch(a, b, connectionstyle="arc3,rad=-0.28", arrowstyle="-|>",
                     mutation_scale=16, color=th["red"], lw=2.2, zorder=5))
    ax.text((pts[0][0] + pts[1][0]) / 2, pts[0][1] + 96, ll(theme, "order"), color=th["red"],
            fontsize=12, ha="center", va="bottom")

    # ---- 序位：第三轴（右侧小坐标） ----
    axp = fig.add_axes([0.885, 0.30, 0.085, 0.42]); axp.set_facecolor(th["bg"])
    for s in axp.spines.values():
        s.set_color(th["faint"])
    axp.set_xticks([]); axp.set_yticks([0, 1, 2, 3])
    axp.set_yticklabels(["1st", "2nd", "3rd", "4th"], color=th["goldd"], fontsize=9)
    axp.tick_params(length=0)
    axp.set_ylabel("") 
    axp.text(0.5, 1.06, ll(theme, "pos"), transform=axp.transAxes, color=th["goldd"],
             fontsize=11, ha="center", va="bottom")

    # ---- 时间轴 ----
    ay = 120
    ax.add_patch(FancyArrowPatch((sx0, ay), (sx1 + 30, ay), arrowstyle="-|>", mutation_scale=18,
                                 color=th["dim"], lw=1.6))
    ax.text((sx0 + sx1) / 2, ay - 22, ll(theme, "axis"), color=th["dim"], fontsize=12,
            ha="center", va="top", style="italic")

    fig.text(0.045, 0.968, ll(theme, "title"), color=th["gold"], fontsize=23, fontweight="bold", va="top")
    fig.text(0.045, 0.928, ll(theme, "sub"), color=th["dim"], fontsize=12, va="top")
    fig.text(0.045, 0.028, ll(theme, "foot"), color=th["dim"], fontsize=10.5, va="top")

    tag = "dark" if theme == "dark" else "light"
    for ext in ("svg", "png"):
        fig.savefig(os.path.join(OUT, f"coexistence-order-skeleton-{tag}.{ext}"), facecolor=th["bg"])
    plt.close(fig)
    print(f"✔ coexistence-order-skeleton-{tag}.{{svg,png}}")


if __name__ == "__main__":
    main("dark")
    main("light")
