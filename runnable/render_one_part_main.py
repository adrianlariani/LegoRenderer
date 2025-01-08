import os
import math
from blender_scripts.run_blender import run_blender


def render_one_model(blender, script, model_files, colors_rgb, ldraw_import, output_location, part_id, color,
                     camera_x_rot, camera_y_rot, camera_zoom):
    run_blender([blender,
                 "--background",
                 "--python", script,
                 "--",
                 model_files,
                 colors_rgb,
                 ldraw_import,
                 output_location,
                 part_id,
                 color,
                 str(camera_x_rot),
                 str(camera_y_rot),
                 str(camera_zoom)])


def main():
    render_one_model(blender="C:\\Program Files\\Blender Foundation\\Blender 3.6\\blender.exe",
                     script=os.path.join("..", "blender_scripts", "render_part.py"),
                     model_files=os.path.abspath("../complete/ldraw/parts"),
                     colors_rgb=os.path.abspath("../assets/colors_rgb.csv"),
                     ldraw_import=os.path.abspath("../importldraw.zip"),
                     output_location=os.path.abspath("C:\\Renders"),
                     part_id="3003",  # Put Part Bricklink id here
                     color="Blue",  # Put color of brick here, colors can be found in colors_rgb.csv
                     camera_x_rot=(math.pi / 5),  # Camera x rotation
                     camera_y_rot=(math.pi / 5),  # Camera y rotation
                     camera_zoom=30)  # Camera zoom




if __name__ == "__main__":
    main()
