#!/usr/bin/env python3
# blender -b -P scripts/blender_draft_body_slices.py
# 「总谱与剖面」— 主人草图 IMG_2560（总谱：长条 + 刀口）＋ IMG_2561（长轴与 slice 交汇示意）的实现。
#
# 依 2561 改几何（本版）:
#   · 本体 = 圆柱（非方柱）—— 故无「角」，上一版「长轴棱线在切面顶点打叉」之病自消
#   · 切面 = 圆盘（细圆环 + 半透明金面）
#   · 长轴三条：上轮廓 / 中轴 / 下轮廓，穿切面处各打一个「树结」
#   · 本体在每道刀口真断开（缝），中轴同样断开
#
# 三态（主人草图「不放全体，只放名人」的落实）:
#   金环真像 = 名人且馆有官方头像   ／  虚环灰影 = 名人而档案无像
#   微灰剪影 = 同届其余球员（1984 届 216 人／10 轮；1996 与 2003 各 46 人／2 轮）
import bpy, math, csv, os, random, mathutils

DIR = "/Users/mac/Programming/code-2026/cora-atlas"
OUT = DIR + "/docs/figs"
GOLD = (0.85, 0.71, 0.38)
GRAY = (0.40, 0.41, 0.44)

YEARS = [1984, 1996, 2003]
R_CYL = 2.75                      # 圆柱半径（切面盘半径）
X0, X1, Y0, Y1 = -24.0, 24.0, 1947, 2025
TILE = 0.90                       # 名人头像块边长
FAM_ROWS = [2, 4, 4, 2]           # 12 张，内接于圆盘
FAM_DY, FAM_DZ = 0.97, 1.03
CRO_DY, CRO_DZ = 0.30, 0.30       # 灰剪影格距
CRO_R = 2.62                      # 灰剪影填充半径
CUT_GAP = 0.30                    # 刀口缝半宽
SLICE_OVER = 1.06                 # 切片盘略大于截面 → 读作「刀」
KNOT_R = 0.075

RES = (2400, 1350)
CAM_POS = (49.3, -53.2, 18.6)
CAM_TARGET = mathutils.Vector((4.6, 0.0, -0.9))
CAM_LENS = 135
LABEL_S = {1984: (3.20, 3.85), 1996: (3.85, 4.50), 2003: (4.40, 5.00)}


# ── 基础 ────────────────────────────────────────────────────────────
def clean():
    bpy.ops.wm.read_factory_settings(use_empty=True)


def world():
    sc = bpy.context.scene
    w = bpy.data.worlds.new("W"); sc.world = w; w.use_nodes = True
    bg = w.node_tree.nodes["Background"]
    bg.inputs[0].default_value = (0.016, 0.016, 0.023, 1)
    bg.inputs[1].default_value = 1.0


def _emit(b, rgb, e):
    for k in ("Emission Color", "Emission"):
        if k in b.inputs:
            b.inputs[k].default_value = (*rgb, 1); break
    if "Emission Strength" in b.inputs:
        b.inputs["Emission Strength"].default_value = e


def _blend(m):
    for a, v in (("blend_method", "BLEND"), ("surface_render_method", "BLENDED")):
        try:
            setattr(m, a, v)
        except Exception:
            pass


def mat_emit(name, rgb, e=1.0):
    m = bpy.data.materials.new(name); m.use_nodes = True
    b = m.node_tree.nodes["Principled BSDF"]
    b.inputs["Base Color"].default_value = (*rgb, 1); _emit(b, rgb, e)
    if "Roughness" in b.inputs:
        b.inputs["Roughness"].default_value = 0.55
    return m


def mat_glass(name, rgb, a=0.16):
    m = bpy.data.materials.new(name); m.use_nodes = True
    b = m.node_tree.nodes["Principled BSDF"]
    b.inputs["Base Color"].default_value = (*rgb, 1)
    b.inputs["Alpha"].default_value = a
    if "Roughness" in b.inputs:
        b.inputs["Roughness"].default_value = 0.10
    _emit(b, rgb, 0.22)
    _blend(m)
    return m


