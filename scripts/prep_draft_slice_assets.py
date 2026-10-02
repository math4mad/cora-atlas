#!/usr/bin/env python3
"""prep_draft_slice_assets.py — 为 blender 切片图备料:
  · data/headshots/tile_{pid}.png    头像 + 金环 (圆裁, 名人用)
  · data/silhouettes/sil_{k}.png     灰剪影 (无名者用, 非真人照片)
"""
import os, csv, random
from PIL import Image, ImageDraw

D = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
HS = os.path.join(D, "data", "headshots")
SV = os.path.join(D, "data", "silhouettes")
SIZE = 320
GOLD = (217, 181, 97)
SLATE = (122, 130, 146)       # 「档案无像」之环色
FLAT_SD = 12                  # 占位图判据: 不透明像素 R 信道标准差 < 12


def is_placeholder(im):
    """cdn.nba.com 对无官方头像者返回同一张平灰剪影 (md5 37c8168532, sd 0.6)。"""
    import statistics
    op = [p for p in im.convert("RGBA").getdata() if p[3] > 200]
    if len(op) < 100:
        return True
    return statistics.pstdev([p[0] for p in op]) < FLAT_SD


def ring_tile(pid):
    src = os.path.join(HS, f"{pid}.png")
    if not os.path.exists(src):
        return None, False
    im = Image.open(src).convert("RGBA")
    missing = is_placeholder(im)
    S = SIZE * 4
    im = im.resize((S, S), Image.LANCZOS)
    if missing:                                   # 无像: 压暗去色, 成灰影
        r, g, b, a = im.split()
        gray = Image.merge("RGB", (r, g, b)).convert("L")
        tint = Image.new("RGB", (S, S), (86, 94, 110))
        im = Image.merge("RGBA", (*Image.blend(Image.merge("RGB", (gray, gray, gray)), tint, 0.55).split(), a))
        im.putalpha(im.getchannel("A").point(lambda v: int(v * 0.75)))
    ring = Image.new("RGBA", (S, S), (0, 0, 0, 0))
    d = ImageDraw.Draw(ring)
    w = int(S * 0.030)
    box = (w // 2, w // 2, S - 1 - w // 2, S - 1 - w // 2)
    if missing:                                   # 虚环 = 名有而像无
        col, n, step = SLATE + (235,), 96, 360 / 96
        for i in range(0, n, 2):
            d.arc(box, i * step, (i + 1) * step, fill=col, width=w)
    else:
        d.ellipse(box, outline=GOLD + (255,), width=w)
    outer = Image.new("L", (S, S), 0)
    ImageDraw.Draw(outer).ellipse((0, 0, S - 1, S - 1), fill=255)
    im.putalpha(Image.composite(im.getchannel("A"), Image.new("L", (S, S), 0), outer))
    out = Image.alpha_composite(im, ring).resize((SIZE, SIZE), Image.LANCZOS)
    dst = os.path.join(HS, f"tile_{pid}.png")
    out.save(dst)
    return dst, missing


def silhouette(k):
    """灰剪影: 头 + 肩, 三型微差。alpha 掩, 灰度填充。"""
    S = 256
    im = Image.new("RGBA", (S, S), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    g = 150 - k * 14
    col = (g, g, g, 255)
    hw = [0.30, 0.34, 0.27][k]          # 头半径
    sw = [0.62, 0.72, 0.55][k]          # 肩宽
    cy = 0.33
    d.ellipse(((0.5 - hw) * S, (cy - hw) * S, (0.5 + hw) * S, (cy + hw) * S), fill=col)
    d.polygon([((0.5 - sw) * S, S), ((0.5 - sw * 0.72) * S, 0.68 * S),
               ((0.5 + sw * 0.72) * S, 0.68 * S), ((0.5 + sw) * S, S)], fill=col)
    d.ellipse(((0.5 - sw) * S, 0.62 * S, (0.5 + sw) * S, 1.06 * S), fill=col)
    dst = os.path.join(SV, f"sil_{k}.png")
    im.save(dst)
    return dst


if __name__ == "__main__":
    os.makedirs(SV, exist_ok=True)
    pids = [r["person_id"] for r in csv.DictReader(open(os.path.join(D, "data", "draft-class-faces.csv")))]
    miss = []
    for p in pids:
        _, m = ring_tile(p)
        if m:
            miss.append(p)
    print(f"tiles: {len(pids) - len(miss)}/{len(pids)} 有像 ; 无像 {len(miss)}")
    print("silhouettes:", [os.path.basename(silhouette(k)) for k in range(3)])

    # 名人与无名者的整届台账 (供 blender 读)
    picks = {}
    for r in csv.DictReader(open(os.path.join(D, "data", "nba-draft-history.csv"))):
        y = r["SEASON"]
        if not y.isdigit():
            continue
        picks.setdefault(int(y), []).append((int(r["OVERALL_PICK"]), int(r["PERSON_ID"]), r["PLAYER_NAME"]))
    famous = {}
    noimg = set(miss)
    with open(os.path.join(D, "data", "draft-class-faces.csv")) as f:
        rows2 = list(csv.DictReader(f))
    fld = list(rows2[0].keys()) + ["has_portrait"]
    with open(os.path.join(D, "data", "draft-class-faces.csv"), "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fld); w.writeheader()
        for r in rows2:
            r["has_portrait"] = 0 if r["person_id"] in noimg else 1
            w.writerow(r)
    for r in rows2:
        famous.setdefault(int(r["draft_year"]), set()).add(int(r["person_id"]))
    with open(os.path.join(D, "data", "draft-class-crowd.csv"), "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["draft_year", "n_picks", "n_famous", "n_anonymous", "n_famous_with_portrait"])
        for y in sorted(famous):
            k = sum(1 for r in rows2 if int(r["draft_year"]) == y and r["has_portrait"] == 1)
            w.writerow([y, len(picks[y]), len(famous[y]), len(picks[y]) - len(famous[y]), k])
    print(open(os.path.join(D, "data", "draft-class-crowd.csv")).read())
