from sys import argv
from os import listdir
from os.path import isdir, isfile, normpath, join

def construct_mmp(width, height, packing, data):
    mips = 1
    
    res = bytes([0x4d, 0x4d, 0x50, 0x00])

    res += width.to_bytes(4, "little")
    res += height.to_bytes(4, "little")

    res += mips.to_bytes(4, "little")

    # FourCC
    if packing == "ARGB8":
        res += bytes([0x88, 0x88, 0x00, 0x00])
        bit_count = 32
    elif packing == "DXT1":
        res += bytes([0x44, 0x58, 0x54, 0x31])
        bit_count = 4
    elif packing == "DXT5":
        res += bytes([0x44, 0x58, 0x54, 0x35])
        bit_count = 8
    else:
        raise ValueError("Unknown texture compression")

    res += bit_count.to_bytes(4, "little")

    res += bytes([0] * 48)

    # Offset
    res += bytes([0x00, 0x00, 0x00, 0x00])

    assert(len(res) == 76)
    
    return res + data

def dds_read(file):
    magic = file.read(4)
    assert(magic == b"\x44\x44\x53\x20")

    header_size = int.from_bytes(file.read(4), "little")
    assert(header_size == 124)

    flags = int.from_bytes(file.read(4), "little")

    height = int.from_bytes(file.read(4), "little")
    width = int.from_bytes(file.read(4), "little")

    file.seek(76)

    header_size = int.from_bytes(file.read(4), "little")
    assert(header_size == 32)

    pix_flags = int.from_bytes(file.read(4), "little")

    if pix_flags & 0x4:
        packing = file.read(4).decode("ASCII")

        assert(packing in ["DXT1", "DXT5"])

        if packing == "DXT1":
            data_size = height * width // 2
        else:
            data_size = height * width
    elif pix_flags & 0x1 and pix_flags & 0x40:
        file.read(4)
        assert(file.read(20) == b"\x20\x00\x00\x00\x00\x00\xFF\x00\x00\xFF\x00\x00\xFF\x00\x00\x00\x00\x00\x00\xFF")
        
        packing = "ARGB8"
        data_size = height * width * 4
    else:
        raise ValueError("Unknown format")

    file.seek(128)
    
    data = file.read(data_size)

    print(file.name, packing, width, "x", height, data_size, "bytes")

    assert(len(data) == data_size)

    return [width, height, packing, data]


if __name__ == "__main__":
    files = []

    need_help = False

    if len(argv) > 1:
        if isdir(argv[1]):
            if len(argv) != 3 or not isdir(argv[2]):
                need_help = True
            else:
                # Convert folder
                for fname in listdir(argv[1]):
                    if isfile(join(argv[1], fname)) and fname[-4:].lower() == ".dds":
                        new_name = fname[:-4] + ".mmp"
                        
                        new_name = join(argv[2], new_name)
                        files.append([normpath(join(argv[1], fname)), normpath(new_name)])
        else:
            if len(argv) == 3 and argv[2][-4:].lower() == ".mmp":
                # Convert file to new name
                files.append([normpath(argv[1]), normpath(argv[2])])
            else:
                for fname in argv[1:]:
                    if isfile(fname) and fname[-4:].lower() == ".dds":
                        new_name = fname[:-4] + ".mmp"

                        files.append([normpath(fname), normpath(new_name)])
                    else:
                        need_help = True
                        break
    else:
        need_help = True

    if len(files) == 0:
        print("No files to convert!\n")
        need_help = True

    if need_help:
        print("DDS to MMP converter v1.0 by aspadm\n")
        print("Support no-mipmap DXT1, DXT5, RGBA8\n")
        print("Usage:\ndds2mmp.exe in.dds\ndds2mmp.exe in1.dds in2.dds ...")
        print("dds2mmp.exe in.dds out.mmp\ndds2mmp.exe input_folder output_folder")
    else:
        print("Will be converted:")
        for pair in files:
            print(pair[0], "->", pair[1])

        print("\nStart convertion\n")

        for pair in files:
            try:
                with open(pair[0], "rb") as f:
                    src = dds_read(f)

                with open(pair[1], "wb") as f:
                    f.write(construct_mmp(*src))
            except:
                print("Some error with file", pair[0])


        print("\nConvertion ended")
