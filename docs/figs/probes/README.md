# 探针 · 同一道题的「两把尺子」

> **缘起（主人 2026-10-03）**：ide-lola 在试 Kaggle `juliacall` + GPU 的 GLMakie 管线。
> 主人点破 **「Python 自己也有 SSAO，PyVista」**，并令：**先做 pyvista 冒烟测试**，
> 再把**同一道题**用 GLMakie 也渲一张 —— 于是 Kaggle 那条成不成，都不再挡路。

**题目（两路同参，逐球对齐）**：`gauss2d` 三团云密度地形 —— 二维网格铺小球，
`位置＝公共基底坐标 · 浓淡＝密度 · 色相＝哪团云`，各 **729 球**。
这道题与将来那张「塑胶凳 / 肠粉-蒸饭-烧烤摊 **密度图**」同构。

---

## 裁定 ⚖️：这张图走 **PyVista**

| 能力（GLMakie 当初被选中的理由） | PyVista 0.49 / VTK 9.7.1 | GLMakie 0.13.15 |
|---|---|---|
| **逐球 / 逐格 RGBA 浓淡**（密度→透明度） | ✅ `scalars` + `opacity="linear"` | ⚠️ `meshscatter` 有，**但见下** |
| **SSAO** | ✅ 同题两渲差 **26.6%**（均值 7.4） | ⚠️ 不透明才生效：差 **8.9%**（均值 2.6） |
| **两者兼得** | ✅ **兼得**（本目录对照图左列即是） | ❌ **互斥** |
| 无头离屏（macOS，无 X11） | ✅ `OFF_SCREEN` + `screenshot()` | ✅ `save()`（GLFW 要 GUI 会话） |
| 交互 | 有（`Plotter.show`） | 有（原生 GLFW 窗口） |

### 根因（实测三步定位）

| 变量 | SSAO 效果 | 判 |
|---|---|---|
| `meshscatter!` ＋ 透明 | 变动 **0.0%** | ✘ SSAO 被忽略 |
| `mesh!` ＋ **透明** | 变动 **0.0%** | ✘ |
| `mesh!` ＋ **不透明** | 变动 **8.9%**（最大 110） | ✅ |

1. **`meshscatter!` 不吃 `ssao` 属性**（0.13.15）—— 换逐球 `mesh!` 才有；
2. **`transparency = true` 会静默吃掉 SSAO** —— SSAO 走不透明深度通道，透明物被排除，
   **不报错、不警告**，只是效果为零。

**故「逐实例 RGBA 透明 ＋ SSAO」在 GLMakie 0.13.15 里互斥** ——
而这恰是当初选 GLMakie 的那条理由。**PyVista 两件同时做到**，故这张图改走 PyVista。

> 注：GLMakie 仍可用于**不透明**的三维图（如「总谱与剖面」那种实心切片／贴图），
> 那条轨未被否掉；被否掉的只是「**半透明 ＋ SSAO**」这一类。

---

## 目录

```
pyvista-ssao-smoke/
  README.md                      ← PyVista 侧三问三答 + v01→v02 勘误（色带接管色相）
  v01-pyvista/                   ← 初版（三团云色相全丢，勘误照存）
  v02-pyvista-cmap/    ✅ 本轮正本（每团云自备同色系色带）
glmakie-ssao-smoke/
  v01-glmakie/                   ← meshscatter：SSAO 静默失效
  v02-glmakie-mesh/               ← 换逐球 mesh!：仍失效（透明之过）
  v03-glmakie-opaque/  ← 不透明：SSAO 才生效（用于对照）
same-problem-two-rails.png       ← 对照总图
```

**跑法**

```bash
# Python 侧
python3 -m venv .venv && ./.venv/bin/python -m pip install pyvista
VER=v03-xxx ./.venv/bin/python scripts/pyvista_ssao_smoke.py

# Julia 侧
SSAO=1 TRANS=1 VER=v04-xxx julia -t 4 scripts/glmakie_ssao_smoke.jl
```

图：lola · cora-atlas
