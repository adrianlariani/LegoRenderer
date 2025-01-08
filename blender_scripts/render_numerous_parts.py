import sys
import os
from blender_scripts.init import *
from blender_scripts.render_part import import_model, setup_render_scene, setup_piece, render_image
from blender_scripts.reference_obtainers import reset_delete


def main():
    argv = sys.argv
    parts_dir = argv[5]
    colors_dict = load_colors(argv[6])
    import_ldraw = argv[7]
    output_dir = argv[8]
    models_csv = argv[9]
    start_index = int(argv[10])
    end_index = int(argv[11])
    num_renders_each = int(argv[12])
    camera_min_x_rot = float(argv[13])
    camera_max_x_rot = float(argv[14])
    camera_min_y_rot = float(argv[15])
    camera_max_y_rot = float(argv[16])
    camera_zoom_min = float(argv[17])
    camera_zoom_max = float(argv[18])
    flip_part = bool(int(argv[19]))
    random_spin = bool(int(argv[20]))
    render_res_x = int(argv[21])
    render_res_y = int(argv[22])

    init(import_ldraw, render_res_x, render_res_y)
    models_failed = []
    start_found = False
    with open(models_csv, 'r', encoding="utf-8") as file:
        csvfile = csv.reader(file)

        for line in csvfile:
            if not start_found:
                if line[0] == str(start_index):
                    start_found = True
                else:
                    continue
            part_id = line[1]
            reset_delete()
            valid = import_model(os.path.join(parts_dir, part_id + ".dat"), parts_dir)
            if not valid:
                models_failed.append(part_id)
                continue
            setup_render_scene()
            for j in range(1, num_renders_each + 1):
                setup_piece(colors=line[2], colors_dict=colors_dict, camera_min_x_rot=camera_min_x_rot,
                            camera_max_x_rot=camera_max_x_rot, camera_min_y_rot=camera_min_y_rot,
                            camera_max_y_rot=camera_max_y_rot, camera_zoom_min=camera_zoom_min,
                            camera_zoom_max=camera_zoom_max, flip_part=flip_part, random_spin=random_spin)
                render_image(part_id=part_id, output_dir=output_dir, num_renders_each=num_renders_each, number=j)
            if str(end_index) == line[0]:
                print(f"Models that failed: {models_failed}")
                print("Ending....")
                return


if __name__ == "__main__":
    main()
