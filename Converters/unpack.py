import sys
import argparse
import os
import os.path
import shutil
import res, mod, bon, adb, anm, cam, db, fig, lnk, mmp, mp, reg, sec, text, mob,\
       convert_map, compact, convert_model, textures_link, merge_collada

from PyQt5 import QtWidgets#, uic
from PyQt5.QtCore import QThread, pyqtSignal
from PyQt5.QtWidgets import QFileDialog, QMessageBox

from GUI import Ui_Form

import time

funcs = []
not_copy = ["asi", "dll", "exe", "sav"]
simple_copy = ["mp3", "rtf", "dat", "grp", "bik", "ini", "txt", "wav",
               "mat", "scr"]
archives = ["mq", "mpr", "res", "bon", "mod", "anm"]
convert = ["cam", "reg", "adb", "bon", "anm", "bon", "db", "idb", "mob",
           "fig", "lnk", "mmp", "mp", "pdb", "qdb", "sec", "sdb", "udb", "ldb"]

def unpack(args):
    update_progress("STARTED_AT_" + time.strftime("%H:%M:%S"))
    if args.verbose:
        print_log("Source dir: " + args.src_dir)
        print_log("Destination dir: " + args.dst_dir)
        print_log("\nCreate working copy\n")

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
                            print_log("Create folder \"" + dest + "\"")
                        os.makedirs(dest)
                    shutil.copyfile(os.path.join(d, file),
                                    os.path.join(dest, file))
                    count += 1
                    update_progress()
                elif args.verbose:
                    print_log("Skip \"" + file + "\"")

    update_progress("FOLDERS_CONVERTED_" + time.strftime("%H:%M:%S"))
    # Распаковка архивов, пока есть, что распаковывать
    if args.verbose:
        print_log("{} files copied; no need to read source \
folder anymore".format(count))
        print_log("\nUnpack archives recursively")

    count = 0
    flag = 0 if args.skip_extract else 1
    while flag:
        count += 1
        flag = 0
        if args.verbose:
            print_log("\n{} iteration of file unpacking".format(count))

        arr = []
        for d, dirs, files in os.walk(args.dst_dir):
            for file in files:
                if os.path.splitext(file)[1][1:].lower() in archives:
                    with open(os.path.join(d, file), "rb") as f_tst:
                        magic = f_tst.read(4)
                    if magic == b'\x3C\xE2\x9C\x01':
                        print_log(os.path.join(d, file))
                        update_progress()
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

    update_progress("ARCHIVES_CONVERTED_" + time.strftime("%H:%M:%S"))
    if args.verbose:
        print_log("\nAfter {} iterations all archives unpacked".format(count))
        print_log("\nStart figures folder reorganisation\n")

    try:
        compact.compact_figs(os.path.join(args.dst_dir, "Res", "figures"))
    except:
        if args.verbose:
            print_log("Can't reorganise figures folder!")

    # Конвертация файлов
    if args.verbose:
        print_log("\nFigures folder reorganised\n")

    if not args.skip_convert:
        if args.verbose:
            print_log("\nConvert files\n")
        static_objs = {} # name, objname, texture, complection, position, rotation, parts
        maps = []
        figs = []
        count = 0
        for d, dirs, files in os.walk(args.dst_dir):
            for file in files:
                file_e = os.path.splitext(file)[1][1:].lower()
                if file_e in convert:
                    count += 1
                    update_progress()
                    file_n = os.path.splitext(file)[0]
                    print_log(os.path.join(d, file))
                    if file_e == "adb":
                        try:
                            info = adb.read_info(os.path.join(d, file))
                        except:
                            print_log("ADB ERROR in file \"{}\"".format(file))
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
                        continue
                        # model convertion later
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
                        continue
                        # model convertion later
                    elif file_e == "lnk":
                        figs.append([d, file_n])
                        continue
                        # model convertion later
                    elif file_e == "mmp":
                        image = mmp.read_image(os.path.join(d, file))
                        image.save(os.path.join(d, file_n) + ".png")
                    elif file_e == "mp":
                        maps.append([d, file_n])
                        continue
                        # map convertion later
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
                    elif file_e == "mob":
                        info = mob.read_info(os.path.join(d, file))
                        if info != None:
                            with open(os.path.join(d, file) + ".yaml", "w") as f:
                                f.write(mob.build_yaml(info))
                        # Просмотрим файл на статику
                        buf_objs = []
                        with open(os.path.join(d, file) + ".yaml") as f:
                            cnt = 0
                            for line in f.readlines():
                                if len(line) > 100:
                                    continue
                                buf = line.replace("\n", "").replace("\r", "").\
                                           replace(" ", "").replace("\"", "").split(":")

                                if cnt > 0:
                                    if buf_objs[-1][var_lbl][-cnt] is None:
                                        buf_objs[-1][var_lbl][-cnt] = float(buf[0][1:])
                                        cnt -= 1
                                    continue
                                elif cnt < 0:
                                    if buf[0][0] == "-":
                                        buf_objs[-1][6].append(buf[0][1:])
                                        continue
                                    else:
                                        cnt = 0
                                
                                if buf[0] == "OBJTEMPLATE":
                                    count += 1
                                    buf_objs[-1][0] = buf[1]
                                    buf_objs[-1][1] = buf[1] + "_" + file_n + "_{}".format(count)
                                if buf[0] == "OBJPRIMTXTR" and buf_objs[-1][2] is None:
                                    buf_objs[-1][2] = buf[1]
                                if buf[0] == "OBJCOMPLECTION":
                                    var_lbl = 3
                                    cnt = 3
                                if buf[0] == "OBJPOSITION":
                                    var_lbl = 4
                                    cnt = 3
                                if buf[0] == "OBJROTATION":
                                    var_lbl = 5
                                    cnt = 4
                                if buf[0] == "OBJBODYPARTS":
                                    buf_objs.append([None, None, None, [None, None, None],
                                                     [None, None, None], [None, None, None,
                                                     None], None])
                                    if buf[1] != "None":
                                        buf_objs[-1][6] = []
                                        var_lbl = 6
                                        cnt = -1
                
                        static_objs.update({file_n.lower(): buf_objs})
                    os.remove(os.path.join(d, file))

        update_progress("COMMON_CONVERTED_" + time.strftime("%H:%M:%S"))
        if args.verbose:
            print_log("{} files converted".format(count))
            print_log("\nConvert game maps\n")

        # Конвертация карт
        # Для этого используются MP, SEC файлы карты и дополнительные текстуры
        count = 0
        for i in maps:
            if i[1].lower() not in static_objs:
                if os.path.isfile(os.path.join(args.dst_dir, "Maps",
                                               i[1] + ".mob.yaml")):
                    # Просмотрим файл на статику
                    buf_objs = []
                    with open(os.path.join(args.dst_dir, "Maps",
                                           i[1] + ".mob.yaml")) as f:
                        cnt = 0
                        for line in f.readlines():
                            if len(line) > 100:
                                continue
                            buf = line.replace("\n", "").replace("\r", "").\
                                       replace(" ", "").replace("\"", "").split(":")

                            if cnt > 0:
                                if buf_objs[-1][var_lbl][-cnt] is None:
                                    buf_objs[-1][var_lbl][-cnt] = float(buf[0][1:])
                                    cnt -= 1
                                continue
                            elif cnt < 0:
                                if buf[0][0] == "-":
                                    buf_objs[-1][6].append(buf[0][1:])
                                    continue
                                else:
                                    cnt = 0
                            
                            if buf[0] == "OBJTEMPLATE":
                                count += 1
                                buf_objs[-1][0] = buf[1]
                                buf_objs[-1][1] = buf[1] + "_" + i[1] + "_{}".format(count)
                            if buf[0] == "OBJPRIMTXTR" and buf_objs[-1][2] is None:
                                buf_objs[-1][2] = buf[1]
                            if buf[0] == "OBJCOMPLECTION":
                                var_lbl = 3
                                cnt = 3
                            if buf[0] == "OBJPOSITION":
                                var_lbl = 4
                                cnt = 3
                            if buf[0] == "OBJROTATION":
                                var_lbl = 5
                                cnt = 4
                            if buf[0] == "OBJBODYPARTS":
                                buf_objs.append([None, None, None, [None, None, None],
                                                 [None, None, None], [None, None, None,
                                                 None], None])
                                if buf[1] != "None":
                                    buf_objs[-1][6] = []
                                    var_lbl = 6
                                    cnt = -1
            
                    static_objs.update({i[1].lower(): buf_objs})
                else:
                    static_objs.update({i[1].lower(): None})
            
            # Параметры карты
            map_info = mp.read_info(os.path.join(i[0], i[1] + ".mp"))
            if args.verbose:
                print_log(os.path.join(i[0], i[1]),
                      "  + {} textures and {}x{} sectors".format(map_info[3],
                                                                 map_info[1],
                                                                 map_info[2]))
            count += map_info[3] + map_info[1] * map_info[2] + 1
            update_progress(map_info[3] + map_info[1] * map_info[2] + 1)
            # Скопируем текстуры
            for j in range(map_info[3]):
                shutil.copyfile(os.path.join(args.dst_dir, "Res", "textures",
                                             i[1] + "{:03}.png".format(j)),
                                os.path.join(i[0], i[1] + "{:03}.png".format(j)))

            if static_objs[i[1].lower()] is not None:
                # Позиции юнитов на карте, с относительной Z
                unit_pos = [s_obj[4] for s_obj in static_objs[i[1].lower()]]
                if len(unit_pos) == 0:
                    unit_pos = None
            else:
                unit_pos = None
                
            # Конвертация карты и текстур, получение Z координаты юнитов
            unit_pos = convert_map.convert_map(os.path.join(i[0], i[1]), unit_pos)

            if static_objs[i[1].lower()] is not None:
                # Сконвертируем статику
                # name, objname, texture, complection, position, rotation, parts
                list_fpath_inputs = [os.path.join(args.dst_dir, "Res", "figures",
                                                  s_obj[0], s_obj[1] + ".dae") \
                                     for s_obj in static_objs[i[1].lower()]]

                for k, s_obj in enumerate(static_objs[i[1].lower()]):
                    convert_model.convert_model(os.path.join(args.dst_dir, "Res", "figures",
                                                             s_obj[0], s_obj[0]),
                                                add_suf=s_obj[1][len(s_obj[0]):],
                                                coefs=s_obj[3],
                                                root_pos=unit_pos[k],
                                                root_rot=s_obj[5],
                                                tex_name=s_obj[2],
                                                need_parts=s_obj[6])

                ind = 0
                while ind < len(list_fpath_inputs):
                    if os.path.isfile(list_fpath_inputs[ind]):
                        ind += 1
                    else:
                        print_log("File {} not exist".format(list_fpath_inputs.pop(ind)))
                
                # Создадим карту со статикой
                list_fpath_inputs.append(os.path.join(i[0], i[1]) + ".dae")
                merge_collada.merge_dae_files(list_fpath_inputs,
                                              os.path.join(i[0], i[1] + "_full.dae"),
                                              i[1] + "_full")
                
                # Скопируем текстуры статики
                for s_obj in static_objs[i[1].lower()]:
                    if not os.path.isfile(os.path.join(i[0], s_obj[2] + ".png")):
                        shutil.copyfile(os.path.join(args.dst_dir, "Res", "textures",
                                                     s_obj[2] + ".png"),
                                        os.path.join(i[0], s_obj[2] + ".png"))

                # Удалим использованную статику
                for st_dae in list_fpath_inputs[:-1]:
                    os.remove(st_dae)

            # Удаляем исходные файлы
            for j in range(map_info[1]):
                for k in range(map_info[2]):
                    os.remove(os.path.join(i[0], i[1] + \
                                           "{:03}{:03}.sec".format(j, k)))
            for j in range(map_info[3]):
                os.remove(os.path.join(i[0], i[1] + "{:03}.png".format(j)))
            os.remove(os.path.join(i[0], i[1] + ".mp"))

        update_progress("MAPS_CONVERTED_" + time.strftime("%H:%M:%S"))
        if args.verbose:
            print_log("{} files converted ({} maps)".format(count, len(maps)))
            print_log("\nConvert models\n")            
            
        # Конвертация моделей
        # Включает LNK, SEC, ANM, BON файлы
        count = 0
        for i in figs:
            print_log(i[0])
            try:
                if convert_model.convert_model(os.path.join(i[0], i[1])) is not None:
                    continue
            except Exception as e:
                print_log(str(e))
                continue
            # Копируем текстуры
            for j in textures_link.textures.get(i[1], []):
                try:
                    shutil.copyfile(os.path.join(args.dst_dir, "Res",
                                                 "textures",
                                                 j + ".png"),
                                    os.path.join(i[0], j + ".png"))
                except Exception as e:
                    print_log(str(e))

            filelist = convert_model.flat_tree(lnk.read_info(
                os.path.join(i[0], i[1] + ".lnk")))
            count += 1 + len(filelist) * 2
            update_progress(1 + len(filelist) * 2)

            # Удаляем исходные файлы
            for j in filelist:
                os.remove(os.path.join(i[0], j + ".fig"))
                os.remove(os.path.join(i[0], j + ".bon"))
            os.remove(os.path.join(i[0], i[1] + ".lnk"))
            
        update_progress("FIGURES_CONVERTED_" + time.strftime("%H:%M:%S"))
        if args.verbose:
            print_log("{} files converted".format(count))

    # Конвертация текстов игры
    # Примечание: в оригинальной игре есть кривой файл -
    # "Gipat Medium (тип материала - кожа), мы его пропускаем
    count = 0
    if args.text_joint and os.path.isdir(os.path.join(args.dst_dir,
                               "Res", "texts")):
        if args.verbose:
            print_log("\nJoint game strings\n")
            
        with open(os.path.join(args.dst_dir,
                               "Res", "texts", "texts.yaml"), "w") as file:
            file.write(text.build_yaml(text.read_info(os.path.join(args.dst_dir,
                                                                   "Res", "texts"))))
        for file in os.listdir(os.path.join(args.dst_dir, "Res", "texts")):
            if "." in file or "(" in file:
                continue
            os.remove(os.path.join(args.dst_dir, "Res", "texts", file))
            count += 1
            update_progress()
            
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
            update_progress()

        update_progress("TEXTS_CONVERTED_" + time.strftime("%H:%M:%S"))
        if args.verbose:
            print_log("{} files converted".format(count))


