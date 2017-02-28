import bpy
from bpy.props import *
import bmesh
from math import *
from mathutils import Color, Euler, Vector, Quaternion
import os

class Planetographic:

    def __init__(self):
        self.rad90 = radians(90)
        self.rad180 = radians(180)
        self.baseRotation = Euler((rad90, 0, rad90), 'XYZ')
        self.baseRotationQuat = baseRotation.to_quaternion()

    def pollcondition(self, context):
        return context.mode == 'OBJECT' and context.active_object != None

    def loadimage(imagePath, fileName):
        try:
            return bpy.data.images[fileName]
        except:
            try:
                fullFileName = bpy.path.abspath(imagePath + fileName)
                return bpy.data.images.load(fullFileName, check_existing=False)
            except:
                return None

    def AssignColorToMat(mat, nodeName, color):
        node = mat.node_tree.nodes.get(nodeName)
        if node != None:
            node.inputs['Color'].default_value = (color.r, color.g, color.b, 1)

    def AssignTextureToMat(mat, nodeName, image):
        if image:
            node = mat.node_tree.nodes.get(nodeName)
            node.image = image

    def PlaceCamera_Lat_Long(worldLocation, radius, latDeg, lonDeg, scale, pin, card):

        latRad, lonRad = radians(latDeg), radians(lonDeg)

        x = cos(latRad) * cos(lonRad)
        y = cos(latRad) * sin(lonRad)
        z = sin(latRad)

        location = Vector((x, y, z)) * radius
        locationFromWorld = location + worldLocation
        scale3D = (scale, scale, scale)

        aroundZ = Quaternion((0, 0, 1), lonRad)
        aroundY = Vector((0, -1, 0))
        aroundY.rotate(aroundZ)
        aroundX = Quaternion(aroundY, latRad)

        rotation = Quaternion(baseRotationQuat)
        rotation.rotate(aroundZ)
        rotation.rotate(aroundX)

        pin.scale = scale3D
        pin.location = locationFromWorld
        pin.rotation_euler = rotation.to_euler('XYZ')

        card.scale = scale3D
        card.location = locationFromWorld
        card.rotation_euler = rotation.to_euler('XYZ')

    def MakePins(world, file, pin, pinMaterial, pinNode, card, cardMaterial, cardNode, imagePath):
        worldLocation = world.location
        radius = world.dimensions.x / 2.0