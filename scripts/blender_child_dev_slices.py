#!/usr/bin/env python3
# blender -b -P scripts/blender_child_dev_slices.py
# 「儿童发展 · 切片柱阵」— 承 NBA「总谱与剖面」之 Blender 三维语法（主人 1003 令：
#   child-dev-slices 各阶段 slice 替换 NBA 选秀 slice，用 Blender 3D 渲染）。
#   本体(长条) = 儿童发展时间长河 (月龄 12 → 42)；六道刀口 = 六月龄阶段 12/18/24/30/36/42。
#   每道切面之上：五指标各立一方柱，柱高 ∝ 该指标在该月的值（词汇量·MLU·词类多样性·句法复杂度·指代清晰度）。
import bpy, math, os, json, mathutils
DIR = "/Users/mac/Programming/code-2026/cora-atlas"
OUT = DIR + "/docs/figs"
GOLD = (0.85, 0.71, 0.38)
METRIC_RGB = [(0.16, 0.61, 0.56), (0.25, 0.50, 0.70), (0.54, 0.44, 0.69),
              (0.85, 0.54, 0.24), (0.75, 0.36, 0.36)]

VAL = json.load(open(DIR + "/data/child-dev-values.json"))
MONTHS = VAL["months"]; METRICS = VAL["metrics"]; VALS = VAL["values"]

X0, X1 = -24.0, 24.0
M0, M1 = MONTHS[0], MONTHS[-1]
HI_Y, HI_Z = 2.40, 3.20
RES = (2400, 1350)
CUT_GAP = 0.44
BAR_DY, BAR_DX = 0.70, 0.40          # 柱: 横宽(Y) / 厚(X)
BAR_BASE = -HI_Z + 0.40
BAR_GAIN = 4.30                       # 柱高 = BAR_GAIN * value


def clean():
    bpy.ops.wm.read_factory_settings(use_empty=True)


def world():
    sc = bpy.context.scene
    w = bpy.data.worlds.new("W"); sc.world = w; w.use_nodes = True
    bg = w.node_tree.nodes["Background"]
    bg.inputs[0].default_value = (0.016, 0.016, 0.023, 1); bg.inputs[1].default_value = 1.0


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
        b.inputs["Roughness"].default_value = 0.5
    return m


def mat_glass(name, rgb, a=0.16):
    m = bpy.data.materials.new(name); m.use_nodes = True
    b = m.node_tree.nodes["Principled BSDF"]
    b.inputs["Base Color"].default_value = (*rgb, 1)
    b.inputs["Alpha"].default_value = a
    if "Roughness" in b.inputs:
        b.inputs["Roughness"].default_value = 0.10
    _emit(b, rgb, 0.22); _blend(m)
    return m


def x_of(m):
    return X0 + (X1 - X0) * (m - M0) / (M1 - M0)


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


def add_knot(p, rgb=GOLD, e=2.8, r=0.085):
    bpy.ops.mesh.primitive_uv_sphere_add(radius=r, location=p)
    k = bpy.context.active_object; k.scale = (1.0, 1.0, 0.72)
    k.data.materials.append(mat_emit("kn", rgb, e))
    bpy.ops.mesh.primitive_torus_add(location=p, major_radius=r * 1.85, minor_radius=r * 0.22,
                                     major_segments=20, minor_segments=6,
                                     rotation=(math.radians(90), 0, 0))
    bpy.context.active_object.data.materials.append(mat_emit("kr", GOLD, e + 0.6))


def add_beam():
    xs = [X0] + [x_of(m) for m in MONTHS] + [X1]
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
        add_line((a0, 0, 0), (b0, 0, 0), GOLD)
    for x in (X0, X1):
        for i in range(4):
            (ay, az), (by, bz) = CORNERS[i], CORNERS[(i + 1) % 4]
            add_line((x, ay * HI_Y, az * HI_Z), (x, by * HI_Y, bz * HI_Z), GOLD)


def add_slice_plane(x):
    bpy.ops.mesh.primitive_plane_add(size=1, location=(x, 0, 0))
    p = bpy.context.active_object
    p.rotation_euler = (0, math.radians(90), 0)
    p.scale = (HI_Y * 2, HI_Z * 2, 1)
    bpy.ops.object.transform_apply(scale=True)
    p.data.materials.append(mat_glass("slice", GOLD, 0.16))
    for i in range(4):
        (ay, az), (by, bz) = CORNERS[i], CORNERS[(i + 1) % 4]
        add_line((x, ay * HI_Y, az * HI_Z), (x, by * HI_Y, bz * HI_Z), GOLD, e=3.0, r=0.018)
    add_knot((x, 0.0, 0.0))


