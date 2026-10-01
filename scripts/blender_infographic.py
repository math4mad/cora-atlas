#!/usr/bin/env python3
# blender -b -P scripts/blender_infographic.py
# 信息图版「时间切片」: 切片上挂锚词标签(真词库) + 结旁标 Tₙ₋ₖ/T₀/T₁ + 一条 3D 时间路径。
import bpy, math, mathutils

OUT = "/Users/mac/Programming/code-2026/cora-atlas/docs/figs"
FONTP = "/System/Library/Fonts/STHeiti Medium.ttc"
GOLD = (0.88, 0.74, 0.40)
SAGE = (0.58, 0.72, 0.56)
WHITE = (0.92, 0.91, 0.86)

SLICES = [(-2.6, "Tₙ₋ₖ"), (0.0, "T₀"), (2.6, "T₁")]
BROWN = (0.80, 0.62, 0.34)
# (词, y, z, 色)  —— 真词库锚词: 超市群(上) / 路边摊群(下)
WORDS = [
    ("收银台", 0.62, 1.18, GOLD), ("货架", -0.02, 1.42, GOLD), ("购物车", -0.66, 1.12, GOLD),
    ("折叠桌", 0.66, -1.16, SAGE), ("烧烤摊", -0.02, -1.44, SAGE), ("大排档", -0.70, -1.10, SAGE),
]
PANE_A = 0.16
FONT = None


def clean():
    bpy.ops.wm.read_factory_settings(use_empty=True)


def world():
    sc = bpy.context.scene
    w = bpy.data.worlds.new("W"); sc.world = w; w.use_nodes = True
    bg = w.node_tree.nodes["Background"]; bg.inputs[0].default_value = (0.016, 0.016, 0.024, 1); bg.inputs[1].default_value = 1.0


def _emit(b, rgb, e):
    for k in ("Emission Color", "Emission"):
        if k in b.inputs:
            b.inputs[k].default_value = (*rgb, 1); break
    if "Emission Strength" in b.inputs:
        b.inputs["Emission Strength"].default_value = e


def mat_emit(name, rgb, e):
    m = bpy.data.materials.new(name); m.use_nodes = True
    b = m.node_tree.nodes["Principled BSDF"]
    b.inputs["Base Color"].default_value = (*rgb, 1); _emit(b, rgb, e)
    return m


def mat_glass(name, rgb, a=PANE_A):
    m = bpy.data.materials.new(name); m.use_nodes = True
    b = m.node_tree.nodes["Principled BSDF"]
    b.inputs["Base Color"].default_value = (*rgb, 1); b.inputs["Alpha"].default_value = a
    if "Roughness" in b.inputs:
        b.inputs["Roughness"].default_value = 0.14
    _emit(b, rgb, 0.25)
    m.blend_method = "BLEND"
    return m


CAM = mathutils.Vector((10.6, -14.6, 6.9))


def text_obj(s, loc, size=0.30, rgb=WHITE, emis=3.2, face=True, rot=None):
    bpy.ops.object.text_add(location=loc)
    ob = bpy.context.active_object
    ob.data.body = s; ob.data.size = size
    ob.data.align_x = "CENTER"; ob.data.align_y = "CENTER"
    ob.data.extrude = 0.006
    if FONT:
        ob.data.font = FONT
    if rot is not None:
        ob.rotation_euler = rot
    elif face:
        ob.rotation_euler = (CAM - mathutils.Vector(loc)).to_track_quat("Z", "Y").to_euler()
    ob.data.materials.append(mat_emit("mt", rgb, emis))
    return ob


