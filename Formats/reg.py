import sys
from binary_readers import *

ENCODE = "cp866"

def build_yaml(tree):
    buf = ""
    for section in tree:
        buf += "{}:\n".format(section[0])
        for key in section[1]:
            buf += "  {}:".format(key[0])
            if type(key[1]) != type([]):
                if type(key[1]) == str:
                    buf += " \"{}\"\n".format(key[1])
                else:
                    buf += " {}\n".format(key[1])
            else:
                buf += "\n"
                for item in key[1]:
                    if type(item) == str:
                        buf += "    - \"{}\"\n".format(item)
                    else:
                        buf += "    - {}\n".format(item)
    return buf[:-1]
                

def print_tree(tree):
    for section in tree:
        print(section[0])
        for key in section[1]:
            print(key[0], "=", key[1])

def read_key(file, key_type):
    count = 1
    if key_type >= 128:
        count = read_ushort(file)
        key_type -= 128

    buf = []
    for i in range(count):
        if key_type == 0:
            buf.append(read_int(file))
        elif key_type == 1:
            buf.append(read_float(file))
        else:
            length = read_ushort(file)
            buf.append(read_str(file, length, ENCODE))
    
    return buf[0] if count == 1 else buf

def read_info(f_name):
    with open(f_name, "rb") as file:
        magic = file.read(4)

        if magic != b'\xFB\x3E\xAB\x45':
            print("Incorrect magic!")
            return

        tree = []
        
        sections_count = read_ushort(file)
        # Read sections offsets
        for i in range(sections_count):
            read_short(file)
            tree.append(["", [], read_uint(file)])
            
        # Read sections names and keys
        for section in tree:
            file.seek(section[2])
            keys_count = read_ushort(file)
            for i in range(keys_count):
                section[1].append(["", 0])
                
            name_len = read_ushort(file)
            section[0] = read_str(file, name_len, ENCODE)

            for key in section[1]:
                read_short(file)
                key[1] = read_uint(file)

            for key in section[1]:
                file.seek(section[2] + key[1])
                key_type = read_byte(file)
                name_len = read_ushort(file)
                key[0] = read_str(file, name_len, ENCODE)
                key[1] = read_key(file, key_type)
        
        return tree

if __name__ == '__main__':
    #print_tree(read_tree("ai.reg"))
    #exit()
    if 2 <= len(sys.argv) <= 3:
        tree = read_info(sys.argv[1])
        
        if len(sys.argv) == 2:
            print(build_yaml(tree))
        else:
            with open(sys.argv[2], "w") as file:
                file.write(build_yaml(tree))
    else:
        print("Usage: reg.py input.reg [output.yaml]")
