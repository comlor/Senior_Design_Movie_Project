import os
#import bpy

class FilePaths:

    def __init__(self, file_name, blend_file_name):
        # Absolute File Paths to working directories in project
        self.abs_project_dir = "/home/chrisomlor/MovieDemo"
        self.abs_temp_dir = "/home/chrisomlor/MovieDemo/temp/"
        self.abs_output_dir = "/home/chrisomlor/MovieDemo/"
        self.abs_obj_dir = "/home/chrisomlor/MovieDemo/Assets/"
        self.CZML_loc = "/home/chrisomlor/MovieDemo/Assets/"

        # File names for files in project
        self.img_filename = file_name
        self.CZML_filename = ""

        # Variable to hold absolute file path to Files used by program.  OBJ file exists, blend file is created
        # by this program`\#
        self.obj_file = os.path.join(self.abs_obj_dir, file_name)
        self.img_file = os.path.join(self.abs_obj_dir, self.img_filename)
        self.blend_file = blend_file_name


        # CAMERA CONFIGURATION OPTIONS
        self.camera_preset = 'Nikon D3100'

        # RENDER CONFIG
        self.end_frame = 100
        self.render_res_x = 1280
        self.render_res_y = 720
        self.render_res_percent = 50
        self.use_anti_aliasing = False
        self.use_shadows = False
        self.use_sss = False
        self.render_tile_x = 128
        self.render_tile_y = 128
        self.use_simplify = False
        self.simplify_subdivision = 2
        self.simplify_subdivision_render = 2
        self.use_border = False
        self.use_ray_trace = False

        # LIGHT CONFIG
        self.energy = 0.5
        self.use_specular = False
        self.shadow_method = "RAY_SHADOW"
        self.shadow_soft_size = 1.000
        self.shadow_ray_samples = 1

    def get_camera_preset(self):
        return self.camera_preset

    def set_blend_file(self, path):
        self.blend_file = path

    def get_blend_file(self):
        return os.path.join(self.abs_output_dir, self.blend_file)

    def obj_file(self):
        return self.obj_file

    def get_temp(self):
        return self.abs_temp_dir

    def get_output(self):
        return self.abs_output_dir

    def get_obj(self):
        return self.abs_obj_dir

    def get_relative_path(self, abs_path, start_path):
        return os.path.relpath(abs_path, start=start_path)
