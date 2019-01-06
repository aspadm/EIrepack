import sys
import numpy as np
import collada as dae
import lnk
import fig
import bon
import anm
from textures_link import textures
from math import sqrt, atan2

"""
.lnk
  |
 \|/
*.fig <- .bon
  |
 \|/
 .anm

LNK - model hierarchy;
FIG - model parts;
BON - position of parts;
ANM - animation of parts.
"""

def flat_tree(tree, arr=None):
    if arr is None:
        arr = []
        
    arr.append(tree[0])
    if len(tree[1]) != 0:
        for leaf in tree[1]:
            flat_tree(leaf, arr)

    return arr

"""
Vertex position is tri-linear value from 8 arrays:

t1 = 0 + (1 - 0) * s
t2 = 2 + (3 - 2) * s
v1 = t1 + (t2 - t1) * d

t1 = 4 + (5 - 4) * s
t2 = 6 + (7 - 6) * s
v2 = t1 + (t2 - t1) * d

res = v1 + (v2 - v1) * h
"""
def trilinear(val, coefs=[0, 0, 0]):
    # Linear interpolation by str
    t1 = val[0] + (val[1] - val[0]) * coefs[1]
    t2 = val[2] + (val[3] - val[2]) * coefs[1]
    # Bilinear interpolation by dex
    v1 = t1 + (t2 - t1) * coefs[0]

    # Linear interpolation by str
    t1 = val[4] + (val[5] - val[4]) * coefs[1]
    t2 = val[6] + (val[7] - val[6]) * coefs[1]
    # Bilinear interpolation by dex
    v2 = t1 + (t2 - t1) * coefs[0]

    # Trilinear interpolation by height
    return v1 + (v2 - v1) * coefs[2]

def convert_to_obj(name, coefs=[0, 0, 0]):
    model_name = name.split("\\")[-1].split("/")[-1]
    model_folder = name[:-len(model_name)]

    model_tree = lnk.read_info(name + ".lnk")
    parts_list = flat_tree(model_tree)

    with open(name + ".mtl", "w") as mtl:
        mtl.write("newmtl material_0\nmap_Kd " +
                  textures.get(model_name, ["default"])[0] + ".png\n")

    for part_name in parts_list:
        part_pos = bon.read_info(model_folder + part_name + ".bon")
        part_data = fig.read_info(model_folder + part_name + ".fig")

        if part_data is None:
            return

                          # v_data   v xyz blk
        vertex_buf = [[part_data[13][i][0][0][:], \
                       part_data[13][i][1][0][:], \
                       part_data[13][i][2][0][:]] for i in range(part_data[1])]

        obj_buf = "mtllib ./" + model_name + ".mtl\nusemtl material_0\n"
        # Vertex
        for i in part_data[17]:
            obj_buf += "v {:.8f} {:.8f} {:.8f}\n".format(vertex_buf[i[0]][0][i[1]],
                                             vertex_buf[i[0]][1][i[1]],
                                             vertex_buf[i[0]][2][i[1]])
        # Normal
        for i in part_data[17]:
            obj_buf += "vn {:.8f} {:.8f} {:.8f}\n".format(part_data[14][i[2]][0][i[3]],
                                              part_data[14][i[2]][1][i[3]],
                                              part_data[14][i[2]][2][i[3]])
        # UV
        for i in part_data[17]:
            obj_buf += "vt {:.8f} {:.8f}\n".format(part_data[15][i[4]][0],
                                                   part_data[15][i[4]][1])

        for i in part_data[16]:
            obj_buf += "f {}/{}/{} {}/{}/{} {}/{}/{}\n".format(i[0] + 1,
                        i[0] + 1, i[0] + 1, i[1] + 1, i[1] + 1, i[1] + 1,
                        i[2] + 1, i[2] + 1, i[2] + 1)

        with open(model_folder + part_name + ".obj", "w") as file:
            file.write(obj_buf)

