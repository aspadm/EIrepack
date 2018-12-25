meta:
  id: anm
  title: Evil Islands, ANM file (bone animation)
  application: Evil Islands
  file-extension: anm
  license: MIT
  endian: le
doc: Bone animation
seq:
  - id: rotation_frames_count
    type: u4
    doc: Number of rotation frames
  - id: rotation_frames
    type: quat
    repeat: expr
    repeat-expr: rotation_frames_count
    doc: Bone rotations
  - id: translation_frames_count
    type: u4
    doc: Number of translation frames
  - id: translation_frames
    type: vec3
    repeat: expr
    repeat-expr: translation_frames_count
    doc: Bone translation
  - id: morphing_frames_count
    type: u4
    doc: Number of morphing frames
  - id: morphing_vertex_count
    type: u4
    doc: Number of vertices with morphing
  - id: morphing_frames
    type: morphing_frame
    repeat: expr
    repeat-expr: morphing_frames_count
    doc: Array of morphing frames
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
  morphing_frame:
    doc: Array of verteces morphing
    seq:
      - id: vertex_shift
        type: vec3
        repeat: expr
        repeat-expr: _parent.morphing_vertex_count
        doc: Morphing shift per vertex