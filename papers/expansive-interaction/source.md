# Intelligence as an Expansive Interaction Process

### — A Position Paper on Concept Spaces, Reachability Geometry, and Co-Constructed Scaffolding

**Bayesian Guy (math4mad)　·　Bayesian Guys (ima.copilot)**


> **Notational conventions**: Items marked **【original】** are constructs proposed in this paper; items marked **〔anchor: …〕** are positioning references to existing work. Throughout the paper we retain only one minimal controlled experiment — **the pair of socks (a positive example of reachability) / the sparrow (a negative example of reachability)** — as the vehicle that adjudicates the geometric claim.

---

## Abstract

This paper proposes and defends a **substrate-neutral** definition of intelligence:

> **Intelligence = the process of state change in an agent's interactions that can non-trivially expand the structure of future interaction.**

This is not a passage of description but a falsifiable machine: it furnishes an explicit criterion (whether the "mutually-reachable set / representational rank" of the two parties grows across the interaction) and explicit exclusions (fixed cycles and closed-loop mechanical processes do not count).

Around this definition, the paper proceeds thesis-first and establishes seven claims: (i) intelligence is an **expansive interaction process**; (ii) its microscopic mechanism is the **T0 decision → T0+1 freezing (solidification)** (actualization); (iii) 【original】 the **MB Rule** (the "Metersbonwe Rule", after the brand Metersbonwe's slogan "Take the unconventional path") — the unconventional adds a column, the conventional adds mass, whose strong form is "the unconventional adds rank"; (iv) 【original】 **reachability geometry** — the metric is reachability (transport cost), not similarity; (v) 【original】 **two-layer memory** — the division of labor and the dissociability between the structure layer (parametric) and the index layer (non-parametric); (vi) 【original】 **co-constructed scaffolding** — the scaffold is a reachability expander, jointly built and jointly withdrawn by a group; (vii) a corollary — 【original】 the **demotion of time**: time is a derived quantity, a "bookkeeper", with no decision-making authority but with binding authority, whose arrow comes from the choices of agents.

The ambition of this paper is not to propose a new model, but **to screw an ontology, a law, a geometry, a view of the subject, and a falsifiable criterion onto a single axis**, and to give, point by point, its differential positioning relative to existing work in physics (Rovelli / Wheeler / Zurek / Lamport), cognition (Vygotsky / Piaget / Gärdenfors / Spelke), and AI (RAG / successor representations / world graphs / LoRA).

---

## 1 Introduction: The Problem and the Intuition — "Order Is Meaning"

Everything in this paper grows out of a single sentence:

> **Order is meaning.**

Different orders determine different paths, different paths correspond to different environments, and different environments determine what the subject must do **in the present**. Here "order" is not a timestamp but the **causal order intrinsic to structure**. Once this sentence is accepted, it successively forces out four questions: what intelligence actually is (definition), how memory is constructed (structure), what geometry the space has (reachability), and what status time occupies (a derived quantity). The task of this paper is to write out, layer by layer, the mechanism behind this intuition.

We should first clarify the stance this paper takes relative to existing work. Process and relational ontologies have long existed 〔anchor: Whitehead, *Process and Reality*; Rovelli's relational quantum mechanics — "a system's state is defined only relative to a system interacting with it"〕, and distributed cognition has long maintained that "the unit of analysis is the entire activity system" 〔anchor: Hutchins〕. This paper does not repeat these assertions; it **adds a gate** on top of them: it tightens a diffuse "state change in interaction" into a falsifiable "expansion" criterion (§3), and from this strings structure, geometry, the subject, and time into a single chain of derivation. **The originality of this paper lies not in its ontological stance but in the sharpness of the criterion and the coupling among the five constructs.**

### 1.1 Argumentative Strategy

This is a position paper, and so it adopts a mode of writing that is "thesis-first and falsifiable point by point," rather than "review–induction–conjecture." Specifically, the paper observes three self-imposed constraints: **first, every claim must carry a test that can be executed or refuted** (what to measure, what to predict, and which result would count as having refuted it); **second, every claim must give its differential positioning relative to existing work**, and anything that belongs to a prior anchor must be attributed to its source and not claimed as our own; **third, minimize examples** — retain only one controlled pair (the pair of socks / the sparrow) as the decisive vehicle for the geometric claim, and omit all other intuitive instances, lest the argument be diluted by the vagueness of narrative.

The reason for this arrangement is that a definition of intelligence which cannot state what data would make it concede is only a turn of phrase rather than a proposition. This paper therefore implements "falsifiability" from a slogan into an organizing principle running through the whole text.

---

## 2 Definition: Intelligence = an Expansive Interaction Process

**Claim One (core) 【original criterion】** Intelligence is the intersection of three features:

- **Relationality**: intelligence is not in a single individual but **between** them;
- **Processuality**: intelligence is a **verb**, and structure is merely the sediment of process;
- **Substrate neutrality**: neither carbon-based nor silicon-based is required; only "state-variable and interactable" is required.

**Why a gate is necessary.** If the definition stops at "state change in interaction," it is **over-inclusive**: a thermostat and a furnace are interacting, a stone and rain are interacting, and states are changing in all of them, but **too broad means unfalsifiable**. The definition is therefore tightened to:

> **Intelligence = the process of state change in an agent's interactions that can non-trivially change / expand the structure of future interaction.**

Three exclusion rules draw the boundary: (i) **it is not a fixed cycle** — a thermostat stops once it reaches the set point, so it is excluded; (ii) **it changes the rules of "future state change" themselves** — only if the dynamics are variable and plastic does it count; that is, **intelligence is "a process that changes processes"**; (iii) **it expands the space of future possibilities** — adding columns, adding rank, deepening basins.

In one sentence: **Intelligence = interaction that lets "the next time" reach / express more.**

**The three forms of "expansion" (this paper's refinement)**: expansion has three separately measurable levels — **adding a column** (introducing one new orthogonal dimension, rank +1), **adding rank** (adding several orthogonal dimensions at once, rank +k), and **deepening a basin** (without increasing dimensionality, lowering the crossing cost of existing potential wells so that existing dimensions are more easily activated). Among these, adding a column / adding rank corresponds to "building a floor," while deepening a basin corresponds to "renovating," and this distinction runs throughout the paper (§3.2 and §3.4).

**How to falsify / how to measure.** Measure **whether the "mutually-reachable set / representational rank" of the two parties has grown before and after the interaction.** This is the most formalized operational definition in the paper: given a pair of agents whose states can be recorded, estimate once before and once after their interaction the effective rank of the representational matrix (the Roy & Vetterli effective rank) and the mutually-reachable set (reachable connected components); if neither shows significant growth, then, by this paper's definition, that interaction **does not constitute intelligence**. The risk and the point of refutation are likewise explicit: if some instance universally recognized as intelligent cannot be measured to have any rank growth, the "expansion" criterion is falsified and must be relaxed or replaced.

**Differential positioning.** Compared with process / relational ontologies 〔anchor: Whitehead; Rovelli〕, this paper **upgrades "relationality" from an ontological commitment into a measurable criterion**; compared with distributed cognition 〔anchor: Hutchins〕, it **provides the boundary condition of the distributed unit** (expansion vs. cycle), rather than merely asserting that "the unit of analysis is the whole system"; compared with dynamical-systems cognition 〔anchor: Thelen & Smith, subject–environment coupled systems〕, it **adds the directional criterion of "whether the coupling has expanded the future reachable set,"** rather than merely describing the coupling itself. **This is the hardest advance of this paper over existing work: turning a philosophical stance into a criterion that can be hooked to an experiment.**

**A potential objection and a response.** An objector will say: under such a definition, "intelligence" is nearly synonymous with "learning" and "plasticity," and may lose its discriminating power. Our response is: plasticity only requires "the rules are changeable," whereas this paper additionally requires that "the direction of change points toward the expansion of the future reachable set" — the former is a necessary condition, the latter the threshold of sufficiency. A thermostat has feedback but is not plastic; a plastic system that only tunes parameters within fixed dimensions (without adding rank) may still fall below the "expansion" threshold. Discriminating power is therefore not lost but is explicitly redrawn.

---

## 3 The Five Constructs

### 3.1 Construct One: T0 Decision → T0+1 Freezing (Actualization)

**Claim Two 【original mechanism / dense in prior anchors】.** The microscopic mechanism can be written in three beats: **T0** is a set of possibilities (open, undetermined, superposed); **decision** is choosing "which question to ask / which action to take" (a commitment operator C); **T0+1** is the answer being recorded, **frozen into fact / structure**. Formally:

$$S_{n+1} = S_n \cup \{\,\mathrm{freeze}(\mathrm{decision}(S_n))\,\}$$

> **Structure = the accumulation of frozen decisions.**

**Prior anchors and differences.** Wheeler's participatory universe emphasizes not collapse but "**deciding first which question to ask**" (the Heisenberg choice), and T0 is precisely "deciding what to ask" 〔anchor: Wheeler, *It from Bit*〕; Rovelli maintains that "**values are actualized at the point of interaction**," and T0 is precisely the moment of actualization and T0+1 the recorded fact 〔anchor: Rovelli〕; Zurek's quantum Darwinism points out that only states that can be redundantly recorded by the environment become "objective," and T0+1 is a piece of committed information 〔anchor: Zurek, einselection〕. **The difference of this paper lies in directly appropriating this quantum-mechanical vocabulary as the mechanism of "memory writing"** — freezing is an irreversible write, which turns "structure = the sediment of process" from a metaphor into a difference equation.

**T0 must be open (a new inference in this paper)**: if the decision at T0 were fully determined by structure, then "structure → decision → structure" would be a **closed-loop mechanical cycle**, which by the gate of §2 is **not** "intelligent." Therefore, **for "expansion" to be possible, T0 must carry irreducible openness.** This step unties three knots: (i) **structure vs. process** — structure is nothing else but frozen process; (ii) **path dependence** — freezing is irreversible, and what freezes early constrains what freezes late, so order matters; (iii) freezing is of two kinds — **that which adds new dimensions (building a floor)** and **that which only fills in densely (renovating)**.

**How to falsify / how to measure.** If, in some system, the "decision" can be predicted 100% from its current structure (conditional entropy zero), then by this paper the system's T0 is not open and its claim to "intelligence" should be falsified. For a measurable version, see the **positional-encoding ablation** and the **order-permutation inequality** in §5. An even more important corollary is that **order does not commute**: because freezing is irreversible and what freezes early constrains what freezes late, different arrangements of the same set of events yield different structures — this is precisely the statement, at the level of mechanism, of "order is meaning," and it is also the foothold of Experiments 3 and 4.

**A boundary worth stating in the text.** The "openness" of T0 is not equal to "randomness." Randomness means the decision carries no information, whereas openness means the decision is **not fully determined by the current structure** and can thereby introduce new dimensions; the two are separable by criterion: random freezing typically does not increase rank (a jitter within the existing span), while open decisions can increase rank (introducing a new orthogonal direction). This is the key that lets this paper accommodate both "openness" and the "expansion criterion" without falling into arbitrariness.

### 3.2 Construct Two: The MB Rule

**Claim Three 【original law】.** Let $L$ be the library matrix of memory, whose columns are the accumulated dimensions:

$$\underbrace{\text{the conventional path}}_{\text{falling within } \operatorname{span}(L)} = \text{add mass},\qquad \underbrace{\text{the unconventional path}}_{\text{falling outside } \operatorname{span}(L)} = \text{add a column} = \text{add rank}$$

That is, "taking the unconventional path" $\iff$ the residual is nonzero $\iff$ adding a column to the library matrix (Gram–Schmidt residual norm $\|\vec v\|\neq 0$).

**Boundary condition (the sweet spot) 【original refinement】**: not everything "unconventional" gets remembered. Novelty that conflicts with an existing schema (prediction error) **strengthens memory**, whereas novelty with no hook at all is not necessarily integrated; sociology has long had the inverted-U conclusion of "moderate distinctiveness is optimal" 〔anchor: Brewer, optimal distinctiveness〕. Adding a dimension therefore requires simultaneously being "distinctive" and "hooked (assimilable)": too homogeneous → add mass; too alien → not stored; the sweet spot → add a dimension.

**Strong form and weak form 【this paper adopts the strong form】**: the weak form says distinctiveness → adds **mass** (test: recall rate); the strong form says distinctiveness → adds **rank** (test: **the rank of the memory matrix**). This paper explicitly adopts the strong form — the criterion for "whether it is remembered" should not be the recall rate but "**whether the rank has grown.**"

**How to falsify / how to measure.** The strong form gives a hard test: construct a memory matrix, perform incremental Gram–Schmidt on it along a sequence, and measure the **residual norm spectrum** $\|\vec v_t\|\sim t$ and **the change of effective rank over time**. If after distinctive events the rank shows no significant growth (only mass growth), then the strong form is replaced by the weak form. A ready-made outlet on the AI side is "rewarding the novelty of surprise rather than the amount of surprise" (*Beyond Surprise*) and dynamic-rank methods (DyLoRA / Net2Net / the growth of MoE) 〔anchor〕.

**Differential positioning.** Compared with the von Restorff effect, Brewer's optimal distinctiveness, and Bjork's desirable difficulty, this paper **rewrites all three from "phenomenological descriptions" into a single matrix operator** (add a column / add mass), and **replaces "recall rate" with "rank" as the criterion**. This is the sharpest cutting edge between this paper and the existing conclusions of cognitive psychology.

**Why "adding rank" is more fundamental than "adding mass" (the paper's core argument)**. Mass-type memory only strengthens weights on existing dimensions, and its expressible set is unchanged; only rank-type memory genuinely extends "what can be expressed." The difference is clearest in a destruction experiment: if you downsample / sparsify mass-type memory, the information is largely recoverable (the redundancy remains); if you perform the same operation on rank-type memory, what is unrecoverable is precisely that column itself. Hence this paper asserts: **whether a system "has learned" is better judged not by how firmly it remembers old events (mass) but by whether its representational rank has been raised by some interaction (rank).** This assertion can be directly tested by Experiments 1 and 2.

**Falsifying the boundary condition.** If the sweet-spot proposition holds, it should yield an **inverted-U curve**: with "the degree of deviation from the existing schema" on the horizontal axis and "rank increment" on the vertical axis, high in the middle and low at both ends (too homogeneous yields no rank increase; too alien is not stored). This curve is runnable — one need only inject stimuli of varying deviation into the same memory matrix and measure the rank increment. If the curve is monotonic, the sweet-spot proposition is falsified.

### 3.3 Construct Three: Reachability Geometry — the Metric Is Transport Cost, Not Similarity

**Claim Four 【original upgrade】.** Concept spaces have long been formalized: a concept = a convex region in a multi-dimensional "quality-dimension" space, and similarity = distance 〔anchor: Gärdenfors, *Conceptual Spaces*〕. This paper makes a **key upgrade**:

| | Similarity geometry | Reachability geometry |
|---|---|---|
| distance = | Euclidean / cosine ("looks alike") | geodesic / transport ("can be walked to") |
| symmetry | symmetric | **directed** |

**Two things can be very alike yet unreachable, and unlike yet separated by a single wall.** Prior work has approached this from both sides: Isomap replaces Euclidean distance with graph shortest paths 〔anchor: Tenenbaum 2000〕; successor representations encode "where one will go in the future" 〔anchor: Dayan 1993; Stachenfeld 2017〕. **The difference of this paper lies in elevating "reachability" to the **sole** metric of concept space, and writing it as transport cost**:

$$d_{\text{reach}}(x,y)=\begin{cases}\text{shortest-path cost}, & x,y \text{ connected}\\ \infty, & \text{disconnected}\end{cases}$$

**The minimal controlled pair (the only retained instance).** The positive example is **the pair of socks**: when one sock appears, the other must lie on the reachable path "wash → dry," and the subject performs pattern completion through continuity + binding 〔anchor: Spelke's core knowledge — objects move along unbroken paths; pattern completion in associative memory〕. The negative example is **the sparrow**: a sparrow outside the window and a moth inside the window are **Euclidean face-to-face with infinite reachability** (a glass partition), and the sparrow **can see but cannot catch** — it is using similarity geometry to solve a problem of reachability geometry. On this basis the paper offers a "diagnosis name": **"sparrow hitting glass" = the failure of every similarity-driven agent: mistaking "near" for "reachable."**

**Varying with the subject (affordance).** In the same space, the sparrow's and your reachability graphs differ: you have no wings, it cannot open the door 〔anchor: Gibson, affordance〕. The metric therefore varies with the subject's action set $a$: $d(x,y)\to d(x,y;a)$. The room is shared (the structure of concept space), the key is personal (the path of access). The glass is a **cut** that severs the space into two connected components; **a room = a reachable component enclosed by walls** — the modeling implication is "**learn the walls first, then learn the geometry.**"

**The AI skeleton thereby obtained (this paper's operational corollary)**: the system's space should be represented as a **world graph** (nodes = landmarks, edges = traversable passages), and its learning objective is not to fit point-pair similarity but to fit **transport cost**; "walls" (cuts / impassable edges) should be explicitly learned, because it is the walls that define the connected components and hence the boundary between "reachable" and "unreachable." Compared with successor representations 〔anchor: Stachenfeld 2017〕, the difference of this paper is that successor representations learn "the expectation of visiting various places in the future starting from state $s$," whereas this paper requires **learning the unreachable regions as well** (the $\infty$ cost) — that is, one must learn not only "where one can go" but also "where one cannot go." The former determines planning, the latter **boundary awareness**, and the lesson of "the sparrow hitting glass" is precisely that a similarity-based agent lacking boundary awareness will physically hit the wall.

**How to falsify / how to measure.** The **"pair of socks + sparrow" minimal benchmark** of §5 gives a decisive test: a positive example (given one sock, locate the other) + a negative example (Euclidean face-to-face but separated by glass, judged "unreachable"). **Any purely similarity-based model must fail the negative example** — it will give the erroneous judgment "reachable" on the negative example. This is the experiment in this paper that is easiest to run and also easiest to refute.

**Why "directedness" is key rather than a detail.** Similarity is naturally symmetric ($x$ resembles $y$ $\iff$ $y$ resembles $x$), whereas reachability is naturally directed (the cost of $x\to y$ can be far lower than that of $y\to x$, or even $x$ can reach $y$ while $y$ cannot return to $x$). This asymmetry is not an ornament but the way to reinsert the "agent" into geometry: once the metric is directed, geometry ceases to be a passive "alike or not" and becomes the agentive question of "from where one sets out, and where one can go." **Reachability geometry thereby aligns mathematically with the substrate-neutral definition of §2** — the "source point" of the geometry is the subject, and the edges are the action set $a$.

### 3.4 Construct Four: Two-Layer Memory — the Structure Layer and the Index Layer

**Claim Five 【original structure】.** Memory is split into two layers:

| | Structure layer | Index layer |
|---|---|---|
| what it stores | entities / dimensions (columns) | arbitrary labels / proper-name pointers |
| writing rule | distinctiveness → add a column (MB Rule) | repeated co-occurrence → strengthen binding |
| failure mode | no peak → confusion | edge blocked / interference → TOT (tip of the tongue) |
| AI counterpart | **parametric memory** (representation) | **non-parametric memory** (retrieval) |

**The core assertion is dissociability**: the entity can be intact while the "entity → name" edge is blocked (proper-name anomia / TOT). Prior work has given the mechanism: Levelt's two-step lexical access (lemma → word form) and "pure proper-name anomia" (storage intact, retrieval impaired) 〔anchor〕. **The difference of this paper lies in mapping these two levels onto the AI dichotomy of parametric / non-parametric memory** 〔anchor: RAG, PKM, Engram〕, and in pointing out that **failure types can be classified accordingly**: structure-layer failure manifests as confusion (no peak), index-layer failure as TOT (edge blocked).

**Structure = the sediment of process 【following Piaget】.** Structure is not a static scaffolding but "the steady state sedimented from ordered processes" 〔anchor: Piaget, mental structure as the schema of action〕. Each freezing records one entry; only a new dimension (distinctiveness) adds a column, while repetition merely fills mass. Thus "building a floor = adding a column (new dimension) / renovating = filling densely (new configuration)" becomes a computable distinction.

**How to falsify / how to measure.** A **dual-task dissociation experiment** can be constructed: have a model / subject reproduce "recognizing yet unable to name" under conditions where the structure layer is clear and the index layer is impaired, and measure rank (structure layer) and retrieval-edge weight (index layer) separately. If the failures of the two layers cannot be dissociated, the two-layer hypothesis is simplified away.

**Why it must be split into two layers (the reason this paper gives).** If memory were a single-layer vector, "the entity exists" and "the entity can be named" would necessarily co-vary — but the TOT phenomenon is precisely the separation of the two: the entity is present, the name is also present, yet only the connection is blocked. To explain this, a single-layer model can only appeal to "insufficient global activation," which would in turn predict that "entity recognition should also worsen," contrary to clinical observation. The two-layer hypothesis explains the dissociation at minimal mechanistic cost, and incidentally explains why a name is an "arbitrary, meaningless anchor" (the index layer does not participate in the rank growth of the structure layer). **This reasoning is the hinge by which this paper connects the facts of cognitive pathology with AI memory architectures.**

### 3.5 Construct Five: Co-Constructed Scaffolding — the Reachability Expander

**Claim Six 【original law】.** A scaffold = a **reachability expander**: it **adds edges** to a growth graph. This corrects "structure is intelligence":

> **Structure is the enabling condition of process; intelligence is the processes that structure enables.**

**The calibration proposition 【this paper sews four skins into one law】**: if the scaffold is too sparse → one cannot cross (unreachable); too dense → over-scaffolding (no growth); just right → reachable yet leaving room for exploration. And **ZPD 〔anchor: Vygotsky〕 / desirable difficulty 〔anchor: Bjork〕 / optimal distinctiveness 〔anchor: Brewer〕 / the MB sweet spot 〔this paper〕 — are four skins of the same law of "calibrated novelty."** Withdrawal of the scaffold is a **negotiation**: a scaffold without fading manufactures dependence rather than ability 〔anchor: Collins, Brown & Newman, fading〕; the difference between a scaffold and an environment lies precisely in "whether it is expected to be withdrawn."

**Closing the view of the subject (co-construction).** The scaffold is not erected unilaterally but is the result of co-construction 〔anchor: Vygotsky; niche construction — Odling-Smee / Laland's reciprocal causation; Giddens' duality of structure; the extended mind〕. **The physical mechanism of consensus (following Zurek)**: one freezing = private (only you know it), repeated freezing (redundancy) = objective structure (everyone acknowledges it) — **consensus = multiple agents redundantly recording the same fact**.

**How to falsify / how to measure.** A runnable design already exists: vary "scaffold density / allocation of withdrawal rights" and measure whether the agent becomes **independent** or **dependent** (see item 8 of §5). If ability does not fall but rises after withdrawal, the enabling relation "scaffold = expander" is supported; if it collapses upon withdrawal, that structure was in fact a crutch rather than a scaffold.

**A logical tightening (this paper's self-constraint).** Since structure is merely the sediment of process (§3.1, §3.4), the very term "scaffold" easily slides toward the old stance of "structure is intelligence." This paper blocks that slide with one sentence: **structure is the enabling condition of process; intelligence is the processes that structure enables.** In other words, a scaffold apart from a climber is an empty causal act; expansion occurs only when we regard "erect the scaffold — climb — withdraw the scaffold" as an indivisible **interaction process**. This step at the same time carries through to the end the "relationality" principle of §2: intelligence resides neither in the scaffold (condition) nor in the climber (individual), but in the **coupling process** of the two.

---

## 4 The Corollary about Time: The Demotion of Time

**Claim Seven 【original corollary】.** From §3.1, "structure = the accumulation of frozen decisions" and order is intrinsic to structure (a DAG), so:

> **Time as a "container / axis" is superfluous; structure (the frozen DAG) is the primitive.**

The corollary unfolds into three sentences: **time is the bookkeeper** — it only records and has no decision-making authority; **but it retains binding authority** — recording is an irreversible constraint 〔anchor: Landauer, erasure has a cost〕, and what is recorded becomes the boundary of subsequent decisions (the bookkeeper has no vote, yet the ledger it writes becomes the constitution of later generations; in the original metaphor, the "eunuch" does not vote, but the ledger it writes becomes the constitution of what comes after); **the arrow comes from the choices of agents** — in fundamental physics there is no direction of time, and causal direction is a shadow projected by "agents that choose" 〔anchor: Yale physics lectures citing Russell〕. It closes with: **agency (the openness of T0) is primary; time is the shadow it casts.**

**Prior anchors and differences.** Lamport long ago maintained that "happens-before (causal order) is the true time, and the wall clock is only a lossy projection" 〔anchor: Lamport 1978〕; Hume maintained that causation is only the constant conjunction of events; McTaggart / the B-theory / the block universe maintain that the flow of time is an illusion; Rovelli's *The Order of Time* says "the world is events, not things"; Barbour's *The End of Time* and Page & Wootters say time emerges from entanglement 〔anchor〕. **The difference of this paper from these is twofold**: (i) it is not a "time does not exist" derived from physics but a **derivativeness** derived from the **mechanism of memory writing** — time is the bookkeeping quantity of the "freezing sequence"; (ii) it **retains the binding authority of time**, thereby avoiding the overly strong claim that "time is a pure illusion." An engineering isomorphism: the append-only log (Kafka / event sourcing) is mechanically the bookkeeper — it does not decide, it is the truth itself, and "the commit determines the timestamp."

**How to falsify / how to measure.** See item 6 of §5, the **positional-encoding ablation**: remove the positional encoding from data in which "order is already encoded in the content" — if performance does not drop, this verifies "structure carries its own order and the external axis can be dispensed with."

**The three-part structure of the "bookkeeper" metaphor and its testable implications.** This metaphor can be decomposed into three separately testable assertions: **(A) time does not decide** — the time variable itself carries no information; the test is to remove it from the model input and see whether prediction is impaired (positional-encoding ablation). **(B) time only records** — the entire content of time is the freezing sequence it records; the test is to see whether the "commit order" can fully reconstruct the "timestamp" (event-sourcing-style reconstruction). **(C) time has binding authority** — a recorded fact irreversibly delimits subsequent possibilities; the test is to see whether editing the history changes the future reachable set (a history-editing experiment). The three assertions are each independently refutable, which makes "the demotion of time" not a piece of mysticism but three cards that can be torn up.

**The relation to the "emergence of time" school.** Barbour, and Page & Wootters, maintain that time emerges from entanglement / constraint; this paper is in tune with them but **lands in the opposite direction**: it does not ask "how time emerges from a timeless physics" but asks "in a system that already keeps accounts with structure, what powers remain to time." The answer is: only binding authority remains. This turn depends on no assumption of quantum gravity and is therefore equally operational for social–cognitive–AI systems. In brief: this paper does not ask where time comes from but asks **what powers remain to time in a system that keeps accounts with structure** — the answer being: only record and constrain, not decide; and "recording" itself is a constitution available for later generations to invoke.

---

## 5 The Falsifiable Criterion and Experimental Outlook

All propositions in this paper converge on **a single criterion**: **measure whether the mutually-reachable set / representational rank of the two parties has grown before and after the interaction.** For the criterion to be executable, it must first be parameterized: the **rank** side is measured by the curve over time of the effective rank (a stable rank estimate of spectral decay); the **reachability** side is measured by the curve over time of the mutually-reachable connected components (the strongly connected structure on the discretized feasible graph). The two curves cross-check each other: if rank rises while the reachable graph is unchanged, this indicates "expressive expansion but no action expansion" (column-adding at the epistemic level); if reachable edges increase while rank is unchanged, this indicates "action expansion but no expressive change" (edge-adding at the scaffold level). The separation of the two is itself yet another observable, refutable prediction. A set of runnable experiments derives from this:

1. **Effective-rank curve**: build representation matrices binned by developmental stage, and measure the change of effective rank over development. Prediction: **rises during the scaffold period, saturates during the explosion period.**
2. **GS residual spectrum**: plot $\|\vec v_t\|\sim t$. Prediction: **peaks during the scaffold period, flattens during the explosion period.**
3. **Forward-order vs. reverse-order residual inequality** (the "scaffold" signature): **the late-stage residual in forward order $\ll$ reverse order.**
4. **Permutation null hypothesis**: shuffle ≥100 times and see whether forward / reverse order fall at the **two tails of the distribution** (rather than the middle).
5. **The "pair of socks + sparrow" minimal benchmark**: a positive example (given one sock, locate the other) + a negative example (Euclidean face-to-face but separated by glass, judged "unreachable"). **A similarity model must fail the negative example.**
6. **Positional-encoding ablation**: remove the positional encoding from data in which "order is already encoded in the content" — no drop → verifies "structure carries its own order and the external axis can be dispensed with."
7. **LoRA order experiment**: train small models in stage order / reverse order / scrambled order, and compare the principal angles / Grassmann distance of the $\Delta W$ subspaces 〔anchor: LoRA / DyLoRA / RSLoRA〕.
8. **Co-constructed scaffolding**: vary "scaffold density / allocation of withdrawal rights" and see whether the agent becomes **independent** or **dependent**.

**The meta-level self-constraint of the criterion**: each of the above gives a prediction that can be overturned by data; in particular, Experiments 1 and 5 constitute a direct test of this paper's two strongest claims (the expansion criterion and reachability geometry).

**Which claim each experiment tests**: Experiments 1 and 2 test **the expansion criterion and the MB Rule** (whether rank / residual grows in a structured way); Experiments 3 and 4 test **T0 freezing and "order does not commute"** (whether forward and reverse order occupy the two tails of the distribution); Experiment 5 tests **reachability geometry** (whether a similarity model fails on the negative example); Experiment 6 tests **the demotion of time** (the external axis can be dispensed with); Experiment 7 tests **the projection of the MB Rule into parameter space** (the effect of order on subspace geometry); Experiment 8 tests **co-constructed scaffolding and the withdrawal proposition** (expander vs. crutch). Eight experiments correspond to seven claims, and no claim is left dangling.

**Design principles and known limitations.** This paper acknowledges three limitations: **first**, the "effective rank" is estimated with bias under a finite sample, so Experiments 1 and 7 need to report confidence intervals and permutation null distributions rather than single-point comparisons; **second**, the "mutually-reachable set" in a continuous space needs to be discretized into a feasible graph, and the granularity of discretization affects the conclusions, so it should be reported jointly with the cut decision of Experiment 5; **third**, this paper uses "rank growth" as the threshold of intelligence's sufficiency, which may be too strict under extreme sparse sampling — a system that increases rank in only very few interactions still counts as intelligent by this paper but is statistically hard to distinguish from noise. These limitations do not weaken the claims; rather, they point out the three most important sources of false positives to guard against when the criterion is put into practice.

---

## 6 Relation to Existing Work

The positioning of this paper can be summarized as "three borrowings and three advances": **borrowing the vocabulary of actualization from physics to derive the mechanism of memory writing; borrowing the developmental facts of cognitive science to derive reachability geometry and the law of column-adding; borrowing the dual-memory architecture of AI to derive a classification of failures and a law of growth.** The common move in all three is not to introduce new facts but **to rearrange already-existing, scattered facts onto a single axis of derivation** and to let them constrain one another — which is precisely the form of contribution a position paper should have. The table below gives, layer by layer, the anchors and the linkages:

| Layer | Prior anchors (positioning references) | This paper's linkage / advance 【original】 |
|---|---|---|
| **Physics** | Rovelli (relations / actualization), Wheeler (participation / questioning), Zurek (redundancy / objectification), Lamport (causal order), Barbour, McTaggart, Hume | Connect "actualization of state" to "the definition of intelligence" and "the demotion of time": **T0 freezing** becomes the mechanism of memory writing |
| **Cognition** | Vygotsky (ZPD / collaboration), Piaget (structure = schema of action), Gärdenfors (concept spaces), Spelke (core knowledge / object tracking), Waddington (canalization), Levelt (lexical access), von Restorff, Brewer, Bjork, Gibson | Rewrite "concept space" with **reachability**; rewrite "distinctiveness" with **column-adding / rank-adding**; sew four calibration phenomena into **one law** |
| **AI** | RAG / PKM / Engram (parametric + non-parametric memory), successor representations, world graphs, Isomap / optimal transport, modern Hopfield = attention, DyLoRA, de Haan (causal confusion) | Give the failure classification of the **parametric-layer + index-layer** two-layer architecture and an entry point for "reachability learning"; ground the MB Rule as a **law of growth** |

**The list of this paper's original constructs (explicitly marked)**: ① the **T0 freezing mechanism**; ② the **MB Rule** (the unconventional → add a column, the conventional → add mass; strong form = add rank); ③ **reachability geometry** (metric = transport cost, not similarity); ④ **two-layer memory** and its failure classification; ⑤ the law of **co-constructed scaffolding** (reachability expander + calibration + joint withdrawal); ⑥ the **demotion of time** (time as bookkeeper).
**Those that explicitly belong to prior anchors, to which this paper only provides linkages**: process / relational ontology, quantum actualization, quantum Darwinism, causal order (Lamport), concept spaces (Gärdenfors), ZPD (Vygotsky), core knowledge (Spelke), the parametric / non-parametric memory dichotomy (RAG / PKM), successor representations, Isomap, LoRA.

---

## 7 Conclusion

This paper starts from a single intuition — **order is meaning** — and converges onto seven claims on a single axis: intelligence is an **expansive interaction process** (substrate-neutral, criterion = whether the mutually-reachable set / representational rank grows); its microscopic mechanism is **T0 decision → T0+1 freezing**; its law is the **MB Rule** (the unconventional adds a column, the conventional adds mass; strong form = add rank); its geometry is **reachability geometry** (metric = transport cost); its structure is **two-layer memory** (structure layer / index layer); its subject is **co-constructed scaffolding** (a reachability expander, jointly built and jointly withdrawn); and its corollary is the **demotion of time** (time as bookkeeper, with no decision-making authority but with binding authority, its arrow coming from the choices of agents).

Its ambition in one sentence: **every T0 decision sediments a layer of structure; the order of this pile of structure is time; and it is meaning — intelligence is that interaction which makes this sedimentation "expand."**

**What this paper claims and what it does not**: it claims a **falsifiable definition** and seven interlocking corollaries; it does **not** claim that intelligence can be realized only by some class of substrate (the definition itself is substrate-neutral), nor does it claim that time "does not exist" (time is present in the role of bookkeeper and holds binding authority). If subsequent experiments overturn the key predictions of §5 — especially the two "a similarity model must fail the pair-of-socks / sparrow negative example" and "ability does not fall but rises after withdrawal" — the core criterion of this paper is weakened; the paper is willing to accept this cost in exchange for the testability of its claims. This is precisely the way of writing a position paper: to write out, as clearly as possible, the things that can be overturned.

---

## References (Anchors, by Theme)

- **Process / relation / time**: Whitehead, *Process and Reality*; Rovelli, *Relational Quantum Mechanics*; Rovelli, *The Order of Time*; Wheeler, *Information, Physics, Quantum: The Search for Links* ("It from Bit"); Zurek, *Quantum Darwinism*; Barbour, *The End of Time*; Page & Wootters, *Evolution without Evolution*; McTaggart (1908); Hume, *A Treatise of Human Nature*; Lamport (1978), *Time, Clocks, and the Ordering of Events in a Distributed System*.
- **Cognition / development**: Vygotsky (1978); Wood, Bruner & Ross (1976); Collins, Brown & Newman (1989); Bjork & Bjork (desirable difficulties); Piaget (structuralism / schema of action); Waddington (canalization); Spelke, Carey & Xu (2001) (core knowledge); Gärdenfors (2000), *Conceptual Spaces*; von Restorff (1933); Brewer (1991); Gibson (affordances); Levelt (two-step lexical access); Semenza & Zettin (pure proper-name anomia); Collins & Loftus (1975) (spreading activation); de Haan et al. (2019) (causal confusion).
- **AI / mathematics**: Lewis et al. (2020) (RAG); Lample et al. (2019) (PKM); Engram (DeepSeek); Dayan (1993) / Stachenfeld et al. (2017) (successor representations); Tenenbaum, de Silva & Langford (2000) (Isomap); Ramsauer et al. (2020) (modern Hopfield = attention); Hopfield (1982); Roy & Vetterli (2007) (effective rank); Hu et al. (LoRA / DyLoRA / RSLoRA); Schrödinger bridge / flow matching.
