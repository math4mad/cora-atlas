#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""topography-iso.py — 园体地形志·等距微缩版 (平面化/建筑小/间距紧/拓扑优先)
网格坐标 (gx,gy) → 等距菱形棋盘; 数据与 topography.py 同源 (NODES 增补网格)。
输出 docs/figs/topos-iso.svg"""

W, H = 1280, 860
PARCH, INK, GOLD, RED, BLUE, GREEN = "#f6efdf", "#3a3128", "#b0762a", "#8c2f2f", "#2E8FA3", "#6f8f5a"
TW, TH, OX, OY = 78, 44, 640, 150  # 半格宽/半格高/原点

# id, 汉, 希腊, gx, gy, 类型, 色组
N = [
 ("exp",    "实验田",   "οἱ ἀγροί",      1, 1, "fields", GREEN),
 ("chora",  "本域",     "ἡ Χώρα",        2, 2, "land",   GOLD),
 ("lyc",    "职册署",   "Λύκειον",       3, 0, "hall",   INK),
 ("mail",   "驿馆",     "σταθμός",       4, 2, "hall",   INK),
 ("steleH", "汉谟拉比柱","ἡ Στήλη",       3, 3, "stele",  GOLD),
 ("ledger", "台账广场", "Δελτοί",        1, 4, "city",   RED),
 ("gloss",  "术语碑林", "Λεξικόν",       0, 6, "steles", INK),
 ("atlas",  "碑园",     "ἡ Ἀτλαντίς",    2, 6, "land",   GOLD),
 ("itiner", "手记驿道", "ἱστορική ὁδός", 1, 7, "road",   INK),
 ("agora",  "市集",     "ἡ Ἀγορά",       3, 6, "city",   RED),
 ("onom",   "正名表",   "Ὀνοματολόγιον", 4, 8, "steles", INK),
 ("akad",   "学园",     "Ἀκαδημία",      6, 3, "temple", GOLD),
 ("angel",  "天使道",   "Ἀγγέλων ὁδός",  6, 5, "road",   INK),
 ("arch",   "档案馆",   "Ἀρχεῖον",       7, 6, "temple", GOLD),
 ("kaggle", "火神庙",   "Πυραεῖον",      8, 0, "forge",  RED),
 ("maca",   "双神·甲",  "Διόσκουρος α′", 9, 3, "city",   BLUE),
 ("macb",   "双神·乙",  "Διόσκουρος β′", 8, 7, "city",   BLUE),
 ("icloud", "书山",     "βιβλίων ὄρος",  9, 8, "mount",  GOLD),
 ("ext",    "检疫港",   "ὁ λιμήν",       7, 9, "port",   BLUE),
]
E = [
 ("chora","exp","lane",""),("chora","lyc","lane",""),("chora","mail","lane",""),
 ("atlas","ledger","lane",""),("atlas","gloss","lane",""),("atlas","itiner","lane",""),
 ("atlas","onom","lane",""),("atlas","steleH","lane",""),
 ("akad","arch","road","git"),("akad","agora","road","git"),
 ("akad","maca","road","git"),("akad","macb","road","git"),
 ("arch","maca","lane",""),("arch","ext","lane","存目"),
 ("maca","kaggle","sea","σπέρματα→ἔργα"),("macb","kaggle","sea","分遣"),
 ("macb","ext","lane","检疫"),("icloud","ext","lane","pin"),
 ("angel","kaggle","road","斥候"),("angel","arch","lane",""),
 ("agora","steleH","lane",""),("agora","onom","lane",""),
]
pos = {n[0]: (n[3], n[4]) for n in N}
def iso(gx, gy): return OX + (gx-gy)*TW, OY + (gx+gy)*TH

def glyph(id_, cn, gr, x, y, t, c):
    if t=="temple":  # 小庙: 山花+四柱
        g=f'<rect x="{x-16}" y="{y-12}" width="32" height="18" fill="#fff" opacity=".65" stroke="{INK}"/><path d="M{x-18},{y-12} L{x},{y-24} L{x+18},{y-12} Z" fill="{c}" stroke="{INK}"/>'
        for i in range(4): g+=f'<rect x="{x-13+i*8}" y="{y-10}" width="3" height="15" fill="{INK}" opacity=".8"/>'
    elif t=="city":
        g=f'<rect x="{x-13}" y="{y-10}" width="26" height="16" fill="#fff" opacity=".7" stroke="{INK}"/><path d="M{x-13},{y-10} L{x},{y-20} L{x+13},{y-10} Z" fill="{c}" stroke="{INK}"/>'
    elif t=="hall":
        g=f'<rect x="{x-11}" y="{y-8}" width="22" height="13" fill="#fff" opacity=".7" stroke="{INK}"/><path d="M{x-12},{y-8} L{x},{y-16} L{x+12},{y-8}" fill="none" stroke="{INK}"/>'
    elif t=="land":
        g=f'<path d="M{x},{y-26} L{x+34},{y} L{x},{y+26} L{x-34},{y} Z" fill="{c}" opacity=".16" stroke="{c}" stroke-dasharray="4 3"/>'
    elif t=="mount":
        g=f'<path d="M{x-20},{y+10} L{x-4},{y-18} L{x+4},{y-4} L{x+14},{y-16} L{x+24},{y+10} Z" fill="{c}" opacity=".7" stroke="{INK}"/>'
    elif t=="forge":
        g=f'<path d="M{x-14},{y+8} L{x-7},{y-14} L{x+7},{y-14} L{x+14},{y+8} Z" fill="#e8d8b6" stroke="{RED}"/><path d="M{x},{y-16} q6,-10 0,-16 q10,6 4,18" fill="{RED}"/>'
    elif t=="port":
        g=f'<circle cx="{x}" cy="{y-4}" r="10" fill="none" stroke="{BLUE}" stroke-width="2.5"/><path d="M{x},{y-18} v28 M{x-9},{y+6} q9,8 18,0" stroke="{BLUE}" stroke-width="2" fill="none"/>'
    elif t=="fields":
        g=f'<path d="M{x-22},{y} L{x},{y-12} L{x+22},{y} L{x},{y+12} Z" fill="{c}" opacity=".3" stroke="{INK}"/>'
        for i in range(3): g+=f'<path d="M{x-15+i*10},{y+7-i*3} q15,-8 30,0" stroke="{c}" fill="none"/>'
    elif t=="steles":
        g="".join(f'<rect x="{x-14+i*11}" y="{y-14+(0 if i==1 else 3)}" width="7" height="{18 if i==1 else 14}" fill="#e6d9b6" stroke="{INK}"/>' for i in range(3))
    elif t=="stele":
        g=f'<rect x="{x-5}" y="{y-22}" width="10" height="30" rx="2" fill="#d8c9a4" stroke="{INK}"/><circle cx="{x}" cy="{y-16}" r="3" fill="{GOLD}"/>'
    else:
        g=f'<circle cx="{x}" cy="{y-4}" r="4" fill="{c}"/>'
    g+=f'<text x="{x}" y="{y+22}" text-anchor="middle" font-size="12.5" fill="{INK}" font-weight="600">{gr}</text>'
    g+=f'<text x="{x}" y="{y+35}" text-anchor="middle" font-size="10" fill="#6b5f4d">{cn}</text>'
    return g

s=[f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" font-family="Hiragino Sans GB, PingFang SC, serif">',
   f'<rect width="{W}" height="{H}" fill="{PARCH}"/>']
# 棋盘底 (淡网格)
for gx in range(11):
    a=iso(gx,0); b=iso(gx,10)
    s.append(f'<line x1="{a[0]}" y1="{a[1]}" x2="{b[0]}" y2="{b[1]}" stroke="{INK}" opacity=".07"/>')
for gy in range(11):
    a=iso(0,gy); b=iso(10,gy)
    s.append(f'<line x1="{a[0]}" y1="{a[1]}" x2="{b[0]}" y2="{b[1]}" stroke="{INK}" opacity=".07"/>')
# 边
for a,b,st,note in E:
    x1,y1=iso(*pos[a]); x2,y2=iso(*pos[b])
    col={"road":GOLD,"sea":BLUE,"lane":"#9a8a6e"}[st]
    dash=' stroke-dasharray="6 5"' if st=="sea" else (' stroke-dasharray="2 4"' if st=="lane" else "")
    wd=2.6 if st=="road" else 1.6
    s.append(f'<line x1="{x1}" y1="{y1-6}" x2="{x2}" y2="{y2-6}" stroke="{col}" stroke-width="{wd}" opacity=".85"{dash}/>')
    if note:
        s.append(f'<text x="{(x1+x2)/2}" y="{(y1+y2)/2-8}" font-size="9.5" fill="{col}" text-anchor="middle" font-style="italic">{note}</text>')
for n in N:
    x,y=iso(n[3],n[4]); s.append(glyph(*n[:6],n[5]))
s.append(f'<text x="{W/2}" y="52" text-anchor="middle" font-size="26" fill="{INK}" font-weight="700" letter-spacing="4">ΙΣΟΤΟΠΟΣ · 园体地形·等距微缩</text>')
s.append(f'<text x="{W/2}" y="76" text-anchor="middle" font-size="12" fill="#6b5f4d">平面化 · 建筑缩小 · 间距收紧 · 只留拓扑 — 数据同源 scripts/topography.py</text>')
s.append('</svg>')
open("docs/figs/topos-iso.svg","w").write("\n".join(s))
print("wrote docs/figs/topos-iso.svg")
