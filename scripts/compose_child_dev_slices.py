#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""compose_child_dev_slices.py — 给 Blender 底版加月份标签 + 页脚带（两趟法）。

底版: docs/figs/child-dev-slices-3d/<VER>/plate.png (Blender 渲, 2400x1350)
出图: docs/figs/child-dev-slices-3d/<VER>/child-dev-slices-3d-{zh,en}.png (2400x1640)
用法: VER=v03 python3 scripts/compose_child_dev_slices.py
"""
import os, json
from PIL import Image, ImageDraw, ImageFont

D = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FIG = os.path.join(D, "docs", "figs", "child-dev-slices-3d")
VER = os.environ.get("VER", "v03")
BG = (16, 16, 23); GOLD = (231, 195, 111); SLATE = (150, 156, 170); DIM = (128, 134, 148)
BAND = 300
METRIC_RGB = [(0.08, 0.52, 0.46), (0.15, 0.40, 0.66), (0.42, 0.30, 0.60),
              (0.84, 0.42, 0.10), (0.70, 0.22, 0.24)]
METRICS = ["词汇量", "MLU", "词类多样性", "句法复杂度", "指代清晰度"]
CJK = [("/System/Library/Fonts/Hiragino Sans GB.ttc", 0),
       ("/System/Library/Fonts/Supplemental/Songti.ttc", 0)]


def font(size):
    for p, i in CJK:
        try:
            return ImageFont.truetype(p, size, index=i)
        except Exception:
            continue
    return ImageFont.load_default()


def main():
    vdir = os.path.join(FIG, VER)
    plate = Image.open(os.path.join(vdir, "plate.png")).convert("RGB")
    labels = json.load(open(os.path.join(vdir, "labels.json")))
    W, H = plate.size
    canvas = Image.new("RGB", (W, H + BAND), BG)
    canvas.paste(plate, (0, 0))
    d = ImageDraw.Draw(canvas)

    # 月份标签（投影位；描边保证在深底上可读）
    for L in labels:
        if L["kind"] != "month":
            continue
        x, y = L["px"], L["py"]
        for dx in (-2, 0, 2):
            for dy in (-2, 0, 2):
                d.text((x + dx, y + dy), L["text"], font=font(34), fill=(10, 12, 16), anchor="mm")
        d.text((x, y), L["text"], font=font(34), fill=GOLD, anchor="mm")

    # 页脚带
    d.text((56, H + 30), "儿童发展 · 切片柱阵（Blender 3D）", font=font(52), fill=GOLD)
    d.text((56, H + 104), "本体＝发展时间长河（月龄 12 → 42）· 六道刀口＝六月龄阶段 · "
                          "切面之上五指标各立一方柱（柱高 ∝ 值）", font=font(28), fill=SLATE)
    lx = 56
    for mi, m in enumerate(METRICS):
        col = tuple(int(255 * v) for v in METRIC_RGB[mi])
        d.rectangle([lx, H + 168, lx + 26, H + 194], fill=col)
        d.text((lx + 36, H + 160), m, font=font(26), fill=SLATE)
        lx += 40 + 24 * len(m) + 60
    d.text((56, H + 224), "概念演示：看「变化」与「轴趋势」，非精确读数　·　"
                          "数据＝本地 CHILDES（各指标自身 max 归一，仅作形状/高低）　·　"
                          f"ver {VER} · lola 2026-10-03", font=font(24), fill=DIM)
    canvas.save(os.path.join(vdir, "child-dev-slices-3d-zh.png"))
    print("→", os.path.join(vdir, "child-dev-slices-3d-zh.png"), canvas.size)


if __name__ == "__main__":
    main()