def create_geometry(part_data, coefs=[0, 0, 0]):
    vert_buf = []
    norm_buf = []
    tex_buf = []
    ind_buf = []

    for i in range(part_data[1]):
        for j in range(4):
            vert_buf.extend([trilinear([part_data[13][i][0][k][j] for k in range(8)],
                                        coefs),
                             trilinear([part_data[13][i][1][k][j] for k in range(8)],
                                        coefs),
                             trilinear([part_data[13][i][2][k][j] for k in range(8)],
                                        coefs)])
            
    for i in range(part_data[2]):
        for j in range(4):
            norm_buf.extend([part_data[14][i][0][j],
                             part_data[14][i][1][j],
                             part_data[14][i][2][j]])

    for i in range(part_data[3]):
        tex_buf.extend(part_data[15][i])

    for i in part_data[16]:
        ind_buf.extend([part_data[17][i[0]][0] * 4 + part_data[17][i[0]][1],
                        part_data[17][i[0]][2] * 4 + part_data[17][i[0]][3],
                        part_data[17][i[0]][4],
                        part_data[17][i[1]][0] * 4 + part_data[17][i[1]][1],
                        part_data[17][i[1]][2] * 4 + part_data[17][i[1]][3],
                        part_data[17][i[1]][4],
                        part_data[17][i[2]][0] * 4 + part_data[17][i[2]][1],
                        part_data[17][i[2]][2] * 4 + part_data[17][i[2]][3],
                        part_data[17][i[2]][4]])

    return vert_buf, norm_buf, tex_buf, ind_buf

def build_scene_hierarchy(tree, nodes_prepare, need_parts):
    buf = []

    for name in tree[1]:
        buf.append(build_scene_hierarchy(name, nodes_prepare, need_parts))

    if need_parts is None or tree[0] in need_parts:
        buf.append(nodes_prepare[tree[0]][0])

    return dae.scene.Node(tree[0], children=buf, transforms=[nodes_prepare[tree[0]][1]])

