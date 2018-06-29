from binary_readers import *

def build_tree():
    pass

def print_tree(tree):
    for section in tree:
        print(section[0])
        for key in section[1]:
            print(key[0], "=", key[1])

def read_tree(f_name):
    with open(f_name, "rb") as file:
        magic = file.read(4)

        if magic != b'\xFB\x3E\xAB\x45':
            print("Incorrect magic!")
            return

        tree = []

        sections_count = read_ushort(file);
        
        return tree

if __name__ == '__main__':
    tree = read_tree("autorunpro.reg")
