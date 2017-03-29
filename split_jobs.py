from jpl_conf import Blender_Config_Options
from jpl_conf import FilePaths
import sys
import bpy
import os

def set_end_frame(end_frame):
    bpy.data.scenes["Scene"].frame_end = int(end_frame)

def set_start_frame(start_frame):
    bpy.data.scenes["Scene"].frame_start = int(start_frame)

def save_new_scene_file(file_path, job_num):
    save_loc = file_path.get_abs_path_assets()
    #save_file = file_path.get_blend_file_name()
    #print("SAVE_FILE_PATH_OBJ: ", save_file)
    #file_name_parts = save_file.split('.')
    #print("File_Name_Parts: ", str(file_name_parts))
    save_file = "job_"
    save_file += str(job_num)
    save_file += ".blend"
    print("SAVE FILE: ", str(save_file))
    save = os.path.join(save_loc, save_file)
    bpy.ops.wm.save_as_mainfile(filepath=save)
    return None

def main():
    file_path = FilePaths("my_image.IMG", "my_test.blend", "texture_sb.jpg")
    #print('Number of arguments:', len(sys.argv), 'arguments.')
    #print('Argument List:', str(sys.argv))

    index_args = sys.argv.index("--")
    #print("index --: " + str(index_args))
    my_args = sys.argv[index_args+1::]
    #print("My_args: ", str(my_args))
    job_num = my_args[0]
    start_frame = my_args[1]
    end_frame = my_args[2]
    #print("Job_num: ", str(job_num))
    #print("Start: ", str(start_frame))
    #print("End: ", str(end_frame))
    set_start_frame(start_frame)
    set_end_frame(end_frame)
    save_new_scene_file(file_path, job_num)

if __name__ == '__main__':
    main()
