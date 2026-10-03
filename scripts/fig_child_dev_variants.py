#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""fig_child_dev_variants.py — 儿童发展切片柱阵 · 多形式对照集

主人 1003 令：「多出几种形式，比较哪种更易理解、更美观」；方案二存为迭代，之前的格式保留。
同数据（本地 CHILDES，五指标 × 六月龄切片），六种呈现：

  A · 圆簇（bubble cluster，面积∝值）
  B · 45° 三维柱（isometric bars）          ← 方案二
  C · 立起方柱（切片柱阵原式·分组柱）
  D · 热力矩阵（metrics × months，色＋数）
  E · 雷达小多图（每片一雷达）
  F · 趋势折线（五线跨月）

出：docs/figs/child-dev-variants/v01/var-{A..F}.png ＋ compare.png（2×3 对照贴）
用法: .venv/bin/python scripts/fig_child_dev_variants.py
"""
import os, math, sys
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, Polygon
from PIL import Image

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from fig_child_dev_slices import collect, iso_bar, SLICES, METRICS, COLORS, BG, INK, DIM  # noqa

D = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
VER = os.environ.get("VER", "v01")
OUT = os.path.join(D, "docs", "figs", "child-dev-variants", VER)
os.makedirs(OUT, exist_ok=True)
XS = list(range(len(SLICES)))


def _frame(w=12.6, h=5.4, title=""):
    fig = plt.figure(figsize=(w, h), dpi=110)
    fig.patch.set_facecolor(BG)
    if title:
        fig.text(0.035, 0.945, title, color=INK, fontsize=17, fontweight="bold", va="top")
    fig.text(0.035, 0.045, "儿童发展 · 五指标 × 月龄切片 12→42（各指标自身 max 归一）· 本地 CHILDES · lola",
             color=DIM, fontsize=8.6)
    return fig


def save(fig, name):
    fig.savefig(os.path.join(OUT, name), facecolor=BG)
    plt.close(fig)
    print("  ", name)


def var_A(V):
    fig = _frame(title="A · 圆簇（面积 ∝ 值）")
    ax = fig.add_axes([0.05, 0.13, 0.92, 0.74]); ax.set_facecolor(BG); ax.axis("off")
    ax.set_xlim(-0.6, len(SLICES) - 0.4); ax.set_ylim(-0.7, 0.9)
    OFF = [(0.0, 0.42), (-0.30, 0.06), (0.30, 0.06), (-0.16, -0.34), (0.16, -0.34)]
    for si, x in enumerate(XS):
        for mi in range(5):
            v = V[si, mi]; r = 0.05 + 0.16 * math.sqrt(v); ox, oy = OFF[mi]
            ax.add_patch(Circle((x + ox, oy), r, facecolor=COLORS[mi], edgecolor="white", lw=1, alpha=0.9))
            ax.text(x + ox, oy, f"{v:.2f}", color="white", fontsize=6.4, ha="center", va="center")
        ax.text(x, -0.62, SLICES[si], color=INK, fontsize=10.5, ha="center")
    save(fig, "var-A-circles.png")


def var_B(V):
    fig = _frame(title="B · 45° 三维柱（方案二）")
    ax = fig.add_axes([0.04, 0.13, 0.94, 0.74]); ax.set_facecolor(BG); ax.axis("off")
    ax.set_xlim(-0.8, len(SLICES) - 0.2); ax.set_ylim(-0.9, 1.5)
    BARW, GAP, DX, DY = 0.15, 0.18, 0.115, 0.075
    for si, x in enumerate(XS):
        bx = x - 0.44
        ax.add_patch(Polygon([(bx - 0.05, -0.60), (bx - 0.05 + 4 * GAP + BARW, -0.60),
                              (bx - 0.05 + 4 * GAP + BARW + DX, -0.60 + DY), (bx - 0.05 + DX, -0.60 + DY)],
                             closed=True, facecolor="#e7ecea", edgecolor="#cfd8d5", lw=0.6, zorder=1))
        for mi in range(5):
            iso_bar(ax, bx + mi * GAP, -0.58, 0.08 + 1.05 * V[si, mi], COLORS[mi], w=BARW,
                    d=(DX, DY), z=3 + si * 0.5 + mi * 0.05)
        ax.text(x, -0.85, SLICES[si], color=INK, fontsize=10.5, ha="center")
    save(fig, "var-B-iso-bars.png")


def var_C(V):
    fig = _frame(title="C · 立起方柱（切片柱阵原式）")
    ax = fig.add_axes([0.05, 0.13, 0.92, 0.74]); ax.set_facecolor(BG); ax.axis("off")
    ax.set_xlim(-0.6, len(SLICES) - 0.4); ax.set_ylim(-0.25, 1.05)
    W = 0.15
    for si, x in enumerate(XS):
        base = x - 0.42
        for mi in range(5):
            h = 0.03 + 0.9 * V[si, mi]
            ax.add_patch(Polygon([(base + mi * (W + 0.03), 0), (base + mi * (W + 0.03) + W, 0),
                                  (base + mi * (W + 0.03) + W, h), (base + mi * (W + 0.03), h)],
                                 closed=True, facecolor=COLORS[mi], edgecolor="white", lw=0.6))
        ax.plot([x - 0.5, x + 0.5], [0, 0], color="#cfd8d5", lw=0.8)
        ax.text(x, -0.18, SLICES[si], color=INK, fontsize=10.5, ha="center")
    save(fig, "var-C-pillars.png")


def var_D(V):
    fig = _frame(title="D · 热力矩阵（色＋数）")
    ax = fig.add_axes([0.16, 0.16, 0.80, 0.70]); ax.set_facecolor(BG)
    for sp in ax.spines.values():
        sp.set_visible(False)
    ax.set_xlim(-0.5, len(SLICES) - 0.5); ax.set_ylim(-0.5, 4.5)
    ax.set_xticks(XS); ax.set_xticklabels([str(m) for m in SLICES], color=INK, fontsize=10.5)
    ax.set_yticks(range(5)); ax.set_yticklabels(METRICS[::-1], color=INK, fontsize=10)
    ax.tick_params(length=0)
    for ri in range(5):
        for ci in range(len(SLICES)):
            v = V[ci, ri]; y = 4 - ri
            from matplotlib import cm
            c = plt.get_cmap("YlGnBu")(0.08 + 0.92 * v)
            ax.add_patch(plt.Rectangle((ci - 0.47, y - 0.42), 0.94, 0.84, facecolor=c,
                                       edgecolor="white", lw=1.2))
            ax.text(ci, y, f"{v:.2f}", color=("#12212a" if v > 0.55 else "#33474f"),
                    fontsize=8.4, ha="center", va="center")
    save(fig, "var-D-heatmap.png")


def var_E(V):
    fig = _frame(w=12.6, h=5.2, title="E · 雷达小多图（每片一雷达）")
    for si in range(len(SLICES)):
        ax = fig.add_axes([0.02 + si * 0.163, 0.16, 0.155, 0.66], polar=True)
        ax.set_facecolor(BG)
        ang = np.linspace(0, 2 * math.pi, 6)[:-1]
        vals = list(V[si]) + [V[si][0]]
        ax.plot(np.append(ang, ang[0]), vals, color="#2a9d8f", lw=1.6)
        ax.fill(np.append(ang, ang[0]), vals, color="#2a9d8f", alpha=0.25)
        ax.set_ylim(0, 1); ax.set_xticks(ang)
        ax.set_xticklabels(["词","MLU","类","句","代"], color=DIM, fontsize=7.5)
        ax.set_yticks([0.5, 1.0]); ax.set_yticklabels([])
        ax.tick_params(length=0)
        ax.grid(color="#d6e0dd", lw=0.6)
        ax.spines["polar"].set_color("#d6e0dd")
        ax.set_title(f"{SLICES[si]}月", color=INK, fontsize=9.5, pad=2)
    save(fig, "var-E-radar.png")


def var_F(V):
    fig = _frame(title="F · 趋势折线（五线跨月）")
    ax = fig.add_axes([0.07, 0.16, 0.88, 0.70]); ax.set_facecolor(BG)
    for sp in ax.spines.values():
        sp.set_color("#d6e0dd")
    for mi in range(5):
        ax.plot(XS, V[:, mi], color=COLORS[mi], lw=2.2, marker="o", ms=4, label=METRICS[mi])
    ax.set_xticks(XS); ax.set_xticklabels([str(m) for m in SLICES], color=INK, fontsize=10.5)
    ax.set_ylim(0, 1.05); ax.set_yticks([0, .5, 1.0])
    ax.tick_params(colors=DIM, length=0)
    ax.grid(color="#e6ebe9", lw=0.7)
    ax.legend(loc="lower right", frameon=False, fontsize=9.5, labelcolor=INK)
    ax.set_xlabel("月龄", color=DIM, fontsize=10)
    save(fig, "var-F-lines.png")


def contact_sheet():
    names = ["var-A-circles.png", "var-B-iso-bars.png", "var-C-pillars.png",
             "var-D-heatmap.png", "var-E-radar.png", "var-F-lines.png"]
    ims = [Image.open(os.path.join(OUT, n)).convert("RGB") for n in names]
    w = 900
    ims = [im.resize((w, int(im.height * w / im.width))) for im in ims]
    hh = max(im.height for im in ims)
    gap = 16
    W = w * 2 + gap * 3
    H = hh * 3 + gap * 4
    sheet = Image.new("RGB", (W, H), (10, 12, 15))
    for i, im in enumerate(ims):
        r, c = i // 2, i % 2
        sheet.paste(im, (gap + c * (w + gap), gap + r * (hh + gap)))
    sheet.save(os.path.join(OUT, "compare.png"))
    print("   compare.png", sheet.size)


def main():
    V = collect()
    print("明暗/高度矩阵（norm）:\n", np.round(V, 2))
    for fn in (var_A, var_B, var_C, var_D, var_E, var_F):
        fn(V)
    contact_sheet()
    print("→", OUT)
    print("CHILD_DEV_VARIANTS_DONE")


if __name__ == "__main__":
    main()
