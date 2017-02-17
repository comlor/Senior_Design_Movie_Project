import os
import bpy
import addon_utils


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

    def import_hirise_img(self):
        # Enable the HiRISE IMG Import Addon
        addon_utils.enable("io_convert_image_to_mesh_img")

        # Execute the addon to import the IMG file, additional options available for resolution and quality
        bpy.ops.import_shape.img(filepath="/home/chrisomlor/MovieDemo/Assets/my_image.IMG")

    '''def __create_material(self):
        active_object = bpy.context.active_object

        # Get material
        mat = bpy.data.materials.get("Material")
        if mat is None:
            # create material
            mat = bpy.data.materials.new(name="Material")

        # Assign it to object
        if active_object.data.materials:
            # assign to 1st material slot
            active_object.data.materials[0] = mat
        else:
            # no slots
            active_object.data.materials.append(mat)

        return mat

    def __create_texture(self):
        active_object = bpy.context.active_object

        if active_object:
            for mat_slot in active_object.material_slots:
                for tex_slot in mat_slot.material.texture_slots:
                    if tex_slot:
                        if

        tex = bpy.data.textures.get("Texture")

        if tex is None:
            tex = bpy.data.textures.new(name="Texture", type="IMAGE")
        else:
            tex.type = "IMAGE"
            tex.name = "Texture"

        return tex'''


    def import_collada(self):
        bpy.ops.wm.collada_import(filepath="/home/chrisomlor/MovieDemo/Assets/mars_sample.dae")
        bpy.ops.object.select_all(action='SELECT')

        #mat_obj = self.__create_material()
        #tex = self.__create_texture()

        #tex = bpy.data.textures.new(name="Texture", type="IMAGE")
        #slot = mat_obj.texture_slots.add()
        #slot.texture = tex
        #tex_img = bpy.data.images.load(filepath="/home/chrisomlor/MovieDemo/Assets/texture_cb.jpg")
        #tex.image = tex_img

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