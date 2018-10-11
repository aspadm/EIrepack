import sys
from binary_readers import *

def unpack_normal(normal):
    x = (((normal >> 11) & 0x7FF) - 1000.0) / 1000.0;
    y = ((normal & 0x7FF) - 1000.0) / 1000.0;
    z = (normal >> 22) / 1000.0;

    return [x, y, z]

def build_yaml(info):
    buf = ""

    buf += "liquids: " + str(info[0]) + "\n"
    buf += "land_vertices:\n"

    cur_index = 1
    for vert in info[cur_index]:
        buf += "  - x_offset: " + str(vert[0]) + "\n"
        buf += "    y_offset: " + str(vert[1]) + "\n"
        buf += "    z_position: " + str(vert[2]) + "\n"
        buf += "    normal_x: " + str(vert[3]) + "\n"
        buf += "    normal_y: " + str(vert[4]) + "\n"
        buf += "    normal_z: " + str(vert[5]) + "\n"
    cur_index += 1

    if info[0] != 0:
        buf += "liquid_vertices:\n"
        for vert in info[cur_index]:
            buf += "  - x_offset: " + str(vert[0]) + "\n"
            buf += "    y_offset: " + str(vert[1]) + "\n"
            buf += "    z_position: " + str(vert[2]) + "\n"
            buf += "    normal_x: " + str(vert[3]) + "\n"
            buf += "    normal_y: " + str(vert[4]) + "\n"
            buf += "    normal_z: " + str(vert[5]) + "\n"
        cur_index += 1

    buf += "land_textures:\n"
    for i in info[cur_index]:
        buf += "  - index: " + str(i[0]) + "\n"
        buf += "    texture: " + str(i[1]) + "\n"
        buf += "    rotation: " + str(i[2]) + "\n"
    cur_index += 1

    if info[0] != 0:
        buf += "liquid_textures:\n"
        for i in info[cur_index]:
            buf += "  - index: " + str(i[0]) + "\n"
            buf += "    texture: " + str(i[1]) + "\n"
            buf += "    rotation: " + str(i[2]) + "\n"
        cur_index += 1

    if info[0] != 0:
        buf += "liquid_material:\n"
        for i in info[cur_index]:
            buf += "  - " + str(i) + "\n"

    return buf

def build_obj(info, altitude, off_x, off_y):
    buf = "# EI map chunk, pos is {};{}. Generated by EIrepack tools.\n".format(
                                                                off_x, off_y)

    # Вершины
    for i, vert in enumerate(info[1]):
        buf += "v {} {} {}\n".format(float(i % 33 + vert[0] / 254 + off_x * 32),
                                     float(i //33 + vert[1] / 254 + off_y * 32),
                                     vert[2] * altitude / 65535)
    # Нормали
    for i, vert in enumerate(info[1]):
        buf += "vn {} {} {}\n".format(vert[3], vert[4], vert[5])
        i += 1

    # Текстурные координаты
    for i in range(32, -1, -1):
        for j in range(65):
            buf += "vt {} {}\n".format(j / 64, i / 32)

    need_water_mask = 0 if len(info) != 4 else 3
    # Генерация полигонов
    for j in range(16):
        for i in range(16):
            if need_water_mask and info[need_water_mask][j*16 + i] != 1:
                continue
            tex_p = info[2 if info[0] == 0 else 3][j * 16 + i]
            index = tex_p[1] * 64 + tex_p[0]
            tex_c = [1 + index % 32 * 2 + index // 32 * 130,
                     2 + index % 32 * 2 + index // 32 * 130,
                     3 + index % 32 * 2 + index // 32 * 130,
                     1 + index % 32 * 2 + index // 32 * 130 + 65,
                     2 + index % 32 * 2 + index // 32 * 130 + 65,
                     3 + index % 32 * 2 + index // 32 * 130 + 65,
                     1 + index % 32 * 2 + index // 32 * 130 + 130,
                     2 + index % 32 * 2 + index // 32 * 130 + 130,
                     3 + index % 32 * 2 + index // 32 * 130 + 130]
            if tex_p[2] == 3:
                tex_c = [tex_c[6], tex_c[3], tex_c[0],
                         tex_c[7], tex_c[4], tex_c[1],
                         tex_c[8], tex_c[5], tex_c[2]]
            elif tex_p[2] == 2:
                tex_c = [tex_c[8], tex_c[7], tex_c[6],
                         tex_c[5], tex_c[4], tex_c[3],
                         tex_c[2], tex_c[1], tex_c[0]]
            elif tex_p[2] == 1:
                tex_c = [tex_c[2], tex_c[5], tex_c[8],
                         tex_c[1], tex_c[4], tex_c[7],
                         tex_c[0], tex_c[3], tex_c[6]]
            for y in range(2):
                for x in range(2):
                    buf += "f {}/{}/{} {}/{}/{} {}/{}/{}\n".format(
                                34 + j * 66 + y * 33 + i * 2 + x,
                                tex_c[(y + 1) * 3 + x],
                                34 + j * 66 + y * 33 + i * 2 + x,
                                1  + j * 66 + y * 33 + i * 2 + x,
                                tex_c[y * 3 + x],
                                1  + j * 66 + y * 33 + i * 2 + x,
                                2  + j * 66 + y * 33 + i * 2 + x,
                                tex_c[y * 3 + (x + 1)],
                                2  + j * 66 + y * 33 + i * 2 + x)
                    buf += "f {}/{}/{} {}/{}/{} {}/{}/{}\n".format(
                                2  + j * 66 + y * 33 + i * 2 + x,
                                tex_c[y * 3 + (x + 1)],
                                2  + j * 66 + y * 33 + i * 2 + x,
                                35 + j * 66 + y * 33 + i * 2 + x,
                                tex_c[(y + 1) * 3 + (x + 1)],
                                35 + j * 66 + y * 33 + i * 2 + x,
                                34 + j * 66 + y * 33 + i * 2 + x,
                                tex_c[(y + 1) * 3 + x],
                                34 + j * 66 + y * 33 + i * 2 + x)
            
    return buf

def make_texture(arr):
    return [[f & 63, (f >> 6) & 255, (f >> 14) & 3] for f in arr]

def read_info(file_name):
    info = []
    with open(file_name, "rb") as file:
        if file.read(4) != b"\x74\xF7\x4B\xCF":
            print("Incorrect magic!")
            return

        info.append(read_byte(file))
        info.append([])

        for i in range(1089):
            info[-1].append(read_char(file, 2))
            info[-1][-1].append(read_ushort(file))
            info[-1][-1].extend(unpack_normal(read_uint(file)))

        if info[0] != 0:
            info.append([])
            for i in range(1089):
                info[-1].append(read_byte(file, 2))
                info[-1][-1].append(read_ushort(file))
                info[-1][-1].extend(unpack_normal(read_uint(file)))

        info.append(make_texture(read_ushort(file, 256)))

        if info[0] != 0:
            info.append(make_texture(read_ushort(file, 256)))

        if info[0] != 0:
            info.append(read_ushort(file, 256))

    return info

if __name__ == '__main__':
    if len(sys.argv) in [3, 4]:
        info = read_info(sys.argv[1])
        
        if len(sys.argv) == 3:
            with open(sys.argv[2], "w") as file:
                file.write(build_yaml(info))
        else:
            with open(sys.argv[3], "w") as file:
                file.write(build_obj(info, int(sys.argv[2]),
                                     int(sys.argv[1][-10:-7]),
                                     int(sys.argv[1][-7:-4])))
    else:
        print("Usage:\nsec.py input.sec altitude output.obj\n\
sec.py input.sec output.yaml")
