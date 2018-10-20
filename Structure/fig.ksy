meta:
  id: fig
  title: Evil Islands, FIG file (figure)
  application: Evil Islands
  file-extension: fig
  license: MIT
  endian: le
doc: 3d mesh
seq:
  - id: magic
    contents: [0x46, 0x49, 0x47, 0x38]
    doc: Magic bytes
  - id: vertex_count
    type: u4
    doc: Number of vertices blocks
  - id: normal_count
    type: u4
    doc: Number of normals blocks
  - id: texcoord_count
    type: u4
    doc: Number of UV pairs
  - id: index_count
    type: u4
    doc: Number of indeces
  - id: vertex_components_count
    type: u4
    doc: Number of vertex components
  - id: morph_components_count
    type: u4
    doc: Number of morphing components
  - id: unknown
    contents: [0, 0, 0, 0]
    doc: Unknown (aligment)
  - id: group
    type: u4
    doc: Render group
  - id: texture_index
    type: u4
    doc: Texture offset
  - id: center
    type: vec3
    doc: Center of mesh
    repeat: expr
    repeat-expr: 8
  - id: aabb_min
    type: vec3
    doc: AABB point of mesh
    repeat: expr
    repeat-expr: 8
  - id: aabb_max
    type: vec3
    doc: AABB point of mesh
    repeat: expr
    repeat-expr: 8
  - id: radius
    type: f4
    doc: Radius of boundings
    repeat: expr
    repeat-expr: 8
  - id: vertex_array
    type: vertex_block
    doc: Blocks of raw vertex data
    repeat: expr
    repeat-expr: 8
  - id: normal_array
    type: vec4x4
    doc: Packed normal data
    repeat: expr
    repeat-expr: normal_count
  - id: texcoord_array
    type: vec2
    doc: Texture coordinates data
    repeat: expr
    repeat-expr: texcoord_count
  - id: index_array
    type: u2
    doc: Triangles indeces
    repeat: expr
    repeat-expr: index_count
  - id: vertex_components_array
    type: vertex_component
    doc: Vertex components array
    repeat: expr
    repeat-expr: vertex_components_count
  - id: morph_components_array
    type: morph_component
    doc: Morphing components array
    repeat: expr
    repeat-expr: morph_components_count
types:
  morph_component:
    doc: Morphing components indeces
    seq:
      - id: morph_index
        type: u2
        doc: Index of morphing data
      - id: vertex_index
        type: u2
        doc: Index of vertex
  vertex_component:
    doc: Vertex components indeces
    seq:
      - id: position_index
        type: u2
        doc: Index of position data
      - id: normal_index
        type: u2
        doc: Index of normal data
      - id: texture_index
        type: u2
        doc: Index of texcoord data
  vec2:
    doc: 2d vector
    seq:
      - id: u
        type: f4
        doc: u axis
      - id: v
        type: f4
        doc: v axis
  vec3:
    doc: 3d vector
    seq:
      - id: x
        type: f4
        doc: x axis
      - id: y
        type: f4
        doc: y axis
      - id: z
        type: f4
        doc: z axis
  vec3x4:
    doc: 3d vector with 4 values per axis
    seq:
      - id: x
        type: f4
        doc: x axis
        repeat: expr
        repeat-expr: 4
      - id: y
        type: f4
        doc: y axis
        repeat: expr
        repeat-expr: 4
      - id: z
        type: f4
        doc: z axis
        repeat: expr
        repeat-expr: 4
  vertex_block:
    doc: Vertex raw block
    seq:
      - id: block
        type: vec3x4
        doc: Vertex data
        repeat: expr
        repeat-expr: _root.vertex_count
  vec4x4:
    doc: 4d vector with 4 values per axis
    seq:
      - id: x
        type: f4
        doc: x axis
        repeat: expr
        repeat-expr: 4
      - id: y
        type: f4
        doc: y axis
        repeat: expr
        repeat-expr: 4
      - id: z
        type: f4
        doc: z axis
        repeat: expr
        repeat-expr: 4
      - id: w
        type: f4
        doc: w axis
        repeat: expr
        repeat-expr: 4