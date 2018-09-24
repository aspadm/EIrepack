from PIL import Image
import sys

def join_tiles(name, files_count):
    new_map = Image.new("RGB", (2048, 1024))

    count = 0
    for i in range(files_count):
        tileset = Image.open(name + str(i) + ".png")
        for y in range(8):
            for x in range(8):
                new_map.paste(tileset.crop((x*64, y*64, (x+1)*64, (y+1)*64)),
                              (count%32*64, count//32*64))
                count += 1

    new_map.save(name[:-2] + ".png")

if __name__ == '__main__':
    if 3 == len(sys.argv):
        join_tiles(sys.argv[1][:-5], int(sys.argv[2]))
    else:
        print("Usage: convert_map.py input.png tilemap_count")
