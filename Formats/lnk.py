import sys
from binary_readers import *

def build_level(level, info):
    buf = "  " * level + "- " + info[0]
    if len(info[1]) == 0:
        buf += "\n"
    else:
        buf += ":\n"
        for bone in info[1]:
            buf += build_level(level + 1, bone)

    return buf


def build_yaml(info):
    return build_level(0, info)

def add_child(arr, p_name, name):
    if arr[0] == p_name:
        arr[1].append([name, []])
    else:
        for bone in arr[1]:
            add_child(bone, p_name, name)

def read_info(file_name):
    info = []
    with open(file_name, "rb") as file:
        for i in range(read_uint(file)):
            name_len = read_uint(file)
            name = read_str(file, name_len)

            parent_name_len = read_uint(file)
            if parent_name_len == 0:
                info = [name, []]
            else:
                parent_name = read_str(file, parent_name_len)
                add_child(info, parent_name, name)

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
        print("Usage: lnk.py input.lnk [output.yaml]")
