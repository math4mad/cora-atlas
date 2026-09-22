#!/usr/bin/env bash
# 碑体建站: quarto 渲染 site/ → docs/ (Pages 源), 旧站诸 PDF/页原样保留。
set -euo pipefail
cd "$(dirname "$0")/.."
Q=${QUARTO:-$HOME/tools/bin/quarto}
[ -x "$Q" ] || { echo "✘ quarto 未就位"; exit 1; }
( cd site && "$Q" render )
rsync -a docs-quarto/ docs/ 2>/dev/null || cp -R docs-quarto/. docs/
echo "✔ 碑体站成: docs/ ($(find docs -name '*.html' | wc -l | tr -d ' ') 页)"
