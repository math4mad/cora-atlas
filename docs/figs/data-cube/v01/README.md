# 数据立方体 / Data Cube（时空数据立方体）（v01 · 真数据版）

> **母本**：ima 笔记《数据立方体 / Data Cube》`doc 7512032127513120`。
> 方法学名＝**时空数据立方体**（Spatio-temporal Data Cube）；视觉名＝**等轴测堆叠切片**（isometric stacked slices）。
> **读法**：时间做深度轴（Z），每层 2D 切片＝一个时刻的横截面；结构＝**实体 × 指标 × 时间**。
> **与园子接榫**：与「**切片柱阵**」同族——只差**扁平方块堆叠** vs **立起方柱**。

## 两例（皆真数据）

| 面板 | X 实体 | Y 指标 | Z 深度 |
|---|---|---|---|
| **A** | NBA 2003 届 8 人（LeBron/Wade/Bosh/Melo/Kaman/Hinrich/West/Howard） | 出场 · 攻 · 防 · 总 · 胜场贡献 | 赛季 2004→2013 |
| **B** | 本地 CHILDES 6 童（Sarah/Adam/Eve/Alice/Anne/Dale） | 词汇量 · MLU · 句法 · 话轮 · 新词率 | 月龄 12→42 |

**读**：① 抽一层切片＝某赛季/某月龄的**横截面**（全员同现）；② 沿深度竖看＝**单实体轨迹**；
③ 切片内**色离散度**＝同龄/同届**个体差异**。

## 诚实条款

- 色 ＝ **各指标自身 min-max 归一**（跨指标标度不同，**勿横向比较颜色**）。
- A：FiveThirtyEight RAPTOR by player（CC BY 4.0）；B：本地 CHILDES Brown+Bernstein（CHI）。
- B 的「语音清晰度」母本有、本版**未列**（无音系层）；「新词率」＝该片新词型/词数。
- 未上站、未入碑（母本笔记点名「数据立方体」为方法名，是否立碑候主人）。

## 跑法

```bash
cd cora-atlas
.venv/bin/python scripts/fig_data_cube.py
```

图：lola · cora-atlas · 2026-10-03
