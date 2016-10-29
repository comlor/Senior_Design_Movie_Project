# Render images
# blender test.blend --background -t 0 --python /Users/chrisomlor/PycharmProjects/objload/render.py

import bpy
from math import radians
import blend_render_info

filepath = '/Users/chrisomlor/test.blend'
data = blend_render_info.read_blend_rend_chunk(filepath)
#frame_count = (data[0][1]) - (data[0][0]) + 1
print("total frames:", (data[0][1] - data[0][0]) + 1)

bpy.context.scene.camera = bpy.data.objects['Camera']
scene = bpy.context.scene
fp = '/Users/chrisomlor/MovieDemo/temp/'
#fp = scene.render.filepath # get existing output path
scene.render.image_settings.file_format = 'PNG' # set output format to .png

print(fp)

frames = 5

for frame_nr in range(10):#frame_count):

    # set current frame to frame 5
    scene.frame_set(frame_nr)

    # set output path so render won't get overwritten
    scene.render.filepath = fp + str(frame_nr)
    bpy.ops.render.render(write_still=True) # render still

# restore the filepath
scene.render.filepath = fp

#generate the rendered images here
#
#
#
#cam = bpy.context.scene.camera

#for area in bpy.context.screen.areas:
#    if area.type == 'VIEW_3D':
#        area.spaces[0].region_3d.view_perspective = 'CAMERA'

#step_count = 100

#for step in range(0, step_count):
#    cam.rotation_euler[2] = radians(step * (360.0 / step_count))

#    bpy.data.scenes["Scene"].render.filepath = '/Users/chrisomlor/MovieDemo/temp/vr_shot_%d.jpg' % step
#    bpy.ops.render.render(write_still=True)
