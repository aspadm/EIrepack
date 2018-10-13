meta:
  id: res
  title: Evil Islands, RES file (resources archive)
  application: Evil Islands
  file-extension: res
  license: MIT
  endian: le
doc: Resources archive
seq:
  - id: magic
    contents: [0x3C, 0xE2, 0x9C, 0x01]
    doc: Magic bytes
  - id: files_count
    type: u4
    doc: Number of files in archive
  - id: filetable_offset
    type: u4
    doc: Filetable offset
  - id: nametable_size
    type: u4
    doc: Size of filenames
instances:
  nametable_offset:
    value: filetable_offset + 22 * files_count
    doc: Offset of filenames table
  filetable:
    pos: filetable_offset
    type: file_record
    repeat: expr
    repeat-expr: files_count
    doc: Files metadata table
types:
  file_record:
    doc: File metadata
    seq:
      - id: next_index
        type: s4
        doc: Next file index
      - id: file_size
        type: u4
        doc: Size of file in bytes
      - id: file_offset
        type: u4
        doc: File data offset
      - id: last_change
        type: u4
        doc: Unix timestamp of last change time
      - id: name_len
        type: u2
        doc: Lenght of filename
      - id: name_offset
        type: u4
        doc: Filename offset in name array
    instances:
      name:
        io: _root._io
        pos: name_offset + _parent.nametable_offset
        type: str
        encoding: cp1251
        size: name_len
        doc: File name
      data:
        io: _root._io
        pos: file_offset
        size: file_size
        doc: Content of file