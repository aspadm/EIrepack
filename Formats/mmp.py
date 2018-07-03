import sys
from PIL import Image
import numpy as np
from binary_readers import *

def extract_color(pixel, mask, shift, count):
    return int(0.5 + 255 * ((pixel & mask) >> shift) / (mask >> shift))

def get_color(pixel, a_d, r_d, g_d, b_d):
    if a_d[2] == 0:
        a = 255
    else:
        a = extract_color(pixel, a_d[0], a_d[1], a_d[2])
        
    r = extract_color(pixel, r_d[0], r_d[1], r_d[2])
    g = extract_color(pixel, g_d[0], g_d[1], g_d[2])
    b = extract_color(pixel, b_d[0], b_d[1], b_d[2])
    
    return [r, g, b, a]

def convert_DXT(file, width, height, DXT3=False):
    data = np.zeros((height, width, 4), dtype=np.uint8)
    color = [0, 0, 0, 0]
    
    for i in range(height // 4):
        for j in range(width // 4):
            if DXT3:
                for x in range(4):
                    row = read_ushort(file)
                    for y in range(4):
                        data[i * 4 + x, j * 4 + y, 3] = (row & 15) * 17
                        row >>= 4
                        
            gen_c1 = read_ushort(file)
            gen_c2 = read_ushort(file)
            color[0] = get_color(gen_c1, [0, 0, 0], [63488, 11, 5], [2016, 5, 6], [31, 0, 5])
            color[1] = get_color(gen_c2, [0, 0, 0], [63488, 11, 5], [2016, 5, 6], [31, 0, 5])
            
            if gen_c1 > gen_c2 or DXT3:
                color[2] = [(2 * color[0][i] + color[1][i]) // 3 for i in range(4)]
                color[3] = [(color[0][i] + 2 * color[1][i]) // 3 for i in range(4)]
            else:
                color[2] = [(color[1][i] + color[3][i]) // 2 for i in range(4)]
                color[3] = [0, 0, 0, 0]

            for x in range(4):
                row = read_byte(file)
                for y in range(4):
                    if DXT3:
                        for k in range(3):
                            data[i * 4 + x, j * 4 + y, k] = color[row & 3][k]
                    else:
                        data[i * 4 + x, j * 4 + y] = color[row & 3]
                    row >>= 2

    return data

def read_image(f_name):
    with open(f_name, "rb") as file:
        if file.read(4) != b"\x4D\x4D\x50\x00":
            print("Incorrect magic!")
            return
        
        width = read_uint(file)
        height = read_uint(file)
        mip_count = read_uint(file)
        form = file.read(4)

        if form == b"DXT1":
            file.seek(76)
            data = convert_DXT(file, width, height)
        elif form == b"DXT3":
            file.seek(76)
            data = convert_DXT(file, width, height, DXT3=True)
        elif form == b"PNT3":
            file.seek(76)
            data = decompress_PNT3(file, mip_count, width, height)
        else:
            pixel_size = read_uint(file) // 8
            a_d = read_uint(file, 3)
            r_d = read_uint(file, 3)
            g_d = read_uint(file, 3)
            b_d = read_uint(file, 3)
            file.seek(76)
            data = np.zeros((height, width, 4), dtype=np.uint8)

            if pixel_size == 2:
                pix_reader = read_ushort
            elif pixel_size == 4:
                pix_reader = read_uint
                
            for i in range(height):
                for j in range(width):
                    pixel = pix_reader(file)
                    data[i, j] = get_color(pixel, a_d, r_d, g_d, b_d)

        return Image.fromarray(data, 'RGBA')

def decompress_PNT3(file, size, width, height):
    source = file.read(size)
    src = 0
    
    n = 0
    destination = b""
    
    while src < size:
        v = int.from_bytes(source[src:src + 4], byteorder='little')
        src += 4
        
        if v > 1000000 or v == 0:
            n += 1
        else:
            destination += source[src - (1 + n) * 4:src - 4]
            destination += b"\x00" * v
            n = 0

    destination += source[src - n * 4:src]
    data = np.zeros((height, width, 4), dtype=np.uint8)

    n = 0
    for i in range(height):
        for j in range(width):
            data[i, j] = [int.from_bytes(destination[n + 2:n + 3], byteorder='little'),
                          int.from_bytes(destination[n + 1:n + 2], byteorder='little'),
                          int.from_bytes(destination[n + 0:n + 1], byteorder='little'),
                          int.from_bytes(destination[n + 3:n + 4], byteorder='little')]
            n += 4
            
    return data

if __name__ == '__main__':
    if 2 <= len(sys.argv) <= 3:
        image = read_image(sys.argv[1])
        if len(sys.argv) == 2:
            f_name = sys.argv[1][:-4] + ".png"
        else:
            f_name = sys.argv[2]
        if image != None:
            image.save(f_name)
    else:
        print("Usage: mmp.py input.mmp output.png")
