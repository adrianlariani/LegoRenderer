import os
from blender_scripts.run_blender import run_blender

def render_many_models(blender, script, model_files, colors_rgb, ldraw_import, output_location,
                       confirmed_models_csv, start_index, end_index, num_renders_each):
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
                 str(num_renders_each)])


def main():
    render_many_models(blender="C:\\Program Files\\Blender Foundation\\Blender 3.6\\blender.exe",
                       script=os.path.join("..", "blender_scripts", "render_numerous_parts.py"),
                       model_files=os.path.abspath("../complete/ldraw/parts"),
                       colors_rgb=os.path.abspath("../assets/colors_rgb.csv"),
                       ldraw_import=os.path.abspath("../importldraw.zip"),
                       output_location=os.path.abspath("C:\\Renders"),
                       confirmed_models_csv=os.path.abspath("../assets/confirmed_models.csv"),
                       start_index=244,  # Index to start on, indexes of pieces in confirmed_models.csv
                       end_index=246,  # Index to end on, indexes of pieces in confirmed_models.csv
                       num_renders_each=5)  # Number of renders to produce for each piece


if __name__ == "__main__":
    main()
