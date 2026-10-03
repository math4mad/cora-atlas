# 儿童语言发育柱阵（切片柱阵 · 图1）（v02 · 补齐版）

> 承 v01。**主人 1003「按顺序来」** → 图1 补齐两件：
> ① **词汇量挂 Wordbank 常模**（母本笔记指定）；② **指代清晰度换正向代理**（v01 的显名率随龄下降不是发育）。

## v02 改了什么

| 维 | v01 | v02 |
|---|---|---|
| **词汇量** | 本地 CHILDES 累计词型（语料成长，非词汇量） | **Wordbank 常模**（English American，production 中位）：**4 / 52 / 256 / 492 / —**；36 月超出 CDI 域（斜纹空心柱「CDI 止」）|
| **指代清晰度** | 显名率 noun/(noun+pron) —— **随龄下降**（代词化） | **有定标记率** ＝ (det+noun)/noun —— **正向**：0 / 0.12 / 0.20 / 0.10 / 0.28 |
| 其余三维 | CHILDES | 不变（MLU / POS 熵 / 依存边数）|

## 数据出处（源锚）

- **Wordbank 常模**：`data/wordbank-norms-en.csv`（provenance 在文件头）。
  源 `langcog.github.io/wordbank-datapage/slices/admins/english_american_{wg,ws}.csv`；
  逐 administration 现算 per-age median；Wordbank（Frank et al. 2017）。**CDI 覆盖 8–30 月。**
- **其余四维**：本地 CHILDES Brown+Bernstein（CHI，`%mor`/`%gra` 直取，取 9–39 月入片）。

## 读数

- **词汇量**：4 → 52 → 256 → 492（**Wordbank 常模，稳爬坡**；36 月 CDI 无值）。
- **词类多样性**：1.33 → 2.10 → 2.26 → 2.19 → 2.21（早长后平）。
- **MLU / 句法复杂度**：总趋势向上，有**回落噪声**。
- **指代清晰度**：0 → 0.12 → 0.20 → 0.10 → 0.28（**整体上升**，30 月处回落）。

## 诚实条款

1. **混合数据源**：词汇量＝Wordbank 常模；其余＝本地 CHILDES。两源样本不同，**柱高各自行内 max 归一**，只作形状对照、不作跨行数值比较。
2. **12 月片**：CHILDES 薄（n=3）；Wordbank 12 月 n=615（稳）——词汇量行不缺，其余四维该片弱。
3. **36 月**：Wordbank 无（CDI 止于 30）；CHILDES 有。
4. **仅限研究·非商业**。
5. 未上站、未入碑。v01 照律留档。

## 跑法

```bash
cd cora-atlas
VER=v03-xxx .venv/bin/python scripts/fig_child_language_pillar.py
```

图：lola · cora-atlas · 2026-10-03
