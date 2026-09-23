#!/usr/bin/env bash
# 碑体建站: quarto 渲染 site/ → docs/ (Pages 源), 旧站诸 PDF/页原样保留。
set -euo pipefail
cd "$(dirname "$0")/.."
Q=${QUARTO:-$HOME/tools/bin/quarto}
[ -x "$Q" ] || { echo "✘ quarto 未就位"; exit 1; }
# 术语碑: ｜ 分隔行 → markdown 真表 (源文件保持凿刻体)
python3 - <<'PY'
import re
src=open("GLOSSARY.md").read().splitlines()
out=[]; buf=[]
def flush():
    if buf:
        out.append("")
        out.append("| 术语 | 义 | 账 |"); out.append("|---|---|---|")
        for ln in buf:
            parts=[p.strip() for p in re.split("｜|\|", ln) if p.strip()]
            if len(parts)>=3:
                t,e,a=parts[0], " ｜ ".join(parts[1:-1]), parts[-1]
            elif len(parts)==2:
                t,e,a=parts[0],parts[1],"—"
            else:
                t,e,a=parts[0] if parts else "","—","—"
            out.append(f"| **{t}** | {e} | {a} |")
        buf.clear(); out.append("")
for ln in src:
    if ("｜" in ln or ("|" in ln and not ln.startswith("#"))) and not ln.startswith("|---"):
        buf.append(ln)
    else:
        flush(); out.append(ln)
flush()
open("site/GLOSSARY.qmd","w").write("\n".join(out)+"\n")
PY
# 外传: 注入碑体导航条
python3 - <<'PY'
src=open("docs/gaiden.html").read()
if "cora-nav" not in src:
    nav='<div class="cora-nav" style="background:#2b3a42;padding:.6rem 1rem;max-width:880px;margin:0 auto;border-radius:0 0 8px 8px"><a href="index.html" style="color:#f2efe8;text-decoration:none;margin-right:1.2rem;font-weight:600">🏛 碑前</a><a href="papers/index.html" style="color:#f2efe8;text-decoration:none;margin-right:1.2rem">论文</a><a href="iterations/index.html" style="color:#f2efe8;text-decoration:none;margin-right:1.2rem">迭代手记</a><a href="LEDGER.html" style="color:#f2efe8;text-decoration:none;margin-right:1.2rem">台账</a><a href="GLOSSARY.html" style="color:#f2efe8;text-decoration:none">术语碑</a></div>'
    src=src.replace("</head>",'<style>body{background:#fdfcf9;color:#2d2d2d} a{color:#b05f24}</style></head>')
    src=src.replace("</h1>","</h1>"+nav) if "</h1>" in src else src.replace("<body>","<body>"+nav)
open("docs/gaiden.html","w").write(src)
PY
# 台账同源归化: LEDGER.md → site/LEDGER.qmd (孤行账行转鎏刻体, 免被 pandoc 吐成裸竖线)
python3 scripts/ledger-normalize.py LEDGER.md site/LEDGER.qmd
( cd site && "$Q" render )
rsync -a docs-quarto/ docs/ 2>/dev/null || cp -R docs-quarto/. docs/
python3 scripts/shelf-links.py docs/GLOSSARY.html docs/LEDGER.html

echo "✔ 碑体站成: docs/ ($(find docs -name '*.html' | wc -l | tr -d ' ') 页)"
