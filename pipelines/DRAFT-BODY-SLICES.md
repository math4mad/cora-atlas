# 渲染路程 · 「总谱与剖面」Draft Body & Three Cuts

> 可复算 prompt。**v4（2026-10-03）** —— 主人连发两张草图：
> `IMG_2560.HEIC`「总谱」（长条＝Total draft；刀口＝某届「collection players」）；
> `IMG_2561.HEIC`「**长轴与 slice 交汇示意图**」。
> **几何定为：方柱 ＋ 矩形切面（主人 1003 明令「方柱和矩形 slice 不动」）；改动只在「交汇」处 ——
> 长轴（四条棱线 ＋ 中轴）穿切面，****「按三个切片来」：每道切面各一结，打在长轴（中轴）交汇处。**
> 矩形四角**不标结点**——草图上那些红圈是主人**标重点给我看的记号**，不是设计元素（P10）。**
> **v4.1**：切面尺寸定为 **`SLICE_OVER = 1.00`** —— **时间切片的长宽高受外围长方体边界**（主人 1003 令；此前 1.18 会探出体外）。**
>
> ⚠ **勘误**：本文件 v2 曾把草图读成「圆柱＋圆盘」，**系误读，已撤回**。方柱与矩形切面自始未动。
> 本文件即**整条渲染路程的规格**，供对岸（ima-Lola @ ima.copilot）在沙箱内重渲交叉校验。

---

## 0 · 目标物（一句话）

一根**方柱长条＝本体**（NBA 全部选秀 1947–2025）；三道半透明**矩形刀口**＝**1984 / 1996 / 2003** 三届。
**长轴（四条棱线 ＋ 中轴）穿每道切面，交汇处各打一结。** 每道切面上三态并置：

| 态 | 含义 | 出处 |
|---|---|---|
| **金环真像** | 名人，且馆有官方头像 | cdn.nba.com 真图 |
| **虚环灰影** | 名人，而**档案无像** | cdn.nba.com 占位剪影（§1.3） |
| **微灰剪影** | 同届其余球员 | 自绘剪影（**不用真人照片**） |

---

## 1 · 数据（三件，皆可复算）

### 1.1 选秀总表 — `data/nba-draft-history.csv`
- 正源 `stats.nba.com/stats/drafthistory`，**直连被挡**（回 HTML 挡板，非 JSON）。
- 可用路径：`nba_api` 仓的**录制 cassette** `tests/integration/smoke/cassettes/test_endpoints[DraftHistory].yaml`，
  经镜像 `https://ghproxy.net/https://raw.githubusercontent.com/swar/nba_api/master/<path>` 取。
- 结果：**8374 行 / 1947–2025**，列 `PERSON_ID, PLAYER_NAME, SEASON, ROUND_NUMBER, ROUND_PICK, OVERALL_PICK,
  DRAFT_TYPE, TEAM_ID, TEAM_CITY, TEAM_NAME, TEAM_ABBREVIATION, ORGANIZATION, ORGANIZATION_TYPE, PLAYER_PROFILE_FLAG`。

### 1.2 强度（判「最著名」）— `data/nba-raptor-by-player.csv`
- FiveThirtyEight *historical_RAPTOR_by_player*，**CC BY 4.0**，19159 行 / 1977–2022。
- 按 `Σ war_total` 排每届前 12，**再人手补名**：**名人 ≠ WAR**（Len Bias 零出场却最著名；Petrović 同理）。

### 1.3 头像 — `https://cdn.nba.com/headshots/nba/latest/1040x760/{PERSON_ID}.png`
- 真图 1040×760 RGBA。
- ⚠ **无官方头像者返回同一张平灰占位剪影**（HTTP **200**、字节数够，**不是 404**）。
  判据：**不透明像素 R 信道的 pstdev < 12** 即占位。
- 本版实测：36 名人中 **10 无像** —— 1984：Bowie / Perkins / Willis / Robertson / Kersey / Cage / Fleming；
  1996：J. O'Neal / Fisher；2003：Ridnour。
- 替代源全部不通：Wikipedia / commons `000`、basketball-reference `403`、ESPN search API `count=0`、
  `cdn.nba.com/headshots/nba/legends/...` `403`。

---

## 2 · 素材预处理（PIL）

| 产物 | 规格 |
|---|---|
| `tile_{pid}.png` 320×320 | 原图取中心 (520, 250) 的 460 方框 → 圆裁 → **有像**套金环 `#D9B561`；**无像**压暗去色套**虚线石板环** `#7A8292` |
| `sil_{0..2}.png` | 灰剪影三型（头球 + 肩锥），无名者阵列用 |
| `draft-class-faces.csv` | 36 名人 + `has_portrait` 旗 |
| `draft-class-crowd.csv` | 各届 `n_picks / n_famous / n_anonymous / n_famous_with_portrait` |

> **1984 届 228 人 / 10 轮；1996 与 2003 各 58 人 / 2 轮** —— 切面面积本该不同，本版取等截面、以**密度**承载。

---

## 3 · 三维场景（数值即规格）

坐标：**X ＝ 时间**（1947→2025 线性映到 −24 … +24，故 1984→−1.23、1996→+6.15、2003→+10.46）；
**Y ＝ 宽 ±2.40**；**Z ＝ 高 ±3.20**。

