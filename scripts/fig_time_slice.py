#!/usr/bin/env python3
"""fig_time_slice.py — 由主人草图 (Desktop/time-slice of status.jpeg) 重绘之矢量插图。
多条状态曲线 × 三处切片 (T_{n-k} · T_0 · T_1) ＋ 底部时间箭头。

变体:
  time-slice-of-status.svg            zh / dark   (碑体站)
  time-slice-of-status-en.svg         en / dark   (碑体站·英文)
  time-slice-of-status-en-light.svg   en / light  (论文·白底)
"""
import math, os

W, H = 1200, 680
X0, X1 = 90, 1120
YTOP, YBOT = 150, 470

PAL = {
    "dark":  dict(bg="#0e0f12", panel="#14161b", line="#2a2d36", ink="#d8d4c8",
                  dim="#8d8a80", gold="#c9a959", red="#b46a5a", green="#7fa07a"),
    "light": dict(bg="#ffffff", panel="#ffffff", line="#dcdcdc", ink="#1a1a1a",
                  dim="#6b6b6b", gold="#b8860b", red="#a0522d", green="#4f6f4a"),
}
SUBS = ["n−k", "0", "1"]
CURVE_ROLES = ["gold", "ink", "green", "dim", "red", "ink"]  # 6 curves
# (base_y, a1, f1, p1, a2, f2, p2)
GEO = [
    (200, 46, 1.7, 0.0, 16, 4.3, 1.1),
    (248, 34, 2.1, 0.9, 12, 5.1, 0.3),
    (296, 52, 1.4, 1.8, 14, 3.7, 2.2),
    (344, 30, 2.5, 0.4, 10, 6.0, 1.5),
    (392, 44, 1.9, 2.6, 13, 4.7, 0.7),
    (436, 28, 2.3, 1.3, 9, 5.6, 2.9),
]
SLICE_X = [300, 696, 956]

TXT = {
    "zh": dict(title="多线切片 · the multi-line slice",
               sub="状态 ＝ 各曲线在 t 处的剖面快照（slice of status）",
               axis="时间 →",
               foot="T₀ 不是冻结点，是多条曲线在此刻的切片；T₁ 的 slice 不能决定 T₀ 的 slice。"),
    "en": dict(title="The Multi-line Slice",
               sub="State = each curve's cross-section (slice) at t",
               axis="time →",
               foot="T0 is not a frozen point but a slice of many curves; T1's slice cannot determine T0's slice."),
}


def y_of(g, x):
    base, a1, f1, p1, a2, f2, p2 = g
    t = (x - X0) / (X1 - X0)
    return base + a1 * math.sin(2 * math.pi * f1 * t + p1) + a2 * math.sin(2 * math.pi * f2 * t + p2)


def path_of(g):
    xs = [X0 + (X1 - X0) * i / 240 for i in range(241)]
    return "M " + " L ".join(f"{x:.1f} {y_of(g, x):.1f}" for x in xs)


def tlabel(x, y, sub, fill, size=30):
    return (f'<text x="{x}" y="{y}" fill="{fill}" font-size="{size}" text-anchor="middle" '
            f'font-style="italic">T<tspan baseline-shift="sub" font-size="{int(size*0.62)}">{sub}</tspan></text>')


def render(lang, theme):
    p = PAL[theme]
    s = []
    s.append(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" '
             f'font-family="Palatino, Georgia, \'Songti SC\', serif">')
    s.append(f'<rect x="0" y="0" width="{W}" height="{H}" rx="14" fill="{p["panel"]}" stroke="{p["line"]}"/>')
    s.append(f'<text x="90" y="70" fill="{p["gold"]}" font-size="30" letter-spacing="3">{TXT[lang]["title"]}</text>')
    s.append(f'<text x="90" y="104" fill="{p["dim"]}" font-size="18">{TXT[lang]["sub"]}</text>')
    # 切片带
    for x, sub in zip(SLICE_X, SUBS):
        s.append(f'<rect x="{x-22}" y="{YTOP-42}" width="44" height="{YBOT-YTOP+84}" rx="16" fill="{p["gold"]}" '
                 f'fill-opacity="0.10" stroke="{p["gold"]}" stroke-opacity="0.75" stroke-width="1.6" stroke-dasharray="7 6"/>')
        s.append(tlabel(x, YTOP - 58, sub, p["gold"]))
    # 曲线
    for g, role in zip(GEO, CURVE_ROLES):
        s.append(f'<path d="{path_of(g)}" fill="none" stroke="{p[role]}" stroke-width="2.2" '
                 f'stroke-linecap="round" stroke-linejoin="round" opacity="0.92"/>')
    # 交点
    for x in SLICE_X:
        for g, role in zip(GEO, CURVE_ROLES):
            s.append(f'<circle cx="{x:.1f}" cy="{y_of(g, x):.1f}" r="4.2" fill="{p["panel"]}" '
                     f'stroke="{p[role]}" stroke-width="2"/>')
    # 时间轴
    ay = 570
    s.append(f'<line x1="{X0}" y1="{ay}" x2="{X1-14}" y2="{ay}" stroke="{p["gold"]}" stroke-width="2.6"/>')
    s.append(f'<path d="M {X1-14} {ay} l -22 -9 l 0 18 z" fill="{p["gold"]}"/>')
    s.append(f'<text x="{(X0+X1)//2}" y="{ay+38}" fill="{p["dim"]}" font-size="22" text-anchor="middle">{TXT[lang]["axis"]}</text>')
    s.append(f'<text x="90" y="{H-24}" fill="{p["dim"]}" font-size="15">{TXT[lang]["foot"]}</text>')
    s.append('</svg>')
    return "\n".join(s) + "\n"


def main():
    base = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "docs", "figs")
    os.makedirs(base, exist_ok=True)
    for name, lang, theme in [
        ("time-slice-of-status.svg", "zh", "dark"),
        ("time-slice-of-status-en.svg", "en", "dark"),
        ("time-slice-of-status-en-light.svg", "en", "light"),
    ]:
        svg = render(lang, theme)
        open(os.path.join(base, name), "w", encoding="utf-8").write(svg)
        print("✔", name, len(svg), "bytes")


if __name__ == "__main__":
    main()
