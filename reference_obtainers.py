import bpy


def get_lowest_pt() -> int:
    lowest_pt = 10e10
    for obj in bpy.context.scene.objects:
        if obj.type == "MESH" and "Plane" not in obj.name:
            temp = min([(obj.matrix_world @ v.co).z for v in obj.data.vertices])
            if temp < lowest_pt:
                lowest_pt = temp
    return lowest_pt


def select_all_objects():
    for o in bpy.context.scene.objects:
        if o.type == "MESH" and "Plane" not in o.name:
            o.select_set(True)
        else:
            o.select_set(False)


def select_obj():
    for o in bpy.context.scene.objects:
        if o.type == "MESH" and "Plane" not in o.name:
            o.select_set(True)
        else:
            o.select_set(False)
    bpy.context.view_layer.objects.active = bpy.context.selected_objects[0]


def select_plane():
    for o in bpy.context.scene.objects:
        if "Plane" in o.name:
            o.select_set(True)
        else:
            o.select_set(False)
    bpy.context.view_layer.objects.active = bpy.context.selected_objects[0]


def select_camera():
    for o in bpy.context.scene.objects:
        if o.type == "CAMERA":
            o.select_set(True)
        else:
            o.select_set(False)
    bpy.context.view_layer.objects.active = bpy.context.selected_objects[0]


def select_light():
    for o in bpy.context.scene.objects:
        if o.type == "LIGHT":
            o.select_set(True)
        else:
            o.select_set(False)
    bpy.context.view_layer.objects.active = bpy.context.selected_objects[0]


def select_empty():
    for o in bpy.context.scene.objects:
        if o.type == "EMPTY":
            o.select_set(True)
        else:
            o.select_set(False)
    bpy.context.view_layer.objects.active = bpy.context.selected_objects[0]


def reset_delete():
    for o in bpy.context.scene.objects:
        if o.type == 'MESH' and "Plane" not in o.name:
            o.select_set(True)
        elif o.type == "EMPTY":
            o.select_set(True)
        else:
            o.select_set(False)
    bpy.ops.object.delete()
