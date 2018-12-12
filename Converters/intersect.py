# Векторное произведение
def cross(v1, v2):
    return [v1[1] * v2[2] - v1[2] * v2[1],
            v1[2] * v2[0] - v1[0] * v2[2],
            v1[0] * v2[1] - v1[1] * v2[0]]

# Скалярное произведение
def dot(v1, v2):
    return v1[0] * v2[0] + v1[1] * v2[1] + v1[2] * v2[2]

# Разность векторов
def sub(v1, v2):
    return [v1[0] - v2[0], v1[1] - v2[1], v1[2] - v2[2]]

# Нахождение координаты Z на треугольнике по координатам X, Y
# Thömas Moller, Ben Trumbore: fast minimal storage ray triangle intersection
def get_z(x, y, vert0, vert1, vert2):
    orig = [x, y, 0]
    direction = [0, 0, 1]

    edge1 = sub(vert1, vert0)
    edge2 = sub(vert2, vert0)

    pvec = cross(direction, edge2)
    det = dot(edge1, pvec)

    # Треугольник - вертикален
    if -0.00001 < det < 0.00001:
        return 0.0

    tvec = sub(orig, vert0)
    u = dot(tvec, pvec) / det

    # Пересечение вне треугольника
    if u < 0.0 or u > 1.0:
        return -1.0

    qvec = cross(tvec, edge1)
    v = dot(direction, qvec) / det

    # Пересечение вне треугольника
    if v < 0.0 or u + v > 1.0:
        return -1.0

    return dot(edge2, qvec) / det
