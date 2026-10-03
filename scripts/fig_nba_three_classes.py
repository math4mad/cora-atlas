#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""fig_nba_three_classes.py — NBA 三届 · 实体数据立方体（Data Cube · 深度＝选秀届次）

承《数据立方体 / Data Cube》笔记之变体：「把深度换成选秀届次，看联盟球员类型如何逐届漂移」。
取园中「三道刀口」同届三届：**1984 / 1996 / 2003**。

结构：X＝球员实体（每届 7 人）· Y＝指标（5）· Z＝届次（3）。
数据：FiveThirtyEight RAPTOR by player（CC BY 4.0），career 级聚合。
输出：docs/figs/nba-three-classes/v01/… ＋ data/nba-three-classes.csv（实体数据表）
用法: .venv/bin/python scripts/fig_nba_three_classes.py
"""
import os, sys, csv, collections
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from fig_data_cube import draw_cube, BG, INK, DIM  # noqa

matplotlib.rcParams["font.family"] = ["Hiragino Sans GB", "Arial Unicode MS", "sans-serif"]
matplotlib.rcParams["axes.unicode_minus"] = False
D = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
VER = os.environ.get("VER", "v01")
OUT = os.path.join(D, "docs", "figs", "nba-three-classes", VER)
os.makedirs(OUT, exist_ok=True)

CLASSES = {
    1984: ["Michael Jordan", "Hakeem Olajuwon", "Charles Barkley", "John Stockton",
           "Alvin Robertson", "Otis Thorpe", "Kevin Willis"],
    1996: ["Kobe Bryant", "Allen Iverson", "Steve Nash", "Ray Allen",
           "Ben Wallace", "Peja Stojakovic", "Stephon Marbury"],
    2003: ["LeBron James", "Dwyane Wade", "Chris Bosh", "Carmelo Anthony",
           "Chris Kaman", "Kirk Hinrich", "David West"],
}
METRICS = ["生涯WAR", "巅峰季WAR", "生涯季数", "平均WAR", "巅峰RAPTOR"]


def build():
    per = collections.defaultdict(list)
    with open(os.path.join(D, "data", "nba-raptor-by-player.csv")) as f:
        for r in csv.DictReader(f):
            try:
                per[r["player_name"]].append((float(r["war_total"] or 0),
                                              float(r["raptor_total"] or 0)))
            except Exception:
                pass
    rows, zlab, xlab = [], [], []
    M = np.full((len(CLASSES), 7, len(METRICS)), np.nan)
    for zi, (yr, roster) in enumerate(CLASSES.items()):
        zlab.append(str(yr))
        scored = []
        for p in roster:
            xs = per.get(p)
            if not xs:
                continue
            wars = [w for w, _ in xs]; raps = [q for _, q in xs]
            vals = [sum(wars), max(wars), len(xs), sum(wars) / len(xs), max(raps)]
            scored.append((vals[0], p, vals))
        scored.sort(key=lambda x: -x[0])                 # 按生涯 WAR 降序 → 共享「排名槽」
        names = []
        for xi, (_, p, vals) in enumerate(scored):
            M[zi, xi, :] = vals
            names.append(p.split()[-1])
            rows.append([yr, p] + [round(v, 2) for v in vals])
        xlab.append(names)
    with open(os.path.join(D, "data", "nba-three-classes.csv"), "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["class", "rank", "player"] + METRICS)
        rk = collections.Counter()
        for r in rows:
            rk[r[0]] += 1
            w.writerow([r[0], rk[r[0]], r[1]] + r[2:])
    return M, xlab, METRICS, zlab


def main():
    M, xlab, ylab, zlab = build()
    fig = plt.figure(figsize=(15, 8.4), dpi=110)
    fig.patch.set_facecolor(BG)
    fig.text(0.045, 0.965, "NBA 三届 · 实体数据立方体", color=INK, fontsize=24,
             fontweight="bold", va="top")
    fig.text(0.045, 0.925, "Data Cube · 深度＝选秀届次（1984 / 1996 / 2003）· X＝球员实体 · Y＝生涯指标　"
                           "—— 每层切片＝一届的实体数据横截面", color=DIM, fontsize=12, va="top")

    ax = fig.add_axes([0.10, 0.12, 0.80, 0.75]); ax.set_facecolor(BG); ax.axis("off")
    draw_cube(ax, M, xlab, [m for m in ylab], zlab, cmap="magma", o=(0.95, 0.62))
    Z = M.shape[0]
    ax.set_xlim(-2.4, M.shape[1] + 0.95 * Z + 1.6)
    ax.set_ylim(-1.4, M.shape[2] + 0.62 * Z + 1.2)

    fig.text(0.045, 0.055,
             "读：一层＝一届实体（球员）的数据横截面；沿深度竖看＝同一「顺位槽」跨届对照；"
             "色＝各指标自身 min-max 归一（跨指标不同标度，勿横比）。", color=INK, fontsize=11)
    fig.text(0.045, 0.028,
             "实体数据表：data/nba-three-classes.csv（每球员×5 指标，可复算）· "
             "数据 FiveThirtyEight RAPTOR by player（CC BY 4.0）· 母本 ima doc 7512032127513120 · "
             f"ver {VER} · lola 2026-10-03", color=DIM, fontsize=9.2)

    for ext in ("png", "svg"):
        fig.savefig(os.path.join(OUT, f"nba-three-classes-zh.{ext}"), facecolor=BG)
    plt.close(fig)
    print("→", OUT)
    print("NBA_THREE_DONE")


if __name__ == "__main__":
    main()
