import os
#import bpy

class FilePaths:
    # Working Directory of current job.  Set dynamically by job.py
    cur_working_dir = ""
    IMG_binmode = "BIN12-FAST"
    IMG_scale = 0.01

    def __init__(self, import_file=None, blend_file=None, texture_file=None):
        # File Name to import
        self.__file_name = import_file

        # File Name of the blender file
        self.__blend_file_name = blend_file

        # File Name of Texture Image to use
        self.__texture_name = texture_file

        # Server Location to store job related files
        self.__job_dir = "/home/chrisomlor/MovieDemo/jobs/"

        # Absolute File Path to project files.  This will be directory on server where to find
        # all the python files such as this file.
        self.__abs_project_dir = "/home/chrisomlor/MovieDemo/"

        # Absolute File Path to directory containing assets.
        # This should point to directory where all DTM files located
        self.__img_dir = "/home/chrisomlor/MovieDemo/Assets/"

        # Absolute file path to directory containing texture file images
        self.__texture_dir = "/home/chrisomlor/MovieDemo/Assets/"

        # Hadoop Executable, if in system path just change to hadoop
        self.__hadoop_exec = "/usr/local/hadoop/bin/hadoop"

        # Blender Exececutable, if in system path just type blender
        self.__blender_exec = "/usr/lib/blender/blender"

        # Hadoop mapreduce streaming jar
        self.__hadoop_streaming = "/usr/local/hadoop/share/hadoop/tools/lib/hadoop-streaming-2.8.0.jar"

        # Output directory: where to save the final video rendered
        self.__final_output_dir = "/home/chrisomlor/MovieDemo/jobs/"

        # Log file location
        self._log_file = "/home/chrisomlor/MovieDemo/jobs/movie_log.txt"

        # Static value how to divide splitting of jobs.  This value will create splits on the number
        # of frames specified.  If the value is set at 60, this will create render jobs with 60 frames
        # each
        self.__render_frame_count = 60


    ######################################################
    ###### Getters and Setters for Member Variables ######
    ######################################################
    def log_events(self, line):
        f = open(self._log_file, "a")
        f.write(line)
        f.close()

    def get_render_count(self):
        return self.__render_frame_count

    def get_cur_working_dir(self):
        return self.cur_working_dir

    def set_cur_working_dir(self, cur_dir):
        self.cur_working_dir = cur_dir

    def get_hadoop_streaming(self):
        return self.__hadoop_streaming

    def get_final_output_dir(self):
        return self.__final_output_dir

    def get_job_dir(self):
        return self.__job_dir

    def get_blender_exec(self):
        return self.__blender_exec

    def get_hadoop_exec(self):
        return self.__hadoop_exec

    def get_blend_file(self):
        return self.__blend_file_name
        #return os.path.join(self.__cur_working_dir + "/assets/", self.__blend_file_name)

    def get_import_file_name(self):
        return os.path.join(self.__img_dir, self.__file_name)

    def get_texture_file(self):
        if self.__texture_name is not None:
            return os.path.join(self.__texture_dir, self.__texture_name)
        else:
            return None

    def get_abs_path_project(self):
        return self.__abs_project_dir

    def get_blend_file_name(self):
        return self.__blend_file_name

    def get_IMG_scale(self):
        return self.IMG_scale

    def get_IMG_binmode(self):
        return self.IMG_binmode

    def set_binmode(self, binmode):
        self.IMG_binmode = binmode


