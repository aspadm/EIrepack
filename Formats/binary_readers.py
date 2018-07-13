import struct

# Unsigned 1b integer
def read_byte(file, count=1):
    array = [] 
    for i in range(count): 
        array.append(struct.unpack('B', file.read(1))[0])
        
    return array if count > 1 else array[0]

# Signed 1b integer
def read_char(file, count=1):
    array = [] 
    for i in range(count): 
        array.append(struct.unpack('b', file.read(1))[0])
        
    return array if count > 1 else array[0]

# Signed 2b integer
def read_short(file, count=1):
    array = [] 
    for i in range(count): 
        array.append(struct.unpack('h', file.read(2))[0])
        
    return array if count > 1 else array[0]

# Unsigned 2b integer
def read_ushort(file, count=1):
    array = [] 
    for i in range(count): 
        array.append(struct.unpack('H', file.read(2))[0])
        
    return array if count > 1 else array[0]

# Signed 4b integer
def read_int(file, count=1):
    array = [] 
    for i in range(count): 
        array.append(struct.unpack('i', file.read(4))[0])
        
    return array if count > 1 else array[0]

# Unsigned 4b integer
def read_uint(file, count=1):
    array = [] 
    for i in range(count): 
        array.append(struct.unpack('I', file.read(4))[0])
        
    return array if count > 1 else array[0]

# Signed 4b integer
def read_int64(file, count=1):
    array = [] 
    for i in range(count): 
        array.append(struct.unpack('q', file.read(8))[0])
        
    return array if count > 1 else array[0]

# Unsigned 8b integer
def read_uin64(file, count=1):
    array = [] 
    for i in range(count): 
        array.append(struct.unpack('Q', file.read(8))[0])
        
    return array if count > 1 else array[0]

# Conversion between 2b half to 4b float
def half_to_float(h):
    s = int((h >> 15) & 0x00000001)    # sign
    e = int((h >> 10) & 0x0000001f)    # exponent
    f = int(h & 0x000003ff)            # fraction

    if e == 0:
       if f == 0:
          return int(s << 31)
       else:
          while not (f & 0x00000400):
             f <<= 1
             e -= 1
          e += 1
          f &= ~0x00000400
    elif e == 31:
       if f == 0:
          return int((s << 31) | 0x7f800000)
       else:
          return int((s << 31) | 0x7f800000 | (f << 13))

    e = e + (127 -15)
    f = f << 13

    return int((s << 31) | (e << 23) | f)

# Hard-float 2b real
def read_half(file, count=1):
    array = [] 
    for i in range(count):
        nz = file.read(2)
        
        v = struct.unpack('H', nz)
        x = half_to_float(v[0])
        # hack to coerce int to float
        pck = struct.pack('I', x)
        f = struct.unpack('f', pck)
        array.append(f[0])
        
    return array if count > 1 else array[0]

# Floating-point 4b real
def read_float(file, count=1):
    array = [] 
    for i in range(count): 
        array.append(struct.unpack('f', file.read(4))[0])
        
    return array if count > 1 else array[0]

# Floating-point 8b real
def read_double(file, count=1):
    array = [] 
    for i in range(count): 
        array.append(struct.unpack('d', file.read(4))[0])
        
    return array if count > 1 else array[0]

# Non-terminated char array
def read_str(file, length, code="cp1251"):
    buf = ""
    for i in range(length):
        b = struct.unpack('c', file.read(1))[0]
        if ord(b) != 0:
            buf += b.decode(code)
    return buf

# Zero-terminated char array (C-style string)
def read_cstr(file, code="cp1251"):
    buf = ""
    while True:
        b = struct.unpack('c', file.read(1))[0]
        
        if b is None or ord(b) == 0:
            return buf
        else:
            buf += b.decode(code)
