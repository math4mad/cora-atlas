#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""topography-flat.py — 园体地铁图 (metro map 正典: 45° 折线/等宽/换乘环)
主人 09-23 定纲: 拓扑图里距离与时间一样无关紧要, 对象之间的位置关系才是信息本身。
—— 这正是地铁图的公理: 乘客要的是拓扑, 不是里程。"""

W, H = 1240, 800
BG, INK, MUT = "#fbf7ec", "#2f2a24", "#6f6558"
GIT, SEA, LANE, HAT = "#b0762a", "#2E8FA3", "#9a8f7a", "#8c2f2f"

# 站表: id -> (English, col, row, kind)  kind: st=普通站 po=政体(大菱形) ix=换乘环
S = {
 "exp":    ("Field Trials",        2, 0, "st"),
 "lyc":    ("Skills Registry",     8, 0, "st"),
 "kaggle": ("Forge · Kaggle",     13, 0, "st"),
 "chora":  ("CHORA",               5, 2, "po"),
 "mail":   ("Post House",          8, 2, "st"),
 "stele":  ("Code of Law",         6, 3, "ix"),
 "akad":   ("ACADEMY",            10, 3, "po"),
 "angel":  ("Couriers",           11, 4, "st"),
 "maca":   ("Machine A",          13, 4, "ix"),
 "ledger": ("Ledger",              1, 4, "st"),
 "atlas":  ("ATLAS",               3, 5, "po"),
 "arch":   ("ARCHIVE",            10, 5, "po"),
 "agora":  ("Market/Stele Site",   6, 5, "ix"),
 "gloss":  ("Glossary Steles",     1, 6, "st"),
 "ext":    ("Quarantine Port",    13, 6, "st"),
 "onom":   ("Name Register",       6, 7, "st"),
 "itiner": ("Itinerary Notes",     3, 8, "st"),
 "macb":   ("Machine B",          10, 8, "ix"),
 "icloud": ("Book Mountain",      13, 8, "st"),
}
HAT = {"ledger":"Irene","onom":"Nikos","macb":"Nikos","lyc":"Theuth","arch":"Thea","icloud":"Irene","stele":"Hammurabi"}

# 三层架构 (主人 0924 令): 园体 → 项目群 → 个体站 —— 群表在此落户口
GROUPS = {
 "atlas":   ("ATLAS 碑园",   ["ledger","atlas","gloss","itiner","onom","stele"]),
 "chora":   ("CHORA 实验田", ["chora","exp","kaggle","lyc","mail"]),
 "academy": ("ACADEMY 学园", ["akad","angel","maca","macb"]),
 "archive": ("ARCHIVE 馆港", ["arch","ext","icloud"]),
 "agora":   ("AGORA 市集",   ["agora"]),
}
ST2GRP = {k: g for g, (_, ks) in GROUPS.items() for k in ks}

# 线路表: (名, 色, 站点序列) —— 每段自动走 横/45°/竖 地铁三向
LINES = [
 ("chora lane",  LANE, ["exp","chora","mail","lyc"]),
 ("atlas lane",  LANE, ["ledger","atlas","gloss"]),
 ("atlas spur",  LANE, ["atlas","itiner"]),
 ("law loop",    LANE, ["chora","stele","agora","onom","atlas"]),
 ("market link", LANE, ["agora","arch"]),
 ("git trunk",   GIT,  ["akad","arch"]),
 ("git south",   GIT,  ["akad","agora"]),
 ("git east",    GIT,  ["akad","maca"]),
 ("git south-e", GIT,  ["maca","macb"]),
 ("courier exp", GIT,  ["angel","kaggle"]),
 ("sea north",   SEA,  ["maca","kaggle"]),
 ("sea south",   SEA,  ["macb","kaggle"]),
 ("archive lane",LANE, ["arch","ext"]),
 ("book lane",   LANE, ["icloud","ext"]),
 ("quar lane",   LANE, ["macb","ext"]),
 ("courier ln",  LANE, ["angel","arch"]),
]
G = 52; OX, OY = 90, 120
def pt(k):
    _, c, r, _ = S[k]; return (OX + c*G, OY + r*G)

def metro(a, b):
    """三向走线: 先横, 再 45°, 后竖 —— 地铁图正典。"""
    x1, y1 = pt(a); x2, y2 = pt(b)
    dx, dy = x2-x1, y2-y1
    adx, ady = abs(dx), abs(dy)
    sx, sy = (1 if dx>0 else -1), (1 if dy>0 else -1)
    d = min(adx, ady)                       # 45° 段投影
    rest = adx - d
    # 拐点分配: 横->斜->竖
    mx1, my1 = x1 + sx*rest, y1
    mx2, my2 = x1 + sx*rest + sx*d, y1 + sy*d
    if adx >= ady:
        return f'M{x1},{y1} L{mx1},{my1} L{mx2},{my2} L{x2},{y2}'
    d2 = min(adx, ady); rest2 = ady - d2
    ax1, ay1 = x1, y1 + sy*rest2
    ax2, ay2 = x1 + sx*d2, y1 + sy*rest2 + sy*d2
    return f'M{x1},{y1} L{ax1},{ay1} L{ax2},{ay2} L{x2},{y2}'

import json
_GJ = json.dumps({g: {"label": lab, "members": ks} for g, (lab, ks) in GROUPS.items()}, ensure_ascii=False).replace('"', '&quot;')
s = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" font-family="Helvetica Neue, Helvetica, Arial, sans-serif" id="garden-metro" data-groups="{_GJ}">',
     f'<rect width="{W}" height="{H}" fill="{BG}"/>',
     '<style>.st{cursor:pointer}.st.dim{opacity:.16}.st.kin{opacity:.5}.st.kin .mark{stroke:' + "#c9a959" + ';stroke-opacity:.9}.st.here .mark{stroke:#8a6a1f;stroke-width:5.5;filter:drop-shadow(0 0 7px #ffd97a)}.st.here .lbl{fill:#8a6a1f;font-weight:800}#lnwrap.dim{opacity:.14}.lines path{transition:opacity .3s} g.st{transition:opacity .3s}</style>',
     f'<text x="{W/2}" y="46" text-anchor="middle" font-size="25" fill="{INK}" font-weight="700" letter-spacing="4">THE GARDEN METRO · 园体运行图</text>',
     f'<text x="{W/2}" y="68" text-anchor="middle" font-size="11.5" fill="{MUT}" letter-spacing="4">距离与时间无关紧要 · 位置关系才是信息本身</text>']
# 线路
s.append('<g id="lnwrap" class="lines">')
for name, col, stops in LINES:
    for a, b in zip(stops, stops[1:]):
        dash = ' stroke-dasharray="9 7"' if col == SEA else ""
        s.append(f'<path d="{metro(a,b)}" data-via="{a} {b}" fill="none" stroke="{col}" stroke-width="4.5" stroke-linecap="round" stroke-linejoin="round"{dash} opacity=".88"/>')
s.append('</g>')
# 车站（三层户口: class=st, id=st-站, data-group=群）
for k, (en, c, r, kind) in S.items():
    x, y = pt(k)
    g = ST2GRP.get(k, "none")
    s.append(f'<g class="st" id="st-{k}" data-group="{g}" data-name="{en}">')
    if kind == "po":
        s.append(f'<path class="mark" d="M{x},{y-11} L{x+11},{y} L{x},{y+11} L{x-11},{y} Z" fill="{BG}" stroke="{HAT}" stroke-width="3.4"/>')
        s.append(f'<text class="lbl" x="{x}" y="{y-19}" text-anchor="middle" font-size="14.5" fill="{INK}" font-weight="700" stroke="{BG}" stroke-width="4" paint-order="stroke">{en}</text>')
    elif kind == "ix":
        s.append(f'<circle class="mark" cx="{x}" cy="{y}" r="9" fill="{BG}" stroke="{INK}" stroke-width="3.4"/>')
        s.append(f'<text class="lbl" x="{x}" y="{y-16}" text-anchor="middle" font-size="13" fill="{INK}" font-weight="600" stroke="{BG}" stroke-width="4" paint-order="stroke">{en}</text>')
    else:
        s.append(f'<circle class="mark" cx="{x}" cy="{y}" r="6.5" fill="{BG}" stroke="{INK}" stroke-width="2.6"/>')
        s.append(f'<text class="lbl" x="{x}" y="{y-12}" text-anchor="middle" font-size="12.5" fill="{INK}" stroke="{BG}" stroke-width="4" paint-order="stroke">{en}</text>')
    if k in HAT:
        s.append(f'<text x="{x}" y="{y+24}" text-anchor="middle" font-size="9.5" fill="{HAT}" font-weight="600">hat·{HAT[k]}</text>')
    s.append('</g>')
# 图例
lg = f'<g transform="translate(70,{H-46})">'
lg += f'<line x1="0" y1="0" x2="42" y2="0" stroke="{GIT}" stroke-width="4.5" stroke-linecap="round"/><text x="50" y="4" font-size="12" fill="{MUT}">git trunk (机构大路)</text>'
lg += f'<line x1="250" y1="0" x2="292" y2="0" stroke="{SEA}" stroke-width="4.5" stroke-dasharray="9 7" stroke-linecap="round"/><text x="300" y="4" font-size="12" fill="{MUT}">sea route (火神航线)</text>'
lg += f'<line x1="500" y1="0" x2="542" y2="0" stroke="{LANE}" stroke-width="4.5" stroke-linecap="round"/><text x="550" y="4" font-size="12" fill="{MUT}">in-repo lane (仓内小径)</text>'
lg += f'<circle cx="760" cy="0" r="9" fill="{BG}" stroke="{INK}" stroke-width="3.4"/><text x="778" y="4" font-size="12" fill="{MUT}">interchange 换乘</text>'
lg += f'<path d="M920,-10 L930,0 L920,10 L910,0 Z" fill="{BG}" stroke="{HAT}" stroke-width="3.4"/><text x="940" y="4" font-size="12" fill="{MUT}">polity 政体</text>'
lg += f'<text x="1080" y="4" font-size="11" fill="{MUT}">点站定位 / ?at=站id</text></g>'
s.append(lg)
s.append('</svg>')
open("docs/figs/topos-flat.svg", "w").write("\n".join(s))
print("wrote docs/figs/topos-flat.svg (metro 版)")
