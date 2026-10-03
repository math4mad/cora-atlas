#!/usr/bin/env python3
"""fig_concept_density.py — 塑胶凳 / 肠粉-蒸饭-烧烤摊 · 义素基公共坐标系密度图。

主人 1003 令「密度图可以开工，今天就做这些世界模型轴变化的尝试」。
本脚本是那张「将来那张密度图」（`docs/figs/probes/README.md` 称与冒烟同构）的第一版真图。

【已定的三件（承 1003 handoff，不要重开）】
  1. 位置 = 义素基坐标（**不是**时间 t）；总谱答「何时」，密度图答「何处」。
  2. 三概念空间用【同一副公共坐标系】（不是三张并排）——
     并排会预设三个抽屉互不相干，而它们的锋利处正是共用同一副义素基。
  3. 渲染 rail = PyVista + SSAO（GLMakie 里「透明＋SSAO」互斥）。

【题面】
  · 地 = 一副公共义素基，取两条**带符号的义素轴**作平面 (pos_dim - neg_dim)。
  · 云 = 三个概念空间（肠粉摊 / 蒸饭摊 / 烧烤摊）各一团密度云；
        云心 ＝ 该空间的义素基向量；云展 ＝ 其内部词汇在该平面上的散布（词＝核，MaxSim 相似度＝权重）。
  · 弹 = 证据词 **塑胶凳** ＝ 一个亮标记，落在它自己的义素坐标上。
  · 真 = 引擎里**真实存在**的 超市 / 路边摊 两球以细竖线标出，作真数据锚。

【今天的主实验：轴变化】
  同一份数据，换不同的义素轴对重画，看三团云何时抱成一团、何时分开
  —— 三摊同属「路边摊」族，差异只在少数义素维上；轴选得对，它们才分得开。

用法:
    .venv/bin/python scripts/fig_concept_density.py            # 默认轴对 + 轴变化联表
    AXPAIR=flow .venv/bin/python scripts/fig_concept_density.py
    VER=v02-xxx .venv/bin/python scripts/fig_concept_density.py
"""
import os
import sys
import numpy as np
import pyvista as pv
from PIL import Image, ImageDraw, ImageFont
from matplotlib.colors import LinearSegmentedColormap

sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
sys.path.insert(0, "/Users/mac/Programming/code-2026/Concept-Space-Sphere")
from cognitive_engine import SemeBasedCognitiveEngine  # noqa: E402

pv.OFF_SCREEN = True

D = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
VER = os.environ.get("VER", "v01-terrain")
OUT = os.path.join(D, "docs", "figs", "concept-density", VER)
os.makedirs(OUT, exist_ok=True)

W, H = 1600, 1100
N = 44
EXT = 2.30
R0 = 0.115
THRESH = 0.14
BG = (0.055, 0.058, 0.070)
GOLD = (231, 195, 111)
SLATE = (150, 156, 170)
DIM = (120, 126, 140)


# ── 义素轴：带符号的一维 (pos_dim − neg_dim) ─────────────────────────────
# 每条轴 = 正极义素 − 负极义素; 箭头自负极指向正极 (Hiragino 无 ↔，故用 →)
AXES = {
    "outdoor": ("outdoor", "indoor"),          # 室内 → 室外
    "flow":    ("movable_cart", "fixed_shelf"),  # 固定货架 → 流动摊车
    "make":    ("fresh_made", "packaged"),     # 预包装 → 现做
    "noise":   ("noisy", "formal"),            # 正式 → 喧闹
    "casual":  ("casual", "formal"),           # 正式 → 随意
}
AXLABEL = {
    "outdoor": "室内 → 室外",
    "flow":    "固定货架 → 流动摊车",
    "make":    "预包装 → 现做",
    "noise":   "正式 → 喧闹",
    "casual":  "正式 → 随意",
}

