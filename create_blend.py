import os
import bpy


class Import_OBJ:

    def __init__(self, path, out_file):
        self.path = path
        self.out_file = out_file

    def clear_blend_file(self):
        # Delete all default objects from scene
        bpy.ops.object.select_all(action='SELECT')
        bpy.ops.object.delete(use_global=True)

    def import_obj_file(self):
        # Import the OBJ file specified in command into blender
        bpy.ops.import_scene.obj(filepath=self.path.obj_file)

    def select_object(self):
        # Deselects theMartianColor object name that was just imported
        # This needs to happen as it is selected by default and will
        # cause problems with camera animation if left selected.
        bpy.ops.object.select_all(action='DESELECT')

    def set_textured_view(self):
        # Set 3D View to textured so textures are displayed in .blend
        for area in bpy.context.screen.areas:  # iterate through areas in current screen
            if area.type == 'VIEW_3D':
                for space in area.spaces:  # iterate through spaces in current VIEW_3D area
                    if space.type == 'VIEW_3D':  # check if space is a 3D view
                        space.viewport_shade = 'TEXTURED'  # set the viewport shading to rendered

    def save_scene(self):
        save = os.path.join(self.path.abs_obj_dir, self.out_file)
        bpy.ops.wm.save_as_mainfile(filepath=save)