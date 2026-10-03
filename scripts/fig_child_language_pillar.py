#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""fig_child_language_pillar.py —「儿童语言发育柱阵」(切片柱阵 · 图1)

母本＝今晨 ima 笔记《切片柱阵·三图提示词（ima Copilot 图库）》doc 7511883443609699：
  · 视觉语法：纵向实体行（顶→底）＋ 共享横向切片轴 ＋ 立起方柱（柱高＝信号）
  · 图1 行（5 维）：词汇量 / 平均句长 MLU / 词类多样性 / 句法复杂度 / 指代清晰度
  · 横轴：月龄切片 12 · 18 · 24 · 30 · 36
  · 铁律②：切片怎么 bin，柱阵就讲什么故事 —— 本图 bin ＝ 月龄切片（±3 月）
数据：本地 CHILDES Brown + Bernstein（CHI 自身产出，带 %mor/%gra）；Wordbank 常模 †候补。
输出：docs/figs/child-language-pillar/v01/child-language-pillar-{zh,en}.{png,svg}
用法: .venv/bin/python scripts/fig_child_language_pillar.py
"""
import os, re, glob, collections, math
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

HERE = os.path.dirname(os.path.abspath(__file__))
D = os.path.dirname(HERE)
VER = os.environ.get("VER", "v01")
OUT = os.path.join(D, "docs", "figs", "child-language-pillar", VER)
os.makedirs(OUT, exist_ok=True)
CHAT = "/Users/mac/Programming/code-2026/Concept-Space-Sphere/corpus/ladder05/layers/childes/chat"

SLICES = [12, 18, 24, 30, 36]
DIMS = ["词汇量", "平均句长 MLU", "词类多样性", "句法复杂度", "指代清晰度"]
CONTENT = set("noun verb adj adv propn".split())
PRON = set("pron".split())
NOUN = set("noun propn".split())
MAT = matplotlib.rcParams
MAT["font.family"] = ["Hiragino Sans GB", "Arial Unicode MS", "sans-serif"]
MAT["axes.unicode_minus"] = False

BG = "#f4f7f6"; INK = "#1d2b2a"; DIM = "#6b7b79"; GRID = "#d6e0dd"
COLS = ["#2a9d8f", "#3aa79b", "#57b8ab", "#7dc9bd", "#a8dadc"]


def age(t):
    m = re.search(r'^@ID:\s*eng\|[^|]*\|CHI\|(\d+);(\d+)\.', t, re.M)
    return int(m.group(1)) * 12 + int(m.group(2)) if m else None


def binof(a):
    # 月龄切片 [9,15) [15,21) [21,27) [27,33) [33,39)；图外（≥39 或 <9）不取
    return None if (a < 9 or a >= 39) else int((a - 9) // 6)


def toks(line):
    o = []
    for r in line[5:].strip().split():
        x = r.lower(); x = re.sub(r'\(.*?\)', '', x).replace("'s", "").replace("'", "")
        x = re.sub(r'[^a-z]+', '', x)
        if x:
            o.append(x)
    return o


def mor_pos(line):
    out = []
    for t in line.split(":", 1)[1].strip().split():
        if "|" in t:
            out.append(t.split("|", 1)[0].lower())
    return out


def gra_edges(line):
    n = 0
    for t in line.split(":", 1)[1].strip().split():
        if t.count("|") >= 2:
            n += 1
    return n


def main():
    # per bin accumulators
    acc = [dict(tok=0, utt=0, len=0, types=set(), pos=collections.Counter(),
                verb=0, noun=0, pron=0, gra=0) for _ in SLICES]
    nsess = [0] * 5
    for f in sorted(glob.glob(os.path.join(CHAT, "*.cha"))):
        txt = open(f, encoding="utf-8", errors="ignore").read()
        a = age(txt)
        if a is None:
            continue
        b = binof(a)
        if b is None:
            continue
        nsess[b] += 1
        lines = txt.splitlines()
        for i, line in enumerate(lines):
            if not line.startswith("*CHI:"):
                continue
            W = toks(line)
            r = acc[b]
            if W:
                r["utt"] += 1; r["len"] += len(W); r["tok"] += len(W)
                r["types"].update(W)
            # 紧跟的 %mor / %gra
            for j in (i + 1, i + 2):
                if j < len(lines) and lines[j].startswith("%mor:"):
                    P = mor_pos(lines[j])
                    r["pos"].update(P)
                    r["verb"] += sum(1 for p in P if p == "verb")
                    r["noun"] += sum(1 for p in P if p in NOUN)
                    r["pron"] += sum(1 for p in P if p in PRON)
                if j < len(lines) and lines[j].startswith("%gra:"):
                    r["gra"] += gra_edges(lines[j])

    # 逐维原始值（每 bin）
    vals = {d: [] for d in DIMS}
    cumtypes = set()
    for b in range(5):
        r = acc[b]
        u = max(r["utt"], 1)
        cumtypes |= r["types"]
        vals["词汇量"].append(len(cumtypes))            # 累计词汇量（单调爬坡）
        vals["平均句长 MLU"].append(r["len"] / u)
        tot = sum(r["pos"].values()) or 1              # 词类多样性 ＝ POS 熵（nats）
        vals["词类多样性"].append(-sum(c / tot * math.log(c / tot) for c in r["pos"].values()))
        vals["句法复杂度"].append(r["gra"] / u)          # 每话轮依存边数
        denom = r["noun"] + r["pron"]                    # 指代清晰度 ＝ 显名率
        vals["指代清晰度"].append(r["noun"] / denom if denom else 0.0)

    # 归一化到本行 max（柱高＝掌握度/频率的相对高度）
    norm = {}
    for d in DIMS:
        v = np.array(vals[d], float)
        mx = v.max() if v.max() > 0 else 1.0
        norm[d] = v / mx
        print(f"[{d}] raw={np.round(v,3)}  norm={np.round(v/mx,3)}")

    # ── 画 ─────────────────────────────────────────────
    fig = plt.figure(figsize=(13.5, 8.6), dpi=110)
    fig.patch.set_facecolor(BG)
    ax = fig.add_axes([0.135, 0.115, 0.83, 0.755])
    ax.set_facecolor(BG)
    for sp in ax.spines.values():
        sp.set_visible(False)
    ax.set_xlim(-0.6, 4.6); ax.set_ylim(-0.15, 5.35)
    ax.set_xticks(range(5)); ax.set_xticklabels([f"{m}" for m in SLICES], color=INK, fontsize=13)
    ax.set_yticks([])
    ax.tick_params(length=0)
    for x in range(5):
        ax.plot([x, x], [0, 5], color=GRID, lw=0.8, zorder=0)
    for y in range(6):
        ax.plot([-0.55, 4.55], [y, y], color=GRID, lw=0.8, zorder=0)

    for ri, d in enumerate(DIMS):
        ybase = (4 - ri)          # 顶行(词汇量)在最上
        for ci in range(5):
            h = float(norm[d][ci]) * 0.86
            ax.add_patch(Rectangle((ci - 0.27, ybase + 0.06), 0.54, h,
                                   facecolor=COLS[ri], edgecolor="white", lw=0.8,
                                   alpha=0.92, zorder=3))
            ax.text(ci, ybase + 0.06 + h + 0.05, f"{norm[d][ci]:.2f}", color=DIM,
                    fontsize=8.5, ha="center", va="bottom", zorder=4)

    for ri, d in enumerate(DIMS):
        ybase = (4 - ri)
        ax.text(-0.72, ybase + 0.5, d, color=INK, fontsize=13.5, ha="right", va="center")
        raw = vals[d]
        fmt = (lambda v: f"{v:,.0f}") if d == "词汇量" else (lambda v: f"{v:.2f}")
        ax.text(-0.72, ybase + 0.24, "  ".join(fmt(v) for v in raw), color=DIM,
                fontsize=8.2, ha="right", va="center")

    fig.text(0.045, 0.068,
             "横轴 · 月龄切片（±3 月）＝ 共享切片轴　——　切片轴律：怎么 bin，柱阵就讲什么故事",
             color=DIM, fontsize=11)

    fig.text(0.045, 0.965, "儿童语言发育柱阵", color=INK, fontsize=26, fontweight="bold", va="top")
    fig.text(0.045, 0.925, "切片柱阵 Slice-Pillar Array · 五维 × 五月龄切片 · 柱高＝该维在该片的掌握度"
                           "（本行 max 归一）", color=DIM, fontsize=12.5, va="top")
    fig.text(0.045, 0.040,
             "数据：本地 CHILDES Brown + Bernstein（CHI 自身产出，真实月龄，%mor/%gra 直取）· "
             "语料 13–62 月 · 12 月片样本薄（n=3 会话）† · Wordbank 常模候补（母本笔记指定）。",
             color=DIM, fontsize=9.5)
    fig.text(0.045, 0.018,
             f"母本：ima 笔记《切片柱阵·三图提示词》doc 7511883443609699（2026-10-03）· "
             f"仅限研究·非商业 · ver {VER} · lola", color=DIM, fontsize=9.5)

    for ext in ("png", "svg"):
        fig.savefig(os.path.join(OUT, f"child-language-pillar-zh.{ext}"), facecolor=BG)
    plt.close(fig)
    print("→", OUT)
    print("CHILD_PILLAR_DONE")


if __name__ == "__main__":
    main()
