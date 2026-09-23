#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""topography-iso.py — 园体拓扑·等距版 v2 (45° 轴, 无建筑, 纯拓扑, 英语标签)
主人 09-23 定规: 等距 = 45 度投影; 图内不放建筑; 只留节点与连线; 希腊语入词汇表。"""
import math

W, H = 1280, 840
BG, INK, MUT = "#fbf7ec", "#2f2a24", "#7a6f5e"
GIT, SEA, LANE, HAT = "#b0762a", "#2E8FA3", "#b3a88f", "#8c2f2f"
TW, TH = 96, 40          # 45° 等距半格 (扁菱形)
OX, OY = 560, 110

# id, English, gx, gy, kind, hat
N = [
 ("exp",    "Field Trials",      1, 2, "lane", ""),
 ("lyc",    "Skills Registry",   4, 0, "lane", "Theuth"),
 ("mail",   "Post House",        4, 2, "lane", ""),
 ("chora",  "CHORA",             2, 2, "polity", ""),
 ("stele",  "Code of Law",       3, 4, "lane", "Hammurabi"),
 ("ledger", "Ledger",            1, 5, "lane", "Irene"),
 ("gloss",  "Glossary Steles",   0, 6, "lane", ""),
 ("itiner", "Itinerary Notes",   2, 7, "lane", ""),
 ("atlas",  "ATLAS",             1, 6, "polity", ""),
 ("onom",   "Name Register",     3, 8, "lane", "Nikos"),
 ("agora",  "Market / Stele Site",5, 6, "lane", ""),
 ("akad",   "ACADEMY",           6, 2, "polity", ""),
 ("arch",   "ARCHIVE",           7, 5, "polity", "Thea"),
 ("angel",  "Couriers Queue",    7, 3, "lane", ""),
 ("kaggle", "Forge (Kaggle)",    8, 0, "lane", ""),
 ("maca",   "Machine A",         9, 3, "lane", ""),
 ("macb",   "Machine B",         8, 6, "lane", "Nikos"),
 ("icloud", "Book Mountain",     9, 8, "lane", "Irene"),
 ("ext",    "Quarantine Port",   10, 6, "lane", ""),
]
E = [
 ("chora","exp",LANE),("chora","lyc",LANE),("chora","mail",LANE),
 ("atlas","ledger",LANE),("atlas","gloss",LANE),("atlas","itiner",LANE),("atlas","onom",LANE),
 ("atlas","stele",LANE),("chora","stele",LANE),("agora","stele",LANE),("agora","onom",LANE),
 ("akad","arch",GIT),("akad","agora",GIT),("akad","maca",GIT),("akad","macb",GIT),
 ("arch","maca",LANE),("arch","ext",LANE),
 ("maca","kaggle",SEA),("macb","kaggle",SEA),("macb","ext",LANE),
 ("icloud","ext",LANE),("angel","kaggle",GIT),("angel","arch",LANE),
 ("akad","angel",GIT),
]
def iso(gx, gy): return OX + (gx-gy)*TW, OY + (gx+gy)*TH
pos = {n[0]: iso(n[2], n[3]) for n in N}

def route(a, b):
    """沿 45° 等距轴折线: 先走 u 向再走 v 向 (地铁图正典笔法)。"""
    g1 = (N_[a][2], N_[a][3]); g2 = (N_[b][2], N_[b][3])
    p0 = pos[a]
    pm = iso(g2[0], g1[1])          # 拐点: 混合格坐标 => 两段皆沿轴
    p2 = pos[b]
    return f'M{p0[0]},{p0[1]} L{pm[0]},{pm[1]} L{p2[0]},{p2[1]}'
N_ = {n[0]: n for n in N}

s = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" font-family="Helvetica Neue, Helvetica, Arial, sans-serif">',
     f'<rect width="{W}" height="{H}" fill="{BG}"/>']
# 45° 底纹格 (淡)
for g in range(-2, 15):
    a, b = iso(g, -2), iso(g, 14)
    s.append(f'<line x1="{a[0]}" y1="{a[1]}" x2="{b[0]}" y2="{b[1]}" stroke="{INK}" opacity=".05"/>')
    a, b = iso(-2, g), iso(14, g)
    s.append(f'<line x1="{a[0]}" y1="{a[1]}" x2="{b[0]}" y2="{b[1]}" stroke="{INK}" opacity=".05"/>')
# 边
for a, b, c in E:
    dash = ' stroke-dasharray="8 6"' if c == SEA else (' stroke-dasharray="2 5"' if c == LANE else "")
    wd = 3 if c == GIT else (2 if c == SEA else 1.4)
    s.append(f'<path d="{route(a,b)}" fill="none" stroke="{c}" stroke-width="{wd}"{dash} opacity="{0.9 if c!=LANE else 0.7}"/>')
# 节点: 政体=菱形双环, 机构=圆, 帽=小注
for n in N:
    x, y = pos[n[0]]
    if n[4] == "polity":
        s.append(f'<path d="M{x},{y-16} L{x+16},{y} L{x},{y+16} L{x-16},{y} Z" fill="{BG}" stroke="{HAT}" stroke-width="2.8"/>')
        s.append(f'<path d="M{x},{y-8} L{x+8},{y} L{x},{y+8} L{x-8},{y} Z" fill="{HAT}"/>')
    else:
        s.append(f'<circle cx="{x}" cy="{y}" r="7" fill="{BG}" stroke="{INK}" stroke-width="2.2"/>')
    dy = -22 if n[4] == "polity" else -14
    s.append(f'<text x="{x}" y="{y+dy}" text-anchor="middle" font-size="13.5" fill="{INK}" font-weight="700">{n[1]}</text>')
    if n[5]:
        s.append(f'<text x="{x}" y="{y+26}" text-anchor="middle" font-size="10" fill="{HAT}">hat: {n[5]}</text>')
s.append(f'<text x="{W/2}" y="46" text-anchor="middle" font-size="24" fill="{INK}" font-weight="700" letter-spacing="3">ISO-TOPOLOGY · 45° · no buildings, only relations</text>')
lg = f'<g transform="translate(60,{H-52})">'
lg += f'<line x1="0" y1="0" x2="44" y2="0" stroke="{GIT}" stroke-width="3"/><text x="50" y="4" font-size="11.5" fill="{MUT}">git road</text>'
lg += f'<line x1="140" y1="0" x2="184" y2="0" stroke="{SEA}" stroke-width="2" stroke-dasharray="8 6"/><text x="190" y="4" font-size="11.5" fill="{MUT}">sea route</text>'
lg += f'<line x1="290" y1="0" x2="334" y2="0" stroke="{LANE}" stroke-width="1.4" stroke-dasharray="2 5"/><text x="340" y="4" font-size="11.5" fill="{MUT}">in-repo lane</text>'
lg += f'<path d="M450,-9 L459,0 L450,9 L441,0 Z" fill="{HAT}"/><text x="468" y="4" font-size="11.5" fill="{MUT}">polity</text></g>'
s.append(lg)
s.append('</svg>')
open("docs/figs/topos-iso.svg", "w").write("\n".join(s))
print("wrote docs/figs/topos-iso.svg (45°, 无建筑)")
