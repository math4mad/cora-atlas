#!/usr/bin/env python3
# blender -b -P scripts/blender_time_slice.py
# 「时间切片」3D 概念图 (低采样): 多条状态曲线成发光管, 三处切片成半透明金面。
import bpy, math, os

OUT = os.path.join(os.path.dirname(os.path.abspath(bpy.data.filepath or ".")), "docs", "figs")
OUT = "/Users/mac/Programming/code-2026/cora-atlas/docs/figs"

GOLD = (0.79, 0.66, 0.35)
CURVE_COLORS = [
    (0.79, 0.66, 0.35), (0.85, 0.83, 0.78), (0.50, 0.63, 0.48),
    (0.55, 0.54, 0.50), (0.71, 0.42, 0.35), (0.85, 0.83, 0.78), (0.50, 0.63, 0.48),
]
BASE = [2.6, 1.7, 0.8, -0.1, -1.0, -1.9, -2.8]


def clean():
    bpy.ops.wm.read_factory_settings(use_empty=True)


def world():
    sc = bpy.context.scene
    w = bpy.data.worlds.new("W"); sc.world = w; w.use_nodes = True
    bg = w.node_tree.nodes["Background"]
    bg.inputs[0].default_value = (0.025, 0.025, 0.032, 1.0)
    bg.inputs[1].default_value = 1.0


def mat_c(name, rgb, emis=1.6):
    m = bpy.data.materials.new(name); m.use_nodes = True
    b = m.node_tree.nodes["Principled BSDF"]
    b.inputs["Base Color"].default_value = (*rgb, 1)
    for key in ("Emission Color", "Emission"):
        if key in b.inputs:
            b.inputs[key].default_value = (*rgb, 1)
            break
    if "Emission Strength" in b.inputs:
        b.inputs["Emission Strength"].default_value = emis
    return m


def mat_glass(name, rgb, a=0.10):
    m = bpy.data.materials.new(name); m.use_nodes = True
    b = m.node_tree.nodes["Principled BSDF"]
    b.inputs["Base Color"].default_value = (*rgb, 1)
    b.inputs["Alpha"].default_value = a
    m.blend_method = "BLEND"
    return m


def add_curve(base, color, thick=0.055):
    cu = bpy.data.curves.new("c", "CURVE"); cu.dimensions = "3D"
    cu.bevel_depth = thick; cu.bevel_resolution = 3
    sp = cu.splines.new("POLY"); N = 240; sp.points.add(N - 1)
    for i in range(N):
        t = i / (N - 1); x = -5.0 + 10.0 * t
        y = base + 0.55 * math.sin(2 * math.pi * 1.7 * t + base) + 0.18 * math.sin(2 * math.pi * 4.6 * t + 2 * base)
        z = 0.55 * math.sin(2 * math.pi * 0.7 * t + base) + 0.12 * math.cos(2 * math.pi * 3.1 * t)
        sp.points[i].co = (x, y, z, 1.0)
    ob = bpy.data.objects.new("c", cu); bpy.context.scene.collection.objects.link(ob)
    ob.data.materials.append(mat_c("mc", color))
    return ob


def add_slice(x):
    bpy.ops.mesh.primitive_plane_add(size=7.0, location=(x, 0, 0))
    pl = bpy.context.active_object
    pl.rotation_euler = (math.radians(90), 0, math.radians(90))
    pl.data.materials.append(mat_glass("sg", GOLD, 0.12))
    return pl


def camera_lights():
    cam_d = bpy.data.cameras.new("C"); cam = bpy.data.objects.new("C", cam_d)
    bpy.context.scene.collection.objects.link(cam)
    cam.location = (8.5, -11.5, 6.5)
    cam.rotation_euler = (math.radians(64), 0, math.radians(37))
    cam_d.lens = 42
    bpy.context.scene.camera = cam
    for loc, energy, col in [((6, -6, 9), 900, (1.0, 0.92, 0.75)), ((-7, -4, 5), 300, (0.6, 0.75, 1.0))]:
        ld = bpy.data.lights.new("L", "AREA"); ld.energy = energy; ld.size = 6; ld.color = col
        lo = bpy.data.objects.new("L", ld); lo.location = loc
        lo.rotation_euler = (math.radians(45), 0, math.radians(-25))
        bpy.context.scene.collection.objects.link(lo)


def render():
    sc = bpy.context.scene
    try:
        sc.render.engine = "BLENDER_EEVEE_NEXT"
    except Exception:
        try:
            sc.render.engine = "BLENDER_EEVEE"
        except Exception:
            sc.render.engine = "CYCLES"
    if sc.render.engine == "CYCLES":
        sc.cycles.samples = 24
    else:
        if hasattr(sc, "eevee") and hasattr(sc.eevee, "taa_render_samples"):
            sc.eevee.taa_render_samples = 24
    sc.render.resolution_x = 1600; sc.render.resolution_y = 900
    sc.render.film_transparent = False
    sc.render.image_settings.file_format = "PNG"
    sc.render.filepath = os.path.join(OUT, "time-slice-3d-concept.png")
    bpy.ops.render.render(write_still=True)
    print("✔", sc.render.filepath)


clean(); world()
for i, base in enumerate(BASE):
    add_curve(base, CURVE_COLORS[i])
for x in (-2.8, 0.9, 3.4):
    add_slice(x)
camera_lights(); render()
