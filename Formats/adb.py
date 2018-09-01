import sys
from binary_readers import *

keys = [""]

def build_yaml(info):
    buf = ""

    buf += "model_name: \"" + info[1] + "\"\n"
    buf += "actions_count: " + str(info[0]) + "\n"

    buf += "minimal_height: " + str(info[2]) + "\n"
    buf += "average_height: " + str(info[3]) + "\n"
    buf += "maximal_height: " + str(info[4]) + "\n"

    buf += "actions:\n"
    for element in info[5]:
        buf += "  - action_name: \"" + element[0] + "\"\n"
        buf += "    action_number: " + str(element[1]) + "\n"
        
        buf += "    weapons:"
        if type(element[2]) == str:
            buf += " " + element[2] + "\n"
        else:
            buf += "\n"
            for item in element[2]:
                buf += "      - " + item + "\n"

        buf += "    allowed_states: " + element[3] + "\n"

        buf += "    action_type:\n      type: " + element[4][0] + "\n"
        buf += "      modifier: " + element[4][1] + "\n"
        
        buf += "    animation_stage: " + element[5] + "\n"
        
        buf += "    action_forms:"
        if type(element[6]) == str:
            buf += " " + element[6] + "\n"
        else:
            buf += "\n"
            for item in element[6]:
                buf += "      - " + item + "\n"
        
        buf += "    action_probability: " + str(element[7]) + "\n"
        buf += "    animation_length: " + str(element[8]) + "\n"
        buf += "    movement_speed: " + str(element[9]) + "\n"
        buf += "    show_hide_frame_1: " + str(element[10]) + "\n"
        buf += "    show_hide_frame_2: " + str(element[11]) + "\n"
        buf += "    sound_frame_1: " + str(element[12]) + "\n"
        buf += "    sound_frame_2: " + str(element[13]) + "\n"
        buf += "    sound_frame_3: " + str(element[14]) + "\n"
        buf += "    sound_frame_4: " + str(element[15]) + "\n"
        buf += "    hit_frame: " + str(element[16]) + "\n"
        buf += "    special_sound_frame: " + str(element[17]) + "\n"
        buf += "    sound_id_1: " + str(element[18]) + "\n"
        buf += "    sound_id_2: " + str(element[19]) + "\n"
        buf += "    sound_id_3: " + str(element[20]) + "\n"
        buf += "    sound_id_4: " + str(element[21]) + "\n"
        
    
    return buf

weapons = ["SWORD", "AXE", "DAGGER", "SPEAR", "HAMMER", "BOW", "CROSSBOW"]
states = ["NEUTRAL", "REST", "ATTACK", "UNK3", "WARRY", "UNK5", "LIE", "ALL"]
forms = ["HIDES", "STEPS", "HIT", "SFXES", "LOWSHAPE", "HIGHSHAPE"]
types = ["UNK0", "SPECIAL", "ATTACK", "CAST", "RUN", "WALK", "IDLE", "DEATH",
         "SUFFER", "CROSS", "UNK10", "UNK11", "UNK12", "UNK13", "UNK14", "ALL"]             

def read_info(file_name):
    info = []
    with open(file_name, "rb") as file:
        if file.read(4) != b'\x41\x44\x42\x00':
            print("Incorrect magic!")
            return

        info.append(read_uint(file))
        info.append(read_str(file, 24))
        info.extend(read_float(file, 3))

        info.append([])
        for i in range(info[0]):
            info[-1].append([])
            info[-1][i].append(read_str(file, 16))
            info[-1][i].append(read_uint(file))

            packed_data = read_uint64(file) # packed
            
            # weapons
            info[-1][i].append([])
            for j in range(7):
                if packed_data & 1:
                    info[-1][i][-1].append(weapons[j])
                packed_data >>= 1
            if len(info[-1][i][-1]) == 0:
                info[-1][i][-1] = "NONE"
            elif len(info[-1][i][-1]) == 7:
                info[-1][i][-1] = "ALL"
            packed_data >>= 8

            # allowed states
            info[-1][i].append(states[packed_data & 7])
            packed_data >>= 3

            # action type
            action_type = packed_data & 15
            packed_data >>= 4
            action_modifier = packed_data & 255
            packed_data >>= 8
            info[-1][i].append([types[action_type], str(action_modifier)])

            # animation stage
            info[-1][i].append(["UNIQUE", "START", "CYCLE", "END"][packed_data & 3])
            packed_data >>= 2

            # action forms
            info[-1][i].append([])
            for j in range(6):
                if packed_data & 1:
                    info[-1][i][-1].append(forms[j])
                packed_data >>= 1
            if len(info[-1][i][-1]) == 0:
                info[-1][i][-1] = "NONE"

            info[-1][i].extend(read_uint(file, 2))
            
            info[-1][i].append(read_float(file))
            info[-1][i].extend(read_uint(file, 12))


    return info

if __name__ == '__main__':
    if 2 <= len(sys.argv) <= 3:
        info = read_info(sys.argv[1])
        
        if info != None:
            if len(sys.argv) == 2:
                print(build_yaml(info))
            else:
                with open(sys.argv[2], "w") as file:
                    file.write(build_yaml(info))
    else:
        print("Usage: adb.py input.adb [output.yaml]")
