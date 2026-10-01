#!/usr/bin/env python3
# blender -b -P scripts/blender_face_slices.py
# 「人脸切片」概念图 (第二张): 53 个地标 = 53 条时间线; 切片上的「结」聚成人脸拓图。
#   脸形随切片而变(morph); 中片(此刻)最亮 —— 时间即断层扫描, 每刀切出一张脸。
import bpy, math, json, mathutils

DIR = "/Users/mac/Programming/code-2026/cora-atlas"
OUT = DIR + "/docs/figs"
LM = json.load(open(DIR + "/docs/figs/face-landmarks.json"))
U, V = LM["u"], LM["v"]
N = len(U)
SCALE = 2.45
HL = 2.75                      # 半时轴
SLICE_T = [-0.88, 0.0, 0.88]   # 三刀: 过去 / 此刻 / 将来
GOLD = (0.85, 0.71, 0.38)
VC = 0.135                     # 脸心 v (居中用)
PAL = [(0.88, 0.74, 0.40), (0.90, 0.88, 0.82), (0.56, 0.70, 0.54), (0.76, 0.48, 0.40), (0.62, 0.60, 0.56)]


def clean():
    bpy.ops.wm.read_factory_settings(use_empty=True)


def world():
    sc = bpy.context.scene
    w = bpy.data.worlds.new("W"); sc.world = w; w.use_nodes = True
    bg = w.node_tree.nodes["Background"]; bg.inputs[0].default_value = (0.020, 0.020, 0.028, 1); bg.inputs[1].default_value = 1.0


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


def mat_glass(name, rgb, a=0.34):
    m = bpy.data.materials.new(name); m.use_nodes = True
    b = m.node_tree.nodes["Principled BSDF"]
    b.inputs["Base Color"].default_value = (*rgb, 1); b.inputs["Alpha"].default_value = a
    if "Roughness" in b.inputs:
        b.inputs["Roughness"].default_value = 0.12
    _emit(b, rgb, 0.30)
    m.blend_method = "BLEND"
    return m


def lm_color(i):
    return PAL[min(len(PAL) - 1, int((V[i] + 0.9) / 2.0 * len(PAL)))]


def lm_uv(i, t):
    """地标 i 在时刻 t∈[-1,1] 的 (y,z): 各走己路, 整体 morph。"""
    u, v = U[i], V[i]
    y = SCALE * (u * (1.0 + 0.14 * t) + 0.018 * math.sin(2.4 * t + 3.1 * u + 0.7 * v))
    z = SCALE * (v * (1.0 - 0.07 * t) + 0.018 * math.sin(2.1 * t + 3.1 * v) - VC * (1.0 - 0.04 * t))
    return y, z


def add_line(p, q, rgb, e, r=0.011):
    cu = bpy.data.curves.new("ln", "CURVE"); cu.dimensions = "3D"; cu.bevel_depth = r; cu.bevel_resolution = 2
    sp = cu.splines.new("POLY"); sp.points.add(1)
    sp.points[0].co = (*p, 1.0); sp.points[1].co = (*q, 1.0)
    ob = bpy.data.objects.new("ln", cu); bpy.context.scene.collection.objects.link(ob)
    ob.data.materials.append(mat_emit("ml", rgb, e))
    return ob


def add_timeline(i):
    cu = bpy.data.curves.new("tl", "CURVE"); cu.dimensions = "3D"; cu.bevel_depth = 0.016; cu.bevel_resolution = 2
    sp = cu.splines.new("POLY"); M = 60; sp.points.add(M - 1)
    for j in range(M):
        t = -1.0 + 2.0 * j / (M - 1); y, z = lm_uv(i, t)
        sp.points[j].co = (t * HL, y, z, 1.0)
    ob = bpy.data.objects.new("tl", cu); bpy.context.scene.collection.objects.link(ob)
    ob.data.materials.append(mat_emit("mtl", lm_color(i), 0.95))
    return ob


def add_knot(p, rgb, e, r=0.050):
    bpy.ops.mesh.primitive_uv_sphere_add(radius=r, location=p)
    k = bpy.context.active_object; k.scale = (1.0, 1.0, 0.7)
    k.data.materials.append(mat_emit("kn", rgb, e))
    bpy.ops.mesh.primitive_torus_add(location=p, major_radius=r * 1.72, minor_radius=r * 0.20,
                                     major_segments=18, minor_segments=5, rotation=(math.radians(90), 0, 0))
    bpy.context.active_object.data.materials.append(mat_emit("kr", GOLD, 1.4))


def add_slice(t, is_now):
    x = t * HL
    bpy.ops.mesh.primitive_plane_add(size=6.4, location=(x, 0, 0))
    pane = bpy.context.active_object; pane.rotation_euler = (math.radians(90), 0, math.radians(90))
    pane.data.materials.append(mat_glass("sg", GOLD, 0.40 if is_now else 0.20))
    bpy.ops.mesh.primitive_plane_add(size=6.4, location=(x, 0, 0))
    fr = bpy.context.active_object; fr.rotation_euler = (math.radians(90), 0, math.radians(90))
    fr.modifiers.new("wf", "WIREFRAME").thickness = 0.024
    fr.data.materials.append(mat_emit("gf", GOLD, 3.0 if is_now else 2.0))


def nn_edges(k=3):
    """脸的拓图: 各点连最近 k 邻 (拓扑在整条时间线上恒定)。"""
    E = set()
    for i in range(N):
        d = sorted(((U[i] - U[j]) ** 2 + (V[i] - V[j]) ** 2, j) for j in range(N) if j != i)
        for _, j in d[:k]:
            E.add((min(i, j), max(i, j)))
    return sorted(E)


def add_web(t, edges):
    """切片上的人脸拓图网 (细线, 于该时刻的坐标)。"""
    rgb = GOLD
    for i, j in edges:
        y1, z1 = lm_uv(i, t); y2, z2 = lm_uv(j, t)
        add_line((t * HL, y1, z1), (t * HL, y2, z2), rgb, 0.34, r=0.0058)


def camera_lights():
    cam_d = bpy.data.cameras.new("C"); cam = bpy.data.objects.new("C", cam_d)
    bpy.context.scene.collection.objects.link(cam)
    loc = mathutils.Vector((13.7, -0.55, 0.45)); cam.location = loc
    cam.rotation_euler = (mathutils.Vector((0, 0, -0.06)) - loc).normalized().to_track_quat("-Z", "Y").to_euler()
    cam_d.lens = 50
    bpy.context.scene.camera = cam
    for loc, e, col in [((7, -8, 10), 1250, (1.0, 0.92, 0.75)), ((-9, -5, 4), 300, (0.55, 0.72, 1.0)), ((0, 7, 2), 260, (0.9, 0.85, 0.7))]:
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
    sc.render.resolution_x = 1800; sc.render.resolution_y = 1012
    sc.render.film_transparent = False
    sc.render.image_settings.file_format = "PNG"
    sc.render.filepath = OUT + "/face-slices-concept.png"
    bpy.ops.render.render(write_still=True)
    print("✔", sc.render.filepath)


clean(); world()
E = nn_edges(2)
for i in range(N):
    add_timeline(i)
for t in SLICE_T:
    is_now = abs(t) < 1e-6
    add_slice(t, is_now)
    add_web(t, E)
    for i in range(N):                       # 交点 = 脸上的地标
        y, z = lm_uv(i, t)
        e, r = (2.6, 0.058) if is_now else (0.95, 0.027)
        add_knot((t * HL, y, z), lm_color(i), e, r)
camera_lights(); render()
