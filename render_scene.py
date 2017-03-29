import blend_render_info
from jpl_conf import FilePaths
import bpy
import math
import bmesh
from mathutils import Vector
from bpy_extras.object_utils import world_to_camera_view
from bpy import context as C


class RenderStills:

    def __init__(self, blender_options, path):
        self.__blender_options = blender_options
        self.path = path

    def get_frame_count(self):
        # Read .blend file header to get frame data
        data = blend_render_info.read_blend_rend_chunk(self.path.get_blend_file())
        # calculate the frame count
        return (data[0][1]) - (data[0][0]) + 1

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
                ob.modifiers["Decimate"].ratio = 0.02
                self.select_object()

        for ob in bpy.context.scene.objects:
            for i, val in enumerate(zlist):
                if ob.type == 'MESH' and ob.name.startswith(terrain):
                    if ob.name == val:
                        ob.select = True
                        bpy.context.scene.objects.active = ob
                        ob.modifiers["Decimate"].ratio = 0.9
                        self.select_object()

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

    def select_object(self):
        # Deselects theMartianColor object name that was just imported
        # This needs to happen as it is selected by default and will
        # cause problems with camera animation if left selected.
        bpy.ops.object.select_all(action='DESELECT')

    def pointsOfMesh(self, object):
        points = []
        if getattr(object, 'type', '') == 'MESH':
            points = [v.co for v in object.data.vertices]

        return points

    def render_stills(self):
        # Set the camera object for the scene
        bpy.context.scene.camera = bpy.data.objects['MyCamera']

        # Get the scene context to render
        scene = bpy.context.scene

        # Directory path to store rendered frames
        fp = self.path.get_abs_path_temp()

        # Define render file format
        scene.render.image_settings.file_format = 'PNG'  # set output format to .png

        print('End Frame: ' + str(self.__blender_options.get_end_frame()))

        def num_padding(x, y):
            value = ''
            for i in range((int((math.log(x, 10)))) - (int((math.log(y, 10)))) + 1):
                print(str(int(math.log(x, 10))) + '   --   ' + str(int(math.log(y, 10))))
                value += '0'
            return value

        # Render each frame individually
        for frame_nr in range(self.get_frame_count()):
            # Select the current frame
            scene.frame_set(frame_nr)

            #if frame_nr % 10 == 0:
            #    terrain = self.__blender_options.get_terrain()
            #    self.update_on_visible(terrain)

            # Set output location and filename
            end_fr = self.__blender_options.get_end_frame()
            scene.render.filepath = fp + 'part' + num_padding(end_fr, (1 if (frame_nr == 0) else frame_nr)) + str(frame_nr)
            #scene.render.filepath = fp + 'part' + str(frame_nr)

            # Render the frame to a still image
            bpy.ops.render.render(write_still=True)

        # Reset file path for rendering
        #scene.render.filepath = fp