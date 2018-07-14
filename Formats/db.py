import sys
import os.path
from binary_readers import *

END = b"\x00\x00\x02\x0C\x02\x08\x01\x00\x00\x00" # 10 bytes at the end

types = [".idb", # items
         ".ldb", # levers
         ".pdb", # perks
         "prints.db", # prints
         ".sdb", # spells
         ".udb", # units
         "acks.db", # acks
         ".qdb"] # quests

# S - string
# I - 4b int
# U - 4b unsigned
# F - 4b float
# X - bits byte
# f - float array
# i - int array
# B - bool
# b - bool array
# H - unknown hex bytes
# T - time
# 1 - " FII"
# 2 - "SUFF"
# 3 - "FFFF"
# 4 - " SISS"
# 5 - " SISS     U"

types_struct = [
    # items
    ["SSSIFFFIFIFfIX", # materials
     "SSISIIIFFFFIFIXB     IHFFFfHHFF", # weapons
     "SSISIIIFFFFIFIXB     ffBiHH", # armors
     "SSISIIIFFFFIFIXB     IIFFSbH", # quick items
     "SSISIIIFFFFIFIXB     Is", # quest items
     "SSISIIIFFFFIFIXB     IHI"], # loot items
    # levers
    ["SfIFTSSS"], # lever prototypes
    # perks
    ["SSI       s", # skills
     "SSI       SSIIIFFFIIIIBI"], # perks
    # prints
    [" S11", # blood prints
     " S11      1", # fire prints
     " S11"], # footprints
    # spells
    ["SSSFIFIFFFFIIIIUSSIIbIXFFFFF", # spell prototypes
     "SSFIFFISX", # spell modifiers
     " SssSX", # spell templates
     " SssSX", # armor spell templates
     " SssSX"], # weapon spell templates
    # units
    ["SffUU", # hit locations
     "SUFFUUFfFUUf222222            SssFSsfUUfUUIUSBFUUUU", # race models
     "SSIUIFFFSFFFFFFFFFUFFFFFFff33sfssSFFFFFUFUSF", # monster prototypes
     "SUFFFFbbssssFUB"], # NPCs
    # acks
    [" S        44444444444444444444445444444444444", # answers
     " S        44444", # cryes
     " S        44"], # others
    # quests
    ["SFIISIIs", # quests
     "SFFsSsssssI"] # briefings
    ]

