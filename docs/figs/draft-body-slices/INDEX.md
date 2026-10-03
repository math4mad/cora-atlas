# 图件迭代档 · 总谱与剖面 · 三道刀口

主人 1003 令：**不要覆盖旧图, 保留迭代结果。**
故每版渲进 `vNN-slug/`，**从不覆盖**；本表即演化年表（演化必留痕迹）。

| 版 | 日期 | 改了什么 | 图 | git |
|---|---|---|---|---|
| `v01-initial` | 2026-10-03 | 方柱 · 四角棱线整条 · 切面无缝（初版） | zh/en | `ec2b33f` |
| `v02-cylinder-misread` | 2026-10-03 | 圆柱 + 圆盘 — 误读草图，已撤回 | zh/en | `6284916` |
| `v03-box-knot5` | 2026-10-03 | 复方柱+矩形切面 · 每片 5 结（四角+中轴） | zh/en | `d42721a` |
| `v04-knot3` | 2026-10-03 | 「按三个切片来」：每片 1 结，撤四角结点 | zh/en | `8e6bd6e` |
| `v05-bounded` | 2026-10-03 | 时间切片受外围长方体边界（SLICE_OVER 1.00） | zh/en | `621159e` |
| `v06-polish` ✅**定稿** | 2026-10-03 | 两趟法: 标签由 PIL 后合成(不受三维遮挡) + 底衬 + 采样 160 | zh/en | `(未提交)` |

## ✅ 定稿

**v06-polish 即定稿**（主人 2026-10-03：「先定稿，把我想的基本都变现出来了。位置站住了。」）。
冻结后不动几何；再改另开 v07 带号档，旧版照存。

## 封版律 ⚖

古 PNG 一张 ~2.7MB，版版全量入库会让仓以每版 ~5MB 膨胀。故：

- **最新版**留 PNG（工作版，全质量）
- **旧版** PNG → JPEG q93 留档（用来看，不用来制版），体积降 ~85%
- `plate.png`（三维底版）**不入库** —— 由脚本 + `VER` 可重现：
  ```bash
  VER=v06-polish blender -b -P scripts/blender_draft_body_slices.py
  VER=v06-polish python3 scripts/compose_draft_body_slices.py
  ```

封版一跑：`python3 scripts/fig_history_pack.py`（自动保留最新版，`--keep vNN` 可指定，`--dry-run` 可预演）。

## 两趟法（v06 起）🎬

三维底版与文字**分开两趟**，文字由 PIL 后合成——
免去长轴细线从标签里穿过（3D 文字无论怎么沿视线前推，都压不过离相机更近的本体近端）：

1. Blender 只渲三维（人头、切面、本体、长轴），并把标签的 3D 锚点经
   `world_to_camera_view` 投成像素坐标 → `labels.json`（**投影前须先定画幅并 `view_layer.update()`**，否则全错）
2. `compose_draft_body_slices.py` 用 PIL 把标签画在底版**之上** —— 字更锐、绝不被遮
