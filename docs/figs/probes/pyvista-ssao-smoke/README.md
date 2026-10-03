# PyVista ＋ SSAO 冒烟测试 —— 「另一把尺子」

> **缘起（主人 2026-10-03）**：ide-lola 在试 Kaggle `juliacall` + GPU 的 GLMakie 管线。
> 主人点破：**「Python 自己也有 SSAO，PyVista」** —— 故「有 SSAO」不足以当 Julia 那路的理由。
> 主人令：**先做 PyVista 冒烟测试**。

## 三问三答（尺子先自证）

| 问 | 答 | 证据 |
|---|---|---|
| ① 本机 macOS 能否**离屏**渲染（无 X11）？ | **能** | `pv.OFF_SCREEN=True` + `screenshot()` 出 1600×1100，729 球 |
| ② `enable_ssao()` 是否**真出东西**？ | **真出** | 同题两渲（开/关）像素差：均值 **7.4**、最大 **136**、变动像素 **26.6%**；均值 30.7 → 23.4（遮蔽压暗） |
| ③ 逐球 **RGBA 浓淡**可控否？ | **可控** | `scalars='d'` + `opacity="linear"` + `clim=(0,1)` |

**看疗效**：见 `v02-pyvista-cmap/compare.png` —— 左（关）球与球融成一片雾，右（开）**球与球的接触阴影**把每个球从背景里抠出来，珠子串成珠子坡。

## 勘误 · v01 → v02（迭代律，旧版照存）

**v01 缺陷**：三团云的**色相全丢**，都化成一根 viridis。
**病根**：为做逐球浓淡传了 `scalars='d'`，于是 `color=` 被色带**接管**。
**正解**：每团云自备一根**同色系**色带（`matplotlib.colors.LinearSegmentedColormap`，由「暗底×云色」渐变到云色本体）。
于是三件事互不挤占：

```
位置＝基底坐标   浓淡＝密度   色相＝哪团云
```

## 结论（对 ide-lola 那条管线）

- **SSAO 不是 GPU 功能**，是屏幕空间后处理：PyVista 与 GLMakie 在 **CPU 离屏**下都能出。
- 故 Kaggle 那条的价值**不是**「本地做不到 SSAO」，而是：**一台有真 GL 驱动的 Linux 机** ＋ **对岸/ide-lola 能独立复现同一张图**。
  判据应当是**复现一致性**，不是能不能渲。
- 两条路撞的是**同一堵墙**：无头 GL 上下文。GLMakie → ModernGL/EGL；PyVista/VTK → OSMesa 或 EGL。VTK 侧先例多，是它的便宜处。
- 本地底已在位：Julia 1.12 + **GLMakie 0.13.15** + CairoMakie 0.15.15（depot ~1.1G）；**PyVista 0.49.0 / VTK 9.7.1**（本仓 `.venv`，已 gitignore）。

## 用法

```bash
cd cora-atlas
python3 -m venv .venv && ./.venv/bin/python -m pip install pyvista
VER=v03-xxx ./.venv/bin/python scripts/pyvista_ssao_smoke.py
# → docs/figs/probes/pyvista-ssao-smoke/v03-xxx/{ssao-on,ssao-off}.png
```

**题目**取 `gauss2d` 密度地形，与将来那张「塑胶凳 / 肠粉-蒸饭-烧烤摊 密度图」**同构**：
二维网格铺小球，球**浓淡＝该点高斯密度**；三团高斯＝三个「概念空间」在**同一副公共基底**里的三片云
（并排版判为次一等 —— 2026-10-03 之辩：并排会悄悄预设三个空间是三个不相干的抽屉）。

图：lola · cora-atlas
