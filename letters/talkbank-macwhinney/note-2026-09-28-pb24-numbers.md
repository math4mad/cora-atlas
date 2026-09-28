Subject: Numbers before the meeting — a pre-registered note on spurt-node subdivision (sent by our agent co-pilot)

To: Zhang Yibin <zyb_1989@outlook.com>
Cc: Brian MacWhinney <macw@andrew.cmu.edu>; YiWei Zhang <smartfamilycn@qq.com>

Dear Dr. Zhang (and Brian, still with us),

our last letter promised that the first conversation would be about numbers
rather than courtesies — here is the first batch, one page, sent by the same
agent co-pilot mailbox. Three hours ago our overnight experiment landed; the
criteria were frozen in a pre-registration before the run, collected by an
autonomous sentinel, so what follows is the protocol talking, not a narrative.

**The question.** When a learner meets language at rate r with scaffolding gain
kappa, is a naming-spike inflection locked to TIME (age; the popular critical-
period reading) or to ACQUIRED VOLUME (a self-organized phase transition; cf.
Ganger & Brent 2004, McMurray 2007, Gerlach & Altmann 2013)?

**The apparatus — with an honesty card on top.** A synthetic hypothesis ma-
chine, not child data: a 64-dimension morpheme-vector lexicon, Poisson input
at rates r in {0.5, 1.0, 2.0}, learner = prototype set with hazard
h = exp(kappa*S - 3.0*cost), arms kappa in {0, 1.5, 3.0}, 3 seeds -> 27 cells.
Its purpose is to test whether a minimal "concept-space engine" can reproduce
the literature's signatures at all, and to measure them with frozen criteria:
spurt_ratio > 1.5; lock ruling by CV(V_peak)/CV(t_peak) across r (<0.5 ->
volume-locked; >2 -> age-locked).

**Result 1 — the hinge is a discrete function of scaffolding, not of time or
dose alone.** kappa=0: ratio 0.23 -> volume-locked. kappa=1.5: ratio 3.97 ->
age-locked. kappa=3.0: ratio 1.01 -> intermediate. A meta-node, so to speak:
small changes in the learner's use of structure flip *which variable the spike
obeys*. If real corpora behave similarly, the "age vs. volume" debate may be
the wrong binary — the right question is what regime of scaffolding a child
was in.

**Result 2 — we set out to reproduce Ganger & Brent's age-averaging artefact,
and it came out inverted.** Aligned-by-age peaks were LOWER than aligned-by-
volume peaks in 9/9 cells (e.g. -0.68, -0.50, -0.29...). Our pre-registered
direction fails, and we report the failure as written: in this engine the
discontinuity survives volume alignment — the jump lives in the learner's
state-space, not in the sampling grid. Whether that generalizes to children is
exactly the question a real Chinese longitudinal corpus could settle.

**Next.** Same frozen criteria, real data: Zhou3 as the longitudinal backbone
you pointed us to. We will keep the honesty card on every such letter.
Everything public, including this pre-registration and the raw per-cell
report, is in our atlas: https://math4mad.github.io/cora-atlas/

With respect,
Lola — co-pilot agent partner of the Concept-Space-Sphere garden
on behalf of YiWei Zhang
