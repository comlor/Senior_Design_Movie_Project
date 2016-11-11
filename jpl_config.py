import os
import bpy

class FilePaths:

    def __init__(self, file_name):
        # FILE PATH OPTIONS
        self.abs_temp_dir = "/home/comlor/MovieDemo/temp/"
        self.abs_output_dir = "/home/comlor/MovieDemo/"
        self.abs_obj_dir = "/home/comlor/MovieDemo/"
        self.obj_file = os.path.join(self.abs_obj_dir, file_name) # Works to load the obj file
        self.blend_file = ''

        # CAMERA CONFIGURATION OPTIONS
        self.camera_preset = 'Nikon D3100'


        # RENDER CONFIG
        self.res_x = 1280
        self.res_y = 720
        self.res_percent = 50

        # LIGHT CONFIG
        self.energy = 0.5

    def get_camera_preset(self):
        return self.camera_preset

    def set_blend_file(self, path):
        self.blend_file = path

    def get_blend_file(self):
        return self.blend_file

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
