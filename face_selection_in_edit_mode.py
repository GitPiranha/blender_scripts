# You need to be in edit mode

import bpy
import bmesh

obj = bpy.context.edit_object
me = obj.data
bm = bmesh.from_edit_mesh(me)

bm.faces.ensure_lookup_table()

# notice in Bmesh polygons are called faces
bm.faces[0].select = True  # select index 4

# print normal vector of face
print(bm.faces[0].normal)

# Show the updates in the viewport
bmesh.update_edit_mesh(me)