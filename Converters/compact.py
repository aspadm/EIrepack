import os
import os.path
import shutil
import sys

def compact_figs(dirname="."):
    arr = []
    for i in os.listdir(dirname):
        if os.path.splitext(i)[-1].lower() == ".lnk":
            arr.append(os.path.splitext(i)[0])
##            if os.path.isdir(os.path.join(dirname, arr[-1])):
##                print("Folder exist!", arr[-1])
##                arr = arr[:-1]
        
    arr.sort(key=len, reverse=True)
    files = [f for f in os.listdir(dirname) if os.path.isfile(os.path.join(dirname, f))]
    for i in arr:
        if not os.path.exists(os.path.join(dirname, i)):
            os.makedirs(os.path.join(dirname, i))
        dels = []
        for j in files:
            if j.lower().startswith(i.lower()):
                dels.append(j)
##        print(i, dels)
        for j in dels:
            files.remove(j)
            wk = j if j[-4:].lower() == ".lnk" else j[len(i):]
            shutil.move(os.path.join(dirname, j), os.path.join(dirname, i, wk))

if __name__ == '__main__':
    if 2 == len(sys.argv):
        compact_figs(sys.argv[1])
    else:
        print("Usage: compact.py figures_folder")
