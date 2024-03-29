import bpy
import os
import sys
import re
import glob
from jpl_conf import FilePaths


class AnimateScene:

    def __init__(self, file_dir, output_dir):
        #self.path = path

        # Directory where rendered stills are located
        self.in_dir = file_dir

        # Get list of frames from directory
        self.lst = os.listdir(self.in_dir)

        # Set output directory to save final video
        self.out_dir = output_dir


    def animate(self):
        # Filter file list by valid file types.
        candidates = []
        c = 0
        for item in self.lst:
            fileName, fileExtension = os.path.splitext(self.lst[c])
            if fileExtension == ".png":
                candidates.append(item)
            c = + 1

        FilePaths().log_events("Number of Images: " + str(len(candidates)) + "\n")

        candidates.sort()

        file = [{"name": i} for i in candidates]
        n = len(file)

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
                                              frame_end=n - 1,  sort_method='FILE_SORT_ALPHA',
                                              channel=1, replace_sel=True, files=file)
        # (directory=in_dir, files=file, channel=1, frame_start=0, frame_end=n - 1)

        stripname = file[0].get("name")
        bpy.data.scenes["Scene"].frame_end = n
        bpy.data.scenes["Scene"].render.image_settings.file_format = 'H264'
        bpy.data.scenes["Scene"].render.filepath = self.out_dir
        bpy.ops.render.render(animation=True)

        # Diagnostic to check whether the images were loaded
        stripname = file[0].get("name")
        FilePaths().log_events(str(bpy.data.scenes["Scene"].sequence_editor.sequences[stripname]) + "\n")
        FilePaths().log_events(str(dir(bpy.data.scenes["Scene"].sequence_editor.sequences[stripname])) + "\n")


def main():
    FilePaths().log_events("ANIMATE STILL IMAGES")
    image_path = sys.argv[5]
    FilePaths().log_events("Image Path: " + image_path)
    output_path = sys.argv[6]
    FilePaths().log_events("Output Path: " + output_path)
    animater = AnimateScene(image_path, output_path)
    animater.animate()

if __name__ == "__main__":
    main()
