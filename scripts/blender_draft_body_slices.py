#!/usr/bin/env python3
# blender -b -P scripts/blender_draft_body_slices.py
# 「总谱与剖面」— 主人 1003 草图 IMG_2560 的 C 版（真三维半透明切面）。
#   长条 = 本体 (Total draft, 1947-2025 全选秀池); 三道刀口 = 1984 / 1996 / 2003 三届。
#   切面之上: 名人 12 张真头像 (金环, 亮度高) = 锚点;
#             其余全体 = 灰剪影小阵 (1984 一行 12x18 填满, 1996/2003 只 46 人 → 四行, 八成空)。
#   ⇒ 同形不同物: 三个切面长得一样, 密度与面孔却全不同 —— 投影不可恢复律的物证。
import bpy, math, csv, os, random, mathutils
DIR = "/Users/mac/Programming/code-2026/cora-atlas"
OUT = DIR + "/docs/figs"
GOLD = (0.85, 0.71, 0.38)
GRAY = (0.40, 0.41, 0.44)

YEARS = [1984, 1996, 2003]
HI_Y, HI_Z = 2.40, 3.20          # 切面半宽 / 半高
X0, X1, Y0, Y1 = -24.0, 24.0, 1947, 2025
TILE = 1.05                       # 名人头像块边长
FAM_COLS, FAM_ROWS = 3, 4         # 12 = 3x4 面孔阵
CRO_COLS = 12                     # 灰剪影阵列数
CRO_DY, CRO_DZ = 0.42, 0.36       # 灰剪影格距

RES = (2400, 1350)
CUT_GAP = 0.30                   # 刀口缝半宽: 本体在切面处断开, 棱线到缝即止 (主人 1003 令)
SLICE_OVER = 1.18                # 切片面板明显大于截面 → 顶角落在体外, 不与长轴棱线咬合


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


# ── 几何 ────────────────────────────────────────────────────────────
def x_of(year):
    return X0 + (X1 - X0) * (year - Y0) / (Y1 - Y0)


def add_line(p, q, rgb, e=0.55, r=0.011):
    cu = bpy.data.curves.new("ln", "CURVE"); cu.dimensions = "3D"
    cu.bevel_depth = r; cu.bevel_resolution = 2
    sp = cu.splines.new("POLY"); sp.points.add(1)
    sp.points[0].co = (*p, 1.0); sp.points[1].co = (*q, 1.0)
    ob = bpy.data.objects.new("ln", cu)
    bpy.context.scene.collection.objects.link(ob)
    ob.data.materials.append(mat_emit("ml", rgb, e))
    return ob


CORNERS = [(-1, -1), (1, -1), (1, 1), (-1, 1)]
KNOT_R = 0.085


def add_knot(p, rgb=GOLD, e=2.8, r=KNOT_R):
    """树结: 长轴(轮廓线/中轴)穿过切面处打的小结核 + 微环 —— 主人草图 IMG_2561 之意。"""
    bpy.ops.mesh.primitive_uv_sphere_add(radius=r, location=p)
    k = bpy.context.active_object
    k.scale = (1.0, 1.0, 0.72)
    k.data.materials.append(mat_emit("kn", rgb, e))
    bpy.ops.mesh.primitive_torus_add(location=p, major_radius=r * 1.85, minor_radius=r * 0.22,
                                     major_segments=20, minor_segments=6,
                                     rotation=(math.radians(90), 0, 0))
    bpy.context.active_object.data.materials.append(mat_emit("kr", GOLD, e + 0.6))


def add_beam():
    """本体: 半透明长条 1947→2025, 在每道刀口断开成四段。
    棱线分段绘制 —— 否则它们会穿过切面、在切面顶点处打叉。"""
    xs = [X0] + [x_of(y) for y in YEARS] + [X1]
    glass = mat_glass("beam", (0.62, 0.68, 0.80), 0.055)
    for a, b in zip(xs[:-1], xs[1:]):
        a0 = a + (CUT_GAP if a > X0 else 0.0)
        b0 = b - (CUT_GAP if b < X1 else 0.0)
        bpy.ops.mesh.primitive_cube_add(size=1, location=((a0 + b0) / 2, 0, 0))
        s = bpy.context.active_object
        s.scale = (b0 - a0, HI_Y * 2, HI_Z * 2)
        bpy.ops.object.transform_apply(scale=True)
        s.data.materials.append(glass)
        for cy, cz in CORNERS:
            add_line((a0, cy * HI_Y, cz * HI_Z), (b0, cy * HI_Y, cz * HI_Z), GOLD)
        add_line((a0, 0, 0), (b0, 0, 0), GOLD)          # 中轴 (长轴)
    for x in (X0, X1):                                # 两端封口矩形
        for i in range(4):
            (ay, az), (by, bz) = CORNERS[i], CORNERS[(i + 1) % 4]
            add_line((x, ay * HI_Y, az * HI_Z), (x, by * HI_Y, bz * HI_Z), GOLD)


def add_slice_plane(x):
    oy, oz = HI_Y * SLICE_OVER, HI_Z * SLICE_OVER
    bpy.ops.mesh.primitive_plane_add(size=1, location=(x, 0, 0))
    p = bpy.context.active_object
    p.rotation_euler = (0, math.radians(90), 0)
    p.scale = (oy * 2, oz * 2, 1)
    bpy.ops.object.transform_apply(scale=True)
    p.data.materials.append(mat_glass("slice", GOLD, 0.20))
    for i in range(4):
        (ay, az), (by, bz) = CORNERS[i], CORNERS[(i + 1) % 4]
        add_line((x, ay * oy, az * oz), (x, by * oy, bz * oz), GOLD, e=3.0, r=0.020)
    add_knot((x, 0.0, 0.0))          # 三个切片各一: 长轴(中轴)与切片交汇处


