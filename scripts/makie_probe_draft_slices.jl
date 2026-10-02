#!/usr/bin/env julia
# makie_probe_draft_slices.jl — 「总谱与剖面」Makie 轨 判据探针 (先冻后用, 铁律 5)
#   P1 3D 半透明切片能否正确 z-sort?   (预期: 否 —— CairoMakie 无 z-clipping)
#   P2 scatter(marker=PNG头像) 能否贴到 3D 切片上?
#   P3 出 SVG/PDF?
#   P4 3D 投影下 image marker 是否变形?
#
# 用法: julia -t 4 scripts/makie_probe_draft_slices.jl
const DIR = "/Users/mac/Programming/code-2026/cora-atlas"
const OUT = DIR * "/docs/figs"
using CairoMakie, FileIO

CairoMakie.activate!(px_per_unit = 2.0)

faces = ["2544", "893", "977"]   # LeBron / Jordan / Kobe
imgs = [rotr90(FileIO.load(DIR * "/data/headshots/" * f * ".png")) for f in faces]

GOLD = RGBf(0.85, 0.71, 0.38)
GRAY = RGBf(0.42, 0.43, 0.46)

fig = Figure(size = (1500, 620), backgroundcolor = RGBf(0.02, 0.02, 0.028))
Label(fig[0, 1:3], "Makie probe: draft slices (P1-P4)", color = GOLD, fontsize = 20)

# ── P1 / P2 / P4: Axis3 内三片半透明切片 + 头像 marker ───────────────
ax = Axis3(fig[1, 1], aspect = (2, 1, 1),
           xlabel = "time", ylabel = "pick", zlabel = "class",
           backgroundcolor = RGBf(0.05, 0.05, 0.06))
xs = [-1.0, 0.0, 1.0]
for (k, x) in enumerate(xs)
    # 两面半透明切片 (yz 平面): 用 surface 画方形薄片
    ys = range(-1, 1, length = 2); zs = range(-1, 1, length = 2)
    surface!(ax, fill(x, 2, 2), [y for _ in ys, y in ys], [z for z in zs, _ in zs],
             color = fill(GOLD, 2, 2), alpha = 0.30, shading = false)
end
# 头像 marker 贴在 3D 切片上 (P2: 能否贴? P4: 是否变形?)
for (k, x) in enumerate(xs)
    n = 4
    for i in 1:n
        scatter!(ax, [Point3f(x, -0.75 + 0.5 * i, 0.0)],
                 marker = imgs[k], markersize = 0.55, color = (:white, 1.0))
    end
end
hidedecorations!(ax); hidespines!(ax)

# ── 对照组: 纯 2D 「剖面抽出」(A 版) = Makie 真正的用武之地 ───────────
ax2 = Axis(fig[1, 2], title = "2D panel pull-out (A) - Makie strength",
           backgroundcolor = RGBf(0.05, 0.05, 0.06), aspect = DataAspect())
hidedecorations!(ax2); hidespines!(ax2)
# 无名者 = 灰剪影矩阵; 名人 = 头像 (选择性栅格 rasterize)
for i in 1:8, j in 1:6
    scatter!(ax2, [Point2f(i, j)], marker = Circle(Point2f(0), 0.30f0), color = GRAY)
end
for (k, x) in enumerate([2, 4.5, 7])
    scatter!(ax2, [Point2f(x, 3.5)], marker = imgs[k], markersize = 62, rasterize = 6)
end

# ── 3D 版头型 marker 在 2D 对照组 (P3: 矢量输出) ─────────────────────
Label(fig[2, 1:3], "cairo 3D: z-sort fails / 2D: rasterized faces + vector same file", color = GRAY, fontsize = 13)

mkpath(OUT)
save(OUT * "/makie-probe-draft-slices.svg", fig)
save(OUT * "/makie-probe-draft-slices.png", fig)
println("P2_P3_svg_ok=true")
println("svg_bytes=", filesize(OUT * "/makie-probe-draft-slices.svg"))
println("png_bytes=", filesize(OUT * "/makie-probe-draft-slices.png"))
println("=== PROBE-DONE-MAKIE ===")
