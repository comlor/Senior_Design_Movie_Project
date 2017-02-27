import bpy
from osgeo import gdal, osr

class BuildScene:

    def __init__(self, blender_options, file_path, geo_pts, user_selections):
        self.__user_points = user_selections[0]
        self.__camera_orientation = user_selections[1]
        self.__blender_options = blender_options
        self.__file_path = file_path
        self.__geo_pts = geo_pts

        # Get Instance Object of the current blender scene
        self.__scene = bpy.context.scene

        self.__num_points = len(self.__user_points)

        self.__points = self.inter(self.__user_points)
        self.__eval_time = self.__user_points[self.__num_points - 1][0]
        self.set_end_frame(len(self.__points))

    # Linear Interpolation between each user selected point
    def inter(self, points):
        result = []
        num_points = len(points)

        for pt in range(num_points):
            result.append(self.geo_2_pix(points[pt][1], points[pt][2], points[pt][3]))
            if pt + 1 < num_points:
                dif_x = points[pt + 1][1] - points[pt][1]
                dif_y = points[pt + 1][2] - points[pt][2]
                dif_z = points[pt + 1][3] - points[pt][3]

                offset = (points[pt + 1][0] - points[pt][0]) * 24

                delta_x = dif_x / offset
                delta_y = dif_y / offset
                delta_z = dif_z / offset

                new_x = points[pt][1]
                new_y = points[pt][2]
                new_z = points[pt][3]

                for i in range(offset):
                    new_x += delta_x
                    new_y += delta_y
                    new_z += delta_z
                    result.append(self.geo_2_pix(new_x, new_y, new_z))

        return result

    # Convert GPS Lon/Lat to pixel coordinates in blender
    # Altitude needs work yet
    def geo_2_pix(self, x, y, z):
        img_scale = self.__file_path.get_IMG_scale()
        lon_origin = self.__geo_pts[2][0][0]
        lat_origin = self.__geo_pts[2][0][1]
        lon_max = self.__geo_pts[2][2][0]
        lat_max = self.__geo_pts[2][2][1]
        lon_proj = x
        lat_proj = y
        width = self.__geo_pts[0][2][0]
        height = self.__geo_pts[0][2][1]

        delta_lon = abs(lon_max - lon_origin)
        delta_lat = abs(lat_max - lat_origin)

        x_dpp = delta_lon / width
        y_dpp = delta_lat / height

        x_proj = ((lon_proj - lon_origin) / x_dpp) * img_scale
        y_proj = ((lat_proj - lat_origin) / y_dpp) * img_scale
        z_proj = z * img_scale

        return [x_proj, y_proj, z_proj]

    # Sets the end_frame inside blender and saves information in blender configuration
    # class variable for rendering tasks to use
    def set_end_frame(self, end_frame):
        self.__blender_options.set_end_frame(end_frame)
        bpy.data.scenes["Scene"].frame_end = end_frame
        bpy.data.scenes["Scene"].frame_step = 1.0

    # Creates a sun lamp.
    # Not scientifically accurate yet
    def create_lamp(self):
        # Create a new light source object as a sun
        lamp_data = bpy.data.lamps.new(name="Sun", type='SUN')

        # Create new object with our lamp datablock
        lamp_object = bpy.data.objects.new(name="Sun", object_data=lamp_data)

        # Link lamp object to the scene so it'll appear in this scene
        self.__scene.objects.link(lamp_object)

        # Place lamp to a specified location
        lamp_object.location = (148.0, -100.0, 77.0)

        # Set the rotation of the lamp
        lamp_object.rotation_euler = (1.6, -0.82, 0.18)

        # Set lighting options so textures can be rendered and visible
        #lmp = bpy.data.lamps[lamp_data.name]
        #lmp.energy = self.path.energy
        #lmp.use_specular = False

    # Creates a camera object and places at beginning of animation position
    # Camera rotation in quaternion mode but not taking specific data yet
    def create_camera(self):
        # Create a new camera object
        camera_data = bpy.data.cameras.new("MyCamera")

        # bpy.data.cameras['MyCamera'].CAMERA_MT_presets = self.path.get_camera_preset()

        # Create new object with the camera data
        camera_object = bpy.data.objects.new(name="MyCamera", object_data=camera_data)

        # Link camera to the scene
        self.__scene.objects.link(camera_object)

        # Place camera to a specified location
        # camera_object.location = (150.0, -85.0, 100.0)
        camera_object.location = (self.__points[0][0], self.__points[0][1], self.__points[0][2])

        # Set the rotation of the camera
        camera_object.rotation_mode = 'QUATERNION'
        camera_object.rotation_quaternion = (self.__camera_orientation[0][0], self.__camera_orientation[0][1],
                                             self.__camera_orientation[0][2], self.__camera_orientation[0][3])

        # Get new camera object we created
        cam = bpy.data.cameras[camera_data.name]

        # Set the focal length of the camera lens.  Zoom out(default 32)
        cam.lens = 10

    def create_camera_path(self): # FAKE DATA ----- Change this to create path from given data
        # Create a new curve in 3D
        curve_data = bpy.data.curves.new('Camera_Path', type='CURVE')
        curve_data.dimensions = '3D'
        curve_data.resolution_u = 2

        # map coords to spline
        polyline = curve_data.splines.new('NURBS')
        polyline.points.add(self.__blender_options.get_end_frame())

        for p in range(len(self.__points)):
            polyline.points[p].co = (self.__points[p][0], self.__points[p][1], self.__points[p][2], 1)

        bpy.data.curves["Camera_Path"].path_duration = len(self.__points)
        bpy.data.curves["Camera_Path"].eval_time = self.__eval_time

        # Create a curve object with the name Camera_Path
        curve_object = bpy.data.objects.new('Camera_Path', curve_data)

        # Link path to the Scene
        self.__scene.objects.link(curve_object)

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

    def set_camera_orientation(self):
        # Need to set keyframes at the frame where the users point is located.
        # Estimation based on T&E start rotation 20 frames before and end 20 frames after desired frame change
        # to make a smooth transition of camera
        # General Idea:
        # Insert keyframe 20 frames before desired frame
        # At 20 frames after change the orientation to desired rotation and insert second keyframe
        # Blender should create a smooth curve transition

        scene = bpy.context.scene
        scene.objects.active = bpy.data.objects['MyCamera']

        # Deselect All objects.  only camera can be selected for this
        bpy.ops.object.select_all(action='DESELECT')
        camera = bpy.data.objects['MyCamera']
        camera.select = True

        # Create camera object from our currently selected camera
        camera_object = bpy.context.active_object

        time_offsets = []
        for item in self.__user_points:
            time_offsets.append(item[0])

        for index in range(len(time_offsets)):
            frame = time_offsets[index] * 24

            if(frame == 0) or (frame == self.__blender_options.get_end_frame()):
                continue
            else:
                bpy.context.scene.frame_set(frame-10)
                camera_object.rotation_quaternion = (self.__camera_orientation[index-1][0],
                                                     self.__camera_orientation[index-1][1],
                                                     self.__camera_orientation[index-1][2],
                                                     self.__camera_orientation[index-1][3])
                camera_object.keyframe_insert(data_path='rotation_quaternion')

                bpy.context.scene.frame_set(frame+10)
                camera_object.rotation_quaternion = (self.__camera_orientation[index][0],
                                                     self.__camera_orientation[index][1],
                                                     self.__camera_orientation[index][2],
                                                     self.__camera_orientation[index][3])
                camera_object.keyframe_insert(data_path='rotation_quaternion')
