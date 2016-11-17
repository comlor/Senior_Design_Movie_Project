import bpy, bmesh
from bpy import context as C

bpy.ops.object.mode_set(mode='EDIT')

bm = bmesh.from_edit_mesh(C.object.data)

#dm = ob.modifiers.new('Decimate', 'DECIMATE')
#dm.ratio = 0.2

edges = []

location = C.object.delta_location
dimension = C.object.dimensions
splits = 3

for i in range(int(location[0]), int(dimension[0]), int(dimension[0]/3)):
        ret = bmesh.ops.bisect_plane(bm, geom=bm.verts[:]+bm.edges[:]+bm.faces[:], plane_co=(i,0,0), plane_no=(1,0,0))
        bmesh.ops.split_edges(bm, edges=[e for e in ret['geom_cut'] if isinstance(e, bmesh.types.BMEdge)])


for i in range(int(location[1]), int(dimension[1]), int(dimension[1]/3)):
        ret = bmesh.ops.bisect_plane(bm, geom=bm.verts[:]+bm.edges[:]+bm.faces[:], plane_co=(0,i,0), plane_no=(0,1,0))
        bmesh.ops.split_edges(bm, edges=[e for e in ret['geom_cut'] if isinstance(e, bmesh.types.BMEdge)])


bmesh.update_edit_mesh(C.object.data)

bpy.ops.mesh.separate(type='LOOSE')
bpy.ops.object.mode_set(mode='OBJECT')

for ob in bpy.data.objects:
        if ob.type == 'MESH':
                dm = ob.modifiers.new('Decimate','DECIMATE')
                dm.ratio = 0.5

