# Render images
# blender test.blend --background -t 0 --python /Users/chrisomlor/PycharmProjects/objload/render.py

import bpy
from math import radians
import blend_render_info

# Path to blend file created by OBJ_import.py
filepath = '/Users/chrisomlor/test.blend'

# Read .blend file header to get frame data
data = blend_render_info.read_blend_rend_chunk(filepath)

# calculate the frame count
frame_count = (data[0][1]) - (data[0][0]) + 1

# Display the number of frames
print("total frames:", (data[0][1] - data[0][0]) + 1)

# Set the camera object for the scene
bpy.context.scene.camera = bpy.data.objects['Camera']

# Get the scene context to render
scene = bpy.context.scene

# Directory path to store rendered frames
fp = '/Users/chrisomlor/MovieDemo/temp/'

# Define render file format
scene.render.image_settings.file_format = 'PNG' # set output format to .png

# Render each frame individually
for frame_nr in range(10):#(frame_count):

    # Select the current frame
    scene.frame_set(frame_nr)

    # Set output location and filename
    scene.render.filepath = fp + str(frame_nr)

    # Render the frame to a still image
    bpy.ops.render.render(write_still=True)

# Reset file path for rendering
scene.render.filepath = fp

