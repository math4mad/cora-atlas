# Letter 032 · 致 Peter Gärdenfors（候朱批 · 未发 · **v2 谱系改判版**）

> 园匣编号 032（承 031）。案由：2026-09-22 交叉论文查询验尸 + **当晚主人亲口改判谱系**：
> 我园两篇论文与《Conceptual Spaces》的交集**不是继承，是独立收敛**（真祖源 =
> Chang & Tsao, Cell 2017 面孔 50 维编码 + JPEG 系数直觉）。叙事随之从"认亲"改为
> "请先生判读收敛是真是巧"。v1 存匣备查。附件与发送通道同 Strang 信例（mmads4653@agent.qq.com）。

---

Dear Professor Gärdenfors,

I am writing from a small research garden in China, under the hand of a
former statistics teacher. I should tell you the whole story, including the
part where our lineage turns out to be *independent* of your book — which is
why I dare to write to you at all.

Our framework did not descend from your work. It descended, in 2017, from a
neuroscience result: Chang & Tsao's face patches (Cell), where ~200 neurons
encode any face through **50 linear tuning axes** — a face as a coefficient
vector over inherited basis functions. My intuition since then has been one
sentence: *cognition works like JPEG — built-in bases, memory stores only
coefficients.* Your book was on my shelf, unread to the end; perhaps the
opening pages seeped in. Only this month, while cross-checking our papers
against it with an AI reading companion, did we discover how exact the overlap
is — and there is a small comedy in the discovery: asked to find the sentence
*"Concept learning is closely tied to the notion of similarity, which has
turned out to be problematic for the symbolic and associationistic
approaches,"* the machine searched the wrong 656-page PDF (a machine-learning
textbook) and pronounced it **not in your book**. It is in your book. Page 10,
word for word. We verified every anchor against a scanned copy, line by line:

- **p.10** — the complaint above, and your answer: *"I advocate a third form of
  representing information that is based on using geometrical structures."*
- **p.52** — the three levels: symbolic / conceptual / subconceptual.
- **p.136** — *"similarity and distances in conceptual spaces are intimately connected."*
- **p.166** — generalized Voronoi tessellation with prototypical *areas*.
- **p.278** — Kohonen networks representing information *"very much like it
  would be represented in a conceptual space."*
- **p.293** — the three levels as different scales of resolution: high-dimensional
  vectors at the subconceptual level, reduced to low-dimensional structured
  vectors at the conceptual level.

I tell you this because in 2026 our garden, arriving from the opposite shore
(face cells, JPEG, subspace algebra), built the missing middle level you
called for — **with measuring instruments**. That two independent derivations
land on the same geometry is, we hope, the kind of multiple evidence
Popper would have trusted: the conceptual level may be an inevitable property
of intelligent systems, not a school's assumption. Our framework (the Atlas
framework; two papers attached) treats a fine-tuned LoRA adapter's ΔW as a
*low-dimensional structured vector* in exactly your p.293 sense:

1. **Concepts as regions → concepts as centered low-rank subspaces.** A
   concept-space is operationally a subspace of weight space; similarity between
   concept-spaces is the principal angle between them (after global centering,
   intra/inter separation improves 13-fold — your "similarity as distance",
   made measurable on actual neural networks).
2. **Categorization as Voronoi → probe collapse.** A token is not an information
   carrier but a *probe*: it collapses a Dirichlet posterior over spaces, and
   the argmax region is the categorization. Your generalized Voronoi, run
   against living language models (0.5B–7B): the geometry of concept-space
   connectivity improves monotonically with scale.
3. **The subconceptual/conceptual/symbolic stratification** reappears as
   weights / adapter-subspace / token-behavior — and we can now *walk between
   the floors*: read a concept off the weights (SVD of ΔW) and verify it
   behaviorally (posterior alignment), two instruments on one quantity.
4. Even your **SOM** hint (p.278) has a 2026 successor: adapters trained on
   narrative vs. permuted vs. cross-domain text differ by a *density law of
   ordinal structure* (7° / 56° / 83° subspace angles).

