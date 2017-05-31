import sys
import bpy
from jpl_conf import Blender_Config_Options
from jpl_conf import FilePaths
import math
from subprocess import call


blender_options = Blender_Config_Options()
# Set Render Engine to Cycles
bpy.data.scenes["Scene"].render.engine = blender_options.get_render_engine()

bpy.data.scenes["Scene"].view_settings.view_transform = blender_options.get_view_render_color()

# Rendering Resolution
bpy.data.scenes["Scene"].render.resolution_x = blender_options.get_render_res_x()
bpy.data.scenes["Scene"].render.resolution_y = blender_options.get_render_res_y()
bpy.data.scenes["Scene"].render.resolution_percentage = blender_options.get_render_res_percent()
bpy.data.scenes["Scene"].render.use_border = blender_options.get_use_border()
bpy.data.scenes["Scene"].render.use_crop_to_border = blender_options.get_crop_to_border()

# Render Performance
bpy.data.scenes["Scene"].render.tile_x = blender_options.get_render_tile_x()
bpy.data.scenes["Scene"].render.tile_y = blender_options.get_render_tile_y()

bpy.data.scenes["Scene"].cycles.seed = 0
bpy.data.scenes["Scene"].cycles.samples = 16
bpy.data.scenes["Scene"].cycles.preview_samples = 16
bpy.data.scenes["Scene"].cycles_curves.use_curves = True
bpy.data.scenes["Scene"].cycles_curves.cull_backfacing = True
bpy.data.scenes["Scene"].cycles.max_bounces = 8
bpy.data.scenes["Scene"].cycles.min_bounces = 4
bpy.data.scenes["Scene"].cycles.diffuse_bounces = 0
bpy.data.scenes["Scene"].cycles.glossy_bounces = 1
bpy.data.scenes["Scene"].cycles.transmission_bounces = 2
bpy.data.scenes["Scene"].cycles.volume_bounces = 0
bpy.data.scenes["Scene"].cycles.use_transparent_shadows = True
bpy.data.scenes["Scene"].cycles.caustics_reflective = False
bpy.data.scenes["Scene"].cycles.caustics_refractive = False
bpy.data.scenes["Scene"].render.use_motion_blur = False
bpy.data.scenes["Scene"].cycles.debug_use_spatial_splits = True
bpy.data.scenes["Scene"].render.use_simplify = True
bpy.data.scenes["Scene"].render.simplify_subdivision_render = 1
bpy.data.scenes["Scene"].cycles.use_camera_cull = True

# bpy.data.scenes["terrain"].cycles.use_camera_cull = True


bpy.data.lamps["MySun"].shadow_soft_size = blender_options.get_shadow_soft_size()
bpy.data.lamps["MySun"].cycles.max_bounces = 16
bpy.data.lamps["MySun"].cycles.cast_shadow = False
bpy.data.lamps["MySun"].cycles.use_multiple_importance_sampling = False

print("System Args: ")
print(str(sys.argv))

input = sys.argv[-3:]

print("INPUT: ____ : " + str(input))

start, end, rid = input[0], input[1], input[2]

file_path = FilePaths()

bpy.context.scene.camera = bpy.data.objects['MyCamera']
# Get the scene context to render
scene = bpy.context.scene

# Directory path to store rendered frames
fp = file_path.get_job_dir() + str(rid) + "/temp/"
print(str(fp))

# Define render file format
scene.render.image_settings.file_format = 'PNG'  # set output format to .png


def num_padding(x, y):
    value = ''
    for i in range((int((math.log(float(x), 10)))) - (int((math.log(float(y), 10)))) + 1):
        print(str(int(math.log(float(x), 10))) + '   --   ' + str(int(math.log(float(y), 10))))
        value += '0'
    return value


# Render each frame individually
for frame_nr in range(int(start), int(end) + 1, 1):
    # Select the current frame
    scene.frame_set(frame_nr)

    # Set output location and filename
    scene.render.filepath = fp + 'part' + num_padding(end,
                                                      (1 if (frame_nr == 0) else frame_nr)) + str(frame_nr)
    # scene.render.filepath = fp + 'part' + str(frame_nr)

    # Render the frame to a still image
    bpy.ops.render.render(write_still=True)

