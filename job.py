from jpl_conf import FilePaths
from jpl_conf import Blender_Config_Options
from create_blend import Importer
from create_scene import BuildScene
from osgeo import gdal, osr
from CzmlParser import CZML_Parser
import sys
import math

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
    bag = gdal.Open(path.get_import_file_name())
    bag_gtrn = bag.GetGeoTransform()
    bag_proj = bag.GetProjectionRef()
    bag_srs = osr.SpatialReference(bag_proj)
    geo_srs = bag_srs.CloneGeogCS()
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

    return [xy_pts, pix_pts, geo_pts]


def generate_sun(sun):
    uv = unitize(sun)
    return zenith(uv), azimuth(uv)


def unitize(v):
    r = math.sqrt((v[0] * v[0]) + (v[1] * v[1]) + (v[2] * v[2]))
    return v[0] / r, v[1] / r, v[2] / r


def azimuth(u):
    return math.atan2(u[1], u[0])


def zenith(u):
    return math.atan2(u[0], u[2])


@timing
def do_import(in_obj, blend_config):
    in_obj.clear_blend_file()
    objName = "terrain"
    blend_config.set_terrain(objName)

    # Importing Functions.
    #in_obj.import_hirise_img("BIN2")
    #in_obj.import_hirise_img("BIN6", 0.01)
    in_obj.import_hirise_img("BIN12-FAST", 0.01)

    in_obj.set_material_option()
    in_obj.select_object()


@timing
def do_create_scene(scene, split):
    scene.camera_path()
    scene.make_camera()
    scene.create_lamp()
    scene.key_frame_camera()
    scene.set_camera_orientation()
    scene.set_cycles_options()
    scene.set_end_frame()
    split.split_terrain(2, "terrain")


@timing
def do_render(path, config, split, rid):
    input = path.get_cur_working_dir() + "/hadoop/input/"
    #input = path.get_cur_working_dir() + "/hadoop/input/input.txt"
    #f = open(input, 'w')
    frame_count = config.get_end_frame()
    frame_step = config.get_end_frame() if path.get_render_count() > config.get_end_frame() else path.get_render_count()
    start = end = 1
    job_num = 0
    while end < frame_count:
        f = open(input + "input_" + str(job_num) + ".txt", 'w')
        end = start + frame_step
        job_file = split.create_job(start, end, path.get_cur_working_dir() + "/assets/", job_num, 'terrain', path.get_blend_file())
        print("JOB FILE NAME: " + str(job_file))
        f.write(str(start) + " " + str(end) + " " + str(rid) + " " + str(job_file) + " ")

        start = end + 1
        job_num += 1
        f.close()


def main(json=None):
    print(str(sys.argv))

    # Parse JSON input into point, angle and sun_data
    json_parse = CZML_Parser(sys.argv[5])
    point, angle = json_parse.blenderCamera()
    sun_data = json_parse.sundata()

    # Convert Sun Data to usable points of azimuth and zenith
    sun_pos = unitize(sun_data)
    sun_ori = generate_sun(sun_data)

    # Set Filename variables
    out_file = sys.argv[7]
    in_file = sys.argv[9]
    if sys.argv[8] == "None":
        text_file = None
    else:
        text_file = sys.argv[8]

    # Create Class Objects
    file_path = FilePaths(in_file, out_file, text_file)
    blend_config = Blender_Config_Options()
    meta_data = get_meta_data(file_path)
    my_importer = Importer(file_path, blend_config)
    my_scene = BuildScene(blend_config, file_path, meta_data, [point, angle, sun_ori, sun_pos])

    # Set the current working directory for this job
    file_path.set_cur_working_dir(sys.argv[6])

    # Convert Camera locations to blender coordinates
    user_points_converted = []
    for pt in point:
        convert = my_scene.geo_2_pix(float(pt[1]), float(pt[2]), float(pt[3]))
        user_points_converted.append(convert)

    # Execute Class Functions
    do_import(my_importer, blend_config)
    do_create_scene(my_scene, my_importer)

    # Save all the options into a blend file
    my_importer.save_scene(out_file)

    do_render(file_path, blend_config, my_importer, out_file[0:out_file.find('.')])

if __name__ == "__main__":
    main()
