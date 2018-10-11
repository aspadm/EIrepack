meta:
  id: sec
  title: Evil Islands, SEC file (map sector)
  application: Evil Islands
  file-extension: sec
  license: MIT
  endian: le
doc: Map sector
seq:
  - id: magic
    contents: [0x74, 0xF7, 0x4B, 0xCF]
    doc: Magic bytes
  - id: liquids
    type: u1
    doc: Liquids layer indicator
  - id: vertexes
    type: vertex
    doc: Vertex array 33x33
    repeat: expr
    repeat-expr: 1089
  - id: liquid_vertexes
    type: vertex
    doc: Vertex array 33x33
    if: liquids != 0
    repeat: expr
    repeat-expr: 'liquids != 0 ? 1089 : 0'
  - id: tiles
    type: tile
    doc: Tile array 16x16
    repeat: expr
    repeat-expr: 256
  - id: liquid_tiles
    type: tile
    doc: Tile array 16x16
    if: liquids != 0
    repeat: expr
    repeat-expr: 'liquids != 0 ? 256 : 0'
  - id: liquid_material
    type: u2
    doc: Index of material
    if: liquids != 0
    repeat: expr
    repeat-expr: 'liquids != 0 ? 256 : 0'
types:
  vertex:
    doc: Vertex data
    seq:
      - id: x_shift
        type: s1
        doc: Shift by x axis
      - id: y_shift
        type: s1
        doc: Shift by y axis
      - id: altitude
        type: u2
        doc: Height (z position)
      - id: packed_normal
        type: normal
        doc: Packed normal
  normal:
    doc: Normal (3d vector)
    seq:
      - id: packed
        type: u4
        doc: Normal packed in 4b
    instances:
      x:
        doc: Unpacked x component
        value: packed >> 11 & 0x7FF
      y:
        doc: Unpacked y component
        value: packed & 0x7FF
      z:
        doc: Unpacked z component
        value: packed >> 22
  tile:
    doc: Tile parameters
    seq:
      - id: packed
        type: u2
        doc: Tile information packed in 2b
    instances:
      index:
        doc: Tile index in texture
        value: packed & 63
      texture:
        doc: Texture index
        value: packed >> 6 & 255
      rotation:
        doc: Tile rotation (*90 degrees)
        value: packed >> 14 & 3