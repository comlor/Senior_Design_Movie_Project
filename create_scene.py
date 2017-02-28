from jpl_config import FilePaths
import bpy
import bmesh
from bpy import context as C



class BuildScene:

    def __init__(self, points, path,name, in_obj, planetographic):
        self.path = path
        self.planetographic = planetographic

        # Get a object of the current scene
        self.scene = bpy.context.scene

        num_points = len(points)
        print("Number of points: " + str(num_points))
        self.eval_time = points[num_points - 1][0]

        self.points = self.inter(points)
        self.path.end_frame = len(self.points)
        self.set_end_frame()

    def inter(self, points):
        result = [] # [[points[0][0], points[0][1], points[0][2]], ]
        num_points = len(points)

        for pt in range(num_points):
            result.append([points[pt][1], points[pt][2], points[pt][3]])
            if pt + 1 < num_points:
                dif_x = points[pt + 1][1] - points[pt][1]
                dif_y = points[pt + 1][2] - points[pt][2]
                dif_z = points[pt + 1][3] - points[pt][3]
                print("dif_x: " + str(dif_x) + "   dif_y: " + str(dif_y) + "   dif_z: " + str(dif_z))
                offset = (points[pt + 1][0] - points[pt][0]) * 24
                print("offset: " + str(offset))
                delta_x = offset != 0 and dif_x / offset or dif_x
                delta_y = offset != 0 and dif_y / offset or dif_y
                delta_z = offset != 0 and dif_z / offset or dif_z
                print("delta_x: " + str(delta_x) + "   delta_y: " + str(delta_y) + "   delta_z: " + str(delta_z))
                new_x = points[pt][1]
                new_y = points[pt][2]
                new_z = points[pt][3]

                for i in range(offset):
                    new_x += delta_x
                    new_y += delta_y
                    new_z += delta_z
                    result.append([new_x, new_y, new_z])
        return result

    def set_end_frame(self):
        bpy.data.scenes["Scene"].frame_end = self.path.end_frame
        bpy.data.scenes["Scene"].frame_step = 1.0

    def create_lamp(self):
        # Create a new light source object as a sun
        lamp_data = bpy.data.lamps.new(name="Sun", type='SUN')

        # Create new object with our lamp datablock
        lamp_object = bpy.data.objects.new(name="Sun", object_data=lamp_data)

        # Link lamp object to the scene so it'll appear in this scene
        self.scene.objects.link(lamp_object)

        # Place lamp to a specified location
        lamp_object.location = (148.0, -100.0, 77.0)

        # Set the rotation of the lamp
        lamp_object.rotation_euler = (1.6, -0.82, 0.18)

        # Set lighting options so textures can be rendered and visible
        #lmp = bpy.data.lamps[lamp_data.name]
        #lmp.energy = self.path.energy
        #lmp.use_specular = False

    def create_camera(self):
        if self.planetographic is None:
            # Create a new camera object
            camera_data = bpy.data.cameras.new("MyCamera")

            # bpy.data.cameras['MyCamera'].CAMERA_MT_presets = self.path.get_camera_preset()

            # Create new object with the camera data
            camera_object = bpy.data.objects.new(name="MyCamera", object_data=camera_data)

            # Link camera to the scene
            self.scene.objects.link(camera_object)

            # Place camera to a specified location
            # camera_object.location = (150.0, -85.0, 100.0)
            print("camera x: " + str(self.points[0][0]))
            print("camera y: " + str(self.points[0][1]))
            print("camera z: " + str(self.points[0][2]))
            camera_object.location = (self.points[0][0], self.points[0][1], self.points[0][2])

            # Set the rotation of the camera
            camera_object.rotation_euler = (1.57, 0.0, 0.0)

            # Get new camera object we created
            cam = bpy.data.cameras[camera_data.name]

            # Set the focal length of the camera lens.  Zoom out(default 32)
            cam.lens = 10
        else:
            #TODO: do planetographic stuff here
            return

    def create_camera_path(self): # FAKE DATA ----- Change this to create path from given data
        if self.planetographic is None:
            # Create a new curve in 3D
            curve_data = bpy.data.curves.new('Camera_Path', type='CURVE')
            curve_data.dimensions = '3D'
            curve_data.resolution_u = 2

            # map coords to spline
            polyline = curve_data.splines.new('NURBS')
            polyline.points.add(self.path.end_frame)

            num = len(self.points)
            print("size; " + str(num))
            for p in range(len(self.points)):
                polyline.points[p].co = (self.points[p][0], self.points[p][1], self.points[p][2], 1)
            # ###########################
            # Test Data for Camera Path
            # ###########################
            # Creates a diagonal polyline path
            # x_pos = 150.0
            # y_pos = -85.0
            # z_pos = 100.0
            # for i in range(self.end_frame):
            #    polyline.points[i].co = (x_pos, y_pos, z_pos, 1)
            #    x_pos += 1
            #    z_pos += 3
            #############################

            print("length: " + str(len(self.points)))
            print("eval_time: " + str(self.eval_time))
            bpy.data.curves["Camera_Path"].path_duration = len(self.points)
            bpy.data.curves["Camera_Path"].eval_time = self.eval_time

            # Create a curve object with the name Camera_Path
            curve_object = bpy.data.objects.new('Camera_Path', curve_data)

            # Link path to the Scene
            self.scene.objects.link(curve_object)
        else:
            #TODO: do planetographic stuff
            return

    def create_key_frames(self): # Fake data ---- Should receive list and create keyframes from data
        # Set Key Frames ---- Currently breaks camera path binding
        bpy.data.scenes['Scene'].frame_current = 50
        bpy.data.curves['Camera_Path'].eval_time = 30
        bpy.data.curves['Camera_Path'].keyframe_insert(data_path='eval_time')

        bpy.data.scenes['Scene'].frame_current = 125
        bpy.data.curves['Camera_Path'].eval_time = 60
        bpy.data.curves['Camera_Path'].keyframe_insert(data_path='eval_time')

        bpy.data.scenes['Scene'].frame_current = 250
        bpy.data.curves['Camera_Path'].eval_time = 120
        bpy.data.curves['Camera_Path'].keyframe_insert(data_path='eval_time')

    def bind_camera_path(self):
        # Get Camera object
        camera = bpy.data.objects['MyCamera']
        # Get Camera_Path object
        path = bpy.data.objects['Camera_Path']

        # Set both Camera and Camera_Path object as selected
        camera.select = True
        path.select = True

        # Make objects active and set camera to follow camera path.
        bpy.context.scene.objects.active = path
        bpy.ops.object.parent_set(type='FOLLOW')  # follow path


    def new_reducer(self):
        myobject = bpy.data.objects['theMartianColor']
        myobject.select = True

        bpy.context.scene.objects.active = myobject

        me = bpy.context.object.data

        bm = bmesh.new()
        bm.from_mesh(me)

        location = C.object.delta_location
        dimension = C.object.dimensions

        for i in range(int(location[0]), int(dimension[0]), int(dimension[0] / 3)):
            ret = bmesh.ops.bisect_plane(bm, geom=bm.verts[:] + bm.edges[:] + bm.faces[:], plane_co=(i, 0, 0),
                                         plane_no=(1, 0, 0))
            bmesh.ops.split_edges(bm, edges=[e for e in ret['geom_cut'] if isinstance(e, bmesh.types.BMEdge)])

        for i in range(int(location[1]), int(dimension[1]), int(dimension[1] / 3)):
            ret = bmesh.ops.bisect_plane(bm, geom=bm.verts[:] + bm.edges[:] + bm.faces[:], plane_co=(0, i, 0),
                                         plane_no=(0, 1, 0))
            bmesh.ops.split_edges(bm, edges=[e for e in ret['geom_cut'] if isinstance(e, bmesh.types.BMEdge)])

        bm.to_mesh(me)
        bm.free()
        myobject.select = False


    def set_render_options(self):
        # Set Rendering Options
        bpy.data.scenes["Scene"].render.resolution_x = self.path.render_res_x
        bpy.data.scenes["Scene"].render.resolution_y = self.path.render_res_y
        bpy.data.scenes["Scene"].render.resolution_percentage = self.path.render_res_percent
        bpy.data.scenes["Scene"].render.use_border = self.path.use_border
        bpy.data.scenes["Scene"].render.use_raytrace = self.path.use_ray_trace
        bpy.data.scenes["Scene"].render.use_antialiasing = self.path.use_anti_aliasing
        bpy.data.scenes["Scene"].render.use_shadows = self.path.use_shadows
        bpy.data.scenes["Scene"].render.use_sss = self.path.use_sss
        bpy.data.scenes["Scene"].render.tile_x = self.path.render_tile_x
        bpy.data.scenes["Scene"].render.tile_y = self.path.render_tile_y
        bpy.data.scenes["Scene"].render.use_simplify = self.path.use_simplify
        bpy.data.scenes["Scene"].render.simplify_subdivision = self.path.simplify_subdivision
        bpy.data.scenes["Scene"].render.simplify_subdivision_render = self.path.simplify_subdivision_render

        # Set Lighting Options
        bpy.data.lamps["Sun"].shadow_method = self.path.shadow_method
        bpy.data.lamps["Sun"].shadow_soft_size = self.path.shadow_soft_size
        bpy.data.lamps["Sun"].shadow_ray_samples = self.path.shadow_ray_samples
        bpy.data.lamps["Sun"].use_specular = self.path.use_specular
        bpy.data.lamps["Sun"].energy = self.path.energy