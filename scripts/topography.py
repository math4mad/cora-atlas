#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""topography.py — 园体地形志发生器 (Mathematistan 风幻想制图 + 力导向关系图)
数据即地图: 改 NODES/EDGES 重跑, 图随政体生长。输出 docs/figs/topos.svg, topos-graph.svg
"""
import math, random

W, H = 1480, 1000
PARCH, INK, SEA, GOLD, RED, BLUE = "#f0e6d0", "#3a3128", "#cfd8cf", "#b05f24", "#8c2f2f", "#2E8FA3"

# (id, 中文名, 希腊名, x, y, 类型, 注记)
NODES = [
    ("agora",   "市集·碑站", "ἡ Ἀγορά",           430, 640, "city",  "Στήλη 发布 · 公开立言"),
    ("akad",    "学园",       "ἡ Ἀκαδημία",        760, 380, "temple", "Παιδεία·Προσαγωγή·Βιβλιοφυλακή·Τέχνη"),
    ("arch",    "档案馆",     "Τὸ Ἀρχεῖον",        1090, 590, "temple", "Ἐπιστολαί·Γραφαί·Νόμοι·Κατάλογοι"),
    ("chora",   "本域",       "ἡ Χώρα",            420, 300, "land",   "实验本域"),
    ("exp",     "实验田",     "οἱ ἀγροί",          250, 210, "fields", "experiments/ 诸案"),
    ("lyc",     "职册署",     "Λύκειον",           590, 175, "hall",   "Theuth 席位 · skill 册"),
    ("mail",    "驿馆",       "τὸ σταθμός",        610, 400, "hall",   "mail.sh · 信=md=commit"),
    ("atlas",   "碑园",       "ἡ Ἀτλαντίς",        250, 560, "land",   "账本与正刊"),
    ("ledger",  "台账广场",   "Δελτοί",            150, 480, "city",   "C38-C43 · 事件账"),
    ("gloss",   "术语碑林",   "Λεξικόν",           150, 650, "steles", "凿刻体 · 同架串门"),
    ("itiner",  "手记驿道",   "ὁδὸς ἱστορική",     350, 720, "road",   "iterations/ 23+ 石"),
    ("onom",    "正名表碑亭", "Ὀνοματολόγιον",     560, 800, "steles", "名从希腊 · 路不改名"),
    ("kaggle",  "火神庙",     "Τὸ Πυραεῖον",       1290, 210, "forge", "Kaggle · 26h 额度租火"),
    ("macb",    "双子神·乙",  "Διόσκουρος β'",      950, 760, "city",  "m1-16g · 三臂在耕"),
    ("maca",    "双子神·甲",  "Διόσκουρος α'",      1290, 430, "city", "m1pro-32g · 锻造座"),
    ("icloud",  "书山",       "βιβλίων ὄρος",      1180, 900, "mount", "iCloud 283 册·假说之矿"),
    ("ext",     "检疫港",     "ὁ λιμήν",           820, 905, "port",  "external/ · pin 海关"),
    ("angel",   "天使道",     "ὁδὸς Ἀγγέλων",      800, 540, "road",  "queue.py · 信使与斥候"),
    ("steleH",  "汉谟拉比柱", "ἡ Στήλη",            330, 430, "stele", "判据先冻 · 刻石为证"),
]
EDGES = [  # (from, to, 样式, 注)
    ("chora", "exp", "path", ""), ("chora", "lyc", "path", ""), ("chora", "mail", "path", ""),
    ("atlas", "ledger", "path", ""), ("atlas", "gloss", "path", ""), ("atlas", "itiner", "path", ""),
    ("atlas", "onom", "path", ""), ("atlas", "steleH", "path", ""),
    ("akad", "arch", "road", "git"), ("akad", "agora", "road", "git"),
    ("akad", "maca", "road", "git"), ("akad", "macb", "road", "git"),
    ("arch", "maca", "path", ""), ("arch", "ext", "path", "存目"),
    ("maca", "kaggle", "sea", "σπέρματα↔ἔργα"), ("macb", "kaggle", "sea", "分遣"),
    ("macb", "ext", "path", "检疫"), ("icloud", "ext", "path", "pin 海关"),
    ("angel", "kaggle", "road", "斥候"), ("angel", "arch", "path", ""),
    ("agora", "steleH", "path", ""), ("agora", "onom", "path", ""),
]

def svg_head():
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" '
            f'viewBox="0 0 {W} {H}" font-family="Hiragino Sans GB, PingFang SC, serif">')

def glyph(n):
    x, y = n[3], n[4]; t = n[5]
    if t == "land":
        return f'<ellipse cx="{x}" cy="{y}" rx="150" ry="95" fill="#e6d9b8" stroke="{INK}" stroke-width="1.4" stroke-dasharray="4 3"/>'
    if t == "mount":
        return (f'<path d="M{x-70},{y+40} L{x-25},{y-40} L{x},y-5 L{x+28},{y-48} L{x+70},{y+40} Z" fill="#d9cbaa" stroke="{INK}" stroke-width="1.4"/>'
                f'<path d="M{x-25},{y-40} L{x-12},{y-18} L{x-38},{y-18} Z" fill="#fff" opacity=".7"/>')
    if t == "city":
        return (f'<rect x="{x-46}" y="{y-26}" width="92" height="52" rx="6" fill="#eadfc4" stroke="{INK}" stroke-width="1.6"/>'
                f'<path d="M{x-46},{y-26} L{x},{y-52} L{x+46},{y-26}" fill="#d9c9a3" stroke="{INK}" stroke-width="1.4"/>')
    if t in ("temple", "hall"):
        s = 1.0 if t == "temple" else .78
        cols = "".join(f'<rect x="{x-40*s+i*20*s}" y="{y-18*s}" width="7" height="{36*s}" fill="{INK}" opacity=".85"/>' for i in range(5))
        return (f'<rect x="{x-52*s}" y="{y-30*s}" width="{104*s}" height="{60*s}" rx="4" fill="#f3ead2" stroke="{INK}" stroke-width="1.5"/>'
                f'<path d="M{x-56*s},{y-30*s} L{x},{y-52*s} L{x+56*s},{y-30*s} Z" fill="#e0d0ac" stroke="{INK}" stroke-width="1.4"/>{cols}')
    if t == "forge":
        return (f'<path d="M{x-40},{y+30} L{x-22},{y-30} L{x+22},{y-30} L{x+40},{y+30} Z" fill="#e3cfa8" stroke="{RED}" stroke-width="1.6"/>'
                f'<path d="M{x-8},{y-34} q8,-16 0,-26 q18,10 10,30" fill="{RED}" opacity=".8"/>')
    if t == "port":
        return (f'<circle cx="{x}" cy="{y}" r="34" fill="none" stroke="{BLUE}" stroke-width="3"/>'
                f'<path d="M{x},{y-44} v88 M{x-30},{y+18} q30,26 60,0" stroke="{BLUE}" stroke-width="3" fill="none"/>')
    if t == "fields":
        rows = "".join(f'<path d="M{x-52+i*4},{y+34-i*13} q52,-14 104,0" stroke="{INK}" stroke-width="1.1" fill="none" opacity=".7"/>' for i in range(6))
        return f'<rect x="{x-58}" y="{y-38}" width="116" height="76" rx="8" fill="#e7dcc0" stroke="{INK}" stroke-width="1.2"/>{rows}'
    if t == "steles":
        return "".join(f'<rect x="{x-46+i*30}" y="{y-26}" width="18" height="{52-6*abs(i-1)}" rx="3" fill="#dcd0b2" stroke="{INK}" stroke-width="1.3"/>' for i in range(3))
    if t == "stele":
        return (f'<rect x="{x-16}" y="{y-56}" width="32" height="112" rx="6" fill="#d8c9a4" stroke="{INK}" stroke-width="1.8"/>'
                f'<circle cx="{x}" cy="{y-40}" r="8" fill="{GOLD}"/>')
    if t == "road":
        return ""
    return ""

def label(n):
    x, y = n[3], n[4]
    dy = 66 if n[5] not in ("land",) else 0
    anchor = "middle"
    g = (f'<text x="{x}" y="{y-dy if n[5]=="land" else y-62}" text-anchor="{anchor}" font-size="19" fill="{INK}" font-weight="600">{n[2]}</text>'
         f'<text x="{x}" y="{y-dy+20 if n[5]=="land" else y-42}" text-anchor="{anchor}" font-size="14" fill="{INK}">{n[1]}</text>')
    if n[6]:
        g += f'<text x="{x}" y="{y+ (74 if n[5]!="land" else -80)}" text-anchor="middle" font-size="11" fill="#6b5f4d" font-style="italic">{n[6]}</text>'
    return g

def edges_svg(pos):
    out = []
    for a, b, style, note in EDGES:
        x1, y1 = pos[a][:2]; x2, y2 = pos[b][:2]
        mx, my = (x1+x2)/2 + (y2-y1)*.12, (y1+y2)/2 - (x2-x1)*.12
        dash = ' stroke-dasharray="7 6"' if style == "sea" else (' stroke-dasharray="2 5"' if style == "path" else "")
        col = BLUE if style == "sea" else (GOLD if style == "road" else "#7a6a52")
        wdt = 2.2 if style == "road" else 1.5
        out.append(f'<path d="M{x1},{y1} Q{mx},{my} {x2},{y2}" fill="none" stroke="{col}" stroke-width="{wdt}" opacity=".75"{dash}/>')
        if note:
            out.append(f'<text x="{mx}" y="{my-4}" font-size="10" fill="{col}" text-anchor="middle" font-style="italic">{note}</text>')
    return "".join(out)

def main():
    pos = {n[0]: (n[3], n[4]) for n in NODES}
    s = [svg_head()]
    s.append(f'<rect width="{W}" height="{H}" fill="{PARCH}"/>')
    s.append(f'<path d="M1010,0 H{W} V470 Q1160,540 960,500 Z" fill="{SEA}" opacity=".55"/>')
    s.append(f'<text x="1215" y="120" font-size="15" fill="{BLUE}" font-style="italic" transform="rotate(12 1215 120)">ὁ πλοῦς τοῦ πυρός · 火神航线</text>')
    s.append('<rect x="14" y="14" width="%d" height="%d" fill="none" stroke="%s" stroke-width="3"/><rect x="24" y="24" width="%d" height="%d" fill="none" stroke="%s" stroke-width="1"/>' % (W-28, H-28, INK, W-48, H-48, INK))
    s.append(f'<text x="{W/2}" y="66" text-anchor="middle" font-size="30" fill="{INK}" font-weight="700" letter-spacing="6">ΤΟΠΟΓΡΑΦΊΑ · 园体地形志</text>')
    s.append(f'<text x="{W/2}" y="92" text-anchor="middle" font-size="13" fill="#6b5f4d">συμπολιτεία chart · 人·机·账同图 · 2026-09-23 (数据驱动: scripts/topography.py)</text>')
    s.append(edges_svg(pos))
    for n in NODES:
        s.append(glyph(n))
    for n in NODES:
        s.append(label(n))
    s.append(f'<g transform="translate({W-120},{H-130})"><path d="M0,-46 L10,-10 L46,0 L10,10 L0,46 L-10,10 L-46,0 L-10,-10 Z" fill="#e0d0ac" stroke="{INK}"/><text x="0" y="-52" text-anchor="middle" font-size="13" fill="{INK}">Β</text></g>')
    s.append('</svg>')
    open("docs/figs/topos.svg", "w").write("\n".join(s))

    # 力导向关系图 (第二视图: 拓扑而非地理)
    random.seed(43)
    P = {n[0]: [random.uniform(150, W-150), random.uniform(150, H-150)] for n in NODES}
    for it in range(380):
        ks = list(P)
        for a in ks:
            fx = fy = 0.0
            for b in ks:
                if a == b: continue
                dx, dy = P[a][0]-P[b][0], P[a][1]-P[b][1]
                d2 = max(dx*dx+dy*dy, 400)
                f = 2600/d2
                fx += dx*f; fy += dy*f
            for a2, b2, st, _ in EDGES:
                if a2 == a or b2 == a:
                    o = b2 if a2 == a else a2
                    dx, dy = P[o][0]-P[a][0], P[o][1]-P[a][1]
                    d = max(math.hypot(dx, dy), 1)
                    f = (d-190)*0.012
                    fx += dx/d*f*40; fy += dy/d*f*40
            P[a][0] = max(90, min(W-90, P[a][0]+fx*0.5)); P[a][1] = max(110, min(H-70, P[a][1]+fy*0.5))
    g2 = [svg_head(), f'<rect width="{W}" height="{H}" fill="#fbf6ea"/>']
    for a, b, st, note in EDGES:
        col = BLUE if st == "sea" else (GOLD if st == "road" else "#9a8a6e")
        g2.append(f'<line x1="{P[a][0]:.0f}" y1="{P[a][1]:.0f}" x2="{P[b][0]:.0f}" y2="{P[b][1]:.0f}" stroke="{col}" stroke-width="{"2.4" if st=="road" else "1.4"}" opacity=".8"/>')
    for n in NODES:
        x, y = P[n[0]]
        col = {"land": "#c9b98a", "city": RED, "temple": GOLD, "hall": "#7a6a52", "forge": RED,
               "mount": "#8a7a52", "port": BLUE, "fields": "#7f9a5c", "steles": "#6b5f4d",
               "stele": GOLD, "road": "#9a8a6e"}[n[5]]
        g2.append(f'<circle cx="{x:.0f}" cy="{y:.0f}" r="9" fill="{col}" stroke="{INK}"/>')
        g2.append(f'<text x="{x+13:.0f}" y="{y+5:.0f}" font-size="14" fill="{INK}">{n[2]} {n[1]}</text>')
    g2.append(f'<text x="{W/2}" y="50" text-anchor="middle" font-size="22" fill="{INK}" font-weight="700">园体关系拓扑 (力导向 · 距离=耦合之反)</text>')
    g2.append('</svg>')
    open("docs/figs/topos-graph.svg", "w").write("\n".join(g2))
    print("wrote docs/figs/topos.svg + topos-graph.svg")

if __name__ == "__main__":
    main()
