#!/usr/bin/env python3
# blender -b -P scripts/blender_lighttrail.py
# 光轨版「时间切片」小样: 曲线 = 长曝光光轨 —— 锥形(尾细头亮) + 双管假泛光(晕管+芯管) + 冷暖双色, 暗夜底。
# 不动站位图; 出图 time-slice-lighttrail.png。
import bpy, math, mathutils

OUT = "/Users/mac/Programming/code-2026/cora-atlas/docs/figs"
GOLD = (0.85, 0.71, 0.38)
# 光轨配色: 暖白前灯为主, 金, 红尾灯点缀
TRAILS = [
    (1.00, 0.97, 0.90), (1.00, 0.95, 0.82), (0.85, 0.71, 0.38),
    (0.95, 0.93, 0.88), (0.94, 0.26, 0.16), (0.99, 0.52, 0.20), (1.00, 0.97, 0.90),
]
BASE = [2.7, 1.8, 0.9, 0.0, -0.9, -1.8, -2.7]
SLICES = [-2.9, 0.0, 2.9]
X0, X1 = -5.2, 5.2
PANE_A = 0.11
HALO = [(0.10, 0.22), (0.034, 2.8)]   # (管径, 自发光): 晕管 / 芯管


def clean():
    bpy.ops.wm.read_factory_settings(use_empty=True)


def world():
    sc = bpy.context.scene
    w = bpy.data.worlds.new("W"); sc.world = w; w.use_nodes = True
    bg = w.node_tree.nodes["Background"]
    bg.inputs[0].default_value = (0.007, 0.007, 0.012, 1); bg.inputs[1].default_value = 1.0


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
        b.inputs["Roughness"].default_value = 0.12
    _emit(b, rgb, 0.30)
    m.blend_method = "BLEND"
    return m


def curve_pt(base, t):
    x = X0 + (X1 - X0) * t
    y = base + 0.5 * math.sin(2 * math.pi * 1.7 * t + base) + 0.16 * math.sin(2 * math.pi * 4.6 * t + 2 * base)
    z = 0.5 * math.sin(2 * math.pi * 0.7 * t + base) + 0.11 * math.cos(2 * math.pi * 3.1 * t)
    return (x, y, z)


def add_trail(base, color, thick, emis):
    cu = bpy.data.curves.new("c", "CURVE"); cu.dimensions = "3D"; cu.bevel_depth = thick; cu.bevel_resolution = 3
    sp = cu.splines.new("POLY"); N = 260; sp.points.add(N - 1)
    for i in range(N):
        t = i / (N - 1); x, y, z = curve_pt(base, t)
        sp.points[i].co = (x, y, z, 1.0)
        sp.points[i].radius = 0.25 + 1.05 * (t ** 1.6)      # 光轨锥度: 尾细头亮
    ob = bpy.data.objects.new("c", cu); bpy.context.scene.collection.objects.link(ob)
    ob.data.materials.append(mat_emit("mc", color, emis))
    return ob


def add_slice(x):
    bpy.ops.mesh.primitive_plane_add(size=6.6, location=(x, 0, 0))
    pane = bpy.context.active_object; pane.rotation_euler = (math.radians(90), 0, math.radians(90))
    pane.data.materials.append(mat_glass("sg", GOLD))
    bpy.ops.mesh.primitive_plane_add(size=6.6, location=(x, 0, 0))
    fr = bpy.context.active_object; fr.rotation_euler = (math.radians(90), 0, math.radians(90))
    fr.modifiers.new("wf", "WIREFRAME").thickness = 0.022
    fr.data.materials.append(mat_emit("gf", GOLD, 2.6))


def camera_lights():
    cam_d = bpy.data.cameras.new("C"); cam = bpy.data.objects.new("C", cam_d)
    bpy.context.scene.collection.objects.link(cam)
    loc = mathutils.Vector((10.5, -13.5, 8.6)); cam.location = loc
    cam.rotation_euler = (mathutils.Vector((0, 0, -0.2)) - loc).normalized().to_track_quat("-Z", "Y").to_euler()
    cam_d.lens = 40
    bpy.context.scene.camera = cam
    for loc, e, col in [((7, -8, 10), 900, (1.0, 0.92, 0.75)), ((-9, -5, 4), 180, (0.55, 0.72, 1.0)), ((0, 7, 2), 160, (0.9, 0.85, 0.7))]:
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
    sc.view_settings.look = "AgX - Punchy" if "AgX - Punchy" in [l.name for l in bpy.types.ColorManagedViewSettings.bl_rna.properties["look"].enum_items] else sc.view_settings.look
    sc.render.resolution_x = 1800; sc.render.resolution_y = 1012
    sc.render.image_settings.file_format = "PNG"
    sc.render.filepath = OUT + "/time-slice-lighttrail.png"
    bpy.ops.render.render(write_still=True)
    print("✔", sc.render.filepath)


clean(); world()
for i, base in enumerate(BASE):
    for thick, emis in HALO:
        add_trail(base, TRAILS[i], thick, emis)
for x in SLICES:
    add_slice(x)
camera_lights(); render()
