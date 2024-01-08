import sys
import bpy
import os
from init import *
from reference_obtainers import *


def import_model(model_file, parts_dir):
    try:
        bpy.ops.import_scene.importldraw(filepath=model_file,
                                         ldrawPath=os.path.abspath(os.path.join(parts_dir, os.pardir)),
                                         importCameras=False, positionOnGround=False,
                                         resPrims="Standard", addEnvironment=False)
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

    material = selected_object.active_material

    for mat in selected_object.material_slots:
        if "_4_" in mat.name:
            material = mat.material
    if material is None:
        for child in selected_object.children:
            for mat in child.material_slots:
                if "_4_" in mat.name:
                    material = mat.material

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


def setup_piece(colors: str, colors_dict):
    change_color(colors=colors, colors_dict=colors_dict)

    select_camera()

    bpy.context.object.rotation_euler[0] = random.uniform((-math.pi / 4), (math.pi / 4))

    bpy.context.object.rotation_euler[1] = random.uniform((-math.pi / 4), (math.pi / 4))

    try:
        for obj in bpy.context.scene.objects:
            if obj.type == "EMPTY":
                obj.select_set(True)
            else:
                obj.select_set(False)
        bpy.context.view_layer.objects.active = bpy.context.selected_objects[0]
    except:
        select_obj()

    bpy.context.object.rotation_euler[2] = random.uniform(0, (math.pi * 2))
    bpy.context.object.rotation_euler[1] = random.choice([0, math.pi])

    select_all_objects()
    bpy.ops.view3d.camera_to_view_selected()

    select_plane()
    bpy.context.object.location[2] = get_lowest_pt()

    select_light()

    bpy.context.object.location[0] = random.choice([-0.5, 0.5])
    bpy.context.object.location[1] = random.choice([-0.5, 0.5])
    bpy.context.object.data.energy = random.uniform(0.5, 6)


def render_image(part_id, output_dir, num_renders_each, number=False):
    bpy.context.scene.cycles.samples = 32
    if number:
        print(f"Rendering Part ID: {part_id}  |  {number} / {num_renders_each}")
        bpy.context.scene.render.filepath = os.path.join(output_dir + "/" + part_id,
                                                         (part_id + "-" + str(number) + ".jpg"))
    else:
        print(f"Rendering Part ID: {part_id}")
        bpy.context.scene.render.filepath = os.path.join(output_dir + "/" + part_id, (part_id + ".jpg"))

    bpy.ops.render.render(write_still=True)


def main():
    argv = sys.argv
    parts_dir = argv[5]
    colors_dict = load_colors(argv[6])
    import_ldraw = argv[7]
    output_dir = argv[8]
    part_id = argv[9]
    color = argv[10]
    init(import_ldraw)
    import_model(os.path.join(parts_dir, part_id + ".dat"), parts_dir)
    setup_render_scene()
    setup_piece(colors=color, colors_dict=colors_dict)
    render_image(part_id=part_id, output_dir=output_dir, num_renders_each=1)


if __name__ == "__main__":
    main()
