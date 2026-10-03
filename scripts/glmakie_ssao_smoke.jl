#!/usr/bin/env julia
# glmakie_ssao_smoke.jl — 「同一道题，两把尺子」之 Julia 侧
#
# 主人 1003 令: 把 **同一道题** (gauss2d 三团云密度地形) 也用 GLMakie 渲一张,
# 与 `scripts/pyvista_ssao_smoke.py` 做**真正的同题两路对照** ——
# 于是 ide-lola 那边 Kaggle 的管线成不成, 都不再挡路。
#
# 与 PyVista 版逐项对齐: 网格 N=30 / 边长 8.0 / 球半径基数 0.20 / 阈值 0.10 /
#   位置=基底坐标  浓淡=密度  色相=哪团云 (每团云自备同色系, 同 v02 勘误)
#   SSAO 同题两渲 (开/关) 好对像素
#
# 用法:  SSAO=1 VER=v01-glmakie julia -t 4 scripts/glmakie_ssao_smoke.jl
const DIR = "/Users/mac/Programming/code-2026/cora-atlas"
const VER = get(ENV, "VER", "v01-glmakie")
const OUT = DIR * "/docs/figs/probes/glmakie-ssao-smoke/" * VER
const SSAO_ON = get(ENV, "SSAO", "1") != "0"
const TRANS = get(ENV, "TRANS", "1") != "0"   # 验: 透明是否吃掉 SSAO

using GLMakie, Colors
using GeometryBasics: Sphere

GLMakie.activate!(ssao = true, px_per_unit = 1)
GLMakie.closeall()

const N = 30                      # 网格 N×N
const EXT = 8.0                   # 公共基底边长
const R0 = 0.20                   # 球半径基数
const THRESH = 0.10               # 密度低于此不铺球
const BG = RGBf(0.055, 0.058, 0.070)

# 三个「概念空间」——同一副基底里的三片云 (mu, sigma, 色, 名)  (与 PyVista 版同参)
const CLOUDS = [
    ((2.7, 2.1), (1.45, 1.00), RGBf(0.97, 0.76, 0.36), "路边摊"),
    ((-2.5, 1.5), (1.10, 1.30), RGBf(0.44, 0.72, 0.95), "超市"),
    ((0.3, -2.7), (1.65, 0.95), RGBf(0.62, 0.90, 0.58), "家里"),
]

gauss2d(x, y, mu, sig) = exp(-(((x - mu[1])^2) / (2 * sig[1]^2) + ((y - mu[2])^2) / (2 * sig[2]^2)))

ssao_cfg = Makie.SSAO(radius = 4.0, blur = 2)
fig = Figure(size = (1600, 1100), backgroundcolor = BG)
ax = LScene(fig[1, 1]; show_axis = false,
            scenekw = SSAO_ON ? (ssao = ssao_cfg,) : NamedTuple())
if SSAO_ON
    ax.scene.ssao.radius[] = 4.0
    ax.scene.ssao.bias[] = 0.006
end

# ── 地板: SSAO 要有遮挡体才看得出接触阴影 ────────────────────────────
mesh!(ax, Rect3f(Point3f(-EXT / 2 - 1, -EXT / 2 - 1, -0.02),
                 Vec3f(EXT + 2, EXT + 2, 0.02));
      color = RGBf(0.11, 0.12, 0.145), ssao = SSAO_ON)

# ── 三团云: 位置=基底坐标 / 浓淡=密度 (逐实例 RGBA) / 色相=哪团云 ──────
const xs = range(-EXT / 2, EXT / 2, length = N)
ntot = 0
for (mu, sig, col, nm) in CLOUDS
    ps = Point3f[]
    sizes = Float32[]
    cols = RGBAf[]
    for x in xs, y in xs
        d = gauss2d(x, y, mu, sig)
        d < THRESH && continue
        push!(ps, Point3f(x, y, 0.30 * d))
        push!(sizes, Float32(2 * R0 * (0.55 + 0.75 * d)))   # 直径 (marker 是单位球径 2)
        push!(cols, RGBAf(col.r, col.g, col.b, Float32(clamp(d, 0.0, 1.0))))
    end
    global ntot
    ntot += length(ps)   # julia 顶层软作用域: 此句 global 必需
    # 坑 (v01 实测): `meshscatter!` **不吃 `ssao` 属性** —— 开/关两渲像素差 0.0%。
    # 逐球改用 `mesh!` (与上述 ssao_probe 同路), SSAO 才真生效。
    for k in eachindex(ps)
        c = TRANS ? cols[k] : RGBf(cols[k].r, cols[k].g, cols[k].b)
        mesh!(ax, Sphere(ps[k], sizes[k] / 2);
              color = c, transparency = TRANS, ssao = SSAO_ON)
    end
    # marker = 单位球 (径 2) → markersize 即直径; 逐实例 alpha 靠 RGBA 向量 + transparency
    # (meshscatter 的逐实例 RGBA 是它的强项, 但 SSAO 失效 → 见上)
    println("  $nm: ", length(ps), " 球")
end

# 相机 (zoom! 会引 GLFW 显示器枚举 segfault → 直接给眼点)
tgt = Vec3f(0, 0, 0)
update_cam!(ax.scene, Vec3f(-9.5, -11.0, 8.6), tgt)


mkpath(OUT)
p = OUT * "/ssao-" * (SSAO_ON ? "on" : "off") * ".png"
save(p, fig)
println("ssao=", SSAO_ON, "  球数=", ntot, "  png_bytes=", filesize(p))
println("=== GLMAKIE-SSAO-SMOKE-DONE ===")
