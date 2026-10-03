#!/usr/bin/env python3
"""封版 —— 图件迭代档的减重器。

主人 1003 令: 「不要覆盖旧图, 保留迭代结果」。于是每版渲进
`docs/figs/draft-body-slices/vNN-slug/`, 从不覆盖。但 PNG 一张 ~2.7MB,
若版版全量入库, 仓会以每版 ~5MB 的速度膨胀。故立封版律:

  · **最新版**留 PNG (工作版, 要求全质量)
  · **旧版**PNG → JPEG q93 (留档, 用来看, 不用来制版), 体积约降 85%
  · `plate.png` (三维底版, 由脚本+VER 可重现) 不入库 —— 见 .gitignore

用法:
    python3 scripts/fig_history_pack.py              # 自动保留最新版
    python3 scripts/fig_history_pack.py --keep v07-x # 指定保留哪版
    python3 scripts/fig_history_pack.py --dry-run
"""
import os
import re
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
HIST = os.path.join(ROOT, "docs", "figs", "draft-body-slices")
QUALITY = 93

VRE = re.compile(r"^v(\d+)")


def versions():
    if not os.path.isdir(HIST):
        return []
    vs = [d for d in os.listdir(HIST)
          if VRE.match(d) and os.path.isdir(os.path.join(HIST, d))]
    return sorted(vs, key=lambda d: int(VRE.match(d).group(1)))


def pack(ver, dry=False):
    d = os.path.join(HIST, ver)
    n = 0
    for f in sorted(os.listdir(d)):
        if not f.endswith(".png") or f == "plate.png":
            continue
        src = os.path.join(d, f)
        dst = os.path.join(d, f[:-4] + ".jpg")
        if os.path.exists(dst):
            os.remove(src)
            print(f"  {ver}/{f}: 已有 jpg, 删 png")
            continue
        if dry:
            print(f"  [dry] {ver}/{f} → {f[:-4]}.jpg")
            n += 1
            continue
        subprocess.run(["sips", "-s", "format", "jpeg",
                        "-s", "formatOptions", str(QUALITY),
                        src, "--out", dst],
                       check=True, capture_output=True)
        before, after = os.path.getsize(src), os.path.getsize(dst)
        os.remove(src)
        print(f"  {ver}/{f}: {before/1e6:.2f}MB → {after/1e6:.2f}MB (jpg)")
        n += 1
    return n


def main():
    args = sys.argv[1:]
    dry = "--dry-run" in args
    keep = None
    if "--keep" in args:
        keep = args[args.index("--keep") + 1]
    vs = versions()
    if not vs:
        print("没有带号版本目录"); return
    keep = keep or vs[-1]
    print(f"版本: {', '.join(vs)}   |   保留 PNG: {keep}")
    tot = 0
    for v in vs:
        if v == keep:
            print(f"  {v}: 最新版, 留 PNG")
            continue
        tot += pack(v, dry)
    print(f"{'[dry] ' if dry else ''}封版完成, 处理 {tot} 张")


if __name__ == "__main__":
    main()
