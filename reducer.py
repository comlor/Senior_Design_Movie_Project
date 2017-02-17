#!/usr/bin/env python

import sys
import bpy
from jpl_config import FilePaths
import math
from subprocess import call

for input in sys.stdin:
    input = input.strip()
    print(input)
    start, end = input.split()
    print("start: " + str(start))
    print("end: " + str(end))

    file_path = FilePaths('theMartianColor.obj')

    bpy.context.scene.camera = bpy.data.objects['MyCamera']
    bpy.data.scenes['scene'].render.engine = ""
    # Get the scene context to render
    scene = bpy.context.scene

    # Directory path to store rendered frames
    fp = file_path.get_temp()

    # Define render file format
    scene.render.image_settings.file_format = 'PNG'  # set output format to .png


    def num_padding(x, y):
        value = ''
        for i in range((int((math.log(float(x), 10)))) - (int((math.log(float(y), 10)))) + 1):
            print(str(int(math.log(float(x), 10))) + '   --   ' + str(int(math.log(float(y), 10))))
            value += '0'
        return value


    # Render each frame individually
    for frame_nr in range(int(start), int(end), 1):
        # Select the current frame
        scene.frame_set(frame_nr)

        # Set output location and filename
        scene.render.filepath = fp + 'part' + num_padding(end,
                                                          (1 if (frame_nr == 0) else frame_nr)) + str(frame_nr)
        # scene.render.filepath = fp + 'part' + str(frame_nr)

        # Render the frame to a still image
        bpy.ops.render.render(write_still=True)

