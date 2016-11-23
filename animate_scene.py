import bpy
import os
import re
import glob
from jpl_config import FilePaths


class AnimateScene:

    def __init__(self, path):
        self.path = path

        # Directory where rendered stills are located
        self.in_dir = "./temp"

        # Get list of frames from directory
        self.lst = os.listdir(self.in_dir)

        # Set output directory to save final video
        self.out_dir = "./"

        bpy.data.scenes["Scene"].render.resolution_x = self.path.render_res_x
        bpy.data.scenes["Scene"].render.resolution_y = self.path.render_res_y
        bpy.data.scenes["Scene"].render.resolution_percentage = self.path.render_res_percent

    def animate(self):
        # Filter file list by valid file types.
        candidates = []
        c = 0
        for item in self.lst:
            fileName, fileExtension = os.path.splitext(self.lst[c])
            if fileExtension == ".png":
                candidates.append(item)
            c = + 1

        candidates.sort()

        file = [{"name": i} for i in candidates]
        n = len(file)
        print(n)

        def find_sequencer_area():
            screens = [bpy.context.screen] + list(bpy.data.screens)
            for screen in screens:
                for area in screen.areas:
                    if area.type == 'SEQUENCE_EDITOR':
                        return area

            # If that still doesn't work, I don't know what will
            return area

        a = bpy.ops.sequencer.image_strip_add({'area': find_sequencer_area()}, directory=self.in_dir,
                                              filter_blender=False, filter_image=True, filter_movie=False,
                                              filter_python=False, filter_font=False, filter_sound=False,
                                              filter_text=False,
                                              filter_btx=False, filter_collada=False,
                                              filter_folder=True, filemode=9, relative_path=False, frame_start=0,
                                              frame_end=n - 1,
                                              channel=1, replace_sel=True, files=file)
        # (directory=in_dir, files=file, channel=1, frame_start=0, frame_end=n - 1)

        stripname = file[0].get("name");
        bpy.data.scenes["Scene"].frame_end = n
        bpy.data.scenes["Scene"].render.image_settings.file_format = 'AVI_JPEG'
        bpy.data.scenes["Scene"].render.filepath = self.out_dir
        bpy.ops.render.render(animation=True)

        # Diagnostic to check whether the images were loaded
        stripname = file[0].get("name");
        print(bpy.data.scenes["Scene"].sequence_editor.sequences[stripname])
        print(dir(bpy.data.scenes["Scene"].sequence_editor.sequences[stripname]))



