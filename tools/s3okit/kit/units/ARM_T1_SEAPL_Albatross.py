"""Albatross (ARM_T1_SEAPL_Albatross) - Arm T1 torpedo seaplane. A needle fuselage between two big forward-reaching
float pods (the planing hulls the wakes come from), with a dark trench either side of the nose carrying two long light
torpedoes. Twin canted fins. The wings stow inside the pods on the water and swing out 24 deg from a hinge at the pod
noses in flight (COB turn y), leaving a broad delta: from above a wide arrowhead with a split nose and steel torpedoes.
Pieces (TA layout): base, LWing (at +x; RWing = mirrored clone), bombdrop, RearGun, flare1/flare2, wake1/wake2 (empty).
Value groups from above: light Arm pods and fuselage, dark trench and engines, paint2 fins, steel torpedoes, team on the
wing outer halves and pod noses.
Coordinates are ENGINE/global: X right, Y up, Z forward. mirror=True builds the -X twin sharing UVs."""
import math

UNIT = dict(
    res=1024,
    wreck=dict(seed=33, remove=['RWing'], pose={'LWing': (0, -14, 0)}),
    preview_pose={'LWing': (0, -24.06, 0), 'RWing': (0, 24.06, 0)},     # flight (COB activatescr)
)


def build(k):
    b = k.piece('base')
    # ------------------------------------------------------------------ fuselage (crosses x = 0)
    b.hull([(x * sx, y, z) for sx in (-1, 1) for x, y, z in
            [(0.4, 2.6, 21.6), (0.4, 3.4, 21.2), (1.5, 1.6, 15.0), (1.7, 5.0, 14.0),
             (2.8, 0.6, 3.0), (2.6, 6.3, 3.0), (2.9, 0.8, -14.0), (2.6, 6.4, -12.0),
             (1.8, 1.8, -23.0), (1.6, 5.8, -23.0)]], 'paint', bevel=0.14)
    # canopy, spine vents
    b.hull([(x * sx, y, z) for sx in (-1, 1) for x, y, z in
            [(1.2, 4.9, 13.4), (1.9, 6.1, 7.6), (1.8, 6.1, 3.4), (0.7, 7.0, 6.0), (0.7, 7.0, 4.0)]], 'glass', bevel=0.06)
    for z in (-1.0, -3.6, -6.2):
        b.box((-2.1, 6.2, z - 0.8), (2.1, 6.75, z + 0.8), 'black', bevel=0.0)
    # dark trench floor between fuselage and pods (above the stowed wings)
    b.hull([(x * sx, y, z) for sx in (-1, 1) for x, y, z in
            [(1.2, 2.7, 19.0), (1.2, 3.2, 19.0), (7.0, 2.7, 19.0), (7.0, 3.2, 19.0), (4.0, 2.7, -7.0), (4.0, 3.2, -7.0)]],
           'dark', bevel=0.0)
    # ------------------------------------------------------------------ float pods (planing hulls, V bottom, flat tops)
    top = [(6.9, 21.0), (11.0, 21.0), (9.8, -16.6), (3.8, -16.6), (3.8, -6.6)]
    b.hull([(x, 4.7, z) for x, z in top] +
           [(6.9, 2.6, 21.8), (11.2, 2.6, 21.8), (9.6, 0.2, 18.6), (8.0, 0.0, -17.4), (10.0, 2.0, -17.4), (3.7, 1.6, -17.4), (3.8, 1.4, -6.0)],
           'paint', bevel=0.16, mirror=True)
    # team pod noses
    b.hull([(x, y, z) for x, z in ((7.5, 20.4), (10.4, 20.4), (10.2, 9.0), (5.7, 9.0)) for y in (4.75, 4.95)],
           'team', bevel=0.0, mirror=True)
    # black intake on the pods
    b.hull([(x, y, z) for x, z in ((4.8, -4.0), (9.7, -4.0), (9.6, -12.0), (4.4, -12.0)) for y in (4.75, 5.05)],
           'black', bevel=0.0, mirror=True)
    # engines at the pod sterns (wake emit points at z -21.6)
    b.hull([(x, y, z) for x, y0, y1, z in ((4.4, 1.6, 4.4, -16.0), (9.2, 1.8, 4.4, -16.0), (5.2, 2.0, 4.0, -21.0), (8.4, 2.0, 4.0, -21.0))
            for y in (y0, y1)], 'paint2', bevel=0.1, mirror=True)
    b.cyl((6.8, 3.0, -20.8), (6.8, 3.0, -22.0), 1.3, 10, 'dark', r2=1.1, mirror=True)
    b.cyl((6.8, 3.0, -21.95), (6.8, 3.0, -22.1), 0.8, 10, 'lightc', mirror=True)
    # ------------------------------------------------------------------ steel torpedoes in the trench (bombdrop under them)
    for x in (4.1,):
        b.cyl((x, 4.1, -4.0), (x, 4.1, 13.0), 1.15, 8, 'steel', rot=math.pi / 8, mirror=True)
        b.cyl((x, 4.1, 13.0), (x, 4.1, 15.8), 1.15, 8, 'steel', r2=0.3, rot=math.pi / 8, mirror=True)
        b.cyl((x, 4.1, 12.4), (x, 4.1, 13.0), 1.2, 8, 'lightr', rot=math.pi / 8, mirror=True)
        b.box((x - 1.5, 3.9, -5.4), (x + 1.5, 4.3, -3.6), 'dark', bevel=0.0, mirror=True)
    # ------------------------------------------------------------------ twin canted fins
    b.hull([(1.8, 5.2, -9.0), (1.8, 5.0, -23.0), (2.6, 4.6, -9.0), (2.6, 4.4, -23.0),
            (7.5, 9.3, -19.6), (7.5, 9.3, -24.4), (8.1, 9.0, -19.6), (8.1, 9.0, -24.4)], 'paint2', bevel=0.06, mirror=True)
    b.box((7.2, 9.1, -24.4), (8.3, 9.6, -23.4), 'lightr', bevel=0.0, mirror=True)

    # ------------------------------------------------------------------ wing, hinge at the pod nose (RWing = mirror)
    w = k.piece('LWing'); W = w.at
    out = [(0.0, 0.0), (-2.5, -38.0), (-6.0, -37.5), (-14.0, -31.0), (-13.0, -19.0), (-6.0, -1.0)]
    w.hull([W(x, y, z) for x, z in out for y in (0.15, 0.85)], 'paint', bevel=0.05)
    w.hull([W(x, y, z) for x, z in ((-2.0, -18.0), (-2.5, -37.4), (-6.0, -36.9), (-12.0, -31.4), (-11.0, -21.6)) for y in (0.9, 1.05)],
           'team', bevel=0.0)
    w.cyl(W(-2.3, 0.5, -37.6), W(-2.3, 0.5, -39.0), 0.45, 8, 'lightc')
    k.clone('RWing', 'LWing', mirror_x=True)
