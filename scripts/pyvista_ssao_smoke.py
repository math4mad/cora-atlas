#!/usr/bin/env python3
"""PyVista ＋ SSAO 冒烟测试 —— 「另一把尺子」的先证。

主人 1003 令: 「可以先做 pyvista 冒烟测试」.
缘起: ide-lola 在试 Kaggle julia(call)+GPU 的 GLMakie 管线;
主人点破 —— **PyVista 自己就有 SSAO**, 故 SSAO 不足以当 Julia 那路的理由。

题目取 **gauss2d 密度地形**, 与将来那张「塑胶凳 / 肠粉-蒸饭-烧烤摊 密度图」同构:
二维网格铺小球, 球的**浓淡 = 该点的高斯密度**; 三团高斯 = 三个「概念空间」
在**同一副公共基底**里的三片云 (并排版判为次一等 —— 见 2026-10-03 之辩)。

只证三件事 (尺子先自证):
  ① 本机 macOS 能否**离屏**渲染 (无 X11)
  ② `enable_ssao()` 通道**是否真出东西** —— 故同题两渲 (开/关) 并对像素差
  ③ 逐球 **RGBA 浓淡**是否可控 (VTK 不透明度传递函数) —— GLMakie 被选中的那条能力

用法:
    .venv/bin/python scripts/pyvista_ssao_smoke.py            # → docs/figs/probes/pyvista-ssao-smoke/vNN/
    VER=v01-pyvista .venv/bin/python scripts/pyvista_ssao_smoke.py
"""
import os
import sys
import numpy as np
import pyvista as pv
from PIL import Image
from matplotlib.colors import LinearSegmentedColormap


def cloud_cmap(name, col):
    """每团云自备色带: 由「暗底 × 云色」渐变到「云色本体」。

    坑 (v01 实测): 传 `scalars='d'` 来做浓淡，`color=` 就被色带接管 —— 三团云
    尽化成一根 viridis，色相全丢。正解: 每团云自带一根同色系色带 (浓淡＝明度)，
    于是「位置＝基底坐标 / 浓淡＝密度 / 色相＝哪团云」三件事互不挤占。
    """
    c = np.array(col, float)
    lo = c * 0.14 + np.array(BG, float) * 0.30
    return LinearSegmentedColormap.from_list(name, [lo, c * 0.55, c])

pv.OFF_SCREEN = True

DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
VER = os.environ.get("VER", "v01-pyvista")
OUT = os.path.join(DIR, "docs", "figs", "probes", "pyvista-ssao-smoke", VER)
os.makedirs(OUT, exist_ok=True)

W, H = 1600, 1100
N = 30                     # 网格 N×N
EXT = 8.0                  # 公共基底边长
R0 = 0.20                  # 球半径基数
THRESH = 0.10              # 密度低于此不铺球
BG = (0.055, 0.058, 0.070)

# 三个「概念空间」——同一副基底里的三片云 (mu, sigma, 色, 名)
CLOUDS = [
    ((2.7, 2.1), (1.45, 1.00), (0.97, 0.76, 0.36), "路边摊"),
    ((-2.5, 1.5), (1.10, 1.30), (0.44, 0.72, 0.95), "超市"),
    ((0.3, -2.7), (1.65, 0.95), (0.62, 0.90, 0.58), "家里"),
]


def gauss2d(x, y, mu, sig):
    """二维高斯 —— 与 conora 实验里 gauss2d 同形。"""
    return np.exp(-(((x - mu[0]) ** 2) / (2.0 * sig[0] ** 2)
                    + ((y - mu[1]) ** 2) / (2.0 * sig[1] ** 2)))


def cloud_mesh(mu, sig):
    """把一团高斯铺成球阵: 球的位置由基底坐标定, 浓淡由密度定。"""
    xs = np.linspace(-EXT / 2, EXT / 2, N)
    blocks, dens = [], []
    for x in xs:
        for y in xs:
            d = gauss2d(x, y, mu, sig)
            if d < THRESH:
                continue
            s = pv.Sphere(radius=R0 * (0.55 + 0.75 * d),
                          center=(x, y, 0.30 * d),
                          theta_resolution=12, phi_resolution=12)
            s.point_data["d"] = np.full(s.n_points, d)
            blocks.append(s)
            dens.append(d)
    if not blocks:
        return None, 0
    return pv.merge(blocks), len(blocks)


def build(ssao, out_png):
    pl = pv.Plotter(off_screen=True, window_size=(W, H))
    pl.set_background(BG)

    # 地板 —— SSAO 需要遮挡体才看得出接触阴影
    floor = pv.Plane(center=(0, 0, -0.02), direction=(0, 0, 1),
                     i_size=EXT + 2, j_size=EXT + 2)
    pl.add_mesh(floor, color=(0.11, 0.12, 0.145), smooth_shading=False,
                show_edges=False, lighting=True)

    total = 0
    for mu, sig, col, nm in CLOUDS:
        m, n = cloud_mesh(mu, sig)
        if m is None:
            continue
        total += n
        pl.add_mesh(m, scalars="d", clim=(0.0, 1.0),
                    cmap=cloud_cmap(nm, col), opacity="linear",
                    show_scalar_bar=False, smooth_shading=True,
                    specular=0.30, specular_power=18.0)

    if ssao:
        pl.enable_ssao(radius=0.55, bias=0.006, kernel_size=192, blur=True)

    pl.camera_position = [(-9.5, -11.0, 8.6), (0.0, 0.0, 0.0), (0, 0, 1)]
    pl.camera.zoom(1.12)
    img = pl.screenshot(return_img=True)          # ndarray H×W×3
    pl.close()
    Image.fromarray(img).save(out_png)
    return img, total


if __name__ == "__main__":
    print(f"ver={VER}  pyvista={pv.__version__}  → {OUT}")
    on, n = build(True, os.path.join(OUT, "ssao-on.png"))
    off, _ = build(False, os.path.join(OUT, "ssao-off.png"))

    a, b = on.astype(np.int16), off.astype(np.int16)
    diff = np.abs(a - b)
    print(f"  球数 {n}")
    print(f"  画幅 {on.shape[1]}×{on.shape[0]}")
    print(f"  开 均值 {on.mean():.2f} / 关 均值 {off.mean():.2f}")
    print(f"  像素差 均值 {diff.mean():.3f}  最大 {diff.max()}  "
          f"变动像素占比 {(diff.max(axis=2) > 6).mean() * 100:.1f}%")
    print("PYVISTA_SSAO_SMOKE_DONE")
    sys.exit(0)