def text_pair(base, sub, loc, size=0.40, subsize=0.25, rgb=GOLD, emis=3.4, gap=0.23):
    """真下标: 「T」 + 小一号的脚标 —— 绕开字体缺下标字符(ₙ₋ₖ)之病。"""
    loc = mathutils.Vector(loc)
    rot = (CAM - loc).to_track_quat("Z", "Y")
    M = rot.to_matrix()
    right = M @ mathutils.Vector((1, 0, 0)); up = M @ mathutils.Vector((0, 1, 0))
    text_obj(base, loc - right * gap, size=size, rgb=rgb, emis=emis, rot=rot.to_euler())
    text_obj(sub, loc + right * (gap * 0.80) - up * (size * 0.26), size=subsize, rgb=rgb, emis=emis, rot=rot.to_euler())


def add_line(p, q, rgb, e, r=0.008):
    cu = bpy.data.curves.new("ln", "CURVE"); cu.dimensions = "3D"; cu.bevel_depth = r; cu.bevel_resolution = 2
    sp = cu.splines.new("POLY"); sp.points.add(1)
    sp.points[0].co = (*p, 1.0); sp.points[1].co = (*q, 1.0)
    ob = bpy.data.objects.new("ln", cu); bpy.context.scene.collection.objects.link(ob)
    ob.data.materials.append(mat_emit("ml", rgb, e))
    return ob


def anchor_pos(i, x, t):
    """锚词在切片 x 处的坐标 (每片略移, 令时间线微斜)。"""
    _, y, z, _ = WORDS[i]
    return (x, y * (1.0 + 0.10 * t) + 0.05 * math.sin(2.4 * t + i), z * (1.0 + 0.07 * t))


def add_anchor_curve(i, rgb):
    cu = bpy.data.curves.new("ac", "CURVE"); cu.dimensions = "3D"; cu.bevel_depth = 0.020; cu.bevel_resolution = 3
    sp = cu.splines.new("POLY"); M = 48; sp.points.add(M - 1)
    for j in range(M):
        t = -1.0 + 2.0 * j / (M - 1)
        x, y, z = anchor_pos(i, t * 2.6, t)
        x = t * 2.6
        sp.points[j].co = (x, y, z, 1.0)
        sp.points[j].radius = 0.7 + 0.5 * math.cos(1.5 * t)
    ob = bpy.data.objects.new("ac", cu); bpy.context.scene.collection.objects.link(ob)
    ob.data.materials.append(mat_emit("ma", rgb, 1.1))
    return ob


def add_slice(x, label):
    bpy.ops.mesh.primitive_plane_add(size=5.4, location=(x, 0, 0))
    pane = bpy.context.active_object; pane.rotation_euler = (math.radians(90), 0, math.radians(90))
    pane.data.materials.append(mat_glass("sg", GOLD))
    bpy.ops.mesh.primitive_plane_add(size=5.4, location=(x, 0, 0))
    fr = bpy.context.active_object; fr.rotation_euler = (math.radians(90), 0, math.radians(90))
    fr.modifiers.new("wf", "WIREFRAME").thickness = 0.022
    fr.data.materials.append(mat_emit("gf", GOLD, 2.2))
    # 切片名 Tₙ₋ₖ/T₀/T₁ —— 挂片上缘 (真下标)
    TB = {"Tₙ₋ₖ": "n−k", "T₀": "0", "T₁": "1"}[label]
    text_pair("T", TB, (x, -2.28, 2.42), size=0.46, subsize=0.28)


def add_rail():
    """3D 时间路径: 底部轨道 + 刻度 + 箭头(时间方向)。"""
    z = -3.15; y0 = -1.55
    add_line((-3.3, y0, z), (3.3, y0, z), GOLD, 2.4, r=0.022)
    for x, lab in SLICES:
        add_line((x, y0 - 0.14, z), (x, y0 + 0.14, z), GOLD, 2.4, r=0.018)
        TB = {"Tₙ₋ₖ": "n−k", "T₀": "0", "T₁": "1"}[lab]
        text_pair("T", TB, (x, y0 + 0.50, z - 0.30), size=0.30, subsize=0.19, emis=2.6)
    # 箭头
    for s in (-1, 1):
        add_line((3.3, y0, z), (2.95, y0 + s * 0.13, z), GOLD, 2.4, r=0.018)
    text_obj("时间 →", (4.05, y0 + 0.30, z + 0.30), size=0.26, rgb=WHITE, emis=2.4)