class Thread(QThread):
    args = None
    print_call = pyqtSignal(str)
    progress_call = pyqtSignal(int)
    complete_call = pyqtSignal()
    progress = 0
    
    def __init__(self, parent=None):
        QThread.__init__(self, parent=parent)
        self.isRunning = True

    def run(self):
        self.progress = 0
        self.add_progress(0)
        unpack(self.args)
        w.start.setEnabled(True)
        print_log("\nEnd of convertion\n")
        self.complete_call.emit()

    def stop(self):
        self.isRunning = False
        self.quit()
        self.wait()

    def print_c(self, string):
        self.print_call.emit(string)

    def add_progress(self, value=1):
        if type(value) == str:
            print(value, self.progress)
        else:
            self.progress += value
            self.progress_call.emit(self.progress)

def start_unpack():
    max_progress = 50033
    w.start.setEnabled(False)
    argarr = [w.src_folder.text()]
    
    if not w.in_place.isChecked():
        argarr.append(w.dst_folder.text())
        if not w.need_copy.isChecked():
            argarr.append("--skip_copy")
            max_progress -= 287
    else:
        argarr.append(w.src_folder.text())
        argarr.append("--skip_copy")
        max_progress -= 287
    
    if not w.need_extracting.isChecked():
        argarr.append("--skip_extract")
        max_progress -= 2009
    if not w.need_converting.isChecked():
        argarr.append("--skip_convert")
        max_progress -= 47737
    if w.need_verbose.isChecked():
        argarr.append("--verbose")
    if w.need_text_merging.isChecked():
        argarr.append("--text_joint")
        max_progress += 3561

    w.progress.setMaximum(max_progress)
    unpack_thread.args = parser.parse_args(argarr)
    unpack_thread.start()

