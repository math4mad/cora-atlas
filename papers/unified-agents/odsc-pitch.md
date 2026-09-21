# ODSC 投稿包（入口 https://odsc.ai/contact-us/ → Blog contribution；亦投 editor@odsc.com 惯例地址）

## 表单/邮件正文（整段粘贴）

Subject: Pitch — "We Built a Theory Garden and Let It Punch Us: Measuring Concept Spaces with LoRA Angles"

Dear ODSC editors,

We would like to offer a guest post for the ODSC blog: a hands-on account of a small open research project ("The Cora Project") that measures concept spaces inside 0.5B–7B language models using nothing but LoRA adapters, linear probes, and high-school geometry.

What the reader gets:
- A reproducible recipe: train 11 mixture-ratio adapters on two tiny corpora (30 GPU-minutes on one free Kaggle T4), then solve the triangle between their weight vectors.
- A concrete result we did not expect: mixture midpoints sit 44°–47° off the geodesic between their parents — conserved across unrelated corpus pairs ("composition is parthenogenesis").
- An ordinal-density law: narrative order rotates weights by 7°, social rankings (Ballon d'Or, NBA draft, MLB WAR) by 56°, domain change by 85° — with a 9/9 diagonal NLL matrix and a built-in null control.
- An honest failure, front and center: our scale-monotonicity prediction broke at 7B, and we publish the breach with three candidate causes and a scheduled adjudication — as a demonstration of pre-registered, ledger-driven research (PREREG before every run; git history as receipts; stateless kernels as the strictest "new session" there is).

Draft is complete with numbers frozen pre-judgment; every experiment is a stateless Kaggle kernel we can attach. Author byline: Yiwei Zhang (The Cora Project), with "Lola", the project's AI host, credited as co-editor.

Link to the theory paper (v2, 5pp): math4mad.github.io/cora-atlas
Would you consider it? We are happy to adapt tone, length, or figures to ODSC style.

Best,
Yiwei

## 正文（若编辑回信索要）
直接给 `medium-en.md` 的 BODY 段——仅需两处改写即成 ODSC 版：
1. 首节"unfriendly sentence"的哲学腔降半度，前面加一句教程承诺："In this post you will learn to measure how LoRA adapters remember order, domain, and mixture — in under an hour of free GPU."
2. 结尾加一节 "Try it yourself"：三行指令（fork kernel → 换语料 sha → 重跑 11 点扫描），符合 ODSC 读者口味。

## 账
- 状态：待主人过目 → 发送（表单人机验证需人工，家法同款）。
- Medium / TDS / FreeCodeCamp 三腿与本案并行不互斥（一稿多发需在 pitch 里声明 prior/public availability——咱们全开源，天然合规）。
