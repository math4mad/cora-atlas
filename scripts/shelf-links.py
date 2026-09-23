#!/usr/bin/env python3
# 同架推荐 v1 (主人 E10 一针所生): 给 GLOSSARY/LEDGER 表行注入"上一架/下一架"串门条
# 设计律: 检索接口必须暴露邻域结构 (neighbors-as-API) —— 逛架内行化。
import re, sys

def shelf(path):
    try:
        html = open(path, encoding="utf-8").read()
    except FileNotFoundError:
        print("跳过(无页):", path); return 0
    pat = re.compile(r"<tr[^>]*>.*?</tr>", re.S)
    rows = pat.findall(html)
    body = [r for r in rows if "<td" in r]
    if len(body) < 3:
        print("跳过(行不足):", path); return 0
    def label(r):
        t = re.sub(r"<[^>]+>", " ", r)
        t = re.sub(r"\s+", " ", t).strip()
        return t[:24] + ("…" if len(t) > 24 else "")
    n = len(body)
    newrows = {}
    for i, r in enumerate(body):
        rid = re.sub(r"<tr", f'<tr id="sr{i}"', r, count=1) if "id=" not in r else r
        prev = f'<a href="#sr{i-1}" title="{label(body[i-1])}">⬆ 上一架</a>' if i > 0 else "▲ 架首"
        nxt = f'<a href="#sr{i+1}" title="{label(body[i+1])}">下一架 ⬇</a>' if i < n-1 else "▼ 架尾"
        newrows[r] = rid + f'<div class="shelfbar">{prev} · 同架串门 · {nxt}</div>'
    cnt = 0
    def sub(m):
        nonlocal cnt
        g = m.group(0)
        if g in newrows:
            cnt += 1
            return newrows[g]
        return g
    html2 = pat.sub(sub, html)
    css = ("<style>.shelfbar{font-size:.78em;color:#8a7a5f;text-align:right;"
           "padding:.1rem .4rem;border-bottom:1px dashed #e5dcc8}"
           ".shelfbar a{color:#b05f24;text-decoration:none}</style>")
    html2 = html2.replace("</head>", css, 1)
    open(path, "w", encoding="utf-8").write(html2)
    print(f"同架条注入: {path} ({cnt} 行)")
    return cnt

if __name__ == "__main__":
    target = sys.argv[1:] or ["docs/GLOSSARY.html", "docs/LEDGER.html"]
    tot = sum(shelf(t) for t in target)
    sys.exit(0 if tot else 1)
