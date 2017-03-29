import os
import bpy, bmesh
import addon_utils
import math
from bpy import context as C
from mathutils import Vector
from bpy_extras.object_utils import world_to_camera_view

class Mesh_Reducer:

    def __init__(self, file_path, blend_config):
        self.__file_path = file_path
        self.__blender_config = blend_config
        self.__initvisible = []

    def returnObjectByName(passedName=""):
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
        # print(zlist)
        return zlist


    def testInView(self, coord, tolerance):
        pointInView = False
        z = -1
        scene = bpy.context.scene
        camera = bpy.data.objects['Camera']
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


    def objectsVisible(self, total, current):
        for item in current:
            total.append(item)
        total = list(set(total))


    def findFrameForNewScene(self, initvisible, startingframe, terrain=""):
        total = []
        current = self.update_on_visible(terrain)
        s = set(initvisible) & set(current)
        scene = bpy.context.scene
        while len(s) > 0 & startingframe < 147:
            scene.frame_set(startingframe)
            current = self.update_on_visible(terrain)
            self.objectsVisible(total, current)
            startingframe += 1;
            s = set(initvisible) & set(current)
            print("Current Frame: " + str(startingframe) + "\n\n")
        return startingframe, list(set(total))


#split_terrain(10, "DTM - BIN12-FAST")
#initialize_lod("DTM - BIN12-FAST")
#initvisible = update_on_visible("DTM - BIN12-FAST")
#endframe, terrain = findFrameForNewScene(initvisible, 0, "DTM - BIN12-FAST")
#print(endframe)
#print(terrain)