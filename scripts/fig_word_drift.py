#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""fig_word_drift.py — 「儿童语义 · 词义漂移 · 近邻时间线」(v01)

承 `corpus/ladder05/analysis/word_drift/` 的探针链（v3 分布语义近邻成器）。
每词一行、四龄段四列；**同一近邻若跨龄留下，就以线相连**（留者金、过客灰）。
诚实条款：此图是**定性**读数（v4 跨龄对齐弱，定量「轴转动」尚不可测，见 README）。

用法: .venv/bin/python scripts/fig_word_drift.py
"""
import os, sys, glob, collections
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

WD = "/Users/mac/Programming/code-2026/Concept-Space-Sphere/corpus/ladder05/analysis/word_drift"
sys.path.insert(0, WD)
from drift4_space import (build_band, svd_embed, utt_tokens, age, band_of,
                          BANDS, BANDLAB, CHAT, cos)          # noqa: E402
from drift5_report import NOISE                                # noqa: E402

D = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
VER = os.environ.get("VER", "v01-neighbors")
OUT = os.path.join(D, "docs", "figs", "word-drift", VER)
os.makedirs(OUT, exist_ok=True)

BG = "#0b0c10"
GOLD = "#e7c36f"
SLATE = "#8d93a3"
DIM = "#5f6673"
INK = "#d8d4c8"

# 词序（上→下）：锚词在上（稳），自然现象在下（漂/体裁）
WORDS = [("dog", "狗"), ("ball", "球"), ("car", "车"), ("milk", "奶"),
         ("tree", "树"), ("moon", "月亮")]
TOPK = 5

matplotlib.rcParams["font.family"] = ["Hiragino Sans GB", "Arial Unicode MS", "sans-serif"]
matplotlib.rcParams["axes.unicode_minus"] = False


def neighbors():
    bs = collections.defaultdict(list)
    for f in sorted(glob.glob(os.path.join(CHAT, "*.cha"))):
        txt = open(f, encoding="utf-8", errors="ignore").read()
        m = age(txt)
        if m is None:
            continue
        b = band_of(m)
        if b is None:
            continue
        utts = [[w for w in utt_tokens(l) if w not in NOISE]
                for l in txt.splitlines() if l.startswith("*CHI:")]
        utts = [u for u in utts if u]
        if utts:
            bs[b].append(utts)
    spaces, nsess = {}, {}
    for b in range(len(BANDS)):
        vocab, idx, ppmi, freq = build_band(bs[b])
        Z, _, _ = svd_embed(ppmi)
        spaces[b] = (vocab, idx, Z)
        nsess[b] = len(bs[b])
    top = {}
    for w, _ in WORDS:
        row = []
        for b in range(len(BANDS)):
            vocab, idx, Z = spaces[b]
            if w not in idx:
                row.append([])
                continue
            v = Z[idx[w]]
            sims = sorted(((u, cos(v, Z[i])) for u, i in idx.items() if u != w),
                          key=lambda x: -x[1])
            row.append([u for u, s in sims[:TOPK] if s > 0.15])
        top[w] = row
    return top, nsess


def draw():
    top, nsess = neighbors()
    fig = plt.figure(figsize=(16, 10.4), dpi=100)
    fig.patch.set_facecolor(BG)
    ax = fig.add_axes([0, 0, 1, 1]); ax.set_xlim(0, 1); ax.set_ylim(0, 1)
    ax.axis("off"); ax.set_facecolor(BG)

    fig.text(0.045, 0.975, "儿童语义 · 词义漂移 · 近邻时间线", color=GOLD,
             fontsize=25, fontweight="bold", va="top")
    fig.text(0.045, 0.938, "语料＝CHILDES Brown+Bernstein 264 会话（真实月龄）· 探针＝每龄段 "
                           "PPMI+SVD 分布语义空间 · 留者金线、过客灰字　【定性读数】",
             color=SLATE, fontsize=12.5, va="top")

    cx = [0.255, 0.475, 0.695, 0.915]
    top_y, bot_y = 0.835, 0.150
    nrow = len(WORDS)
    row_h = (top_y - bot_y) / nrow

    # 列头
    for j, b in enumerate(range(len(BANDS))):
        ax.text(cx[j], top_y + 0.030, BANDLAB[b] + " 月", color=INK, fontsize=13.5,
                ha="center", va="bottom", fontweight="bold")
        ax.text(cx[j], top_y + 0.012, f"{nsess[b]} 会话", color=DIM, fontsize=9.5,
                ha="center", va="bottom")

    for i, (w, zh) in enumerate(WORDS):
        yc = top_y - (i + 0.5) * row_h
        # 行底纹
        if i % 2 == 0:
            ax.add_patch(plt.Rectangle((0.02, yc - row_h / 2 + 0.006), 0.96, row_h - 0.012,
                                       facecolor="#12141b", edgecolor="none", zorder=0))
        ax.text(0.045, yc, w, color=GOLD, fontsize=17, fontweight="bold", va="center")
        ax.text(0.045, yc - 0.021, zh, color=SLATE, fontsize=12, va="center")

        cols = top[w]
        # 每列近邻的 y 位置
        pos = []
        for j, nbs in enumerate(cols):
            k = max(len(nbs), 1)
            span = min(row_h * 0.72, 0.017 * k)
            ys = np.linspace(yc + span / 2, yc - span / 2, k) if k > 1 else [yc]
            pos.append(list(zip(nbs, ys)))

        # 连接：同一字符串跨相邻列
        for j in range(len(BANDS) - 1):
            d = {u: y for u, y in pos[j]}
            for u, y2 in pos[j + 1]:
                if u in d:
                    ax.plot([cx[j] + 0.028, cx[j + 1] - 0.028], [d[u], y2],
                            color=GOLD, lw=1.4, alpha=0.85, zorder=1,
                            solid_capstyle="round")

        # 近邻文字
        for j, p in enumerate(pos):
            for u, y in p:
                ax.text(cx[j], y, u, color=INK, fontsize=12.2, ha="center", va="center",
                        zorder=2, fontfamily="Arial")

    # moon 行注（体裁折光）——置于末行下方空处，避让近邻栈
    ymoon = top_y - (nrow - 0.5) * row_h
    ax.text(0.985, bot_y - 0.052, "↑ 体裁折光：女巫书 / 收信书 / 海洋书",
            color="#c98b7a", fontsize=12, ha="right", va="center", style="italic")

    ax.plot([0.04, 0.96], [bot_y - 0.028, bot_y - 0.028], color="#2a2d36", lw=1)
    fig.text(0.045, 0.085,
             "判读：词义漂移＝「换邻居」。dog/ball 的邻居跨龄稳固（世界模型里动物/物件有定所）；"
             "car/milk/tree 的邻居逐龄专业化（玩具车→真车 / 物→流程 / 节日→生态）；",
             color=SLATE, fontsize=11.5)
    fig.text(0.045, 0.060,
             "moon 的邻居随书走——其「泛灵」是童书童谣的折光，非儿童本体论。"
             "此图为定性读数；定量「轴转动」须换弹药（zho Zhou3 纵向库），见 word_drift/README.md。",
             color=SLATE, fontsize=11.5)
    fig.text(0.045, 0.028,
             f"source: corpus/ladder05/layers/childes (CHI only, 清洗后) · 探针 v3/v4 "
             f"drift4_space.py · ver {VER} · lola 2026-10-03", color=DIM, fontsize=9.5)

    out = os.path.join(OUT, "word-drift-neighbors.png")
    fig.savefig(out, facecolor=BG)
    fig.savefig(os.path.join(OUT, "word-drift-neighbors.svg"), facecolor=BG)
    plt.close(fig)
    print("→", out)
    print("WORD_DRIFT_FIG_DONE")


if __name__ == "__main__":
    draw()
