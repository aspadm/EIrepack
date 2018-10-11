meta:
  id: mp
  title: Evil Islands, MP file (map header)
  application: Evil Islands
  file-extension: mp
  license: MIT
  endian: le
doc: Map header
seq:
  - id: magic
    contents: [0x72, 0xF6, 0x4A, 0xCE]
    doc: Magic bytes
  - id: max_altitude
    type: f4
    doc: Maximal height of terrain
  - id: x_chunks_count
    type: u4
    doc: Number of sectors by x
  - id: y_chunks_count
    type: u4
    doc: Number of sectors by y
  - id: textures_count
    type: u4
    doc: Number of texture files
  - id: texture_size
    type: u4
    doc: Size of texture in pixels by side
  - id: tiles_count
    type: u4
    doc: Number of tiles
  - id: tile_size
    type: u4
    doc: Size of tile in pixels by side
  - id: materials_count
    type: u2
    doc: Number of materials
  - id: animated_tiles_count
    type: u4
    doc: Number of animated tiles
  - id: materials
    type: material
    doc: Map materials
    repeat: expr
    repeat-expr: materials_count
  - id: id_array
    type: u4
    doc: Tile type
    repeat: expr
    repeat-expr: tiles_count
    enum: tile_type
types:
  material:
    doc: Material parameters
    seq:
      - id: type
        type: u4
        doc: Material type by
        enum: terrain_type
      - id: color
        type: rgba
        doc: RGBA diffuse color
      - id: self_illumination
        type: f4
        doc: Self illumination
      - id: wave_multiplier
        type: f4
        doc: Wave speed multiplier
      - id: warp_speed
        type: f4
        doc: Warp speed multiplier
      - id: unknown
        size: 12
    types:
      rgba:
        doc: RGBA color
        seq:
          - id: r
            type: f4
            doc: Red channel
          - id: g
            type: f4
            doc: Green channel
          - id: b
            type: f4
            doc: Blue channel
          - id: a
            type: f4
            doc: Alpha channel
    enums:
      terrain_type:
        0: base
        1: water_notexture
        2: grass
        3: water
enums:
  tile_type:
    0: grass
    1: ground
    2: stone
    3: sand
    4: rock
    5: field
    6: water
    7: road
    8: empty
    9: snow
    10: ice
    11: drygrass
    12: snowballs
    13: lava
    14: swamp
    15: highrock