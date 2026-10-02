#!/usr/bin/env python3
"""fig_nba_slice_pillar_mp.py — 「切片柱阵」NBA 选秀，按 MPI-BGI / Lázaro Alonso
SeasFire Cube 海报的构图语言重画：深炭灰底 ＋ 橙色分隔线 ＋ 一列列叠起的三维方块
＋ 上扬刀片（长度＝生涯 ΣWAR）＋ 左侧题头/数据源/覆盖表 ＋ 右侧色标与彩色清单。

编码（与术语碑 v5「切片柱阵 Slice-Pillar Array」对齐的竖向变体）:
  · 每一列 = 一个实体（一名球员）；列序 = 选秀顺位（序位轴落在横向）
  · 每一块 = 一个 slice（一个赛季）；纵向堆叠 = 时间轴（切片线横穿所有列）
  · 方块颜色 = 该实体在该 slice 的强度（该季 WAR，连续色标）
  · 最低一行 = 选秀夜那一片：整届同现（所有列共享同一切片）
  · 上扬刀片 = 该列生涯 ΣWAR（把「高度」这一维补回生涯层面）

数据: data/nba-raptor-by-player.csv  (FiveThirtyEight RAPTOR, CC BY 4.0)
输出: docs/figs/nba-slice-pillar-mp-{zh,en}-{dark,light}.{svg,png}
"""
import os, csv, math
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Polygon
from matplotlib.colors import LinearSegmentedColormap, rgb_to_hsv, hsv_to_rgb

matplotlib.rcParams["font.family"] = ["Hiragino Sans GB", "Arial Unicode MS", "sans-serif"]
matplotlib.rcParams["axes.unicode_minus"] = False
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "docs", "figs")
DATA = os.path.join(HERE, "..", "data", "nba-raptor-by-player.csv")

# 2003 NBA draft：选秀顺位 → 球员（表的次序＝序；公开事实）
PICKS = [
    (1, "LeBron James"), (2, "Darko Milicic"), (3, "Carmelo Anthony"),
    (4, "Chris Bosh"), (5, "Dwyane Wade"), (6, "Chris Kaman"),
    (7, "Kirk Hinrich"), (18, "David West"), (29, "Josh Howard"),
    (47, "Mo Williams"), (51, "Kyle Korver"),
]

CMAP = LinearSegmentedColormap.from_list("mp", [
    (0.00, "#6d2a2a"), (0.16, "#4a4a4a"), (0.34, "#2ea3a3"),
    (0.58, "#8fbf5a"), (0.80, "#e0c060"), (1.00, "#ffeaa7"),
])
VMIN, VMAX = -7.0, 28.0

TH = {
    "dark":  dict(bg="#2e2e2e", ink="#ece8e1", dim="#a9a49b", line="#454545",
                  orange="#e08a2e", lime="#a3c24a", teal="#2ea3a3"),
    "light": dict(bg="#f4f1ec", ink="#26241f", dim="#6b675f", line="#d5cec1",
                  orange="#c96a12", lime="#6f8f22", teal="#1f7d7d"),
}

W, H = 1700, 1080
RULE_Y = 372
COL_X0, PITCH, COLW, DX, DY = 560, 70, 56, 9, 9
FLOOR, CUBE_H = 300, 26
X_END = COL_X0 + PITCH * len(PICKS)
LX = 46


def shade(color, f):
    r, g, b = matplotlib.colors.to_rgb(color)
    h, s, v = rgb_to_hsv((r, g, b))
    v = min(1.0, v * f); s = min(1.0, s * (0.75 + 0.25 * f))
    return hsv_to_rgb((h, s, v))


