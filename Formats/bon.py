import sys
import os.path
from binary_readers import *

def build_yaml(info):
    buf = ""

    if info != None:
        for value in info:
            buf += "- x: {:}\n  y: {:}\n  z: {:}\n".format(value[0],
                                                           value[1],
                                                           value[2])
    
    return buf

def read_info(file_name):
    info = []
    with open(file_name, "rb") as file:
        if file.read(4) == b'\x3C\xE2\x9C\x01':
            print("Unpack as res first")
            file.seek(0)

            from res import read_filetree, unpack_res

            tree = read_filetree(file)
            for element in tree:
                element[0] += ".bon"
            unpack_res(file, tree, file_name)
            
            return
        else:
            file.seek(0)
            for i in range(os.path.getsize(file_name) // 12):
                info.append(read_float(file, 3))

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
        print("Usage: bon.py input.bon [output.yaml]")