def lock_dst():
    w.dst_folder.setEnabled(not w.in_place.isChecked())
    w.dst_folder_choser.setEnabled(not w.in_place.isChecked())
    w.need_copy.setEnabled(not w.in_place.isChecked())

def choose_src():
    src_folder_new = QFileDialog.getExistingDirectory(
        caption="Выберите директорию игры (содержит файл game.exe)")
    if src_folder_new != "":
        w.src_folder.setText(src_folder_new)

def choose_dst():
    dst_folder_new = QFileDialog.getExistingDirectory(
        caption="Выберите папку для экспортированных файлов")
    if dst_folder_new != "":
        w.dst_folder.setText(dst_folder_new)

def phldr(val=1):
    pass

def complete():
    QMessageBox.information(window, "Конвертация завершена",
                                "Все операции выполнены!")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="EIrepack v1.0 \
(Evil Islands resources unpacker and converter)",
                                     add_help=True)
    parser.add_argument("src_dir", type=str,
                    help="game folder")
    parser.add_argument("dst_dir", type=str,
                    help="output folder")
    parser.add_argument("-v", "--verbose", action="store_true",
                    help="increase output verbosity")
    parser.add_argument("-c", "--skip_copy", action="store_true",
                    help="skip file copy")
    parser.add_argument("-s", "--skip_extract", action="store_true",
                    help="skip archive extraction")
    parser.add_argument("-r", "--skip_convert", action="store_true",
                    help="skip files convertion")
    parser.add_argument("-t", "--text_joint", action="store_true",
                    help="joint game strings")

    if len(sys.argv) > 1:
        print_log = print
        print_log("Starting console version. \
For GUI start program without arguments.\n")

        update_progress = phldr

        args = parser.parse_args()
        unpack(args)
    else:
        app = QtWidgets.QApplication(sys.argv)
        #w = uic.loadUi("GUI.ui")

        window = QtWidgets.QWidget()
        w = Ui_Form()
        w.setupUi(window)

        unpack_thread = Thread()
        
        print_log = unpack_thread.print_c
        update_progress = unpack_thread.add_progress

        unpack_thread.print_call.connect(w.log_window.append)
        unpack_thread.progress_call.connect(w.progress.setValue)
        unpack_thread.complete_call.connect(complete)
        
        print_log("Starting GUI version. \
For console version use some arguments (like --help).\n")

        w.start.clicked.connect(start_unpack)
        w.in_place.clicked.connect(lock_dst)
        w.src_folder_choser.clicked.connect(choose_src)
        w.dst_folder_choser.clicked.connect(choose_dst)
        
        window.show()
        sys.exit(app.exec_())
    
