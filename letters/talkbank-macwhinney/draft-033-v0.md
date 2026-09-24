# Letter 033 · 致 Brian MacWhinney（TalkBank/CHILDES 管理方）（候朱批 · 未发 · v0）

> 园匣编号 033（承 032）。案由：AGE-LADDER 年阶语料梯 L2 对话层需 CHILDES。
> 主人已于 sla.talkbank.org 注册成功（2026-09-24），但站点前端挂 Google 资源、
> 国内加载极缓；且我方通信须先向数据方**申明研究用途并承诺引用/不回传原文**。
> 收件地址: macw@cmu.edu（talkbank.org 首页明文留的注册/联络通道, 地址=官方自布, 候发送前再核）。
> 发送通道: 同前例（mmads4653@agent.qq.com → agently 授权候检）。

---

Subject: A request from a small research garden in China — CHILDES as structured knowledge for developmentally-ordered model training

Dear Professor MacWhinney,

I am a former statistics teacher, running a small independent research garden
in China. I registered a TalkBank account today (2026-09-24) and am writing to
explain, before downloading anything at scale, exactly what we intend to do
with CHILDES — because our use is deliberately unusual, and you should have it
in writing.

**What we are building.** We study concept spaces as measurable geometry: a
concept is a region in a structured space, categorization is an anchoring
(maximum-similarity) decision, and learning is sequential Bayesian updating
that never resets — today's posterior is tomorrow's prior. Reading Piaget
through this machinery, we noticed something that guides our whole experiment:
the MaxSim anchor mechanism *is* what developmental psychologists call
centration — the hallmark of the preoperational child. Our engine is, by
construction, a child's mind. It therefore needs a child's education.

**The plan (we call it the AGE-LADDER).** We are assembling a legally clean,
age-tiered curriculum: board-book catalogs and public-domain early readers for
the naming and classification layers (0–5), school-era public-domain readers
for the concrete-operational layers (6–15), and adult web text as the
"终态快照" control. The CHILDES corpus — specifically the classic
longitudinal collections (Brown's Eve/Adam/Ken, Bernstein's Rohina,
NewBrunson & Lux) — is the irreplaceable middle layer: it is the only kind of
data in the world that is *ordered by real development*, containing children's
own utterances, errors, questions and negations, at monthly resolution.

**What we will measure.** We train/fine-tune small language models (0.5B–7B,
adapter-level, on modest compute) on the *same corpus bag* under two feeding
regimes: strictly stage-ordered exposure versus shuffled exposure. The
hypothesis is that order itself leaves a trace in internal parameters: we
track, layer by layer, how adaptation subspaces (ΔW spectra, principal angles
between concept regions, per-dimension feature weights) are born, migrate, and
become irreversible — a developmental trajectory of "animism hump" events
(the child's moon first joining the animal region, later migrating out, and
not returning under replay of the original evidence). To our knowledge no one
has used CHILDES as a *temporal curriculum* rather than a descriptive corpus;
we believe the parameter-change laws we hope to extract are new to both
developmental science and to the interpretability literature.

**Our commitments to TalkBank.**
1. Every published result will cite each corpus used and acknowledge
   NICHD HD082736, per your access rules.
2. We will not re-host or redistribute raw CHAT files. We will publish only
   derived measurements (feature norms, trajectories, verdict tables).
3. Our code and derived data will carry the same spirit of open sharing
   (CC BY-NC-SA), and we will send you a copy of any paper that uses CHILDES
   in this way — you may cite it, correct it, or veto our reading of your
   corpus.
4. This work is a garden, not a company: no commercial use, ever.

**One practical ask.** The TalkBank web browser loads its interface from
Google-hosted assets, which are impractical to reach reliably from here.
Could you point us to the most bandwidth-frugal acquisition path for the
collections named above — e.g. the CLAN command-line `@Explore` bulk
download over HTTPS, or any plain-HTTP archive route that does not depend on
the single-page app? We only need to be polite to your servers and to the
law.

Thank you for keeping CHILDES open for four decades. If our small experiment
shows that developmental *order* is a measurable variable in parameter space,
the first evidence will carry your corpus's name.

With respect,

[Owner's name — to be filled by the owner]
Independent Research Garden (Concept-Space-Sphere), China
TalkBank account email: [registration email]

---

> 匣注: ①正文 AI 起草（阅读伴侣协助）, 人类负全责 —— 发前主人过目改句;
> ②署名与 TalkBank 注册邮箱两处空格**必须人填**, agent 不得代填;
> ③附件: 无（首信不裸弹, 待回音再决定是否附 DESIGN_ladder 摘要页）。
> ④路由: 甲案直邮 macw@cmu.edu; 乙案走 TalkBank 站内消息/Google Group
>   chibolts@googlegroups.com 公开帖（30 天无回音即乙案, 同 Strang 例）。