def mat_tex(name, path, e=0.60):
    m = bpy.data.materials.new(name); m.use_nodes = True
    nt = m.node_tree; bsdf = nt.nodes["Principled BSDF"]
    tex = nt.nodes.new("ShaderNodeTexImage")
    tex.image = bpy.data.images.load(path)
    tex.image.alpha_mode = "STRAIGHT"
    tex.interpolation = "Cubic"
    nt.links.new(tex.outputs["Color"], bsdf.inputs["Base Color"])
    nt.links.new(tex.outputs["Alpha"], bsdf.inputs["Alpha"])
    for k in ("Emission Color", "Emission"):
        if k in bsdf.inputs:
            nt.links.new(tex.outputs["Color"], bsdf.inputs[k]); break
    if "Emission Strength" in bsdf.inputs:
        bsdf.inputs["Emission Strength"].default_value = e
    if "Roughness" in bsdf.inputs:
        bsdf.inputs["Roughness"].default_value = 0.45
    _blend(m)
    return m


def add_line(p, q, rgb=GOLD, e=0.55, r=0.011):
    cu = bpy.data.curves.new("ln", "CURVE"); cu.dimensions = "3D"
    cu.bevel_depth = r; cu.bevel_resolution = 2
    sp = cu.splines.new("POLY"); sp.points.add(1)
    sp.points[0].co = (*p, 1.0); sp.points[1].co = (*q, 1.0)
    ob = bpy.data.objects.new("ln", cu)
    bpy.context.scene.collection.objects.link(ob)
    ob.data.materials.append(mat_emit("ml", rgb, e))
    return ob


def add_ring(x, radius, minor=0.026, rgb=GOLD, e=2.6, seg=96):
    bpy.ops.mesh.primitive_torus_add(location=(x, 0, 0), major_radius=radius, minor_radius=minor,
                                     major_segments=seg, minor_segments=6,
                                     rotation=(0, math.radians(90), 0))
    o = bpy.context.active_object
    o.data.materials.append(mat_emit("ring", rgb, e))
    return o


def add_knot(p, rgb=GOLD, e=2.8, r=KNOT_R):
    """树结: 长轴穿过切面处打的小结核 + 微环。"""
    bpy.ops.mesh.primitive_uv_sphere_add(radius=r, location=p)
    k = bpy.context.active_object
    k.scale = (1.0, 1.0, 0.72)
    k.data.materials.append(mat_emit("kn", rgb, e))
    bpy.ops.mesh.primitive_torus_add(location=p, major_radius=r * 1.85, minor_radius=r * 0.22,
                                     major_segments=20, minor_segments=6,
                                     rotation=(math.radians(90), 0, 0))
    bpy.context.active_object.data.materials.append(mat_emit("kr", GOLD, e + 0.6))


# ── 几何 ────────────────────────────────────────────────────────────
def x_of(year):
    return X0 + (X1 - X0) * (year - Y0) / (Y1 - Y0)


def add_body():
    """圆柱本体，在每道刀口断开成四段；中轴同样断开。"""
    xs = [X0] + [x_of(y) for y in YEARS] + [X1]
    glass = mat_glass("body", (0.62, 0.68, 0.80), 0.085)
    for a, b in zip(xs[:-1], xs[1:]):
        a0 = a + (CUT_GAP if a > X0 else 0.0)
        b0 = b - (CUT_GAP if b < X1 else 0.0)
        bpy.ops.mesh.primitive_cylinder_add(vertices=96, radius=R_CYL, depth=b0 - a0,
                                            location=((a0 + b0) / 2, 0, 0),
                                            rotation=(0, math.radians(90), 0))
        bpy.context.active_object.data.materials.append(glass)
        for zz in (R_CYL, 0.0, -R_CYL):                       # 上轮廓 / 中轴 / 下轮廓
            add_line((a0, 0, zz), (b0, 0, zz))
    for x in (X0, X1):                                         # 两端封口环
        add_ring(x, R_CYL, minor=0.020, e=1.5)


