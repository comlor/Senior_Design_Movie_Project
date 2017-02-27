import os
import bpy
import addon_utils

class Importer:

    def __init__(self, file_path):
        self.__file_path = file_path

    # Delete all default objects from blender so we have an
    # empty scene to work with.
    def clear_blend_file(self):
        # Delete all default objects from scene
        bpy.ops.object.select_all(action='SELECT')
        bpy.ops.object.delete(use_global=True)

    # Import Wavefront OBJ file into blender
    def import_obj_file(self):
        # Import the OBJ file specified in command into blender
        bpy.ops.import_scene.obj(filepath=self.__file_path.get_import_file_name())

    # Import HiRISE IMG file into blender
    def import_hirise_img(self, bin_mode='BIN12', scale="0.01"):
        # Enable the HiRISE IMG Import Addon
        addon_utils.enable("io_convert_image_to_mesh_img")
        print(self.__file_path.get_blend_file())
        # Execute the addon to import the IMG file, additional options available for resolution and quality
        bpy.ops.import_shape.img(filepath=self.__file_path.get_import_file_name(), bin_mode=bin_mode)

    # Import Collada DAE into blender
    def import_collada(self):
        bpy.ops.wm.collada_import(filepath=self.__file_path.get_import_file_name())
        bpy.ops.object.select_all(action='SELECT')

    # Deselects the object by name that was just imported
    # This needs to happen as it is selected by default and will
    # cause problems with camera animation if left selected.
    def select_object(self):
        bpy.ops.object.select_all(action='DESELECT')

    # Save the blend file with the new imported mesh
    def save_scene(self):
        save_loc = self.__file_path.get_abs_path_assets()
        save_file = self.__file_path.get_blend_file()
        save = os.path.join(save_loc, save_file)
        print("SAVE: " + save)
        bpy.ops.wm.save_as_mainfile(filepath=save)