# ── 三个概念空间（1001 母本之三摊；义素基向量 v01 草案，候主人勘）──────────
# 烧烤摊 ＝ 与引擎词库里的「烧烤摊」同向量（真数据）；肠粉/蒸饭为同族微调。
SPACES = [
    dict(name="肠粉摊", short="肠粉", color=(0.97, 0.76, 0.36),
         time="晨", coeff={"outdoor": 0.90, "indoor": 0.00, "movable_cart": 0.75,
                           "fixed_shelf": 0.10, "fresh_made": 1.00, "packaged": 0.35,
                           "cold_chain": 0.00, "formal": 0.05, "casual": 0.85, "noisy": 0.45}),
    dict(name="蒸饭摊", short="蒸饭", color=(0.62, 0.90, 0.58),
         time="午", coeff={"outdoor": 0.85, "indoor": 0.10, "movable_cart": 0.70,
                           "fixed_shelf": 0.20, "fresh_made": 1.00, "packaged": 0.50,
                           "cold_chain": 0.10, "formal": 0.15, "casual": 0.75, "noisy": 0.60}),
    dict(name="烧烤摊", short="烧烤", color=(0.92, 0.45, 0.38),
         time="夜", coeff={"outdoor": 1.00, "indoor": 0.00, "movable_cart": 1.00,
                           "fixed_shelf": 0.00, "fresh_made": 1.00, "packaged": 0.10,
                           "cold_chain": 0.00, "formal": 0.00, "casual": 0.90, "noisy": 0.90}),
]
EVIDENCE = "塑胶凳"

DIMS = list(SemeBasedCognitiveEngine().basis_dict.keys())
MARKET = [w for w, v in SemeBasedCognitiveEngine().vocab.items()
          if not any(d in v for d in ("觉醒", "服从", "循环", "身份", "暴力", "命运"))]


# ── 坐标 ────────────────────────────────────────────────────────────────
def axis_val(coeff, ax):
    pos, neg = AXES[ax]
    return float(coeff.get(pos, 0.0)) - float(coeff.get(neg, 0.0))


class Frame:
    """把义素向量投到 (ax1, ax2) 平面，并做 min-max 归一化到 [-1,1]。"""

    def __init__(self, ax1, ax2, pts):
        self.ax1, self.ax2 = ax1, ax2
        a1 = [axis_val(p, ax1) for p in pts]
        a2 = [axis_val(p, ax2) for p in pts]
        self.lo1, self.hi1 = min(a1), max(a1)
        self.lo2, self.hi2 = min(a2), max(a2)
        if self.hi1 - self.lo1 < 1e-6:
            self.hi1 = self.lo1 + 1.0
        if self.hi2 - self.lo2 < 1e-6:
            self.hi2 = self.lo2 + 1.0

    def __call__(self, coeff):
        u = (axis_val(coeff, self.ax1) - self.lo1) / (self.hi1 - self.lo1) * 2 - 1
        v = (axis_val(coeff, self.ax2) - self.lo2) / (self.hi2 - self.lo2) * 2 - 1
        return (u, v)


def cosine(a, b):
    a = np.asarray(a, float)
    b = np.asarray(b, float)
    d = (np.linalg.norm(a) * np.linalg.norm(b)) + 1e-9
    return float(np.dot(a, b) / d)


def vec(coeff):
    return np.array([coeff.get(d, 0.0) for d in DIMS], float)


def cloud_cmap(name, col):
    c = np.array(col, float)
    lo = c * 0.14 + np.array(BG, float) * 0.30
    return LinearSegmentedColormap.from_list(name, [lo, c * 0.55, c])


def gauss2d(x, y, mu, sig):
    return np.exp(-(((x - mu[0]) ** 2) / (2.0 * sig[0] ** 2)
                    + ((y - mu[1]) ** 2) / (2.0 * sig[1] ** 2)))


def cloud_mesh(mu, sig, n=N):
    xs = np.linspace(-EXT / 2, EXT / 2, n)
    blocks, dens = [], []
    for x in xs:
        for y in xs:
            d = gauss2d(x, y, mu, sig)
            if d < THRESH:
                continue
            s = pv.Sphere(radius=R0 * (0.55 + 0.85 * d),
                          center=(x, y, 0.30 * d),
                          theta_resolution=12, phi_resolution=12)
            s.point_data["d"] = np.full(s.n_points, d)
            blocks.append(s)
            dens.append(d)
    if not blocks:
        return None, 0
    return pv.merge(blocks), len(blocks)


def sigmas_for(space, frame, eng):
    """云展: 由该空间内部词汇在平面上的散布定 (各向异性)。"""
    sv = vec(space["coeff"])
    members = []
    for w in MARKET:
        wv = eng.encode_word(w)
        if np.linalg.norm(wv) == 0:
            continue
        sim = cosine(wv, sv)
        if sim > 0.80:                                # 归属阈值
            members.append((w, sim, frame(eng.vocab[w])))
    c = frame(space["coeff"])
    if len(members) >= 3:
        pts = np.array([p for _, _, p in members])
        s1 = float(np.clip(np.std(pts[:, 0]) * 1.10, 0.16, 0.26))
        s2 = float(np.clip(np.std(pts[:, 1]) * 1.10, 0.16, 0.26))
    else:
        s1 = s2 = 0.21
    return c, (s1, s2), members


