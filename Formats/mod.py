import sys
import os.path
from binary_readers import *
from res import *

buf = ""

def read_info(file_name):
    with open(file_name, "rb") as file:
        tree = read_filetree(file)
        f_name = os.path.splitext(os.path.basename(file_name))[0]
        for element in tree:
            element[0] += ".fig" if f_name != element[0] else ".lnk"
        unpack_res(file, tree, file_name)


    return tree

if __name__ == '__main__':
    if 2 <= len(sys.argv) <= 3:
        filetree = read_info(sys.argv[1])

        if len(sys.argv) == 3:
            with open(sys.argv[2], "w") as file:
                file.write(build_yaml(filetree, sys.argv[1]))
        else:
            with open(sys.argv[1], "rb") as file:
                unpack_res(file, filetree, sys.argv[1])
    else:
        print("Usage: res.py input.res [output.yaml]")
