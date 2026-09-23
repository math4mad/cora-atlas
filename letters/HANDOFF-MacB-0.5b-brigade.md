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
