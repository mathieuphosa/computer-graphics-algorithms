"""
Exercice correspondant au cours n°3 de Algorithmes géométriques
"""

from Render import *
from tkinter import *

vertices = [Vector3(-1, -1, 1), Vector3(1, -1, 1), Vector3(-1, 1, 1), Vector3(1, 1, 1),
            Vector3(-1, -1, -1), Vector3(1, -1, -1), Vector3(-1, 1, -1), Vector3(1, 1, -1)]

faces = [[0, 1, 3], [0, 3, 2], [4, 5, 1], [4, 1, 0], [4, 2, 6], [4, 0, 2],
          [1, 5, 7], [1, 7, 3], [2, 3, 7], [2, 7, 6], [5, 4, 7], [4, 6, 7]]

triangle_render = list()

perspective_view = False
face_culling = False
filled = False

mouse_pos = [0, 0]
light = Vector3(0.0, 3.0, 0.0)


def rendering(obj, c):
    vec3_list = list()
    S = Scene(-1, 1, 1, -1, 1, -1, 100, 100, -1, 1, 0, 0)
    triangle_render.clear()
    for i in range(len(obj.faces)):
        base_triangle = list()
        for j in range(3):
            if perspective_view:
                m = S.viewport.mul_mat(S.perspective)
                m = m.mul_mat(S.projection)
            else:
                m = S.viewport.mul_mat(S.projection)
            m = m.mul_mat(S.compute_view(camera_position, camera_direction, camera_up))
            m = m.mul_mat(obj.model)
            tmp_vec = m.mul_vect(obj.vertices[obj.faces[i][j]].cart2hom())
            base_triangle.append(obj.vertices[obj.faces[i][j]])
            vec3_list.append(tmp_vec.hom2cart())

        vec_a = base_triangle[1].sub(base_triangle[0])
        vec_b = base_triangle[2].sub(base_triangle[0])
        normal = vec_a.cross(vec_b).normalize().cart2hom()

        if perspective_view:
            m = S.viewport.mul_mat(S.perspective)
            m = m.mul_mat(S.projection)
        else:
            m = S.viewport.mul_mat(S.projection)
        m = m.mul_mat(S.compute_view(camera_position, camera_direction, camera_up))

        normal = m.mul_vect(normal)
        # normal = obj.model.mul_vect(normal)

        normal = normal.hom2cart().normalize()

        color = max(int(normal.dot(light)), 0)

        triangle_render.append(ScreenTriangle(vec3_list[0], vec3_list[1], vec3_list[2], color))
        vec3_list.clear()

        c.create_line([0, 0, 0, 5], tag='mesh', fill='#1f1', width=1)
        c.create_line([0, 0, 5, 0], tag='mesh', fill='#11f', width=1)
    for i in range(len(triangle_render)):
        triangle_render[i].intersect(mouse_pos[0], mouse_pos[1])
        triangle_render[i].render_triangle(c, face_culling, filled)


obj = TriangleMesh(vertices, faces)


def move_right(_):
    canvas.delete("mesh")
    obj.translation(Vector3(0.1, 0, 0))
    rendering(obj, canvas)


def move_left(_):
    canvas.delete("mesh")
    obj.translation(Vector3(-0.1, 0, 0))
    rendering(obj, canvas)


def move_up(_):
    canvas.delete("mesh")
    obj.translation(Vector3(0, -0.1, 0))
    rendering(obj, canvas)


def move_down(_):
    canvas.delete("mesh")
    obj.translation(Vector3(0, 0.1, 0))
    rendering(obj, canvas)


def scale_up_x(_):
    canvas.delete("mesh")
    obj.scale(Vector3(1.1, 1, 1))
    rendering(obj, canvas)


def scale_down_x(_):
    canvas.delete("mesh")
    obj.scale(Vector3(0.9, 1, 1))
    rendering(obj, canvas)


def scale_up_y(_):
    canvas.delete("mesh")
    obj.scale(Vector3(1, 1.1, 1))
    rendering(obj, canvas)


def scale_down_y(_):
    canvas.delete("mesh")
    obj.scale(Vector3(1, 0.9, 1))
    rendering(obj, canvas)


def scale_up_z(_):
    canvas.delete("mesh")
    obj.scale(Vector3(1, 1, 1.1))
    rendering(obj, canvas)


def scale_down_z(_):
    canvas.delete("mesh")
    obj.scale(Vector3(1, 1, 0.9))
    rendering(obj, canvas)


def rotate_plus_x(_):
    canvas.delete("mesh")
    obj.rotation(Vector3(0.1, 0, 0))
    reset_all_labels()
    rendering(obj, canvas)


def rotate_minus_x(_):
    canvas.delete("mesh")
    obj.rotation(Vector3(-0.1, 0, 0))
    reset_all_labels()
    rendering(obj, canvas)


def rotate_plus_y(_):
    canvas.delete("mesh")
    obj.rotation(Vector3(0, 0.1, 0))
    reset_all_labels()
    rendering(obj, canvas)


