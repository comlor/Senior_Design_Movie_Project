# Animate the rendered stills
# blender test.blend --background --python /Users/chrisomlor/PycharmProjects/objload/animate.py

import bpy
import os

# Directory where rendered stills are located
in_dir = "./temp"

# Get list of frames from directory
lst = os.listdir(in_dir)

# Set output directory to save final video
out_dir = "./"

# Define resolution for video
resx = 720;  # 1920
resy = 480;  # 1080
bpy.data.scenes["Scene"].render.resolution_x = resx
bpy.data.scenes["Scene"].render.resolution_y = resy
bpy.data.scenes["Scene"].render.resolution_percentage = 100

# Filter file list by valid file types.
candidates = []
c = 0
for item in lst:
    fileName, fileExtension = os.path.splitext(lst[c])
    if fileExtension == ".png":
        candidates.append(item)
    c = + 1


file = [{"name": i} for i in candidates]
n = len(file)
print(n)

def find_sequencer_area():
    screens = [bpy.context.screen] + list(bpy.data.screens)
    for screen in screens:
        for area in screen.areas:
            if area.type == 'SEQUENCE_EDITOR':
                return area

    # If that still doesn't work, I don't know what will
    return area


a = bpy.ops.sequencer.image_strip_add({'area': find_sequencer_area()}, directory=in_dir, filter_blender=False,
                                      filter_image=True, filter_movie=False,
                                      filter_python=False, filter_font=False, filter_sound=False, filter_text=False,
                                      filter_btx=False, filter_collada=False,
                                      filter_folder=True, filemode=9, relative_path=False, frame_start=0,
                                      frame_end=n - 1,
                                      channel=1, replace_sel=True, files=file)
# (directory=in_dir, files=file, channel=1, frame_start=0, frame_end=n - 1)

stripname = file[0].get("name");
bpy.data.scenes["Scene"].frame_end = n
bpy.data.scenes["Scene"].render.image_settings.file_format = 'AVI_JPEG'
bpy.data.scenes["Scene"].render.filepath = out_dir
bpy.ops.render.render(animation=True)

# Diagnostic to check whether the images were loaded
stripname = file[0].get("name");
print(bpy.data.scenes["Scene"].sequence_editor.sequences[stripname])
print(dir(bpy.data.scenes["Scene"].sequence_editor.sequences[stripname]))