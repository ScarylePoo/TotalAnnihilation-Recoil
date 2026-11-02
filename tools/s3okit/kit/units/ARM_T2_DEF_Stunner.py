"""Stunner (ARM_T2_DEF_Stunner) - Arm EMP missile launcher. Closed it is a compact gabled block: four light corner
towers with two sloping roof covers between them over a buried launch pit. To fire, the hazard-striped pit doors slide
apart, the four towers roll outward 14.5 elmo and the roof covers slide out and swing 90 deg up, leaving the EMP
missile (cyan glowing nose) standing in the open pit between two pairs of towers.
Identity from above: closed = a light rectangle with team tower tops and a dark roof ridge; open = four light team-
capped towers in two pairs, two hazard pit doors and a dark pit with a cyan dot - an 'H' where the Core Neutron is a
dark star.
Pieces (COB): GP, Base, Door1/2, Frame1..4 (move x), Cover1/2 (move x, turn z), Dummy (hide/show: the missile),
Launch (emit). The preview shows the OPEN state.
Coordinates are ENGINE/global: X right, Y up, Z forward."""
import math

UNIT = dict(
    res=2048, bake_res=2048,          # no 2x supersampling: machine time (see the batch report)
    wreck=dict(seed=27, drop=['Cover2'], remove=['Dummy']),
    preview_pose={'Door1': {'move': (-7.25, 0, 0)}, 'Door2': {'move': (7.25, 0, 0)},
                  'Frame1': {'move': (-14.5, 0, 0)}, 'Frame2': {'move': (-14.5, 0, 0)},
                  'Frame3': {'move': (14.5, 0, 0)}, 'Frame4': {'move': (14.5, 0, 0)},
                  'Cover1': {'move': (-7.5, 0, 0), 'rot': (0, 0, -90)}, 'Cover2': {'move': (7.5, 0, 0), 'rot': (0, 0, 90)}},
)


def tower(f, sx, sz):
    """corner tower: x from 0 to sx*9, z from sz*11.2 to sz*23.5, 28 tall with a chamfered top; team roof plate"""
    X = lambda u: sx * u
    Z = lambda w: sz * w
    f.hull([(X(x), y, Z(z)) for x in (0.2, 8.8) for z in (11.4, 23.3) for y in (0.0,)] +
           [(X(x), 20.0, Z(z)) for x in (0.2, 8.8) for z in (11.4, 23.3)] +
           [(X(x), 26.0, Z(z)) for x in (0.6, 7.0) for z in (12.4, 21.0)], 'paint', bevel=0.3)
    f.hull([(X(x), y, Z(z)) for x in (1.4, 6.2) for z in (13.4, 20.0) for y in (25.95, 26.2)], 'team', bevel=0.0)
    # dark side band where the cover meets the tower, and a cyan status light
    f.hull([(X(x), y, Z(z)) for x in (0.0, 9.0) for z in (11.2, 12.2) for y in (2.0, 18.0)], 'dark', bevel=0.06)
    f.box((X(3.6) if sx > 0 else X(5.4), 14.0, Z(23.3) if sz > 0 else Z(23.6)),
          (X(5.4) if sx > 0 else X(3.6), 15.4, Z(23.6) if sz > 0 else Z(23.3)), 'lightc', bevel=0.0)


def build(k):
    # ------------------------------------------------------------------ Base: ground slab round the launch pit
    b = k.piece('Base')
    for lo, hi in (((-24.0, -20.0), (24.0, -11.4)), ((-24.0, 11.4), (24.0, 20.0)),
                   ((-24.0, -11.4), (-17.2, 11.4)), ((17.2, -11.4), (24.0, 11.4))):
        b.box((lo[0], 0.0, lo[1]), (hi[0], 1.4, hi[1]), 'paint2', bevel=0.2)
    # team strips on the slab ends between the tower pairs
    for sz in (-1, 1):
        b.box((-10.0, 1.3, min(sz * 13.2, sz * 18.6)), (10.0, 1.6, max(sz * 13.2, sz * 18.6)), 'team', bevel=0.04)
    # door rails
    for z in (-11.0, 11.0):
        b.box((-23.6, 1.3, z - 0.8), (23.6, 1.8, z + 0.8), 'dark', bevel=0.05)
    # pit: dark walls and a black floor
    b.box((-17.0, -11.4, -11.2), (17.0, -10.6, 11.2), 'black', bevel=0.0)
    for lo, hi in (((-17.0, -11.4), (17.0, -10.6)), ((-17.0, 10.6), (17.0, 11.4))):
        b.box((lo[0], -11.0, lo[1]), (hi[0], 0.2, hi[1]), 'dark', bevel=0.0)
    for lo, hi in (((-17.2, -11.2), (-16.4, 11.2)), ((16.4, -11.2), (17.2, 11.2))):
        b.box((lo[0], -11.0, lo[1]), (hi[0], 0.2, hi[1]), 'dark', bevel=0.0)

    # ------------------------------------------------------------------ Doors: hazard-striped pit doors
    d1 = k.piece('Door1')
    d1.box((-16.6, 0.2, -11.0), (0.0, 2.6, 11.0), 'dark', bevel=0.12)
    d1.box((-15.8, 2.5, -10.2), (-0.8, 2.75, 10.2), 'hazard', bevel=0.03)
    k.clone('Door2', 'Door1', mirror_x=True)

    # ------------------------------------------------------------------ Frames: the four corner towers
    tower(k.piece('Frame1'), -1, 1)
    tower(k.piece('Frame2'), -1, -1)
    k.clone('Frame4', 'Frame1', mirror_x=True)
    k.clone('Frame3', 'Frame2', mirror_x=True)

    # ------------------------------------------------------------------ Covers: sloping roof panels (Cover1 origin 0, 5, 0)
    c = k.piece('Cover1'); C = c.at
    c.hull([C(x, y, z) for x, y in ((-7.4, 0.0), (-7.4, 1.6), (0.0, 11.0), (0.0, 12.4)) for z in (-11.0, 11.0)], 'paint2', bevel=0.2)
    c.hull([C(x, y + 0.08, z) for x, y in ((-6.0, 1.8), (-1.2, 11.0)) for z in (-8.4, 8.4)] +
           [C(x, y + 0.3, z) for x, y in ((-6.0, 1.8), (-1.2, 11.0)) for z in (-8.4, 8.4)], 'team', bevel=0.0)
    c.box(C(-1.0, 11.2, -11.0), C(0.0, 12.6, 11.0), 'dark', bevel=0.06)
    k.clone('Cover2', 'Cover1', mirror_x=True)

    # ------------------------------------------------------------------ Dummy: the EMP missile in the pit
    m = k.piece('Dummy')
    m.cyl((0, -11.0, 0), (0, -1.0, 0), 2.6, 10, 'paint', bevel=0.05)
    m.cyl((0, -1.0, 0), (0, 3.0, 0), 2.6, 10, 'steel', r2=0.6, bevel=0.04)
    m.cyl((0, -2.0, 0), (0, -1.0, 0), 2.7, 10, 'lightc')
    for ang in (45, 135, 225, 315):
        a = math.radians(ang)
        m.hull([(math.cos(a) * rr, y, math.sin(a) * rr) for rr in (2.0, 4.6) for y in (-11.0, -7.0)] +
               [(math.cos(a) * 2.0, -4.0, math.sin(a) * 2.0)], 'dark', bevel=0.0)
