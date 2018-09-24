import sec
import mp
import sys

def convert_map(name):
    map_info = mp.read_info(name + ".mp")

    for i in range(map_info[2]):
        for j in range(map_info[1]):
            info = sec.read_info(name + "{:03}{:03}.sec".format(i, j))
            with open(name + "{:03}{:03}.obj".format(i, j), "w") as file:
                file.write(sec.build_obj(info, map_info[0], i, j))

if __name__ == '__main__':
    if 2 == len(sys.argv):
        convert_map(sys.argv[1][:-3])
    else:
        print("Usage: convert_map.py input.mp")