def add_quad(center, size, normal, mat, square=True):
    bpy.ops.mesh.primitive_plane_add(size=1, location=center)
    o = bpy.context.active_object
    o.rotation_euler = normal.to_track_quat("Z", "Y").to_euler()
    o.scale = (size, size, 1)
    bpy.ops.object.transform_apply(scale=True)
    o.data.materials.append(mat)
    return o


def add_crowd(x, n):
    """灰剪影小阵: 12 列, 自下而上填; 1984 满 18 行, 1996/2003 只 4 行。"""
    rnd = random.Random(1984 + n)
    meshes = [bpy.data.objects[f"sil_{k}"] for k in range(3)]
    for i in range(n):
        c, r = i % CRO_COLS, i // CRO_COLS
        y = -HI_Y + 0.30 + c * CRO_DY + rnd.uniform(-0.035, 0.035)
        z = -HI_Z + 0.22 + r * CRO_DZ + rnd.uniform(-0.035, 0.035)
        o = meshes[rnd.randrange(3)].copy()          # 共享 mesh, 只立新对象
        o.location = (x + rnd.uniform(-0.05, 0.05), y, z)
        o.rotation_euler = (0, 0, rnd.uniform(-0.30, 0.30))
        o.scale = (0.055, 0.048, 0.062)
        o.hide_render = False; o.hide_viewport = False
        bpy.context.scene.collection.objects.link(o)


def build_silhouettes():
    """三型灰剪影各建一个共享 mesh (头球 + 肩锥)。"""
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


def add_text(txt, loc, size, rgb, normal, align="CENTER"):
    bpy.ops.object.text_add(location=loc)
    t = bpy.context.active_object
    t.data.body = txt
    t.data.size = size
    t.data.align_x = align
    t.rotation_euler = normal.to_track_quat("Z", "Y").to_euler()
    t.data.materials.append(mat_emit("txt", rgb, 2.4))
    return t


def cam_dir(pos):
    return (CAM_TARGET - mathutils.Vector(pos)).normalized()


def face_cam(pos):
    """从 pos 指向相机 —— 面片/文字之 +Z 应朝此 (正面朝观众)。"""
    return (mathutils.Vector(CAM_POS) - mathutils.Vector(pos)).normalized()


def cam_basis():
    """屏幕基: 返回 (向右, 向上) 之世界向量, 供文字贴屏幕方向摆位。"""
    v = (CAM_TARGET - mathutils.Vector(CAM_POS)).normalized()
    right = v.cross(mathutils.Vector((0.0, 0.0, 1.0))).normalized()
    sup = right.cross(v).normalized()
    return right, sup


def over(pos, d):
    return mathutils.Vector(pos) + cam_basis()[1] * d


def under(pos, d):
    return mathutils.Vector(pos) - cam_basis()[1] * d


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
        lo.rotation_euler = (mathutils.Vector((2, 0, 0)) - mathutils.Vector(l)).normalized().to_track_quat("-Z", "Y").to_euler()
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
CAM_POS = (49.3, -53.2, 18.6)
CAM_TARGET = mathutils.Vector((4.6, 0.0, -0.9))
CAM_LENS = 135
LABEL_S = {1984: (3.20, 3.85), 1996: (3.85, 4.50), 2003: (4.40, 5.00)}   # 屏幕单位, 非世界单位


def label(pos, s):
    """按屏幕偏移 s 摆位 (远处切片要放大世界距离, 以保屏幕等距)。"""
    R = (CAM_TARGET - mathutils.Vector(CAM_POS)).length
    d = (mathutils.Vector(pos) - mathutils.Vector(CAM_POS)).length
    return under(pos, s * d / R)

clean(); world()
build_silhouettes()

faces = {}
for r in csv.DictReader(open(DIR + "/data/draft-class-faces.csv")):
    faces.setdefault(int(r["draft_year"]), []).append(r)
crowd_n = {}
for r in csv.DictReader(open(DIR + "/data/draft-class-crowd.csv")):
    crowd_n[int(r["draft_year"])] = int(r["n_anonymous"])

add_beam()

for year in YEARS:
    x = x_of(year)
    add_slice_plane(x)
    add_crowd(x, 0 if os.environ.get("NO_CROWD") else crowd_n[year])
    fam = sorted(faces[year], key=lambda r: int(r["overall_pick"]))
    for i, r in enumerate(fam):
        c, rw = i % FAM_COLS, i // FAM_COLS        # 3 列 × 4 行
        y = (c - (FAM_COLS - 1) / 2.0) * 1.18
        z = ((FAM_ROWS - 1) / 2.0 - rw) * 1.18 + 0.25
        mat = mat_tex("face" + r["person_id"], DIR + "/data/headshots/tile_" + r["person_id"] + ".png")
        add_quad((x + 0.10, y, z), TILE, face_cam((x + 0.10, y, z)), mat)
    tp = label((x, 0, 0), LABEL_S[year][0])
    add_text(f"{year}   ·   {len(fam) + crowd_n[year]} picks", tp, 0.46, GOLD, face_cam(tp))
    np_ = sum(1 for r in fam if r["has_portrait"] == "1")
    tq = label((x, 0, 0), LABEL_S[year][1])
    add_text(f"{np_}/{len(fam)} portraits", tq, 0.34, (0.62, 0.65, 0.72), face_cam(tq))
    print(f"  {year}: x={x:+.2f}  faces={len(fam)} ({np_} with portrait)  crowd={crowd_n[year]}")

tp = over((4.6, 0, 0), 3.90)
add_text("TOTAL DRAFT   1947 - 2025", tp, 0.80, GOLD, face_cam(tp))

camera_lights()
render(OUT + "/draft-body-slices-plate.png")
