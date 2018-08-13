import sys
import os.path
from binary_readers import *
from collections import defaultdict

ENCODE = "cp1251"

def add_file(t, path):
    for node in path:
        t = t[node]

def tree():
    return defaultdict(tree)

def dicts(t):
    return {k: dicts(t[k]) for k in t}

buf = ""
def gen_tree(t, depth = 0):
    global buf
    for k in t.keys():
        buf += "{}".format(depth * "  ")
        if len(t[k]) == 0:
            buf += "- "
        buf += "{}".format(k)
        if len(t[k]) != 0:
            buf += ":"
        buf += "\n"
        depth += 1
        gen_tree(t[k], depth)
        depth -= 1

def build_yaml(filetree, f_name):
    global buf
    buf = ""
    
    ftree = tree()
    for file in filetree:
        path = [f_name] + file[0].split("\\")
        add_file(ftree, path)

    gen_tree(ftree)
    
    return buf

def read_filetree(file):
    magic = file.read(4)

    if magic != b'\x3C\xE2\x9C\x01':
        print("Incorrect magic!")
        return
        
    filetree = []
    buf = []

    table_size = read_uint(file)
    table_offset = read_uint(file)
    names_len = read_uint(file)

    file.seek(table_offset)
    for i in range(table_size):
        buf.append(read_uint(file, 4))
        buf[i].append(read_ushort(file))
        buf[i].append(read_uint(file))
    names_offset = file.tell()

    for i in range(table_size):
        file.seek(buf[i][5] + names_offset)
        filetree.append([read_str(file, buf[i][4], ENCODE), buf[i][2], buf[i][1]])

    return filetree

def unpack_res(file, filetree, file_name):
    f_name = file_name[:file_name.rfind(".")]
    for element in filetree:
        name = os.path.dirname(element[0])
        if not os.path.exists(f_name + "\\" + name):
            os.makedirs(f_name + "\\" + name)
        with open(f_name + "\\" + element[0], "wb") as new_file:
            file.seek(element[1])
            buf = file.read(element[2])
            new_file.write(buf)


if __name__ == '__main__':
    if len(sys.argv) == 3:
        with open(sys.argv[1], "rb") as file:
            filetree = read_filetree(file)
        with open(sys.argv[2], "w") as file:
            file.write(build_yaml(filetree, sys.argv[1]))
    elif len(sys.argv) == 2:
        with open(sys.argv[1], "rb") as file:
            filetree = read_filetree(file)
            unpack_res(file, filetree, sys.argv[1])
    else:
        print("Usage: res.py input.res [output.yaml]")
