import argparse
import os
import os.path
import shutil
import res, mod, bon, adb, anm, cam, db, fig, lnk, mmp, mp, reg, sec, text, mob,\
       convert_map

funcs = []
not_copy = ["asi", "dll", "exe", "sav"]
simple_copy = ["mp3", "rtf", "dat", "grp", "bik", "ini", "txt", "wav",
               "mat", "scr"]
archives = ["mq", "mpr", "res", "bon", "mod", "anm"]
convert = ["cam", "reg", "adb", "bon", "anm", "bon", "db", "idb", "mob",
           "fig", "lnk", "mmp", "mp", "pdb", "qdb", "sec", "sdb", "udb", "ldb"]


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="EIrepack v.0.9a \
(Evil Islands resources unpacker and converter)",
                                     add_help=True)
    parser.add_argument("src_dir", type=str,
                    help="game folder")
    parser.add_argument("dst_dir", type=str,
                    help="output folder")
    parser.add_argument("-v", "--verbose", action="store_true",
                    help="increase output verbosity")
    parser.add_argument("-s", "--skip_extract", action="store_true",
                    help="skip archive extraction")
    parser.add_argument("-c", "--skip_copy", action="store_true",
                    help="skip file copy")
    parser.add_argument("-t", "--text_joint", action="store_true",
                    help="joint game strings")

    args = parser.parse_args()

    if args.verbose:
        print("Source dir: " + args.src_dir)
        print("Destination dir: " + args.dst_dir)
        print("\nCreate working copy\n")

    count = 0
    if not args.skip_copy:
        # Создание папок и копирование контента игры
        for d, dirs, files in os.walk(args.src_dir):
            for file in files:
                if os.path.splitext(file)[1][1:].lower() not in not_copy:
                    dest = os.path.join(args.dst_dir,
                                        os.path.relpath(d, args.src_dir))
                    if not os.path.exists(dest):
                        if args.verbose:
                            print("Create folder \"" + dest + "\"")
                        os.makedirs(dest)
                    shutil.copyfile(os.path.join(d, file),
                                    os.path.join(dest, file))
                    count += 1
                elif args.verbose:
                    print("Skip \"" + file + "\"")

    # Распаковка архивов, пока есть, что распаковывать
    if args.verbose:
        print("{} files copied; no need to read source \
folder anymore".format(count))
        print("\nUnpack archives recursively")

    count = 0
    flag = 0 if args.skip_extract else 1
    while flag:
        count += 1
        flag = 0
        if args.verbose:
            print("\n{} iteration of file unpacking".format(count))

        arr = []
        for d, dirs, files in os.walk(args.dst_dir):
            for file in files:
                if os.path.splitext(file)[1][1:].lower() in archives:
                    with open(os.path.join(d, file), "rb") as f_tst:
                        magic = f_tst.read(4)
                    if magic == b'\x3C\xE2\x9C\x01':
                        print(os.path.join(d, file))
                        flag = 1
                        if file[-3:] == "mod":
                            mod.read_info(os.path.join(d, file))
                        elif file[-3:] == "bon":
                            with open(os.path.join(d, file), "rb") as f:
                                tree = res.read_filetree(f)
                                for element in tree:
                                    element[0] += ".bon"
                                res.unpack_res(f, tree, os.path.join(d, file))
                        elif file[-3:] == "anm":
                            with open(os.path.join(d, file), "rb") as f:
                                tree = res.read_filetree(f)
                                for element in tree:
                                    element[0] += ".anm"
                                res.unpack_res(f, tree, os.path.join(d, file))
                        else:
                            with open(os.path.join(d, file), "rb") as f:
                                filetree = res.read_filetree(f)
                                res.unpack_res(f, filetree, os.path.join(d, file))
                        os.remove(os.path.join(d, file))

    # Конвертация файлов
    if args.verbose:
        print("\nAfter {} iterations all archives unpacked".format(count))
        print("\nConvert files\n")

    maps = []
    count = 0
    for d, dirs, files in os.walk(args.dst_dir):
        for file in files:
            file_e = os.path.splitext(file)[1][1:].lower()
            if file_e in convert:
                count += 1
                file_n = os.path.splitext(file)[0]
                print(os.path.join(d, file))
                if file_e == "adb":
                    try:
                        info = adb.read_info(os.path.join(d, file))
                    except:
                        print("ADB ERROR in file \"{}\"".format(file))
                        info = None
                    if info != None:
                        with open(os.path.join(d, file) + ".yaml", "w") as f:
                            f.write(adb.build_yaml(info))
                elif file_e == "anm":
                    info = anm.read_info(os.path.join(d, file))
                    if info != None:
                        with open(os.path.join(d, file) + ".yaml", "w") as f:
                            f.write(anm.build_yaml(info))
                elif file_e == "bon":
                    info = bon.read_info(os.path.join(d, file))
                    if info != None:
                        with open(os.path.join(d, file) + ".yaml", "w") as f:
                            f.write(bon.build_yaml(info))
                elif file_e == "cam":
                    info = cam.read_info(os.path.join(d, file))
                    if info != None:
                        with open(os.path.join(d, file) + ".yaml", "w") as f:
                            f.write(cam.build_yaml(info))
                elif file_e in ["idb", "ldb", "pdb", "db", "sdb", "udb", "qdb"]:
                    data = db.read_data(os.path.join(d, file))
                    with open(os.path.join(d, file) + ".csv", "w") as f:
                        f.write(db.build_data(data))
                elif file_e == "fig":
                    info = fig.read_info(os.path.join(d, file))
                    if info != None:
                        with open(os.path.join(d, file) + ".yaml", "w") as f:
                            f.write(fig.build_yaml(info))
                elif file_e == "lnk":
                    info = lnk.read_info(os.path.join(d, file))
                    if info != None:
                        with open(os.path.join(d, file) + ".yaml", "w") as f:
                            f.write(lnk.build_yaml(info))
                elif file_e == "mmp":
                    image = mmp.read_image(os.path.join(d, file))
                    image.save(os.path.join(d, file_n) + ".png")
                elif file_e == "mp":
                    maps.append([d, file_n])
                    continue
                    # map convertion later
