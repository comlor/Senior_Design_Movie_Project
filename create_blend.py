import os
import bpy, bmesh
import addon_utils
import math
from bpy import context as C


class Import_OBJ:

    def __init__(self, path, out_file,camera_cone):
        self.path = path
        self.out_file = out_file
        self.camera_cone = camera_cone

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

    def create_blender_object(self):
        return



'''
@Param: split_count: this variable refers to how many times the mesh will be split. Default to 3
@Param: terrain: this is a string that refers to the name of the terrain that will be getting split
'''
    def split(self,splits=3,terrain=""):
        ob = bpy.data.objects.get(terrain)
        ob.select = True
        bpy.context.scene.objects.active = ob
        bpy.ops.object.mode_set(mode='EDIT')

        bm = bmesh.from_edit_mesh(ob.data)

        edges = []

        location = C.object.delta_location
        dimension = C.object.dimensions

        for i in range(int(location[0]), int(dimension[0]), int(dimension[0] / splits)):
            ret = bmesh.ops.bisect_plane(bm, geom=bm.verts[:] + bm.edges[:] + bm.faces[:], plane_co=(i, 0, 0),
                                         plane_no=(1, 0, 0))
            bmesh.ops.split_edges(bm, edges=[e for e in ret['geom_cut'] if isinstance(e, bmesh.types.BMEdge)])

        for i in range(int(location[1]), int(dimension[1]), int(dimension[1] / splits)):
            ret = bmesh.ops.bisect_plane(bm, geom=bm.verts[:] + bm.edges[:] + bm.faces[:], plane_co=(0, i, 0),
                                         plane_no=(0, 1, 0))
            bmesh.ops.split_edges(bm, edges=[e for e in ret['geom_cut'] if isinstance(e, bmesh.types.BMEdge)])

        bmesh.update_edit_mesh(C.object.data)

        bpy.ops.mesh.separate(type='LOOSE')
        bpy.ops.object.mode_set(mode='OBJECT')
        self.select_object()


    def initialize_lod(self, terrain=""):
        for ob in bpy.context.selected_objects:
            if ob.type == 'MESH' and bpy.ops.object.select_pattern(pattern=terrain):
                dm = ob.modifiers.new('Decimate', 'DECIMATE')
                dm.ratio = 0.2

    def update_lod(self, CameraCone):


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