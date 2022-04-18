import bpy
import random

def clean_scene():
    for obj in bpy.data.objects:
        bpy.data.objects.remove(obj)

    for mat in bpy.data.materials:
        bpy.data.materials.remove(mat)


clean_scene()

# function needed to use loopcuts
def get_context_override():
    win      = bpy.context.window
    scr      = win.screen
    areas3d  = [area for area in scr.areas if area.type == 'VIEW_3D']
    region   = [region for region in areas3d[0].regions if region.type == 'WINDOW']

    override = {'window':win,
                'screen':scr,
                'area'  :areas3d[0],
                'region':region[0],
                'scene' :bpy.context.scene,
                }

    return override






def change_to_edit_mode():
    #bpy.ops.object.editmode_toggle()
    bpy.ops.object.mode_set(mode = "EDIT")

def change_to_object_mode():
    #bpy.ops.object.editmode_toggle()
    bpy.ops.object.mode_set(mode = "OBJECT")


def create_cube(cube_size = 1):
    # Add cube 
    bpy.ops.mesh.primitive_cube_add(size=cube_size, enter_editmode=False, align='WORLD', location=(0, 0, 0), scale=(1, 1, 1))

    x_size = random.uniform(0.15, 0.3)
    y_size = random.uniform(0.75, 0.90)
    z_size = random.uniform(1.15, 1.3)

    resize_cube(x_size, y_size, z_size)
    align_sides(x_size, y_size, z_size)

    return bpy.context.selected_objects[0]


def create_random_sizes_for_axes():
    pass


def align_sides(x_height, y_height, z_heigt):
    # Place obect on top of xy-plane
    bpy.ops.transform.translate(value=(x_height * 0.5, y_height * 0.5, z_heigt * 0.5), orient_axis_ortho='X', orient_type='GLOBAL', orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)), orient_matrix_type='GLOBAL', constraint_axis=(False, False, True), mirror=False, use_proportional_edit=False, proportional_edit_falloff='SMOOTH', proportional_size=1, use_proportional_connected=False, use_proportional_projected=False)
    pass

def resize_cube(scale_x, scale_y, scale_z):
    bpy.ops.transform.resize(value=(scale_x, scale_y, scale_z), orient_type='GLOBAL', orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)), orient_matrix_type='GLOBAL', constraint_axis=(True, False, False), mirror=False, use_proportional_edit=False, proportional_edit_falloff='SMOOTH', proportional_size=1, use_proportional_connected=False, use_proportional_projected=False)

    


def make_loopcut(number_of_cuts, edge_index, offset):
    context_override = get_context_override()
    bpy.ops.mesh.loopcut_slide(context_override, 
        MESH_OT_loopcut={"number_cuts":number_of_cuts,
                         "smoothness":0,
                         "falloff":'INVERSE_SQUARE',
                         "object_index":0,
                         "edge_index":edge_index,
                         "mesh_select_mode_init":(False, False, True)},
        TRANSFORM_OT_edge_slide={"value":offset,
                                 "single_side":False,
                                 "use_even":False,
                                 "flipped":False,
                                 "use_clamp":True,
                                 "mirror":True,
                                 "snap":False,
                                 "snap_target":'CLOSEST',
                                 "snap_point":(0, 0, 0), "snap_align":False, "snap_normal":(0, 0, 0), "correct_uv":True, "release_confirm":False, "use_accurate":False})



def place_loopcuts():
    change_to_edit_mode()
        
    make_loopcut(1, 8, -0.7)
    
    make_loopcut(1, 15, 0)

    make_loopcut(2, 11 ,0)
    
    #Reposition the above loopcut
    resize_cube(2,1,1)
    
    change_to_object_mode()
    

def update_mesh(obj):
    bpy.ops.object.mode_set(mode = "OBJECT")
    obj.data.update(calc_edges=False)

