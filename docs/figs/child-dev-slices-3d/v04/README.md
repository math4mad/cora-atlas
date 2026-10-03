# 儿童发展 · 切片柱阵（Blender 3D）（v04 · 微调版）

> 承 v03；主人 1003「2 微调一下，今天就暂定」。微调两处：
> ① **加深色彩**（五指标更饱和）；② **加趋势连线**——五指标各自把六月龄柱顶连成一线的趋势折线，
> **贯穿各切片**，正合「概念演示：变化与轴趋势」。

- 本体＝发展长河（12→42 月）· 六道刀口＝六月龄阶段 · 切面之上五指标立柱 ＋ 柱顶趋势线。
- 数据：`data/child-dev-values.json`（本地 CHILDES，各指标自身 max 归一）。
- 概念演示，非精确读数；12 月片样本薄 †。未上站、未入碑。

```bash
VER=v04 blender -b -P scripts/blender_child_dev_slices.py
VER=v04 .venv/bin/python scripts/compose_child_dev_slices.py
```

图：lola · cora-atlas · 2026-10-03
