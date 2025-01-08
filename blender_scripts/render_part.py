import sys
import bpy
import os
from blender_scripts.init import *
from blender_scripts.reference_obtainers import *


def import_model(model_file, parts_dir):
    try:
        bpy.ops.import_scene.importldraw(filepath=model_file,
                                         ldrawPath=os.path.abspath(os.path.join(parts_dir, os.pardir)),
                                         importCameras=False,
                                         positionOnGround=False,
                                         resPrims="Standard",
                                         addEnvironment=False,
                                         useLogoStuds=True)
        return True
    except:
        return False


def change_color(colors: str, colors_dict: dict):
    if len(colors) > 2:
        color_list = colors.strip("[]").replace(" ", "").replace("'", "").split(",")
        random_color = random.choice(color_list)
        while random_color not in colors_dict:
            random_color = random.choice(color_list)
    else:
        random_color = random.choice(list(colors_dict.keys()))

    select_all_objects()

    selected_object = bpy.context.selected_objects[0]

    materials = set()

    material = selected_object.active_material

    for mat in selected_object.material_slots:
        if "_4_" in mat.name:
            materials.add(mat.material)
    if material is None:
        for child in selected_object.children:
            for mat in child.material_slots:
                if "_4_" in mat.name:
                    materials.add(mat.material)

    if "_4_" not in material.name:
        select_all_objects()
        try:
            selected_object = bpy.context.selected_objects[1]
            materials.add(selected_object.active_material)
        except:
            pass
    for material in materials:
        if material is None:
            continue
        material.use_nodes = True

        for node in material.node_tree.nodes:
            inputs = list(node.inputs)
            if inputs[0].bl_label == "Color":
                material.node_tree.nodes.remove(node)
                break

        select_all_objects()

        group = material.node_tree.nodes.new("ShaderNodeGroup")
        group.node_tree = bpy.data.node_groups['Lego Standard']

        if "Chrome" in random_color:
            group.node_tree = bpy.data.node_groups['Lego Chrome']
        elif "Pearl" in random_color:
            group.node_tree = bpy.data.node_groups['Lego Pearlescent']
        elif "Trans" in random_color:
            group.node_tree = bpy.data.node_groups['Lego Transparent']
        elif "Speckle" in random_color:
            group.node_tree = bpy.data.node_groups['Lego Speckle']
        elif "Metal" in random_color:
            group.node_tree = bpy.data.node_groups['Lego Metal']
        elif "Glitter" in random_color:
            group.node_tree = bpy.data.node_groups['Lego Glitter']
        elif "Milky White" in random_color:
            group.node_tree = bpy.data.node_groups['Lego Milky White']
        else:
            group.node_tree = bpy.data.node_groups['Lego Standard']

        material.node_tree.links.new(material.node_tree.nodes[1].outputs[0], group.inputs[len(group.inputs) - 1])
        material.node_tree.links.new(group.outputs[0], material.node_tree.nodes[0].inputs[0])

        group.inputs["Color"].default_value = colors_dict[random_color]


def setup_piece(colors: str, colors_dict, camera_min_x_rot, camera_max_x_rot, camera_min_y_rot,
                camera_max_y_rot, camera_zoom_min, camera_zoom_max, flip_part, random_spin):
    for o in bpy.context.scene.objects:
        if o.type == 'MESH' and "light" in o.name:
            o.select_set(True)
        else:
            o.select_set(False)
    bpy.ops.object.delete()
    change_color(colors=colors, colors_dict=colors_dict)

    set_correct_rotation()

    select_camera()
    bpy.context.object.data.lens = 50

    # bpy.context.object.rotation_euler[0] = random.uniform((-math.pi / 5), (math.pi / 5))

    # bpy.context.object.rotation_euler[1] = random.uniform((-math.pi / 5), (math.pi / 5))

    bpy.context.object.rotation_euler[0] = random.uniform(camera_min_x_rot, camera_max_x_rot)

    bpy.context.object.rotation_euler[1] = random.uniform(camera_min_y_rot, camera_max_y_rot)
    try:
        for obj in bpy.context.scene.objects:
            if obj.type == "EMPTY":
                obj.select_set(True)
            else:
                obj.select_set(False)
        bpy.context.view_layer.objects.active = bpy.context.selected_objects[0]
    except:
        select_obj()
    if random_spin:
        bpy.context.object.rotation_euler[2] = random.uniform(0, (math.pi * 2))
    if flip_part:
        bpy.context.object.rotation_euler[1] = random.choice([0, math.pi])

    select_all_objects()
    bpy.ops.view3d.camera_to_view_selected()

    select_camera()

    bpy.context.object.data.lens_unit = 'MILLIMETERS'
    if camera_zoom_min != camera_zoom_max:
        bpy.context.object.data.lens = random.randrange(camera_zoom_min, camera_zoom_max, 1)
    else:
        bpy.context.object.data.lens = camera_zoom_min

    select_plane()
    bpy.context.object.location[2] = get_lowest_pt()

    select_light()

    bpy.context.object.location[0] = random.choice([-0.5, 0.5])
    bpy.context.object.location[1] = random.choice([-0.5, 0.5])
    bpy.context.object.data.energy = random.uniform(10, 70)


