# ODSC dry version — paste-ready body (pitch in odsc-pitch.md unchanged)

# Measuring Concept Spaces in Small LMs: a 60-minute, free-GPU recipe

You can profile how a language model represents order, domain, and mixture using three LoRA adapters and a triangle solver. Everything below runs on one free Kaggle T4; our whole run took 7.6 minutes for 11 adapters.

## Setup (what we actually ran)

- Base models: Qwen2.5 0.5B/1.5B/3B/7B, stateless Kaggle kernels (a kernel boot is the strictest "new session" in existence — nothing carries over).
- One corpus pair per experiment (55 QA pairs each: Spring Festival vs. Midsummer; then a noir "underworld vs. police" pair as replication).
- LoRA r=16 on q/k/v/o + MLP, seed 13, 6 epochs, batch 2×accum 4. Fixed before any result was seen (PREREG-first).
- For each trained adapter, flatten all ΔW = B·A into one vector. Compare adapters by the angle between those vectors. That's the entire instrument.

## Result 1 — mixtures detour off the line

Train 11 adapters at ratios 0:100 → 100:0 (11 mixture steps of the two corpora). If combining were interpolating, the midpoint's two angles should sum to the parent angle.

- Parents: 85.2° apart. Midpoint: 61.7° + 60.9° = 122.6°.
- Solve the triangle (SSS): the midpoint sits **44.0° off the straight path**.
- Replication on an unrelated corpus pair (noir): **46.5° off**.

Mixture training finds directions neither parent supplies. If you want the punchy name: composition is parthenogenesis[^1]. But the number is the finding, not the name.

[^1]: Our ledger calls it the detour law (C34). Angles conserved within ±2.5° across domains.

## Result 2 — order strength scales with order density

Take one corpus. Train three arms: text as-is (ordered), sentences reversed (rev), sentences shuffled (shuf). Score every arm against all three text types (NLL).

- Each arm prefers its own training order: 3 domains (Ballon d'Or voting, NBA draft picks, MLB WAR boards) × 3 arms = **9/9 diagonal dominance**.
- Direction index (NLL_rev − NLL_ord) flips sign with training: +0.42 (ord arm), −0.21 (rev arm), ≈ 0 (shuf arm — a built-in null control).
- Weight-space angles: narrative order **7°**, dense list order **56°**, domain change **83°**.

Read: order in text rotates weights proportionally to how much order the text contains. Sparse order is a garnish; ordered rankings are half the dish.

## Result 3 — innate spaces, a scale ladder, and one breach

Aim 11 "fresh" sentences (common words, never-before-seen pairings) at 172 concept spaces built from 1,032 context-labeled tokens; measure the mean rank of the intended space (stateless model = no session memory possible).

- Mean rank (chance = 86 of 172): 0.5B → 33.4, 1.5B → 25.9, 3B → **15.5**. Connectivity improves with scale.
- 7B → **31.0**. The ladder broke. Prime suspects, in order: pretraining leakage of our "fresh" pairings; mean-pooling drift; genuine non-monotonicity. Adjudication experiment is scheduled, not decided.

## Result 4 — center or you're measuring a cone

Raw cosine similarity between 172 spaces: within-space 0.969, between-space 0.896 — routings collapse to chance (we measured 3.2% accuracy on a 172-way baseline; chance is 0.6%).

Subtract the global mean of all embeddings first, renormalize:
- Between-space similarity: **0.896 → 0.0056**.
- Separation (intra − inter): 0.051 → **0.677**.

One line of preprocessing is the difference between a lottery and a map. Every probe number above uses centered embeddings.

## Try it yourself

1. Fork any Qwen2.5-0.5B LoRA notebook on Kaggle; swap in two small corpora (~50 pairs).
2. Train the 11-point mixture sweep (≈8 min); flatten ΔW; compute the three endpoint angles.
3. Check whether your midpoint also leaves the line — and if it doesn't, publish that too.

All our kernels, PREREGs, and raw reports are public; the git log is the experiment's receipt. (Authors: Yiwei Zhang and Lola — the project's AI host, who files the numbers whether they flatter the theory or not.)
