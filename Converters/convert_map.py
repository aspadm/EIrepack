import sec
import mp
import sys
import join_tiles
import numpy as np
import collada as dae

"""
scene -> nodes (position) -> geometry nodes -> geometry data 
"""

def create_geometry(v_arr, t_arr, altitude, tiles_count, water_mask=None):
    vert_buf = []
    norm_buf = []
    
    for i, vert in enumerate(v_arr):
        vert_buf.extend([float(i % 33 + vert[0] / 254),
                        float(i //33 + vert[1] / 254),
                        vert[2] * altitude / 65535])
        norm_buf.extend(vert[3:6])

    tex_buf = []

    # Текстурные координаты
    for i in range(32, -1, -1):
        for j in range(65):
            tex_buf.extend([j / 64, i / 32])

    ind_buf = []

    for j in range(16):
        for i in range(16):
            if water_mask != None:
##                if water_mask[j*16 + i] == 0:
##                    continue
                if water_mask[j*16 + i] == 65535:
                    for y in range(2):
                        for x in range(2):
                            ind_buf.extend([33 + j * 66 + y * 33 + i * 2 + x,
                                            33 + j * 66 + y * 33 + i * 2 + x,
                                            0,
                                            j * 66 + y * 33 + i * 2 + x,
                                            j * 66 + y * 33 + i * 2 + x,
                                            0,
                                            1  + j * 66 + y * 33 + i * 2 + x,
                                            1  + j * 66 + y * 33 + i * 2 + x,
                                            0])
                            ind_buf.extend([1  + j * 66 + y * 33 + i * 2 + x,
                                            1  + j * 66 + y * 33 + i * 2 + x,
                                            0,
                                            34 + j * 66 + y * 33 + i * 2 + x,
                                            34 + j * 66 + y * 33 + i * 2 + x,
                                            0,
                                            33 + j * 66 + y * 33 + i * 2 + x,
                                            33 + j * 66 + y * 33 + i * 2 + x,
                                            0])
                    continue
                #else:
                #    print(water_mask[j*16 + i])
            tex_p = t_arr[j * 16 + i]
            index = tex_p[1] * 64 + tex_p[0]
            tex_c = [    index % 32 * 2 + index // 32 * 130,
                     1 + index % 32 * 2 + index // 32 * 130,
                     2 + index % 32 * 2 + index // 32 * 130,
                         index % 32 * 2 + index // 32 * 130 + 65,
                     1 + index % 32 * 2 + index // 32 * 130 + 65,
                     2 + index % 32 * 2 + index // 32 * 130 + 65,
                         index % 32 * 2 + index // 32 * 130 + 130,
                     1 + index % 32 * 2 + index // 32 * 130 + 130,
                     2 + index % 32 * 2 + index // 32 * 130 + 130]
            if tex_p[2] == 3:
                tex_c = [tex_c[6], tex_c[3], tex_c[0],
                         tex_c[7], tex_c[4], tex_c[1],
                         tex_c[8], tex_c[5], tex_c[2]]
            elif tex_p[2] == 2:
                tex_c = [tex_c[8], tex_c[7], tex_c[6],
                         tex_c[5], tex_c[4], tex_c[3],
                         tex_c[2], tex_c[1], tex_c[0]]
            elif tex_p[2] == 1:
                tex_c = [tex_c[2], tex_c[5], tex_c[8],
                         tex_c[1], tex_c[4], tex_c[7],
                         tex_c[0], tex_c[3], tex_c[6]]
            for y in range(2):
                for x in range(2):
                    ind_buf.extend([33 + j * 66 + y * 33 + i * 2 + x,
                                    33 + j * 66 + y * 33 + i * 2 + x,
                                    tex_c[(y + 1) * 3 + x],
                                    j * 66 + y * 33 + i * 2 + x,
                                    j * 66 + y * 33 + i * 2 + x,
                                    tex_c[y * 3 + x],
                                    1  + j * 66 + y * 33 + i * 2 + x,
                                    1  + j * 66 + y * 33 + i * 2 + x,
                                    tex_c[y * 3 + (x + 1)]])
                    ind_buf.extend([1  + j * 66 + y * 33 + i * 2 + x,
                                    1  + j * 66 + y * 33 + i * 2 + x,
                                    tex_c[y * 3 + (x + 1)],
                                    34 + j * 66 + y * 33 + i * 2 + x,
                                    34 + j * 66 + y * 33 + i * 2 + x,
                                    tex_c[(y + 1) * 3 + (x + 1)],
                                    33 + j * 66 + y * 33 + i * 2 + x,
                                    33 + j * 66 + y * 33 + i * 2 + x,
                                    tex_c[(y + 1) * 3 + x]])
            
    return vert_buf, norm_buf, tex_buf, ind_buf

def prepare_nodes(mesh, mat, i, j, name, v_arr, t_arr, altitude, tiles_count, water_mask=None):
    subname = "land" if water_mask == None else "liquid"

    # convert sector data
    vert, norm, tex, ind = create_geometry(v_arr, t_arr, altitude, tiles_count, water_mask)
    #print(i, j, len(ind))
    # prepare geometry data
    vert_source = dae.source.FloatSource("vert_arr", np.array(vert),
                                         ("X", "Y", "Z"))
    norm_source = dae.source.FloatSource("norm_arr", np.array(norm),
                                         ("X", "Y", "Z"))
    tex_source = dae.source.FloatSource("tex_arr", np.array(tex),
                                        ("S", "T"))
    ind_source = np.array(ind)

    # create empty mesh
    geom = dae.geometry.Geometry(mesh, subname + "_{:03}_{:03}".format(i, j),
                                 subname + " sector {:03}:{:03}".format(i, j),
                                 [vert_source, norm_source, tex_source])

    # describe mesh data structure
    input_list = dae.source.InputList()
    input_list.addInput(0, "VERTEX", "#vert_arr")
    input_list.addInput(1, "NORMAL", "#norm_arr")
    input_list.addInput(2, "TEXCOORD", "#tex_arr")

    # generate geometry data
    triset = geom.createTriangleSet(ind_source, input_list, "mapmaterial0")
    geom.primitives.append(triset)
    mesh.geometries.append(geom)

    # map sector offset
    pos = dae.scene.TranslateTransform(32 * i, 32 * j, 0)
    # reinstance material
    matnode = dae.scene.MaterialNode("mapmaterial0", mat, inputs=[])
    # add sector geometries to map node
    geomnodes = [dae.scene.GeometryNode(geom, [matnode])]

    return dae.scene.Node(name + "_" + subname + "_{:03}_{:03}".format(i, j),
                                children=geomnodes, transforms=[pos])

def convert_map(name):
    map_name = name.split("\\")[-1].split("/")[-1]
    
    # common info about map
    map_info = mp.read_info(name + ".mp")

    # join tile textures in one atlas
    join_tiles.join_tiles(name + "00", map_info[3])

    # common information
    contrib = dae.asset.Contributor(authoring_tool="EIrepack",
                                    copyright="Only for educational purposes")
    asset = dae.asset.Asset(upaxis=dae.asset.UP_AXIS.Z_UP, title=map_name,
                            contributors=[contrib], unitname="meter",
                            unitmeter=1)

    # create empty collada mesh
    mesh = dae.Collada()
    mesh.assetInfo = asset

    
    mats = []
    for i in range(map_info[7]):
        # create texture material
        image = dae.material.CImage("maptexture{:}".format(i),
                                    "./" + map_name.lower() + ".png")
        surface = dae.material.Surface("maptexture_surface{:}".format(i),
                                       image)
        sampler2d = dae.material.Sampler2D("maptexture_sampler{:}".format(i),
                                           surface)
        texmap = dae.material.Map(sampler2d, "UVSET0")
        
        effect = dae.material.Effect("effect{:}".format(i),
                                     [surface, sampler2d], "blinn",
                                     diffuse=texmap if map_info[9][i][0] != 0\
                                     else (map_info[9][i][1],
                                           map_info[9][i][2],
                                           map_info[9][i][3]),
                                     transparency=map_info[9][i][4],
                                     ambient=(map_info[9][i][1],
                                           map_info[9][i][2],
                                           map_info[9][i][3]),
                                     specular=(map_info[9][i][1],
                                           map_info[9][i][2],
                                           map_info[9][i][3]))
        mat = dae.material.Material("material{:}".format(i),
                                    "mapmaterial{:}".format(i), effect)

        # add material in mesh
        mesh.effects.append(effect)
        mesh.materials.append(mat)
        mesh.images.append(image)

        mats.append(mat)

    nodes = []
    liquid_nodes = []

    # convert map chunks
    for i in range(map_info[1]):
        for j in range(map_info[2]):
            # read map sector
            info = sec.read_info(name + "{:03}{:03}.sec".format(i, j))

            
            nodes.append(prepare_nodes(mesh, mat, i, j, name, info[1][:],
                                       info[3 if info[0] else 2][:],
                                       map_info[0], map_info[5]))
##info[1][:],
##                                           info[3 if info[0] else 2][:],
##                                           map_info[0],
##                                           map_info[5]
            
##            nodes.append(prepare_nodes(i, j, name, v_arr, t_arr, altitude,
##                                       tiles_count))
            if info[0] != 0:
                liquid_nodes.append(prepare_nodes(mesh, mat, i, j, name, info[2][:],
                                    info[4][:],
                                    map_info[0], map_info[5], info[5]))
##            if info[0] != 0:
##                geomnodes.append(create_geometry("liquid_{:03}_{:03}".format(i, j),
##                                                 info[2],
##                                                 info[4], info[5],
##                                                 map_info[0]))

    # add base light
    sun = dae.light.DirectionalLight("Sun", (1, 1, 1))
    mesh.lights.append(sun)
    terrain_node = dae.scene.Node("lanscape", children=nodes)
    liquid_node = dae.scene.Node("liquid", children=liquid_nodes)
    sun_node = dae.scene.Node("sunshine", children=[dae.scene.LightNode(sun)],
                                transforms=[dae.scene.MatrixTransform(np.array(
                                    [1, 0, 0, 0,
                                     0, 1, 0, 0,
                                     0, 0, 1, 0,
                                     0, 0, 0, 1]))])
    # create main scene
    myscene = dae.scene.Scene(map_name, [sun_node, terrain_node, liquid_node])
    mesh.scenes.append(myscene)
    mesh.scene = myscene

    # finalyze and save mesh
    mesh.write(name + ".dae")

if __name__ == '__main__':
    if 2 == len(sys.argv):
        convert_map(sys.argv[1][:-3])
    else:
        print("Usage: convert_map.py input.mp")