def build(frame, ax1, ax2, ssao, out_png, eng):
    pl = pv.Plotter(off_screen=True, window_size=(W, H))
    pl.set_background(BG)

    floor = pv.Plane(center=(0, 0, -0.02), direction=(0, 0, 1),
                     i_size=EXT + 1.0, j_size=EXT + 1.0)
    pl.add_mesh(floor, color=(0.11, 0.12, 0.145), smooth_shading=False,
                show_edges=False, lighting=True)

    # 真数据锚: 引擎里真实的 超市 / 路边摊 两球 (细竖线)
    for nm, col in (("超市", (0.44, 0.72, 0.95)), ("路边摊", (0.80, 0.80, 0.84))):
        p = frame(eng.concept_spaces[nm]["coefficients"])
        pl.add_mesh(pv.Line((p[0], p[1], 0.0), (p[0], p[1], 0.62)),
                    color=col, line_width=2.0, opacity=0.55)
        pl.add_mesh(pv.Sphere(radius=0.045, center=(p[0], p[1], 0.62)),
                    color=col, smooth_shading=True)

    total = 0
    info = []
    for sp in SPACES:
        c, sig, members = sigmas_for(sp, frame, eng)
        m, n = cloud_mesh(c, sig)
        info.append((sp, c, sig, len(members), n))
        if m is None:
            continue
        total += n
        pl.add_mesh(m, scalars="d", clim=(0.0, 1.0),
                    cmap=cloud_cmap(sp["name"], sp["color"]), opacity="linear",
                    show_scalar_bar=False, smooth_shading=True,
                    specular=0.30, specular_power=18.0)

    # 证据词: 塑胶凳
    ev = frame(eng.vocab[EVIDENCE])
    for r in (0.085, 0.055):
        pl.add_mesh(pv.Sphere(radius=r, center=(ev[0], ev[1], 0.52)),
                    color=(1.0, 1.0, 1.0), smooth_shading=True)
    pl.add_mesh(pv.Line((ev[0], ev[1], 0.0), (ev[0], ev[1], 0.46)),
                color=(1.0, 1.0, 1.0), line_width=1.4, opacity=0.7)

    if ssao:
        pl.enable_ssao(radius=0.55, bias=0.006, kernel_size=192, blur=True)

    # 镜头对准三团云的质心（不一定是原点）
    cen = np.mean([frame(sp["coeff"]) for sp in SPACES], axis=0)
    pl.camera_position = [(cen[0] - 2.35, cen[1] - 2.85, 2.55),
                          (cen[0], cen[1], 0.10), (0, 0, 1)]
    pl.camera.zoom(1.02)
    img = pl.screenshot(return_img=True)
    pl.close()
    Image.fromarray(img).save(out_png)
    return img, info, ev


# ── 两趟法: 3D 只渲形体, 文字由 PIL 合成 ────────────────────────────────
CJK = [("/System/Library/Fonts/Hiragino Sans GB.ttc", 0),
       ("/System/Library/Fonts/Supplemental/Songti.ttc", 0),
       ("/System/Library/Fonts/STHeiti Light.ttc", 0)]


def font(size, bold=False):
    for p, i in (CJK if not bold else []) + CJK:
        try:
            return ImageFont.truetype(p, size, index=i)
        except Exception:
            continue
    return ImageFont.load_default()


