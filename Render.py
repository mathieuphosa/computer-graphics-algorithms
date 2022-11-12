from Matrix4 import Matrix4
from Vectors import *
from math import *


class Scene:
    projection: Matrix4
    viewport: Matrix4
    perspective: Matrix4

    def __init__(self, l, r, t, b, n, f, ws, hs, fs, ns, sx, sy):
        self.projection = Matrix4([
            [(2 / (r - l)), 0, 0, (-((r + l) / (r - l)))],
            [0, (2 / (t - b)), 0, (-((t + b) / (t - b)))],
            [0, 0, (-2 / (f - n)), (-((f + n) / (f - n)))],
            [0, 0, 0, 1]
        ])
        self.viewport = Matrix4([
            [ws / 2, 0, 0, sx + (ws / 2)],
            [0, hs / 2, 0, sy + (hs / 2)],
            [0, 0, (fs - ns) / 2, (ns + fs) / 2],
            [0, 0, 0, 1]
        ])
        self.compute_perspective(5, 0, 1)

    def compute_perspective(self, angle_view, far, near):
        d = 1 / (tan(angle_view / 2))
        self.perspective = Matrix4([
            [d, 0, 0, 0],
            [0, d, 0, 0],
            [0, 0, near + far / (near - far), 2 * near * far / (near - far)],
            [0, 0, -1, 0]
        ])

    @staticmethod
    def compute_view(pos, d, up):
        vz = d.normalize().neg()
        vx = d.cross(up).normalize()
        vy = vz.cross(vx)
        camera_matrix = Matrix4([
            [vx.x, vy.x, vz.x, pos.x],
            [vx.y, vy.y, vz.y, pos.y],
            [vx.z, vy.z, vz.z, pos.z],
            [0, 0, 0, 1]
        ])
        return camera_matrix.inv()


class TriangleMesh:
    model: Matrix4

    def __init__(self, vertices, faces):
        self.vertices = vertices
        self.faces = faces
        self.origin_matrix()
        self.rotation_matrix = self.matrix_identity()
        self.euler_angles = Vector3(0, 0, 0)
        self.angle = 0
        self.axis = Vector3(0, 0, 0)
        self.quaternion = Vector4(0, 0, 0, 0)

    def origin_matrix(self):
        self.model = self.matrix_identity()
        self.model.mat[0][3] = 4
        self.model.mat[1][3] = 2.5

    @staticmethod
    def matrix_identity():
        return Matrix4(list([[0 if i != j else 1 for j in range(4)] for i in range(4)]))

    def translation(self, v_translate):
        for i in range(3):
            self.model.mat[i][3] += v_translate.attr_to_list()[i]

    def scale(self, v_scale):
        for i in range(4):
            for j in range(4):
                self.model.mat[i][j] *= v_scale.attr_to_list()[j] if i != 3 and j != 3 else 1

    def rotation(self, v_rotation):
        if v_rotation.x != 0:
            rotation_x = Matrix4([[1, 0, 0, 0], [0, cos(v_rotation.x), -sin(v_rotation.x), 0],
                                  [0, sin(v_rotation.x), cos(v_rotation.x), 0], [0, 0, 0, 1]])
            self.model = self.model.mul_mat(rotation_x)
            self.rotation_matrix = self.rotation_matrix.mul_mat(rotation_x)
        if v_rotation.y != 0:
            rotation_y = Matrix4([[cos(v_rotation.y), 0, sin(v_rotation.y), 0], [0, 1, 0, 0],
                                  [-sin(v_rotation.y), 0, cos(v_rotation.y), 0], [0, 0, 0, 1]])
            self.model = self.model.mul_mat(rotation_y)
            self.rotation_matrix = self.rotation_matrix.mul_mat(rotation_y)
        if v_rotation.z != 0:
            rotation_z = Matrix4(
                [[cos(v_rotation.z), -sin(v_rotation.z), 0, 0], [sin(v_rotation.z), cos(v_rotation.z), 0, 0],
                 [0, 0, 1, 0], [0, 0, 0, 1]])
            self.model = self.model.mul_mat(rotation_z)
            self.rotation_matrix = self.rotation_matrix.mul_mat(rotation_z)

        self.euler_angles.y = atan2(self.rotation_matrix.mat[2][1], self.rotation_matrix.mat[2][2])
        self.euler_angles.x = atan2(-self.rotation_matrix.mat[2][0],
                                    sqrt(self.rotation_matrix.mat[2][1] ** 2 + self.rotation_matrix.mat[2][2] ** 2))
        self.euler_angles.z = atan2(self.rotation_matrix.mat[1][0], self.rotation_matrix.mat[0][0])

        self.angle = acos(round(
            (self.rotation_matrix.mat[0][0] + self.rotation_matrix.mat[1][1] + self.rotation_matrix.mat[2][2] - 1) / 2,
            12))
        divider = sqrt((self.rotation_matrix.mat[2][1] - self.rotation_matrix.mat[1][2]) ** 2 + (
                    self.rotation_matrix.mat[0][2] - self.rotation_matrix.mat[2][0]) ** 2 + (
                                   self.rotation_matrix.mat[1][0] + self.rotation_matrix.mat[0][1]) ** 2)
        divider = divider if divider != 0 else 1
        self.axis.x = (self.rotation_matrix.mat[2][1] - self.rotation_matrix.mat[1][2]) / divider
        self.axis.y = (self.rotation_matrix.mat[0][2] - self.rotation_matrix.mat[2][0]) / divider
        self.axis.z = (self.rotation_matrix.mat[1][0] - self.rotation_matrix.mat[0][1]) / divider

        self.quaternion.x = sqrt(
            1 + self.rotation_matrix.mat[0][0] + self.rotation_matrix.mat[1][1] + self.rotation_matrix.mat[2][2]) / 2
        self.quaternion.y = (self.rotation_matrix.mat[2][1] - self.rotation_matrix.mat[1][2]) / (4 * self.quaternion.x)
        self.quaternion.z = (self.rotation_matrix.mat[0][2] - self.rotation_matrix.mat[2][0]) / (4 * self.quaternion.x)
        self.quaternion.t = (self.rotation_matrix.mat[1][0] - self.rotation_matrix.mat[0][1]) / (4 * self.quaternion.x)

    def reset(self):
        self.origin_matrix()
        self.rotation_matrix = self.matrix_identity()
        self.euler_angles = Vector3(0, 0, 0)
        self.angle = 0
        self.axis = Vector3(0, 0, 0)
        self.quaternion = Vector4(0, 0, 0, 0)


