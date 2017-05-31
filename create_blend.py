import os
import bpy
import addon_utils
import bmesh
import math
from bpy import context as C
from mathutils import Vector
from bpy_extras.object_utils import world_to_camera_view


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
        # Execute the addon to import the IMG file,
        # #additional options available for resolution and quality
        bpy.ops.import_shape.img(filepath=self.__file_path.get_import_file_name(),
                                 bin_mode=bin_mode, scale=scale)

        # Rename the imported object to terrain so we know
        # the name in every scene created when the job split occurs
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
        mat_name = "Material"
        ob = self.returnObjectByName(self.__blender_config.get_terrain())
        ob.select = True
        bpy.context.scene.objects.active = ob

        # Get a reference to the materials in blender
        # Check to see if material exists and create a new on if no material is found
        mat = (bpy.data.materials.get(mat_name) or bpy.data.materials.new(mat_name))
        mat.use_nodes = True

        node_tree = mat.node_tree
        links = node_tree.links

        for n in node_tree.nodes:
            node_tree.nodes.remove(n)

        shader_output = node_tree.nodes.new(type='ShaderNodeOutputMaterial')
        shader = node_tree.nodes.new(type='ShaderNodeBsdfDiffuse')

        # Assign it to the imported object
        if ob.data.materials:
            # assign to 1st material slot
            ob.data.materials[0] = mat
        else:
            # no slots
            ob.data.materials.append(mat)

        links.new(shader.outputs[0], shader_output.inputs[0])

        textures = mat.texture_slots

        texture_file = self.__file_path.get_texture_file()

        if texture_file is not None:
            img = ''
            for tex in textures:
                if tex:
                    if tex.texture.type == 'IMAGE':
                        img = tex.texture.image
                        print(img.name)

            if not img:
                img = bpy.data.images.load(texture_file)

            shtext = node_tree.nodes.new('ShaderNodeTexImage')
            shtext.image = img

            links.new(shtext.outputs[0], shader.inputs[0])

            text_coord = node_tree.nodes.new('ShaderNodeTexCoord')
            links.new(text_coord.outputs['Generated'], shtext.inputs['Vector'])
        else:
            print("NO TEXTURE IMAGE --> SET COLOR")
            color = [0.800, 0.300, 0.017, 1.0]
            shader.inputs["Color"].default_value = color

    # Deselects the object by name that was just imported
    # This needs to happen as it is selected by default and will
    # cause problems with camera animation if left selected.
    def select_object(self):
        bpy.ops.object.select_all(action='DESELECT')

    # Save the blend file with the new imported mesh
    def save_scene(self, file_name):
        save_loc = self.__file_path.get_cur_working_dir() + "/assets/"
        save_file = self.__file_path.get_blend_file()
        save = save_loc + save_file
        print(str(save))
        bpy.ops.wm.save_as_mainfile(filepath=save)

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

    def split_terrain(self, split_count=10, terrain=""):
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
        splitx = int(x_val / split_count) == 0 and 1 or int(x_val / split_count)
        splity = int(y_val / split_count) == 0 and 1 or int(y_val / split_count)
        splitz = int(z_val / split_count) == 0 and 1 or int(z_val / split_count)

        print(location)
        print(dimension)
        print("Real Dimensions:X:" + str(x_val) + ",Y:" + str(y_val) + ",Z:" + str(
            z_val) + " " + "split_units:X:" + str(splitx) + ",Y:" + str(splity) + ",Z:" + str(splitz))
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
        print(r.name)
        return r

    def select_object(self):
        # Deselects theMartianColor object name that was just imported
        # This needs to happen as it is selected by default and will
        # cause problems with camera animation if left selected.
        bpy.ops.object.select_all(action='DESELECT')

    def update_on_visible(self, terrain=""):
        # tolerance is related to screen factor hard coded 0.03 for default
        # TODO: update this value based on screen factor
        tolerance = 0.03
        zlist = []
        for ob in bpy.context.scene.objects:
            if ob.type == 'MESH' and ob.name.startswith(terrain):
                mat_world = ob.matrix_world
                points = self.pointsOfMesh(ob)
                for point in points:
                    pointInView, z = self.testInView(mat_world * point, tolerance)
                    if pointInView:
                        zlist.append(ob.name)
                        # dm = ob.modifier_remove('DECIMATE')
        zlist = list(set(zlist))
        print(zlist)
        for ob in bpy.context.scene.objects:
            if ob.type == 'MESH' and ob.name.startswith(terrain):
                ob.select = True
                bpy.context.scene.objects.active = ob
                ob.modifiers["Decimate"].ratio = 0.1
                ob.modifiers["Mask"].show_render = True
                self.select_object()

        for ob in bpy.context.scene.objects:
            for i, val in enumerate(zlist):
                if ob.type == 'MESH' and ob.name.startswith(terrain):
                    if ob.name == val:
                        ob.select = True
                        bpy.context.scene.objects.active = ob
                        ob.modifiers["Decimate"].ratio = 0.9
                        ob.modifiers["Mask"].show_render = False
                        self.select_object()

    def is_visible(self, terrain=""):
        # tolerance is related to screen factor hard coded 0.03 for default
        # TODO: update this value based on screen factor
        tolerance = 0.03
        zlist = []
        for ob in bpy.context.scene.objects:
            if ob.type == 'MESH' and ob.name.startswith(terrain):
                mat_world = ob.matrix_world
                points = self.pointsOfMesh(ob)
                for point in points:
                    pointInView, z = self.testInView(mat_world * point, tolerance)
                    if pointInView:
                        zlist.append(ob.name)
                        # dm = ob.modifier_remove('DECIMATE')
        zlist = list(set(zlist))
        # print(zlist)
        return zlist

    def testInView(self, coord, tolerance):
        pointInView = False
        z = -1
        scene = bpy.context.scene
        camera = bpy.data.objects['MyCamera']
        if scene is not None and camera is not None and coord is not None:
            xFactor, yFactor, z = world_to_camera_view(scene, camera, coord)

            # add this if you use ortho !!!:
            if camera.data.type != "PERSPECTIVE":
                sx, sy = camera.data.shift_x, camera.data.shift_y
                xFactor, yFactor = xFactor - 2 * sx, yFactor - 2 * sy

            # !! tolerance can be computed with above z and radius or so
            if -tolerance < xFactor < 1 + tolerance and -tolerance < yFactor < 1 + tolerance and z > 0:
                pointInView = True

        return pointInView, z

    def pointsOfMesh(self, object):
        points = []
        if getattr(object, 'type', '') == 'MESH':
            points = [v.co for v in object.data.vertices]

        return points

        # this will run until the set of visible objects clears up or will stop at the last frame

    def get_Visible(self, start_frame=0, end_frame=0, terrain=""):
        s = []
        scene = bpy.context.scene
        print("Debug>" + str(start_frame) + " " + str(end_frame))
        for i in range(start_frame, end_frame):
            if i % 10 is 0:
                print("Debug>" + str(i))
                scene.frame_set(i)
                current = self.is_visible(terrain)
                s = s + current
                end_frame += 1;
                s = list(set(s))
                print("Visible Chunks: " + str(s) + "\nVisible Chunk Count:" + str(len(s)))
        return list(set(s))

    def set_cycles_options(self):
        # Set Render Engine to Cycles
        bpy.data.scenes["Scene"].render.engine = 'CYCLES'

        bpy.data.scenes["Scene"].view_settings.view_transform = "Raw"

        # Rendering Resolution
        bpy.data.scenes["Scene"].render.resolution_x = 1920
        bpy.data.scenes["Scene"].render.resolution_y = 1080
        bpy.data.scenes["Scene"].render.resolution_percentage = 75
        bpy.data.scenes["Scene"].render.use_border = True
        bpy.data.scenes["Scene"].render.use_crop_to_border = True

        # Render Performance
        bpy.data.scenes["Scene"].render.tile_x = 256
        bpy.data.scenes["Scene"].render.tile_y = 256

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

        bpy.data.lamps["Sun"].shadow_soft_size = 0.500
        bpy.data.lamps["Sun"].cycles.max_bounces = 16
        bpy.data.lamps["Sun"].cycles.cast_shadow = False
        bpy.data.lamps["Sun"].cycles.use_multiple_importance_sampling = False

    def set_end_frame(self, end_frame):
        bpy.data.scenes["Scene"].frame_end = int(end_frame)

    def set_start_frame(self, start_frame):
        bpy.data.scenes["Scene"].frame_start = int(start_frame)

    def save_new_scene_file(self, file_path, job_num):
        save_file = 'job_'
        save_file += str(job_num)
        save_file += '.blend'
        save = file_path + save_file
        print("SAVE FILE: ", str(save))
        bpy.ops.wm.save_as_mainfile(filepath=save)
        return save_file

    def create_job(self, start_frame=0, end_frame=0, file_path="", job_num=0, terrain="", active_file=""):
        self.set_start_frame(start_frame)
        self.set_end_frame(end_frame)
        #self.split_terrain(2, terrain)
        terrains = self.get_Visible(start_frame, end_frame, terrain)
        self.delete_terrain(terrain, terrains)
        self.combine_terrain(terrain)
        save_file = self.save_new_scene_file(file_path, job_num)
        save = os.path.join(file_path, active_file)
        bpy.ops.wm.open_mainfile(filepath=save)
        return save_file

    def delete_terrain(self, terrain="", terrains=[]):
        unused = []
        for ob in bpy.context.scene.objects:
            if ob.type == 'MESH' and ob.name.startswith(terrain):
                unused.append(ob.name)
        print("All Terrains: " + str(unused) + "\nVisible terrains:" + str(terrains))
        unused = list(set(unused) - set(terrains))
        print(unused)
        for ob in bpy.context.scene.objects:
            for i, val in enumerate(unused):
                if ob.type == 'MESH' and ob.name.startswith(terrain):
                    if ob.name == val:
                        print(ob.name)
                        ob.select = True
                        bpy.ops.object.delete()
                        self.select_object()

    def combine_terrain(self, terrain=""):
        bpy.ops.object.select_all(action='DESELECT')
        for ob in bpy.context.scene.objects:
            if ob.type == 'MESH' and ob.name.startswith(terrain):
                ob.select = True
                bpy.context.scene.objects.active = ob
        bpy.ops.object.join()
        self.select_object()

    def rename(self, terrain=""):
        bpy.ops.object.select_all(action='DESELECT')
        for ob in bpy.context.scene.objects:
            if ob.type == 'MESH' and ob.name.startswith(terrain):
                ob.select = True
                ob.name = terrain
        self.select_object()


    # Set material options in blender.  These values can be modified in the jpl_conf.py file.
    def set_material_option(self):
        bpy.data.materials["Material"].specular_shader = self.__blender_config.get_material_specular_shader()
        bpy.data.materials["Material"].diffuse_shader = self.__blender_config.get_material_diffuse_shader()
        bpy.data.materials["Material"].specular_intensity = self.__blender_config.get_material_specular_intensity()
        bpy.data.materials["Material"].diffuse_intensity = self.__blender_config.get_material_diffuse_intensity()
