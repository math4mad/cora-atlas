#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""fig_child_dev_slices.py — 儿童发展 · 切片柱阵（模仿 NBA 选秀切片柱；长轴＝时间）

主人 1003 令：儿童发展仿 NBA 选秀「切片柱」，**长轴为时间**；每个切片里的
词汇量 · MLU · 词类多样性 · 句法复杂度 · 指代清晰度 用——
  方案一：**大小不同的圆**表示；
  方案二：**45° 视角**，每片为**三维柱状图**（5 指标高矮不同）。

数据：本地 CHILDES Brown+Bernstein（CHI，%mor/%gra 直取）；月龄切片 12/18/24/30/36/42（±3）。
输出：docs/figs/child-dev-slices/v01/child-dev-slices-zh.{png,svg}
用法: .venv/bin/python scripts/fig_child_dev_slices.py
"""
import os, re, glob, collections, math
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, Polygon

D = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
VER = os.environ.get("VER", "v01")
OUT = os.path.join(D, "docs", "figs", "child-dev-slices", VER)
os.makedirs(OUT, exist_ok=True)
CHAT = "/Users/mac/Programming/code-2026/Concept-Space-Sphere/corpus/ladder05/layers/childes/chat"
matplotlib.rcParams["font.family"] = ["Hiragino Sans GB", "Arial Unicode MS", "sans-serif"]
matplotlib.rcParams["axes.unicode_minus"] = False

BG = "#f5f7f6"; INK = "#1d2b2a"; DIM = "#6b7b79"; GRID = "#d6e0dd"
SLICES = [12, 18, 24, 30, 36, 42]
METRICS = ["词汇量", "MLU", "词类多样性", "句法复杂度", "指代清晰度"]
COLORS = ["#2a9d8f", "#3f7fb3", "#8a6fb0", "#d98a3c", "#c05b5b"]
NOUN = set("noun propn".split()); PRON = set("pron".split())


def age(t):
    m = re.search(r'^@ID:\s*eng\|[^|]*\|CHI\|(\d+);(\d+)\.', t, re.M)
    return int(m.group(1)) * 12 + int(m.group(2)) if m else None


def toks(line):
    o = []
    for r in line[5:].strip().split():
        x = r.lower(); x = re.sub(r'\(.*?\)', '', x).replace("'s", "").replace("'", "")
        x = re.sub(r'[^a-z]+', '', x)
        if x:
            o.append(x)
    return o


def collect():
    acc = [dict(utt=0, ln=0, types=set(), pos=collections.Counter(),
                gra=0, nt=0, dn=0) for _ in SLICES]
    for f in sorted(glob.glob(os.path.join(CHAT, "*.cha"))):
        txt = open(f, encoding="utf-8", errors="ignore").read()
        a = age(txt)
        if a is None:
            continue
        b = min(range(len(SLICES)), key=lambda i: abs(a - SLICES[i]))
        if abs(a - SLICES[b]) > 3:
            continue
        r = acc[b]; lines = txt.splitlines()
        for i, ln in enumerate(lines):
            if not ln.startswith("*CHI:"):
                continue
            W = toks(ln)
            if not W:
                continue
            r["utt"] += 1; r["ln"] += len(W); r["types"].update(W)
            for j in (i + 1, i + 2):
                if j < len(lines) and lines[j].startswith("%mor:"):
                    P = [t.split("|", 1)[0].lower() for t in lines[j].split(":", 1)[1].split() if "|" in t]
                    r["pos"].update(P)
                    for k, p in enumerate(P):
                        if p in NOUN:
                            r["nt"] += 1
                            if k > 0 and P[k - 1] == "det":
                                r["dn"] += 1
                if j < len(lines) and lines[j].startswith("%gra:"):
                    r["gra"] += sum(1 for t in lines[j].split(":", 1)[1].split() if t.count("|") >= 2)
    V = np.zeros((len(SLICES), len(METRICS)))
    cum = set()
    for b, r in enumerate(acc):
        u = max(r["utt"], 1)
        cum |= r["types"]
        V[b, 0] = len(cum)
        V[b, 1] = r["ln"] / u
        tot = sum(r["pos"].values()) or 1
        V[b, 2] = -sum(c / tot * math.log(c / tot) for c in r["pos"].values())
        V[b, 3] = r["gra"] / u
        V[b, 4] = r["dn"] / max(r["nt"], 1)
    Vn = V / np.where(V.max(0) == 0, 1, V.max(0))
    np.set_printoptions(precision=2, suppress=True)
    print("raw:\n", V)
    print("norm:\n", Vn)
    return Vn


def iso_bar(ax, x0, y0, h, col, w=0.5, d=(0.34, 0.20), z=3):
    """45° 视角的方柱：底面(x0,y0) 宽 w，高 h，退向 d。"""
    f = [(x0, y0), (x0 + w, y0), (x0 + w, y0 + h), (x0, y0 + h)]                # 正面
    r = [(x0 + w, y0), (x0 + w + d[0], y0 + d[1]), (x0 + w + d[0], y0 + d[1] + h),
         (x0 + w, y0 + h)]                                                     # 右面
    t = [(x0, y0 + h), (x0 + w, y0 + h), (x0 + w + d[0], y0 + d[1] + h),
         (x0 + d[0], y0 + d[1] + h)]                                           # 顶面
    ax.add_patch(Polygon(r, closed=True, facecolor=_shade(col, 0.72), edgecolor="white", lw=0.5, zorder=z))
    ax.add_patch(Polygon(t, closed=True, facecolor=_shade(col, 1.15), edgecolor="white", lw=0.5, zorder=z + 0.01))
    ax.add_patch(Polygon(f, closed=True, facecolor=col, edgecolor="white", lw=0.6, zorder=z + 0.02))


def _shade(hexc, f):
    hexc = hexc.lstrip("#"); r, g, b = (int(hexc[i:i + 2], 16) for i in (0, 2, 4))
    cl = lambda v: max(0, min(255, int(v * f)))
    return f"#{cl(r):02x}{cl(g):02x}{cl(b):02x}"


def main():
    V = collect()
    fig = plt.figure(figsize=(15.5, 10.4), dpi=110)
    fig.patch.set_facecolor(BG)
    fig.text(0.04, 0.97, "儿童发展 · 切片柱阵（长轴＝时间）", color=INK, fontsize=24,
             fontweight="bold", va="top")
    fig.text(0.04, 0.935, "仿 NBA 选秀切片柱 · 月龄切片 12→42 · 五指标：词汇量 · MLU · 词类多样性 · "
                          "句法复杂度 · 指代清晰度（各指标自身 max 归一）", color=DIM, fontsize=12, va="top")

    xs = list(range(len(SLICES)))

    # ── 方案一 · 圆 ──────────────────────────────────────
    axA = fig.add_axes([0.06, 0.545, 0.90, 0.335]); axA.set_facecolor(BG)
    for sp in axA.spines.values():
        sp.set_visible(False)
    axA.set_xlim(-0.6, len(SLICES) - 0.4); axA.set_ylim(-0.7, 0.95)
    axA.set_xticks(xs); axA.set_xticklabels([str(m) for m in SLICES], color=INK, fontsize=11)
    axA.set_yticks([]); axA.tick_params(length=0)
    # 方案一 · 五圆排布（3+2）
    OFF = [(0.0, 0.42), (-0.30, 0.06), (0.30, 0.06), (-0.16, -0.34), (0.16, -0.34)]
    for si, x in enumerate(xs):
        for mi in range(5):
            v = V[si, mi]
            r = 0.05 + 0.16 * math.sqrt(v)
            ox, oy = OFF[mi]
            axA.add_patch(Circle((x + ox, oy), r, facecolor=COLORS[mi], edgecolor="white",
                                 lw=1.0, alpha=0.9, zorder=3))
            axA.text(x + ox, oy, f"{v:.2f}", color="white", fontsize=6.6, ha="center",
                     va="center", zorder=4)
    axA.set_title("方案一 · 每片五指标＝大小不同的圆（面积 ∝ 值）", color=INK, fontsize=13, pad=6)
    for mi, m in enumerate(METRICS):
        axA.add_patch(Circle((0.97, 0.86 - mi * 0.001), 0.0001, facecolor=COLORS[mi]))  # 占位
    fig.text(0.965, 0.868, " · ".join(METRICS), color=DIM, fontsize=9, ha="right")

    # ── 方案二 · 45° 三维柱 ──────────────────────────────
    axB = fig.add_axes([0.06, 0.115, 0.90, 0.36]); axB.set_facecolor(BG)
    for sp in axB.spines.values():
        sp.set_visible(False)
    axB.set_xlim(-0.8, len(SLICES) - 0.2); axB.set_ylim(-0.95, 1.45)
    axB.set_xticks(xs); axB.set_xticklabels([str(m) for m in SLICES], color=INK, fontsize=12)
    axB.set_yticks([]); axB.tick_params(length=0)
    # 每片：5 株一排，45° 退向；地板划出切片
    BARW, GAP, DX, DY = 0.150, 0.180, 0.115, 0.075
    for si, x in enumerate(xs):
        bx = x - 0.44
        fl = [(bx - 0.05, -0.60), (bx - 0.05 + 4 * GAP + BARW, -0.60),
              (bx - 0.05 + 4 * GAP + BARW + DX, -0.60 + DY), (bx - 0.05 + DX, -0.60 + DY)]
        axB.add_patch(Polygon(fl, closed=True, facecolor="#e7ecea", edgecolor="#cfd8d5",
                              lw=0.6, zorder=1))
        for mi in range(5):
            h = 0.08 + 1.05 * V[si, mi]
            iso_bar(axB, bx + mi * GAP, -0.58, h, COLORS[mi], w=BARW, d=(DX, DY),
                    z=3 + si * 0.5 + mi * 0.05)
    axB.set_title("方案二 · 每片＝45° 三维柱状图（五指标高矮不同）", color=INK, fontsize=13, pad=6)

    fig.text(0.04, 0.058,
             "读：长轴＝时间（月龄）；每片＝该月龄五指标的横截面。方案一看「大小」、方案二看「高低」；"
             "各指标自身 max 归一到同一高度域。", color=INK, fontsize=11)
    fig.text(0.04, 0.03,
             "数据：本地 CHILDES Brown+Bernstein（CHI，%mor/%gra 直取）· 12 月片样本薄 † · "
             f"母本＝主人 1003 口述（仿 NBA 选秀切片柱）· ver {VER} · lola 2026-10-03", color=DIM, fontsize=9.2)

    for ext in ("png", "svg"):
        fig.savefig(os.path.join(OUT, f"child-dev-slices-zh.{ext}"), facecolor=BG)
    plt.close(fig)
    print("→", OUT)
    print("CHILD_DEV_SLICES_DONE")


if __name__ == "__main__":
    main()