def rotate_minus_y(_):
    canvas.delete("mesh")
    obj.rotation(Vector3(0, -0.1, 0))
    reset_all_labels()
    rendering(obj, canvas)


def rotate_plus_z(_):
    canvas.delete("mesh")
    obj.rotation(Vector3(0, 0, 0.1))
    reset_all_labels()
    rendering(obj, canvas)


def rotate_minus_z(_):
    canvas.delete("mesh")
    obj.rotation(Vector3(0, 0, -0.1))
    reset_all_labels()
    rendering(obj, canvas)


def reset_view(_):
    canvas.delete("mesh")
    obj.reset()
    reset_all_labels()
    rendering(obj, canvas)


def reset_all_labels():
    reset_label(label)
    reset_label_euler(labelEuler)
    reset_label_angle_axis(labelAngleAxis)
    reset_label_quaternion(labelQuaternion)


def reset_label(lbl):
    lbl.config(text="Rotation matrix\n" + "\n".join([" | ".join([str("{:.2f}".format(y)) for y in x]) for x in obj.rotation_matrix.mat]))


def reset_label_euler(lbl):
    lbl.config(text="Yaw-Pitch-Roll\n" + obj.euler_angles.__str__())


def reset_label_angle_axis(lbl):
    lbl.config(text="Exponentional map\n" + obj.axis.mul(obj.angle).__str__())


def reset_label_quaternion(lbl):
    lbl.config(text="Quaternion\n" + obj.quaternion.__str__())


def move_camera_right(_):
    global camera_position
    canvas.delete("mesh")
    camera_position = camera_position.add(Vector3(0.1, 0, 0))
    rendering(obj, canvas)


def move_camera_left(_):
    global camera_position
    canvas.delete("mesh")
    camera_position = camera_position.add(Vector3(-0.1, 0, 0))
    rendering(obj, canvas)


def move_camera_up(_):
    global camera_position
    canvas.delete("mesh")
    camera_position = camera_position.add(Vector3(0, -0.1, 0))
    rendering(obj, canvas)


def move_camera_down(_):
    global camera_position
    canvas.delete("mesh")
    camera_position = camera_position.add(Vector3(0, 0.1, 0))
    rendering(obj, canvas)


def reset_camera(_):
    global camera_position
    global camera_direction
    global camera_up
    camera_position = Vector3(0, 0, -2)
    camera_direction = Vector3(0, 0, -1)
    camera_up = Vector3(0, 1, 0)
    canvas.delete("mesh")
    rendering(obj, canvas)


def change_view(_):
    global perspective_view
    perspective_view = not perspective_view
    canvas.delete("mesh")
    rendering(obj, canvas)


def change_face_culling(_):
    global face_culling
    face_culling = not face_culling
    canvas.delete("mesh")
    rendering(obj, canvas)


def change_filled(_):
    global filled
    filled = not filled
    canvas.delete("mesh")
    rendering(obj, canvas)


def mouse_motion(event):
    global mouse_pos
    mouse_pos[0] = event.x
    mouse_pos[1] = event.y
    canvas.delete("mesh")
    rendering(obj, canvas)


global camera_position
global camera_direction
global camera_up


root = Tk()

canvas = Canvas(root, width=1000, height=1000)
reset_camera(1)
rendering(obj, canvas)

root.bind("<Right>", move_right)
root.bind("<Left>", move_left)
root.bind("<Up>", move_up)
root.bind("<Down>", move_down)

root.bind("<X>", scale_up_x)
root.bind("<x>", scale_down_x)
root.bind("<Y>", scale_up_y)
root.bind("<y>", scale_down_y)
root.bind("<Z>", scale_up_z)
root.bind("<z>", scale_down_z)

root.bind("<l>", rotate_plus_y)
root.bind("<j>", rotate_minus_y)
root.bind("<i>", rotate_plus_x)
root.bind("<k>", rotate_minus_x)
root.bind("<p>", rotate_plus_z)
root.bind("<m>", rotate_minus_z)

root.bind("<h>", move_camera_right)
root.bind("<f>", move_camera_left)
root.bind("<t>", move_camera_up)
root.bind("<g>", move_camera_down)

root.bind("<R>", reset_view)
root.bind("<r>", reset_camera)
root.bind("<o>", change_view)
root.bind("<c>", change_face_culling)
root.bind("<F>", change_filled)

root.bind("<Motion>", mouse_motion)

label = Label(root, text="")
reset_label(label)
label.pack()

labelEuler = Label(root, text="")
reset_label_euler(labelEuler)
labelEuler.pack()

labelAngleAxis = Label(root, text="")
reset_label_angle_axis(labelAngleAxis)
labelAngleAxis.pack()

labelQuaternion = Label(root, text="")
reset_label_quaternion(labelQuaternion)
labelQuaternion.pack()

canvas.pack()

root.mainloop()
