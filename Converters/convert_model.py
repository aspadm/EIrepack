import sys
import numpy as np
import collada as dae
import lnk
import fig
import bon
import anm

textures = {
"nafltr59": "tree02",
"stst30": "mineDetails00",
"nafltr23": "tree02",
"naflbu6": "tree02",
"nafltr56": "tree02",
"nafltr20": "tree02",
"unhuma": "default0",
"stbuho7": "HumanHouse04",
"naflbu17": "tree02",
"nast8": "Stone02",
"stto5": "Campfire00",
"stst155": "dummy00",
"stst151": "fake00",
"stto6": "torchBase00",
"naflbu18": "tree02",
"unanhopi": "Pig00",
"unhufe": "default0",
"nafltr83": "tree02",
"naflbu19": "tree02",
"stbuho6": "MasterHouse00",
"stst14": "BigShop01",
"stst4": "Skin00",
"stwe3": "Well00",
"nafltr57": "tree02",
"nafltr21": "tree02",
"nafltr22": "tree02",
"stga1": "Gate00",
"stbr1": "Bridge00",
"nast16": "Stone02",
"stwame1": "Fence03",
"nafltr86": "tree02",
"stwali1": "Fence00",
"stst56": "moneySack00",
"naflbu16": "tree02",
"unanhodo": "Dog00",
"stbuho5": "BigShop01",
"stbr4": "Bridge4x12",
"stst13": "ColumnRuins01",
"nast13": "Stone02",
"unmogo": "Goblin00L",
"unmodr": "Driad00L",
"unanhoha": "Hare01",
"stst19": "skeleton00",
"nafltr69": "tree03",
"stst74": "flyerFurniture00",
"stto9": "caveDoor00",
"stst76": "flyerFurniture00",
"stst37": "ogrHouse00",
"stst73": "flyerFurniture00",
"stto10": "caveDoor00",
"unmomi": "MindFlayer00",
"nast14": "Stone02",
"stbuho56": "panelTent00",
"stst57": "caveDoor00",
"stst43": "kanianArc00",
"stst75": "flyerFurniture00",
"stst81": "caveDoor00",
"stto11": "caveDoor00",
"unanwira": "Rat00",
"stbuho57": "hadoganPrison00",
"naflbu14": "tree04",
"naflbu13": "tree04",
"stst111": "hadoganGates00",
"nafltr73": "tree04",
"stbuho39": "dome00",
"stga6": "hadoganGates00",
"stbuho42": "hadoganHouse00",
"stbuho43": "hadoganHouse00",
"stwa13": "hadoganWall01",
"stst90": "dome00",
"stst91": "dome00",
"stwa11": "hadoganWall00",
"stst38": "kanianGate00",
"stst98": "sortir00",
"stst96": "sortir00",
"stst97": "sortir00",
"nafltr72": "tree04",
"nafltr71": "tree04",
"stst92": "hadoganChest00",
"stst129": "stocks00",
"stst58": "caveLevel00",
"unanwihy": "Hyena00",
"unmosp": "Spider00",
"stto2": "Torch00",
"stst156": "jug03",
"nast12": "Stone05",
"stst44": "mine00",
"stst45": "mine00",
"stst83": "moneySack00",
"stst158": "carpet00",
"stst93": "hadoganChest00",
"stst127": "PotFire00",
"stbuho53": "runnersTent00",
"stbuho50": "runnersBlacksmith00",
"stst159": "carpet00",
"stbuho51": "runnersThrone00",
"stst99": "runnersTent00",
"stbuho54": "runnersTent00",
"stst141": "witchStuff00",
"stto8": "torchBase00",
"stbr6": "orcBridge00",
"stst94": "hadoganChest00",
"stst128": "ladder00",
"stbr13": "stone06",
"unmozo0": "ZombieMale00",
"stst89": "dome00",
"stbuho44": "hadoganVeranda00",
"stbuho45": "hadoganVeranda00",
"stbuho52": "sortir00",
"stst126": "necroTable00",
"unmosh": "Shadow00",
"stbuho46": "necroTower00",
"stbuho48": "vivary00",
"stwa10": "hadoganWall00",
"stst82": "moneySack00",
"stst66": "torchBase00",
"stst59": "squirrelSkin00",
"stst125": "Cart00",
"nast9": "Stone02",
"nast10": "Stone02",
"nast5": "Stone02",
"nast11": "Stone05",
"nafltr74": "tree02",
"stbr7": "orcBridge00",
"stst142": "witchStuff00",
"stst36": "bridge00",
"nafltr70": "tree02",
"stst79": "kanianFurniture00",
"stsi3": "level01",
"stst35": "ambush00",
"unmotr": "Troll01",
"naflbu7": "tree02",
"naflbu8": "tree02",
"stst21": "DgunTorch00",
"nafltr77": "mushroom01_1",
"stst16": "cellar00",
"stst002": "DgunFace02",
"unmosk": "Skeleton00",
"stst17": "cave01",
"stwa2": "kanianGate00",
"stst47": "crypt00",
"stst46": "crypt00",
"nafltr75": "tree02",
"stwa1": "kanianWalls00",
"stst39": "kanianGate00",
"nafltr68": "tree02",
"stwa3": "kanianArc00",
"unmodg": "Dragon01",
"nast7": "Stone02",
"stst50": "kanianRuins00",
"stst54": "kanianRuins00",
"stst52": "kanianRuins00",
"stst67": "boar00",
"unanhoho": "Horse01",
"unanwibo": "Boar01",
"stbuho11": "tent00",
"unmoto": "Toad00",
"unmowi": "Willowisp00",
"unmoli": "LizardMan00",
"nast15": "Stone02",
"nafltr76": "tree02",
"stst32": "lizardCage00",
"unanwiba": "Bat00",
"stbr3": "DgunBridge01",
"stbuho10": "lizardHouse00",
"stbuho4": "GoblinHouse00",
"unorma": "default0",
"unorfe": "default0",
"stbr8": "orcBridge00",
"stst68": "orcBridge00",
"stbr10": "tree02",
"stst3": "DgunAkvarium00",
"unmogo1": "Golem00",
"stst9": "DgunTorchRuins01",
"stst1": "DgunBird00",
"stto1": "DgunTorch00",
"stbuto1": "DgunPyramid00",
"stbr2": "DgunBridge00",
"unmogo2": "Golem01",
"stst23": "DgunTorchRuins01",
"stst2": "DgunBird01",
"unmori": "Rick",
"stst12": "DgunDragon00",
"stst69": "kanianHouse00",
"stst42": "mine00",
"stst72": "tree03",
"stbuho27": "witchHouse00",
"stbuho18": "shopperTent00",
"stwa5": "kanianHouse00",
"stbuho38": "kanianHouse00",
"stst80": "kanianFurniture00",
"stsi1": "SignBoard00",
"stst147": "Bridge00",
"stbuho19": "kanianHouse00",
"stbuho29": "captainHouse00",
"stbuho25": "kanianHouse00",
"stbuho26": "kanianHouse00",
"stbuho30": "govenorHouse00",
"stbuho14": "kanianHouse00",
"stbuto2": "kanianTower01",
"stbuho13": "kanianHouseDetails00",
"stbuho22": "quater00",
"stbuho28": "smallShop00",
"stbuho20": "kanianHouse00",
"stst148": "Bridge00",
"unanwiti": "Tiger01",
"unmoun": "Unicorn00",
"stbr11": "kanianBridge00",
"stbr12": "kanianBridge00",
"unanwide": "Deer01",
"unmoel2": "Earth01",
"stst71": "tree03",
"unanhoco": "Cow00",
"unmocy": "Cyclop00",
"unmozo1": "ZombieFemale00",
"unanwiwo": "Wolf00",
"stst161": "Bridge00",
"stst87": "goblin00",
"stst27": "crypt00",
"unmoog1": "Ogre00",
"stst15": "ruins00",
"stst8": "DgunBirdRuins00",
"stst24": "DgunTorchRuins01",
"stst22": "DgunTorchRuins01",
"stst25": "DgunTorchRuins01",
"stst26": "DgunDragon01",
"nast6": "Stone02",
"unmoba2": "Banshee00",
"unmoel0": "Earth02",
"stga4": "dgunGate00",
"stst62": "golemCenter",
"nafltr78": "mushroom02_2",
"stga5": "kanianHouse00",
"stst70": "tree03",
"stbuho33": "kanianHouse00",
"stbuho35": "kanianTower00",
"stbuho34": "kanianTower00",
"stwa8": "driadFence00",
"stwa7": "driadFence00",
"stwa9": "driadFence00",
"stst116": "tree03",
"efcu0": "sound",
"stbuho32": "kanianHouse00",
"stwa4": "strongFence00",
"stbuho37": "kanianHouse00",
"stbuho65": "driadPrison00",
"stbuho64": "driadPrison00",
"stbuho15": "driadPrison00",
"stbuho12": "bigMachine00",
"stbuho17": "shopperTent00",
"stbuho16": "armyTent00",
"stst63": "kanianTower00",
"naflbu9": "tree03",
"stbuho24": "diningHall00",
"stbuho23": "headquaters00",
"stbuho21": "managerHouse00",
"stst153": "FakeDocument00",
"unmosu": "Succubus01",
"stst77": "kanianFurniture00",
"stst78": "kanianFurniture00",
"unmobe0": "Beholder00",
"nafltr82": "tree04",
"stbuho49": "dekhanHouse00",
"stbr18": "hadoganBridge00",
"stbuho63": "HadoganShipYard00",
"stga8": "HadoganCaveDoor00",
"stst130": "tarOven00",
"stst135": "deadWarrior00",
"stst134": "deadWarrior00",
"stst136": "deadScientist00",
"naflbu20": "tree04",
"naflbu21": "tree04",
"stst114": "healingStatue00",
"stst154": "heroSit00",
"unmoba1": "Banshee00",
"stbr17": "FlyerBridge00",
"stst95": "FlyerBridge00",
"nast2": "Stone02",
"unmoel1": "Earth02",
"stbuho60": "flyerTemple00",
"stbuho66": "flyerTemple00",
"unmobe1": "Beholder01",
"stst88": "dome00",
"stst100": "hadoganWell00",
"stst106": "deadScientist00",
"stst107": "deadWarrior00",
"stbuho3": "OgrHouse00",
"unmoog2": "Ogre02",
"stst117": "hadoganPrison00",
"stbuho58": "hadoganHouse00",
"stst113": "hadoganStatues00",
"stwe1": "Fontain00",
"stbuho55": "dome00",
"stwa15": "hadoganWall00",
"stbuho62": "dekhanHouse00",
"stga7": "hadoganGates00",
"stwa14": "hadoganWall00",
"stbuho61": "vivary00",
"stbr15": "waterLock00",
"stbuho47": "dgunistHouse00",
"stst157": "basket01",
"stst150": "DgunistNote00",
"stst115": "mineControl00",
"stst112": "hadoganStatues00",
"stbr19": "SuspensionBridge00",
"stst105": "panelTent00",
"stbuho41": "teleport00",
"stbuho40": "teleport00",
"stst101": "pool00",
"stst131": "warriorStatue00",
"stst132": "podiums00",
"stst133": "podiums00",
"stsi5": "level00",
"stst123": "dgunFace02",
"stst118": "dgunBirdRuins00",
"stst121": "dgunDragon00",
"unmocu": "Curse00",
"stst108": "brokenPlate01",
"stst139": "brokenPlate00",
"stst001": "DgunFace01",
"stga2": "DgunGate00",
"stst20": "Goblin00L",
"stbuho8": "Tipy00",
"stbuho9": "GoblinHouse01",
"unanwicr": "Crab01",
"stst29": "mine00",
"nast25": "Stone02",
"stst145": "DgunDragon01",
"stst64": "moneySack00",
"stst144": "DgunDragon01",
"stbuho67": "teleportSmall00",
"stbuho68": "teleportSmall00",
"stst28": "source00",
"stbr9": "orcBridge00",
"nast1": "Stone02",
"stst51": "kanianRuins00",
"stst33": "tree02",
"stst65": "sunClock00",
"stst31": "driadIdol01",
"stst110": "girlSign00",
"stst34": "altar00",
"stsi4": "billboard00",
"stbr14": "orcBridge00",
"stst102": "stone02",
"stst84": "ogreChest00",
"stst40": "mine00",
"stst41": "mine00",
"stst49": "kanianArc00",
"stst48": "kanianArc00",
"stga3": "kanianGate00",
"stst55": "kanianRuins00",
"unmoco2": "mainmenu00",
"stst146": "Bridge00",
"stst149": "Bridge00"}

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

