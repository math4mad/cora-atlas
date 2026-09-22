#!/usr/bin/env bash
# Letter 032 候验轨道 (单趟版): 每次调用巡一轮五路 slug; 节律由 bin/queue.py 管 (指数退避)。
# 命中即写 letters/gardenfors/address-verified.txt 并退 0 (队列记 ☑)。铁律: 未验不发。
set -u
L="$(dirname "$0")/../letters/gardenfors"; cd "$L"
CAND=(
 "https://portal.research.lu.se/en/persons/peter-gardenfors"
 "https://portal.research.lu.se/sv/persons/peter-gardenfors"
 "https://www.philosophy.lu.se/personal/peter-g%C3%A4rdenfors"
 "https://www.cogsci.lu.se/staff/peterg"
 "https://en.wikipedia.org/wiki/Peter_G%C3%A4rdenfors"
)
  for u in "${CAND[@]}"; do
    body=$(curl -s -m 15 -L -A "Mozilla/5.0" "$u" 2>/dev/null) || continue
    mail=$(printf '%s' "$body" | grep -aoE "[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.lu\.se" | sort -u | head -1)
    if [ -n "$mail" ] && printf '%s' "$body" | grep -qi "gardenfors"; then
      { echo "# Letter 032 收件地址验讫 $(date '+%F %T')"; echo "email: $mail"; echo "source: $u"; } > address-verified.txt
      echo "$(date '+%F %T') VERIFIED $mail via $u" >> verify-log.txt; exit 0
    fi
  done
  echo "$(date '+%F %T') 本轮未通 (网络或 slug 不对)" >> verify-log.txt
echo "$(date '+%F %T') 本轮未中 — 地址仍候核, 信不发" >> verify-log.txt; exit 1