class ScreenTriangle:
    v0: Vector3
    v1: Vector3
    v2: Vector3
    selected: bool
    facing: bool

    def __init__(self, a, b, c, color):
        self.v0 = a
        self.v1 = b
        self.v2 = c
        self.color = color
        self.face_culling()

    def render_triangle(self, canvas, is_face_culling, is_filled):
        if (is_face_culling and self.facing) or not is_face_culling:
            if is_filled:
                canvas.create_polygon([self.v0.x, self.v0.y, self.v1.x, self.v1.y, self.v2.x, self.v2.y], tag='mesh', fill='red' if self.selected else self.from_rgb((self.color, self.color, self.color)))
            else:
                canvas.create_line([self.v0.x, self.v0.y, self.v1.x, self.v1.y, self.v2.x, self.v2.y, self.v0.x, self.v0.y],
                               tag='mesh', fill='red' if self.selected else 'black', width='2' if self.selected else '1')

    def __str__(self):
        return "(v0 = " + str(self.v0) + " / v1 = " + str(self.v1) + " / v2 = " + str(self.v2) + ")"

    @staticmethod
    def sign(p1, p2, p3):
        return (p1.x - p3.x) * (p2.y - p3.y) - (p2.x - p3.x) * (p1.y - p3.y)

    def intersect(self, x, y):
        p = Vector3(x, y, 1)
        d1 = self.sign(p, self.v0, self.v1)
        d2 = self.sign(p, self.v1, self.v2)
        d3 = self.sign(p, self.v2, self.v0)

        has_neg = (d1 < 0) or (d2 < 0) or (d3 < 0)
        has_pos = (d1 > 0) or (d2 > 0) or (d3 > 0)

        if not (has_neg and has_pos):
            self.selected = True
        else:
            self.selected = False

    @staticmethod
    def orientation(seg_a, point):
        seg_b = Segment(seg_a.a, point)
        prod_vect = seg_a.x * seg_b.y - seg_b.x * seg_a.y
        if prod_vect > 0:
            return 4
        elif prod_vect < 0:
            return 5
        else:
            prod_scal = seg_a.x * seg_b.x + seg_a.y * seg_b.y
            if prod_scal < 0:
                return 3
            elif prod_scal <= 1:
                return 1
            else:
                return 2

    def face_culling(self):
        if self.orientation(Segment(self.v0, self.v1), self.v2) == 4:
            self.facing = True
        else:
            self.facing = False

    @staticmethod
    def from_rgb(gray):
        return "#%02x%02x%02x" % gray


class Segment:
    a: Vector3
    b: Vector3
    x: float
    y: float

    def __init__(self, point_a, point_b):
        self.a = point_a
        self.b = point_b
        self.x = self.b.x - self.a.x
        self.y = self.b.y - self.a.y