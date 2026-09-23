# 审读报告 · Matrix Behaviorology 英文初稿（园笔 v1）

> 底本: external/ Matrix Behaviorology.docx · sha256 `c62c8014…`（pin 在 sidecar）
> 定位判语: 此稿 = **C40「结构即智能」的学科命名篇** —— 园体从此有英文族名
> (Matrix Behaviorology)。骨架成立，逻辑走通；以下按"必改 / 宜补 / 建议"三档开票，
> 凡涉数字，皆从 LEDGER/匣底实档取数，禁裸写。

## 一、必改（数字与引用之correctness）

**§3.2 夹角数据 —— 用实档替换约数**（`exp11-horizontal-matrix/results/report_11_p0.json`）：
- spring~summer: **dWov = 0.137**（ specialists 对最大值, H6 字段在册）
- spring~general: **0.018** · summer~general: 0.018 · code~general: 0.020
- "approximately orthogonal" **成立**（cos 0.018 即近正交），但请给数不给形容词；
- 若引"角"口径（V-A_k90 之度数版），用 C34 在册值: 春雾 85.2° / 黑白端点 83.3° /
  中点鼓包 122.6°→124.9°（跨语料守恒 = "合非拼接" A3 之判决数）。
- **LoRA 配置照抄 PREREG（勿凭记忆）**: r=16, α=32, dropout 0.05,
  targets = q/k/v/o + gate/up/down_proj, lr 1e-4, batch 2×accum 4, seed 13,
  6 epochs/arm, base Qwen2.5-0.5B-instruct（exp11/18 两案同方, 在册）。

**§1.2 书目两处**：
- 《Doing Bayesian Analysis》→ 正名 **Gelman et al., Bayesian Data Analysis**
  （或 Kruschke 的书名才是 Doing Bayesian ……二选一，Crossref 核后落 DOI）；
- "日本学者切蛋糕" = 小谷水元『確率とは何か』其书，英译版宜改引 **de Finetti** 或
  **Jaynes** 并注 cake-cutting 为译本比喻，否则英文读者无从查证。

**§2.2 Neutral JS 案例** —— 园账查无此案（无日期、无 pin、无 log 引文）。
两条路选一：① 补挂进 LEDGER（何日、何 agent、注入原文、前后行为差），升格为
**观察记录 O-号**；② 措辞降级为 anecdote（"in one logged session, unblinded"）。
**不可裸引** —— 我们自己的碑律：凡数字带收据，凡案例带日期。

**§4.3 漏字**："and only 叠加 the next" → **superpose/stack**。

## 二、宜补（把园账的弹药接进正文）

1. **§2.1 PCR**：接补五"DNA 画的后验"对号表（引物=先验均值/退火=似然/扩增=坍缩/
   条带=读出）—— 一段即可，本节从"类比"升"同构"。
2. **§2.2 基因枪**：加**位置效应**一笔（弹道插入位点随机、命运由宿主定 =
   base-fit 之湿实验原证, 主人亲证）—— 这是全文最硬的作者权威性，不用可惜。
3. **§2.4 同基因异功能**：措辞"thousands of base pairs 的 coefficient 配置"宜精确为
   **调控差异 = 剂量与地类**（启动子/表达时相），并接三条园账：
   G2 借维（单维转入只得部分表型——红树耐盐是多维之果）、
   C43 剂量律、双语概念/词形分层（同基因≡共概念库, 调控≡词形检索）。
   此节即"生地论"（水田梯田沃土）之分子版, 可互引。
4. **§3.3 定义句**："Intelligence = structural change during interaction"
   —— 比 C40 四字更可操作, **建议正式入碑为 C40 之英文操作定义**（已另条候批）。
5. **§4.2 T0/T1/T2**：接关键期翻案（LLM 无窗唯序一维, C42）——
   T 之方法论是"时序结构"而非"时间窗", 一字之差防读者误会我们信硬窗。

## 三、建议（缺的两节, 恰是园账最富的两块）

- **新 §5 Methods: The Red-Blue Exercise** —— PB16/PB16-D 详案（传统课程 vs 中型旅,
  逐 epoch 三战, V1-V10 十图, M1-M8 冻指标）: 本文目前只有"论", 军演给它"法";
- **新 §6 Falsification: the Bare Probe** —— 裸探针律 + P-B15 序海选（25 跑审全族）
  + 说话人先验/否决权诸律: 好理论的标志是**存在便宜到羞愧的证伪装置**, 这条
  方法论碑正好收在结论前, 英文可题作 "a probe cheap enough to be embarrassing";
- **Roadmap 段**: 三向最小学习者（P-L2/M 案聋盲双臂）一句带过即可, 留续篇;
- **术语对照表**（附录）: Matrix Behaviorology=矩阵行为学 / 圈地=occupancy /
  地籍=cadastral map / 旅制=brigade curriculum / 缴械=merge survival —— 园语出口
  统一从这里发。

## 四、总评

逻辑链（分子实验→贝叶斯重分配→滴灌课程→rank-1 逐维）**通**;
措辞英文八成地道, 唯数字与案例两处"裸", 按上表补票即可过审。
**判: 骨架可用, 修后即可入 papers/matrix-behaviorology/ 立为 C40 命名篇。**
