# Senior_Design_Movie_Project
CSULA Senior Design Project for JPL Movie Project

<p>Blender Files:</p>
<p>jpl_config.py - Configuration file for file paths</p>
<p>create_blend.py - Clears default objects and imports OBJ, Sets up textures</p>
<p>create_scene.py - Creates lighting object, camera object, camera path and interpolates points</p>
<p>render_scene.py - Renders the camera viewport into still images</p>

<p>Main File to perform job</p>
<p>job.py - Performs each task using the Blender python files</p>


<p>To use this version</p>
<p>All blender files must be stored in the appropriate directory.</p>

<p>Windows</p>
<p>C:\Documents and Settings\All Users\AppData\Roaming\Blender Foundation\Blender\2.78\scripts\modules\</p>

<p>Linux</p>
<p>/usr/share/blender/scripts/modules/</p>

<p>Job.py does not go here.  This file belongs with the project files</p>

<p>To run the script</p>

<p>if from the command prompt you should CD into directory where job.py is located.  Otherwise you will need to </p>
<p>include full filepath to job.py</p>
<code>(path to blender) -b -t 0 -P job.py</code>

