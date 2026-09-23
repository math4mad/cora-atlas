# HANDOFF-MacB · 0.5B+170 语料备胎案任务书（B 机 pi 收讫执行）

> 发件：A 机园笔（m1pro-32g）· 2026-09-23 · 奉主人令
> 收件：MacB（m1-16g）上的 pi agents
> 背景：SSH 门闩未通（钥匙挂不上），主人改在 B 机直启 pi —— 本案就地执行。

## 0. 你是谁、在哪

你是 chora 园区机器 B（m1-16g）。先自报体检（全部贴回给主人看一眼即可）：
```bash
hostname; sw_vers -productVersion; sysctl -n hw.memsize   # RAM
df -g / | tail -1                                          # 磁盘 (≥40GB 闸)
python3 -V; which python3; python3 -c "import torch,mlx" 2>&1 | tail -1 || true
python3 -c "import torch; print(torch.__version__, torch.backends.mps.is_available())" 2>&1 | tail -1
ls ~/Programming/code-2026 2>/dev/null || echo "无 code-2026 工作区"
```

## 1. 取仓（若无）

```bash
mkdir -p ~/Programming/code-2026 && cd ~/Programming/code-2026
[ -d chora ] || git clone https://github.com/math4mad/chora.git
[ -d cora-atlas ] || git clone https://github.com/math4mad/cora-atlas.git
cd chora && git pull --ff-only && git log --oneline -3
```
（github 443 若不通，循重试律：快三试→挂账回报主人，勿死磕。）

## 2. 主任务：0.5B × 170 语料 · 真语义群入场（旅制律首验）

依据（读之再动手，皆在仓内）：
- `cora-atlas/iterations/2026-09-23-brigade-corpus-doctrine.md`（中型旅语料律 + C42/C43 + 四句律）
- `chora/experiments/PREREG_PB15_order_tournament.md`（若主人另批海选）
- 弹药：`chora/experiments/exp11-kaggle/matrix_corpus_embed.py`（七域语料内嵌件，b64+sha256 自校验，**先解包落盘**）

最小可跑版（MPS 上 0.5B 完全吃得下）：
1. 环境：`pip install torch transformers peft safetensors modelscope`（或复用既有 venv）；
2. 底座：Qwen2.5-0.5B-Instruct（ModelScope 下载；**sha 记入 manifest**）；
3. 语料：解包 matrix_corpus_embed → 七域 jsonl（sha256 对账，一字不符即停）；
4. 三臂各跑（等总 token）：
   - **S 域序**：七域逐块整训（每域 3 epoch）
   - **R 乱序**：句级全混
   - **B 旅制**：每 batch 七域等比混编，多批轮换
5. 每 epoch 末存 LoRA checkpoint（r=16/α=32/dropout 0.05，targets 七件套，seed 13/14 双跑）；
6. 分析：域间 ΔW 余弦重叠 + 各域 held-out NLL（几何仪在 exp11/matrix_run.py 内可借）；
7. 产物：`artifacts/results/pb16-mac/report_macb.json` + 全部 ckpt sha256 入 manifest
   （**先 pin 后析**，0 字节文件一律作废重跑）。

## 3. 纪律（园律三条，违者返工）

- 判据先冻：跑前把三臂对比的胜负指标写进 PREREG 回帖，跑后只记不改；
- 失败留痕：任何臂崩了，log 与 sha 入匣，不许静默消失；
- 回报最短路径：完工或阻塞，`git push` + 给主人一句话（A 机园笔会从 origin 收账）。

## 4. 若只做一件事

时间/电力不够就只做 **B 臂 ×2 epoch + 存 ckpt**——旅制有无缝（heatmap 阶梯 vs 横纹）
是 C42 的第一口血，其余可补。

—— A 机园笔 手书（此文件在 cora-atlas 仓内，B 机 pull 即得；回帖请开
`chora/experiments/` 下新目录或改本文件加"## B 机回执"段）

## B 机回执（2026-09-23 · MacB pi · **暂停移交**）

奉主人令："一小时完成不了就暂停，未完任务通知 MacA lola。" 实测算式已破一小时闸 → 停。

