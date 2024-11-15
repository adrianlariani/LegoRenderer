import os
from blender_scripts.run_blender import run_blender


def render_one_model(blender, script, model_files, colors_rgb, ldraw_import, output_location, part_id, color):
    run_blender([blender,
                 "--background",
                 "--python", script,
                 "--",
                 model_files,
                 colors_rgb,
                 ldraw_import,
                 output_location,
                 part_id,
                 color])


def main():
    render_one_model(blender="C:\\Program Files\\Blender Foundation\\Blender 3.6\\blender.exe",
                     script=os.path.join("..", "blender_scripts", "render_part.py"),
                     model_files=os.path.abspath("../complete/ldraw/parts"),
                     colors_rgb=os.path.abspath("../assets/colors_rgb.csv"),
                     ldraw_import=os.path.abspath("../importldraw.zip"),
                     output_location=os.path.abspath("C://Renders"),
                     part_id="3001",  # Put Part Bricklink id here
                     color="Blue")  # Put color of brick here, colors can be found in colors_rgb.csv


if __name__ == "__main__":
    main()
