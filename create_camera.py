# Create the camera path
# blender test.blend --background --python /Users/chrisomlor/PycharmProjects/objload/create_camera.py

import bpy
from mathutils import Vector

# Add Camera Object
# Rotation is in radians about the selected axis (x, y, z), setting x = 1.57 --> ~90 degrees or 1.57 radians
# Location is (x, y, z) coordinates where camera is located on scene
# Layers is what layer the object is added to.
camera = bpy.ops.object.camera_add(location=(150.0, -75.0, 100.0), rotation=(1.57, 0.0, 0.0), layers=(True, False, False,
                                           False, False, False, False, False, False, False, False,
                                           False, False, False, False, False, False, False, False, False))

coords = [(150.0, -75.0, 100.0), (151.0, -75.0, 100.0), (152.0, -75.0, 100.0), (153.0, -75.0, 100.0),
              (154.0, -75.0, 100.0), (155.0, -75.0, 100.0), (156.0, -75.0, 100.0), (157.0, -75.0, 100.0),
              (158.0, -75.0, 100.0), (159.0, -75.0, 100.0), (160.0, -75.0, 100.0), (161.0, -75.0, 100.0),
              (162.0, -75.0, 100.0), (163.0, -75.0, 100.0), (164.0, -75.0, 100.0), (165.0, -75.0, 100.0),
              (166.0, -75.0, 100.0), (167.0, -75.0, 100.0), (168.0, -75.0, 100.0), (169.0, -75.0, 100.0),
              (170.0, -75.0, 100.0), (171.0, -75.0, 100.0), (172.0, -75.0, 100.0), (173.0, -75.0, 100.0),
              (174.0, -75.0, 100.0), (175.0, -75.0, 100.0), (176.0, -75.0, 100.0), (177.0, -75.0, 100.0),
              (178.0, -75.0, 100.0), (179.0, -75.0, 100.0), (180.0, -75.0, 100.0), (181.0, -75.0, 100.0),
              (182.0, -75.0, 100.0), (183.0, -75.0, 100.0), (184.0, -75.0, 100.0), (185.0, -75.0, 100.0),
              (186.0, -75.0, 100.0), (187.0, -75.0, 100.0), (188.0, -75.0, 100.0), (189.0, -75.0, 100.0),
              (190.0, -75.0, 100.0), (191.0, -75.0, 100.0), (192.0, -75.0, 100.0), (193.0, -75.0, 100.0),
              (194.0, -75.0, 100.0), (195.0, -75.0, 100.0), (196.0, -75.0, 100.0), (197.0, -75.0, 100.0),
              (198.0, -75.0, 100.0), (199.0, -75.0, 100.0), (200.0, -75.0, 100.0), (201.0, -75.0, 100.0)]

# create the Curve Datablock
curveData = bpy.data.curves.new('Camera_Path', type='CURVE')
curveData.dimensions = '3D'
curveData.resolution_u = 2

# map coords to spline
polyline = curveData.splines.new('NURBS')
polyline.points.add(len(coords))
for i, coord in enumerate(coords):
    x,y,z = coord
    polyline.points[i].co = (x, y, z, 1)

# create Object
curveOB = bpy.data.objects.new('Camera_Path', curveData)

# attach to scene and validate context
scn = bpy.context.scene
scn.objects.link(curveOB)
scn.objects.active = curveOB
curveOB.select = True

camera = bpy.data.objects['Camera']
path = bpy.data.objects['Camera_Path']
#lamp = bpy.data.objects['Lamp']

camera.select = True
#lamp.select = True
path.select = True

bpy.context.scene.objects.active = path #parent

bpy.ops.object.parent_set(type='FOLLOW') #follow path


# Create new lamp datablock
lamp_data = bpy.data.lamps.new(name="Sun", type='POINT')

# Create new object with our lamp datablock
lamp_object = bpy.data.objects.new(name="Sun", object_data=lamp_data)

