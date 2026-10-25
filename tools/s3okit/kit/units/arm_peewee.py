"""Peewee (arm_peewee). Coordinates are ENGINE/global: X right, Y up, Z forward. See HANDOFF.md."""
UNIT = dict(
    skeleton='biped',          # standard walker hierarchy; skeleton_opts=dict(height=, hipx=)
    # side='ARM', res=1024, bake_res=2048, ground=True, air=False,
    wreck=dict(seed=1),            # pose={'turret': (0, 30, 0)}, drop=['barrel'], remove=[]
    preview_pose={},              # {'turret': (0, 35, 0)}
)


def build(k):
    P = k.P   # piece name -> global origin (Vector). b.at(x, y, z) = coordinates relative to a piece origin.
    # Blockout: the original TA polygons. Replace piece by piece with real shapes.
    k.standard_legs()   # backwards Federation-style legs, all legs share UVs
    k.piece('torso').from_3do()
    k.piece('luparm').from_3do()
    k.piece('lloarm').from_3do()
    k.piece('ruparm').from_3do()
    k.piece('rloarm').from_3do()
