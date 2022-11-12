import math


class Vector2:
    x: float
    y: float

    def __init__(self, *args, **kwargs):
        if args:
            self.x = args[0]
            self.y = args[1]
        elif kwargs and kwargs['points']:
            self.x = kwargs['points'][1].x - kwargs['points'][0].x
            self.y = kwargs['points'][1].y - kwargs['points'][0].y

    def __str__(self):
        return "(x = " + str("{:.2f}".format(self.x)) + ", y = " + str("{:.2f}".format(self.y)) + ")"


class Vector3:
    x: float
    y: float
    z: float

    def __init__(self, *args, **kwargs):
        if args:
            self.x = args[0]
            self.y = args[1]
            self.z = args[2]
        elif kwargs and kwargs['points']:
            self.x = kwargs['points'][1].x - kwargs['points'][0].x
            self.y = kwargs['points'][1].y - kwargs['points'][0].y
            self.z = kwargs['points'][1].z - kwargs['points'][0].z

    def __str__(self):
        return "(x = " + str("{:.2f}".format(self.x)) + ", y = " + str("{:.2f}".format(self.y)) + ", z = " + str("{:.2f}".format(self.z)) + ")"

    def mul(self, k):
        return Vector3(self.x * k, self.y * k, self.z * k)

    def neg(self):
        return self.mul(-1)

    def abs(self):
        return Vector3(abs(self.x), abs(self.y), abs(self.z))

    def length(self):
        return math.sqrt(self.x * self.x + self.y * self.y + self.z * self.z)

    def normalize(self):
        mag = self.length()
        return self.mul(1/mag) if mag != 0 else Vector3(0, 0, 0)

    def add(self, w):
        return Vector3(self.x + w.x, self.y + w.y, self.z + w.z)

    def sub(self, w):
        return self.add(w.neg())

    def dot(self, w):
        return self.x * w.x + self.y * w.y + self.z * w.z

    def cross(self, w):
        return Vector3(self.y * w.z - w.y * self.z, self.z * w.x - w.z * self.x, self.x * w.y - w.x * self.y)

    def print(self):
        print(self)

    def cart2hom(self):
        return Vector4(self.x, self.y, self.z)

    def co_render(self):
        return [self.x, self.y]

    def attr_to_list(self):
        return [self.x, self.y, self.z]


class Vector4:
    x: float
    y: float
    z: float
    t: float = 1

    def __init__(self, *args, **kwargs):
        if args:
            self.x = args[0]
            self.y = args[1]
            self.z = args[2]
            if len(args) == 4:
                self.t = args[3]
        elif kwargs:
            if 'vector3' in list(kwargs.keys()):
                self.x = kwargs['vector3'].x
                self.y = kwargs['vector3'].y
                self.z = kwargs['vector3'].z
            if 'list' in list(kwargs.keys()):
                self.x = kwargs['list'][0]
                self.y = kwargs['list'][1]
                self.z = kwargs['list'][2]
                self.t = kwargs['list'][3]

    def __str__(self):
        return "(x = " + str("{:.2f}".format(self.x)) + ", y = " + str("{:.2f}".format(self.y)) + ", z = " + str("{:.2f}".format(self.z)) + ", t = " + str("{:.2f}".format(self.t)) + ")"

    def hom2cart(self):
        return Vector3(self.x/self.t, self.y/self.t, self.z/self.t)

    def print(self):
        return print(self)

    def attr_to_list(self):
        return [self.x, self.y, self.z, self.t]
