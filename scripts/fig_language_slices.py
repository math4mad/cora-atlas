#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""fig_language_slices.py —「语言版 · 总谱与剖面」(v01, 2.5D 版)

主人 1003 勘误后的定式：「不用年龄语义概念空间做时间线；**和 NBA 选秀那张图一样的语法**，
只不过变化的是**词、语法结构、逻辑**」；主人圈定「**三刀＝三阶段**」。

照 NBA 图的语法搬：
  本体（长条）＝语言发展的**长河**（CHILDES 13→62 月，全池）
  三道刀口    ＝**三个阶段**：单词期 13–23 月 / 句法期 24–43 月 / 逻辑期 44–62 月
  格内容      ＝该阶段的**词**（高频实词，明暗∝频次）—— 即 NBA 图里的"面孔"
  **同形不同物**＝三片切面形状一样，但填进去的词全不同；且 MLU（语法）与连接词率（逻辑）逐阶抬升。

数据：CHILDES Brown+Bernstein（CHI 自身产出，清洗转写噪声）。真三维版（Blender）候认。
用法: .venv/bin/python scripts/fig_language_slices.py
"""
import os, re, glob, collections
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon

D = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
VER = os.environ.get("VER", "v01-2d5")
OUT = os.path.join(D, "docs", "figs", "language-slices", VER)
os.makedirs(OUT, exist_ok=True)
CHAT = "/Users/mac/Programming/code-2026/Concept-Space-Sphere/corpus/ladder05/layers/childes/chat"

BG = "#0b0c10"; GOLD = "#e7c36f"; SLATE = "#8d93a3"; DIM = "#5f6673"; INK = "#ded9cc"
STAGES = [("单词期", 13, 23), ("句法期", 24, 43), ("逻辑期", 44, 62)]
CONN = set("because if so then but when why how and or what where who which before after".split())
ARTI = set("""xxx yyy zzz res dat dis dere huh mm hm uh oh ah er um imit gonn goin gonna
 yeah yep nope dont cant wont doesnt isnt wasnt didnt aint alotof ooh hey whoa""".split())
STOP = set("""a an the and or to of in on at by for with from up down out off over under
it its is are was were be been am do does did have has had can could will would
i you he she we they me him her us them my your his mine yours ours their theirs
this that these those there here what who why how when where as also just now only well
no yes not too very one two three go going gone get got put see look want know think say
said like make made come came back again mommy daddy mom mama dada""".split())
COLS, ROWS = 4, 6          # 每片 24 格


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
    wf = [collections.Counter() for _ in STAGES]
    uttlen = [[] for _ in STAGES]; conn = [0] * 3; nutt = [0] * 3; nsess = [0] * 3
    tot = [0] * 3
    for f in sorted(glob.glob(os.path.join(CHAT, "*.cha"))):
        txt = open(f, encoding="utf-8", errors="ignore").read()
        a = age(txt)
        if a is None:
            continue
        s = next((i for i, (n, lo, hi) in enumerate(STAGES) if lo <= a <= hi), None)
        if s is None:
            continue
        nsess[s] += 1
        for line in txt.splitlines():
            if not line.startswith("*CHI:"):
                continue
            W = toks(line)
            if not W:
                continue
            nutt[s] += 1; uttlen[s].append(len(W)); tot[s] += len(W)
            wf[s].update(W)
            if any(w in CONN for w in W):
                conn[s] += 1
    words = []
    for s in range(3):
        cand = [w for w, c in wf[s].most_common(200)
                if w not in STOP and w not in ARTI and len(w) >= 3 and c >= 4]
        seen, pick = set(), []
        for w in cand:
            if w in seen:
                continue
            seen.add(w); pick.append((w, wf[s][w]))
            if len(pick) >= COLS * ROWS:
                break
        words.append(pick)
    stats = [dict(sess=nsess[s], utt=nutt[s], tok=tot[s],
                  mlu=sum(uttlen[s]) / max(1, len(uttlen[s])),
                  conn=100 * conn[s] / max(1, nutt[s])) for s in range(3)]
    return words, stats


def bilin(corners, s, t):
    TL, TR, BR, BL = corners
    return ((1 - s) * (1 - t) * np.array(TL) + s * (1 - t) * np.array(TR)
            + s * t * np.array(BR) + (1 - s) * t * np.array(BL))


def panel(cx, cy, wv, hv):
    return [np.array(cx - wv[0] - hv[0], float), np.array(cx + wv[0] - hv[0]),
            np.array(cx + wv[0] + hv[0]), np.array(cx - wv[0] + hv[0])] \
        if False else [
        (cx - wv[0] - hv[0], cy - wv[1] - hv[1]),
        (cx + wv[0] - hv[0], cy + wv[1] - hv[1]),
        (cx + wv[0] + hv[0], cy + wv[1] + hv[1]),
        (cx - wv[0] + hv[0], cy - wv[1] + hv[1])]


def main():
    words, stats = collect()
    matplotlib.rcParams["font.family"] = ["Hiragino Sans GB", "Arial Unicode MS", "sans-serif"]
    fig = plt.figure(figsize=(16, 10), dpi=100)
    fig.patch.set_facecolor(BG)
    ax = fig.add_axes([0, 0, 1, 1]); ax.set_xlim(0, 1); ax.set_ylim(0, 1)
    ax.axis("off")

    fig.text(0.045, 0.955, "语言 · 总谱与剖面 · 三道刀口", color=GOLD,
             fontsize=27, fontweight="bold", va="top")
    fig.text(0.045, 0.912, "本体＝儿童语言发展长河（CHILDES 13→62 月）· 三道刀口＝三阶段 · "
                           "格＝该阶段的词（明暗∝频次）· 同形不同物：三片一样，词与句法/逻辑全不同",
             color=SLATE, fontsize=12.5, va="top")

    P = [panel(0.250, 0.480, (0.132, 0.058), (-0.010, 0.240)),
         panel(0.545, 0.512, (0.101, 0.045), (-0.008, 0.187)),
         panel(0.800, 0.545, (0.076, 0.034), (-0.006, 0.142))]

    # 本体（长条）：连接首末片对应角的箱体剪影
    body = [P[0][0], P[0][1], P[2][1], P[2][2], P[2][3], P[0][3]]
    ax.add_patch(Polygon(body, closed=True, facecolor="#12141b", edgecolor="#23262f",
                         alpha=0.75, lw=1.2, zorder=0))
    # 四条长棱线
    for k in range(4):
        ax.plot([P[0][k][0], P[2][k][0]], [P[0][k][1], P[2][k][1]],
                color="#333845", lw=0.9, zorder=1)

    for i, (panelc, (name, lo, hi), wl) in enumerate(zip(P, STAGES, words)):
        ax.add_patch(Polygon(panelc, closed=True, facecolor="#e7c36f", alpha=0.10,
                             edgecolor="#f0d78c", lw=2.0, zorder=2))
        wx = max((c for w, c in wl), default=1)
        for idx, (w, c) in enumerate(wl):
            col, row = idx % COLS, idx // COLS
            s = (col + 0.5) / COLS
            t = (row + 0.5) / ROWS
            px, py = bilin(panelc, s, t)
            bw = c / wx
            size = 12.0 if i == 0 else (10.5 if i == 1 else 9.0)
            ax.text(px, py, w, color=(1, 1, 1, 0.30 + 0.70 * bw), fontsize=size,
                    ha="center", va="center", zorder=3, fontfamily="Arial",
                    fontweight="bold" if bw > 0.55 else "normal")
        # 片名 + 统计（面板正下方居中，避让词格）
        bx = sum(p[0] for p in panelc) / 4
        bot = min(p[1] for p in panelc)
        cy0 = bot - 0.026
        ax.text(bx, cy0, name, color=GOLD, fontsize=16, ha="center", va="top",
                fontweight="bold")
        st = stats[i]
        ax.text(bx, cy0 - 0.032,
                f"{lo}–{hi} 月 · {st['tok']:,} 词 · MLU {st['mlu']:.2f} · 连接词 {st['conn']:.1f}%",
                color=SLATE, fontsize=10.5, ha="center", va="top")

    ax.plot([0.045, 0.955], [0.115, 0.115], color="#2a2d36", lw=1)
    fig.text(0.045, 0.072,
             "读：三片切面**形状一样**（同形），填进去的**词**全不同（不同物）——语言长河在等形的剖面里，"
             "词在换、句法在长（MLU 2.76→2.99→4.13）、逻辑在接（连接词 4.1%→12.3%→18.2%）。",
             color=SLATE, fontsize=11.5)
    fig.text(0.045, 0.045,
             "诚实：此为 2.5D 版（快速站位，候勘）；词＝各阶段高频实词（清转写噪声）。"
             "真三维版（Blender，与 NBA 图同管线）候认；垂直与密度/词表口径候主人定。",
             color=DIM, fontsize=11)
    fig.text(0.045, 0.020,
             f"source: CHILDES Brown+Bernstein 264 会话 (CHI only) · ver {VER} · lola 2026-10-03",
             color=DIM, fontsize=9.5)

    fig.savefig(os.path.join(OUT, "language-slices.png"), facecolor=BG)
    fig.savefig(os.path.join(OUT, "language-slices.svg"), facecolor=BG)
    plt.close(fig)
    for i, (n, lo, hi) in enumerate(STAGES):
        print(f"[{n}] " + " · ".join(w for w, c in words[i]))
    print("→", OUT)
    print("LANG_SLICES_DONE")


if __name__ == "__main__":
    main()