def add_bars(x, vals):
    """切面之上：五指标各立一方柱，柱高 ∝ 值。"""
    n = len(vals)
    for i, v in enumerate(vals):
        y = (i - (n - 1) / 2.0) * 0.92
        hz = 0.18 + BAR_GAIN * float(v)
        zc = BAR_BASE + hz / 2.0
        bpy.ops.mesh.primitive_cube_add(size=1, location=(x, y, zc))
        o = bpy.context.active_object
        o.scale = (BAR_DX, BAR_DY, hz)
        bpy.ops.object.transform_apply(scale=True)
        o.data.materials.append(mat_emit(f"bar{i}", METRIC_RGB[i], 0.75))
        # 柱顶亮环(标记高度)
        r = 0.11
        bpy.ops.mesh.primitive_uv_sphere_add(radius=r, location=(x, y, BAR_BASE + hz))
        o.data.materials.append(o.data.materials[0])
        bpy.context.active_object.data.materials.append(mat_emit(f"cap{i}", METRIC_RGB[i], 3.0))


def add_text(txt, loc, size, rgb, normal, align="CENTER"):
    bpy.ops.object.text_add(location=loc)
    t = bpy.context.active_object
    t.data.body = txt; t.data.size = size; t.data.align_x = align
    t.rotation_euler = normal.to_track_quat("Z", "Y").to_euler()
    t.data.materials.append(mat_emit("txt", rgb, 2.4))
    return t


def cam_basis():
    v = (CAM_TARGET - mathutils.Vector(CAM_POS)).normalized()
    right = v.cross(mathutils.Vector((0.0, 0.0, 1.0))).normalized()
    sup = right.cross(v).normalized()
    return right, sup


def under(pos, d):
    return mathutils.Vector(pos) - cam_basis()[1] * d


def over(pos, d):
    return mathutils.Vector(pos) + cam_basis()[1] * d


def camera_lights():
    cd = bpy.data.cameras.new("C"); cam = bpy.data.objects.new("C", cd)
    bpy.context.scene.collection.objects.link(cam)
    loc = mathutils.Vector(CAM_POS)
    cam.location = loc
    cam.rotation_euler = (CAM_TARGET - loc).normalized().to_track_quat("-Z", "Y").to_euler()
    cd.lens = CAM_LENS
    bpy.context.scene.camera = cam
    for l, e, col, sz in [((16, -18, 22), 2000, (1.0, 0.95, 0.85), 16),
                          ((-18, -12, 10), 700, (0.60, 0.75, 1.0), 16),
                          ((4, 20, 12), 500, (0.95, 0.90, 0.80), 16),
                          ((30, 6, -6), 400, (0.90, 0.82, 0.70), 14)]:
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
                setattr(sc.eevee, a, 160); break
    sc.render.resolution_x, sc.render.resolution_y = RES
    sc.render.film_transparent = False
    sc.render.image_settings.file_format = "PNG"
    sc.render.filepath = path
    bpy.ops.render.render(write_still=True)
    print("✔", path)


CAM_POS = (50.0, -58.0, 21.0)
CAM_TARGET = mathutils.Vector((0.0, 0.0, -0.5))
CAM_LENS = 62
LABEL_S = 3.95


def label(pos, s):
    R = (CAM_TARGET - mathutils.Vector(CAM_POS)).length
    d = (mathutils.Vector(pos) - mathutils.Vector(CAM_POS)).length
    return under(pos, s * d / R)


clean(); world()
LABELS = []
add_beam()
for mi, m in enumerate(MONTHS):
    x = x_of(m)
    add_slice_plane(x)
    add_bars(x, VALS[mi])
    tp = label((x, 0, -HI_Z), LABEL_S)
    LABELS.append(dict(text=f"{m} 月", kind="month", pos=[tp[0], tp[1], tp[2]]))
    print(f"  {m}mo: x={x:+.2f}")

tp = over((4.6, 0, 0), 3.95)
LABELS.append(dict(text="CHILD DEVELOPMENT   12 - 42 MO", kind="title", pos=[tp[0], tp[1], tp[2]]))

camera_lights()
VER = os.environ.get("VER", "v01")
VDIR = os.path.join(OUT, "child-dev-slices-3d", VER)
os.makedirs(VDIR, exist_ok=True)
from bpy_extras.object_utils import world_to_camera_view
sc = bpy.context.scene
sc.render.resolution_x, sc.render.resolution_y = RES
bpy.context.view_layer.update()
for L in LABELS:
    c = world_to_camera_view(sc, sc.camera, mathutils.Vector(L["pos"]))
    L["px"], L["py"] = round(c.x * RES[0], 1), round((1.0 - c.y) * RES[1], 1)
json.dump(LABELS, open(VDIR + "/labels.json", "w"), ensure_ascii=False, indent=1)
print("labels ->", [(L["kind"], L["px"], L["py"]) for L in LABELS])
render(VDIR + "/plate.png")
