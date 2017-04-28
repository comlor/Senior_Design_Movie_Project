import bpy
#from osgeo import gdal, osr
#import random
#import mathutils
import math
#import numpy


class BuildScene:

    def __init__(self, blender_options, file_path, geo_pts, user_selections):
        # Scene Objects that will be created by this class
        self.__camera_object = None
        self.__sun_object = None
        self.__camera_path = None
        self.__curve_data = None
        self.__polyline = None
        self.__curve_object = None
        self.__scene = bpy.context.scene

        # Points Received from front end of camera path points
        self.__user_points = user_selections[0]

        # Camera rotations where index corresponds to same index from user_points
        # list positions [time_offset, x, y, z, w]
        self.__camera_orientation = user_selections[1]

        # Lighting Orientations
        self.__light_orientation = user_selections[2]

        # Lighting Position
        self.__light_position = user_selections[3]

        # Blender Configuration options object
        self.__blender_options = blender_options

        # File path object for file locations and use directories
        self.__file_path = file_path

        # GDAL data from meta data of dataset
        self.__geo_pts = geo_pts

        # Number of points the user has selected
        self.__num_points = len(self.__user_points)

    # Create camera path using vertices received from user and using linear interpolation to fille in the
    # path between the points.
    def camera_path(self):
        # Get user selected point into list converted to pixel coordinates in blender
        verts = []
        for pt in self.__user_points:
            verts.append(self.geo_2_pix(float(pt[1]), float(pt[2]), float(pt[3])))

        # Create a new curve in 3D
        self.__curve_data = bpy.data.curves.new('Camera_Path', type='CURVE')
        self.__curve_data.dimensions = '3D'
        self.__curve_data.resolution_u = 2

        # Set the path duration to the number of frames of the last time offset multiplied by the
        # number of frames per second of the animation.
        self.__curve_data.path_duration = float(self.__user_points[self.__num_points - 1][0]) * 24

        self.__polyline = self.__curve_data.splines.new('POLY')
        self.__polyline.points.add(len(verts)-1)

        for n, (x, y, z) in enumerate(verts):
            self.__polyline.points[n].co = (x, y, z, 1)

        self.__camera_path = bpy.data.objects.new('PATH', self.__curve_data)
        self.__scene.frame_end = float(self.__user_points[self.__num_points - 1][0]) * 24
        self.__curve_object = bpy.data.objects['PATH']

    # Create a camera object and place on scene in the starting location of the animation based on user
    # defined points
    def make_camera(self):
        bpy.ops.object.select_all(action='DESELECT')

        cxt = [x for x in bpy.context.screen.areas if x.type == 'VIEW_3D']

        if cxt:
            for v in cxt:
                v.spaces[0].transform_orientation = 'GIMBAL'

        # Create Empty for translating cesium camera rotations in blender
        cesium = bpy.data.objects.new( "cesium", None )
        bpy.context.scene.objects.link(cesium)
        cesium.empty_draw_type = 'CUBE'
        cesium.location = self.geo_2_pix(float(self.__user_points[0][1]), float(self.__user_points[0][2]), float(self.__user_points[0][3]))

        # Create Empty that is child of cesium empty.  This will handle the pitch and heading rotations
        # Rotations occur on the blender x, y axis
        pitch_heading = bpy.data.objects.new( "pitch_heading", None)
        bpy.context.scene.objects.link(pitch_heading)
        cesium.empty_draw_type = 'CUBE'
        cesium.location = self.geo_2_pix(float(self.__user_points[0][1]), float(self.__user_points[0][2]), float(self.__user_points[0][3]))
        pitch_heading.parent = cesium

        # Create the main camera that is child of pitch_heading empty.  The pitch and heading rotations are
        # handled by the parent empty.  The only rotation on this object is the roll on blenders z axis
        new_camera = bpy.data.cameras.new("MyCamera")
        my_camera = bpy.data.objects.new("MyCamera", new_camera)
        bpy.context.scene.objects.link(my_camera)
        my_camera.parent = pitch_heading

        cesium.rotation_mode = 'XYZ'
        cesium.rotation_euler = (90 * math.pi/180, 0, 0)
        cesium.lock_rotation[0] = True
        cesium.lock_rotation[1] = True
        cesium.lock_rotation[2] = True

        pitch_heading.rotation_mode = 'XYZ'
        pitch_heading.rotation_euler = (self.__camera_orientation[0][1] * (math.pi / 180), -1 * self.__camera_orientation[0][3] * (math.pi / 180), 0)
        pitch_heading.lock_rotation[2] = True

        my_camera.lock_rotation[0] = True
        my_camera.lock_rotation[1] = True
        my_camera.rotation_mode = 'ZYX'
        my_camera.rotation_euler = (0, 0, self.__camera_orientation[0][2] * ( math.pi / 180 ))
        my_camera.location = (0, 0, 0)

        self.__camera_object = cesium

        self.__camera_object.select = True

        # Create a constraint on the camera object to follow path and bind to the path created by
        # the camera_path() function.
        self.__camera_object.constraints.new('FOLLOW_PATH')
        self.__camera_object.constraints["Follow Path"].target = self.__camera_path
        self.__camera_object.constraints["Follow Path"].forward_axis = "FORWARD_Z"

    # Make the camera object a chile of the camera path object so the follow path constraint
    # makes camera follow along the path when animated.
    #def link_camera_path(self):
    #    #self.__scene.objects.link(self.__camera_path)
    #    self.__scene.objects.active = self.__camera_path
    #    self.__camera_path.select = True

    #    self.__scene.objects.link(self.__camera_object)

    #   start_loc = self.geo_2_pix(float(self.__user_points[0][1]), float(self.__user_points[0][2]), float(self.__user_points[0][3]))
    #    self.__camera_object.location = start_loc

    #    self.__camera_object.select = True

    # Using key frames and linear interpolation to set the timing between each user defined point
    # of the camera path
    def key_frame_camera(self):
        # Convert each user selected value to pixel coordinates in blender as a new list
        verts = []
        for pt in self.__user_points:
            verts.append(self.geo_2_pix(float(pt[1]), float(pt[2]), float(pt[3])))

        # Camera must be only active object or animation will not run properly.
        bpy.ops.object.select_all(action='DESELECT')
        self.__camera_object.select = True

        # Loop through all the point indexes(verts[]) and insert a key frame at the user selected point
        # after selected the appropriate frame in the animation that that point should represent.  This
        # allows to systematically determine how long the path should animate between any two given
        # points in the animation.
        num_points = len(verts)
        previous_frame = self.__user_points[0]
        current_frame_num = 0
        for point in range(num_points):
            current_frame_num += (float(self.__user_points[point][0]) - float(previous_frame[0])) * 24 + 1
            self.__camera_object.location = verts[point]
            self.__camera_object.keyframe_insert(data_path="location", frame=current_frame_num)
            previous_frame = self.__user_points[point]

        # After all key frames have been created.  Loop through all the key frames and set the interpolation
        # type to linear so that the camera follows the path explicitly.  Otherwise the animation will use
        # bezier as default create smooth curves.
        my_curve = self.__camera_object.animation_data.action.fcurves
        for curve in my_curve:
            for key in curve.keyframe_points:
                key.interpolation = 'LINEAR'

    # Sets the end_frame inside blender and saves information in blender configuration
    # class variable for rendering tasks to use
    def set_end_frame(self, end_frame):
        # Update the end_frame variable in jpl_conf.py for use in other classes
        self.__blender_options.set_end_frame(end_frame)

        # Set the scene values so the animation knows the last frame.
        bpy.data.scenes["Scene"].frame_end = end_frame
        bpy.data.scenes["Scene"].frame_step = 1.0

    # Convert GPS Lon/Lat to pixel coordinates in blender
    # Altitude needs work yet
    def geo_2_pix(self, x, y, z):
        # Retrience the scale of the imported mesh(default is 0.01)
        img_scale = self.__file_path.get_IMG_scale()

        # Get the values of the origin from the HiRise meta data
        lon_origin = self.__geo_pts[2][0][0]
        lat_origin = self.__geo_pts[2][0][1]

        # Get the Max Latitude and Longitude from the meta data using the bottom right corner of the HiRise IMG
        # The upper left corner is the origin in the projections
        lon_max = self.__geo_pts[2][2][0]
        lat_max = self.__geo_pts[2][2][1]

        # Set the value to be converted that is in GPS "Degree, Minutes, Seconds" -> Converted to a decimal value
        lon_proj = x
        lat_proj = y

        # Get the Pixel width and height of the HiRise IMG from the meta data.
        width = self.__geo_pts[0][2][0]
        height = self.__geo_pts[0][2][1]

        # Calculate the absolute value of the the total change in latitude and longitude values from max and origin
        delta_lon = abs(lon_max - lon_origin)
        delta_lat = abs(lat_max - lat_origin)

        # Calculate the degree per pixel(dpp) by dividing delta values by the width and height pixel values
        x_dpp = delta_lon / width
        y_dpp = delta_lat / height

        # Calculate the projection pixel values and multiply by the imported scale so the values are scaled
        # for the imported IMG size.  Without the img_scale this calculation assumes a 1-1 or 1.0 scale import
        x_proj = ((lon_proj - lon_origin) / x_dpp) * img_scale
        y_proj = ((lat_proj - lat_origin) / y_dpp) * img_scale
        z_proj = z * img_scale # Not scientifically accurate yet

        # Return a list of the pixel projected values.
        return [x_proj, y_proj, z_proj]

    # Creates a sun lamp.
    # Not scientifically accurate yet
    def create_lamp(self):
        # Create a new light source object as a sun
        lamp_data = bpy.data.lamps.new(name="Sun", type='SUN')
        lamp_data.use_nodes = True
        bpy.data.lamps["Sun"].node_tree.nodes["Emission"].inputs[1].default_value = 4.31 # Scientific approx 0.431 w/m^2

        # Create new object with our lamp datablock
        lamp_object = bpy.data.objects.new(name="Sun", object_data=lamp_data)

        # Link lamp object to the scene so it'll appear in this scene
        self.__scene.objects.link(lamp_object)

        # Place lamp to a specified location
        lamp_object.location = (self.__light_position[0][1],
                                self.__light_position[0][2],
                                self.__light_position[0][3])

        # Set the rotation of the lamp
        lamp_object.rotation_mode = 'QUATERNION'
        lamp_object.rotation_quaternion = (self.__light_orientation[0][1],
                                           self.__light_orientation[0][2],
                                           self.__light_orientation[0][3],
                                           self.__light_orientation[0][4])

    # Create camera rotations during animation by setting key frames a few frames before and after the
    # transition point and interpolating the rotation values to create a smooth rotational transition of
    # the cameras orientation
    def set_camera_orientation(self):
        self.key_frame_pitch()
        self.key_frame_roll()

    def key_frame_roll(self):
        scene = bpy.context.scene
        scene.objects.active = bpy.data.objects['MyCamera']

        # Deselect All objects.  only camera can be selected for this
        bpy.ops.object.select_all(action='DESELECT')
        camera = bpy.data.objects['MyCamera']
        camera.select = True

        # Create camera object from our currently selected camera
        camera_object = bpy.context.active_object


        # Get a list of the time offsets from the user selected data
        time_offsets = []
        for item in self.__user_points:
            time_offsets.append(float(item[0]))
        print("************************************************************")
        print(time_offsets)

        # For every time offset we create a key frame on the camera object 10 frames before and after each offset
        # so that the camera makes a smooth transition to the new rotation values.
        num_points = len(time_offsets)
        previous_frame = self.__camera_orientation[0]
        current_frame_num = 0
        for index in range(num_points):
            current_frame_num += (float(self.__camera_orientation[index][0]) - float(previous_frame[0])) * 24 + 1
            camera_object.rotation_euler = (0, 0, self.__camera_orientation[index][2] * (math.pi / 180))
            camera_object.keyframe_insert(data_path="rotation_euler", frame=current_frame_num)
            previous_frame = self.__user_points[index]

        '''
        for index in (range(len(time_offsets) - 1)):
            frame = time_offsets[index] * 24

            if(frame == 0) or (frame == self.__blender_options.get_end_frame()):
                continue
            else:
                #bpy.context.scene.frame_set(frame-10) # Need to change so finishes 1 frame before the offset
                bpy.context.scene.frame_set(frame)
                scene.objects.active = bpy.data.objects['MyCamera']
                camera_object.rotation_euler = (0, 0, self.__camera_orientation[index][2] * (math.pi/180))
                camera_object.keyframe_insert(data_path='rotation_euler')
                #bpy.context.scene.frame_set(frame+10)
                bpy.context.scene.frame_set(frame + (time_offsets[index + 1] * 24 - 1))
                camera_object.rotation_euler = (0, 0, self.__camera_orientation[index + 1][2] * (math.pi/180))
                camera_object.keyframe_insert(data_path='rotation_euler')
        '''

    def key_frame_pitch(self):
        scene = bpy.context.scene
        scene.objects.active = bpy.data.objects['pitch_heading']

        # Deselect All objects.  only camera can be selected for this
        bpy.ops.object.select_all(action='DESELECT')
        pitch = bpy.data.objects['pitch_heading']
        pitch.select = True

        # Create camera object from our currently selected camera
        pitch_object = bpy.context.active_object


        # Get a list of the time offsets from the user selected data
        time_offsets = []
        for item in self.__user_points:
            time_offsets.append(float(item[0]))

        # For every time offset we create a key frame on the camera object 10 frames before and after each offset
        # so that the camera makes a smooth transition to the new rotation values.
        num_points = len(time_offsets)
        previous_frame = self.__camera_orientation[0]
        current_frame_num = 0
        for index in range(num_points):
            current_frame_num += (float(self.__camera_orientation[index][0]) - float(previous_frame[0])) * 24 + 1
            pitch_object.rotation_euler = (self.__camera_orientation[index][1] * (math.pi / 180),
                                           -1 * self.__camera_orientation[index][3] * (math.pi / 180), 0)
            pitch_object.keyframe_insert(data_path="rotation_euler", frame=current_frame_num)
            previous_frame = self.__user_points[index]

        '''
        for index in range(len(time_offsets)-1):
            frame = time_offsets[index] * 24

            if(frame == 0) or (frame == self.__blender_options.get_end_frame()):
                continue
            else:
                #bpy.context.scene.frame_set(frame - 10)
                bpy.context.scene.frame_set(frame)
                scene.objects.active = bpy.data.objects['pitch_heading']
                pitch_object.rotation_euler = (self.__camera_orientation[index - 1][1] * (math.pi / 180),
                                               -1 *self.__camera_orientation[index - 1][3] * (math.pi / 180), 0)
                pitch_object.keyframe_insert(data_path='rotation_euler')
                #bpy.context.scene.frame_set(frame + 10)
                bpy.context.scene.frame_set(frame + (time_offsets[index+1] * 24 - 1))
                pitch_object.rotation_euler = (self.__camera_orientation[index][1] * (math.pi / 180),
                                               -1 * self.__camera_orientation[index][3] * (math.pi / 180), 0)
                pitch_object.keyframe_insert(data_path='rotation_euler')
        '''

    # Set the blender options of the Blender Internal Render Engine.  The values of these settings can be set
    # in the jpl_conf.py file.
    def set_render_options(self):
        # Set Rendering Options

        # Rendering Resolution
        bpy.data.scenes["Scene"].render.resolution_x = self.__blender_options.get_render_res_x()
        bpy.data.scenes["Scene"].render.resolution_y = self.__blender_options.get_render_res_y()
        bpy.data.scenes["Scene"].render.resolution_percentage = self.__blender_options.get_render_res_percent()
        bpy.data.scenes["Scene"].render.use_border = self.__blender_options.get_use_border()
        bpy.data.scenes["Scene"].render.use_crop_to_border = self.__blender_options.get_crop_to_border()

        # Render Shading
        bpy.data.scenes["Scene"].render.use_raytrace = self.__blender_options.get_use_ray_trace()
        bpy.data.scenes["Scene"].render.alpha_mode = self.__blender_options.get_alpha_mode()
        bpy.data.scenes["Scene"].render.use_shadows = self.__blender_options.get_use_shadows()
        bpy.data.scenes["Scene"].render.use_sss = self.__blender_options.get_sss()

        # Render Performance
        bpy.data.scenes["Scene"].render.tile_x = self.__blender_options.get_render_tile_x()
        bpy.data.scenes["Scene"].render.tile_y = self.__blender_options.get_render_tile_y()
        bpy.data.scenes["Scene"].render.raytrace_method = self.__blender_options.get_ray_trace_method()
        bpy.data.scenes["Scene"].render.octree_resolution = self.__blender_options.get_octree_resolution()

        # Render Anti Aliasing
        bpy.data.scenes["Scene"].render.use_antialiasing = self.__blender_options.get_use_anti_aliasing()
        bpy.data.scenes["Scene"].render.antialiasing_samples = self.__blender_options.get_anti_aliasing_samples()

        # Render Simplify
        bpy.data.scenes["Scene"].render.use_simplify = self.__blender_options.get_use_simplify()
        bpy.data.scenes["Scene"].render.simplify_subdivision = self.__blender_options.get_simplify_subdivision()
        bpy.data.scenes["Scene"].render.simplify_subdivision_render = \
            self.__blender_options.get_simplify_subdivision_render()

        bpy.data.scenes["Scene"].view_settings.view_transform = self.__blender_options.get_view_render_color()

    # Set the blender options of the Lighting Configurations.  The values of these settings. can be set
    # in the jpl_conf.py file.
    def set_lighting_options(self):
        # Set Lighting Options
        bpy.data.lamps["Sun"].shadow_method = self.__blender_options.get_shadow_method()
        bpy.data.lamps["Sun"].shadow_soft_size = self.__blender_options.get_shadow_soft_size()
        bpy.data.lamps["Sun"].shadow_ray_samples = self.__blender_options.get_shadow_ray_samples()
        bpy.data.lamps["Sun"].use_specular = self.__blender_options.get_use_specular()
        bpy.data.lamps["Sun"].energy = self.__blender_options.get_light_energy()

    def set_cycles_options(self):
        # Set Render Engine to Cycles
        bpy.data.scenes["Scene"].render.engine = self.__blender_options.get_render_engine()
        bpy.data.scenes["Scene"].view_settings.view_transform = self.__blender_options.get_view_render_color()

        # Rendering Resolution
        bpy.data.scenes["Scene"].render.resolution_x = self.__blender_options.get_render_res_x()
        bpy.data.scenes["Scene"].render.resolution_y = self.__blender_options.get_render_res_y()
        bpy.data.scenes["Scene"].render.resolution_percentage = self.__blender_options.get_render_res_percent()
        bpy.data.scenes["Scene"].render.use_border = self.__blender_options.get_use_border()
        bpy.data.scenes["Scene"].render.use_crop_to_border = self.__blender_options.get_crop_to_border()

        # Render Performance
        bpy.data.scenes["Scene"].render.tile_x = self.__blender_options.get_render_tile_x()
        bpy.data.scenes["Scene"].render.tile_y = self.__blender_options.get_render_tile_y()

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

        #lighting
        bpy.data.lamps["Sun"].shadow_soft_size = self.__blender_options.get_shadow_soft_size()
        bpy.data.lamps["Sun"].cycles.max_bounces = 16
        bpy.data.lamps["Sun"].cycles.cast_shadow = False
        bpy.data.lamps["Sun"].cycles.use_multiple_importance_sampling = False