def flat_tree(tree, arr=[]):
    arr.append(tree[0])
    if len(tree) != 0:
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
def trilinear(arr, coefs=[0, 0, 0]):
    buf = [[0.0 for i in range(4)] for j in range(3)]

    for i in range(3):
        for j in range(4):
            # Linear interpolation by str
            t1 = arr[0][i][j] + (arr[1][i][j] - arr[0][i][j]) * coefs[0]
            t2 = arr[2][i][j] + (arr[3][i][j] - arr[2][i][j]) * coefs[0]
            # Bilinear interpolation by dex
            v1 = t1 + (t2 - t1) * coefs[1]

            # Linear interpolation by str
            t1 = arr[4][i][j] + (arr[5][i][j] - arr[4][i][j]) * coefs[0]
            t1 = arr[6][i][j] + (arr[7][i][j] - arr[6][i][j]) * coefs[0]
            # Bilinear interpolation by dex
            v2 = t1 + (t2 - t1) * coefs[1]

            # Trilinear interpolation by height
            buf[i][j] = v1 + (v2 - v1) * coefs[2]

    return buf

def convert_to_obj(name):
    model_name = name.split("\\")[-1].split("/")[-1]
    model_folder = name[:-len(model_name)]

    model_tree = lnk.read_info(name + ".lnk")
    parts_list = flat_tree(model_tree)

    with open(name + ".mtl", "w") as mtl:
        mtl.write("newmtl material_0\nmap_Kd " +
                  textures.get(model_name, "default") + ".png\n")

    for part_name in parts_list:
        part_pos = bon.read_info(model_folder + part_name + ".bon")
        part_data = fig.read_info(model_folder + part_name + ".fig")