def add_legend():
    """图例: 色键标明两个概念空间。"""
    for k, (lab, col) in enumerate([("超市", GOLD), ("路边摊", SAGE)]):
        loc = (-4.55, -1.9, 3.30 - k * 0.46)
        bpy.ops.mesh.primitive_uv_sphere_add(radius=0.082, location=loc)
        bpy.context.active_object.data.materials.append(mat_emit("lg", col, 3.0))
        text_obj(lab, (loc[0] + 0.62, loc[1], loc[2]), size=0.30, rgb=col, emis=3.2)


def camera_lights():
    cam_d = bpy.data.cameras.new("C"); cam = bpy.data.objects.new("C", cam_d)
    bpy.context.scene.collection.objects.link(cam)
    cam.location = CAM
    cam.rotation_euler = (mathutils.Vector((0, 0, -0.1)) - CAM).normalized().to_track_quat("-Z", "Y").to_euler()
    cam_d.lens = 42
    bpy.context.scene.camera = cam
    for loc, e, col in [((7, -8, 10), 1100, (1.0, 0.92, 0.75)), ((-9, -5, 4), 260, (0.55, 0.72, 1.0)), ((0, 7, 2), 240, (0.9, 0.85, 0.7))]:
        ld = bpy.data.lights.new("L", "AREA"); ld.energy = e; ld.size = 6; ld.color = col
        lo = bpy.data.objects.new("L", ld); lo.location = loc; lo.rotation_euler = (math.radians(52), 0, math.radians(-22))
        bpy.context.scene.collection.objects.link(lo)


def render():
    sc = bpy.context.scene
    for eng in ("BLENDER_EEVEE_NEXT", "BLENDER_EEVEE", "CYCLES"):
        try:
            sc.render.engine = eng; break
        except Exception:
            continue
    if sc.render.engine == "CYCLES":
        sc.cycles.samples = 64
    elif hasattr(sc, "eevee"):
        for attr in ("taa_render_samples", "taa_samples"):
            if hasattr(sc.eevee, attr):
                setattr(sc.eevee, attr, 48); break
        for attr in ("use_raytracing", "use_shadows", "use_volumetric_shadows"):
            if hasattr(sc.eevee, attr):
                setattr(sc.eevee, attr, True)
    sc.render.resolution_x = 1800; sc.render.resolution_y = 1125
    sc.render.image_settings.file_format = "PNG"
    sc.render.filepath = OUT + "/time-slice-infographic.png"
    bpy.ops.render.render(write_still=True)
    print("✔", sc.render.filepath)


clean(); world()
FONT = bpy.data.fonts.load(FONTP)
for i in range(len(WORDS)):
    add_anchor_curve(i, WORDS[i][3])
for x, lab in SLICES:
    add_slice(x, lab)
    t = x / 2.6
    for i in range(len(WORDS)):
        p = anchor_pos(i, x, t)
        bpy.ops.mesh.primitive_uv_sphere_add(radius=0.058, location=p)
        bpy.context.active_object.data.materials.append(mat_emit("kn", WORDS[i][3], 3.0))
        # 锚词标签(挂牌): 自脸心径向散开 + 引线
        dy, dz = WORDS[i][1], WORDS[i][2]
        nrm = math.hypot(dy, dz) or 1.0
        lp = (x, dy + 0.62 * dy / nrm, dz + 0.62 * dz / nrm)
        add_line(p, lp, WORDS[i][3], 1.5, r=0.006)
        text_obj(WORDS[i][0], lp, size=0.23, rgb=WORDS[i][3], emis=3.0)
add_rail()
add_legend()
camera_lights(); render()
