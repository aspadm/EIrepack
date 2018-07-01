import sys
import os.path
from binary_readers import *

def build_cams(cams):
    buf = ""
    i = 0
    for cam in cams:
        if i != 0:
            buf += "\n"
        buf += "camera_{}:\n".format(i)
        buf += "  position:\n"
        buf += "    x: {}\n    y: {}\n    z: {}\n".format(cam[0][0],
                                                          cam[0][1],
                                                          cam[0][2])
        buf += "  rotation:\n"
        buf += "    w: {}\n    x: {}\n    y: {}\n    z: {}\n".format(cam[1][0],
                                                                     cam[1][1],
                                                                     cam[1][2],
                                                                     cam[1][3])
        i += 1

    return buf

def read_cams(f_name):
    with open(f_name, "rb") as file:
        cams = []
        for i in range(os.path.getsize(f_name) // 36):
            read_uint(file)
            read_uint(file)
            cams.append([])
            cams[i].append(read_float(file, 3))
            cams[i].append(read_float(file, 4))

    return cams

if __name__ == '__main__':
    if 2 <= len(sys.argv) <= 3:
        cams = read_cams(sys.argv[1])
        #print(cams)
        if len(sys.argv) == 2:
            print(build_cams(cams))
        else:
            with open(sys.argv[2], "w") as file:
                file.write(build_cams(cams))
    else:
        print("Usage: cam.py input.cam [output.yaml]")
