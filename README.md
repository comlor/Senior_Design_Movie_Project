# Senior_Design_Movie_Project
CSULA Senior Design Project for JPL Movie Project

Blender Files:
jpl_config.py - Configuration file for file paths
create_blend.py - Clears default objects and imports OBJ, Sets up textures
create_scene.py - Creates lighting object, camera object, camera path and interpolates points
render_scene.py - Renders the camera viewport into still images

Main File to perform job
job.py - Performs each task using the Blender python files


To use this version
All blender files must be stored in the appropriate directory.

Windows
C:\Documents and Settings\All Users\AppData\Roaming\Blender Foundation\Blender\2.78\scripts\modules\

Linux
/usr/share/blender/scripts/modules/

Job.py does not go here.  This file belongs with the project files

To run the script

if from the command prompt you should CD into directory where job.py is located.  Otherwise you will need to 
include full filepath to job.py
<path to blender> -b -t 0 -P job.py

