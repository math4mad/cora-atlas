# 儿童发展 · 切片柱阵（Blender 3D）（v03 · 定版）

> **主人 1003 令**：把 `child-dev-slices` 的**各阶段 slice 替换 NBA 选秀那张的 slice**，
> **用 Blender 3D 格式渲染**。
> 即：承「总谱与剖面·三道刀口」的 **Blender 三维语法**（长条本体＋刀口切片＋长轴打结），
> 把切面内容从「选秀面孔」换成「儿童五指标」。

## 场景（Blender 5.2.2 · EEVEE）

| 元素 | 取法 |
|---|---|
| **本体（长条）** | 半透明方柱 ＝ **发展时间长河**（月龄 12 → 42），在每道刀口断开成段，四条棱线＋中轴 |
| **六道刀口** | 矩形切面 ＝ **六月龄阶段** 12/18/24/30/36/42；金框＋长轴交汇处**打结** |
| **切面之上** | **五指标各立一方柱**（柱高 ∝ 值）：词汇量 · MLU · 词类多样性 · 句法复杂度 · 指代清晰度，五色 |
| **两趟法** | 3D 只渲形体；月份标签与页脚由 **PIL 合成**（免受三维遮挡、字更锐） |

数据：`data/child-dev-values.json`（本地 CHILDES，各指标自身 max 归一）。

## 跑法

```bash
cd cora-atlas
VER=v04 blender -b -P scripts/blender_child_dev_slices.py        # → docs/figs/child-dev-slices-3d/v04/plate.png
VER=v04 .venv/bin/python scripts/compose_child_dev_slices.py     # → …-zh.png
```

## 迭代留痕（封版律：绝不覆盖）

- `v01` 初渲（相机过近，只框住三分之一长轴）
- `v02` 相机拉远广角（六片入框）
- **`v03` 降灯加饱和 + 拉近（定版）**

## 诚实条款

- **概念演示**：看「变化」与「轴趋势」，**非精确读数**；各指标 max 归一，仅作形状/高低。
- 12 月片样本薄 †。未上站、未入碑。

图：lola · cora-atlas · 2026-10-03
