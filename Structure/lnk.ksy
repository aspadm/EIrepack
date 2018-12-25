meta:
  id: lnk
  title: Evil Islands, LNK file (bones hierarchy)
  application: Evil Islands
  file-extension: lnk
  license: MIT
  endian: le
doc: Bones hierarchy
seq:
  - id: bones_count
    type: u4
    doc: Number of bones
  - id: bones_array
    type: bone
    repeat: expr
    repeat-expr: bones_count
    doc: Array of bones
types:
  bone:
    doc: Bone node
    seq:
      - id: bone_name_len
        type: u4
        doc: Length of bone's name
      - id: bone_name
        type: str
        encoding: cp1251
        size: bone_name_len
        doc: Bone's name
      - id: parent_name_len
        type: u4
        doc: Length of bone's parent name
      - id: parent_name
        type: str
        encoding: cp1251
        size: parent_name_len
        doc: Bone's parent name