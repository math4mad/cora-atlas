#!/usr/bin/env python3
"""compose_draft_body_slices.py — 给 blender 出的 3D 底版配方: 页脚带 (图例 + 中英标题脚注)。

底版: docs/figs/draft-body-slices-plate.png  (blender 渲, 2400x1350)
出图: docs/figs/draft-body-slices-{zh,en}-dark.png  (2400x1660, 页脚带另加, 不压正文)
"""
import os, csv
from PIL import Image, ImageDraw, ImageFont

D = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FIG = os.path.join(D, "docs", "figs")
PLATE = os.path.join(FIG, "draft-body-slices-plate.png")
BG = (16, 16, 23)
GOLD = (231, 195, 111)
SLATE = (150, 156, 170)
DIM = (128, 134, 148)

CJK = [("/System/Library/Fonts/Hiragino Sans GB.ttc", 0), ("/System/Library/Fonts/Supplemental/Songti.ttc", 0),
       ("/System/Library/Fonts/STHeiti Light.ttc", 0), ("/System/Library/Fonts/Supplemental/Arial Unicode.ttf", 0)]
LAT = "/System/Library/Fonts/Supplemental/Arial Unicode.ttf"
LATB = "/System/Library/Fonts/Supplemental/Arial Bold.ttf"
BAND = 290


def font(lang, size, bold=False):
    cands = (CJK if lang == "zh" else [(LATB, 0), (LAT, 0)] if bold else [(LAT, 0)]) + CJK + [(LATB, 0)]
    for p, i in cands:
        try:
            return ImageFont.truetype(p, size, index=i)
        except Exception:
            continue
    return ImageFont.load_default()


LEGEND = {
    "zh": [("tile_2544.png", "馆有真像"), ("tile_965.png", "名在像亡"), ("sil_0.png", "无名灰影")],
    "en": [("tile_2544.png", "portrait in the archive"),
           ("tile_965.png", "famous, no portrait"),
           ("sil_0.png", "every other pick")],
}
TITLE = {"zh": "总谱与剖面 · 三道刀口", "en": "Draft Body & Three Cuts"}
NOTE = {
    "zh": [
        "本体 = NBA 全部选秀（1947–2025）；三道刀口 = 三届。面孔 = 每届按生涯 ΣWAR 取最著名 12 人；同届其余作灰剪影"
        "（1984 届 216 人 / 10 轮；1996 与 2003 各 46 人 / 2 轮）。",
        "同形不同物：三个切面形状一模一样，密度与面孔却全不同；且越往过去，档案的洞越多（有像 5/12 · 10/12 · 11/12）。",
        "数据：NBA DraftHistory（stats.nba.com）· FiveThirtyEight RAPTOR（CC BY 4.0）· 头像 cdn.nba.com（NBA 版权物，本地试验）　"
        "　图：lola · cora-atlas",
    ],
    "en": [
        "Body = every NBA draft, 1947–2025; three cuts = three classes. Faces = the 12 most famous of each class by career ΣWAR; "
        "the rest appear as gray silhouettes (1984: 216 others, 10 rounds; 1996 & 2003: 46 others, 2 rounds each).",
        "Same shape, different object: the three cuts look alike, yet their density and their faces are entirely different — "
        "and the deeper you look into the past, the more holes in the archive (portraits 5/12 · 10/12 · 11/12).",
        "Data: NBA DraftHistory (stats.nba.com) · FiveThirtyEight RAPTOR (CC BY 4.0) · portraits cdn.nba.com (NBA property; local trial)"
        "    Figure: lola · cora-atlas",
    ],
}


def swatch(canvas, src, box, size):
    base = os.path.join(D, "data", "headshots") if src.startswith("tile") else os.path.join(D, "data", "silhouettes")
    im = Image.open(os.path.join(base, src)).convert("RGBA").resize((size, size), Image.LANCZOS)
    canvas.alpha_composite(im, box)


def compose(lang):
    plate = Image.open(PLATE).convert("RGBA")
    W, H = plate.size
    canvas = Image.new("RGBA", (W, H + BAND), BG + (255,))
    canvas.alpha_composite(plate, (0, 0))
    d = ImageDraw.Draw(canvas)

    y0 = H
    d.line([(0, y0), (W, y0)], fill=(58, 54, 44), width=2)
    d.text((74, y0 + 22), TITLE[lang], font=font(lang, 40, True), fill=GOLD)

    # 图例: 尽宽横排三项
    for i, (src, txt) in enumerate(LEGEND[lang]):
        lx = 74 + i * 800
        y = y0 + 92
        swatch(canvas, src, (lx, y), 44)
        d.text((lx + 58, y + 9), txt, font=font(lang, 23 if lang == "en" else 26), fill=SLATE)

    yy = y0 + 168
    for ln in NOTE[lang]:
        d.text((74, yy), ln, font=font(lang, 23), fill=DIM)
        yy += 34

    out = os.path.join(FIG, f"draft-body-slices-{lang}-dark.png")
    canvas.convert("RGB").save(out)
    print("✔", out, canvas.size)


if __name__ == "__main__":
    for lg in ("zh", "en"):
        compose(lg)