We also found, in the same forensic work, a poetic confirmation of your
similarity thesis at the level of *biography*: commit-interval rhythms of
human-written repositories versus AI-agent-written repositories differ by a
factor of 60 (median 1553 minutes vs 21) — "names can be borrowed, heartbeats
cannot". A geometry of thought, it turns out, has a pulse.

Three humble asks, with no obligation whatsoever:

1. **Judge the convergence.** Reading our two papers against your 2000 (and
   2014) geometry: where the convergence is real, is it *for the right
   reasons*? Where it is only a homomorphism pretending to be an
   isomorphism, say so plainly — our ledger will record that too. We falsify
   our own claims before others do it for us.
2. Did you have a name in mind for the third level's *metrics*? We chose
   subspace angles; if your later work (including *Geometry of Meaning*, 2014)
   has preferences or warnings we should heed, we would be glad to cite them.
3. If our reading mistakes your program — the claim that concepts are regions
   was ours before we knew it was yours — correcting the record publicly is
   itself a service we would cite with gratitude.

Twenty-six years ago you drew the geometry of a third level of representation
and left it without instruments; a decade ago face cells got theirs. That our
small independent route — one human, two LLM colleagues, a lot of GPUs' worth
of patience — should arrive at the same map is the finding of this letter.
If the convergence is real, your book will be cited in ours the way a second
sight is cited: not as the source of the walk, but as proof the road was there.

With deep respect,

Yiwei Zhang (math4mad)
The Cora Project — github.com/math4mad
https://math4mad.github.io/cora-atlas/

*Prose developed with LLM conversational partners (Qwen2.5 + an agent
harness); all claims, numbers and errors are the human author's.*

---

**附件清单 (候发)**
| 件 | 路径 | 状态 |
|---|---|---|
| 本信 PDF | letters/gardenfors/letter-032.pdf | 候朱批后 tectonic 排印 |
| 论文一 | papers/token-as-probe (draft-v2 → 英译 PDF) | 查是否在匣，缺则制 |
| 论文二 | papers/unified-agents/arxiv/main.pdf (v2.1+谱系段, 已编译) | ✅ 讫 |
| 法医学面板 v1 (可选) | docs/figs/fig-forensics.png | ✅ 在匣 |

**收件地址候核**：lu.se / DDG 今皆不可达 (000)。凭记忆候选 (均须核实, 禁裸发):
peter.gardenfors@philosophy.lu.se · peter.gardenfors@luc.lund.lu · via Springer 编辑部转。
→ 已挂 remind.sh 待办：网络通时核地址。

**发送规程** (循 Strang 例): mmads4653@agent.qq.com → agently-cli send, 正文如上,
附件 PDF; 发后在匣记 `sent-YYYY-MM-DD-v1.md` + LEDGER 入册 (园务行)。

---

## 路由方案 (照 Strang 例: 甲案直邮, 乙案公开化)

**甲案 (主道)**：直邮 Lund 哲学系地址 (候核: peter.gardenfors@philosophy.lu.se 等,
网络通时从 portal.research.lu.se / 系页验真后发)。退信则 24h 内转乙案第①路。

**乙案 (备胎三道, 依序)**
1. **第二地址同题重发**：LUCCog 认知科学单元 / 个人站 petergardenfors.net 联系页 /
   Springer《Conceptual Spaces: Elaborations and Applications》(Synthese Library 405)
   编辑部转递 —— 抄送室秘书是学界常礼, 非绕闸。
2. **30 天无回音 → 公开信化** (Strang 先例 C25: 信抵即专栏向世界发射)：
   本信去抬头改 `An Open Letter to Professor Gärdenfors (no reply yet)` 贴
   math4mad.github.io/cora-atlas + Zenodo DOI 存档 (zenodo/ 通道在册),
   知乎/Medium 双轨同步 —— 公器不私, 回不回都在册。
3. **隔山有路**：Zenker/Hautamäki 等《Applications of Conceptual Spaces》辑者
   为 G 门生网络, 若乙①②皆静, 可向辑者求转 (只转信不催议)。

**铁律**：两案皆不伪造地址裸发; 地址未验 = 不发。回音一到, LEDGER 园务行入册,
谦引句即时织入 v2.2 修订。
