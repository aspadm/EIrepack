meta:
  id: evil_islands_reg
  title: Evil Islands, REG file (packed INI)
  application: Evil Islands
  file-extension: reg
  license: MIT
  encoding: cp1251
  endian: le
doc: Packed INI file
doc-ref: https://github.com/aspadm/EIrepack/wiki/reg
seq:
  - id: magic
    contents: [0xFB, 0x3E, 0xAB, 0x45]
  - id: num_sections
    type: u2
  - id: sections_table
    type: section_record
    repeat: expr
    repeat-expr: num_sections
types:
  section_record:
    seq:
      - id: order
        type: s2
        doc: Section order number in file
      - id: ofs_section
        type: u4
        doc: Global section offset in file
    instances:
      section:
        pos: ofs_section
        type: section
    types:
      section:
        seq:
          - id: num_keys
            type: u2
          - id: len_name
            type: u2
            doc: Section name length
          - id: name
            type: str
            size: len_name
            doc: Section name
          - id: keys
            type: key_record
            repeat: expr
            repeat-expr: num_keys
        types:
          key_record:
            doc: Named key
            seq:
              - id: order
                type: s2
                doc: Key order in section
              - id: ofs_key
                type: u4
                doc: Key offset in section
            instances:
              key:
                pos: _parent._parent.ofs_section + ofs_key
                type: key_data
          key_data:
            seq:
              - id: packed_type
                type: u1
              - id: len_name
                type: u2
              - id: name
                type: str
                size: len_name
              - id: num_values
                type: u2
                if: is_array
              - id: value
                type:
                  switch-on: value_type
                  cases:
                    'key_value_types::int_key': s4
                    'key_value_types::float_key': f4
                    'key_value_types::string_key': string_key
                repeat: expr
                repeat-expr: 'is_array ? num_values : 1'
            instances:
              is_array:
                value: packed_type > 127
              value_type:
                value: packed_type & 0x7F
                enum: key_value_types
            enums:
              key_value_types:
                0: int_key
                1: float_key
                2: string_key
            types:
              string:
                seq:
                  - id: len
                    type: u2
                  - id: value
                    type: str
                    size: len
