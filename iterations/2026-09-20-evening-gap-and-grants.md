# 夜志 · 2026-09-20 傍晚 —— 缝与羊毛

## 一、exp13 主案落槌（真弹丸 exp13-mixscan-11-point-gap-test，7.6min，COMPLETE）
- 11 点混合扫描全曲线在案（report_exp13.json）：
  - ang→M0 单调 0→85.2°，ang→M10 单调 85.2→0°，loss 缓坡 0.87→1.16 —— **无跳变点：H13.1 平滑论胜**；
  - **三角鼓包**：两端角和 85°，中点 122.6° —— 混合权重不在两端张成的测地线平面上，中间态自带 ~19° 新方向（第三结构，非稀释亦非插值）；
  - **边缘大摆幅**：掺 10% 夏即 cos→M0 从 1.0 摔至 0.82；interp_gap 两端鼓包 0.19-0.21、正中 0.003 —— 缝在边缘不在中心；
  - 边界八句 P_summer 全落 0.65-0.88 中位带，无双峰 —— 学过的模型对骑墙语境不极端站队；对照本机 P0（基线嵌入版双峰 0.32-0.96）：双峰是底物属性，非学习属性。
- 附注：探针训练集 acc=1.0（中心化+lstsq 逻辑回归，各向异性地板已被剪）。

## 二、四弹冤案与炮规重申
- 15:14 的 bw/t12/x2/tri "ERROR" 半数是**错号冤案**：新弹标题未归一化到 id slug，夜哨查询打错门。
- 真凶另有其一：mk_all 铸弹时 MOUNT 用了 model_sources 相对名，缺 /kaggle/input/models/ 前缀 → HF 校验炸。侦察弹（atlas-mount-recon，CPU）实测三格位挂载俱在。
- 修复：铸弹机改前缀+id/slug 对齐，四弹重铸（exp13b/exp12 在跑，x2/tri 排队），夜哨真号复岗。
- 家法再钉：**标题归一化=slug，一步不一致，尸检两行泪。**

## 三、44944=试试就试试 → 考卷上架，地理锁拦路
- xdom-calib-pilot（calib 30 组/70 题，严格名匹配判卷）已 push 成任务并自动开考；点将 gemini/qwen3-next-80b 皆撞 `openai.PermissionDeniedError: User location "CN" is not supported`——账号地区锁，与题面无关。$10 日包暂不可用，考卷原地挂账。

## 四、羊毛正版入库（主人双 PDF → artifacts/external 盖 sha）
- Kaggle Research Grant Program：两条目。**Benchmarks Resource Grant** 要件=①Kaggle Benchmarks SDK 实装新颖 benchmark ②开源承诺；回报=免费算力配额+基础设施+Kaggle 工程直连。咱 SDK 任务已上架、开源是家法——**羊要件两条皆中，待核唯申请页资格字段（是否强制机构邮箱）**。
- Kaggle MCP Server：https://www.kaggle.com/mcp（http transport、token auth）——ORCHESTRA 工具层换代候补，夜哨之正统升级路径。
- 顺手补记：MCP 文档侧栏并列 Efficient GPU Usage Tips——若主人再转 PDF，可把「日额/双倍计费」诸悬案一并钉死。

## 五、理论账
- exp13 鼓包现象归入 C 系候选：**"中点不正"定理（草案）**：若 ΔW_混合 落在两端测地线上，角和应恒等于端点角；实测中点外凸 ~37% —— 混合训练生成的适配器含**共同结构提取分量**，为「通用探针 H7 ~0.02」提供几何旁证。

## 补 · 申表正址（主人钦定，18:2x）
- 申请表= https://services.google.com/fb/forms/kaggle-research-grants-application/
- （PDF 里钓出的另一个是 bench 旧表; 以正址为准。园网出境此刻不通, 填表=主人 eyeball 时刻, Lola 只代笔不代点。）

## 补二 · 18:3x 黑白复制 & atlas 真 v2
- **exp13b 回匣(3.0min)**: 黑白道 11 点曲线与春雾道**同构**——端点角 83.3°(春雾 85.2°), 中点角和鼓包 124.9°(春雾 122.6°), p=0.1 摆幅 32°(春雾 35°)。**「中点不正」跨语料对复制成功**: 鼓包是混合训练的几何常数, 不是某一对话题的特化。
- 边界八句 P_white 0.40-0.87: 「正义和忠诚不能同时选」=0.40(判黑), 「卧底穿这身衣服」=0.87(判白)——**立场词判黑、身份词判白**, 缝的语义学有了第一批标本。
- exp12 二死于 peft 野文件名(/tmp/adpack 无 adapter_model.safetensors)→ 引擎 train() 改 save_pretrained 正门, 重铸已射。
- **atlas v2 悬案告破**: metadata 早指向 verify_kernel_v2.py 但该文件从未存在→历次 push 哑火, COMPLETE 皆旧弹。今夜补铸真 v2(raw/centered 双轨 H-A1), 版本 21/22 出膛。
- pocket 三接线: daily-report 尾部/夜哨回匣/夜哨 ERROR——空档静默, 主人贴 webhook 即响。

## 补三 · 19:0x exp12 回匣 + 口袋通电
- exp12 (3.5min): 双不对称翻转成立(序臂偏序 +0.0312/乱臂偏乱 −0.0155)——**方向性保真存在且可翻转**; 序↔乱 adapter 角 7.0° 对跨域 85.3°: 时间是注释(小旋转), 域是骨架(大旋转), 与 v2 宣言对榫。
- 意外对照: 夏语料答案多为单句, 洗牌=恒等 → 两夏臂逐字节相同, NLL/角度全等——「洗牌对照」需先验证语料内部确有句序结构, 此为语料学第一课, 记入方法附录。
- 18:58 飞书 pocket 通电: 首弹「园报进袋第一声」已达; secret 存 ~/.config/pocket (077, 不进 git)。
- 夜哨空转 bug: 网络打盹期 status 空串不匹配任何 case → 静默。已加 ""→跳过 分支并换班(见下条命令)。