def convert_model(name, add_suf="", coefs=None, root_pos=None, root_rot=None, tex_name=None, need_parts=None):
    if coefs is None:
        coefs = [0, 0, 0]
    if root_pos is None:
        root_pos = [0, 0, 0]
    if root_rot is None:
        root_rot = [1, 0, 0, 0]
    
    model_name = name.split("\\")[-1].split("/")[-1]
    model_folder = name[:-len(model_name)]

    # common information
    contrib = dae.asset.Contributor(authoring_tool="EIrepack",
                                    copyright="Only for educational purposes")
    asset = dae.asset.Asset(upaxis=dae.asset.UP_AXIS.Z_UP, title=model_name,
                            contributors=[contrib], unitname="meter",
                            unitmeter=1)

    # create empty collada mesh
    mesh = dae.Collada()
    mesh.assetInfo = asset

    model_tree = lnk.read_info(name + ".lnk")
    parts_list = flat_tree(model_tree)

    # create texture material
    if tex_name is None:
        tex_name = textures.get(model_name, ["default"])[0]
    image = dae.material.CImage("texture" + add_suf, "./" + tex_name + ".png")
    surface = dae.material.Surface("texture_surface" + add_suf, image)
    sampler2d = dae.material.Sampler2D("texture_sampler" + add_suf, surface)
    texmap = dae.material.Map(sampler2d, "UVSET0")

    effect = dae.material.Effect("effect0" + add_suf, [surface, sampler2d], "phong",
                                 diffuse=texmap)
    mat = dae.material.Material("material0" + add_suf, "material" + add_suf, effect)

    # add material in mesh
    mesh.effects.append(effect)
    mesh.materials.append(mat)
    mesh.images.append(image)

    # generate geometries
    nodes_prepare = {}
    for part_name in parts_list:
        # read model data
        part_pos = bon.read_info(model_folder + part_name + ".bon")

        if part_pos is None or len(part_pos) != 8:
            return 1
        
        # mesh position
        pos = dae.scene.TranslateTransform(trilinear([part_pos[i][0] for i in range(8)],
                                                     coefs),
                                           trilinear([part_pos[i][1] for i in range(8)],
                                                     coefs),
                                           trilinear([part_pos[i][2] for i in range(8)],
                                                     coefs))

        if need_parts is None or part_name in need_parts:
            part_data = fig.read_info(model_folder + part_name + ".fig")

            if part_data is None:
                return 1

            # prepare geometry
            vert, norm, tex, ind = create_geometry(part_data, coefs)
            vert_source = dae.source.FloatSource("vert_arr", np.array(vert),
                                                 ("X", "Y", "Z"))
            norm_source = dae.source.FloatSource("norm_arr", np.array(norm),
                                                 ("X", "Y", "Z"))
            tex_source = dae.source.FloatSource("tex_arr", np.array(tex),
                                                ("S", "T"))
            ind_source = np.array(ind)

            # create empty mesh
            geom = dae.geometry.Geometry(mesh, part_name + "_geom" + add_suf,
                                         part_name,
                                         [vert_source, norm_source, tex_source])

            # describe mesh data structure
            input_list = dae.source.InputList()
            input_list.addInput(0, "VERTEX", "#vert_arr")
            input_list.addInput(1, "NORMAL", "#norm_arr")
            input_list.addInput(2, "TEXCOORD", "#tex_arr")

            # generate geometry data
            triset = geom.createTriangleSet(ind_source, input_list,
                                            "material0" + add_suf)
            geom.primitives.append(triset)
            mesh.geometries.append(geom)
        
            # reinstance material
            matnode = dae.scene.MaterialNode("material0" + add_suf, mat, inputs=[])
            # add geometry to wrap node
            geomnode = dae.scene.GeometryNode(geom, [matnode])
        else:
            geomnode = None

        nodes_prepare.update({part_name: [geomnode, pos]})

    # prepare root transformation
    root_pos = dae.scene.TranslateTransform(root_pos[0],
                                            root_pos[1],
                                            root_pos[2])
    vec_len = sqrt(root_rot[1] ** 2 + root_rot[2] ** 2 + root_rot[3] ** 2)
    # quaternion (w, x, y, z) to vector-based rotation (angle, x, y, z)
    if vec_len < 0.00001:
        root_rot = [0, 0, 0, 0]
    else:
        root_rot[1] /= vec_len
        root_rot[2] /= vec_len
        root_rot[3] /= vec_len
        if root_rot[0] < 0:
            root_rot[0] = 114.59155903 * atan2(- vec_len, - root_rot[0])
        else:
            root_rot[0] = 114.59155903 * atan2(vec_len, root_rot[0])
    root_rot = dae.scene.RotateTransform(root_rot[1], root_rot[2],
                                         root_rot[3], root_rot[0])

    # generate scene hierarchy
    root_node = dae.scene.Node(model_name + add_suf,
                               children=[build_scene_hierarchy(model_tree,
                                                               nodes_prepare,
                                                               need_parts)],
                               transforms=[root_pos, root_rot])
    # add base light
    if add_suf == "":
        sun = dae.light.DirectionalLight("Sun", (1, 1, 1))
        mesh.lights.append(sun)
        sun_node = dae.scene.Node("sunshine",
                                  children=[dae.scene.LightNode(sun)],
                                  transforms=[dae.scene.MatrixTransform(
                                              np.array([1, 0, 0, 0,
                                                        0, 1, 0, 0,
                                                        0, 0, 1, 0,
                                                        0, 0, 0, 1]))])
    # create main scene
        myscene = dae.scene.Scene(model_name + add_suf, [sun_node, root_node])
    else:
        myscene = dae.scene.Scene(model_name + add_suf, [root_node])
    mesh.scenes.append(myscene)
    mesh.scene = myscene

    # finalyze and save mesh
    mesh.write(name + add_suf + ".dae")

if __name__ == '__main__':
    if 2 == len(sys.argv):
        convert_model(sys.argv[1][:-4])
    else:
        print("Usage: convert_model.py input.lnk")
