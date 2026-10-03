#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""fig_data_cube.py — 数据立方体 / Data Cube（时空数据立方体）真数据版

母本＝ima 笔记《数据立方体 / Data Cube》doc 7512032127513120：
  方法＝时空数据立方体（Spatio-temporal Data Cube）；视觉＝等轴测堆叠切片。
  读法＝时间做深度轴，每层 2D 切片＝一个时刻的横截面；结构＝实体 × 指标 × 时间。
  与园中「切片柱阵」同族（只差：扁平方块堆叠 vs 立起方柱）。

本例（真数据）：
  A · NBA 选秀时序：X＝球员（2003 届 8 人）Y＝指标（出场/攻/防/总/胜场贡献）Z＝赛季（2004→2013）
  B · 儿童语言发展：X＝儿童（本地 CHILDES 6 童）Y＝指标（词汇量/MLU/句法/话轮/新词率）Z＝月龄（12→42）

输出: docs/figs/data-cube/v01/data-cube-zh.{png,svg}
用法: .venv/bin/python scripts/fig_data_cube.py
"""
import os, re, glob, collections
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon
from matplotlib import cm

HERE = os.path.dirname(os.path.abspath(__file__))
D = os.path.dirname(HERE)
VER = os.environ.get("VER", "v01")
OUT = os.path.join(D, "docs", "figs", "data-cube", VER)
os.makedirs(OUT, exist_ok=True)
CHAT = "/Users/mac/Programming/code-2026/Concept-Space-Sphere/corpus/ladder05/layers/childes/chat"
matplotlib.rcParams["font.family"] = ["Hiragino Sans GB", "Arial Unicode MS", "sans-serif"]
matplotlib.rcParams["axes.unicode_minus"] = False

BG = "#0e1015"; INK = "#e6e1d6"; DIM = "#8a8f9a"; EDGE = "#0e1015"


# ── 等轴测堆叠切片 ──────────────────────────────────────────────────
def draw_cube(ax, M, xlabels, ylabels, zlabels, cmap="viridis", o=(0.86, 0.60)):
    """M: [Z, X, Y] 数值；逐层（远→近）画方格阵列；色＝逐指标(min-max)归一。"""
    M = np.asarray(M, float)
    Z, NX, NY = M.shape
    lo = np.nanmin(M, axis=(0, 1)); hi = np.nanmax(M, axis=(0, 1))
    rng = np.where(hi - lo == 0, 1.0, hi - lo)
    norm = (M - lo) / rng
    cmo = plt.get_cmap(cmap)
    for k in range(Z - 1, -1, -1):                     # 远→近
        ox, oy = o[0] * k, o[1] * k
        # 切片底衬
        ax.add_patch(Polygon([(ox, oy), (ox + NX, oy), (ox + NX, oy + NY), (ox, oy + NY)],
                             closed=True, facecolor="#171b22", edgecolor="#3a4048",
                             lw=0.8, zorder=Z - k))
        for i in range(NX):
            for j in range(NY):
                v = norm[k, i, j]
                c = cmo(0.15 + 0.85 * (0 if np.isnan(v) else v))
                ax.add_patch(Polygon([(ox + i, oy + j), (ox + i + 0.94, oy + j),
                                      (ox + i + 0.94, oy + j + 0.94), (ox + i, oy + j + 0.94)],
                                     closed=True, facecolor=c, edgecolor=EDGE, lw=0.4,
                                     zorder=Z - k + 0.1))
        ax.text(ox - 0.12, oy + NY / 2, zlabels[k], color=INK, fontsize=7.8,
                ha="right", va="center", zorder=300,
                bbox=dict(boxstyle="round,pad=0.15", fc="#0e1015", ec="none", alpha=0.8))
    # 轴标签
    for i, xl in enumerate(xlabels):
        ax.text(i + 0.5, -0.30, xl, color=DIM, fontsize=6.8, ha="right", va="top",
                rotation=32, rotation_mode="anchor", zorder=300)
    for j, yl in enumerate(ylabels):
        ax.text(-0.25, j + 0.47, yl, color=DIM, fontsize=7.8, ha="right", va="center", zorder=300)


# ── 数据 A: NBA ────────────────────────────────────────────────────
def nba_cube():
    import csv as _csv
    P = ["LeBron James", "Dwyane Wade", "Chris Bosh", "Carmelo Anthony",
         "Chris Kaman", "Kirk Hinrich", "David West", "Josh Howard"]
    Mx = ["出场", "攻", "防", "总", "胜场"]
    cols = ["mp", "raptor_offense", "raptor_defense", "raptor_total", "war_total"]
    years = list(range(2004, 2014))
    data = {}
    with open(os.path.join(D, "data", "nba-raptor-by-player.csv")) as f:
        for r in _csv.DictReader(f):
            if r["player_name"] in P:
                try:
                    data[(r["player_name"], int(r["season"]))] = [float(r[c]) for c in cols]
                except Exception:
                    pass
    M = np.full((len(years), len(P), len(cols)), np.nan)
    for k, yr in enumerate(years):
        for i, p in enumerate(P):
            if (p, yr) in data:
                M[k, i, :] = data[(p, yr)]
    return M, ["LeBron", "Wade", "Bosh", "Melo", "Kaman", "Hinrich", "West", "Howard"], Mx, [str(y) for y in years]


# ── 数据 B: 儿童语言（本地 CHILDES）────────────────────────────────
def age_of(t):
    m = re.search(r'^@ID:\s*eng\|[^|]*\|CHI\|(\d+);(\d+)\.', t, re.M)
    return None if not m else int(m.group(1)) * 12 + int(m.group(2))


def child_of(t):
    m = re.search(r'^@ID:\s*eng\|([^|]*)\|CHI\|', t, re.M)
    return m.group(1) if m else None


def name_of(t):
    return None


def child_from_file(path):
    stem = os.path.basename(path)[:-4]
    toks = [t for t in re.split(r'[_\s]+', stem) if t and not t[0].isdigit()]
    skip = {"Brown", "Bernstein", "Children", "Interview", "cha"}
    toks = [t for t in toks if t not in skip]
    return toks[-1] if toks else None


def toks(line):
    o = []
    for r in line[5:].strip().split():
        x = r.lower(); x = re.sub(r'\(.*?\)', '', x).replace("'s", "").replace("'", "")
        x = re.sub(r'[^a-z]+', '', x)
        if x:
            o.append(x)
    return o


def child_cube():
    months = [12, 18, 24, 30, 36, 42]
    # 先按 (child,month-bin) 聚合
    acc = collections.defaultdict(lambda: dict(utt=0, len=0, types=set(), gra=0, newt=0, tok=0))
    childcount = collections.Counter()
    for f in sorted(glob.glob(os.path.join(CHAT, "*.cha"))):
        txt = open(f, encoding="utf-8", errors="ignore").read()
        a = age_of(txt); c = child_from_file(f)
        if a is None or c is None:
            continue
        b = min(range(len(months)), key=lambda i: abs(a - months[i]))
        if abs(a - months[b]) > 3:
            continue
        r = acc[(c, b)]; childcount[c] += 1
        lines = txt.splitlines()
        for i, ln in enumerate(lines):
            if not ln.startswith("*CHI:"):
                continue
            W = toks(ln)
            if not W:
                continue
            r["utt"] += 1; r["len"] += len(W); r["tok"] += len(W)
            before = set(r["types"]); r["types"].update(W)
            r["newt"] += len(r["types"] - before)
            for j in (i + 1, i + 2):
                if j < len(lines) and lines[j].startswith("%gra:"):
                    r["gra"] += sum(1 for t in lines[j].split(":", 1)[1].split() if t.count("|") >= 2)
    kids = [c for c, _ in childcount.most_common(6)]
    Mx = ["词汇量", "MLU", "句法", "话轮", "新词率"]
    M = np.full((len(months), len(kids), 5), np.nan)
    for bi in range(len(months)):
        for ki, c in enumerate(kids):
            r = acc.get((c, bi))
            if not r or r["utt"] == 0:
                continue
            M[bi, ki, 0] = len(r["types"])                    # 累计词型(该月片累计型数)
            M[bi, ki, 1] = r["len"] / r["utt"]                # MLU
            M[bi, ki, 2] = r["gra"] / r["utt"]                # 依存边/话轮
            M[bi, ki, 3] = r["utt"]                           # 话轮数
            M[bi, ki, 4] = r["newt"] / max(r["tok"], 1)       # 新词率
    return M, kids, Mx, [f"{m}" for m in months]


def main():
    M1, x1, y1, z1 = nba_cube()
    M2, x2, y2, z2 = child_cube()
    fig = plt.figure(figsize=(16, 8.6), dpi=110)
    fig.patch.set_facecolor(BG)
    fig.text(0.04, 0.965, "数据立方体 · Data Cube（时空数据立方体 · 等轴测堆叠切片）", color=INK,
             fontsize=23, fontweight="bold", va="top")
    fig.text(0.04, 0.925, "实体 × 指标 × 时间；时间做深度轴，每层切片＝一个时刻的横截面　"
                          "（与「切片柱阵」同族：方块堆叠 vs 立起方柱）", color=DIM, fontsize=12, va="top")

    axA = fig.add_axes([0.03, 0.10, 0.47, 0.76]); axA.set_facecolor(BG); axA.axis("off")
    axB = fig.add_axes([0.52, 0.10, 0.47, 0.76]); axB.set_facecolor(BG); axB.axis("off")

    for ax, M, xl, yl, zl, ttl in (
            (axA, M1, x1, y1, z1, "A · NBA 选秀球员时序（真数据 RAPTOR）　X=球员 · Y=指标 · Z=赛季"),
            (axB, M2, x2, y2, z2, "B · 儿童语言发展（真数据 CHILDES）　X=儿童 · Y=指标 · Z=月龄")):
        Z = M.shape[0]
        draw_cube(ax, M, xl, yl, zl)
        ax.set_xlim(-2.4, M.shape[1] + 0.72 * Z + 1.4)
        ax.set_ylim(-1.2, M.shape[2] + 0.52 * Z + 1.2)
        ax.set_title(ttl, color=INK, fontsize=12.5, pad=6)

    fig.text(0.04, 0.056,
             "读法：抽一层切片＝某赛季/某月龄的横截面（全员同现）；沿深度竖看＝单实体（球员/孩子）的轨迹；"
             "切片内色离散度＝同龄/同届个体差异。", color=INK, fontsize=11)
    fig.text(0.04, 0.028,
             "数据：A＝FiveThirtyEight RAPTOR by player (CC BY 4.0) · B＝本地 CHILDES Brown+Bernstein（CHI）· "
             "色＝各指标自身 min-max 归一（跨指标不同标度，勿横比）· 母本 ima doc 7512032127513120 · "
             f"ver {VER} · lola 2026-10-03", color=DIM, fontsize=9.2)

    for ext in ("png", "svg"):
        fig.savefig(os.path.join(OUT, f"data-cube-zh.{ext}"), facecolor=BG)
    plt.close(fig)
    print("→", OUT)
    print("DATA_CUBE_DONE")


if __name__ == "__main__":
    main()
