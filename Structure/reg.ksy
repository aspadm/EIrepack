meta:
  id: reg
  title: Evil Islands, REG file (packed INI)
  application: Evil Islands
  file-extension: reg
  license: MIT
  endian: le
doc: Packed INI file
seq:
  - id: magic
    contents: [0xFB, 0x3E, 0xAB, 0x45]
    doc: Magic bytes
  - id: sections_count
    type: u2
    doc: Number of sections
  - id: sections_offsets
    type: section_offset
    doc: Sections offset table
    repeat: expr
    repeat-expr: sections_count
types:
  section_offset:
    doc: Section position in file
    seq:
      - id: order
        type: s2
        doc: Section order number
      - id: offset
        type: u4
        doc: Global offset of section in file
    instances:
      section:
        pos: offset
        type: section
    types:
      section:
        doc: Section representation
        seq:
          - id: keys_count
            type: u2
            doc: Number of keys in section
          - id: name_len
            type: u2
            doc: Section name lenght
          - id: name
            type: str
            encoding: cp1251
            size: name_len
            doc: Section name
          - id: keys
            type: key
            doc: Section's keys
            repeat: expr
            repeat-expr: keys_count
        types:
          key:
            doc: Named key
            seq:
              - id: order
                type: s2
                doc: Key order in section
              - id: offset
                type: u4
                doc: Key offset in section
            instances:
              key_record:
                pos: _parent._parent.offset + offset
                type: key_data
          key_data:
            seq:
              - id: packed_type
                type: u1
                doc: Key value info
              - id: name_len
                type: u2
                doc: Key name lenght
              - id: name
                type: str
                encoding: cp1251
                size: name_len
                doc: Key name
              - id: value
                type: value
                doc: Key value
            instances:
              is_array:
                value: packed_type > 127
                doc: Is this key contain array
              value_type:
                value: packed_type & 0x7F
                doc: Key value type
            types:
              value:
                doc: Key value
                seq:
                  - id: array_size
                    type: u2
                    if: _parent.is_array
                    doc: Value array size
                  - id: data
                    type:
                      switch-on: _parent.value_type
                      cases:
                        0: s4
                        1: f4
                        2: string
                    repeat: expr
                    repeat-expr: '_parent.is_array ? array_size : 1'
                    doc: Key value data
              string:
                doc: Sized string
                seq:
                  - id: len
                    type: u2
                    doc: String lenght
                  - id: value
                    type: str
                    encoding: cp1251
                    size: len
                    doc: String
        