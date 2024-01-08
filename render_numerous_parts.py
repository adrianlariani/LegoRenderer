import sys
import os
from init import *
from render_part import import_model, setup_render_scene, setup_piece, render_image
from reference_obtainers import reset_delete


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
    with open(models_csv, 'r', encoding="utf-8") as file:
        csvfile = csv.reader(file)
        for i in range(start_index + 1):
            next(csvfile)
        for line in csvfile:

            part_id = line[1]
            reset_delete()
            import_model(os.path.join(parts_dir, part_id + ".dat"), parts_dir)
            setup_render_scene()
            for j in range(1, num_renders_each + 1):
                setup_piece(colors=line[2], colors_dict=colors_dict)
                render_image(part_id=part_id, output_dir=output_dir, num_renders_each=num_renders_each, number=j)
            if str(end_index) == line[0]:
                print("Ending....")
                return


if __name__ == "__main__":
    main()
