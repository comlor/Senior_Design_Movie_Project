import subprocess
import os
import sys
from jpl_conf import FilePaths
import requests


# Step 1
def make_blend_file(job_dir, blend_file, texture_file, dtm_file, json):
    # incoming args list
    # args[0]
    # args[1] json
    # args[2] job_path
    # args[3] output_dir
    # args[4] randomid

    blender = FilePaths().get_blender_exec()
    script = FilePaths().get_abs_path_project() + "job.py"
    # subprocess call arguments
    # arg[0] blender
    # arg[1] -b
    # arg[2] -P
    # arg[3] script
    # arg[4] --
    # arg[5] json
    sub = subprocess.Popen(
        [blender + " -b -P " + script + " -- " + json + " " + job_dir + " " + blend_file + " " + texture_file + " " + dtm_file]
        , shell=True)
    sub.communicate()


# Step 2
def render_scenes(hadoop_in):
    hadoop = FilePaths().get_hadoop_exec()
    hadoop_streaming = FilePaths().get_hadoop_streaming()

    cmd = hadoop
    cmd += " jar "
    cmd += hadoop_streaming
    cmd += " -input "
    cmd += hadoop_in + "/input/"
    cmd += " -output "
    cmd += hadoop_in + "/output/"
    cmd += " -mapper "
    cmd += FilePaths().get_abs_path_project() + "mapper.py"
    cmd += " -reducer "
    cmd += FilePaths().get_abs_path_project() + "reducer.py"

    sub = subprocess.Popen([cmd], shell=True)
    sub.communicate()


# Step 3
def animate_movie(job_dir, rid):
    blender = FilePaths().get_blender_exec()
    output = FilePaths().get_final_output_dir() + rid + "/"

    cmd = blender
    cmd += " -b -P "
    cmd += FilePaths().get_abs_path_project() + "animate_scene.py"
    cmd += " -- "
    cmd += job_dir + "/temp/ "
    cmd += output

    sub = subprocess.Popen([cmd], shell=True)
    sub.communicate()

def main():
    job_dir = sys.argv[2]

    # Create Absolute file path variables used to create the job directory structure
    job_hadoop = job_dir + "/hadoop"
    job_hadoop_in = job_hadoop + "/input"
    job_hadoop_out = job_hadoop + "/output"
    job_temp = job_dir + "/temp"
    job_assets = job_dir + "/assets"

    # Name of the blend file
    blend_file = sys.argv[4] + ".blend"
    # For Future Implementation
    texture_file = None
    dtm_file = "my_image.IMG"

    # Create Directory Structure for The Current Job
    if not os.path.isdir(job_dir):
        os.makedirs(job_dir)

    if not os.path.isdir(job_hadoop):
        os.makedirs(job_hadoop)

    if not os.path.isdir(job_hadoop_in):
        os.makedirs(job_hadoop_in)

    if not os.path.isdir(job_temp):
        os.makedirs(job_temp)

    if not os.path.isdir(job_assets):
        os.makedirs(job_assets)

    make_blend_file(job_dir, blend_file, str(texture_file), dtm_file, sys.argv[1])
    render_scenes(job_hadoop)
    animate_movie(job_dir, sys.argv[4])
    #CALL POST SEND EMAIL
    print("ARG4:  " + str(sys.argv[4]))
    r = requests.post("http://localhost:8281/completed", str(sys.argv[4]))

if __name__ == "__main__":
    main()
