import sec
import mp
import sys
import join_tiles
import numpy as np
import collada as dae
from intersect import get_z

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
    t_ind_used = []
    for v in t_arr:
        tmp = v[1] * 64 + v[0]
        if tmp < 512 and tmp not in t_ind_used:
            t_ind_used.append(tmp)
            
    for i in t_ind_used:
        tex_buf.extend([[i % 32 / 32 + 0.00390625, 1 - (i // 32 / 16 + 0.0078125)],
                        [i % 32 / 32 + 0.015625, 1 - (i // 32 / 16 + 0.0078125)],
                        [i % 32 / 32 + 0.02734375, 1 - (i // 32 / 16 + 0.0078125)],

                        [i % 32 / 32 + 0.00390625, 1 - (i // 32 / 16 + 0.03125)],
                        [i % 32 / 32 + 0.015625, 1 - (i // 32 / 16 + 0.03125)],
                        [i % 32 / 32 + 0.02734375, 1 - (i // 32 / 16 + 0.03125)],

                        [i % 32 / 32 + 0.00390625, 1 - (i // 32 / 16 + 0.0546875)],
                        [i % 32 / 32 + 0.015625, 1 - (i // 32 / 16 + 0.0546875)],
                        [i % 32 / 32 + 0.02734375, 1 - (i // 32 / 16 + 0.0546875)]])

    t_ind_used = {val: i for i, val in enumerate(t_ind_used)}

    ind_buf = []

    for j in range(16):
        for i in range(16):
            if water_mask != None:
                if water_mask[j*16 + i] == 65535:
                    continue # comment this line to enable hidden liquids polygons
                    for y in range(2):
                        for x in range(2):
                            ind_buf.extend([33 + j * 66 + y * 33 + i * 2 + x,
                                            33 + j * 66 + y * 33 + i * 2 + x,
                                            0,
                                            j * 66 + y * 33 + i * 2 + x,
                                            j * 66 + y * 33 + i * 2 + x,
                                            0,
                                            34 + j * 66 + y * 33 + i * 2 + x,
                                            34 + j * 66 + y * 33 + i * 2 + x,
                                            0])
                            ind_buf.extend([34 + j * 66 + y * 33 + i * 2 + x,
                                            34 + j * 66 + y * 33 + i * 2 + x,
                                            0,
                                            j * 66 + y * 33 + i * 2 + x,
                                            j * 66 + y * 33 + i * 2 + x,
                                            0,
                                            1 + j * 66 + y * 33 + i * 2 + x,
                                            1 + j * 66 + y * 33 + i * 2 + x,
                                            0])
                    continue
            tex_p = t_arr[j * 16 + i]
            index = t_ind_used[tex_p[1] * 64 + tex_p[0]]
            tex_c = [index * 9 + i for i in range(9)]
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
                                    34 + j * 66 + y * 33 + i * 2 + x,
                                    34 + j * 66 + y * 33 + i * 2 + x,
                                    tex_c[(y + 1) * 3 + (x + 1)]])
                    ind_buf.extend([34 + j * 66 + y * 33 + i * 2 + x,
                                    34 + j * 66 + y * 33 + i * 2 + x,
                                    tex_c[(y + 1) * 3 + (x + 1)],
                                    j * 66 + y * 33 + i * 2 + x,
                                    j * 66 + y * 33 + i * 2 + x,
                                    tex_c[y * 3 + x],
                                    1 + j * 66 + y * 33 + i * 2 + x,
                                    1 + j * 66 + y * 33 + i * 2 + x,
                                    tex_c[y * 3 + (x + 1)]])
            
    return vert_buf, norm_buf, tex_buf, ind_buf

def prepare_nodes(mesh, mat, i, j, name, v_arr, t_arr, altitude, tiles_count, water_mask=None):
    subname = "land" if water_mask == None else "liquid"

    # convert sector data
    vert, norm, tex, ind = create_geometry(v_arr, t_arr, altitude, tiles_count, water_mask)

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

def convert_map(name, unit_points=None):
    if unit_points is not None:
        # unit Z coord by map
        unit_z = [-1.0 for i in range(len(unit_points))]
        
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
                                     diffuse=texmap)
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
            
            nodes.append(prepare_nodes(mesh, mat, i, j, map_name, info[1][:],
                                       info[3 if info[0] else 2][:],
                                       map_info[0], map_info[5]))

            # get unit points Z
            if unit_points is not None and min(unit_z) < 0:
                # still bad optimized, but better than early
                for unit_i in range(len(unit_points)):
                    if unit_z[unit_i] < 0:
                        if -2 <= unit_points[unit_i][0] - i * 32 <= 34 and \
                           -2 <= unit_points[unit_i][1] - j * 32 <= 34:
                            for p_ind in nodes[-1].children[0].geometry.primitives[0].vertex_index:
                                unit_z[unit_i] = get_z(unit_points[unit_i][0] - i * 32,
                                                       unit_points[unit_i][1] - j * 32,
                                                       nodes[-1].children[0].geometry.primitives[0].vertex[p_ind[0]],
                                                       nodes[-1].children[0].geometry.primitives[0].vertex[p_ind[1]],
                                                       nodes[-1].children[0].geometry.primitives[0].vertex[p_ind[2]])
                                if unit_z[unit_i] >= 0.0:
                                    unit_points[unit_i][2] += unit_z[unit_i]
                                    break

            if info[0] != 0:
                liquid_nodes.append(prepare_nodes(mesh, mat, i, j, map_name,
                                                  info[2][:],info[4][:],
                                                  map_info[0], map_info[5],
                                                  info[5]))


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

    if unit_points is not None:
        for i, j in enumerate(unit_z):
            if j == -1:
                print("Unit {} incorrectly placed".format(i))

    return unit_points

if __name__ == '__main__':
    if 2 == len(sys.argv):
        convert_map(sys.argv[1][:-3])
    else:
        print("Usage: convert_map.py input.mp")
