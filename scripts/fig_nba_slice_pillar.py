#!/usr/bin/env python3
"""fig_nba_slice_pillar.py — 「切片柱阵 Slice-Pillar Array」NBA 选秀实例。

术语碑 v5 条目（主人 1003 亲述·草图 D0F1995B）:
  实体沿纵向堆叠成行（每行＝一条 track／一个序列），所有行共享同一条横向 slice 轴；
  每行沿该轴立起方柱，柱高＝该实体在该 slice 的强度。
  生信对标 = genome-browser multi-track (IGV) + Manhattan-plot 站立美学（天际线式方柱）。

本案（NBA 选秀 = 序型对象）:
  · 行序 = 选秀顺位（pick 1..51）= 「序位」第三轴落在纵轴上
  · 横轴 = 赛季切片（2003-04 … 2021-22）
  · 柱高 = 该季 WAR（FiveThirtyEight RAPTOR，共享标度）
  · 看得到：共现＝选秀夜那一片（整届同现）；序＝每人一行向右铺开的轨迹。

数据: data/nba-raptor-by-player.csv
      FiveThirtyEight, "historical_RAPTOR_by_player", CC BY 4.0
输出: docs/figs/nba-slice-pillar-{zh,en}-{dark,light}.{svg,png}
"""
import os, csv
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

matplotlib.rcParams["font.family"] = ["Hiragino Sans GB", "Arial Unicode MS", "sans-serif"]
matplotlib.rcParams["axes.unicode_minus"] = False
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "docs", "figs")
DATA = os.path.join(HERE, "..", "data", "nba-raptor-by-player.csv")

# 2003 NBA draft, 顺位 → 球员（公开事实；用于「序位」纵轴）
PICKS = [
    (1,  "LeBron James"), (2, "Darko Milicic"), (3, "Carmelo Anthony"),
    (4,  "Chris Bosh"),   (5, "Dwyane Wade"),   (6, "Chris Kaman"),
    (7,  "Kirk Hinrich"), (18, "David West"),   (29, "Josh Howard"),
    (47, "Mo Williams"),  (51, "Kyle Korver"),
]

TH = {
    "dark":  dict(bg="#0b0d10", ink="#e4dfd2", dim="#8f8b82", faint="#2c3038",
                  gold="#c9a959", goldd="#e8d59a", red="#b5634f", slice="#3d424c", band="#1a2029"),
    "light": dict(bg="#ffffff", ink="#1a1a1a", dim="#6b6b6b", faint="#e2ddd2",
                  gold="#b8860b", goldd="#7a5c07", red="#a0522d", slice="#cfc9bb", band="#f6f2e9"),
}

W, H = 1400, 1000
LM, RM, TM, BM = 300, 70, 150, 130


def load():
    per = {}
    with open(DATA) as f:
        for r in csv.DictReader(f):
            if r["season"] and r["war_total"]:
                per.setdefault(r["player_name"], {})[int(r["season"])] = float(r["war_total"])
    return per


def ll(theme, k):
    zh = dict(title="切片柱阵 · Slice-Pillar Array",
              sub="NBA 选秀 = 序型对象：行序＝选秀顺位（序位＝第三轴）｜横轴＝赛季切片｜柱高＝该季 WAR（共享标度）",
              seascape="赛季切片 →", presence="共现：选秀夜那一片（整届同现）",
              order="序：每人一条 track，向右铺开的轨迹",
              legend_up="柱高 = 该季 WAR（正值，向上）", legend_dn="负值（向下）",
              foot="源 = FiveThirtyEight RAPTOR（CC BY 4.0）· 生信对标 = IGV multi-track ＋ Manhattan 天际线 · 承 切片联合律 / 超级结 / 变化轴律 / 共现与序")
    en = dict(title="Slice-Pillar Array",
              sub="NBA draft = an order-type object: row order = pick number (ordinal = 3rd axis) | x = season slices | bar height = WAR that season (shared scale)",
              seascape="season slices →", presence="coexistence: draft night = one slice (whole class at once)",
              order="order: one track per player, a trajectory marching right",
              legend_up="bar height = WAR that season (positive)", legend_dn="negative",
              foot="Source = FiveThirtyEight RAPTOR (CC BY 4.0) · bioinformatics analogue = IGV multi-track + Manhattan skyline")
    return (en if theme.startswith("en-") else zh)[k]


