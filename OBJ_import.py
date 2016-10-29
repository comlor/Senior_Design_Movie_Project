# Import OBJ file --> Save as a blend file
# terminal command:
# blender --background --python <path to python script> --<path to OBJ file>
# blender --background --python /Users/chrisomlor/PycharmProjects/objload/OBJ_import.py
#           -- /Users/chrisomlor/MovieDemo/theMartianColor.obj
import bpy
import sys

# Delete all default objects from scene
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete()

# Save the empty scene to a blend file
bpy.ops.wm.save_as_mainfile(filepath='test.blend', relative_remap=True, copy=True)

# Import the OBJ file specified in command into blender
bpy.ops.import_scene.obj(filepath=sys.argv[-1])

# Prints name of all objects on scene in terminal
#obs = bpy.data.objects
#for ob in obs:
#    print(ob.name)

# Save the imported OBJ file
bpy.ops.wm.save_mainfile(filepath='test.blend')