##        vertex_buf = [trilinear([part_data[13][xyz][block][:]]) \
##                      for i in range(part_data[1])]

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

def create_geometry(part_data):
    vert_buf = []
    norm_buf = []
    tex_buf = []
    ind_buf = []
    
    for i in range(part_data[1]):
        for j in range(4):
            vert_buf.extend([part_data[13][i][0][0][j],
                             part_data[13][i][1][0][j],
                             part_data[13][i][2][0][j]])

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

def convert_model(name):
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
    image = dae.material.CImage("texture", "./" + \
                                textures.get(model_name, "default") + ".png")
    surface = dae.material.Surface("texture_surface", image)
    sampler2d = dae.material.Sampler2D("texture_sampler", surface)
    texmap = dae.material.Map(sampler2d, "UVSET0")

    effect = dae.material.Effect("effect0", [surface, sampler2d], "phong",
                                 diffuse=texmap)
    mat = dae.material.Material("material0", "material", effect)

    # add material in mesh
    mesh.effects.append(effect)
    mesh.materials.append(mat)
    mesh.images.append(image)

    # generate geometries
    nodes = []
    for part_name in parts_list:
        # read model data
        part_pos = bon.read_info(model_folder + part_name + ".bon")
        part_data = fig.read_info(model_folder + part_name + ".fig")

        # prepare geometry
        vert, norm, tex, ind = create_geometry(part_data)
        vert_source = dae.source.FloatSource("vert_arr", np.array(vert),
                                             ("X", "Y", "Z"))
        norm_source = dae.source.FloatSource("norm_arr", np.array(norm),
                                             ("X", "Y", "Z"))
        tex_source = dae.source.FloatSource("tex_arr", np.array(tex),
                                            ("S", "T"))
        ind_source = np.array(ind)

        # create empty mesh
        geom = dae.geometry.Geometry(mesh, part_name + "_geom",
                                     part_name + "_geom",
                                     [vert_source, norm_source, tex_source])

        # describe mesh data structure
        input_list = dae.source.InputList()
        input_list.addInput(0, "VERTEX", "#vert_arr")
        input_list.addInput(1, "NORMAL", "#norm_arr")
        input_list.addInput(2, "TEXCOORD", "#tex_arr")

        # generate geometry data
        triset = geom.createTriangleSet(ind_source, input_list, "material0")
        geom.primitives.append(triset)
        mesh.geometries.append(geom)

        # mesh position
        pos = dae.scene.TranslateTransform(part_pos[0][0],
                                           part_pos[0][1],
                                           part_pos[0][2])
        # reinstance material
        matnode = dae.scene.MaterialNode("material0", mat, inputs=[])
        # add geometry to wrap node
        geomnodes = [dae.scene.GeometryNode(geom, [matnode])]

        nodes.append(dae.scene.Node(part_name,
                                    children=geomnodes,
                                    transforms=[pos]))

    # generate scene hierarchy
    #nodes = []

    # add base light
    sun = dae.light.DirectionalLight("Sun", (1, 1, 1))
    mesh.lights.append(sun)
    root_node = dae.scene.Node("root", children=nodes)
    sun_node = dae.scene.Node("sunshine", children=[dae.scene.LightNode(sun)],
                              transforms=[dae.scene.MatrixTransform(np.array(
                                    [1, 0, 0, 0,
                                     0, 1, 0, 0,
                                     0, 0, 1, 0,
                                     0, 0, 0, 1]))])
    # create main scene
    myscene = dae.scene.Scene(model_name, [sun_node, root_node])
    mesh.scenes.append(myscene)
    mesh.scene = myscene

    # finalyze and save mesh
    mesh.write(name + ".dae")

if __name__ == '__main__':
    if 2 == len(sys.argv):
        convert_model(sys.argv[1][:-4])
    else:
        print("Usage: convert_model.py input.lnk")
