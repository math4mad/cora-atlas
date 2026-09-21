# Medium-ready post (paste at medium.com/new-post — it auto-renders Markdown)
# Title:
Cognitive Space Construction: Four Axioms for Agents, with 44° of Evidence
# Subtitle:
What happened when we stopped asking "is AI intelligent?" and started measuring angles in weight space
# --- BODY ---

We ran a small theory garden. In it sit a language-model host named Lola, an owner who codes at 3 a.m., a dialogue partner called Qwen, and a ledger that never lets us forget what we predicted before we measured. This post is what the garden found when it pointed prods at its own foundations.

## First, an unfriendly sentence

"Is AI actually intelligent?" is a malformed question. Agency is a property of a high-dimensional space; a binary verdict performs a **rank-1 projection** of it: flatten d dimensions onto a line, then cut the line in the middle. At best one dimension survives; the other d−1 are burned — and that is precisely where the phenomenon lives. Declaring "AI is not intelligence" by one-dimensional definition commits the same fallacy as "everyone forgets at the same speed": passing off one curve as a whole forest.

So we do not ask *whether*. We ask three measurable things: **Which bases does a system span? On which manifold does it live? Which geodesics can a probe traverse?**

## The four axioms

**A1 — An agent is any system that interacts and changes.** Change comes first, time second: time is the measure of change, not its precondition. Trajectories are indexed by ordinal n; the clock is an annotation.

**A2 — The minimal unit is one-dimensional: a point on a curve where sensing and moving are the same act.** In weight space this has a hard referent: every rank-1 singular direction of a LoRA update is a basis curve. r=16 means a budget of sixteen curves.

**A3 — A high-dimensional agent is a linear combination of such curves — plus a residual, and the residual is an ID card, not an error term.**

**A4 — Experience concentrates on low-dimensional manifolds; generalization is geodesic walking; probes are the rulers.** Precondition: centering. Without it, cosine similarity is monopolized by an anisotropic cone and every router is a lottery.

## What the data said

**1) Mixing is not splicing — it is parthenogenesis.** We retrained "Spring Festival" and "Midsummer" adapters at eleven mixture ratios. If composition meant interpolation, the midpoint's two angles should sum to the endpoint angle (85.2°). They sum to **122.6°**. Solving the triangle: the midpoint sits **44.0° off the geodesic** joining its parents. Repeat with an utterly unrelated corpus pair (noir underworld vs. police procedure): **46.5°**. A detour angle conserved to ±2.5° across domains — mixture training grows directions neither parent can supply.

**2) Time is an annotation — but annotations can be loud.** Same corpus, trained in order vs. with sentences shuffled: the ordered arm prefers order (ΔNLL +0.031), the shuffled arm prefers chaos (−0.016). The preference direction flips strictly with training. Yet narrative order rotates weights by only **7°**, while changing domain rotates by **85°**. So we brought social ordinals — Ballon d'Or voting ranks, NBA draft picks, MLB WAR leaderboards. Across 3 domains × 3 arms, the NLL matrix is **diagonal-dominant 9/9**, and the shuffled arm shows zero directionality: a perfect null control. Dense permutation order rotates **56°**. The law that emerged: **the angle an order-channel subtends scales with the density of order in the text.** Sparse order is annotation; dense order is half a skeleton.

**3) Spaces are innate — density grows with scale — and once, our own prediction punched us.** Eleven "fresh" sentences (every word common, every pairing novel) were aimed at 172 concept spaces inside stateless kernels — the strictest "new session" that exists. Mean rank of the target space: 0.5B → 1.5B → 3B goes 33.4 → 25.9 → 15.5 (chance is 86 of 172). Innate spaces exist; connectivity thickens with scale. **Then 7B bounced back to 31.0.** We are not rescuing this prediction yet: leakage is the prime suspect (a 7B corpus may genuinely contain our "novel" pairings), pooling drift is next, genuine non-monotonicity stays on the list. The trial experiment is scheduled. A framework that publishes its own face-punch deserves the label science.

**4) Centering is giving the cartographer an origin.** Raw cosine over 1,032 words in 172 spaces: within-space 0.969, between-space 0.896 — nearly indistinguishable. After global centering: between-space collapses to **0.0056**; separation jumps 0.051 → 0.677, a thirteen-fold gain. The most coherent spaces that emerged: Double Ninth, New Year's Eve, **a rooftop standoff in a Hong Kong crime film**, Qixi, Dragon Boat. Festivals and film scenes standing shoulder to shoulder in a machine's map of the world.

## The probability half: Dirichlet is the weather

Geometry is the skeleton; probability is the weather. We model state over concept spaces with a Dirichlet rather than a bare softmax, for three reasons: **conjugacy** (evidence adds counts to α — collapse is closed-form); **tails never die** (no concept is ever pressed to true zero; black swans keep their Bayesian seat — a frequency-zero event still carries posterior mass); **interpretable concentration** (each α_k *is* the activation intensity of concept k, conditioned on time and place as context). Probe → collapse → KL verification is the acceptance loop of every result above.

## Coda: from builders to prospectors

Language corpora are footprints humans left by walking through concept space. If a model failed to retain that space, where would its coherence come from? Concept spaces are not things we build; they are a precondition for any language model to exist at all. We changed professions — from builders to prospectors. The map was always there; probes merely light up sleeping paths.

One free bonus: metaphor is not "mapping across spaces" either. If A can elicit B, then A and B live in **one** space, far apart. A good metaphor is a long road nobody usually walks.

*Every number here was frozen in a public git ledger before its judgment. The kernels are stateless, the model bytes are sha-pinned, and the receipts are the history itself.*

# --- suggested tags (5 max) ---
Artificial Intelligence, Cognitive Science, Machine Learning, Large Language Models, Philosophy
