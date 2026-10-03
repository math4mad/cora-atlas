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
DIMS = ["词汇量·Wordbank", "平均句长 MLU", "词类多样性", "句法复杂度", "指代清晰度"]
# Wordbank 常模（English American, production 中位；CDI 止于 30）
WORDBANK_EN = {12: 4, 18: 52, 24: 256, 30: 492, 36: None}
WORDBANK_ZH = {12: None, 18: 172, 24: 622, 30: 750, 36: None}   # 普通话(北京) WS
WB_MAX = 750                                                   # 英/中同标度
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
                verb=0, noun=0, pron=0, gra=0, noun_tot=0, det_noun=0) for _ in SLICES]
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
                    for k, p in enumerate(P):                 # 有定标记：det + noun
                        if p in NOUN:
                            r["noun_tot"] += 1
                            if k > 0 and P[k - 1] == "det":
                                r["det_noun"] += 1
                if j < len(lines) and lines[j].startswith("%gra:"):
                    r["gra"] += gra_edges(lines[j])

    # 逐维原始值（每 bin）
    vals = {d: [] for d in DIMS}
    vals_zh = []
    cumtypes = set()
    for b in range(5):
        r = acc[b]
        u = max(r["utt"], 1)
        cumtypes |= r["types"]
        # 词汇量 → Wordbank 常模（英/中双柱；本地累计词型另存作对照）
        vals["词汇量·Wordbank"].append(WORDBANK_EN[SLICES[b]])
        vals_zh.append(WORDBANK_ZH[SLICES[b]])
        vals["平均句长 MLU"].append(r["len"] / u)
        tot = sum(r["pos"].values()) or 1              # 词类多样性 ＝ POS 熵（nats）
        vals["词类多样性"].append(-sum(c / tot * math.log(c / tot) for c in r["pos"].values()))
        vals["句法复杂度"].append(r["gra"] / u)          # 每话轮依存边数
        # 指代清晰度 → 有定标记率 = det+noun / noun（正向代理）
        vals["指代清晰度"].append(r["det_noun"] / max(r["noun_tot"], 1))

    # 归一化到本行 max（柱高＝掌握度/频率的相对高度；Wordbank 行的 None 不参与）
    norm = {}
    for d in DIMS:
        v = np.array([x if x is not None else np.nan for x in vals[d]], float)
        if d.startswith("词汇量"):
            mx = WB_MAX                                    # 英/中同标度
        else:
            mx = np.nanmax(v) if np.any(~np.isnan(v)) and np.nanmax(v) > 0 else 1.0
        norm[d] = v / mx
        print(f"[{d}] raw={np.round(v,3)}  norm={np.round(v/mx,3)}")
    norm_zh = np.array([x if x is not None else np.nan for x in vals_zh], float) / WB_MAX

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
            if ri == 0:                               # 词汇量行：英（绿）/ 中（橙）双柱
                ev, zv = norm[d][ci], norm_zh[ci]
                if not np.isnan(ev):
                    h = float(ev) * 0.86
                    ax.add_patch(Rectangle((ci - 0.30, ybase + 0.06), 0.25, h, facecolor=COLS[0],
                                           edgecolor="white", lw=0.7, alpha=0.93, zorder=3))
                    ax.text(ci - 0.175, ybase + 0.06 + h + 0.03, f"英 {vals[d][ci]:,.0f}",
                            color=DIM, fontsize=7.2, ha="center", va="bottom", zorder=4)
                if not np.isnan(zv):
                    h = float(zv) * 0.86
                    ax.add_patch(Rectangle((ci + 0.05, ybase + 0.06), 0.25, h, facecolor="#e08a3c",
                                           edgecolor="white", lw=0.7, alpha=0.93, zorder=3))
                    ax.text(ci + 0.175, ybase + 0.06 + h + 0.03, f"中 {vals_zh[ci]:,.0f}",
                            color=DIM, fontsize=7.2, ha="center", va="bottom", zorder=4)
                if np.isnan(ev) and np.isnan(zv):
                    ax.add_patch(Rectangle((ci - 0.27, ybase + 0.06), 0.54, 0.10, facecolor="none",
                                           edgecolor=COLS[0], lw=1.2, hatch="///", alpha=0.7, zorder=3))
                    ax.text(ci, ybase + 0.20, "CDI 止", color=DIM, fontsize=8, ha="center")
                continue
            nv = norm[d][ci]
            if np.isnan(nv):                          # Wordbank 无值（CDI 止于 30）
                ax.add_patch(Rectangle((ci - 0.27, ybase + 0.06), 0.54, 0.10,
                                       facecolor="none", edgecolor=COLS[ri], lw=1.2,
                                       hatch="///", alpha=0.7, zorder=3))
                ax.text(ci, ybase + 0.20, "CDI 止", color=DIM, fontsize=8, ha="center")
                continue
            h = float(nv) * 0.86
            ax.add_patch(Rectangle((ci - 0.27, ybase + 0.06), 0.54, h,
                                   facecolor=COLS[ri], edgecolor="white", lw=0.8,
                                   alpha=0.92, zorder=3))
            ax.text(ci, ybase + 0.06 + h + 0.05, f"{nv:.2f}", color=DIM,
                    fontsize=8.5, ha="center", va="bottom", zorder=4)

    for ri, d in enumerate(DIMS):
        ybase = (4 - ri)
        ax.text(-0.72, ybase + 0.5, d, color=INK, fontsize=13.0, ha="right", va="center")
        raw = vals[d]
        if d.startswith("词汇量"):
            txt = "  ".join("—" if v is None else f"{v:,.0f}" for v in raw)
        else:
            txt = "  ".join("—" if v is None else f"{v:.2f}" for v in raw)
        ax.text(-0.72, ybase + 0.24, txt, color=DIM, fontsize=8.2, ha="right", va="center")

    fig.text(0.045, 0.068,
             "英（绿）＝Wordbank English American · 中（橙）＝Wordbank 普通话（北京）WS —— 同标度（max 750）；"
             "其余四维＝本地 CHILDES。　横轴＝共享月龄切片（切片轴律）", color=DIM, fontsize=10)

    fig.text(0.045, 0.965, "儿童语言发育柱阵", color=INK, fontsize=26, fontweight="bold", va="top")
    fig.text(0.045, 0.925, "切片柱阵 Slice-Pillar Array · 五维 × 五月龄切片 · 柱高＝该维在该片的掌握度"
                           "（本行 max 归一）", color=DIM, fontsize=12.5, va="top")
    fig.text(0.045, 0.040,
             "数据：① 词汇量 ＝ Wordbank 常模（English American，production 中位；CDI 8–30 月，36 月无值）；"
             "② 其余四维 ＝ 本地 CHILDES Brown+Bernstein（CHI，%mor/%gra 直取，取 9–39 月入片）。",
             color=DIM, fontsize=9.5)
    fig.text(0.045, 0.018,
             "指代清晰度 ＝ 有定标记率（det+noun / noun，正向代理）· 12 月片 CHILDES 薄（n=3）· "
             f"母本 ima doc 7511883443609699 · 仅限研究非商业 · ver {VER} · lola",
             color=DIM, fontsize=9.5)

    for ext in ("png", "svg"):
        fig.savefig(os.path.join(OUT, f"child-language-pillar-zh.{ext}"), facecolor=BG)
    plt.close(fig)
    print("→", OUT)
    print("CHILD_PILLAR_DONE")


if __name__ == "__main__":
    main()