def cube(ax, x, y, w, h, color, z=4):
    ax.add_patch(Polygon([(x, y), (x + w, y), (x + w + DX, y + DY), (x + DX, y + DY)], closed=True,
                         facecolor=shade(color, 0.70), edgecolor="none", zorder=z))
    ax.add_patch(Polygon([(x, y + h), (x + w, y + h), (x + w + DX, y + h + DY), (x + DX, y + h + DY)],
                         closed=True, facecolor=shade(color, 1.38), edgecolor="none", zorder=z + 1))
    ax.add_patch(Polygon([(x + w, y), (x + w + DX, y + DY), (x + w + DX, y + h + DY), (x + w, y + h)],
                         closed=True, facecolor=shade(color, 0.76), edgecolor="none", zorder=z + 2))
    ax.add_patch(Rectangle((x, y), w, h, facecolor=color, edgecolor="none", zorder=z + 3))


def blade(ax, x, y, length, color, w0=10.0, w1=3.0, ang=72.0, z=7):
    a = math.radians(ang); ux, uy = math.cos(a), math.sin(a); nx, ny = -uy, ux
    tx, ty = x + ux * length, y + uy * length
    ax.add_patch(Polygon([(x + nx * w0 / 2, y + ny * w0 / 2), (x - nx * w0 / 2, y - ny * w0 / 2),
                          (tx - nx * w1 / 2, ty - ny * w1 / 2), (tx + nx * w1 / 2, ty + ny * w1 / 2)],
                         closed=True, facecolor=color, edgecolor="none", alpha=0.92, zorder=z))


def load():
    per = {}
    with open(DATA) as f:
        for r in csv.DictReader(f):
            if r["season"] and r["war_total"]:
                per.setdefault(r["player_name"], {})[int(r["season"])] = float(r["war_total"])
    return per


def ll(theme):
    en = theme.startswith("en-")
    if en:
        return dict(credit="Fig by lola · cora-atlas",
                    cred2="Composition after Lázaro Alonso (MPI-BGI) SeasFire Cube poster",
                    h1="NBA 2003 Draft · Slice-Pillar Array", h2="Duel-Pillar Grove",
                    src="Data sources", rows_src=["FiveThirtyEight RAPTOR",
                                                  "historical_RAPTOR_by_player (CC BY 4.0)",
                                                  "19,159 player-seasons · 1977–2022"],
                    proj="Sample", rows_proj=["2003 NBA Draft · 11 picks",
                                              "2003-04 → 2021-22",
                                              "column = entity · block = slice · color = intensity"],
                    kvs=[("slice", "season slice"), ("color", "WAR that season"),
                         ("ordinal", "column order = draft pick"), ("blade", "blade length = career ΣWAR")],
                    tail="19 seasons · 2003-04 – 2021-22",
                    note="Glossary v5 · Slice-Pillar Array（Duel-Pillar Grove）| bioinformatics analogue = "
                         "IGV genome-browser multi-track + Manhattan stand-up aesthetics | shape after MPI-BGI SeasFire",
                    coex="coexistence", coex2="bottom row = draft night (whole class at once)",
                    scale="Color · WAR", clist="pick → player · ΣWAR")
    return dict(credit="Fig by lola · cora-atlas",
                cred2="构图参照 Lázaro Alonso（MPI-BGI）SeasFire Cube 海报",
                h1="NBA 2003 选秀 · 切片柱阵", h2="Slice-Pillar Array（艺名 对决柱林）",
                src="数据源", rows_src=["FiveThirtyEight RAPTOR",
                                        "historical_RAPTOR_by_player（CC BY 4.0）",
                                        "19,159 球员-赛季 · 1977–2022"],
                proj="本案样本", rows_proj=["2003 NBA Draft · 11 顺位",
                                            "2003-04 → 2021-22",
                                            "列＝实体 · 块＝切片 · 色＝强度"],
                kvs=[("切片", "赛季切片"), ("色标", "该季 WAR"),
                     ("序位", "列序＝选秀顺位"), ("刀片", "刀片长＝生涯 ΣWAR")],
                tail="覆盖 19 季 · 2003-04 – 2021-22",
                note="术语碑 v5 · 切片柱阵（艺名 对决柱林）｜生信对标 ＝ IGV genome-browser multi-track ＋ "
                     "Manhattan-plot 站立美学｜构图参照 MPI-BGI SeasFire 海报",
                coex="共现", coex2="最低一行 ＝ 选秀夜那一片（整届同现）",
                scale="色标 · WAR", clist="顺位 → 球员 · ΣWAR")


