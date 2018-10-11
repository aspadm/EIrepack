meta:
  id: cam
  title: Evil Islands, CAM file (cameras)
  application: Evil Islands
  file-extension: cam
  license: MIT
  endian: le
doc: Camera representation
seq:
  - id: cams
    type: camera
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
  quat:
    doc: quaternion
    seq:
      - id: w
        type: f4
        doc: w component
      - id: x
        type: f4
        doc: x component
      - id: y
        type: f4
        doc: y component
      - id: z
        type: f4
        doc: z component
  camera:
    doc: Camera parameters
    seq:
      - id: unkn0
        type: u4
        doc: unknown
      - id: unkn1
        type: u4
        doc: unknown
      - id: position
        type: vec3
        doc: camera's position
      - id: rotation
        type: quat
        doc: camera's rotation
