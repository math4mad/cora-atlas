#!/usr/bin/env julia
# glmakie_draft_body_slices.jl — 「总谱与剖面」Makie 轨 (GLMakie + SSAO) 判据探针 = 小一号的真图
#   P1 纹理: mesh!(...; color=<图矩阵>, ssao=true) 能否把 36 张真头像贴上 3D 切面?
#   P2 半透明: 切片面 RGBA alpha 在 3D 里能否正确合成?
#   P3 SSAO: 是否给出 blender 级别的接缝/深度感?
#   P4 无头渲: closeall() 后 save 能否在本机跑通?
#   P5 阵列: meshscatter 几百个灰剪影 + SSAO 是否吃得消?
#
# 用法: julia -t 4 scripts/glmakie_draft_body_slices.jl
const DIR = "/Users/mac/Programming/code-2026/cora-atlas"
const OUT = DIR * "/docs/figs"
using GLMakie, FileIO, Colors, GeometryBasics
using GeometryBasics: Vec2f, Vec3f, Point2f, Point3f, TriangleFace, meta

GLMakie.activate!(ssao = true, px_per_unit = 1)
GLMakie.closeall()

const GOLD = RGBf(0.85, 0.71, 0.38)
const GRAY = RGBf(0.42, 0.43, 0.46)
const YEARS = [1984, 1996, 2003]
const HI_Y, HI_Z = 2.40, 3.20
const X0, X1, YR0, YR1 = -24.0, 24.0, 1947, 2025
const TILE = 1.05
xF(y) = X0 + (X1 - X0) * (y - YR0) / (YR1 - YR0)

csvrows(p) = (h = split(strip(readlines(p)[1]), ","); [Dict(h .=> split(strip(l), ",")) for l in readlines(p)[2:end] if !isempty(strip(l))])

# ── 一片带 uv 的矩形 (法向 +X, 即切面姿态) ───────────────────────────
function panel(x, y, z, w, h)
    v = [Point3f(x, y - w / 2, z - h / 2), Point3f(x, y + w / 2, z - h / 2),
         Point3f(x, y + w / 2, z + h / 2), Point3f(x, y - w / 2, z + h / 2)]
    uv = [Vec2f(0, 1), Vec2f(1, 1), Vec2f(1, 0), Vec2f(0, 0)]
    return Mesh(meta(v; uv = uv), [TriangleFace(1, 2, 3), TriangleFace(1, 3, 4)])
end

# 面朝相机 (billboard): 在 YZ 平面内自转, 使法向指向 cam
function billboard(x, y, z, w, cam)
    v = [Point3f(x, y - w / 2, z - w / 2), Point3f(x, y + w / 2, z - w / 2),
         Point3f(x, y + w / 2, z + w / 2), Point3f(x, y - w / 2, z + w / 2)]
    uv = [Vec2f(0, 1), Vec2f(1, 1), Vec2f(1, 0), Vec2f(0, 0)]
    return Mesh(meta(v; uv = uv), [TriangleFace(1, 2, 3), TriangleFace(1, 3, 4)])
end

const FACE = csvrows(joinpath(DIR, "data", "draft-class-faces.csv"))
const CROWD = Dict(parse(Int, r["draft_year"]) => parse(Int, r["n_anonymous"]) for r in csvrows(joinpath(DIR, "data", "draft-class-crowd.csv")))

ssao = Makie.SSAO(radius = 5.0, blur = 3)
fig = Figure(size = (2000, 1125), backgroundcolor = RGBf(0.016, 0.016, 0.023))
ax = LScene(fig[1, 1]; show_axis = false, scenekw = (ssao = ssao,))
ax.scene.ssao.bias[] = 0.025
ax.scene.ssao.radius[] = 5.0

# ── 本体: 半透明长条 (P2) ─────────────────────────────────────────
bx = (X0 + X1) / 2
mesh!(ax, Rect3f(Point3f(X0, -HI_Y, -HI_Z), Vec3f(X1 - X0, 2HI_Y, 2HI_Z));
      color = RGBAf(0.62, 0.68, 0.80, 0.06), transparency = true, ssao = false)
for (sx, sy, sz, w, d, h) in [(X0, -HI_Y, -HI_Z, X1 - X0, 2HI_Y, 0.03),
                              (X0, -HI_Y, HI_Z, X1 - X0, 2HI_Y, 0.03),
                              (X0, -HI_Y, -HI_Z, X1 - X0, 0.03, 2HI_Z),
                              (X0, HI_Y, -HI_Z, X1 - X0, 0.03, 2HI_Z)]
    mesh!(ax, Rect3f(Point3f(sx, sy, sz), Vec3f(w, d, h)); color = GOLD, ssao = true)
end

ntile = 0
for yr in YEARS
    x = xF(yr)
    # 切片面 (金, 半透明) —— P2
    mesh!(ax, panel(x, 0, 0, 2HI_Y, 2HI_Z); color = RGBAf(GOLD.r, GOLD.g, GOLD.b, 0.22),
          transparency = true, ssao = true)
    # 灰剪影阵列 —— P5
    n = CROWD[yr]
    cols = 12
    ps = Point3f[]
    for i in 0:(n - 1)
        c, r = i % cols, i ÷ cols
        push!(ps, Point3f(x + 0.06 * sin(i), -HI_Y + 0.30 + c * 0.42, -HI_Z + 0.22 + r * 0.36))
    end
    meshscatter!(ax, ps; marker = Rect3f(Vec3f(-0.5, -0.5, -0.5), Vec3f(0.16, 0.13, 0.30)),
                 color = GRAY, ssao = true)
    # 12 张真头像 —— P1
    fam = sort([r for r in FACE if parse(Int, r["draft_year"]) == yr], by = r -> parse(Int, r["overall_pick"]))
    for (i, r) in enumerate(fam)
        c, rw = i % 3, i ÷ 3
        y = (c - 1) * 1.18
        z = (1.5 - rw) * 1.18 + 0.25
        img = FileIO.load(joinpath(DIR, "data", "headshots", "tile_" * r["person_id"] * ".png"))
        mesh!(ax, panel(x + 0.10, y, z, TILE, TILE); color = img, ssao = true)
        global ntile += 1
    end
    println("  $yr: faces=", length(fam), " crowd=", n)
end

update_cam!(ax.scene, Vec3f(49.3, -53.2, 18.6), Vec3f(4.6, 0, -0.9))
ax.scene.camera.projection[] = Makie.PerspectiveProjection(15.2)

mkpath(OUT)
save(OUT * "/makie-draft-body-slices-probe.png", fig)
println("P1_tiles_placed=", ntile)
println("png_bytes=", filesize(OUT * "/makie-draft-body-slices-probe.png"))
println("=== GLMAKIE-PROBE-DONE ===")