def add_slice(x):
    """切面: 圆盘（半透明金面）＋ 细圆环＋ 长轴三交点各一结。"""
    rr = R_CYL * SLICE_OVER
    bpy.ops.mesh.primitive_circle_add(vertices=96, radius=rr, fill_type="NGON",
                                      location=(x, 0, 0), rotation=(0, math.radians(90), 0))
    bpy.context.active_object.data.materials.append(mat_glass("slice", GOLD, 0.18))
    add_ring(x, rr, minor=0.022, e=3.0)
    for z in (rr, 0.0, -rr):                                   # 上轮廓 / 中轴 / 下轮廓
        add_knot((x, 0.0, z))


def add_crowd(x, n):
    """灰剪影: 圆盘内自下而上填。1984 满盘, 1996/2003 只约两成。"""
    rnd = random.Random(1984 + n)
    mesh = bpy.data.objects["sil_0"]
    pts, z = [], -CRO_R
    while len(pts) < n * 3 and z <= CRO_R:
        y = -CRO_R
        while y <= CRO_R and len(pts) < n * 3:
            if math.hypot(y, z) <= CRO_R:
                pts.append((y, z))
            y += CRO_DY
        z += CRO_DZ
    pts.sort(key=lambda p: p[1])                               # 自下而上
    for (y, z) in pts[:n]:
        o = mesh.copy()
        o.location = (x + rnd.uniform(-0.04, 0.04),
                      y + rnd.uniform(-0.03, 0.03),
                      z + rnd.uniform(-0.03, 0.03))
        o.rotation_euler = (0, 0, rnd.uniform(-0.30, 0.30))
        o.scale = (0.052, 0.046, 0.060)
        o.hide_render = False; o.hide_viewport = False
        bpy.context.scene.collection.objects.link(o)


def build_silhouettes():
    for k in range(3):
        hr = [0.60, 0.66, 0.55][k]
        sr = [1.70, 1.90, 1.55][k]
        bpy.ops.mesh.primitive_uv_sphere_add(radius=hr, segments=12, ring_count=8, location=(0, 0, 0.92))
        head = bpy.context.active_object
        head.scale = (1.0, 1.0, 1.08)
        bpy.ops.mesh.primitive_cone_add(vertices=16, radius1=sr, radius2=sr * 0.62, depth=1.45,
                                        location=(0, 0, -0.42), rotation=(math.radians(180), 0, 0))
        body = bpy.context.active_object
        bpy.ops.object.select_all(action="DESELECT")
        head.select_set(True); body.select_set(True)
        bpy.context.view_layer.objects.active = head
        bpy.ops.object.join()
        o = bpy.context.active_object
        o.name = f"sil_{k}"
        o.data.materials.append(mat_emit(f"silm{k}", GRAY, 0.22))
        o.hide_viewport = True; o.hide_render = True
        o.scale = (0.001, 0.001, 0.001)


def add_quad(center, size, normal, mat):
    bpy.ops.mesh.primitive_plane_add(size=1, location=center)
    o = bpy.context.active_object
    o.rotation_euler = normal.to_track_quat("Z", "Y").to_euler()
    o.scale = (size, size, 1)
    bpy.ops.object.transform_apply(scale=True)
    o.data.materials.append(mat)


def face_cam(pos):
    return (mathutils.Vector(CAM_POS) - mathutils.Vector(pos)).normalized()


def cam_basis():
    v = (CAM_TARGET - mathutils.Vector(CAM_POS)).normalized()
    right = v.cross(mathutils.Vector((0.0, 0.0, 1.0))).normalized()
    return right, right.cross(v).normalized()


def over(pos, d):
    return mathutils.Vector(pos) + cam_basis()[1] * d


def add_text(txt, loc, size, rgb):
    bpy.ops.object.text_add(location=loc)
    t = bpy.context.active_object
    t.data.body = txt
    t.data.size = size
    t.data.align_x = "CENTER"
    t.rotation_euler = face_cam(loc).to_track_quat("Z", "Y").to_euler()
    t.data.materials.append(mat_emit("txt", rgb, 2.4))
    return t


def label(pos, s):
    R = (CAM_TARGET - mathutils.Vector(CAM_POS)).length
    d = (mathutils.Vector(pos) - mathutils.Vector(CAM_POS)).length
    return mathutils.Vector(pos) - cam_basis()[1] * (s * d / R)


