meta:
  id: evil_islands_lnk
  title: Evil Islands, LNK file (bones hierarchy)
  application: Evil Islands
  file-extension: lnk
  license: MIT
  encoding: cp1251
  endian: le
doc: Bones hierarchy
doc-ref: https://github.com/aspadm/EIrepack/wiki/lnk
seq:
  - id: num_bones
    type: u4
  - id: bones
    type: bone
    repeat: expr
    repeat-expr: num_bones
types:
  bone:
    seq:
      - id: len_name
        type: u4
      - id: name
        type: str
        size: len_name
      - id: len_parent_name
        type: u4
      - id: parent_name
        type: str
        size: len_parent_name
