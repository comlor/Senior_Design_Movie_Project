import blend_render_info
from jpl_config import FilePaths
import bpy
import math


class RenderStills:

    def __init__(self, path):
        self.path = path

    def get_frame_count(self):
        # Read .blend file header to get frame data
        data = blend_render_info.read_blend_rend_chunk(self.path.get_blend_file())
        # calculate the frame count
        return (data[0][1]) - (data[0][0]) + 1

    def render_stills(self):
        # Set the camera object for the scene
        bpy.context.scene.camera = bpy.data.objects['MyCamera']

        # Get the scene context to render
        scene = bpy.context.scene

        # Directory path to store rendered frames
        fp = self.path.get_temp()

        # Define render file format
        scene.render.image_settings.file_format = 'PNG'  # set output format to .png

        print('End Frame: ' + str(self.path.end_frame))

        def num_padding(x, y):
            value = ''
            for i in range((int((math.log(x, 10)))) - (int((math.log(y, 10)))) + 1):
                print(str(int(math.log(x, 10))) + '   --   ' + str(int(math.log(y, 10))))
                value += '0'
            return value

        # Render each frame individually
        for frame_nr in range(self.get_frame_count()):
            # Select the current frame
            scene.frame_set(frame_nr)

            # Set output location and filename
            scene.render.filepath = fp + 'part' + num_padding(self.path.end_frame, (1 if (frame_nr == 0) else frame_nr)) + str(frame_nr)
            #scene.render.filepath = fp + 'part' + str(frame_nr)

            # Render the frame to a still image
            bpy.ops.render.render(write_still=True)

        # Reset file path for rendering
        #scene.render.filepath = fp