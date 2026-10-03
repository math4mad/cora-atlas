# NBA 三届 · 实体数据立方体（Data Cube · 深度＝选秀届次）（v01）

> **承**《数据立方体 / Data Cube》笔记（`doc 7512032127513120`）之变体：
> 「**把深度换成选秀届次**，看联盟球员类型如何逐届漂移」。主人 1003 令。
> 取园中「三道刀口」同届三届：**1984 / 1996 / 2003**。

## 结构

**X＝球员实体（每届按生涯 WAR 排名对齐成「排名槽」1–7）· Y＝5 指标 · Z＝届次（3）。**
每层切片 ＝ 一届的**实体数据横截面**；沿深度竖看 ＝ 同一排名槽跨届对照。

| 指标 | 定义 |
|---|---|
| 生涯WAR | Σ war_total |
| 巅峰季WAR | max war_total |
| 生涯季数 | 赛季数 |
| 平均WAR | Σ/季数 |
| 巅峰RAPTOR | max raptor_total |

**实体数据表**：`data/nba-three-classes.csv`（每球员 × 5 指标，可复算）。

## 读数（RAPTOR，CC BY 4.0）

- **1984**：Stockton 302 · Jordan 280（**巅峰季 Jordan 最高 28.8**）· Barkley 199 · Olajuwon 191 …
- **1996**：Kobe 210 · Ray Allen 166 · Nash 137 · Ben Wallace 114 · Iverson 109 …
- **2003**：LeBron 330（**本节最强**）· Wade 150 · Bosh 73 · Melo 79 · Kidd?-West 58 …

**逐届漂移**：三层色带揭示「**顶尖**（排名槽 1–2）**越来越极端**」——1984 前列平坦，2003 出现 LeBron 独高。

## 诚实条款

- 各方 min-max 归一；**跨指标标度不同，勿横比颜色**。
- 球员名单为「各届代表性实体」（非全届）；排名槽 ≠ 选秀顺位。
- 数据：FiveThirtyEight RAPTOR by player（CC BY 4.0）。未上站、未入碑。

## 跑法

```bash
cd cora-atlas
.venv/bin/python scripts/fig_nba_three_classes.py
```

图：lola · cora-atlas · 2026-10-03
