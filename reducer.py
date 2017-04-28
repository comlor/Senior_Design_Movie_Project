#!/usr/bin/env python

import sys
import subprocess

main_scene = "/home/chrisomlor/MovieDemo/Assets/my_test.blend"
blender = "/usr/lib/blender/blender"
script = "/home/chrisomlor/MovieDemo/blender_reduce.py"

for input in sys.stdin:
    input = input.strip()
    start, end = input.split()
    sub = subprocess.Popen([blender + " " + main_scene + " -b -P " + script + " -- " +
                            str(start) + " " +
                            str(end)], shell=True)
    sub.communicate()