def render_image(part_id, output_dir, num_renders_each, number=False):
    bpy.context.scene.cycles.samples = 4
    if number:
        print(f"Rendering Part ID: {part_id}  |  {number} / {num_renders_each}")
        bpy.context.scene.render.filepath = os.path.join(output_dir + "/" + part_id,
                                                         (part_id + "-" + str(number) + ".jpg"))
    else:
        print(f"Rendering Part ID: {part_id}")
        bpy.context.scene.render.filepath = os.path.join(output_dir + "/" + part_id, (part_id + ".jpg"))

    bpy.ops.render.render(write_still=True)


def set_correct_rotation():
    import bpy
    from bpy import context
    import numpy as np
    import itertools

    # multiply 3d coord list by matrix
    def np_matmul_coords(coords, matrix, space=None):
        M = (space @ matrix @ space.inverted()
             if space else matrix).transposed()
        ones = np.ones((coords.shape[0], 1))
        coords4d = np.hstack((coords, ones))

        return np.dot(coords4d, M)[:, :-1]
        return coords4d[:, :-1]

    # get the global coordinates of all object bounding box corners
    coords = np.vstack(
        tuple(np_matmul_coords(np.array(o.bound_box), o.matrix_world.copy())
              for o in
              context.scene.objects
              if o.type == 'MESH' and o.name != "Plane"
              )
    )
    # bottom front left (all the mins)
    bfl = coords.min(axis=0)
    # top back right
    tbr = coords.max(axis=0)
    G = np.array((bfl, tbr)).T
    # bound box coords ie the 8 combinations of bfl tbr.
    bbc = [i for i in itertools.product(*G)]
    import math

    coord = np.array(bbc)[0]
    x = coord[0]
    y = coord[1]
    z = coord[2]

    for coordinate in np.array(bbc):
        if x == coordinate[0] and y == coordinate[1]:
            z_axis = math.dist([z], [coordinate[2]])
        if x == coordinate[0] and z == coordinate[2]:
            y_axis = math.dist([y], [coordinate[1]])
        if z == coordinate[2] and y == coordinate[1]:
            x_axis = math.dist([x], [coordinate[0]])

    xy = x_axis * y_axis
    zx = z_axis * x_axis
    yz = y_axis * z_axis
    sides = [xy, zx, yz]

    try:
        for obj in bpy.context.scene.objects:
            if obj.type == "EMPTY":
                obj.select_set(True)
            else:
                obj.select_set(False)
        bpy.context.view_layer.objects.active = bpy.context.selected_objects[0]
    except:
        for o in bpy.context.scene.objects:
            if o.type == "MESH" and "Plane" not in o.name:
                o.select_set(True)
            else:
                o.select_set(False)
        bpy.context.view_layer.objects.active = bpy.context.selected_objects[0]

    if max(sides) == xy:
        pass
    if max(sides) == zx:
        bpy.context.object.rotation_euler[0] = math.pi / 2
    if max(sides) == yz:
        bpy.context.object.rotation_euler[1] = math.pi / 2

    bpy.ops.object.transform_apply(location=False, rotation=True, scale=False)


def main():
    argv = sys.argv
    parts_dir = argv[5]
    colors_dict = load_colors(argv[6])
    import_ldraw = argv[7]
    output_dir = argv[8]
    part_id = argv[9]
    color = argv[10]
    camera_x_rot = float(argv[11])
    camera_y_rot = float(argv[12])
    camera_zoom = float(argv[13])

    init(import_ldraw)
    import_model(os.path.join(parts_dir, part_id + ".dat"), parts_dir)
    setup_render_scene()
    setup_piece(colors=color, colors_dict=colors_dict, camera_min_x_rot=camera_x_rot,
                camera_max_x_rot=camera_x_rot, camera_min_y_rot=camera_y_rot,
                camera_max_y_rot=camera_y_rot, camera_zoom_min=camera_zoom,
                camera_zoom_max=camera_zoom, flip_part=False, random_spin=False)
    render_image(part_id=part_id, output_dir=output_dir, num_renders_each=1)


if __name__ == "__main__":
    main()
