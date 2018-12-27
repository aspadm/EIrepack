meta:
  id: mmp
  title: Evil Islands, MMP file (texture)
  application: Evil Islands
  file-extension: mmp
  license: MIT
  endian: le
doc: MIP-mapping texture
seq:
  - id: magic
    contents: [0x4D, 0x4D, 0x50, 0x00]
    doc: Magic bytes
  - id: width
    type: u4
    doc: Texture width
  - id: height
    type: u4
    doc: Texture height
  - id: mip_levels_count
    type: u4
    doc: Number of MIP-mapping stored levels
  - id: fourcc
    type: u4
    enum: pixel_formats
    doc: FourCC label of pixel format
  - id: bits_per_pixel
    type: u4
    doc: Number of bits per pixel
  - id: alpha_format
    type: channel_format
    doc: Description of alpha bits
  - id: red_format
    type: channel_format
    doc: Description of red bits
  - id: green_format
    type: channel_format
    doc: Description of green bits
  - id: blue_format
    type: channel_format
    doc: Description of blue bits
  - id: unused
    size: 4
    doc: Empty space
  - id: base_texture
    type:
      switch-on: fourcc
      cases:
        'pixel_formats::argb4': block_custom
        'pixel_formats::dxt1': block_dxt1
        'pixel_formats::dxt3': block_dxt3
        'pixel_formats::pnt3': block_pnt3
        'pixel_formats::r5g6b5': block_custom
        'pixel_formats::a1r5g5b5': block_custom
        'pixel_formats::argb8': block_custom
        _: block_custom
types:
  block_pnt3:
    seq:
      - id: raw
        size: _root.bits_per_pixel
  block_dxt1:
    seq:
      - id: raw
        size: _root.width * _root.height >> 1
  block_dxt3:
    seq:
      - id: raw
        size: _root.width * _root.height
  block_custom:
    seq:
      - id: lines
        type: line_custom
        repeat: expr
        repeat-expr: _root.height
    types:
      line_custom:
        seq:
          - id: pixels
            type: pixel_custom
            repeat: expr
            repeat-expr: _root.width
        types:
          pixel_custom:
            seq:
              - id: raw
                type:
                  switch-on: _root.bits_per_pixel
                  cases:
                    8: u1
                    16: u2
                    32: u4
            instances:
              alpha:
                value: '_root.alpha_format.count == 0 ? 255 : 255 * ((raw & _root.alpha_format.mask) >> _root.alpha_format.shift) / (_root.alpha_format.mask >> _root.alpha_format.shift)'
              red:
                value: '255 * ((raw & _root.red_format.mask) >> _root.red_format.shift) / (_root.red_format.mask >> _root.red_format.shift)'
              green:
                value: '255 * ((raw & _root.green_format.mask) >> _root.green_format.shift) / (_root.green_format.mask >> _root.green_format.shift)'
              blue:
                value: '255 * ((raw & _root.blue_format.mask) >> _root.blue_format.shift) / (_root.blue_format.mask >> _root.blue_format.shift)'
  channel_format:
    doc: Description of bits for color channel
    seq:
      - id: mask
        type: u4
        doc: Binary mask for channel bits
      - id: shift
        type: u4
        doc: Binary shift for channel bits
      - id: count
        type: u4
        doc: Count of channel bits
enums:
  pixel_formats:
    0x00004444: argb4
    0x31545844: dxt1
    0x33545844: dxt3
    0x33544E50: pnt3
    0x00005650: r5g6b5
    0x00005551: a1r5g5b5
    0x00008888: argb8