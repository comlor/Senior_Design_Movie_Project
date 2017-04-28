import subprocess
import os
import sys
from CzmlParser import CZML_Parser
import requests

# Step 1
def make_blend_file(json=None):
    cwd = os.getcwd()
    blender = "/usr/lib/blender/blender"
    scene = cwd + "myscene.blend"
    script = "/home/chrisomlor/MovieDemo/job.py"
    sub = subprocess.Popen([blender + " -b -P " + script + " -- " + json], shell=True)
    sub.communicate()

# Step 2
def render_scenes():
    cmd = "/usr/local/hadoop/bin/hadoop jar /usr/local/hadoop/share/hadoop/tools/lib/hadoop-streaming-2.8.0.jar"
    cmd += " -input "
    cmd += "/home/chrisomlor/MovieDemo/hadoop/input/"
    cmd += " -output "
    cmd += "/home/chrisomlor/MovieDemo/hadoop/output"
    cmd += " -mapper "
    cmd += "/home/chrisomlor/MovieDemo/mapper.py"
    cmd += " -reducer "
    cmd += "/home/chrisomlor/MovieDemo/reducer.py"
    sub = subprocess.Popen([cmd], shell=True)
    sub.communicate()

# Step 3
def animate_movie():
    cmd = "/usr/lib/blender/blender -b -P"
    cmd += " /home/chrisomlor/MovieDemo/animate_scene.py"
    cmd += " -- "
    cmd += "/home/chrisomlor/MovieDemo/temp/ "
    cmd += "/home/chrisomlor/MovieDemo/"
    sub = subprocess.Popen([cmd], shell=True)
    sub.communicate()

def main():
    #jparse = CZML_Parser(sys.argv[1])
    make_blend_file(sys.argv[1])
    #render_scenes()
    #animate_movie()
    #CALL POST SEND EMAIL
    #r = requests.post("localhost:8280/completed", data=sys.argv[4])

if __name__ == "__main__":
    main()