def get_faces(book):
    top_face = None
    bottom_face = None
    front_face = None

    update_mesh(book)
    print(len(book.data.polygons))
    for face in book.data.polygons:
        #print(dir(face))
        face_normal = face.normal
        face_area = face.area
        print(face.normal)
        
        # identify the top face
        # the top face faces into positive z-axis 
        # normal in z-direction is third element of face_normal vector
        if round(face_normal[2]) == 1:
            if top_face == None:
                top_face = face
            else:
                if top_face.area < face.area:
                    top_face = face

    # identify the bottom face
        if round(face_normal[2]) == -1:
            if bottom_face == None:
                bottom_face = face
            else:
                if bottom_face.area < face.area:
                    bottom_face = face


    # identify the front face
        if round(face_normal[1]) == -1:
            if front_face == None:
                front_face = face
            else:
                if front_face.area < face.area:
                    front_face = face

    #print(top_face.area, bottom_face.area, front_face.area)



    return top_face, bottom_face, front_face


def select_faces(obj, faces_indexes):
    bpy.ops.object.mode_set(mode = "EDIT")
    bpy.ops.mesh.select_all(action = "DESELECT")

    bpy.ops.object.mode_set(mode = "OBJECT")

    for face_index in faces_indexes:
        obj.data.polygons[face_index].select = True


def extrude_along_normals(value):
   change_to_edit_mode()
   bpy.ops.mesh.extrude_region_shrink_fatten(MESH_OT_extrude_region=
    {"use_normal_flip":False,
     "use_dissolve_ortho_edges":False,
     "mirror":False},
    TRANSFORM_OT_shrink_fatten=
    {"value":value,
     "use_even_offset":False,
     "mirror":False,
     "use_proportional_edit":False,
     "proportional_edit_falloff":'SMOOTH',
     "proportional_size":1,
     "use_proportional_connected":False,
     "use_proportional_projected":False,
     "snap":False,
     "snap_target":'CLOSEST',
     "snap_point":(0, 0, 0),
     "snap_align":False,
     "snap_normal":(0, 0, 0),
     "release_confirm":False, "use_accurate":False})


def create_material(name_of_material, color):
    material = bpy.data.materials.new(name_of_material)
    material.diffuse_color = color
    

    return material



#####################################################
# Create the book
#####################################################

def create_book():
    book = create_cube()

    place_loopcuts()

    top_face, bottom_face, front_face = get_faces(book)
    print(top_face, bottom_face, front_face)


    select_faces(
        book, 
        [top_face.index, bottom_face.index, front_face.index]
    )

    extrude_along_normals(-0.05)

    # Index slot of material = 0
    cover_material = create_material("cover_material", 
                    (random.uniform(0.0, 1.0),
                     random.uniform(0.0, 1.0),
                     random.uniform(0.0, 1.0),
                     1.0
                    ))
    
    # Add material to object
    book.data.materials.append(cover_material)

    # Index slot of material = 1
    paper_material = create_material("paper_material",
        (0.95,
        0.95,
        0.95,
        1
        ))

    book.data.materials.append(paper_material)
    bpy.context.object.active_material_index = 1
    bpy.ops.object.material_slot_assign()

    change_to_object_mode()



#create_book()

def create_book_shelf(number_of_books):
    
    x_position = 0
    for i in range(number_of_books):
        create_book()
        bpy.ops.transform.translate(value=(x_position, 0, 0), orient_axis_ortho='X', orient_type='GLOBAL', orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)), orient_matrix_type='GLOBAL', constraint_axis=(True, False, False), mirror=False, use_proportional_edit=False, proportional_edit_falloff='SMOOTH', proportional_size=1, use_proportional_connected=False, use_proportional_projected=False)
        # make sure that the next book is placed a distance of the current book away from the current book
        x_position += bpy.context.selected_objects[0].dimensions.x
        # create gap between books
        gap_between_book_on_x_axis = random.uniform(0.01,0.03)
        x_position += gap_between_book_on_x_axis

        # disturb y-position to get an irregular ordering of books
        y_position_random_displacement = random.uniform(-0.05,0.05)
        bpy.ops.transform.translate(value=(0, y_position_random_displacement, 0), orient_axis_ortho='X', orient_type='GLOBAL', orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)), orient_matrix_type='GLOBAL', constraint_axis=(True, False, False), mirror=False, use_proportional_edit=False, proportional_edit_falloff='SMOOTH', proportional_size=1, use_proportional_connected=False, use_proportional_projected=False)




create_book_shelf(50)