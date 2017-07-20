import sys
import bpy
import time
from jpl_conf import Blender_Config_Options
from jpl_conf import FilePaths
import math
from subprocess import call

def timing(f):
    def wrap(*args):
        time1 = time.time()
        ret = f(*args)
        time2 = time.time()
        FilePaths().log_events('RENDER ------: %s function took %0.3f ms' % (f.__name__, (time2 - time1)*1000.0) + "\n")
    return wrap


@timing
def main():
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

    FilePaths().log_events("RENDER JOB\n")
    FilePaths().log_events("Args: " + str(sys.argv) + "\n")

    input = sys.argv[-3:]

    FilePaths().log_events("Input: " + str(input) + "\n")

    start, end, rid = int(input[0]), int(input[1]), str(input[2])
    max_frame = int(bpy.context.scene.frame_end)
    FilePaths().log_events("Maximum Frame: " + str(max_frame) + "\n")
    FilePaths().log_events("Start Frame: " + str(start) + "\n")
    FilePaths().log_events("End Frame: " + str(end) + "\n")
    FilePaths().log_events("Random ID: " + str(rid) + "\n")

    file_path = FilePaths()

    bpy.context.scene.camera = bpy.data.objects['MyCamera']
    # Get the scene context to render
    scene = bpy.context.scene

    # Directory path to store rendered frames
    fp = file_path.get_job_dir() + str(rid) + "/temp/"
    FilePaths().log_events("Rendered Stills Location: " + fp + "\n")

    # Define render file format
    scene.render.image_settings.file_format = 'PNG'  # set output format to .png
    FilePaths().log_events("Begin Rendering\n")
    while start <= end:
    	rendered = 'part' + str(start).zfill(math.ceil(math.log(float(max_frame), 10)) + 1)
    	scene.frame_set(int(start))
    	scene.render.filepath = fp + rendered
    	FilePaths().log_events("Rendering Frame: " + str(start) + " ---: " + str(fp + rendered) + "\n")
    	start += 1
    	bpy.ops.render.render(write_still=True)

        # Render the frame to a still image
    FilePaths().log_events("Rendering Job Complete\n")

if __name__ == "__main__":
    main()
