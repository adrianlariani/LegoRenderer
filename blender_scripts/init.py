import bpy
import csv
import math
import random


def load_colors(color_list_filepath):
    colors_dict = dict()
    print("Loading Color.....")
    with open(color_list_filepath, 'r', encoding='utf-8') as file:
        next(file)
        csvfile = csv.reader(file)
        for line in csvfile:

            color_name = line[1].replace(" ", "")
            rgb_vals = line[2].strip("()[]").split(",")

            for i in range(len(rgb_vals)):
                rgb_vals[i] = float(rgb_vals[i])
            colors_dict[color_name] = (rgb_vals[0], rgb_vals[1], rgb_vals[2], rgb_vals[3])

    return colors_dict


def init(ldraw_import_filepath):
    print("Initializing.....")
    import addon_utils
    if not addon_utils.check("io_scene_importldraw")[0]:
        bpy.ops.preferences.addon_install(overwrite=True, filepath=ldraw_import_filepath)

    for o in bpy.context.scene.objects:
        o.select_set(True)
    bpy.ops.object.delete()
    bpy.context.scene.render.resolution_x = 256
    bpy.context.scene.render.resolution_y = 256

    bpy.context.scene.render.engine = 'CYCLES'
    bpy.context.preferences.addons[
        "cycles"
    ].preferences.compute_device_type = "CUDA"
    bpy.context.scene.cycles.device = 'GPU'
    bpy.context.scene.cycles.samples = 4
    bpy.context.scene.render.image_settings.file_format = 'JPEG'
    bpy.context.scene.cycles.use_adaptive_sampling = True
    bpy.context.scene.cycles.adaptive_threshold = 1
    bpy.context.scene.render.film_transparent = True
    bpy.context.scene.use_nodes = True
    bpy.context.scene.render.use_file_extension = False

    bpy.ops.object.camera_add(enter_editmode=False, align='VIEW', location=(0, 0, 0.2),
                              rotation=(math.pi / 15, math.pi / 15, 0), scale=(1, 1, 1))
    bpy.context.scene.camera = bpy.data.objects["Camera"]
    bpy.context.object.data.clip_start = 1e-06

    bpy.ops.object.light_add(type='SPOT', align='WORLD', location=(0, 0, 0.5),
                             scale=(0.1, 0.1, 1))
    bpy.context.object.data.shadow_soft_size = 1
    bpy.context.object.scale[0] = 4
    bpy.context.object.scale[1] = 4
    bpy.context.object.visible_glossy = False
    bpy.context.object.data.energy = 5

    bpy.ops.mesh.primitive_plane_add(location=(0, 0, 0),
                                     scale=(2, 2, 1),
                                     rotation=(0, 0, 0))


def setup_render_scene():
    bpy.ops.object.origin_set(type='ORIGIN_CENTER_OF_VOLUME', center='MEDIAN')

    rot_valid = False

    while not rot_valid:
        yb = bpy.context.object.dimensions.y
        xb = bpy.context.object.dimensions.x
        zb = bpy.context.object.dimensions.z

        xy = xb * yb
        yz = yb * zb
        zx = zb * xb

        dict_areas = {"xy": xy, "yz": yz, "zx": zx}

        max_side = max(dict_areas, key=dict_areas.get)
        if max_side != "xy":

            bpy.context.object.rotation_euler[random.choice([0, 1])] = math.pi / 2
            bpy.ops.object.transform_apply(location=False, rotation=True, scale=False)
        else:
            rot_valid = True
