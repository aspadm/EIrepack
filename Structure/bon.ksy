meta:
  id: bon
  title: Evil Islands, BON file (bone position)
  application: Evil Islands
  file-extension: bon
  license: MIT
  endian: le
doc: Bone position
seq:
  - id: position
    type: vec3
    doc: Bone translation
    repeat: eos
types:
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