class Blender_Config_Options:
    end_frame = 100

    def __init__(self):
        # Object Variables
        # self.__scene = bpy.context.scene
        self.__terrain = ""

        # Global Configuration Options
        self.__interpolation_type = 'LINEAR'
        self.__add_on_names = ["io_convert_image_to_mesh_img", ]

        # Camera Configurations Options
        self.__camera_preset = 'Nikon D3100'
        self.__fps = 24

        # Material Options
        self.__specular_shader = "BLINN"
        self.__specular_intensity = 0.100
        self.__diffuse_shader = "LAMBERT"
        self.__diffuse_intensity = 0.700

        # World Options for rendering
        self.__use_ambient_occlusion = False

        # Lighting Configuration Options
        self.__energy = 0.65
        self.__use_specular = False
        self.__shadow_method = "RAY_SHADOW"
        self.__shadow_soft_size = 1.0
        self.__shadow_ray_samples = 1

        # Rendering Configuration Options
        self.__render_res_x = 1920
        self.__render_res_y = 1080
        self.__render_res_percent = 75
        self.__use_anti_aliasing = True
        self.__anti_aliasing_samples = '5'
        self.__use_shadows = True
        self.__use_sss = False
        self.__render_tile_x = 256
        self.__render_tile_y = 256
        self.__use_simplify = False
        self.__simplify_subdivision = 1
        self.__simplify_subdivision_render = 1
        self.__use_border = True
        self.__crop_to_border = True
        self.__use_ray_trace = True
        self.__alpha_mode = "TRANSPARENT"
        self.__ray_trace_method = "AUTO"
        self.__octree_resolution = '64'
        self.__use_local_coords = False
        self.__use_world_space_shading = False

        self.__view_transform = "Raw"

        #################################
        # Cycles Rendering
        # 'BLENDER_RENDER', 'BLENDER_GAME', 'CYCLES'
        self.__render_engine = 'CYCLES'


    ###############################################
    ##               CYCLES RENDERING            ##
    ###############################################

    def set_render_engine(self, engine):
        self.__render_engine = engine

    def get_render_engine(self):
        return self.__render_engine


    ###############################################
    ############  Rendering Options  ##############
    ###############################################
    def set_view_render_color(self, color):
        self.__view_transform = color

    def get_view_render_color(self):
        return self.__view_transform

    def set_alpha_mode(self, alpha):
        self.__alpha_mode = alpha

    def get_alpha_mode(self):
        return self.__alpha_mode

    def set_crop_to_border(self, crop):
        self.__crop_to_border = crop

    def get_crop_to_border(self):
        return self.__crop_to_border

    def set_anti_aliasing_samples(self, samples):
        self.__anti_aliasing_samples = samples

    def get_anti_aliasing_samples(self):
        return self.__anti_aliasing_samples

    def set_ray_trace_method(self, method):
        self.__ray_trace_method = method

    def get_ray_trace_method(self):
        return self.__ray_trace_method

    def set_octree_resolution(self, res):
        self.__octree_resolution = res

    def get_octree_resolution(self):
        return self.__octree_resolution

    def set_use_local_coords(self, local):
        self.__use_local_coords = local

    def get_use_local_coords(self):
        return self.__use_local_coords

    def set_world_space_shading(self, world_space):
        self.__use_world_space_shading = world_space

    def get_world_space_shading(self):
        return self.__use_world_space_shading

    def set_use_border(self, border):
        self.__use_border = border

    def get_use_border(self):
        return self.__use_border

    def set_use_ray_trace(self, ray_trace):
        self.__use_ray_trace = ray_trace

    def get_use_ray_trace(self):
        return self.__use_ray_trace

    def set_use_simplify(self, simplify):
        self.__use_simplify = simplify

    def get_use_simplify(self):
        return self.__use_simplify

    def set_simplify_subdivision(self, subdivide):
        self.__simplify_subdivision = subdivide

    def get_simplify_subdivision(self):
        return self.__simplify_subdivision

    def set_simplify_subdivision_render(self, subdivide_render):
        self.__simplify_subdivision_render = subdivide_render

    def get_simplify_subdivision_render(self):
        return self.__simplify_subdivision_render

    def set_render_res_x(self, res_x):
        self.__render_res_x = res_x

    def get_render_res_x(self):
        return self.__render_res_x

    def set_render_res_y(self, res_y):
        self.__render_res_y = res_y

    def get_render_res_y(self):
        return self.__render_res_y

    def set_render_res_percent(self, res_percent):
        self.__render_res_percent = res_percent

    def get_render_res_percent(self):
        return self.__render_res_percent

    def set_use_anti_aliasing(self, anti_alias):
        self.__use_anti_aliasing = anti_alias

    def get_use_anti_aliasing(self):
        return self.__use_anti_aliasing

    def set_use_shadows(self, use_shadows):
        self.__use_shadows = use_shadows

    def get_use_shadows(self):
        return self.__use_shadows

    def set_sss(self, sss):
        self.__use_sss = sss

    def get_sss(self):
        return self.__use_sss

    def set_render_tile_x(self, tile_x):
        self.__render_tile_x = tile_x

    def get_render_tile_x(self):
        return self.__render_tile_x

    def set_render_tile_y(self, tile_y):
        self.__render_tile_y = tile_y

    def get_render_tile_y(self):
        return self.__render_tile_y


    ###############################################
    #############  Lighting Options  ##############
    ###############################################
    def set_light_energy(self, energy):
        self.__energy = energy

    def get_light_energy(self):
        return self.__energy

    def set_use_specular(self, specular):
        self.__use_specular = specular

    def get_use_specular(self):
        return self.__use_specular

    def set_shadow_method(self, shadow):
        self.__shadow_method = shadow

    def get_shadow_method(self):
        return self.__shadow_method

    def set_shadow_soft_size(self, soft_size):
        self.__shadow_soft_size = soft_size

    def get_shadow_soft_size(self):
        return self.__shadow_soft_size

    def set_shadow_ray_samples(self, ray_samples):
        self.__shadow_ray_samples = ray_samples

    def get_shadow_ray_samples(self):
        return self.__shadow_ray_samples

    ###############################################
    #############   World Options   ###############
    ###############################################
    def set_ambient_occlusion(self, amb_occ):
        self.__use_ambient_occlusion = amb_occ

    def get_ambient_occlusion(self):
        return self.__use_ambient_occlusion

    ###############################################
    #############   Object Options   ##############
    ###############################################
    def set_terrain(self, terrain):
        self.__terrain = terrain

    def get_terrain(self):
        return self.__terrain

    def get_scene_object(self):
        return self.__scene

    ###############################################
    ###########   Animation Options   #############
    ###############################################
    def set_end_frame(self, end_frame):
        self.end_frame = end_frame

    def get_end_frame(self):
        return self.end_frame

    def set_fps(self, fps):
        self.__fps = fps

    def get_fps(self):
        return self.__fps

    def set_camera_preset(self, camera_preset):
        self.__camera_preset = camera_preset

    def get_camera_preset(self):
        return self.__camera_preset

    ###############################################
    #############  Material Options  ##############
    ###############################################
    def get_material_specular_shader(self):
        return self.__specular_shader

    def get_material_diffuse_shader(self):
        return self.__diffuse_shader

    def get_material_specular_intensity(self):
        return self.__specular_intensity

    def get_material_diffuse_intensity(self):
        return self.__diffuse_intensity

    ###############################################
    ###########  Global Configuratins  ############
    ###############################################
    def set_interpolation_type(self, interpolation_type):
        self.__interpolation_type = interpolation_type

    def get_interpolation_type(self):
        return self.__interpolation_type

    def set_add_ons_list(self, add_ons):
        self.__add_on_names.append(add_ons)

    def get_add_ons_list(self):
        return self.__add_on_names




