#!/usr/bin/env python3
# scripts/ledger-normalize.py — 总账归化: LEDGER.md → site/LEDGER.qmd
#
# 园律两条在此交汇:
#   ① 对话与论文必保 (主人 0923 夜裁定) —— 账行须同源上站, 不许只躺在盘上;
#   ② pandoc 竖线行须成"真表" (带 |---| 分隔线) 且独立成块 —— 总账里大量
#      "孤行账行" (| 号 | 事 | 记 |, 无表头无分隔) 硬搬上站会被吐成一段裸竖线
#      (2026-09-23 修表案病灶, 主人报 PB15 part6)。
#
# 归化规则 (逐行, 绝不合并、绝不改任何人写好的真表):
#   · 竖线行且 ±2 行内出现 |---| 分隔线 → 真表之一部, 原样留;
#   · 其余竖线行 (孤行账行) → 凿刻体列表项 "- **号** ｜ 事 ｜ 记";
#   · 真表若紧贴正文, 前后自动补一空行。
import pathlib
import sys

SRC = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else "LEDGER.md")
DST = pathlib.Path(sys.argv[2] if len(sys.argv) > 2 else "site/LEDGER.qmd")


def is_row(l):
    return l.startswith("|")


def is_sep(l):
    return is_row(l) and "-" in l and set(l) <= set("|-: ")


def cells(l):
    return [c.strip() for c in l.strip().strip("|").split("|")]


def main():
    src = [l.rstrip() for l in SRC.read_text(encoding="utf-8").split("\n")]
    n = len(src)

    def in_table(i):
        return any(is_sep(src[j]) for j in range(max(0, i - 2), min(n, i + 3)))

    out, conv, kept = [], 0, 0
    for i, line in enumerate(src):
        if is_row(line) and in_table(i):
            if out and out[-1].strip() and not is_row(out[-1]) and not in_table(i - 1):
                out.append("")
            out.append(line)
            kept += 1
            continue
        if is_row(line):
            cs = cells(line)
            head, rest = cs[0], " ｜ ".join(c for c in cs[1:] if c)
            out.append(f"- **{head}** ｜ {rest}" if rest else f"- **{head}**")
            conv += 1
            continue
        out.append(line)
    DST.parent.mkdir(parents=True, exist_ok=True)
    DST.write_text("\n".join(out).rstrip() + "\n", encoding="utf-8")
    print(f"台账归化: {SRC} → {DST} · 真表行 {kept} 原样 · 孤行账行 {conv} 转凿刻体")


if __name__ == "__main__":
    main()
