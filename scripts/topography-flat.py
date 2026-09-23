#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""topography-flat.py — 园体拓扑·平面版 (English labels only, no buildings)
主人 09-23 令: 等距缩微效果不佳 → 平面化; 图内希腊词 → 英语, 希腊语入单独 glossary。
输出 docs/figs/topos-flat.svg"""

W, H = 1240, 800
BG, INK, MUT = "#fbf7ec", "#2f2a24", "#7a6f5e"
GIT, SEA, LANE, HAT = "#b0762a", "#2E8FA3", "#b3a88f", "#8c2f2f"

# id, English, gx, gy, group, hat
N = [
 ("exp",     "Field Trials",      1, 1, "chora", ""),
 ("lyc",     "Skills Registry",   4, 1, "chora", "Theuth"),
 ("mail",    "Post House",        3, 2, "chora", ""),
 ("chora",   "CHORA (home base)", 2, 2, "chora", ""),
 ("stele",   "Code of Law",       3, 4, "bridge", "Hammurabi"),
 ("ledger",  "Ledger",            1, 5, "atlas", "Irene"),
 ("gloss",   "Glossary Steles",   0, 6, "atlas", ""),
 ("itiner",  "Itinerary Notes",   1, 7, "atlas", ""),
 ("atlas",   "ATLAS (record)",    2, 6, "atlas", ""),
 ("onom",    "Name Register",     3, 8, "atlas", "Nikos"),
 ("agora",   "Market / Stele Site",4, 6, "atlas", ""),
 ("akad",    "ACADEMY",           6, 2, "polity", ""),
 ("arch",    "ARCHIVE",           6, 5, "polity", "Thea"),
 ("angel",   "Couriers Queue",    8, 4, "infra", ""),
 ("kaggle",  "Forge (Kaggle)",    10, 2, "infra", ""),
 ("maca",    "Machine A",         9, 6, "machine", ""),
 ("macb",    "Machine B",         8, 8, "machine", "Nikos"),
 ("icloud",  "Book Mountain",     10, 9, "infra", "Irene"),
 ("ext",     "Quarantine Port",   11, 6, "infra", ""),
]
E = [
 ("chora","exp",LANE),("chora","lyc",LANE),("chora","mail",LANE),
 ("atlas","ledger",LANE),("atlas","gloss",LANE),("atlas","itiner",LANE),("atlas","onom",LANE),
 ("atlas","stele",LANE),("chora","stele",LANE),("agora","stele",LANE),("agora","onom",LANE),
 ("akad","arch",GIT),("akad","agora",GIT),("akad","maca",GIT),("akad","macb",GIT),
 ("arch","maca",LANE),("arch","ext",LANE),
 ("maca","kaggle",SEA),("macb","kaggle",SEA),("macb","ext",LANE),
 ("icloud","ext",LANE),("angel","kaggle",GIT),("angel","arch",LANE),
]
pos = {n[0]: (90 + n[2]*100, 90 + n[3]*76) for n in N}

s = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" font-family="Helvetica Neue, Helvetica, Arial, sans-serif">',
     f'<rect width="{W}" height="{H}" fill="{BG}"/>']
# 政体软底
def blob(ids, color, name, ny):
    xs=[pos[i][0] for i in ids]; ys=[pos[i][1] for i in ids]
    x0,x1,y0,y1=min(xs)-64,max(xs)+64,min(ys)-52,max(ys)+52
    s.append(f'<rect x="{x0}" y="{y0}" width="{x1-x0}" height="{y1-y0}" rx="34" fill="{color}" opacity="0.07"/>')
    s.append(f'<rect x="{x0}" y="{y0}" width="{x1-x0}" height="{y1-y0}" rx="34" fill="none" stroke="{color}" stroke-dasharray="5 6" opacity=".5"/>')
    s.append(f'<text x="{x0+12}" y="{y0+22}" font-size="12" fill="{color}" letter-spacing="2" opacity=".9">{name}</text>')
blob(["exp","lyc","mail","chora"], "#6f8f5a", "POLITY · CHORA", 0)
blob(["ledger","gloss","itiner","atlas","agora","onom"], "#7a6a52", "POLITY · ATLAS", 0)
blob(["akad"], "#b0762a", "", 0); blob(["arch"], "#b0762a", "", 0)
# 边 (直角折线, 地铁图笔法)
for a,b,c in E:
    x1,y1=pos[a]; x2,y2=pos[b]
    mx = (x1+x2)/2
    s.append(f'<path d="M{x1},{y1} L{mx},{y1} L{mx},{y2} L{x2},{y2}" fill="none" stroke="{c}" stroke-width="{3 if c==GIT else (2 if c==SEA else 1.4)}" stroke-dasharray="{"7 6" if c==SEA else ("2 5" if c==LANE else "0")}" opacity="{0.9 if c!=LANE else 0.75}"/>')
# 节点
for n in N:
    x,y=pos[n[0]]
    r = 11 if n[4] in ("polity","chora","atlas") else 7
    col = {"polity":HAT,"chora":"#6f8f5a","atlas":"#7a6a52","infra":INK,"machine":SEA,"bridge":GIT}[n[4]]
    s.append(f'<circle cx="{x}" cy="{y}" r="{r}" fill="{BG}" stroke="{col}" stroke-width="2.6"/>')
    if r>10: s.append(f'<circle cx="{x}" cy="{y}" r="3.4" fill="{col}"/>')
    s.append(f'<text x="{x}" y="{y-r-7}" text-anchor="middle" font-size="13.5" fill="{INK}" font-weight="600">{n[1]}</text>')
    if n[5]: s.append(f'<text x="{x}" y="{y+r+15}" text-anchor="middle" font-size="10" fill="{HAT}">hat: {n[5]}</text>')
s.append(f'<text x="{W/2}" y="44" text-anchor="middle" font-size="24" fill="{INK}" font-weight="700" letter-spacing="3">TOPOGRAPHY · the garden, as topology</text>')
# 图例
lg = f'<g transform="translate(60,{H-58})">'
lg += f'<line x1="0" y1="0" x2="46" y2="0" stroke="{GIT}" stroke-width="3"/><text x="52" y="4" font-size="11.5" fill="{MUT}">git road (inter-polity)</text>'
lg += f'<line x1="230" y1="0" x2="276" y2="0" stroke="{SEA}" stroke-width="2" stroke-dasharray="7 6"/><text x="282" y="4" font-size="11.5" fill="{MUT}">sea route (compute abroad)</text>'
lg += f'<line x1="490" y1="0" x2="536" y2="0" stroke="{LANE}" stroke-width="1.4" stroke-dasharray="2 5"/><text x="542" y="4" font-size="11.5" fill="{MUT}">in-repo lane</text>'
lg += f'<circle cx="700" cy="0" r="10" fill="{BG}" stroke="{HAT}" stroke-width="2.6"/><circle cx="700" cy="0" r="3.4" fill="{HAT}"/><text x="716" y="4" font-size="11.5" fill="{MUT}">polity / institution</text></g>'
s.append(lg)
s.append('</svg>')
open("docs/figs/topos-flat.svg","w").write("\n".join(s))
print("wrote docs/figs/topos-flat.svg")
