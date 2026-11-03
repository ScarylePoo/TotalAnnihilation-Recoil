"""Construction Seaplane (ARM_T1_SEAPL_Constructor) - Arm T1 sea builder. A fat flying-boat hull with a chined planing
bottom and, unlike any other Arm aircraft, one huge sponson on its left cheek (Cab) carrying the nano gear: the sponson
roof is the big construction-striped block, so from above the unit is a light barrel with a striped slab on one side.
Short wings with tip floats slide out of the belly on take-off (COB move x +-12: LWing goes to +x, RWing to -x). V-tail.
Pieces (TA layout): GP (empty), Base, Cab, LWing (RWing = mirrored clone), Wake1/Wake2, NanoPoint (empty, keel).
Value groups from above: light hull and wings, dark nano mounts and engines, striped sponson, team on the fins, the
hull roof band and the wing outer panels.
Coordinates are ENGINE/global: X right, Y up, Z forward. mirror=True builds the -X twin sharing UVs."""
import math

UNIT = dict(
    res=1024,
    wreck=dict(seed=35, remove=['RWing'], drop=[]),
    preview_pose={'LWing': {'move': (12.0, 0, 0)}, 'RWing': {'move': (-12.0, 0, 0)}},    # flight (engine x = -COB x)
)


def build(k):
    b = k.piece('Base')
    # ------------------------------------------------------------------ boat hull (crosses x = 0)
    b.hull([(x * sx, y, z) for sx in (-1, 1) for x, y, z in
            [(0.8, 0.0, 16.0), (0.8, 0.0, -9.0), (9.6, 2.4, 10.0), (9.6, 2.2, -7.0), (5.0, 2.4, 19.6),
             (2.6, 5.4, 21.6), (6.8, 10.6, 12.0), (8.2, 8.4, 5.0), (8.2, 8.4, -9.0), (6.0, 11.2, -8.0), (5.8, 11.6, 5.0),
             (4.2, 5.0, -21.0), (3.8, 10.0, -21.0)]], 'paint', bevel=0.2, seg=2)
    # glazed nose
    b.hull([(x * sx, y, z) for sx in (-1, 1) for x, y, z in
            [(2.4, 5.6, 21.5), (5.0, 8.4, 15.8), (3.8, 11.0, 11.4), (2.2, 5.74, 21.62), (4.8, 8.56, 15.95), (3.6, 11.15, 11.5)]],
           'glass', bevel=0.05)
    b.box((-2.2, 2.8, 20.8), (2.2, 3.6, 21.2), 'lightw', bevel=0.0)
    # team roof band (hull top is flat at about y 11.6 between z 5 and -8)
    b.hull([(x * sx, y, z) for sx in (-1, 1) for x, y, z in
            [(5.0, 11.62, 5.0), (5.0, 11.8, 5.0), (5.0, 11.24, -8.0), (5.0, 11.42, -8.0)]], 'team', bevel=0.0)
    # engines on the rear deck
    for x in (3.6,):
        b.cyl((x, 12.4, 0.0), (x, 12.4, -12.0), 1.9, 12, 'dark', bevel=0.05, mirror=True)
        b.cyl((x, 12.4, -11.95), (x, 12.4, -12.1), 1.2, 10, 'lightc', mirror=True)
    # V-tail
    b.hull([(2.8, 9.0, -11.0), (3.0, 8.8, -21.0), (12.4, 15.2, -19.6), (12.4, 15.2, -24.2),
            (2.2, 9.6, -11.0), (2.4, 9.4, -21.0), (12.0, 15.6, -19.6), (12.0, 15.6, -24.2)], 'paint', bevel=0.07, mirror=True)
    b.hull([(7.0, 12.0, -14.6), (7.2, 11.9, -22.4), (12.4, 15.5, -19.6), (12.4, 15.5, -24.2),
            (6.8, 12.3, -14.6), (7.0, 12.2, -22.4), (12.1, 15.85, -19.6), (12.1, 15.85, -24.2)], 'team', bevel=0.0, mirror=True)
    b.box((12.0, 15.5, -24.2), (12.9, 16.0, -23.3), 'lightr', bevel=0.0, mirror=True)
    # keel nano emitter over NanoPoint
    b.cyl((0, 0.7, 12.0), (0, 0.0, 12.0), 1.8, 10, 'dark', r2=1.3)
    b.cyl((0, 0.05, 12.0), (0, -0.1, 12.0), 1.0, 10, 'lightc')

    # ------------------------------------------------------------------ Cab: nano sponson on the left cheek
    c = k.piece('Cab')
    c.hull([(-5.4, y, z) for y in (2.9, 7.4) for z in (22.0, -6.6)] +
           [(-16.2, 2.9, 15.0), (-16.2, 2.9, -5.0), (-14.8, 7.0, 16.0), (-14.8, 7.0, -6.2), (-10.0, 2.9, 24.4), (-9.6, 7.0, 24.0)],
           'paint2', bevel=0.16)
    c.hull([(x, y, z) for x, z in ((-8.8, 22.4), (-14.2, 15.8), (-14.2, -5.4), (-8.8, -5.4)) for y in (7.05, 7.5)],
           'hazard', bevel=0.05)
    # nano projector at the sponson's nose
    c.cyl((-11.2, 4.8, 22.0), (-11.2, 4.8, 25.2), 1.6, 10, 'dark', r2=1.2, bevel=0.03)
    c.cyl((-11.2, 4.8, 25.15), (-11.2, 4.8, 25.9), 1.0, 10, 'lightc')
    c.cyl((-16.0, 4.9, -4.2), (-16.0, 4.9, 14.0), 1.05, 8, 'dark', rot=math.pi / 8)

    # ------------------------------------------------------------------ wing (LWing origin at x -5.99; RWing = mirror)
    w = k.piece('LWing'); W = w.at
    out = [(0.0, 12.5), (15.2, 6.0), (15.2, -9.0), (0.0, -10.0)]
    w.hull([W(x, y, z) for x, z in out for y in (-0.32, 0.32)], 'paint', bevel=0.05)
    w.hull([W(x, y, z) for x, z in ((6.6, 9.8), (14.8, 6.4), (14.8, -8.6), (6.6, -9.4)) for y in (0.36, 0.5)],
           'team', bevel=0.0)
    w.cyl(W(13.6, -0.8, 6.2), W(13.6, -0.8, -8.0), 1.0, 8, 'dark', r2=0.75, rot=math.pi / 8)   # tip float
    k.clone('RWing', 'LWing', mirror_x=True)