titles = [
    ["materials\nname,type,code,ID,price,weight,mana,slots,durability,skill,\
damage,piercing,slashing,bludgeoning,thermal,chemical,electrical,general,\
unknown,shop1,shop2,shop3,shop4,shop5",
     "\nweapons\nname,type,type ID,material type,unknown,texture type 1,\
texture type 2,price,weight,size,mana,slots,durability,components,\
shop1,shop2,shop3,shop4,shop5,deconstructable,actions,unknown,range,min damage,\
max damage,piercing,slashing,bludgeoning,thermal,chemical,electrical,general,\
unknown,unknown,attack,defence",
     "\narmors\nname,type,typeID,material type,unknown,texture type 1,\
texture type 2,price,weight,size,mana,slots,durability,components,\
shop1,shop2,shop3,shop4,shop5,deconstructable,absortion,piercing,slashing,\
bludgeoning,thermal,chemical,electrical,general,unknown,absortion,piercing,\
slashing,bludgeoning,thermal,chemical,electrical,general,unknown,apply wounds,\
wear order,unknown,unknown",
     "\nquick items\nname,type,unknown,material type,unknown,texture type 1,\
texture type 2,price,weight,size,mana,slots,durability,components,\
shop1,shop2,shop3,shop4,shop5,deconstructable,itemID,graphics level,damage,\
unknown,spell,science modifier,stealing modifier,unknown,unknown",
     "\nquest items\nname,type,unknown,material type,unknown,texture type 1,\
texture type 2,price,weight,size,mana,slots,durability,components,\
shop1,shop2,shop3,shop4,shop5,deconstructable,scriptID,zones",
     "\nloot items\nname,type,unknown,material type,unknown,texture type 1,\
texture type 2,price,weight,size,mana,slots,durability,components,\
shop1,shop2,shop3,shop4,shop5,deconstructable,typeID,unknown,unknown"],
    ["levers\nname,place1-1,place1-2,place2-1,place2-2,unknown,scale,\
switch time,material,switch sound,lever text"],
    ["skills\nname,code,texture type,base attributes",
     "\nperks\nname,code,texture type,required perk,skill type,skill type ID,\
unknown,SL,str,dex,int,cost,modifier,multiplier,add,active,exclusive"],
    ["blood prints\nterrain type,clear weather opacity,clear weather lifetime,\
clear weather fadeout,weather precipitation opacity,weather precipitation \
lifetime,weather precipitation fadeout",
     "\nfoot prints\nterrain type,clear weather opacity,clear weather lifetime,\
clear weather fadeout,weather precipitation opacity,weather precipitation \
lifetime,weather precipitation fadeout,opacity,lifetime,fadeout",
     "\nblood prints\nterrain type,clear weather opacity,clear weather lifetime,\
clear weather fadeout,weather precipitation opacity,weather precipitation \
lifetime,weather precipitation fadeout"],
    ["spell prototypes\nname,code,subtype,price,typeID,mana,\
slots,speed,range,area,effect,target,targets,duration,actions,require trace,\
buildin mods,special mods,texture type,subtypeID,range mod,targets mod,area mod,\
effects mod,duration mod,complex,shop1,shop2,shop3,shop4,shop5,reg,green,blue,\
light radius,fadeout time",
     "\nspell modifiers\nname,code,price,type,mana,value,complex,allod,shop1,\
shop2,shop3,shop4,shop5",
     "\nspell templates\nprototype,required,optional,power,shop1,shop2,shop3,\
shop4,shop5",
     "\narmor spell templates\nprototype,required,optional,power,shop1,shop2,\
shop3,shop4,shop5",
     "\nweapon spell templates\nprototype,required,optional,power,shop1,shop2,\
shop3,shop4,shop5"],
    ["hit locations\nname,piercing,slashing,bludgeoning,thermal,chemical,\
electrical,general,piercing2,slashing2,bludgeoning2,thermal2,chemical2,\
electrical2,general2,unknown,unknown",
     "\nrace models\nname,typeID,health regen,mana regen,language,locomotion,\
vision arc,run speed,walk speed,sneak speed,crawl speed,attack distance,\
AI stay,AI lie,atk piercing,atk slashing,atk bludgeoning,atk thermal,atk \
chemical,atk electrical,atk general,head type,unknown,head weight,head HP,\
torso type,unknown,torso weight,torso HP,right arm type,unknown,right arm weight,\
right arm HP,left arm type,unknown,left arm weight,left arm HP,right leg type,\
unknown,right leg weight,right leg HP,left leg type,unknown,left leg weight,\
left leg HP,mask name,textures,textures2,model shift,SFX path,steps path,\
anm attack speed,anm cast speed,anm hit speed,anm death speed,anm cross speed,\
anm special speed,idle sound probability,attack sound probability,def piercing,\
def slashing,def bludgeoning,def thermal,def chemical,def electrical,def \
general,blood type,cast type,footprint type,leg segment,skin type,first step \
right,head height,unknown,unknown,unknown,unknown",
     "\nmonster prototypes\nname,base race,unknown,skin index,hair,complection X,\
complection Y,complection Z,unknown,HP,mana,absorbtion,tuning actions,\
tuning move,attack range,stats to hit,stats parry,tuning weapon weight,\
tuning weapon typeID,damage min,damage max,general skills,steal skills,\
tame skills,peripheral skills,sight sense,infra sense,lifesense,hearing,smell,\
tracking,detect sight,detect infra,detect life,detect hearing,detect smell,\
detect tracking,loot chance,loot mask,loot min,loot max,rare loot chance,\
rare loot mask,rare loot min,rare loot max,items,elemental,senses,astral,\
spells,wears,weapon,info scale,altitude,random hit,dialog cam distance,\
dialog cam height,real wepon typeID,detonation,base level,second weapon,\
expirience",
     "\nNPCs\nname,unknown,expirience,strength,dexterity,intelligence,\
science,stealing,tame,melee,archery,backstab,elemental,senses,astral,stealth,\
awareness,perks,weapons,quest items,spells,exp to distribute,money,voice"],
    ["answers\nname,select,move,attack,cast,loot,use object,steal,follow,use \
pot,change position,no path,cant cast,cant teleport,ski fail,no target,\
complete sp,dec to att,stamina out,arm crip,leg crip,bored,unknown,overloaded,\
injured,big att,armor crip,wear crip,att in def,wait foll,scenario,steal emp,\
shop yes,shop no",
     "\ncryes\nname,agression,suspect,kill,rest,in agression",
     "\nothers\nname,talk,rest"],
    ["quests\nname,experience,unknown,zone number,comment,money,record number,\
unknown",
     "\nbriefings\nname,unknown,money,give items,comment,take items,\
give quests 1,give quests 2,open zones,unknown,bonus number"]
    ]
     

def find_db_struct(f_name):
    for i in range(len(types)):
        if f_name[- len(types[i]):] == types[i]:
            #print("Base type is", i)
            return i
    raise ValueError

def read_id_n(file):
    buf_id = read_byte(file)
    buf_len = read_byte(file)
    if buf_len & 1:
        file.seek(-1, 1)
        buf_len = read_uint(file) - 1

    return buf_id, buf_len // 2

def unwrap_arr(arr):
    buf = []
    for item in arr:
        if type(item) == list:
            buf.extend(unwrap_arr(item))
        else:
            buf.append(item)

    return buf

