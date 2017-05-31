#!/usr/bin/env python

import sys
import subprocess
from jpl_conf import FilePaths

main_scene = FilePaths().get_job_dir()
blender = FilePaths().get_blender_exec()
script = FilePaths().get_abs_path_project() + "blender_reduce.py"

for input_data in sys.stdin:
    job_file = main_scene
    print("REDUCER: " + str(sys.stdin))
    input_data = input_data.strip()
    print("REDUCER - PART 2:  " + str(input_data))
    start, end, rid, file_name = input_data.split()
    job_file += rid + "/assets/"
    job_file += file_name
    print("FILE_NAME: " + str(job_file))
    sub = subprocess.Popen([blender + " " + job_file + " -b -P " + script + " -- " +
                            str(start) + " " +
                            str(end) + " " + str(rid)], shell=True)
    sub.communicate()
