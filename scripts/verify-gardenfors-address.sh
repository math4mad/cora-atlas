#!/usr/bin/env bash
# Letter 032 候验轨道: 每 10 分钟试核 Gärdenfors 收件地址 (铁律: 未验不发)。
# 命中即写 letters/gardenfors/address-verified.txt 并退出; 12 试皆败留痕挂账。
set -u
L="$(dirname "$0")/../letters/gardenfors"; cd "$L"
CAND=(
 "https://portal.research.lu.se/en/persons/peter-gardenfors"
 "https://portal.research.lu.se/sv/persons/peter-gardenfors"
 "https://www.philosophy.lu.se/personal/peter-g%C3%A4rdenfors"
 "https://www.cogsci.lu.se/staff/peterg"
 "https://en.wikipedia.org/wiki/Peter_G%C3%A4rdenfors"
)
for i in $(seq 1 12); do
  for u in "${CAND[@]}"; do
    body=$(curl -s -m 15 -L -A "Mozilla/5.0" "$u" 2>/dev/null) || continue
    mail=$(printf '%s' "$body" | grep -aoE "[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.lu\.se" | sort -u | head -1)
    if [ -n "$mail" ] && printf '%s' "$body" | grep -qi "gardenfors"; then
      { echo "# Letter 032 收件地址验讫 $(date '+%F %T')"; echo "email: $mail"; echo "source: $u"; } > address-verified.txt
      echo "$(date '+%F %T') VERIFIED $mail via $u" >> verify-log.txt; exit 0
    fi
  done
  echo "$(date '+%F %T') 第${i}试未通 (网络或 slug 不对)" >> verify-log.txt; sleep 600
done
echo "$(date '+%F %T') 十二试皆静 — 地址仍候核, 信不发" >> verify-log.txt; exit 1