def camera_lights():
    cd = bpy.data.cameras.new("C"); cam = bpy.data.objects.new("C", cd)
    bpy.context.scene.collection.objects.link(cam)
    loc = mathutils.Vector(CAM_POS)
    cam.location = loc
    cam.rotation_euler = (CAM_TARGET - loc).normalized().to_track_quat("-Z", "Y").to_euler()
    cd.lens = CAM_LENS
    bpy.context.scene.camera = cam
    for l, e, col, sz in [((16, -18, 22), 4200, (1.0, 0.93, 0.78), 14),
                          ((-18, -12, 10), 1500, (0.55, 0.72, 1.0), 14),
                          ((4, 20, 12), 1100, (0.90, 0.86, 0.74), 14),
                          ((30, 6, -6), 900, (0.85, 0.75, 0.60), 12)]:
        ld = bpy.data.lights.new("L", "AREA"); ld.energy = e; ld.size = sz; ld.color = col
        lo = bpy.data.objects.new("L", ld); lo.location = l
        lo.rotation_euler = (mathutils.Vector((2, 0, 0)) - mathutils.Vector(l)).normalized() \
            .to_track_quat("-Z", "Y").to_euler()
        bpy.context.scene.collection.objects.link(lo)


def render(path):
    sc = bpy.context.scene
    for eng in ("BLENDER_EEVEE_NEXT", "BLENDER_EEVEE", "CYCLES"):
        try:
            sc.render.engine = eng; break
        except Exception:
            continue
    if sc.render.engine == "CYCLES":
        sc.cycles.samples = 64
    elif hasattr(sc, "eevee"):
        for a in ("taa_render_samples", "taa_samples"):
            if hasattr(sc.eevee, a):
                setattr(sc.eevee, a, 64); break
        for a in ("use_raytracing", "use_shadows"):
            if hasattr(sc.eevee, a):
                setattr(sc.eevee, a, True)
    sc.render.resolution_x, sc.render.resolution_y = RES
    sc.render.film_transparent = False
    sc.render.image_settings.file_format = "PNG"
    sc.render.filepath = path
    bpy.ops.render.render(write_still=True)
    print("✔", path)


# ── 主流程 ──────────────────────────────────────────────────────────
clean(); world()
build_silhouettes()

faces = {}
for r in csv.DictReader(open(DIR + "/data/draft-class-faces.csv")):
    faces.setdefault(int(r["draft_year"]), []).append(r)
crowd_n = {int(r["draft_year"]): int(r["n_anonymous"])
           for r in csv.DictReader(open(DIR + "/data/draft-class-crowd.csv"))}

add_body()
for year in YEARS:
    x = x_of(year)
    add_slice(x)
    add_crowd(x, 0 if os.environ.get("NO_CROWD") else crowd_n[year])
    fam = sorted(faces[year], key=lambda r: int(r["overall_pick"]))
    for i, r in enumerate(fam):
        col = sum(FAM_ROWS[:i]) if False else 0
        rw, c = 0, i
        for k, cnt in enumerate(FAM_ROWS):
            if c < cnt:
                rw = k; break
            c -= cnt
        y = (c - (FAM_ROWS[rw] - 1) / 2.0) * FAM_DY
        z = ((len(FAM_ROWS) - 1) / 2.0 - rw) * FAM_DZ + 0.10
        mat = mat_tex("face" + r["person_id"], DIR + "/data/headshots/tile_" + r["person_id"] + ".png")
        add_quad((x + 0.10, y, z), TILE, face_cam((x + 0.10, y, z)), mat)
    tp = label((x, 0, 0), LABEL_S[year][0])
    add_text(f"{year}   ·   {len(fam) + crowd_n[year]} picks", tp, 0.46, GOLD)
    np_ = sum(1 for r in fam if r["has_portrait"] == "1")
    add_text(f"{np_}/{len(fam)} portraits", label((x, 0, 0), LABEL_S[year][1]), 0.34, (0.62, 0.65, 0.72))
    print(f"  {year}: x={x:+.2f}  faces={len(fam)} ({np_} with portrait)  crowd={crowd_n[year]}")

tp = over((4.6, 0, 0), 3.90)
add_text("TOTAL DRAFT   1947 - 2025", tp, 0.80, GOLD)

camera_lights()
render(OUT + "/draft-body-slices-plate.png")