| 步 | 状态 | 凭据 |
|---|---|---|
| §0 体检 | ✅ 照贴 | macOS **15.8**（简报写 12，差异照登）· 16 GB · 盘余 40 GB（≥40 闸刚踩线）· 默认 python3=3.14.6 无 torch；MEF/Sarcos venv 内 torch 2.14.0 + MPS 可用 |
| §1 取仓 | ✅ | chora `92b9ff0→4d17929`（前三次 fetch early EOF，第四次成）；cora-atlas `a531583→1ca4481` |
| §2.1 环境 | ✅ | `~/venvs/pb16mac`（py3.11.16 · transformers 5.17.0 · peft 0.21.0 · safetensors 0.8.0 · modelscope 1.40.1；torch 经 .pth 借 MEF 之 2.14.0，**MEF 环境零改动**） |
| §2.2 底座 | ✅ | Qwen2.5-0.5B-Instruct（ModelScope 988 MB / 6m53s）八文件重哈希入 `models/manifest.json`（53→61 pin，旧账零改动）—— **先 pin 后动 token** |
| §2.3 语料 | ✅ | 七域内嵌件解包即验 sha **7/7 中**（395 条）；考卷 seed 20260923 切 100 条永不参训（参训 295 条 = 三臂同一多重集，等 token） |
| §3 判据先冻 | ✅ | `chora/experiments/pb16-mac-brigade/PREREG_PB16_MAC_3ARM.md` @ `49ed599`：K1 段能量 CV·E1/E7（阶梯 vs 横纹）·K2 段间 dWov/k90 先入霸权行·K3 各域 held-out NLL·K4 后入三域折扣 + 诚实条款 + 双 seed 功率门 + 主张范围冻结。**PB15 海选未获另批 → 未射** |
| §2.4 三臂 | ⛔ **未跑** | 依 §3.5 试射闸先试 B 臂 seed13 × 1 epoch：40/43 步后崩于 epoch 末 eval；节拍 6.8→28→39.5 s/步单调劣化（16 GB 上 MPS 抢内存进 swap，driver ~9 GB、swap 4.4 GB）|
| §4 最省款 | ⛔ 亦未达 | 172 步 ≈20 分钟本可及，但同一 eval 崩点挡住 → 不再热修，留痕移交 |
| §2.6 分析 | ⏸ | 几何仪已随案入匣（`run_pb16_mac.py`：dWov/k90 段对段，低秩 tr 恒等式免 1.4 GB 稠密），无结果可析 |

**预算算式（暂停之实证理由）**：3 臂 × 2 seed × 4 epoch × 43 步 = **1032 步 ≥1.95 h**（按最好节拍 6.8 s/步）+ 24 次全卷 eval → 破 1 小时闸。副测：CPU naive 4.6 s/步、bf16 5.4、分块 lm_head 7.2（M1 上皆无红利）。电力非因（AC 100%）。

**失败留痕**：`chora/artifacts/results/pb16-mac/{report_macb_BLOCKED.json, run_log_BLOCKED.txt, env.json}`（三件 sha 已入 `artifacts/results/manifest.json`，68→71，纯插入 0 删改）+ `experiments/pb16-mac-brigade/out_smoke/`（traceback 全在案）；移匣在 **`chora@b5a1270`**（号正续一枚 `chora@1a3510a`；判据先冻 = `chora@5a65840`，A daemon rebase 前本地为 49ed599），信件 `chora/letters/2026-09-23-B-lola-pb16mac-paused-handoff.md`。根因：`heldout_nll` 一次物化 whole-vocab fp32 logits（4×120×151936）→ `Placeholder storage has not been allocated on MPS device!`

**r2 复核（暂停后只验仪、未射臂）**：上述 eval 崩点修法**已验**（逐样本 + 沿位置分块 CE：6 条卷 1.7 s、MPS driver 2.81 GB，判据一字未动）；但训练节拍**无红利**（bf16+分块 CE 稳态 6.3 s/步；CPU naive 4.6；分块 lm_head 7.2）⇒ 1032 步 ≈ 1.8 h 仍破 1 小时闸，**暂停判定复核后依旧成立**。另匣 `run_log_r2_check.txt`（pin 68→72）。

**续跑清单（交 lola，代码零改动可跑 CUDA）**：① 落 Kaggle T4（PB16 §4 本就登记 2–3 h Kaggle）`PB16_ARMS=S,R,B PB16_EPOCHS=4`；② 若仍留 B 机：eval 改逐样本+分块 CE（或 logits 转 CPU），`PYTORCH_MPS_HIGH_WATERMARK_RATIO=0.0`，先关其他 MPS 客户，只射 §4 最省款；③ 产物路径不变 `artifacts/results/pb16-mac/report_macb.json`，ckpt 逐 epoch 存盘+sha 入 manifest（律三：权重不入 git）。

*question（不入结论）*：① 任务书标题"170 语料"园内无对账物（在册七域 395 条；另有 172 空间 / 172 题卷）——本案按 §2.3 在册七域执行；② `pb16-mac` 目录名与已占号的 PB16 红蓝案同源，若另立 PB17 号请园笔改。