| 件 | 规格 |
|---|---|
| **本体（方柱）** | 半透明长条 alpha 0.070，**在每道刀口真断开成四段**，缝半宽 `CUT_GAP = 0.30` |
| **长轴** | **四条棱线**（四角 `(±HI_Y, ±HI_Z)`）＋ **一条中轴** `(0,0)`；**逐段**绘制、到缝即止 |
| **切面（矩形）** | **受外围长方体边界 —— `SLICE_OVER = 1.00`（恰为该截面，不探出）**，金 alpha 0.20 ＋ 亮框（`e = 3.0`） |
| **★ 交汇结点** | 每道切面上打 **5 个「树结」**：**四角**（棱线穿切面处）＋ **中轴心**（中轴穿切面处）。结 = 小球（`r = 0.085`，z 压 0.72）＋ 微环（`major = 1.85r`）。**此即主人草图 IMG_2561 的意** |
| **名人 12** | 3 列 × 4 行，块边长 `TILE = 1.05`，列距 1.18、行距 1.18，整体 z 偏 +0.25；面片**朝相机**（billboard），贴 `tile_{pid}.png` |
| **无名者** | 12 列自下而上填；列距 0.42、行距 0.36，体量 0.30×0.34，灰。→ 1984 满 18 行（216 人）；1996/2003 只 4 行（46 人）＝**密度对比** |
| **相机** | 眼 (49.3, −53.2, 18.6)，看 (4.6, 0, −0.9)，等效 fov ≈ 15°，出图 **2400×1350** |
| **3D 文字** | 每片「`年 · 人数 picks`」＋「`n/12 portraits`」；标题「`TOTAL DRAFT 1947 - 2025`」；皆 billboard 朝相机 |

**文字摆位必须走屏幕方向**：`sup = normalize(cross(v, ẑ) × v)`，`v = normalize(target − eye)`，
标签位 = 切面中心 ± `sup × d`，且 `d` 要乘 `dist_to_slice / R` 补偿透视 —— **直接用世界 Z 偏移会错位**。

---

## 4 · 合成（PIL 页脚带）

底版 2400×1350 **另加** 290px 页脚带（**不压正文**）：

1. 标题行　2. 图例三项（金环 / 虚环 / 灰剪影）　3. 三行数据脚注（数据源、同形不同物、有像率梯度）

中文须显式指定字体（`PingFang.ttc` 在部分 macOS 已缺；可用 `Hiragino Sans GB.ttc` / `Songti.ttc`）。

---

## 5 · 判据（先冻后用，铁律 5）

| # | 判据 |
|---|---|
| **D1** | 三片的「有像率」须读出 **5/12 · 10/12 · 11/12**（随年代单调） |
| **D2** | 三片的无名者行数肉眼可分：1984 满片、其余约四分之一 |
| **D3** | 长轴（四条棱线 ＋ 中轴）穿每道切面；**「按三个切片来」＝ 每片 1 结，打在长轴（中轴）交汇处，共 3 结**；**矩形四角不标结点**；切面仍矩形、本体仍方柱 |
| **D4** | 三态符号在 1:1 下可辨（金环 / 虚环 / 灰剪影） |

---

## 6 · 坑（已付代价，勿重蹈）

- **P1** cdn.nba.com 无像者回 **200 + 占位图** → 不验内容就会把灰剪影当真头像渲进去（本版 10/36 中招过一次）。
- **P2** 本机 `urllib` 出不去 → 取件走 `curl`。
- **P3** `stats.nba.com` / `wikipedia` / `basketball-reference` 直连皆挡；GitHub raw 走 `ghproxy.net`。
- **P4** Blender 文字 billboard 要用「**指向相机**」的法向，否则文字镜像。
- **P5** Blender 复制对象**继承 `hide_render`** → 阵列必须显式置 `False`。
- **P6** 斜视下相邻切面会因透视互叠（1996↔2003 相距仅 4.31 时间单位）；相机方位角取 **~50°** 可分离。
- **P7** 页脚压在图内必然撞标签 → **另加页脚带**，不改底版尺寸。
- **P8** 用 wireframe cube 画本体棱框时，长棱线会**贯穿切面**并与之纠缠 → 长轴必须**逐段**绘制（每段到刀口缝即止），交汇处**另打结**标明。
- **P9** ⚠ **别把「交汇示意图」读成「改截面形状」**。主人 `IMG_2561` 只讲**长轴如何与 slice 交汇**，
  **方柱与矩形切面不动**。此处本轮误读过一次（改成圆柱＋圆盘），已撤回。
- **P10** ⚠ **草图上的强调记号 ≠ 设计元素**。主人在矩形顶点画的那些红圈，是**标重点给我看**的；
  照搬进图即为错（本轮又踩一次）。判据：**主人草图上多画的任何装饰，先问是「设计」还是「指给我看」**。

---

## 7 · 交接（对岸 ima-Lola）

请在 ima.copilot 沙箱内按本路程**重渲一版**，用于交叉校验：

- **若沙箱有 Blender**：照 §3–4 数值直接渲，出 2400×1350 底版 ＋ 2400×1640 成图。
- **若无 Blender**：用 **Makie（GLMakie + SSAO）** 或 matplotlib 3D 复现 §3 几何。
  贴图关键：`Mesh(verts, faces; uv = uvs)` ＋ `mesh!(ax, m; color = <图矩阵>)`；
  半透明：`transparency = true` ＋ `RGBA`；SSAO：`GLMakie.activate!(ssao = true)` ＋ `Makie.SSAO(radius, blur)`。
  **回报里须注明偏离项**。
- **回报格式**：① 出图或失败点 ② D1–D4 各判据的**观测值** ③ 与本版的差异清单。
- **契约**：**不推仓、不改冻尺、不动账本**；只渲图 ＋ 回报。改动性动作走 rank 闸。

---

*本地 lola（园笔）· 2026-10-03 · 实现件 `scripts/{fetch_nba_headshots,prep_draft_slice_assets,blender_draft_body_slices,compose_draft_body_slices}.*`*
