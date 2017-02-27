import os

class FilePaths:

    def __init__(self, import_file, blend_file):
        # File Name to import
        self.__file_name = import_file

        # File Name of the blender file
        self.__blend_file_name = blend_file

        # Absolute File Path to project files
        self.__abs_project_dir = "/home/chrisomlor/MovieDemo/"

        # Absolute File Path to directory containing assets
        self.__abs_assets_dir = "/home/chrisomlor/MovieDemo/Assets/"

        # Absolute File Path to directory to save rendered stills to
        # This is a temp directory and contents will be deleted after job completion
        # to maintain disk space
        self.__abs_temp_dir = "/home/chrisomlor/MovieDemo/temp/"

        self.__IMG_binmode = "BIN12-FAST"
        self.__IMG_scale = 0.01

    ######################################################
    ###### Getters and Setters for Member Variables ######
    ######################################################
    def get_blend_file(self):
        return os.path.join(self.__abs_assets_dir, self.__blend_file_name)

    def get_import_file_name(self):
        return os.path.join(self.__abs_assets_dir, self.__file_name)

    def get_abs_path_project(self):
        return self.__abs_project_dir

    def get_abs_path_assets(self):
        return self.__abs_assets_dir

    def get_abs_path_temp(self):
        return self.__abs_temp_dir

    def set_abs_path_temp(self, temp_path):
        self.__abs_temp_dir = temp_path

    def set_abs_path_assets(self, assets_path):
        self.__abs_assets_dir = assets_path

    def set_abs_path_project(self, project_path):
        self.__abs_project_dir = project_path

    def set_blend_file_name(self, blend_file_name):
        self.__blend_file_name = blend_file_name

    def set_import_file_name(self, import_file_name):
        self.__file_name = import_file_name

    def get_IMG_scale(self):
        return self.__IMG_scale

    def get_IMG_binmode(self):
        return self.__IMG_binmode


class Blender_Config_Options:

    def __init__(self):
        # Camera Configurations Options
        self.__camera_preset = 'Nikon D3100'


        # Rendering Configuration Options
        self.__end_frame = 100
        self.__render_res_x = 1280
        self.__render_res_y = 720
        self.__render_res_percent = 50
        self.__use_anti_aliasing = False
        self.__use_shadows = False
        self.__use_sss = False
        self.__render_tile_x = 128
        self.__render_tile_y = 128
        self.__use_simplify = False
        self.__simplify_subdivision = 2
        self.__simplify_subdivision_render = 2
        self.__use_border = False
        self.__use_ray_trace = False

        # Lighting Configuration Options
        self.__energy = 0.5
        self.__use_specular = False
        self.__shadow_method = "RAY_SHADOW"
        self.__shadow_soft_size = 1.000
        self.__shadow_ray_samples = 1

    def set_end_frame(self, end_frame):
        self.__end_frame = end_frame

    def get_end_frame(self):
        return self.__end_frame