# Link lamp object to the scene so it'll appear in this scene
scn.objects.link(lamp_object)

# Place lamp to a specified location
lamp_object.location = (0.0, -200.0, 0.0)

# And finally select it make active
lamp_object.select = True
scn.objects.active = lamp_object







#points = [((-10.875, -0.444, 0.122), (-16.375, 5.056, 0.122), (-5.375, -5.944, 0.122)),
#          ((11.125, -0.444, 0.122), (4.420, -9.648, 0.122), (17.602, 8.447, 0.122)),
#          ((22.125, 10.556, 0.122), (9.216, 6.553, 8.612), (31.022, 13.315, -5.729)),
#          ((-0.284, 16.306, 0.122), (-25.732, 16.306, -49.859), (25.164, 16.306, 50.103))]

# create the Curve Datablock
#curveData = bpy.data.curves.new('myCurve', type='CURVE')
#curveData.dimensions = '3D'
#curveData.resolution_u = 2

# map coords to spline
#polyline = curveData.splines.new('POLY')
#polyline.points.add(len(points))
#for i, coord in enumerate(points):
#    x,y,z = coord
#    polyline.points[i].co = (x, y, z, 1)

# create Object
#curveOB = bpy.data.objects.new('myCurve', curveData)

# attach to scene and validate context
#scn = bpy.context.scene
#scn.objects.link(curveOB)
#scn.objects.active = curveOB
#curveOB.select = True

#def look_at(obj_camera, point):
#    loc_camera = obj_camera.matrix_world.to_translation()

#    direction = point - loc_camera
    # point the cameras '-Z' and use its 'Y' as up
#    rot_quat = direction.to_track_quat('-Z', 'Y')

    # assume we're using euler rotation
    #obj_camera.rotation_euler = rot_quat.to_euler()


#curveData = bpy.data.curves.new('path', type='CURVE')
#curveData.dimensions = '3D'
#curveData.resolution_u = 2

#polyline = curveData.splines.new('BEZIER')
#polyline.bezier_points.add(len(points) - 1)
#polyline.use_cyclic_u = True
#for i, ((x, y, z), (lh_x, lh_y, lh_z), (rh_x, rh_y, rh_z)) in enumerate(points):
#    polyline.bezier_points[i].co = (x, y, z)
#    polyline.bezier_points[i].handle_left = (lh_x, lh_y, lh_z,)
#    polyline.bezier_points[i].handle_right = (rh_x, rh_y, rh_z)

#curveOB = bpy.data.objects.new('path', curveData)

#scn = bpy.context.scene
#scn.objects.link(curveOB)
#scn.objects.active = curveOB
#curveOB.select = True

#cam = bpy.data.cameras.new("Cam")
#cam_ob = bpy.data.objects.new("Cam", cam)
#obj_other = bpy.data.objects["Cube"]
#bpy.context.scene.objects.link(cam_ob)

#cam_ob.location.x = -0.284
#cam_ob.location.y = 16.306
#cam_ob.location.z = 0.122
#cam_ob.location = points[0][0]
#look_at(cam_ob, obj_other.matrix_world.to_translation())

#cam_ob.select = True
#bpy.ops.object.parent_set(type='FOLLOW')

#cam = bpy.data.objects['Camera']
#bpy.data.objects.new("Empty", None)
#origin = bpy.data.objects['Empty']

# Save the imported OBJ file as a .blend file
bpy.ops.wm.save_as_mainfile(filepath='test.blend', check_existing=True, copy=True)














# Set Camera to follow a path
#camera = bpy.data.objects['Camera']
#path = bpy.data.objects['NurbsPath']
#lamp = bpy.data.objects['Lamp']
#camera.select = True
#lamp.select = True
#path.select = True
#bpy.context.scene.objects.active = path #parent
#bpy.ops.object.parent_set(type='FOLLOW') #follow path