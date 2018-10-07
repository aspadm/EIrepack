import sys
from binary_readers import *

def build_yaml(info):
    keys = ["max_altitude", "x_sectors", "y_sectors", "textures_count",
        "texture_size", "tiles_count", "tile_size", "objects_count",
        "animated_tiles_count"]

    terrain_type = ["undefined", "water_no_texture", "grass", "water"]

    buf = ""
    for i in range(len(keys)):
        buf += keys[i] + ": " + str(info[i]) + "\n"

    if info[7] > 0:
        buf += "map_objects:\n"
        for i in range(info[7]):
            buf += "  - type: \"" + terrain_type[info[9][i][0]] + "\"\n"
            buf += "    color_r: " + str(info[9][i][1]) + "\n"
            buf += "    color_g: " + str(info[9][i][2]) + "\n"
            buf += "    color_b: " + str(info[9][i][3]) + "\n"
            buf += "    opacity: " + str(info[9][i][4]) + "\n"
            buf += "    self_illumination: " + str(info[9][i][5]) + "\n"
            buf += "    wave_multiplier: " + str(info[9][i][6]) + "\n"
            buf += "    warp_speed: " + str(info[9][i][7]) + "\n"
            buf += "    unknown:\n      - " + str(info[9][i][8]) + "\n"
            buf += "      - " + str(info[9][i][9]) + "\n"
            buf += "      - " + str(info[9][i][10]) + "\n"

    buf += "id_array:\n"
    for i in info[10]:
        buf += "  - " + str(i) + "\n"

    if info[8] > 0:
        buf += "animated_tiles:\n"
        for i in info[11]:
            buf += "  - tile_index: " + str(i[0]) + "\n"
            buf += "    animation_phases: " + str(i[1]) + "\n"

    return buf

def read_info(file_name):
    info = []
    with open(file_name, "rb") as file:
        if file.read(4) != b"\x72\xF6\x4A\xCE":
            print("Incorrect magic!")
            return

        info.append(read_float(file))
        info.extend(read_uint(file, 6))
        info.append(read_ushort(file))
        info.append(read_uint(file))

        info.append([])
        for i in range(info[7]):
            info[-1].append([read_uint(file)])
            info[-1][-1].extend(read_float(file, 7))
            info[-1][-1].extend(read_uint(file, 3))

        info.append(read_uint(file, info[5]))

        info.append([read_ushort(file, 2) for i in range(info[8])])

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
        print("Usage: mp.py input.mp [output.yaml]")
