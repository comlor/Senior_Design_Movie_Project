import os
import bpy
import addon_utils
import bmesh
from bpy import context as C
from mathutils import Vector

class Importer:

    def __init__(self, file_path, blender_config):
        self.__file_path = file_path
        self.__blender_config = blender_config

        self.__scene = bpy.context.scene
        self.__imported_obj = None

    # Delete all default objects from blender so we have an
    # empty scene to work with.
    def clear_blend_file(self):
        # Delete all default objects from scene
        bpy.ops.object.select_all(action='SELECT')
        bpy.ops.object.delete(use_global=True)

    # Import HiRISE IMG file into blender
    def import_hirise_img(self, bin_mode='BIN12', scale="0.01"):
        # Enable the HiRISE IMG Import Addon
        #addon_utils.enable("io_convert_image_to_mesh_img")

        #print(self.__file_path.get_blend_file())
        # Execute the addon to import the IMG file, additional options available for resolution and quality
        bpy.ops.import_shape.img(filepath=self.__file_path.get_import_file_name(), bin_mode=bin_mode, scale=scale)

        # Rename the imported object to terrain so we know the name in every scene created when the job split occurs
        for obj in bpy.context.selected_objects:
            obj.name = "terrain"
            self.__blender_config.set_terrain(obj.name)
            self.__imported_obj = obj

        ob = self.returnObjectByName("terrain")
        ob.select = True
        bpy.context.scene.objects.active = ob
        bpy.ops.object.mode_set(mode='EDIT')
        bpy.ops.mesh.flip_normals()
        bpy.ops.object.mode_set(mode='OBJECT')

        # Add material and texture to the DTM
        self.__add_texture()

    # Creates a material and texture for the imported HiRISE IMG
    def __add_texture(self):
        # Get an object reference to the imported object
        ob = self.returnObjectByName(self.__blender_config.get_terrain())

        # Get a reference to the materials in blender
        mat = bpy.data.materials['Material']

        # Check to see if material exists and create a new on if no material is found
        # by default blender does not add material so there should never be one at this point
        if mat is None:
            # create material
            mat = bpy.data.materials.new(name="Material")

        # Assign the new material to the imported object
        if ob.data.materials:
            # assign to 1st material slot
            ob.data.materials[0] = mat
        else:
            # no slots
            ob.data.materials.append(mat)
        '''
        # Get the absolute path to the texture image and load the image into blender
        tex_path = self.__file_path.get_texture_file()
        try:
            tex_image = bpy.data.images.load(tex_path)
        except:
            raise NameError("Cannot load image %s" % tex_path)

        # By default blender creates a texture for the material.  Due to an issue with the API, an image file cannot
        # be added to an existing texture, although the texture type can be set to image.  So to work around this,
        # the existing texture is deleted and a new one is created and assigned to the material with the image set.
        if bpy.data.textures["Tex"] is not None:
            bpy.data.textures.remove(bpy.data.textures["Tex"], do_unlink=True)
            slots = mat.texture_slots[0]
            new_tex = bpy.data.textures.new('mesh_texture', 'IMAGE')
            new_tex.image = tex_image
            slots.texture = new_tex
        '''

    # Deselects the object by name that was just imported
    # This needs to happen as it is selected by default and will
    # cause problems with camera animation if left selected.
    def select_object(self):
        bpy.ops.object.select_all(action='DESELECT')

    # Save the blend file with the new imported mesh
    def save_scene(self, file_name):
        self.__file_path.set_blend_file_name(file_name)
        save_loc = self.__file_path.get_abs_path_assets()
        save_file = self.__file_path.get_blend_file()
        save = os.path.join(save_loc, save_file)
        bpy.ops.wm.save_as_mainfile(filepath=save)

    def split_terrain_by_points(self, user_points, split_count=10, terrain=""):
        ob = self.returnObjectByName(terrain)
        ob.select = True
        bpy.context.scene.objects.active = ob
        bpy.ops.object.mode_set(mode='EDIT')

        bm = bmesh.from_edit_mesh(ob.data)

        location = C.object.location
        dimension = C.object.dimensions

        bbox_corners = [C.object.matrix_world * Vector(corner) for corner in C.object.bound_box]
        print("BBOX_CORNERS")
        print(bbox_corners)

        x_val = 0;
        y_val = 0;
        z_val = 0;

        # Get the correct bounds to account for negative since dimenions only push positives
        for vector_c in bbox_corners:
            v_x = int(vector_c[0])
            v_y = int(vector_c[1])
            v_z = int(vector_c[2])
            print(str(v_x) + " " + str(v_y) + " " + str(v_z))
            if int(dimension[0]) == abs(v_x):
                x_val = v_x
            if int(dimension[1]) == abs(v_y):
                y_val = v_y
            if int(dimension[2]) == abs(v_z):
                z_val = v_z;

        # Used in range must be an integer that isn't 0
        splity = int(y_val / split_count) == 0 and 1 or (int(y_val / 4 - 1))

        print("LOCATION")
        print(location)
        print("DIMENSION")
        print(dimension)
        print("Real Dimensions:X:" +
              str(x_val) + ",Y:" +
              str(y_val) + ",Z:" +
              str(z_val) + " " + "split_units Y:" + str(splity))

        if len(user_points) < 3:
            self.split_special(bm, location, y_val, splity)
        else:
            self.split_user_points(bm, user_points)

    def split_user_points(self, bm, user_points):
        for y in user_points:
            print("y: " + str(y[1]))
            ret = bmesh.ops.bisect_plane(bm, geom=bm.verts[:] + bm.edges[:] + bm.faces[:], plane_co=(0, y[1], 0),
                                         plane_no=(0, 1, 0))
            bmesh.ops.split_edges(bm, edges=[e for e in ret['geom_cut'] if isinstance(e, bmesh.types.BMEdge)])

        bmesh.update_edit_mesh(C.object.data)

        bpy.ops.mesh.separate(type='LOOSE')
        bpy.ops.object.mode_set(mode='OBJECT')

        self.select_object()

    def split_special(self, bm, location, y_val, num_splits):
        # Split mesh along the y-axis where the user points are selected
        for i in range(int(location[1]), y_val, num_splits):
            print("y: " + str(i))
            ret = bmesh.ops.bisect_plane(bm, geom=bm.verts[:] + bm.edges[:] + bm.faces[:], plane_co=(0, i, 0),
                                         plane_no=(0, 1, 0))
            bmesh.ops.split_edges(bm, edges=[e for e in ret['geom_cut'] if isinstance(e, bmesh.types.BMEdge)])

        bmesh.update_edit_mesh(C.object.data)

        bpy.ops.mesh.separate(type='LOOSE')
        bpy.ops.object.mode_set(mode='OBJECT')

        self.select_object()

    def split_terrain(self, split_count=6, terrain=""):
        ob = self.returnObjectByName(terrain)
        ob.select = True
        bpy.context.scene.objects.active = ob
        bpy.ops.object.mode_set(mode='EDIT')

        bm = bmesh.from_edit_mesh(ob.data)
        edges = []

        location = C.object.location
        dimension = C.object.dimensions

        bbox_corners = [C.object.matrix_world * Vector(corner) for corner in C.object.bound_box]
        print(bbox_corners)

        x_val = 0
        y_val = 0
        z_val = 0

        # Get the correct bounds to account for negative since dimenions only push positives
        for vector_c in bbox_corners:
            v_x = int(vector_c[0])
            v_y = int(vector_c[1])
            v_z = int(vector_c[2])
            print(str(v_x) + " " + str(v_y) + " " + str(v_z))
            if int(dimension[0]) == abs(v_x):
                x_val = v_x
            if int(dimension[1]) == abs(v_y):
                y_val = v_y
            if int(dimension[2]) == abs(v_z):
                z_val = v_z

        # Used in range must be an integer that isn't 0
        splitx = int(x_val / split_count) == 0 and 1 or int(x_val / split_count)
        splity = int(y_val / split_count) == 0 and 1 or int(y_val / split_count)
        splitz = int(z_val / split_count) == 0 and 1 or int(z_val / split_count)

        print(location)
        print(dimension)
        print(
            "Real Dimensions:X:" + str(x_val) + ",Y:" + str(y_val) + ",Z:" + str(z_val) + " " + "split_units:X:" + str(
                splitx) + ",Y:" + str(splity) + ",Z:" + str(splitz))
        # print(splitx + " " + splity)

        for i in range(int(location[0]), x_val, splitx):
            ret = bmesh.ops.bisect_plane(bm, geom=bm.verts[:] + bm.edges[:] + bm.faces[:], plane_co=(i, 0, 0),
                                         plane_no=(-1, 0, 0))
            bmesh.ops.split_edges(bm, edges=[e for e in ret['geom_cut'] if isinstance(e, bmesh.types.BMEdge)])

        for i in range(int(location[1]), y_val, splity):
            ret = bmesh.ops.bisect_plane(bm, geom=bm.verts[:] + bm.edges[:] + bm.faces[:], plane_co=(0, i, 0),
                                         plane_no=(0, 1, 0))
            bmesh.ops.split_edges(bm, edges=[e for e in ret['geom_cut'] if isinstance(e, bmesh.types.BMEdge)])

        bmesh.update_edit_mesh(C.object.data)

        bpy.ops.mesh.separate(type='LOOSE')
        bpy.ops.object.mode_set(mode='OBJECT')

        self.select_object()

    def returnObjectByName(self, passedName=""):
        r = None
        obs = bpy.data.objects
        for ob in obs:
            if ob.name == passedName:
                r = ob
        #print(r.name)
        return r

    def apply_mask(self, terrain=""):
        for ob in bpy.context.scene.objects:
            if ob.type == 'MESH' and ob.name.startswith(terrain):
                dm = ob.modifiers.new('Mask', 'MASK')

    def initialize_mask(self, invisObjects):
        for item in invisObjects:
            self.apply_mask(item)

    def initialize_lod(self, terrain=""):
        for ob in bpy.context.scene.objects:
            if ob.type == 'MESH' and ob.name.startswith(terrain):
                dm = ob.modifiers.new('Decimate', 'DECIMATE')
                dm.ratio = 0.02

    # Set material options in blender.  These values can be modified in the jpl_conf.py file.
    def set_material_option(self):
        bpy.data.materials["Material"].specular_shader = self.__blender_config.get_material_specular_shader()
        bpy.data.materials["Material"].diffuse_shader = self.__blender_config.get_material_diffuse_shader()
        bpy.data.materials["Material"].specular_intensity = self.__blender_config.get_material_specular_intensity()
        bpy.data.materials["Material"].diffuse_intensity = self.__blender_config.get_material_diffuse_intensity()
