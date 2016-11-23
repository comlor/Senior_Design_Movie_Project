from jpl_config import FilePaths
from create_blend import Import_OBJ
from create_scene import BuildScene
from render_scene import RenderStills
from animate_scene import AnimateScene
import os

# Profiling imports to test timing
import time


def timing(f):
    def wrap(*args):
        time1 = time.time()
        ret = f(*args)
        time2 = time.time()
        print('%s function took %0.3f ms' % (f.__name__, (time2 - time1)*1000.0))
    return wrap


@timing
def do_import(in_obj):
    in_obj.clear_blend_file()
    in_obj.import_obj_file()
    in_obj.select_object()
    in_obj.set_textured_view()


@timing
def do_create_scene(scene):
    #scene.new_reducer()
    scene.set_end_frame()
    scene.create_lamp()
    scene.create_camera()
    scene.create_camera_path()
    #scene.create_key_frames()
    scene.bind_camera_path()
    scene.set_render_options()


@timing
def do_render(render):
    render.render_stills()


@timing
def do_animate(animater):
    animater.animate()

def main():
    #points = [[0, 150.000, -85.000, 100.000],
    #          [10, 150.000, -85.000, 200.000,
    #          [30, 225.000, -85.000, 225.000],
    #          [45, 300.000, -85.000, 275.000]]
    #points = [[0, 150.000, -85.000, 100.000], [10, 150.000, -85.000, 200.000]]
    points = [[0, 150.000, -75.000, 100.000], [10, 150.000, 0.000, 100.000]]
    file_path = FilePaths('theMartianColor.obj')
    out_file = 'my_test.blend'
    file_path.blend_file = out_file
    in_obj = Import_OBJ(file_path, out_file)
    file_path.set_blend_file(os.path.join(file_path.abs_obj_dir, out_file))
    do_import(in_obj)
    in_obj.save_scene()
    scene = BuildScene(points, file_path)
    do_create_scene(scene)
    in_obj.save_scene()
    render = RenderStills(file_path)
    do_render(render)
    animater = AnimateScene(file_path)
    do_animate(animater)

if __name__ == "__main__":
    main()
