# Import OBJ file --> Save as a blend file
# terminal command:
# blender --background --python <path to python script> --<path to OBJ file>
# blender --background --python /Users/chrisomlor/PycharmProjects/objload/OBJ_import.py -- /Users/chrisomlor/MovieDemo/theMartianColor.obj
import bpy
import sys
import os

# Delete all default objects from scene
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete(use_global=True)

# Save the empty scene to a blend file
#bpy.ops.wm.save_as_mainfile(filepath='my_test.blend', relative_remap=True, copy=True)

# Import the OBJ file specified in command into blender
bpy.ops.import_scene.obj(filepath='theMartianColor.obj')

# Deselects theMartianColor object name that was just imported
# This needs to happen as it is selected by default and will
# cause problems with camera animation if left selected.
bpy.ops.object.select_all(action='DESELECT')

# Save the imported OBJ file
bpy.ops.wm.save_as_mainfile(filepath='my_test.blend')
