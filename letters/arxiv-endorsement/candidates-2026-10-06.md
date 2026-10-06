# arXiv cs.LG 担保（endorsement）· 候选推荐人单 · 2026-10-06

> 事由：`unified-agents`（《A Unified Framework for Agents: Curves, Bases, and Manifolds》）首发 arXiv
> 需 **cs.LG 担保人**。09-22 已向 **Jingang Zhou（中科院自动化所，CAMFT）** 发担保请求（F8DHIQ 转发件），
> **静默两周无回音** → 主人 1006 命「再找一下推荐人」。
> 数据源：arXiv API 实时拉取（2026-10-06），排序=提交日期降序。**邮箱须自论文 PDF 首页/主页取，本单标「待取」。**

## 〇 · 机制备忘（一句话）
新账号首次投 cs.LG，需一位**在 cs.LG 发过文**的现作者点一次头（邮件点确认即可，不使其成为作者）。
→ 所以候选 = **近 30–60 天在 cs.LG 发过相关方向、且回复率高**的人（一作学生 > 资深，中文 > 英文）。

---

## 一 · 已在册（含邮箱，可直接用）

| 优先 | 人 | 单位 | 代表作 | 邮箱 | 状态 |
|---|---|---|---|---|---|
| ★1 | **Jingang Zhou** | 中科院自动化所 CASIA | CAMFT (2609.22253)；**新作 2609.39405** | `zhoujingang2025@ia.ac.cn` | **09-22 已发，静默 2 周** |
| ★2 | **Luca Zhou** | Sapienza 罗马大学 | On Emergent Capabilities and Model Merging (2609.24504) | `luca.zhou@uniroma1.it` | 备胎，未发 |
| ★3 | **Divya Appapogu** | Boston University | — | `divsp@bu.edu` | 备胎，未发 |
| ★4 | **Aaryan Sharma** | U. Twente | merging surgery (2608.28547) | `aaryan.sharma@utwente.nl` | 备胎，未发 |

> 注：★1 至今未回，但其 **09-30 又发新文**（2609.39405，task vector composability）——证明人在活跃。
> 可**再发一封极短 nudge**（或换人），二者择一，候主人裁。

## 二 · 新增候选（2026-10-06 arXiv 实时；邮箱待取）

按「主题贴合 × 回复概率」粗排；**☎︎=邮箱待取（PDF 首页 corresponding / 主页）**：

| # | 人（一作 · 通讯/资深） | 单位线索 | 论文（arXiv） | 贴合点 |
|---|---|---|---|---|
| N1 | **Zijing Wang** 等（Hinrich Schütze 组?） | LMU 慕尼黑 | Orthogonal Yet Coupled: Decoupling Geometric Components for Model Merging（**2609.37564**） | **正交几何分量**——与园「逐槽正交/施密特」直亲 |
| N2 | **Hang Yin**（通讯 **Junchi Yan**） | 上海交大 | ChainLoRA: Geometry-Preserving Task Vector Merging for Continual Learning（**2610.00431**） | 几何保持 + 任务向量合并；中文 |
| N3 | **Yan Li** 等 | 中科院深圳/鹏城线索 | CASS: Contribution-Aware Structured Sparsity for Model Merging（**2609.34184**，NeurIPS 2026） | 结构化稀疏合并；中文 |
| N4 | **Yixuan Liu / Yuhao Sun / Sen Song / Jin Li** | 清华（Sen Song） | When the Merge Coefficient Stops Mattering（**2609.32332**） | 合并系数失效点 = 时序临界，极合 |
| N5 | **Wenzhi Fang** 等 | — | Reasoning-Preserving FT with **Null-Basis LoRA**（**2609.25618**） | **零基 LoRA**——子空间近亲 |
| N6 | **Zhengbao He** 等 | 上海交大线索 | Compress then Merge: Multiple LoRAs → One Low-Rank Adapter（**2606.03723**） | 多个 LoRA 压成一个 = 合并非拼接 |
| N7 | **Zhengxuan Wei** 等 | — | SSR-Merge: **Subspace Signal Routing** for Training-Free LoRA Merging（**2606.10617**） | 子空间信号路由 |
| N8 | **Carlos Garrido-Munoz / Jorge Calvo-Zaragoza** | 西班牙 Granada | Handwritten Text Recognition Lives in the **High-Pixel Variance Subspace**（**2609.35473**） | 「能力住子空间」的另一域活证 |
| N9 | — | — | Beyond Uniform Subspaces: **Spectrum-Aware** & Depth-Adaptive Fusion（**2609.24612**） | 谱感知合并（与 P-B18 谱带同轴） |

备选池（同题，供扩招）：2609.33437 SMAT · 2609.34184 CASS · 2608.17366 CORAM（正交旋转）· 2608.27518 Muon×谱 · 2608.25354 高维稀疏解耦 · 2609.22886 Merge++。

## 三 · 取邮箱的路子（下一步可代跑）
1. arXiv **PDF 首页**：对应作者邮箱常印在首页脚注（`export.arxiv.org/pdf/<id>` → 取首段文本）。
2. 作者**主页/GitHub**（论文 comment 里的项目页常带邮箱）。
3. 已有线索：N2 通讯 Junchi Yan（上交，公开邮箱可查）；N4 Sen Song（清华，公开）。

## 四 · 请求信模板（中文版，一作学生用）

> 尊敬的 [姓名] 老师/同学：
>
> 冒昧打扰。我是 arXiv 首次投稿者，想恳请您为我担保 **cs.LG** 分类——转发件内是我的
> unique code，点链接确认即可，**担保不会使您成为本文作者**。
>
> 我的论文《A Unified Framework for Agents: Curves, Bases, and Manifolds》提出一个
> 智能体的统一几何–概率框架，核心是把参数更新看作曲线/子空间上的演化，其中「同基座
> LoRA 线性 merge 的超加性与『合非拼接』鼓包」一节，与您的 [论文简称] 直接相关，正文已引用。
>
> 若不便，也请告知，绝不纠缠。谢谢！
> Luanr Cheung (Yiwei Zhang) — The Cora Project
> https://math4mad.github.io/cora-atlas/

English version available in `request-email-en.md` (同目录).

## 五 · 候主人裁
1. **扩招几位**（从 N1–N9 圈选，我取邮箱后出信）。
2. **N1 是否先发**（Jingang Zhou 已静默两周，是否 nudge/换 ★2 Luca Zhou）。
3. 担保落定后即走提交五步（包已在 `unified-agents-arxiv.tar.gz`）。