def array_to_str(arr):
    buf = unwrap_arr(arr)
    result = ""
    for item in buf:
        if type(item) == str:
            if '"' in item or ';' in item or ',' in item:
                result += '"' + item + '",'
            else:
                result += str(item) + ","
        else:
            result += str(item) + ","
    
    return result[:-1]

def build_data(data):
    buf = ""
    for line in data:
        if type(line) == list:
            for item in line:
                buf += array_to_str(item) + "\n"
        elif type(line) == str:
            buf += line
        else:
            buf += str(line)
        buf += "\n"
        
    return buf

def read_record(file, record):
    buf = []
    section, length = read_id_n(file)
    length += file.tell()
    
    while file.tell() < length:
        l_id, l_len = read_id_n(file)
        spec = record[l_id]
        if spec == "H":
            buf.append(file.read(l_len))
        elif spec == "S":
            buf.append(read_str(file, l_len))
        elif spec == "I":
            buf.append(read_int(file))
        elif spec == "U":
            buf.append(read_uint(file))
        elif spec == "F":
            buf.append(read_float(file))
        elif spec == "B":
            buf.append(bool(read_byte(file)))
        elif spec == "T":
            buf.append(read_uint(file) - 1 / 15 + 0.1)
        elif spec == "f":
            buf.append(read_float(file, l_len // 4))
        elif spec == "i":
            buf.append(read_int(file, l_len // 4))
        elif spec == "b":
            buf.append(list(map(bool, read_byte(file, l_len))))
        elif spec == "X":
            buf.append([])
            if l_len != 4:
                raise ValueError
            value = read_uint(file)
            for bit in range(5):
                buf[-1].append(bool(value & 1))
                value >>= 2
        elif spec == "s":
            buf.append([""])
            border = file.tell() + l_len
            while file.tell() < border:
                s_id, s_len = read_id_n(file)
                if len(buf[-1][-1]) > 0:
                    buf[-1][-1] += "; "
                buf[-1][-1] += read_str(file, s_len)
        elif spec == "1":
            read_id_n(file)
            buf.append(read_float(file))
            read_id_n(file)
            buf.append(read_int(file))
            read_id_n(file)
            buf.append(read_int(file))
        elif spec == "2":
            s_id, s_len = read_id_n(file)
            buf.append(read_str(file, s_len))
            read_id_n(file)
            buf.append(read_uint(file))
            read_id_n(file)
            buf.append(read_float(file))
            read_id_n(file)
            buf.append(read_float(file))
        elif spec == "3":
            read_id_n(file)
            buf.append(read_float(file))
            read_id_n(file)
            buf.append(read_float(file))
            read_id_n(file)
            buf.append(read_float(file))
            read_id_n(file)
            buf.append(read_float(file))
        elif spec == "4":
            buf.append([""])
            border = file.tell() + l_len
            while file.tell() < border:
                r_id, r_len = read_id_n(file)
                r_b = file.tell() + r_len
                while file.tell() < r_b:
                    s_id, s_len = read_id_n(file)
                    if s_id in [1,3,4]:
                        buf[-1][-1] += read_str(file, s_len)
                    else:
                        buf[-1][-1] += "; " + str(read_int(file))
                    if file.tell() < r_b:
                        buf[-1][-1] += "; "
                if file.tell() < border:
                    buf[-1][-1] += " | "
        elif spec == "5":
            buf.append([""])
            border = file.tell() + l_len
            while file.tell() < border:
                r_id, r_len = read_id_n(file)
                r_b = file.tell() + r_len
                while file.tell() < r_b:
                    s_id, s_len = read_id_n(file)
                    if s_id in [1,3,4]:
                        buf[-1][-1] += read_str(file, s_len)
                    else:
                        buf[-1][-1] += "; " + str(read_int(file))
                    if file.tell() < r_b:
                        buf[-1][-1] += "; "
                if file.tell() < border:
                    buf[-1][-1] += " | "
        else:
            print("Skip unknown specificator:", spec, "at", file.tell())
            file.read(l_len)
    
    return buf

def read_data(f_name):
    data = []
    base_type = find_db_struct(f_name)
    with open(f_name, "rb") as file:
        read_id_n(file)
        
        for i in range(len(types_struct[base_type])):
            reg_id, reg_len = read_id_n(file)
            data.append(titles[base_type][i])
            data.append([])
            reg_len += file.tell()
            
            while file.tell() < reg_len:
                data[-1].append(read_record(file, types_struct[base_type][i]))
        is_end = file.read(10)
        if is_end != END:
            print("Some data after table!")
    return data

if __name__ == '__main__':
    if 2 <= len(sys.argv) <= 3:
        data = read_data(sys.argv[1])

        if len(sys.argv) == 2:
            print(build_data(data))
        else:
            with open(sys.argv[2], "w") as file:
                file.write(build_data(data))
    else:
        print("Usage: db.py input.{ilpqsu}db [output.csv]")
