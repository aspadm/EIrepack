import os
import sys
import os.path
from collections import defaultdict

def add_node(t, path):
    for node in path:
        t = t[node]

def tree():
    return defaultdict(tree)

def get_text(f_name):
    with open(f_name, "r") as file:
        buf = file.read()

    while buf[-1] == "\n":
        buf = buf[:-1]
    buf = buf.replace("\n", "\\n")
    buf = buf.replace("\"", "\\\"")

    return buf

def convert_tree(t, f_name, path=""):
    buf = []
    path += " " if path != "" else ""

    for k in t:
        res = convert_tree(t[k], f_name, path + k)
        buf.append([k, res if len(res) > 0 else get_text(os.path.join(f_name, path + k))])
        
    return sorted(buf)

def convert_node(node, buf, level=0):
    for subnode in node:
        buf[0] += "  " * level + subnode[0] + ":"
        if type(subnode[1]) == str:
            buf[0] += " \"" + subnode[1] + "\"\n"
        else:
            buf[0] += "\n"
            convert_node(subnode[1], buf, level + 1)
    
def build_yaml(info):
    buf = [""]
    convert_node(info, buf)
    
    return buf[0]

def read_info(f_name):
    stree = tree()
    arr = sorted(os.listdir(f_name))
    for name in arr:
        if "." in name or "(" in name:
            continue
        add_node(stree, name.lower().split())

    info = convert_tree(stree, f_name)
    
    return info
        

if __name__ == "__main__":
    if 2 <= len(sys.argv) <= 3:
        f_name = "." if len(sys.argv) == 2 else sys.argv[1]

        with open(sys.argv[-1], "w") as file:
            file.write(build_yaml(read_info(f_name)))
    else:
        print("Usage: text.py [input_folder] output.yaml")