def main(theme):
    th = TH[theme.split("-")[-1]]
    lang = "en" if theme.startswith("en-") else "zh"
    per = load()
    data = [(p, n, per.get(n, {})) for p, n in PICKS]
    seasons = sorted({s for _, _, d in data for s in d})
    x0, x1 = seasons[0], seasons[-1]
    n_slot = x1 - x0 + 1
    max_abs = max((abs(v) for _, _, d in data for v in d.values()), default=1.0)

    fig = plt.figure(figsize=(W / 100, H / 100), dpi=200)
    fig.patch.set_facecolor(th["bg"])
    ax = fig.add_axes([0, 0, 1, 1]); ax.set_xlim(0, W); ax.set_ylim(0, H); ax.axis("off")
    ax.set_facecolor(th["bg"])

    px0, px1 = LM, W - RM
    py1, py0 = H - TM, BM
    slot = (px1 - px0) / n_slot
    pitch = (py1 - py0) / len(data)
    half = pitch * 0.46
    scale = half / max_abs

    def X(season):  # season 中心
        return px0 + (season - x0 + 0.5) * slot

    # 背景：赛季切片（IGV 共享坐标）
    for s in range(x0, x1 + 1):
        ax.plot([px0 + (s - x0) * slot] * 2, [py0, py1], color=th["slice"], lw=0.6, zorder=1)
    # 共现带：新秀赛季（整届同现的那一片）
    ax.add_patch(Rectangle((px0, py0), slot, py1 - py0, facecolor=th["band"], edgecolor="none", zorder=0))

    # 标题
    ax.text(LM - 90, H - 52, ll(theme, "title"), color=th["ink"], fontsize=22, weight="bold", ha="left", va="center")
    ax.text(LM - 90, H - 88, ll(theme, "sub"), color=th["dim"], fontsize=11.5, ha="left", va="center")
    ax.text(LM - 90, H - 118, ll(theme, "presence"), color=th["gold"], fontsize=11, ha="left", va="center")

    # 行 + 柱
    for i, (pick, name, d) in enumerate(data):
        yc = py1 - (i + 0.5) * pitch
        ax.plot([px0, px1], [yc, yc], color=th["faint"], lw=0.7, zorder=1)
        # 顺位标签
        ax.text(px0 - 18, yc + 10, f"#{pick}", color=th["gold"], fontsize=13, weight="bold", ha="right", va="center")
        ax.text(px0 - 18 - 46, yc + 10, name, color=th["ink"], fontsize=11.5, ha="right", va="center")
        # 生涯区间淡标
        if d:
            ax.text(px0 - 18 - 46, yc - 12, f"{min(d)}–{max(d)}  ·  ΣWAR {sum(d.values()):.0f}",
                    color=th["dim"], fontsize=8.5, ha="right", va="center")
        for s, v in sorted(d.items()):
            xc = X(s); bw = slot * 0.34
            h = v * scale
            if v >= 0:
                ax.add_patch(Rectangle((xc - bw / 2, yc), bw, h, facecolor=th["gold"],
                                       edgecolor=th["goldd"], lw=0.6, zorder=3))
            else:
                ax.add_patch(Rectangle((xc - bw / 2, yc + h), bw, -h, facecolor=th["red"],
                                       edgecolor="none", alpha=0.85, zorder=3))

    # 轴
    ax.plot([px0, px1], [py0, py0], color=th["faint"], lw=1.2, zorder=2)
    # 方向标：纵＝序位，横＝赛季切片
    ax.annotate("", xy=(px0 - 250, py0 + 6), xytext=(px0 - 250, py1 - 6),
                arrowprops=dict(arrowstyle="-|>", color=th["gold"], lw=1.4, alpha=0.8))
    ax.text(px0 - 262, (py0 + py1) / 2, "序位（顺位）", color=th["gold"], fontsize=10.5,
            ha="center", va="center", rotation=90, alpha=0.9)
    ax.annotate("", xy=(px1, py1 + 26), xytext=(px0, py1 + 26),
                arrowprops=dict(arrowstyle="-|>", color=th["dim"], lw=1.2, alpha=0.8))
    ax.text(px1, py1 + 40, ll(theme, "seascape"), color=th["dim"], fontsize=10.5, ha="right", va="center")
    for s in range(x0, x1 + 1, 2):
        ax.text(X(s), py0 - 20, str(s), color=th["dim"], fontsize=9, ha="center", va="center")

    # 图例
    lgx, lgy = px1 - 300, py0 - 62
    ax.add_patch(Rectangle((lgx, lgy), 14, 22, facecolor=th["gold"], edgecolor=th["goldd"], lw=0.6))
    ax.text(lgx + 22, lgy + 11, ll(theme, "legend_up"), color=th["dim"], fontsize=9.5, ha="left", va="center")
    ax.add_patch(Rectangle((lgx, lgy - 30), 14, 18, facecolor=th["red"], edgecolor="none", alpha=0.85))
    ax.text(lgx + 22, lgy - 21, ll(theme, "legend_dn"), color=th["dim"], fontsize=9.5, ha="left", va="center")

    ax.text(LM - 90, 34, ll(theme, "foot"), color=th["dim"], fontsize=8.8, ha="left", va="center")

    os.makedirs(OUT, exist_ok=True)
    for ext in ("svg", "png"):
        fig.savefig(os.path.join(OUT, f"nba-slice-pillar-{theme}.{ext}"),
                    facecolor=th["bg"], dpi=200)
    plt.close(fig)
    print("wrote", f"nba-slice-pillar-{theme}.{{svg,png}}", f"seasons {x0}-{x1} max|WAR|={max_abs:.1f}")


if __name__ == "__main__":
    import sys
    for t in (sys.argv[1:] or ["zh-dark", "zh-light"]):
        main(t)
