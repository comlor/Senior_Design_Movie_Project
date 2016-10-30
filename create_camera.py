# Create the camera path
# blender test.blend --background --python /Users/chrisomlor/PycharmProjects/objload/create_camera.py

import bpy
from mathutils import Vector, Matrix
from mathutils import Vector

# Add Camera Object
# Rotation is in radians about the selected axis (x, y, z), setting x = 1.57 --> ~90 degrees or 1.57 radians
# Location is (x, y, z) coordinates where camera is located on scene
# Layers is what layer the object is added to.
camera = bpy.ops.object.camera_add(location=(150.0, -85.0, 100.0), rotation=(1.57, 0.0, 0.0), layers=(True, False, False,
                                           False, False, False, False, False, False, False, False,
                                           False, False, False, False, False, False, False, False, False))

# Test data for camera path.  With sample mars data -Y value is positive altitude.
# +X, +Z moves across the map.
coords = [(150.0, -85.0, 100.0), (151.0, -85.0, 100.0), (152.0, -85.0, 100.0), (153.0, -85.0, 100.0),
          (154.0, -85.0, 100.0), (155.0, -85.0, 100.0), (156.0, -85.0, 100.0), (157.0, -85.0, 100.0),
          (158.0, -85.0, 100.0), (159.0, -85.0, 100.0), (160.0, -85.0, 100.0), (161.0, -85.0, 100.0),
          (162.0, -85.0, 100.0), (163.0, -85.0, 100.0), (164.0, -85.0, 100.0), (165.0, -85.0, 100.0),
          (166.0, -85.0, 100.0), (167.0, -85.0, 100.0), (168.0, -85.0, 100.0), (169.0, -85.0, 100.0),
          (170.0, -85.0, 100.0), (171.0, -85.0, 100.0), (172.0, -85.0, 100.0), (173.0, -85.0, 100.0),
          (174.0, -85.0, 100.0), (175.0, -85.0, 100.0), (176.0, -85.0, 100.0), (177.0, -85.0, 100.0),
          (178.0, -85.0, 100.0), (179.0, -85.0, 100.0), (180.0, -85.0, 100.0), (181.0, -85.0, 100.0),
          (182.0, -85.0, 100.0), (183.0, -85.0, 100.0), (184.0, -85.0, 100.0), (185.0, -85.0, 100.0),
          (186.0, -85.0, 100.0), (187.0, -85.0, 100.0), (188.0, -85.0, 100.0), (189.0, -85.0, 100.0),
          (190.0, -85.0, 100.0), (191.0, -85.0, 100.0), (192.0, -85.0, 100.0), (193.0, -85.0, 100.0),
          (194.0, -85.0, 100.0), (195.0, -85.0, 100.0), (196.0, -85.0, 100.0), (197.0, -85.0, 100.0),
          (198.0, -85.0, 100.0), (199.0, -85.0, 100.0), (200.0, -85.0, 100.0), (201.0, -85.0, 100.0),
          (202.0, -85.0, 100.0), (203.0, -85.0, 100.0), (204.0, -85.0, 100.0), (205.0, -85.0, 100.0),
          (206.0, -85.0, 100.0), (207.0, -85.0, 100.0), (208.0, -85.0, 100.0), (209.0, -85.0, 100.0),
          (210.0, -85.0, 100.0), (211.0, -85.0, 100.0), (212.0, -85.0, 100.0), (213.0, -85.0, 100.0),
          (214.0, -85.0, 100.0), (215.0, -85.0, 100.0), (216.0, -85.0, 100.0), (217.0, -85.0, 100.0),
          (218.0, -85.0, 100.0), (219.0, -85.0, 100.0), (220.0, -85.0, 100.0), (221.0, -85.0, 100.0),
          (222.0, -85.0, 100.0), (223.0, -85.0, 100.0), (224.0, -85.0, 100.0), (225.0, -85.0, 100.0),
          (226.0, -85.0, 100.0), (227.0, -85.0, 100.0), (228.0, -85.0, 100.0), (229.0, -85.0, 100.0)]

# Create a new curve in 3D
curveData = bpy.data.curves.new('Camera_Path', type='CURVE')
curveData.dimensions = '3D'
curveData.resolution_u = 2

# map coords to spline
polyline = curveData.splines.new('NURBS')
polyline.points.add(len(coords))
# Add coordinates into polyline
for i, coord in enumerate(coords):
    x,y,z = coord
    polyline.points[i].co = (x, y, z, 1)

# Create a curve object with the name Camera_Path
curveOB = bpy.data.objects.new('Camera_Path', curveData)

# Insert into Scene set as active and selected
scn = bpy.context.scene
scn.objects.link(curveOB)
scn.objects.active = curveOB
curveOB.select = True

# Get Camera object
camera = bpy.data.objects['Camera']
# Get Camera_Path object
path = bpy.data.objects['Camera_Path']

# Set both Camera and Camera_Path object as selected
camera.select = True
path.select = True

# Make objects active and set camera to follow camera path.
bpy.context.scene.objects.active = path
bpy.ops.object.parent_set(type='FOLLOW') #follow path

# Create a new light source object as a sun
bpy.ops.object.lamp_add(type='SUN', view_align=False, location=(148.0, -100.0, 77.0), rotation=(1.6, -0.82, 0.18),
                        layers=(True, False, False, False, False, False, False, False, False, False, False, False,
                                False, False, False, False, False, False, False, False))

# Turn on shadows as RAY_SHADOWS
bpy.types.AreaLamp.shadow_method = 'RAY_SHADOW'

# Get lamp data and set the intensity and distance of the light.
lamp = bpy.data.lamps['Sun']
lamp.energy = 0.500
lamp.distance = 3.0

# Save the imported OBJ file as a .blend file
bpy.ops.wm.save_as_mainfile(filepath='test.blend', check_existing=True, copy=True)
