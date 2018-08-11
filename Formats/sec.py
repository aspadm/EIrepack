import sys
from binary_readers import *

def unpack_normal(normal):
    x = (((normal >> 11) & 0x7FF) - 1000.0) / 1000.0;
    y = ((normal & 0x7FF) - 1000.0) / 1000.0;
    z = (normal >> 22) / 1000.0;

    return [x, y, z]

def build_yaml(info):
    buf = ""

    buf += "water: " + str(info[0]) + "\n"
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
        buf += "water_vertices:\n"
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
        buf += "  - " + str(i) + "\n"
    cur_index += 1

    if info[0] != 0:
        buf += "water_textures:\n"
        for i in info[cur_index]:
            buf += "  - " + str(i) + "\n"
        cur_index += 1

    if info[0] != 0:
        buf += "water_visibility:\n"
        for i in info[cur_index]:
            buf += "  - " + str(i) + "\n"

    return buf

def read_info(file_name):
    info = []
    with open(file_name, "rb") as file:
        if file.read(4) != b"\x74\xF7\x4B\xCF":
            print("Incorrect magic!")
            return

        info.append(read_byte(file))
        info.append([])

        for i in range(1089):
            info[-1].append(read_byte(file, 2))
            info[-1][-1].append(read_ushort(file))
            info[-1][-1].extend(unpack_normal(read_uint(file)))

        if info[0] != 0:
            info.append([])
            for i in range(1089):
                info[-1].append(read_byte(file, 2))
                info[-1][-1].append(read_ushort(file))
                info[-1][-1].extend(unpack_normal(read_uint(file)))

        info.append(read_ushort(file, 256))

        if info[0] != 0:
            info.append(read_ushort(file, 256))

        if info[0] != 0:
            info.append(read_ushort(file, 256))

    return info

if __name__ == '__main__':
    if 2 <= len(sys.argv) <= 3:
        info = read_info(sys.argv[1])
        
        if len(sys.argv) == 2:
            print(build_yaml(info))
        else:
            with open(sys.argv[2], "w") as file:
                file.write(build_yaml(info))
    else:
        print("Usage: sec.py input.sec [output.yaml]")
