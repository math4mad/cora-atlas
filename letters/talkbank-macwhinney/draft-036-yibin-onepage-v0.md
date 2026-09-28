# draft 036 v0 · 一页研究方案摘要 (候朱批, 未发)

To: Zhang Yibin <zyb_1989@outlook.com> (cc: MacWhinney, reply-all)
Subject: Re: ... — the one-page protocol you asked for

Dear Yibin,

thank you for the careful reply — and happy belated Mid-Autumn. Here is the one
page you asked for; the longer preregistration is in our public repos.

**1. What "developmental sequence" means operationally.**
Every .cha file enters the curriculum sorted by the age field already in the
data (target-child age in months). We train a small language model (Qwen 0.5B–
1.5B, LoRA r=16) on an age-tiered ladder: board-book tier -> short dialogue
tier -> long narrative tier, one contiguous block per age band. "Development"
is not simulated inside the model; it is imposed from outside as the ORDER of
exposure. Our engine's own primitives (maximum-similarity anchoring; sequential
Bayesian updating where today's posterior is tomorrow's prior) make the order
the only place a developmental effect can live — which is exactly why the
control conditions matter, see below.

**2. What "order effect" means operationally.**
Three pre-registered measures, each with frozen criteria:
- *Band separation*: after training, we probe held-out utterances per age band
  and compute the distance profile across bands. A genuine ladder leaves a
  monotone step structure; a shuffled curriculum must not. (Latest 12-band
  run: everything above the first step is flat within ~7% at tier-median level,
  while the step itself survives as a pairwise effect between the two lowest
  bands — granularity caveat stated, full report in preparation.)
- *Reversal test*: flip the exposure order (oldest-first). A true order effect
  flips the advantage profile; if nothing changes, our claim dies — and we
  publish that too.
- *Orthogonalisation check*: Gram–Schmidt on per-tier concept vectors; we
  measure how much new information tier k+1 carries that is orthogonal to
  tiers <= k (the "centricity growth" readout, our quantitative stand-in for
  decentering).

**3. What we ask of your zho holdings.**
Zhou3 as the longitudinal backbone (your note that it is the only TD
longitudinal corpus is decisive for us — it becomes the spine, the rest become
cross-sectional age-slice validators). Derived measures only, no re-hosting of
raw data, full attribution to your team. And we honour the boundary you drew:
this research line stays non-commercial; anything that could touch commercial
software will be fenced off from these corpora by construction, not by policy
alone.

**4. On meeting.**
Shanghai is reachable; we would welcome a visit to ECNU (Zhongbei campus) once
the two-tier granularity readout of our Chinese ladder run is on paper — so
that the first conversation over the table is about numbers, not courtesies.
A date, if you are willing, in late October or November would suit us.

With thanks and respect,
YiWei  (for the Concept-Space-Sphere garden)

— 园笔按: 一页之内只答先生两问 (operationalize / order-effect), 不展开希腊院制与
  对话母本; 面谈应而不定日, 先让 Zhou3 读数开门。商用红线第 3 节已照先生之界写死。
