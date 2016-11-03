# Create the camera path
# blender my_test.blend --background --python /Users/chrisomlor/PycharmProjects/objload/create_camera.py

import bpy
from mathutils import Vector, Matrix
from mathutils import Vector

# number of frams for testing
end_frame = 250

# Set 3D View to textured so textures are displayed in .blend
for area in bpy.context.screen.areas: # iterate through areas in current screen
    if area.type == 'VIEW_3D':
        for space in area.spaces: # iterate through spaces in current VIEW_3D area
            if space.type == 'VIEW_3D': # check if space is a 3D view
                space.viewport_shade = 'TEXTURED' # set the viewport shading to rendered

# Get a object of the current scene
scene = bpy.context.scene

# #################################### LIGHTING #####################################
# Create a new light source object as a sun
lamp_data = bpy.data.lamps.new(name="Sun", type='SUN')

# Create new object with our lamp datablock
lamp_object = bpy.data.objects.new(name="Sun", object_data=lamp_data)

# Link lamp object to the scene so it'll appear in this scene
scene.objects.link(lamp_object)

# Place lamp to a specified location
lamp_object.location = (148.0, -100.0, 77.0)

# Set the rotation of the lamp
lamp_object.rotation_euler = (1.6, -0.82, 0.18)

# Set lighting options so textures can be rendered and visible
lmp = bpy.data.lamps[lamp_data.name]
lmp.energy = 0.5
lmp.use_specular = False

# #################################### CAMERA #####################################
# Create a new camera object
camera_data = bpy.data.cameras.new("Camera")

# Create new object with the camera data
camera_object = bpy.data.objects.new(name="Camera", object_data=camera_data)

# Link camera to the scene
scene.objects.link(camera_object)

# Place camera to a specified location
camera_object.location = (150.0, -85.0, 100.0)

# Set the rotation of the camera
camera_object.rotation_euler = (1.57, 0.0, 0.0)

# Get new camera object we created
cam = bpy.data.cameras[camera_data.name]

# Set the focal length of the camera lens.  Zoom out(default 32)
cam.lens = 10

# #################################### CAMERA PATH #####################################
# Create a new curve in 3D
curve_data = bpy.data.curves.new('Camera_Path', type='CURVE')
curve_data.dimensions = '3D'
curve_data.resolution_u = 2

# map coords to spline
polyline = curve_data.splines.new('NURBS')
polyline.points.add(end_frame)

# ###########################
# Test Data for Camera Path
# ###########################
# Creates a diagonal polyline path
x_pos = 150
y_pos = -85
z_pos = 100
for i in range(end_frame):
    polyline.points[i].co = (x_pos, y_pos, z_pos, 1)
    x_pos += 1
    z_pos += 3
#############################

# Create a curve object with the name Camera_Path
curve_object = bpy.data.objects.new('Camera_Path', curve_data)

# Link path to the Scene
scene.objects.link(curve_object)

# Sets the last frame for rendering.  Starting point is frame 1
# and we set path duration to ending frame so path duration is
# then end_frame - start_frame
bpy.data.curves["Camera_Path"].path_duration = end_frame

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

# Save the imported OBJ file as a .blend file
bpy.ops.wm.save_as_mainfile(filepath='my_test.blend', check_existing=True, copy=True)
