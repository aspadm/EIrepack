import sys
from binary_readers import *

def build_yaml(info):
    keys = ["blocks", "vertex_count", "normal_count", "texcoord_count",
            "index_count", "vertex_component_count", "morph_component_count",
            "group", "texture_number", "center", "min", "max", "radius",
            "vertices", "normals", "texcoords", "indexes", "vertex_components",
            "morph_components"]
    
    buf = ""

    for i in range(len(info)):
        buf += keys[i] + ":"
        if type(info[i]) != list:
            buf += " " + str(info[i]) + "\n"
        else:
            buf += "\n"
            if i in [9, 10, 11]:
                for xyz in info[i]:
                    buf += "  - x: {}\n    y: {}\n    z: {}\n".format(xyz[0],
                                                                      xyz[1],
                                                                      xyz[2])
            elif i == 12:
                for obj in info[i]:
                    buf += "  - " + str(obj) + "\n"
            elif i == 13:
                for n in range(info[0]):
                    buf += "  - variant{}:\n".format(n)
                    for xyz in info[i]:
                        buf += "      - x:\n          - {}\n          \
- {}\n          - {}\n          - {}\n".format(xyz[0][n][0], xyz[0][n][1],
                                               xyz[0][n][2], xyz[0][n][3])
                        buf += "        y:\n          - {}\n          \
- {}\n          - {}\n          - {}\n".format(xyz[1][n][0], xyz[1][n][1],
                                               xyz[1][n][2], xyz[1][n][3])
                        buf += "        z:\n          - {}\n          \
- {}\n          - {}\n          - {}\n".format(xyz[2][n][0], xyz[2][n][1],
                                               xyz[2][n][2], xyz[2][n][3])
            elif i == 14:
                for xyz in info[i]:
                    buf += "  - x:\n      - {}\n      - {}\n      - {}\n\
      - {}\n    y:\n      - {}\n      - {}\n      - {}\n      - {}\n\
    z:\n      - {}\n      - {}\n      - {}\n      - {}\n".format(
                                xyz[0][0], xyz[0][1], xyz[0][2], xyz[0][3],
                                xyz[1][0], xyz[1][1], xyz[1][2], xyz[1][3],
                                xyz[2][0], xyz[2][1], xyz[2][2], xyz[2][3])
            elif i == 15:
                for uv in info[i]:
                    buf += "  - u: {}\n    v: {}\n".format(uv[0], uv[1])
            elif i == 16:
                for v3 in info[i]:
                    buf += "  - - {}\n    - {}\n    - {}\n".format(v3[0],
                                                                   v3[1],
                                                                   v3[2])
            elif i == 17:
                for v3 in info[i]:
                    buf += "  - v: {}\n    vi: {}\n    n: {}\n    ni: {}\
\n    t: {}\n".format(v3[0], v3[1], v3[2], v3[3], v3[4])
            elif i == 18:
                for v2 in info[i]:
                    buf += "  - m: {}\n    v: {}\n".format(v2[0], v2[1])
            else:
                print("WARN!__________", i)
    
    return buf

def read_info(file_name):
    info = []
    with open(file_name, "rb") as file:
        if file.read(3) != b'\x46\x49\x47':
            print("Incorrect magic!")
            return

        n = read_byte(file) - 48
        info.append(n)
        info.extend(read_uint(file, 6))
        read_uint(file)
        info.extend(read_uint(file, 2))
        info[4] //= 3
                
        for i in range(3):
            info.append([read_float(file, 3) for j in range(n)])

        info.append(read_float(file, n))

        # Vertex blocks
        info.append([[[read_float(file, 4) for j in range(n)] for xyz in range(3)] for i in range(info[1])])
        # Normals
        info.append([[read_float(file, 4) for xyzw in range(4)] for i in range(info[2])])

        # UV
        info.append([read_float(file, 2) for j in range(info[3])])
        # Indices
        info.append([read_ushort(file, 3) for i in range(info[4])])

        # Vertex components
        info.append([])
        for i in range(info[5]):
            buf = read_ushort(file, 3)
            info[-1].append([buf[0] >> 2, buf[0] & 3, buf[1] >> 2,
                             buf[1] & 3, buf[2]])
        # Deformation
        info.append([read_ushort(file, 2) for i in range(info[6])])

    return info

if __name__ == '__main__':
    if 2 <= len(sys.argv) <= 3:
        info = read_info(sys.argv[1])
        
        if info != None:
            if len(sys.argv) == 2:
                print(build_yaml(info))
            else:
                with open(sys.argv[2], "w") as file:
                    file.write(build_yaml(info))
    else:
        print("Usage: fig.py input.fig [output.yaml]")
