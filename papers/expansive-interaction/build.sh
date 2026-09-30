#!/usr/bin/env bash
# 位置论文《Intelligence as an Expansive Interaction Process》重排脚本
# 治: ① 公式未渲染(Writer 导出把生 LaTeX 当文本) ② 缺字(【】〔〕①–⑥) ③ 书名斜体
# 源: source.md (Markdown, 数学走 $...$ / $$...$$); 排: pandoc → tectonic
set -euo pipefail
cd "$(dirname "$0")"

PANDOC="${PANDOC:-/Users/mac/Applications/quarto/bin/tools/pandoc}"
ENGINE="${ENGINE:-tectonic}"
CJKFONT="${CJKFONT:-PingFang SC}"
OUT="out"
mkdir -p "$OUT"

# --- 预处理 (源不动, 只清渲染障碍) ---
python3 - source.md > "$OUT/clean.md" <<'PY'
import re, sys
c = open(sys.argv[1], encoding='utf-8').read()
# ① 去书名斜体 *Title* → Title (不碰 **粗体** 与数学)
c = re.sub(r'(?<![\*\\])\*(?!\*)([^*\n]+?)\*(?!\*)', r'\1', c)
# ② ≥ 走数学; 尾随空格防 pandoc 因「闭$紧挨数字」而转义成 \$\geq\$
c = c.replace('≥', r'$\geq$ ')
sys.stdout.write(c)
PY

# --- 排 ---
"$PANDOC" "$OUT/clean.md" -o "$OUT/expansive-interaction-v2.pdf" \
  --pdf-engine="$ENGINE" \
  -V CJKmainfont="$CJKFONT" \
  -V geometry:margin=1in \
  -H header.tex

echo "✔ $OUT/expansive-interaction-v2.pdf"
