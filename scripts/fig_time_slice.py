#!/usr/bin/env python3
"""fig_time_slice.py — 由主人草图 (Desktop/time-slice of status.jpeg) 重绘之矢量插图:
多条状态曲线 × 三处切片 (t_{n-k} · t_0 · t_1) ＋ 底部时间箭头。
输出: docs/figs/time-slice-of-status.svg  (碑体站色板: 暗盘 #0e0f12/金 #c9a959)
"""
import math, os

W, H = 1200, 680
X0, X1 = 90, 1120
YTOP, YBOT = 150, 470          # 曲线活动带

BG, PANEL, LINE = "#0e0f12", "#14161b", "#2a2d36"
INK, DIM, GOLD, RED, GREEN = "#d8d4c8", "#8d8a80", "#c9a959", "#b46a5a", "#7fa07a"

# (base_y, a1, f1, p1, a2, f2, p2, color, width)
CURVES = [
    (200, 46, 1.7, 0.0, 16, 4.3, 1.1, GOLD, 2.4),
    (248, 34, 2.1, 0.9, 12, 5.1, 0.3, INK, 2.0),
    (296, 52, 1.4, 1.8, 14, 3.7, 2.2, GREEN, 2.0),
    (344, 30, 2.5, 0.4, 10, 6.0, 1.5, DIM, 1.8),
    (392, 44, 1.9, 2.6, 13, 4.7, 0.7, RED, 2.0),
    (436, 28, 2.3, 1.3, 9, 5.6, 2.9, INK, 1.7),
]

SLICES = [(300, "t"), (696, "t"), (956, "t")]  # (x, prefix)
SLICE_LABELS = ["tₙ₋ₖ", "t₀", "t₁"]


def y_of(c, x):
    base, a1, f1, p1, a2, f2, p2 = c[0], c[1], c[2], c[3], c[4], c[5], c[6]
    t = (x - X0) / (X1 - X0)
    return base + a1 * math.sin(2 * math.pi * f1 * t + p1) + a2 * math.sin(2 * math.pi * f2 * t + p2)


def path_of(c):
    xs = [X0 + (X1 - X0) * i / 240 for i in range(241)]
    return "M " + " L ".join(f"{x:.1f} {y_of(c, x):.1f}" for x in xs)


s = []
s.append(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" font-family="Palatino, Georgia, \'Songti SC\', serif">')
s.append(f'<rect x="0" y="0" width="{W}" height="{H}" rx="14" fill="{PANEL}" stroke="{LINE}"/>')
# 标题
s.append(f'<text x="90" y="70" fill="{GOLD}" font-size="30" letter-spacing="3">多线切片 · the multi-line slice</text>')
s.append(f'<text x="90" y="104" fill="{DIM}" font-size="18">状态 ＝ 各曲线在 t 处的剖面快照（slice of status）</text>')

# 切片带 (画在曲线之下)
for (x, _), lab in zip(SLICES, SLICE_LABELS):
    s.append(f'<rect x="{x-22}" y="{YTOP-42}" width="44" height="{YBOT-YTOP+84}" rx="16" fill="{GOLD}" fill-opacity="0.10" stroke="{GOLD}" stroke-opacity="0.75" stroke-width="1.6" stroke-dasharray="7 6"/>')
    s.append(f'<text x="{x}" y="{YTOP-58}" fill="{GOLD}" font-size="30" text-anchor="middle" font-style="italic">{lab}</text>')

# 曲线
for c in CURVES:
    s.append(f'<path d="{path_of(c)}" fill="none" stroke="{c[7]}" stroke-width="{c[8]}" stroke-linecap="round" stroke-linejoin="round" opacity="0.9"/>')

# 切片与曲线之交点 (剖面读数)
for (x, _) in SLICES:
    for c in CURVES:
        y = y_of(c, x)
        s.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="4.2" fill="{BG}" stroke="{c[7]}" stroke-width="2"/>')

# 时间轴箭头
ax_y = 570
s.append(f'<line x1="{X0}" y1="{ax_y}" x2="{X1-14}" y2="{ax_y}" stroke="{GOLD}" stroke-width="2.6"/>')
s.append(f'<path d="M {X1-14} {ax_y} l -22 -9 l 0 18 z" fill="{GOLD}"/>')
s.append(f'<text x="{(X0+X1)//2}" y="{ax_y+38}" fill="{DIM}" font-size="22" text-anchor="middle">时间 →</text>')

# 脚注
s.append(f'<text x="90" y="{H-24}" fill="{DIM}" font-size="15">T₀ 不是冻结点，是多条曲线在此刻的切片；T₁ 的 slice 不能决定 T₀ 的 slice。</text>')
s.append('</svg>')

out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "docs", "figs", "time-slice-of-status.svg")
open(out, "w", encoding="utf-8").write("\n".join(s) + "\n")
print("✔", os.path.normpath(out), len("\n".join(s)), "bytes")
