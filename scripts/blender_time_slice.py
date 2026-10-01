#!/usr/bin/env python3
# blender -b -P scripts/blender_time_slice.py
# 「时间切片」3D 概念图 v3:
#   切片面更透 (薄金玻璃); 曲线穿刺处生「树结」(结节球); 遮挡段亮度降低 (自发光压低 + 玻璃染色/遮影)。
import bpy, math, mathutils

OUT = "/Users/mac/Programming/code-2026/cora-atlas/docs/figs"
GOLD = (0.85, 0.71, 0.38)
CURVE_COLORS = [
    (0.85, 0.71, 0.38), (0.90, 0.88, 0.82), (0.52, 0.66, 0.50),
    (0.58, 0.57, 0.53), (0.74, 0.44, 0.36), (0.90, 0.88, 0.82), (0.52, 0.66, 0.50),
]
BASE = [2.7, 1.8, 0.9, 0.0, -0.9, -1.8, -2.7]
SLICES = [-2.9, 0.0, 2.9]
X0, X1 = -5.2, 5.2
EMIT = 1.15          # 曲线自发光压低 → 遮挡处靠光照/染色真变暗
PANE_A = 0.40        # 切片透明度(降→更不透明): 穿过之曲线被压暗="被遮挡段变暗"


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


def mat_emit(name, rgb, e=EMIT):
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
    _emit(b, rgb, 0.35)
    m.blend_method = "BLEND"
    return m


def curve_pt(base, t):
    x = X0 + (X1 - X0) * t
    y = base + 0.5 * math.sin(2 * math.pi * 1.7 * t + base) + 0.16 * math.sin(2 * math.pi * 4.6 * t + 2 * base)
    z = 0.5 * math.sin(2 * math.pi * 0.7 * t + base) + 0.11 * math.cos(2 * math.pi * 3.1 * t)
    return (x, y, z)


def t_at_x(x):
    return (x - X0) / (X1 - X0)


def add_curve(base, color, thick=0.05):
    cu = bpy.data.curves.new("c", "CURVE"); cu.dimensions = "3D"; cu.bevel_depth = thick; cu.bevel_resolution = 3
    sp = cu.splines.new("POLY"); N = 260; sp.points.add(N - 1)
    for i in range(N):
        x, y, z = curve_pt(base, i / (N - 1))
        sp.points[i].co = (x, y, z, 1.0)
    ob = bpy.data.objects.new("c", cu); bpy.context.scene.collection.objects.link(ob)
    ob.data.materials.append(mat_emit("mc", color))
    return ob


def add_knot(p, color):
    """穿过切片处之「树结」: 小结核(略扁球) + 微环, 如树干上长枝的结。"""
    bpy.ops.mesh.primitive_uv_sphere_add(radius=0.085, location=p)
    k = bpy.context.active_object
    k.scale = (1.0, 1.0, 0.72)
    k.data.materials.append(mat_emit("kn", color, EMIT + 1.0))
    bpy.ops.mesh.primitive_torus_add(location=p, major_radius=0.15, minor_radius=0.016,
                                     major_segments=20, minor_segments=6,
                                     rotation=(math.radians(90), 0, 0))
    r = bpy.context.active_object
    r.data.materials.append(mat_emit("kr", GOLD, 1.6))


def add_slice(x):
    bpy.ops.mesh.primitive_plane_add(size=6.6, location=(x, 0, 0))
    pane = bpy.context.active_object; pane.rotation_euler = (math.radians(90), 0, math.radians(90))
    pane.data.materials.append(mat_glass("sg", GOLD))
    pane.visible_shadow = True
    bpy.ops.mesh.primitive_plane_add(size=6.6, location=(x, 0, 0))
    fr = bpy.context.active_object; fr.rotation_euler = (math.radians(90), 0, math.radians(90))
    wf = fr.modifiers.new("wf", "WIREFRAME"); wf.thickness = 0.028
    fr.data.materials.append(mat_emit("gf", GOLD, 2.6))
    return pane


def camera_lights():
    cam_d = bpy.data.cameras.new("C"); cam = bpy.data.objects.new("C", cam_d)
    bpy.context.scene.collection.objects.link(cam)
    loc = mathutils.Vector((10.5, -13.5, 8.6)); cam.location = loc
    cam.rotation_euler = (mathutils.Vector((0, 0, -0.2)) - loc).normalized().to_track_quat("-Z", "Y").to_euler()
    cam_d.lens = 40
    bpy.context.scene.camera = cam
    for loc, e, col in [((7, -8, 10), 1200, (1.0, 0.92, 0.75)), ((-9, -5, 4), 300, (0.55, 0.72, 1.0)), ((0, 7, 2), 260, (0.9, 0.85, 0.7))]:
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
    sc.render.filepath = OUT + "/time-slice-3d-concept.png"
    bpy.ops.render.render(write_still=True)
    print("✔", sc.render.filepath)


clean(); world()
for i, base in enumerate(BASE):
    add_curve(base, CURVE_COLORS[i])
for x in SLICES:
    add_slice(x)
    for i, base in enumerate(BASE):          # 交点树结: 每条曲线穿每片切片处
        add_knot(curve_pt(base, t_at_x(x)), CURVE_COLORS[i])
camera_lights(); render()
