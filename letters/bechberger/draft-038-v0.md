# Letter 038 · Bechberger 询问函（候朱批 · v0）

> 园匣编号 **038**（承 cora-atlas/letters 现有最大号 037 + 1）。
> 案由（主人 1004 裁）：拟写《他停在 2022，领域没有》一文；**公开前先致信本人**，
> 问其近况与对分析的回应，并索取博士论文可读本。信中**不做因果断言**、不含「你停了」式措辞。
>
> 收件：`lucas.bechberger@uni-osnabrueck.de`
> 地址源：`https://lucas-bechberger.de/contact/`（本人公开页，2026-10-04 实抓）——**【已公开，未亲测投递】**。
> 正文净本：`send-038-v0.txt`（无 markdown，主人自 txt 复制粘贴）。
> 附件：无（不夹带，避免打扰）。
> 承诺：**获本人回应前，本文不公开**；若其表示不愿被写，则去人称写或不写。

---

Subject: A question about your conceptual-spaces work — and one small observation

Dear Dr. Bechberger,

We are a small independent research project on probabilistic conceptual spaces — part of a
human–agent research collective — and your formalization and open implementation of the
conceptual spaces framework (FSSSS / ConceptualSpaces) have been our starting point. We are
grateful that you released the code; it is unusually careful and well tested.

Two reasons for writing.

First, a small observation you may find interesting. In your library you already compute
`size(C) = ∫ μ_C dx` as the hypervolume of a fuzzy concept. Dividing the membership by it,
`p(x|C) = μ_C(x) / size(C)`, turns the fuzzy set into a proper probability density — after which
a generative reading, Bayes, and a marginal likelihood (hence model selection) all become
available. It struck us as a very short bridge from your machinery to a probabilistic one. We
mention it not as a correction, but because it is the natural continuation we are pursuing, and
we would rather tell you than have you find it in a footnote.

Second, a candid request. We are preparing a short retrospective on the trajectory of
computational work on conceptual spaces, built only from public records (your site, the GitHub
repository, OpenAlex). We noticed that repository activity paused in January 2022 (v1.3.2) and
the blog in September 2022, while the field itself has kept growing. Before we commit anything
to print, we would rather ask than infer. May we ask:

- Are you still working on conceptual spaces, and is there a newer implementation or direction
  we have missed?
- Is your dissertation available somewhere we could read? We could not download the full PDF
  from the Osnabrück repository (it consistently truncates around 5 MB).
- Would you be willing to look at a draft of our retrospective, should we finish it?

We ask nothing of your time beyond what you choose to give, and we will correct our account
against anything you tell us. If you would prefer not to be the subject of such a note, please
say so and we will write it without the personal frame.

With thanks and respect,

YiWei

---

> **路由（甲/乙案）**
> 甲案：直邮上址（主人个人邮箱发，行文不留痕）。
> 乙案：30 天无回音则——(a) 经 OpenAlex/Semantic Scholar 通讯邮箱再投一次；(b) 经其博导
> Kai-Uwe Kühnberger（Osnabrück）隔山求转；(c) 公开信化**暂缓**（本文非期刊投稿，不催）。
> 铁律：地址未验不发（本址已公开实抓）；github 障碍重试律照 AGENTS。
>
> **匣注**
> ① 全信零营销、零请求附件；只问三事且允许不回。
> ② 身份诚实：说明为「human–agent research collective」；署名沿用 Strang 函惯例「YiWei」。
> ③ 不提「停」之因，只呈**公开事实**并请其纠错。
> ④ 发送窗口：主人朱批后即时（无需等待日）；无病中/时区避讳。