##                    info = mp.read_info(os.path.join(d, file))
##                    if info != None:
##                        with open(os.path.join(d, file) + ".yaml", "w") as f:
##                            f.write(mp.build_yaml(info))
                elif file_e == "reg":
                    try:
                        info = reg.read_info(os.path.join(d, file))
                    except UnicodeEncodeError:
                        reg.ENCODE = "cp1251"
                        info = reg.read_info(os.path.join(d, file))
                        reg.ENCODE = "cp866"
                    if info != None:
                        with open(os.path.join(d, file) + ".yaml", "w") as f:
                            try:
                                f.write(reg.build_yaml(info))
                            except UnicodeEncodeError:
                                reg.ENCODE = "cp1251"
                                info = reg.read_info(os.path.join(d, file))
                                f.write(reg.build_yaml(info))
                                reg.ENCODE = "cp866"
                elif file_e == "sec":
                    continue
                    # map convertion later
##                    info = sec.read_info(os.path.join(d, file))
##                    if info != None:
##                        with open(os.path.join(d, file) + ".yaml", "w") as f:
##                            f.write(sec.build_yaml(info))
                elif file_e == "mob":
                    info = mob.read_info(os.path.join(d, file))
                    if info != None:
                        with open(os.path.join(d, file) + ".yaml", "w") as f:
                            f.write(mob.build_yaml(info))
                os.remove(os.path.join(d, file))

    if args.verbose:
        print("{} files converted".format(count))
        print("\nConvert game maps\n")

    # Конвертация карт
    # Для этого используются MP, SEC файлы карты и дополнительные текстуры
    count = 0
    for i in maps:
        map_info = mp.read_info(os.path.join(i[0], i[1] + ".mp"))
        count += map_info[3] + map_info[1] * map_info[2] + 1
        for j in range(map_info[3]):
            shutil.copyfile(os.path.join(args.dst_dir, "Res", "textures",
                                         i[1] + "{:03}.png".format(j)),
                            os.path.join(i[0], i[1] + "{:03}.png".format(j)))
        convert_map.convert_map(os.path.join(args.dst_dir, i[1] + ".mp"))

        # Удаляем исходные файлы
        for j in range(map_info[1]):
            for k in range(map_info[2]):
                os.remove(os.path.join(i[0], i[1] + \
                                       "{:03}{:03}.sec".format(j, k)))
        os.remove(os.path.join(i[0], i[1] + ".mp"))

    if args.verbose:
        print("{} files converted ({} maps)".format(count, len(maps)))

    # Конвертация текстов игры
    # Примечание: в оригинальной игре есть кривой файл -
    # "Gipat Medium (тип материала - кожа), мы его пропускаем
    count = 0
    if args.text_joint:
        if args.verbose:
            print("\nJoint game strings\n")
            
        with open(os.path.join(args.dst_dir,
                               "Res", "texts", "texts.yaml"), "w") as file:
            file.write(text.build_yaml(text.read_info(os.path.join(args.dst_dir,
                                                                   "Res", "texts"))))
        for file in os.listdir(os.path.join(args.dst_dir, "Res", "texts")):
            if "." in file or "(" in file:
                continue
            os.remove(os.path.join(args.dst_dir, "Res", "texts", file))
            count += 1
            
        with open(os.path.join(args.dst_dir, "Res",
                               "textslmp", "textslmp.yaml"), "w") as file:
            file.write(text.build_yaml(text.read_info(os.path.join(args.dst_dir,
                                                                   "Res",
                                                                   "textslmp"))))
        for file in os.listdir(os.path.join(args.dst_dir, "Res", "textslmp")):
            if "." in file or "(" in file:
                continue
            os.remove(os.path.join(args.dst_dir, "Res/textslmp", file))
            count += 1
            
        if args.verbose:
            print("{} files converted".format(count))