def main(theme):
    th = TH[theme.split("-")[-1]]
    L = ll(theme)
    per = load()
    data = [(p, n, per.get(n, {})) for p, n in PICKS]
    seasons = sorted({s for _, _, d in data for s in d})
    y0s, y1s = seasons[0], seasons[-1]
    top = FLOOR + (y1s - y0s + 1) * CUBE_H

    fig = plt.figure(figsize=(W / 100, H / 100), dpi=200)
    fig.patch.set_facecolor(th["bg"])
    ax = fig.add_axes([0, 0, 1, 1]); ax.set_xlim(0, W); ax.set_ylim(0, H); ax.axis("off")
    ax.set_facecolor(th["bg"])

    # 橙色分隔线（压在方块后面，参照海报）
    ax.plot([36, W - 36], [RULE_Y, RULE_Y], color=th["orange"], lw=2.0, zorder=0.5, alpha=0.85)

    # 赛季切片线
    for s in seasons:
        yy = FLOOR + (s - y0s) * CUBE_H
        ax.plot([COL_X0 - 14, X_END + 16], [yy, yy], color=th["line"], lw=0.6, zorder=1)
    # 共现带（最低一片＝选秀夜）
    ax.add_patch(Rectangle((COL_X0 - 14, FLOOR), (X_END + 16) - (COL_X0 - 14), CUBE_H,
                           facecolor=th["orange"], alpha=0.14, zorder=1))
    ax.text(COL_X0 - 26, FLOOR + CUBE_H * 0.72, f"⇤ {L['coex']}", color=th["orange"], fontsize=11,
            weight="bold", ha="right", va="center", zorder=8)
    ax.text(COL_X0 - 26, FLOOR + CUBE_H * 0.18, L["coex2"], color=th["dim"], fontsize=8.8,
            ha="right", va="center", zorder=8)

    # 年份轴（紧贴列阵右侧）
    for s in seasons:
        if s % 2 == 0:
            ax.text(X_END + 22, FLOOR + (s - y0s) * CUBE_H + CUBE_H / 2, str(s),
                    color=th["dim"], fontsize=8.4, ha="left", va="center")
    ax.annotate("", xy=(X_END + 10, top), xytext=(X_END + 10, FLOOR),
                arrowprops=dict(arrowstyle="-|>", color=th["dim"], lw=1.0))

    # 方块列
    for i, (pick, name, d) in enumerate(data):
        x = COL_X0 + i * PITCH
        for s, v in sorted(d.items()):
            y = FLOOR + (s - y0s) * CUBE_H
            c = CMAP(min(1.0, max(0.0, (v - VMIN) / (VMAX - VMIN))))
            cube(ax, x, y, COLW, CUBE_H - 2.0, c)
        ax.text(x + (COLW + DX) / 2, FLOOR - 20, f"#{pick}", color=th["orange"],
                fontsize=11.5, weight="bold", ha="center", va="center")

    # 上扬刀片：长度＝生涯 ΣWAR
    from matplotlib.colors import to_rgba
    smax = max(sum(d.values()) for _, _, d in data) or 1.0
    for i, (pick, name, d) in enumerate(data):
        tot = sum(d.values())
        if tot <= 0:
            continue
        x = COL_X0 + i * PITCH + (COLW + DX) / 2
        blade(ax, x, top + 2, 34 + 150 * (tot / smax), th["lime"] if tot < 100 else th["orange"])

    # 左侧题头
    ax.text(LX, H - 44, L["credit"], color=th["ink"], fontsize=12.5, weight="bold", ha="left", va="center")
    ax.text(LX, H - 66, L["cred2"], color=th["dim"], fontsize=9, ha="left", va="center")
    ax.text(LX, H - 116, L["h1"], color=th["ink"], fontsize=19, weight="bold", ha="left", va="center")
    ax.text(LX, H - 148, L["h2"], color=th["orange"], fontsize=12.5, ha="left", va="center")

    y = H - 194
    ax.text(LX, y, L["src"], color=th["orange"], fontsize=12, weight="bold", ha="left", va="center")
    for t in L["rows_src"]:
        y -= 22; ax.text(LX, y, t, color=th["ink"], fontsize=10, ha="left", va="center")
    y -= 34
    ax.text(LX, y, L["proj"], color=th["orange"], fontsize=12, weight="bold", ha="left", va="center")
    for j, t in enumerate(L["rows_proj"]):
        y -= 22
        ax.text(LX, y, t, color=th["teal"] if j == 2 else th["ink"], fontsize=10, ha="left", va="center")
    y -= 34
    for k, v in L["kvs"]:
        ax.text(LX, y, k, color=th["orange"], fontsize=10.5, weight="bold", ha="left", va="center")
        ax.text(LX + 74, y, v, color=th["ink"], fontsize=10, ha="left", va="center")
        y -= 24
    ax.text(LX, y - 2, L["tail"], color=th["dim"], fontsize=9, ha="left", va="center")

    # 底部方法注
    ax.text(LX, 96, L["note"], color=th["dim"], fontsize=9.2, ha="left", va="center")

    # 右侧色标 + 清单
    px, pw = W - 252, 20
    cpy0, cpy1 = RULE_Y - 30, H - 250
    steps = 140
    for k in range(steps):
        v = VMIN + (VMAX - VMIN) * k / (steps - 1)
        c = CMAP(min(1.0, max(0.0, (v - VMIN) / (VMAX - VMIN))))
        ax.add_patch(Rectangle((px, cpy0 + (cpy1 - cpy0) * k / steps), pw, (cpy1 - cpy0) / steps + 1,
                               facecolor=c, edgecolor="none", zorder=3))
    ax.text(px - 10, cpy1 + 18, L["scale"], color=th["ink"], fontsize=11.5, weight="bold",
            ha="left", va="center")
    for v in (28, 20, 10, 0, -5):
        yy = cpy0 + (cpy1 - cpy0) * (v - VMIN) / (VMAX - VMIN)
        ax.text(px + pw + 8, yy, str(v), color=th["dim"], fontsize=8.6, ha="left", va="center")
        ax.plot([px - 4, px], [yy, yy], color=th["dim"], lw=0.7)

    ax.text(px - 10, cpy0 - 36, L["clist"], color=th["ink"], fontsize=11.5, weight="bold",
            ha="left", va="center")
    ly = cpy0 - 62
    for pick, name, d in data:
        peak = max(d.values()) if d else 0.0
        c = CMAP(min(1.0, max(0.0, (peak - VMIN) / (VMAX - VMIN))))
        ax.add_patch(Rectangle((px - 10, ly - 6), 12, 12, facecolor=c, edgecolor="none", zorder=3))
        ax.text(px + 10, ly, f"#{pick} {name}  ·  Σ{sum(d.values()):.0f}", color=th["ink"],
                fontsize=8.8, ha="left", va="center")
        ly -= 19.5

    os.makedirs(OUT, exist_ok=True)
    for ext in ("svg", "png"):
        fig.savefig(os.path.join(OUT, f"nba-slice-pillar-mp-{theme}.{ext}"), facecolor=th["bg"], dpi=200)
    plt.close(fig)
    print("wrote", f"nba-slice-pillar-mp-{theme}.{{svg,png}}")


if __name__ == "__main__":
    import sys
    for t in (sys.argv[1:] or ["zh-dark"]):
        main(t)
