from jpl_conf import FilePaths
from jpl_conf import Blender_Config_Options
from create_blend import Importer
from create_scene import BuildScene
from osgeo import gdal, osr
from CzmlParser import CZML_Parser

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
def do_import(in_obj):
    in_obj.clear_blend_file()

    # Importing Functions.
    # Supports IMG, Collada, and OBJ
    #in_obj.import_hirise_img("BIN12-FAST")
    in_obj.import_hirise_img("BIN6")
    #in_obj.import_collada()
    # in_obj.import_obj_file()

    in_obj.select_object()
    #in_obj.set_textured_view()

@timing
def do_create_scene(scene):
    scene.create_lamp()
    scene.create_camera()
    scene.create_camera_path()
    scene.bind_camera_path()
    scene.set_camera_orientation()


def main(json_path=None):
    # Testing data for camera positioning
    points = [[0, 27.83998, 28.16131, 500.0000], [10, 27.9000, 28.0000, 1000.0000], [20, 27.99168, 27.85431, 750]]
    cam = [[11.415, -10.087, -59.376, -111.546], [90.0, -25.0, -65.0, -100.0], [90.0, -25, -65, -100]]

    json_file = json_path
    json_parse = CZML_Parser(json_file)

    point, angle = json_parse.blenderCamera()

    print(points)
    print(angle)

    out_file = 'my_test.blend'
    in_file = 'my_image.IMG'

    file_path = FilePaths(in_file, out_file)
    blend_config = Blender_Config_Options()

    meta_data = get_meta_data(file_path)

    my_importer = Importer(file_path)

    do_import(my_importer)

    my_scene = BuildScene(blend_config, file_path, meta_data, [points, cam])

    do_create_scene(my_scene)

    my_importer.save_scene()


if __name__ == "__main__":
    main(json_path='/home/chrisomlor/MovieDemo/Assets/sample.json')
