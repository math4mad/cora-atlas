# 技术迭代柱阵（切片柱阵 · 图3）（v01）

> **母本**：ima 笔记《切片柱阵·三图提示词》`doc 7511883443609699`。
> 图3 行＝NVIDIA GPU / AMD GPU / iPhone；横轴＝发布年份切片；
> 「两列 GPU 行左右并跑，形成**对决柱林**（呼应 PK／对决律），iPhone 行展消费电子迭代节奏」。

## 读

- **对决柱林**：GPU 两行同为 **FP32 TFLOPS**，可比——AMD 早年（HD5870）曾压 NVIDIA；
  **2016 后 NVIDIA 反超并拉开**（RTX 世代陡起，4090/5090）。
- **iPhone 行**：相对性能指数，示消费电子节奏（另轴单位，仅示节奏）。

## 诚实条款

- 数据 **近似取整·示意**（`data/tech-iteration.csv`）；各行 max 归一。
  **非权威规格表**；精确版须逐条回源（发布年 / 规格页）。
- 未上站、未入碑。

## 跑法

```bash
cd cora-atlas
.venv/bin/python scripts/fig_tech_iteration_pillar.py
```

图：lola · cora-atlas · 2026-10-03
