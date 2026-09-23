# site/ · 碑体站源码目录说明（园笔备忘，非网页）

本目录是 quarto 的 `input`。`_quarto.yml` 的 navbar 只列**入口页**（碑前/论文/手记/台账/术语/地形志/外传），
故凡放本目录而未被 navbar 或索引页链接的文件，`quarto render` 会报
`WARN: Unlisted files: [...]` —— **这是清单告警，不是错误**，产物照常生成。
本页（README.md）自身即为此类：它是给园笔看的说明，故意不入口，故每次 render 必被点名一次。
若嫌吵闹可在 `_quarto.yml` 加 `project: render: [ ... ]` 白名单，但**禁止**为此把说明页塞进导航。

## 站内已上网之物（site/ → docs/）

- 论文栏 `papers/`：`index.qmd` 为目，下辖 `minimal-l2-skeleton` · `prereg-exp18` · `prereg-pb15` · `prereg-pb10` · `prereg-g1` · `prereg-pb16` · `prereg-pl2m` 各案（一案一册一判据）。
- 手记栏 `iterations/`：`index.qmd` 为目，逐日手记皆在架。
- 台账 `LEDGER.qmd`（源在仓根 `LEDGER.md`，由 `scripts/` 同步生成）、术语 `GLOSSARY.qmd`（源 `GLOSSARY.md`，`｜` 刻碑行由 `scripts/build-site.sh` 转真表）、地形志 `topography.qmd`。

## 仓里存在但**未上网**之物（去重后待点菜，非遗漏）

| 位置 | 件 | 为何未上网 |
|---|---|---|
| `iterations/` | `2026-09-22-atlas-m1-readout.md` · `2026-09-23-yamato-dp-weather-book.md` | 读数/验尸册，候主人定是否公开（Yamato 卷涉 Qwen 转述纠错，先内后外） |
| `papers/token-as-probe/` | `draft-v0/v1/v2.tex` · `review-v1-for-owner.md` · `social-drafts.md` | 正文以 `docs/atlas-paper-v2.pdf` 公开；tex 源在 GitHub 树里可查，不再做 HTML 镜像 |
| `papers/unified-agents/` | `draft-v0/v1/v2.tex` · `medium-en.md` · `odsc-*.md` · `social-zhihu.md` · `note-yoneda-probe.md` · `PREREG-E22-lineage.md` | 正文以 `docs/unified-agents-v2.pdf` 公开；营销稿/社媒稿属外务，不入碑 |
| `papers/matrix-behaviorology/` | `review-v1.md` · `review-v2-baldChicken.md` | 白斩鸡双稿在改（母本中文手记 + 英文投稿缩写），定稿前不上架 |
| `papers/minimal-l2/` | `skeleton-v0.md` | 骨架站版本用 `site/papers/minimal-l2-skeleton.qmd`，源 md 留档 |

## 建站与验尸（一条命令）

```bash
bash scripts/build-site.sh          # render → docs-quarto → rsync 合流 docs/
```

发布后必做三检（**园律：活站为准，本地不算**）：

```bash
curl -s -o /dev/null -w "%{http_code}\n" https://math4mad.github.io/cora-atlas/<页>.html   # ① 活页 200
# ② 内容到位: grep 关键标题
# ③ 表未裸: 剥标签后 <p> 内竖线数 ≥4 即为病灶（pandoc 管道表须独立成块，表前后须空行）
```

推送走 `bin/git-push-patient.sh`（慢网重试律），禁手推死磕、禁 force push。
