from jpl_conf import FilePaths
from jpl_conf import Blender_Config_Options
from create_blend import Importer
from create_scene import BuildScene
from render_scene import RenderStills
from animate_scene import AnimateScene
from osgeo import gdal, osr
from CzmlParser import CZML_Parser
import sys

# Profiling imports to test timing
import time


def timing(f):
    def wrap(*args):
        time1 = time.time()
        ret = f(*args)
        time2 = time.time()
        print('%s function took %0.3f ms' % (f.__name__, (time2 - time1)*1000.0))
    return wrap

def get_meta_data(path):
    bag = gdal.Open(path.get_import_file_name())  # replace it with your file
    # raster is projected
    bag_gtrn = bag.GetGeoTransform()
    bag_proj = bag.GetProjectionRef()
    bag_srs = osr.SpatialReference(bag_proj)
    geo_srs = bag_srs.CloneGeogCS()  # new srs obj to go from x,y -> φ,λ
    transform = osr.CoordinateTransformation(bag_srs, geo_srs)

    bag_bbox_cells = (
        (0., 0.),
        (0, bag.RasterYSize),
        (bag.RasterXSize, bag.RasterYSize),
        (bag.RasterXSize, 0),
    )

    geo_pts = []
    pix_pts = []
    xy_pts = []
    for x, y in bag_bbox_cells:
        x2 = bag_gtrn[0] + bag_gtrn[1] * x + bag_gtrn[2] * y
        y2 = bag_gtrn[3] + bag_gtrn[4] * x + bag_gtrn[5] * y
        geo_pt = transform.TransformPoint(x2, y2)[:2]
        geo_pts.append(geo_pt)
        pix_pts.append([x2, y2])
        xy_pts.append([x, y])

    #print("index 0: " + str(xy_pts))
    #print("index 1: " + str(pix_pts))
    #print("index 2: " + str(geo_pts))

    return [xy_pts, pix_pts, geo_pts]

@timing
def do_import(in_obj, blend_config, user_points):
    in_obj.clear_blend_file()
    objName = "terrain"
    blend_config.set_terrain(objName)

    # Importing Functions.
    # Supports IMG, Collada, and OBJ
    #in_obj.import_hirise_img("BIN2")
    in_obj.import_hirise_img("BIN6", 0.01)
    #in_obj.import_hirise_img("BIN12-FAST", 0.01)

    in_obj.set_material_option()
    #in_obj.split_terrain_by_points(user_points, 6, objName)
    #in_obj.initialize_lod(objName)
    #in_obj.split_terrain(6, objName)
    in_obj.select_object()

@timing
def do_create_scene(scene):
    scene.camera_path()
    scene.make_camera()
    scene.link_camera_path()
    scene.create_lamp()
    scene.key_frame_camera()

    #scene.path_camera()
    #scene.create_camera_path()
    #scene.create_camera()
    #scene.bind_camera_path()
    scene.set_camera_orientation()
    #scene.set_render_options()
    #scene.set_lighting_options()
    scene.set_cycles_options()

@timing
def do_render(render):
    render.render_stills()

@timing
def do_animate(animater):
    animater.animate()

def main():
    # Testing data for camera positioning
    #points = [[0, 27.83998, 28.16131, 200.0000], [10, 27.9000, 28.0000, 5000.0000], [20, 27.99168, 27.85431, 750]]
    #cam = [[11.415, -10.087, -59.376, -111.546], [90.0, -25.0, -65.0, -100.0], [90.0, -25, -65, -100]]

    #points = [[0, 27.9000, 28.16131, 1000], [3, 27.9000, 28.00, 1000], [6, 27.9000, 27.85431, 1000]]
    #cam = [[0, 11.415, -10.087, -59.376, -111.546], [0, 11.415, -10.087, -59.376, -111.546], [0, 11.415, -10.087, -59.376, -111.546]]
    light_ori = [[0, 1.000, -0.300, 0.000, 0.000], [30, 0.750, 0.640, 0.000, 0.000]]
    light_pos = [[0, -8.000, -123.000, 75.000], [60, -8.000, -123.000, 75.000]]

    print("argv: " + sys.argv[7])
    print("------------------------------------------------------------------------------------------")
    json_parse = CZML_Parser(sys.argv[7])

    point, angle = json_parse.blenderCamera()

    print(point)
    print(angle)

    out_file = 'my_test.blend'
    in_file = 'my_image.IMG'
    text_file = 'texture_sb.jpg'

    # Create Class Objects
    file_path = FilePaths(in_file, out_file, text_file)
    blend_config = Blender_Config_Options()
    meta_data = get_meta_data(file_path)
    my_importer = Importer(file_path, blend_config)
    my_scene = BuildScene(blend_config, file_path, meta_data, [point, angle, light_ori, light_pos])

    user_points_converted = []
    for pt in point:
        convert = my_scene.geo_2_pix(pt[1], pt[2], pt[3])
        user_points_converted.append(convert)

    # Execute Class Functions
    do_import(my_importer, blend_config, user_points_converted)
    do_create_scene(my_scene)

    # Save all the options into a blend file
    my_importer.save_scene(out_file)

    render = RenderStills(blend_config, file_path)
    do_render(render)

    animater = AnimateScene(file_path)
    do_animate(animater)


if __name__ == "__main__":
    main()
