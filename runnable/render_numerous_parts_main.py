import math
import os
from blender_scripts.run_blender import run_blender


def render_many_models(blender, script, model_files, colors_rgb, ldraw_import, output_location,
                       confirmed_models_csv, start_index, end_index, num_renders_each, camera_min_x_rot,
                       camera_max_x_rot, camera_min_y_rot, camera_max_y_rot, camera_zoom_min,
                       camera_zoom_max, flip_part, random_spin):
    run_blender([blender,
                 "--background",
                 "--python", script,
                 "--",
                 model_files,
                 colors_rgb,
                 ldraw_import,
                 output_location,
                 confirmed_models_csv,
                 str(start_index),
                 str(end_index),
                 str(num_renders_each),
                 str(camera_min_x_rot),
                 str(camera_max_x_rot),
                 str(camera_min_y_rot),
                 str(camera_max_y_rot),
                 str(camera_zoom_min),
                 str(camera_zoom_max),
                 str(int(flip_part)),
                 str(int(random_spin))])


def main():
    render_many_models(blender="C:\\Program Files\\Blender Foundation\\Blender 3.6\\blender.exe",
                       script=os.path.join("..", "blender_scripts", "render_numerous_parts.py"),
                       model_files=os.path.abspath("../complete/ldraw/parts"),
                       colors_rgb=os.path.abspath("../assets/colors_rgb.csv"),
                       ldraw_import=os.path.abspath("../importldraw.zip"),
                       confirmed_models_csv=os.path.abspath("../assets/top1000models.csv"),
                       output_location=os.path.abspath("C:\\Renders"),
                       start_index=22,  # Index to start on, indexes of pieces in confirmed_models.csv
                       end_index=112,  # Index to end on, indexes of pieces in confirmed_models.csv
                       num_renders_each=10,  # Number of renders to produce for each piece
                       camera_min_x_rot=(-math.pi / 5),  # Minimum camera x rotation
                       camera_max_x_rot=(math.pi / 5),  # Maximum camera x rotation
                       camera_min_y_rot=(-math.pi / 5),  # Minimum camera y rotation
                       camera_max_y_rot=(math.pi / 5),  # Maximum camera y rotation
                       camera_zoom_min=30,  # Minimum camera zoom
                       camera_zoom_max=40,  # Maximum camera zoom
                       flip_part=True,  # True to flip part upside down randomly, or False otherwise
                       random_spin=True)  # True to spin part randomly on vertical axis, or False otherwise


if __name__ == "__main__":
    main()
