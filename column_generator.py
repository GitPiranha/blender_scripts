# You need to be in edit mode
# Nothing should be selected

import bpy
import bmesh
import random # to create random numbers with randint
import mathutils # to create vectors



##################################################################
# define constants
##################################################################

BEVEL_OFFSET = 0.05

RANDOM_INTEGER_MIN = 2
RANDOM_INTEGER_MAX = 5

SCALE_FACTOR = 0.2


CREATE_MULTIPLE_COLUMNS = True




##################################################################
# vector which points into the positive x, y and z directions
##################################################################

vector_normal_x = mathutils.Vector((1.0, 0.0, 0.0))

vector_normal_y = mathutils.Vector((0.0, 1.0, 0.0))

vector_normal_z = mathutils.Vector((0.0, 0.0, 1.0))



##################################################################
# Select object in scene and make it available to bmesh
##################################################################


obj = bpy.context.edit_object
me = obj.data
bm = bmesh.from_edit_mesh(me)

bm.faces.ensure_lookup_table()


#select_object_in_scene_to_process_in_bmesh()




# Loop through all faces and select face which points into positive x-axis
for i in range(len(bm.faces)):
    print("face", i, "selected")
    print(bm.faces[i].normal)
    
    if bm.faces[i].normal == vector_normal_x:
        print(" good face")
        bm.faces[i].select = True


# Create random integers
def create_random_integer():
    return random.randint(RANDOM_INTEGER_MIN,
                          RANDOM_INTEGER_MAX)

# Extrude selected faces    
def extrude_face(length_extrusion = create_random_integer()):
    bpy.ops.mesh.extrude_region_move(MESH_OT_extrude_region={"use_normal_flip":False, "use_dissolve_ortho_edges":False, "mirror":False},
    TRANSFORM_OT_translate={"value":(0, 0, length_extrusion), "orient_axis_ortho":'X', "orient_type":'NORMAL', "orient_matrix":((0, 1, 0), (0, 0, 1), (1, 0, 0)),
    "orient_matrix_type":'NORMAL', "constraint_axis":(False, False, True), "mirror":False, "use_proportional_edit":False, "proportional_edit_falloff":'SMOOTH', "proportional_size":1, "use_proportional_connected":False, "use_proportional_projected":False, "snap":False, "snap_target":'CLOSEST', "snap_point":(0, 0, 0), "snap_align":False, "snap_normal":(0, 0, 0), "gpencil_strokes":False, "cursor_transform":False, "texture_space":False, "remove_on_cancel":False, "view2d_edge_pan":False, "release_confirm":False, "use_accurate":False, "use_automerge_and_split":False})


def scale_face(factor_scaling):
    bpy.ops.transform.resize(value=(factor_scaling, factor_scaling, factor_scaling),
    orient_type='GLOBAL', orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)),
    orient_matrix_type='GLOBAL', mirror=True, use_proportional_edit=False,
    proportional_edit_falloff='SMOOTH', proportional_size=1, use_proportional_connected=False, use_proportional_projected=False)


def inset_face(thickness_inset):
    bpy.ops.mesh.inset(thickness=thickness_inset, depth=0)


def select_all_faces():
    bpy.ops.mesh.select_all(action='SELECT')


def deselect_all_faces():
    bpy.ops.mesh.select_all(action='DESELECT')


def bevel_whole_object(offset_bevel=0.05):
    bpy.ops.mesh.bevel(offset=offset_bevel, offset_pct=0, affect='EDGES')



# Insert middle part of column
def insert_middle_part(extrude_factor=0.5, scale_factor=0.7):
    extrude_face(extrude_factor)
    scale_face(scale_factor)
    extrude_face(2.0)
    extrude_face(extrude_factor)
    scale_face(1/scale_factor)



# Here we define a funtion to create the column
def create_column():

    extrude_face()
    
    insert_middle_part(scale_factor = SCALE_FACTOR)
    
    extrude_face()

    insert_middle_part(scale_factor = SCALE_FACTOR)

    extrude_face()

    # Add end part because start cube is also 2 metres
    extrude_face(2)


##################################################################
# Create the column
##################################################################

create_column()






##################################################################
# Reselect the current object in scene
##################################################################

obj = bpy.context.edit_object
me = obj.data
bm = bmesh.from_edit_mesh(me)

bm.faces.ensure_lookup_table()

##################################################################
# Loop through all faces and select face which points into positive and negative y-axis
##################################################################

deselect_all_faces()
for i in range(len(bm.faces)):
    print("face", i, "selected")
    print(bm.faces[i].normal)
    
    if bm.faces[i].normal == vector_normal_y:
        print(" good face")
        bm.faces[i].select = True

    if bm.faces[i].normal == (vector_normal_y * (-1.0)):
        print(" good face")
        bm.faces[i].select = True

##################################################################
# extrude faces in positive y-direction
##################################################################

#bpy.ops.mesh.extrude_region_move(MESH_OT_extrude_region={"use_normal_flip":False, "use_dissolve_ortho_edges":False, "mirror":False}, TRANSFORM_OT_translate={"value":(0, 0, 10.1748), "orient_axis_ortho":'X', "orient_type":'NORMAL', "orient_matrix":((-0.127971, 0, 0.991778), (0.991778, -0, 0.127971), (0, 1, 0)), "orient_matrix_type":'NORMAL', "constraint_axis":(False, False, True), "mirror":False, "use_proportional_edit":False, "proportional_edit_falloff":'SMOOTH', "proportional_size":1, "use_proportional_connected":False, "use_proportional_projected":False, "snap":False, "snap_target":'CLOSEST', "snap_point":(0, 0, 0), "snap_align":False, "snap_normal":(0, 0, 0), "gpencil_strokes":False, "cursor_transform":False, "texture_space":False, "remove_on_cancel":False, "view2d_edge_pan":False, "release_confirm":False, "use_accurate":False, "use_automerge_and_split":False})

##################################################################
# Scale in both the positive and negative y-direction
##################################################################

#bpy.ops.mesh.extrude_region_shrink_fatten(MESH_OT_extrude_region={"use_normal_flip":False, "use_dissolve_ortho_edges":False, "mirror":False}, TRANSFORM_OT_shrink_fatten={"value":7.33042, "use_even_offset":False, "mirror":False, "use_proportional_edit":False, "proportional_edit_falloff":'SMOOTH', "proportional_size":1, "use_proportional_connected":False, "use_proportional_projected":False, "snap":False, "snap_target":'CLOSEST', "snap_point":(0, 0, 0), "snap_align":False, "snap_normal":(0, 0, 0), "release_confirm":False, "use_accurate":False})







#select_all_faces()
#bevel_whole_object()






#inset_face(0.1)


# notice in Bmesh polygons are called faces
#bm.faces[0].select = True  # select index 4

# print normal vector of face
#print(bm.faces[0].normal)

# Show the updates in the viewport
bmesh.update_edit_mesh(me)