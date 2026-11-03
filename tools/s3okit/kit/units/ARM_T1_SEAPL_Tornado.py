"""Tornado (ARM_T1_SEAPL_Tornado) - Arm T1 seaplane fighter. A light needle between two dark float pods reaching
forward like tusks with a gun in each nose. The wings are stowed along the pods and swing out 41 deg on take-off about
a hinge at the pod sterns (COB turn y) into forward-swept blades: from above the only forward-swept plan in the Arm
air force (the Albatross is a broad back-swept delta, the Freedom Fighter a back-swept arrow).
Pieces (TA layout): GP (empty), Base, LWing (+x; RWing = mirrored clone), Emit2, Emit3, Wake1/Wake2, Weapon1/Weapon2 (empty).
Value groups from above: light needle and wings, dark paint2 tusks, black nozzles, steel guns, team on the wing outer
halves and the fin tops.
Coordinates are ENGINE/global: X right, Y up, Z forward. mirror=True builds the -X twin sharing UVs."""
import math

UNIT = dict(
    res=1024,
    wreck=dict(seed=37, remove=['LWing'], pose={'RWing': (0, -18, 0)}),
    preview_pose={'LWing': (0, 41.35, 0), 'RWing': (0, -41.35, 0)},     # flight (COB activatescr)
)


def build(k):
    b = k.piece('Base')
    # ------------------------------------------------------------------ needle fuselage (crosses x = 0)
    b.hull([(x * sx, y, z) for sx in (-1, 1) for x, y, z in
            [(0.3, 3.3, 19.6), (0.3, 3.9, 19.2), (1.4, 1.4, 12.0), (1.6, 5.0, 11.0),
             (2.6, 0.5, -1.0), (2.2, 6.0, -1.0), (2.8, 0.5, -15.0), (2.1, 6.4, -13.0), (1.8, 1.6, -21.0), (1.3, 5.4, -21.0)]],
           'paint', bevel=0.14)
    # canopy
    b.hull([(x * sx, y, z) for sx in (-1, 1) for x, y, z in
            [(0.9, 4.8, 11.4), (1.5, 5.7, 5.4), (1.4, 6.0, 0.6), (0.5, 6.9, 3.8), (0.5, 6.9, 1.6)]], 'glass', bevel=0.06)
    # ------------------------------------------------------------------ float tusks (V bottoms), guns in the noses
    b.hull([(4.0, 2.4, 18.8), (7.6, 2.4, 18.8), (5.8, 0.8, 18.0), (4.0, 3.2, 18.2), (7.6, 3.2, 18.2),
            (3.2, 5.0, -4.0), (9.8, 5.0, -4.0), (3.2, 1.2, -4.0), (9.8, 1.8, -4.0), (6.4, 0.0, -4.0),
            (3.0, 5.0, -15.5), (8.6, 5.0, -15.5), (3.0, 1.4, -15.5), (8.6, 2.0, -15.5), (5.8, 0.2, -15.5)],
           'paint2', bevel=0.14, mirror=True)
    b.cyl((4.4, 2.6, 12.0), (4.4, 2.6, 19.8), 0.7, 8, 'steel', rot=math.pi / 8, mirror=True)
    b.cyl((4.4, 2.6, 19.7), (4.4, 2.6, 20.1), 0.42, 8, 'black', mirror=True)
    b.hull([(4.1, 5.06, -5.0), (8.6, 5.06, -5.0), (4.0, 5.06, -13.8), (8.0, 5.06, -13.8),
            (4.1, 5.26, -5.0), (8.6, 5.26, -5.0), (4.0, 5.26, -13.8), (8.0, 5.26, -13.8)], 'team', bevel=0.0, mirror=True)
    # engines at the tusk sterns (wake emit points at z -15.5)
    b.cyl((5.8, 3.4, -15.4), (5.8, 3.4, -17.4), 1.7, 10, 'dark', r2=1.4, bevel=0.03, mirror=True)
    b.cyl((5.8, 3.4, -17.35), (5.8, 3.4, -17.5), 1.0, 10, 'lightc', mirror=True)
    # ------------------------------------------------------------------ twin canted fins
    b.hull([(1.2, 5.4, -10.0), (1.2, 5.0, -20.8), (1.9, 5.0, -10.0), (1.9, 4.6, -20.8),
            (6.8, 9.6, -17.0), (6.8, 9.6, -21.6), (7.3, 9.3, -17.0), (7.3, 9.3, -21.6)], 'paint', bevel=0.06, mirror=True)
    # team fin tips: laid on the fin's upper surface (inner edge x 1.2 -> 6.8, y 5.4 -> 9.6; normal (-0.6, 0.8))
    b.hull([(x - 0.6 * d, y + 0.8 * d, z) for d in (0.05, 0.2) for x, y, z in
            ((4.56, 7.92, -14.3), (4.56, 7.92, -21.2), (6.7, 9.52, -17.0), (6.7, 9.52, -21.5))], 'team', bevel=0.0, mirror=True)

    # ------------------------------------------------------------------ forward-swept wing, hinge at the tusk stern
    w = k.piece('LWing'); W = w.at
    out = [(-5.0, 0.6), (3.2, 0.0), (10.2, 18.0), (6.0, 19.6), (-3.0, 8.0)]
    w.hull([W(x, y, z) for x, z in out for y in (-0.3, 0.3)], 'paint', bevel=0.05)
    w.hull([W(x, y, z) for x, z in ((5.8, 7.6), (9.8, 17.8), (6.2, 19.2), (2.3, 11.4)) for y in (0.34, 0.5)], 'team', bevel=0.0)
    w.cyl(W(8.0, 0, 19.0), W(8.3, 0, 19.9), 0.42, 8, 'lightc')
    k.clone('RWing', 'LWing', mirror_x=True)
