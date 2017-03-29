import bpy
import bmesh

class Split_Scene:

    def __init__(self, path, blender_config, user_points):
        self.__path = path
        self.__blender_options = blender_config
        self.__user_points = user_points



    def get_object_by_name(self, passedName=""):
        r = None
        obs = bpy.data.objects
        for ob in obs:
            if ob.name == passedName:
                r = ob
        # print(r.name)
        return r

    def split_terrain_by_points(self, user_points, split_count=10, terrain=""):
        ob = self.returnObjectByName(terrain)
        ob.select = True
        bpy.context.scene.objects.active = ob
        bpy.ops.object.mode_set(mode='EDIT')

        bm = bmesh.from_edit_mesh(ob.data)

        location = C.object.location
        dimension = C.object.dimensions

        bbox_corners = [C.object.matrix_world * Vector(corner) for corner in C.object.bound_box]
        print("BBOX_CORNERS")
        print(bbox_corners)

        x_val = 0;
        y_val = 0;
        z_val = 0;

        # Get the correct bounds to account for negative since dimenions only push positives
        for vector_c in bbox_corners:
            v_x = int(vector_c[0])
            v_y = int(vector_c[1])
            v_z = int(vector_c[2])
            print(str(v_x) + " " + str(v_y) + " " + str(v_z))
            if int(dimension[0]) == abs(v_x):
                x_val = v_x
            if int(dimension[1]) == abs(v_y):
                y_val = v_y
            if int(dimension[2]) == abs(v_z):
                z_val = v_z;

        # Used in range must be an integer that isn't 0
        splity = int(y_val / split_count) == 0 and 1 or (int(y_val / 4 - 1))

        print("LOCATION")
        print(location)
        print("DIMENSION")
        print(dimension)
        print("Real Dimensions:X:" +
              str(x_val) + ",Y:" +
              str(y_val) + ",Z:" +
              str(z_val) + " " + "split_units Y:" + str(splity))

        if len(user_points) < 3:
            self.split_special(bm, location, y_val, splity)
        else:
            self.split_user_points(bm, user_points)

    def split_user_points(self, bm, user_points):
        for y in user_points:
            print("y: " + str(y[1]))
            ret = bmesh.ops.bisect_plane(bm, geom=bm.verts[:] + bm.edges[:] + bm.faces[:], plane_co=(0, y[1], 0),
                                         plane_no=(0, 1, 0))
            bmesh.ops.split_edges(bm, edges=[e for e in ret['geom_cut'] if isinstance(e, bmesh.types.BMEdge)])

        bmesh.update_edit_mesh(C.object.data)

        bpy.ops.mesh.separate(type='LOOSE')
        bpy.ops.object.mode_set(mode='OBJECT')

        self.select_object()

    def split_special(self, bm, location, y_val, num_splits):
        # Split mesh along the y-axis where the user points are selected
        for i in range(int(location[1]), y_val, num_splits):
            print("y: " + str(i))
            ret = bmesh.ops.bisect_plane(bm, geom=bm.verts[:] + bm.edges[:] + bm.faces[:], plane_co=(0, i, 0),
                                         plane_no=(0, 1, 0))
            bmesh.ops.split_edges(bm, edges=[e for e in ret['geom_cut'] if isinstance(e, bmesh.types.BMEdge)])

        bmesh.update_edit_mesh(C.object.data)

        bpy.ops.mesh.separate(type='LOOSE')
        bpy.ops.object.mode_set(mode='OBJECT')

        self.select_object()