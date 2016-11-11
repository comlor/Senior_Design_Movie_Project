import os
import bpy
import blend_render_info


class FilePaths:

    def __init__(self, file_name):
        self.abs_temp_dir = "/home/jplmv/MovieDemo/temp/"
        self.abs_output_dir = "/home/jplmv/MovieDemo/"
        self.abs_obj_dir = "/home/jplmv/MovieDemo/"
        self.obj_file = os.path.join(self.abs_obj_dir, file_name) # Works to load the obj file
        self.blend_file = ''

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


class BuildScene:

    def __init__(self, end_frame):
        # Set value for last frame
        self.end_frame = end_frame
        # Get a object of the current scene
        self.scene = bpy.context.scene

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
        lmp = bpy.data.lamps[lamp_data.name]
        lmp.energy = 0.5
        lmp.use_specular = False

    def create_camera(self):
        # Create a new camera object
        camera_data = bpy.data.cameras.new("Camera")

        # Create new object with the camera data
        camera_object = bpy.data.objects.new(name="Camera", object_data=camera_data)

        # Link camera to the scene
        self.scene.objects.link(camera_object)

        # Place camera to a specified location
        camera_object.location = (150.0, -85.0, 100.0)

        # Set the rotation of the camera
        camera_object.rotation_euler = (1.57, 0.0, 0.0)

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
        polyline.points.add(self.end_frame)

        # ###########################
        # Test Data for Camera Path
        # ###########################
        # Creates a diagonal polyline path
        x_pos = 150
        y_pos = -85
        z_pos = 100
        for i in range(self.end_frame):
            polyline.points[i].co = (x_pos, y_pos, z_pos, 1)
            x_pos += 1
            z_pos += 3
        #############################

        # Create a curve object with the name Camera_Path
        curve_object = bpy.data.objects.new('Camera_Path', curve_data)

        # Link path to the Scene
        self.scene.objects.link(curve_object)

    def create_key_frames(self): # Fake data ---- Should receive list and create keyframes from data
        # Set Key Frames ---- Currently breaks camera path binding
        bpy.data.scenes['Scene'].frame_current = 50
        bpy.data.curves['Camera_Path'].eval_time = 150
        bpy.data.curves['Camera_Path'].keyframe_insert(data_path='eval_time')

        bpy.data.scenes['Scene'].frame_current = 125
        bpy.data.curves['Camera_Path'].eval_time = 225
        bpy.data.curves['Camera_Path'].keyframe_insert(data_path='eval_time')

        bpy.data.scenes['Scene'].frame_current = 250
        bpy.data.curves['Camera_Path'].eval_time = 250
        bpy.data.curves['Camera_Path'].keyframe_insert(data_path='eval_time')

    def bind_camera_path(self):
        # Get Camera object
        camera = bpy.data.objects['Camera']
        # Get Camera_Path object
        path = bpy.data.objects['Camera_Path']

        # Set both Camera and Camera_Path object as selected
        camera.select = True
        path.select = True

        # Make objects active and set camera to follow camera path.
        bpy.context.scene.objects.active = path
        bpy.ops.object.parent_set(type='FOLLOW')  # follow path

    def set_render_options(self):
        # Set scene render data
        for scene in bpy.data.scenes:
            scene.render.resolution_x = 1280
            scene.render.resolution_y = 720
            scene.render.resolution_percentage = 50
            scene.render.use_border = False
            scene.render.use_raytrace = False


class RenderStills:

    def __init__(self, path):
        self.path = path

    def get_frame_count(self):
        # Read .blend file header to get frame data
        data = blend_render_info.read_blend_rend_chunk(self.path.get_blend_file())
        # calculate the frame count
        return (data[0][1]) - (data[0][0]) + 1

    def render_stills(self):
        # Set the camera object for the scene
        bpy.context.scene.camera = bpy.data.objects['Camera']

        # Get the scene context to render
        scene = bpy.context.scene

        # Directory path to store rendered frames
        fp = self.path.get_temp()

        # Define render file format
        scene.render.image_settings.file_format = 'PNG'  # set output format to .png

        # Render each frame individually
        for frame_nr in range(self.get_frame_count()):
            # Select the current frame
            scene.frame_set(frame_nr)

            # Set output location and filename
            scene.render.filepath = fp + '0000' + str(frame_nr)

            # Render the frame to a still image
            bpy.ops.render.render(write_still=True)

        # Reset file path for rendering
        scene.render.filepath = fp


def do_import(in_obj):
    in_obj.clear_blend_file()
    in_obj.import_obj_file()
    in_obj.select_object()
    in_obj.set_textured_view()


def do_create_scene(scene):
    scene.create_lamp()
    scene.create_camera()
    scene.create_camera_path()
    #scene.create_key_frames()
    scene.bind_camera_path()
    scene.set_render_options()


def do_render(render):
    render.render_stills()


def main():
    file_path = FilePaths('theMartianColor.obj')
    out_file = 'my_test.blend'
    file_path.set_blend_file(os.path.join(file_path.abs_obj_dir, out_file))
    in_obj = Import_OBJ(file_path, out_file)
    do_import(in_obj)
    scene = BuildScene(10)
    do_create_scene(scene)
    in_obj.save_scene()
    render = RenderStills(file_path)
    do_render(render)

if __name__ == "__main__":
    main()
