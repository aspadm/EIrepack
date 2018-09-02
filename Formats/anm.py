import sys
import os.path
from binary_readers import *

def build_yaml(info):
    buf = ""

    buf += "rotation_frames_count: " + str(info[0]) + "\n"
    buf += "rotation_frames:\n"
    for value in info[1]:
        buf += "  - w: {:}\n    x: {:}\n    y: {:}\n    z: {:}\n".format(
            value[0], value[1], value[2], value[3])
    buf += "translation_frames_count: " + str(info[2]) + "\n"
    buf += "translation_frames:\n"
    for value in info[3]:
        buf += "  - x: {:}\n    y: {:}\n    z: {:}\n".format(value[0],
                                                             value[1],
                                                             value[2])
    if info[4] != 0 and info[5] != 0:
        buf += "morphing_frames_count: " + str(info[4]) + "\n"
        buf += "morphing_vertex_count: " + str(info[5]) + "\n"
        buf += "morphing_frames:\n"
        for value in info[6]:
            for i in range(info[5]):
                if i == 0:
                    buf += "  - "
                else:
                    buf += "    "
                buf += "- x: {:}\n      y: {:}\n      z: {:}\n".format(
                    value[i][0], value[i][1], value[i][2])
    
    return buf

def read_info(file_name):
    info = []
    with open(file_name, "rb") as file:
        if file.read(4) == b'\x3C\xE2\x9C\x01':
            print("Unpack as res")
            file.seek(0)

            from res import read_filetree, unpack_res

            tree = read_filetree(file)
            for element in tree:
                element[0] += ".anm"
            unpack_res(file, tree, file_name)
            
            return
        else:
            file.seek(0)
            info.append(read_uint(file))
            info.append([read_float(file, 4) for i in range(info[0])])
            info.append(read_uint(file))
            info.append([read_float(file, 3) for i in range(info[2])])
            info.extend(read_uint(file, 2))
            if info[4] != 0 and info[5] != 0:
                info.append([[read_float(file, 3) for j in range(info[5])] \
                             for i in range(info[4])])

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
        print("Usage: anm.py input.anm [output.yaml]")
