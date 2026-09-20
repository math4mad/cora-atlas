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
