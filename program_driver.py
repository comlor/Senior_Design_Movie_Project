import subprocess
import os
import sys
import time
from jpl_conf import FilePaths
import requests


def timing(f):
    def wrap(*args):
        time1 = time.time()
        ret = f(*args)
        time2 = time.time()
        FilePaths().log_events('TIMING------: %s function took %0.3f ms' % (f.__name__, (time2 - time1)*1000.0) + "\n")
    return wrap


@timing
def make_blend_file(job_dir, blend_file, texture_file, dtm_file, json):
    FilePaths().log_events("CREATE SCENE\n")
    # incoming args list
    # args[0]
    # args[1] json
    # args[2] job_path
    # args[3] output_dir
    # args[4] randomid

    blender = FilePaths().get_blender_exec()
    FilePaths().log_events("Blender Exececutable: " + blender + "\n")
    script = FilePaths().get_abs_path_project() + "job.py"
    FilePaths().log_events("Script File: " + script)
    # subprocess call arguments
    # arg[0] blender
    # arg[1] -b
    # arg[2] -P
    # arg[3] script
    # arg[4] --
    # arg[5] json
    FilePaths().log_events("Creating Scene: " + blender + " -b -P " + script + " -- " + json + " " + job_dir + " " +
                           blend_file + " " + texture_file + " " + dtm_file + "\n")
    sub = subprocess.Popen(
        [blender + " -b -P " + script + " -- " + json + " " + job_dir + " " + blend_file + " " + texture_file + " " +
         dtm_file], shell=True)
    sub.communicate()


@timing
def render_scenes(hadoop_in):
    FilePaths().log_events("RENDER SCENE\n")
    hadoop = FilePaths().get_hadoop_exec()
    FilePaths().log_events("Hadoop Executable: " + hadoop + "\n")
    hadoop_streaming = FilePaths().get_hadoop_streaming()
    FilePaths().log_events("Hadoop Streaming jar: " + hadoop_streaming + "\n")

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

    FilePaths().log_events("Execute Hadoop Process: " + cmd + "\n")
    sub = subprocess.Popen([cmd], shell=True)
    sub.communicate()


@timing
def animate_movie(job_dir, rid):
    FilePaths().log_events("ANIMATE SCENE\n")
    blender = FilePaths().get_blender_exec()
    FilePaths().log_events("Blender Executable: " + blender + "\n")
    output = FilePaths().get_final_output_dir() + rid + "/"
    FilePaths().log_events("Movie Output Location: " + output + "\n")

    cmd = blender
    cmd += " -b -P "
    cmd += FilePaths().get_abs_path_project() + "animate_scene.py"
    cmd += " -- "
    cmd += job_dir + "/temp/ "
    cmd += output

    FilePaths().log_events("Execute Animation: " + cmd + "\n")
    sub = subprocess.Popen([cmd], shell=True)
    sub.communicate()

def main():
    FilePaths().log_events("MAIN PROGRAM\n")
    FilePaths().log_events("System Args: " + str(sys.argv) + "\n")
    job_dir = sys.argv[2]

    # Create Absolute file path variables used to create the job directory structure
    FilePaths().log_events("Creating Directory Structure\n")
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
    FilePaths().log_events("Current Job: " + job_dir + "\n")

    if not os.path.isdir(job_hadoop):
        os.makedirs(job_hadoop)
    FilePaths().log_events("Hadoop Job: " + job_hadoop + "\n")

    if not os.path.isdir(job_hadoop_in):
        os.makedirs(job_hadoop_in)
    FilePaths().log_events("Hadoop Input: " + job_hadoop_in + "\n")

    if not os.path.isdir(job_temp):
        os.makedirs(job_temp)
    FilePaths().log_events("Current Job Temp File: " + job_temp + "\n")

    if not os.path.isdir(job_assets):
        os.makedirs(job_assets)
    FilePaths().log_events("Current Job Assets: " + job_assets + "\n")

    make_blend_file(job_dir, blend_file, str(texture_file), dtm_file, sys.argv[1])
    render_scenes(job_hadoop)
    animate_movie(job_dir, sys.argv[4])
    #CALL POST SEND EMAIL

    FilePaths().log_events("Send Email to User\n")
    r = requests.post("http://et-etb10c-x02:8281/completed", str(sys.argv[4]))

if __name__ == "__main__":
    main()
