#!/usr/bin/env python3
"""取 NBA 官方头像 → 裁成方形圆mask头像块 (供 blender 切片图用)。

源: https://cdn.nba.com/headshots/nba/latest/1040x760/{PERSON_ID}.png
     （cdn.nba.com 直连可达；stats.nba.com / wikipedia 直连被挡）

⚠ 版权: NBA 头像为 NBA 财产。本脚本产物落在 data/headshots/（本地试验用），
   是否上公网发布须主人另裁（见 AGENTS / 术语碑「源须外部可复算」条）。
"""
import os, sys, csv, subprocess, tempfile, io
from PIL import Image, ImageDraw

D = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(D, "data", "headshots")
SIZE = 320          # 输出边长
CROP = 460          # 原图裁框边长 (1040x760 内, 框住头部)
CX, CY = 520, 250   # 裁框中心 (头像五官大致落点)


def fetch(pid):
    """走 curl —— 本机 urllib 出不去, curl 直连 cdn.nba.com 可 (实测 206/200)。"""
    url = f"https://cdn.nba.com/headshots/nba/latest/1040x760/{pid}.png"
    with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as t:
        tmp = t.name
    try:
        r = subprocess.run(["curl", "-sS", "--max-time", "25", "-A", "Mozilla/5.0",
                            "-o", tmp, "-w", "%{http_code}", url],
                           capture_output=True, text=True)
        code = (r.stdout or "").strip()
        if code != "200" or os.path.getsize(tmp) < 2000:
            raise RuntimeError(f"http {code} size {os.path.getsize(tmp)}")
        return open(tmp, "rb").read()
    finally:
        os.path.exists(tmp) and os.remove(tmp)


def tile(raw):
    im = Image.open(io.BytesIO(raw)).convert("RGBA")
    w, h = im.size
    cx = min(CX, w - CROP // 2 - 1) if w > CROP else w // 2
    cy = min(CY, h - CROP // 2 - 1) if h > CROP else h // 2
    box = (cx - CROP // 2, cy - CROP // 2, cx + CROP // 2, cy + CROP // 2)
    im = im.crop(box).resize((SIZE, SIZE), Image.LANCZOS)
    mask = Image.new("L", (SIZE * 4, SIZE * 4), 0)
    ImageDraw.Draw(mask).ellipse((0, 0, SIZE * 4 - 1, SIZE * 4 - 1), fill=255)
    mask = mask.resize((SIZE, SIZE), Image.LANCZOS)
    im.putalpha(Image.composite(im.getchannel("A"), Image.new("L", (SIZE, SIZE), 0), mask))
    return im


def main(ids):
    os.makedirs(OUT, exist_ok=True)
    ok, fail = [], []
    for pid in ids:
        dst = os.path.join(OUT, f"{pid}.png")
        if os.path.exists(dst) and os.path.getsize(dst) > 2000:
            ok.append(pid); continue
        try:
            tile(fetch(pid)).save(dst)
            ok.append(pid)
        except Exception as e:
            fail.append((pid, type(e).__name__))
    print(f"ok={len(ok)} fail={len(fail)} -> {OUT}")
    if fail:
        print("FAILED:", fail)
    return fail


if __name__ == "__main__":
    ids = sys.argv[1:]
    if not ids:
        f = os.path.join(D, "data", "draft-class-faces.csv")
        ids = [r["person_id"] for r in csv.DictReader(open(f))]
    sys.exit(1 if main(ids) else 0)
