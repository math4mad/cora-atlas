#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
法医学面板 v1 · 六现场地毯图 + 双显微镜 + 心跳谱 + 三定律
v1 变更 (2026-09-22, owner 钦点): agent 提交记录在主毯上压缩厉害 →
  显微镜A: 稀疏窗 08-24~09-03 (M4MADS 7发/假名 5发/calculus-note 1发) 逐发展开;
  显微镜B: 园笔密毯 09-19~09-22 三日数百发, 半透明逐辨密度。
数据: docs/figs/forensics-data.json (GitHub API 现场取证, 与 C38 账面对账一致:
  人@lock5 中位Δ=1553分/真空34天, M4MADS@lock5 21分, 人@Stat2-julia 3206分/真空72天,
  Stat2-With-Py 16分, 假名案五发署名 math4mad)。
用法: python3 scripts/fig_forensics.py  → 覆写 docs/figs/fig-forensics.png
"""
import json, datetime as dt, statistics as st
from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.patches import Rectangle

plt.rcParams["font.family"] = ["PingFang SC", "Heiti SC", "Arial Unicode MS"]
plt.rcParams["axes.unicode_minus"] = False

ROOT = Path(__file__).resolve().parent.parent
DATA = json.loads((ROOT / "docs/figs/forensics-data.json").read_text())
P = {k: sorted(dt.datetime.fromisoformat(s).replace(tzinfo=None) for s in v)
     for k, v in DATA.items()}

HUMAN, AGENT = "#D08B55", "#2E8FA3"
D = mdates.date2num

ROWS = [
    ("math4mad @ lock5-stat",        P["human_lock5"],      HUMAN),
    ("M4MADS @ lock5-stat",          P["agent_lock5"],      AGENT),
    ("math4mad @ Stat2-julia",       P["human_julia"],      HUMAN),
    ("※假名: agent @ Stat2-With-Py", P["agent_withpy"],     AGENT),
    ("※ agent @ calculus-note",      P["agent_calcnote"],   AGENT),
    ("园笔: agent @ chora",          P["agent_chora"],      AGENT),
    ("园笔: agent @ cora-atlas",     P["agent_coraatlas"],  AGENT),
]

def gaps_min(ts):
    return [(b - a).total_seconds() / 60 for a, b in zip(ts, ts[1:])]

def max_band(ts):
    if len(ts) < 2: return None
    return max(((b - a, a, b) for a, b in zip(ts, ts[1:])), key=lambda g: g[0])

fig = plt.figure(figsize=(17, 11), dpi=110)
gs = fig.add_gridspec(2, 3, height_ratios=[1.15, 1],
                      width_ratios=[2.6, 1.35, 0.8],
                      hspace=0.55, wspace=0.28,
                      left=0.155, right=0.985, top=0.93, bottom=0.07)

# ════════════════ 主毯 ════════════════
ax = fig.add_subplot(gs[0, :2])
ax.set_title("代码法医学面板 v1 · 六现场地毯图 (rug plot; 每竖线=1 commit, //带=最大睡眠真空; 虚线框=显微镜取景)",
             fontsize=14.5, pad=12)
for y, (label, ts, color) in enumerate(ROWS):
    if ts:
        ax.eventplot([ts], lineoffsets=[y], linelengths=0.55,
                     linewidths=1.6, colors=[color])
    band = max_band(ts)
    if band and band[0].days >= 30:
        _, a, b = band
        ax.add_patch(Rectangle((D(a), y - 0.42), D(b) - D(a), 0.84,
                               facecolor=color, alpha=0.15,
                               hatch="//" if y % 2 == 0 else "\\\\",
                               edgecolor=color, linewidth=0, zorder=0))
        ax.text(D(a), y + 0.5, f"真空{band[0].days}天", fontsize=10, color=color, va="bottom")
    if len(ts) >= 2:
        med = st.median(gaps_min(ts))
        ax.text(D(max(ts)) + 6, y,
                f"中位Δ={med:.0f}分" + (f" · n={len(ts)}" if len(ts) > 30 else ""),
                fontsize=10.5, color=color, va="center")
ax.set_yticks(range(len(ROWS)), [r[0] for r in ROWS], fontsize=12)
ax.set_ylim(len(ROWS) - 0.4, -0.8)
ax.set_xlim(dt.datetime(2023, 7, 1), dt.datetime(2027, 6, 1))
ax.xaxis.set_major_locator(mdates.MonthLocator(bymonth=[1, 7]))
ax.xaxis.set_major_formatter(mdates.DateFormatter("%Y-%m"))
ax.tick_params(axis="x", labelsize=11.5)
for s in ("top", "right", "left"): ax.spines[s].set_visible(False)
ax.axvline(dt.datetime(2024, 4, 15), color="gray", ls=":", lw=1)
ax.text(dt.datetime(2023, 8, 1), -0.78, "2023 人写现场", fontsize=11, color="#999")
ax.text(dt.datetime(2026, 3, 1), -0.78, "2026 agent 现场", fontsize=11, color="#999")

ZA0, ZA1 = dt.datetime(2026, 8, 24), dt.datetime(2026, 9, 3)      # 取景框 A: 稀疏窗
ZB0, ZB1 = dt.datetime(2026, 9, 19), dt.datetime(2026, 9, 22, 12) # 取景框 B: 园笔密毯
ax.add_patch(Rectangle((D(ZA0), 0.6), D(ZA1) - D(ZA0), 3.8,
                       fill=False, edgecolor=AGENT, lw=1.3, ls="--"))
ax.add_patch(Rectangle((D(ZB0), 4.6), D(ZB1) - D(ZB0), 1.8,
                       fill=False, edgecolor=AGENT, lw=1.3, ls="--"))
ax.text(D(ZA0), 4.55, "A", fontsize=12, color=AGENT, ha="left", va="top", weight=600)
ax.text(D(ZB0), 6.45, "B", fontsize=12, color=AGENT, ha="left", va="bottom", weight=600)

# ════════════════ 显微镜 A: 稀疏窗逐发 ════════════════
axA = fig.add_subplot(gs[1, 0])
axA.set_title(f"显微镜A · 稀疏窗逐发展开 {ZA0:%m-%d}~{ZA1:%m-%d}  (主毯框A)\n"
              "M4MADS 7发 / 假名 5发 / calculus-note 1发 — 假名五发时刻逐标, 两小时连班",
              fontsize=11, loc="left")
A_ROWS = [ROWS[1], ROWS[3], ROWS[4]]
for y, (label, ts, color) in enumerate(A_ROWS):
    vis = [t for t in ts if ZA0 <= t <= ZA1]
    axA.eventplot([vis], lineoffsets=[y], linelengths=0.6, linewidths=2.4, colors=[color])
axA.set_yticks(range(len(A_ROWS)), [r[0] for r in A_ROWS], fontsize=10.5)
axA.set_ylim(len(A_ROWS) - 0.4, -0.9)
axA.set_xlim(ZA0, ZA1)
axA.xaxis.set_major_locator(mdates.DayLocator())
axA.xaxis.set_major_formatter(mdates.DateFormatter("%m-%d"))
axA.xaxis.set_minor_locator(mdates.HourLocator(byhour=[12]))
axA.tick_params(axis="x", labelsize=9.5)
for s in ("top", "right"): axA.spines[s].set_visible(False)
shown = []
for t in P["agent_withpy"]:
    if shown and (t - shown[-1][0]).total_seconds() < 900:
        shown[-1][1].append(t); continue
    shown.append([t, [t]])
lines = [f"假名五发时刻 (08-29 UTC):"]
for t, grp in shown:
    lines.append(f"  {t:%H:%M}" + (f"~{grp[-1]:%H:%M} ({len(grp)}发)" if len(grp) > 1 else " (1发)"))
axA.text(0.015, 0.97, "\n".join(lines), transform=axA.transAxes, fontsize=9.5,
         color=AGENT, va="top", linespacing=1.5,
         bbox=dict(fc="white", ec=AGENT, lw=0.7, alpha=0.9))
for t, grp in shown:
    axA.plot([D(t), D(grp[-1])], [1.28, 1.28], color=AGENT, lw=1.2)

# ════════════════ 显微镜 B: 园笔密毯 ════════════════
axB = fig.add_subplot(gs[1, 1])
axB.set_title(f"显微镜B · 园笔密毯 {ZB0:%m-%d}~{ZB1:%m-%d}  (主毯框B)\n"
              f"chora {len(P['agent_chora'])}发 / cora-atlas {len(P['agent_coraatlas'])}发;\n"
              "主毯压成一竖, 此窗再放大千倍仍只见色柱 — 发密无隙即铁证",
              fontsize=11, loc="left")
B_ROWS = [ROWS[5], ROWS[6]]
for y, (label, ts, color) in enumerate(B_ROWS):
    vis = [t for t in ts if ZB0 <= t <= ZB1]
    axB.eventplot([vis], lineoffsets=[y], linelengths=0.6,
                  linewidths=1.4, colors=[color], alpha=0.35)
axB.set_yticks(range(len(B_ROWS)), ["chora", "cora-atlas"], fontsize=10.5)
axB.set_ylim(len(B_ROWS) - 0.4, -0.6)
axB.set_xlim(ZB0, ZB1)
axB.xaxis.set_major_locator(mdates.HourLocator(byhour=[12]))
axB.xaxis.set_major_formatter(mdates.DateFormatter("%m-%d\n12:00"))
axB.tick_params(axis="x", labelsize=9.5)
for s in ("top", "right"): axB.spines[s].set_visible(False)

# ════════════════ 心跳谱 + 三定律 (右列) ════════════════
gsR = gs[:, 2].get_position(fig)
axH = fig.add_axes([gsR.x0, gsR.y0 + 0.36, gsR.width * 0.98, gsR.height - 0.36])
axH.set_title("心跳谱: 不认名字\n只认节奏 (60:1)", fontsize=11.5)
human_g = gaps_min(P["human_lock5"]) + gaps_min(P["human_julia"])
agent_g = (gaps_min(P["agent_lock5"]) + gaps_min(P["agent_withpy"])
           + gaps_min(P["agent_chora"]) + gaps_min(P["agent_coraatlas"]))
bins = np.logspace(np.log10(0.5), np.log10(4e5), 26)
axH.hist([human_g, agent_g], bins=bins, density=True, histtype="stepfilled",
         alpha=0.75, color=[HUMAN, AGENT],
         label=[f"人 n={len(human_g)} 中位{st.median(human_g):.0f}分",
                f"agent n={len(agent_g)} 中位{st.median(agent_g):.0f}分"])
axH.set_xscale("log"); axH.set_yscale("log")
axH.set_xlabel("相邻 commit 间隔 (分钟, log)", fontsize=10)
axH.set_ylabel("密度 (log)", fontsize=10)
axH.tick_params(labelsize=9)
axH.legend(fontsize=9, loc="upper right")

axL = fig.add_axes([gsR.x0, 0.065, gsR.width, 0.245])
axL.axis("off")
axL.text(0, 1.0,
 "三定律 (候封 C38)\n"
 "① 心跳定律: 中位数验物种\nagent≈21分 vs 人≈1553分 (60:1)\n"
 "② 尾巴定律: 人=幂律长尾, agent=短棒\n"
 "③ 睡眠定律: 时区里 8 小时真空=防伪水印\n骗局与诚实同价\n"
 "※ 假名案 Stat2-With-Py: 五发署名 math4mad\n节奏全是 agent — 名字可借, 心跳不可借",
 fontsize=8.4, va="top", linespacing=1.5)
out = ROOT / "docs/figs/fig-forensics.png"
fig.savefig(out)
print("saved:", out)
