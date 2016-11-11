import subprocess
import os

# Variables
project_path = './'
blender_path = 'blender'
background = '--background'
python_switch = '-P'
thread_switch = '-t 2'
OBJ_import = 'OBJ_import.py'
create_camera = 'create_camera.py'
render = 'render.py'
animate = 'animate.py'
obj_file = 'theMartianColor.obj'
blend_file = 'my_test.blend'

# Import OBJ Files
print("Importing OBJ --> this can take a while")
sub = subprocess.Popen('blender --background -t 2 --python OBJ_import.py -- theMartianColor.obj',
                       stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
out, err = sub.communicate()
print("Import Complete...")

# Create Scene with camera, lighting and path
print("Creating scene with your selections")
sub2 = subprocess.Popen('blender my_test.blend --background -t 2 --python create_camera.py',
                        stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
out, err = sub2.communicate()
print("Scene Creation Complete...")

# Render stills from scene
print("Rendering your movie --> This process can take time if your movie is long")
sub3 = subprocess.Popen('blender my_test.blend --background -t 2 --python render.py',
                        stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
out, err = sub3.communicate()
print("Rendering Complete...")

# Animate stills into movie
print("Animating your movie")
sub4 = subprocess.Popen('blender test.blend --background --python animate.py',
                        stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
out, err = sub4.communicate()
print("Your movie is complete and ready to be played")
