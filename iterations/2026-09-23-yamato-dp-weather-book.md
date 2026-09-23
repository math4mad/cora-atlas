# 2026-09-23 夜 · Yamato《Statistics Based on Dirichlet Processes》验尸账（园体天气层的气象学）

底本: external/…Springer(2020).pdf · sha256 `226610f5…` · 80 页全文抽取
问答卷: external/狄利克雷过程与统计学研究-20260923195617.docx (Qwen 八条帮助清单)
**园律执行: 转述不采信, 逐字对书** —— 14 项关键点验 13 中 (Poisson-Dirichlet/GEM 名目
或随排版变体, 补验中), Qwen 的书目理解**总体可信**, 罕见地没扎科目。

## 园体 Dirichlet 层 × Yamato 对表 (六件兑现)

| # | 园体在册物 | Yamato 供给 | 兑现方式 |
|---|---|---|---|
| 1 | 探针坍缩→argmax (P1/论文 II Dir 层) | Blackwell–MacQueen Pólya 序列 ✓在书 | 我们的顺序坍缩**就是** BM  urn 序列——共轭性/可换性定理直接引用, 天气层从"工程约定"升"有定理对象" |
| 2 | fresh-probe mean-rank / distinct 指标 (C35/P-B3) | ESF + Kₙ 分布 (Stirling 数) + **位移二项近似 BnA1** ✓ | 给 rank/distinct 类指标配**免模拟的零分布**——P-B3 breach (7B=31.0) 从此可算 p 值而非肉眼断言 |
| 3 | 概念频率重尾/"长上下文是负债" (A 文) | 双参数 Pitman 抽样公式 + Mittag-Leffler 渐近 ✓ | 单参数 Dir(θ) 低估重尾 → 升级 **Pitman-Yor Dir(θ,α)**, 折扣参数 α 即 Zipf 指数——可测, 且与心跳幂律长尾同族 |
| 4 | 无限概念空间的截断 (60 空间/160 空间/360 token) | Sethuraman stick-breaking ✓ | 截断误差有了构造式表达: 残 Stick 长度即"未展开概念质量"的可信上界 |
| 5 | 坐标级时间 α(t) (A 文 v2 宣言) | Kingman NRMI / gamma 过程 / Doksum 右中性 ✓ | "每个概念自带结晶年代"的严格随机测度版: α(t) 取**独立增量过程**之归一化——时间轴第一次有测度论户口 |
| 6 | 园律"判据先冻" | 本书自带纠错章 (指出文献错误不等式之收敛速率) | 同一条军规的统计学版: **未验速率不入冻结账本** —— 引为外链佐证 |

## 定位呈报

主人"隐约感觉会有大用"——**感觉验讫成立**：两篇论文把 Dirichlet 当**天气**用，
此书供的是**气象定律**。建议入 REFS 列**仪器层第三祖源**
(Ferguson 1973 定义 / Pitman 组合结构 / Yamato 2020 统计应用之综述桥)。
下一步两桩: ① P-B3 breach 之 BnA1 零分布裁决 (纸上可算, 先于再训);
② 探针电池重尾度估计 → 定 Dir(θ) 还是 Dir(θ,α) (一次计数分析, 数据在册)。
