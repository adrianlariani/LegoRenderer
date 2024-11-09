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

    init(import_ldraw)
    models_failed = []
    with open(models_csv, 'r', encoding="utf-8") as file:
        csvfile = csv.reader(file)
        for i in range(start_index + 1):
            next(csvfile)
        for line in csvfile:
            part_id = line[1]
            reset_delete()
            valid = import_model(os.path.join(parts_dir, part_id + ".dat"), parts_dir)
            if not valid:
                models_failed.append(part_id)
                continue
            setup_render_scene()
            for j in range(1, num_renders_each + 1):
                setup_piece(colors=line[2], colors_dict=colors_dict)
                render_image(part_id=part_id, output_dir=output_dir, num_renders_each=num_renders_each, number=j)
            if str(end_index) == line[0]:
                print(f"Models that failed: {models_failed}")
                print("Ending....")
                return


if __name__ == "__main__":
    main()