def compose(img, title, sub, ax1, ax2, info, ev, eng, out_png, ssao_tag):
    im = Image.fromarray(img).convert("RGB")
    w, h = im.size
    d = ImageDraw.Draw(im)
    band = 150
    canvas = Image.new("RGB", (w, h + band), (14, 14, 19))
    canvas.paste(im, (0, 0))
    d = ImageDraw.Draw(canvas)

    d.text((56, 26), title, font=font(34), fill=GOLD)
    d.text((56, 74), sub, font=font(20), fill=(178, 182, 194))

    # 轴注
    d.text((56, h - 178), f"横轴 · {AXLABEL[ax1]}", font=font(21), fill=(210, 214, 224))
    d.text((56, h - 150), f"纵轴 · {AXLABEL[ax2]}", font=font(21), fill=(210, 214, 224))
    d.text((56, h - 122), "竖高 / 明暗 · 概率密度　·　色相 · 哪一团云",
           font=font(19), fill=(150, 156, 170))

    x0 = w - 620
    d.text((x0, h - 178), f"证据 · 【{EVIDENCE}】 → {ev[0]:+.2f}, {ev[1]:+.2f}",
           font=font(20), fill=(255, 255, 255))
    rows = []
    for sp, c, sig, nmemb, nball in info:
        rows.append((sp["color"], f'{sp["name"]}（{sp["time"]}）  '
                                  f'({c[0]:+.2f}, {c[1]:+.2f})  词 {nmemb} · 球 {nball}'))
    rows.append(((0.44, 0.72, 0.95), "细竖线 · 引擎真球【超市】（真数据锚）"))
    rows.append(((0.80, 0.80, 0.84), "细竖线 · 引擎真球【路边摊】（真数据锚）"))
    for i, (col, txt) in enumerate(rows):
        yy = h - 148 + i * 27
        d.rectangle([x0, yy + 7, x0 + 16, yy + 21], outline=tuple(int(255 * v) for v in col),
                    width=2)
        d.text((x0 + 26, yy), txt, font=font(19), fill=(214, 218, 228))

    d.text((56, h + 74), f"rail · PyVista + SSAO({ssao_tag})　·　义素基公共坐标系　·　"
                         f"ver {VER}", font=font(17), fill=(110, 116, 130))
    canvas.save(out_png)
    return canvas


def main():
    eng = SemeBasedCognitiveEngine()
    ax1 = os.environ.get("AX1", "outdoor")
    ax2 = os.environ.get("AX2", "flow")
    key = f"{ax1}-{ax2}"

    pts = [sp["coeff"] for sp in SPACES] + [eng.vocab[EVIDENCE],
                                           eng.concept_spaces["超市"]["coefficients"],
                                           eng.concept_spaces["路边摊"]["coefficients"]]
    frame = Frame(ax1, ax2, pts)

    print(f"ver={VER}  pyvista={pv.__version__}  ax=({ax1},{ax2})  → {OUT}")
    img, info, ev = build(frame, ax1, ax2, True, os.path.join(OUT, "_plate-main.png"), eng)
    for sp, c, sig, nmemb, nball in info:
        print(f"  {sp['name']}: 心({c[0]:+.2f},{c[1]:+.2f}) σ({sig[0]:.2f},{sig[1]:.2f}) "
              f"词{nmemb} 球{nball}")
    print(f"  {EVIDENCE}: ({ev[0]:+.2f},{ev[1]:+.2f})")

    sub = ("位置＝义素基坐标（非时间）· 三概念空间共用同一副基底 · 今日主题：轴变化")
    compose(img, "塑胶凳 · 三摊 · 义素基密度地形", sub, ax1, ax2, info, ev, eng,
            os.path.join(OUT, f"terrain-{key}.png"), "on")

    # ── 轴变化联表: 同一份数据换轴重画 ──────────────────────────────
    pairs = [("outdoor", "flow"), ("flow", "noise"), ("make", "casual")]
    tiles = []
    for a, b in pairs:
        fr = Frame(a, b, pts)
        im, inf, evv = build(fr, a, b, True, os.path.join(OUT, f"_tmp-{a}-{b}.png"), eng)
        tiles.append(compose(im, f"轴对 · {AXLABEL[a]} × {AXLABEL[b]}", "",
                             a, b, inf, evv, eng,
                             os.path.join(OUT, f"axis-{a}-{b}.png"), "on"))
    tw, th = tiles[0].size
    sheet = Image.new("RGB", (tw, th * len(tiles)), (10, 10, 14))
    for i, t in enumerate(tiles):
        sheet.paste(t, (0, i * th))
    sheet.save(os.path.join(OUT, "axis-variation.png"))
    for a, b in pairs:
        for f in (f"_tmp-{a}-{b}.png",):
            try:
                os.remove(os.path.join(OUT, f))
            except OSError:
                pass
    try:
        os.remove(os.path.join(OUT, "_plate-main.png"))
    except OSError:
        pass
    print("axis-variation.png written")
    print("CONCEPT_DENSITY_DONE")


if __name__ == "__main__":
    main()
