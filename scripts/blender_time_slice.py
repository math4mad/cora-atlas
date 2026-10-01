#!/usr/bin/env python3
# blender -b -P scripts/blender_time_slice.py
# 「时间切片」3D 概念图 v2: 曲线成发光管, 切片成**通透玻璃面板** + 金框 —— 曲线穿刺而过。
import bpy, math
from mathutils import Vector

OUT = "/Users/mac/Programming/code-2026/cora-atlas/docs/figs"
GOLD = (0.85, 0.71, 0.38)
CURVE_COLORS = [
    (0.85, 0.71, 0.38), (0.90, 0.88, 0.82), (0.52, 0.66, 0.50),
    (0.58, 0.57, 0.53), (0.74, 0.44, 0.36), (0.90, 0.88, 0.82), (0.52, 0.66, 0.50),
]
BASE = [2.7, 1.8, 0.9, 0.0, -0.9, -1.8, -2.7]
SLICES = [-2.9, 0.0, 2.9]


def clean():
    bpy.ops.wm.read_factory_settings(use_empty=True)


def world():
    sc = bpy.context.scene
    w = bpy.data.worlds.new("W"); sc.world = w; w.use_nodes = True
    bg = w.node_tree.nodes["Background"]; bg.inputs[0].default_value = (0.022, 0.022, 0.030, 1); bg.inputs[1].default_value = 1.0


def mat_emit(name, rgb, emis=2.2):
    m = bpy.data.materials.new(name); m.use_nodes = True
    b = m.node_tree.nodes["Principled BSDF"]
    b.inputs["Base Color"].default_value = (*rgb, 1)
    for k in ("Emission Color", "Emission"):
        if k in b.inputs:
            b.inputs[k].default_value = (*rgb, 1); break
    if "Emission Strength" in b.inputs:
        b.inputs["Emission Strength"].default_value = emis
    return m


def mat_glass(name, rgb, a=0.30):
    """半透玻璃面板: alpha 混合 + 微自发光 (EEVEE 可靠显形), 曲线自后透出 = 穿透。"""
    m = bpy.data.materials.new(name); m.use_nodes = True
    b = m.node_tree.nodes["Principled BSDF"]
    b.inputs["Base Color"].default_value = (*rgb, 1)
    b.inputs["Alpha"].default_value = a
    if "Roughness" in b.inputs:
        b.inputs["Roughness"].default_value = 0.15
    for k in ("Emission Color", "Emission"):
        if k in b.inputs:
            b.inputs[k].default_value = (*rgb, 1); break
    if "Emission Strength" in b.inputs:
        b.inputs["Emission Strength"].default_value = 0.6
    m.blend_method = "BLEND"
    return m


def add_curve(base, color, thick=0.05):
    cu = bpy.data.curves.new("c", "CURVE"); cu.dimensions = "3D"; cu.bevel_depth = thick; cu.bevel_resolution = 3
    sp = cu.splines.new("POLY"); N = 260; sp.points.add(N - 1)
    for i in range(N):
        t = i / (N - 1); x = -5.2 + 10.4 * t
        y = base + 0.5 * math.sin(2 * math.pi * 1.7 * t + base) + 0.16 * math.sin(2 * math.pi * 4.6 * t + 2 * base)
        z = 0.5 * math.sin(2 * math.pi * 0.7 * t + base) + 0.11 * math.cos(2 * math.pi * 3.1 * t)
        sp.points[i].co = (x, y, z, 1.0)
    ob = bpy.data.objects.new("c", cu); bpy.context.scene.collection.objects.link(ob)
    ob.data.materials.append(mat_emit("mc", color, 2.2))
    return ob


def add_slice(x):
    # 通透玻璃面板
    bpy.ops.mesh.primitive_plane_add(size=6.6, location=(x, 0, 0))
    pane = bpy.context.active_object; pane.rotation_euler = (math.radians(90), 0, math.radians(90))
    pane.data.materials.append(mat_glass("sg", GOLD, 0.30))
    # 金框 (wireframe 修饰器: 平面边 → 细杆, 曲线自框中穿出)
    bpy.ops.mesh.primitive_plane_add(size=6.6, location=(x, 0, 0))
    fr = bpy.context.active_object; fr.rotation_euler = (math.radians(90), 0, math.radians(90))
    wf = fr.modifiers.new("wf", "WIREFRAME"); wf.thickness = 0.035
    fr.data.materials.append(mat_emit("gf", GOLD, 3.0))
    return pane


def camera_lights():
    import mathutils
    cam_d = bpy.data.cameras.new("C"); cam = bpy.data.objects.new("C", cam_d)
    bpy.context.scene.collection.objects.link(cam)
    loc = mathutils.Vector((10.5, -13.5, 8.6))
    cam.location = loc
    d = (mathutils.Vector((0.0, 0.0, -0.2)) - loc).normalized()
    cam.rotation_euler = d.to_track_quat("-Z", "Y").to_euler()
    cam_d.lens = 40
    bpy.context.scene.camera = cam
    for loc, e, col in [((6, -7, 9), 1000, (1.0, 0.92, 0.75)), ((-8, -5, 4), 260, (0.55, 0.72, 1.0)), ((0, 6, 3), 220, (0.9, 0.85, 0.7))]:
        ld = bpy.data.lights.new("L", "AREA"); ld.energy = e; ld.size = 6; ld.color = col
        lo = bpy.data.objects.new("L", ld); lo.location = loc; lo.rotation_euler = (math.radians(50), 0, math.radians(-20))
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
        if hasattr(sc.eevee, "use_raytracing"):
            sc.eevee.use_raytracing = True
    sc.render.resolution_x = 1800; sc.render.resolution_y = 1012
    sc.render.film_transparent = False
    sc.render.image_settings.file_format = "PNG"
    sc.render.filepath = OUT + "/time-slice-3d-concept.png"
    bpy.ops.render.render(write_still=True)
    print("✔", sc.render.filepath)


clean(); world()
for i, base in enumerate(BASE):
    add_curve(base, CURVE_COLORS[i])
for x in SLICES:
    add_slice(x)
camera_lights(); render()
