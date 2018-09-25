import sec
import mp
import sys
import join_tiles

def convert_map(name):
    map_info = mp.read_info(name + ".mp")

    join_tiles.join_tiles(name + "00", map_info[3])

    with open(name.lower() + ".mtl", "w") as mtl:
        mtl.write("newmtl material_0\nmap_Kd " + name.lower() + ".png\n")
        mtl.write("newmtl material_1\nmap_Kd " + name.lower() + ".png\n")

    for i in range(map_info[2]):
        for j in range(map_info[1]):
            info = sec.read_info(name + "{:03}{:03}.sec".format(i, j))
            
            with open(name + "{:03}{:03}.obj".format(i, j), "w") as file:
                file.write("mtllib ./" + name.lower() + ".mtl\n" + 
                           "usemtl material_0\n" +
                           sec.build_obj([0, info[1][:], info[3 if info[0] else 2][:]],
                                         map_info[0], i, j))

            if info[0] != 0:
                with open(name + "{:03}{:03}_w.obj".format(i, j), "w") as file:
                    file.write("mtllib ./" + name.lower() + ".mtl\n" + 
                               "usemtl material_1\n" +
                               sec.build_obj([0, info[2], info[4], info[5]],
                                             map_info[0], i, j))

if __name__ == '__main__':
    if 2 == len(sys.argv):
        convert_map(sys.argv[1][:-3])
    else:
        print("Usage: convert_map.py input.mp")
