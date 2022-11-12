import itertools
from Vectors import Vector4


class Matrix4:

    def __init__(self, *args):
        self.mat = [[0.0] * 4 for _ in range(4)]
        if args:
            self.mat = list(args[0])

    def sum_mat(self, m):
        return Matrix4([list(map(lambda x, y: x + y, self.mat[i], m.mat[i])) for i in range(4)])

    def mul_scal(self, k):
        return Matrix4([j * k for j in i] for i in self.mat)

    def mul_mat(self, n):
        return Matrix4([[sum(list(map(lambda x, y: x * y, self.mat[i], n.column(j)))) for j in range(4)] for i in range(4)])

    def mul_vect(self, v):
        return Vector4(list=[sum(list(map(lambda x, y: x * y, self.mat[i], v.attr_to_list()))) for i in range(4)])

    def column(self, i):
        return [row[i] for row in self.mat]

    def __str__(self):
        return str([x for x in self.mat])

    def print(self):
        print(self)

    # TODO : Optimiser ça (pour le plaisir de l'optimisation)
    def det_mat3(self, m):
        return (m[0][0] * m[1][1] * m[2][2] + m[0][1] * m[1][2] * m[2][0] + m[0][2] * m[1][0] * m[2][1]
                - m[0][2] * m[1][1] * m[2][0] - m[0][1] * m[1][0] * m[2][2] - m[0][0] * m[1][2] * m[2][1])

    def inv(self):
        m = self.mat
        determinant = Matrix4.get_matrix_determinant(m)
        # special case for 2x2 matrix:
        if len(m) == 2:
            return [[m[1][1] / determinant, -1 * m[0][1] / determinant],
                    [-1 * m[1][0] / determinant, m[0][0] / determinant]]

        # find matrix of cofactors
        cofactors = list()
        for r in range(len(m)):
            cofactorRow = list()
            for c in range(len(m)):
                minor = Matrix4.get_matrix_minor(m, r, c)
                cofactorRow.append(((-1) ** (r + c)) * Matrix4.get_matrix_determinant(minor))
            cofactors.append(cofactorRow)
        cofactors = Matrix4.transpose_matrix(cofactors)
        for r in range(len(cofactors)):
            for c in range(len(cofactors)):
                cofactors[r][c] = cofactors[r][c] / determinant
        return Matrix4(cofactors)

    @staticmethod
    def transpose_matrix(m):
        return list(map(list,zip(*m)))

    @staticmethod
    def get_matrix_minor(m, i, j):
        return [row[:j] + row[j + 1:] for row in (m[:i] + m[i + 1:])]

    @staticmethod
    def get_matrix_determinant(m):
        # base case for 2x2 matrix
        if len(m) == 2:
            return m[0][0] * m[1][1] - m[0][1] * m[1][0]

        determinant = 0
        for c in range(len(m)):
            determinant += ((-1) ** c) * m[0][c] * Matrix4.get_matrix_determinant(Matrix4.get_matrix_minor(m, 0, c))
        return determinant
