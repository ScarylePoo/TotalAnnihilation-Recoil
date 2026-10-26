"""Reaper (CORE_T2_VEH_Reaper) - Core heavy assault tank. Long, low, angular hull with raked armour skirts and a
pointed prow; a rounded, wide turret carrying TWO long cannon side by side, each in its own elevating sleeve (sleeve1/2
at x -+2.81, turn x; barrel1/2 recoil 5). Piece layout is the third-party S3O's (the COB drives it): body, turret
(turn y), sleeves, barrels, firepoint1/2 + smoke1/2 (emit, empty), tracks1..4 (frame-cycled tread..tread4), wheels1..7
(hub discs both sides, spin x: big and small alternate as in the S3O).
Distinct from the Goliath: lower and longer, a pointed prow instead of a slab nose, twin long guns instead of one fat
one, team colour on a long dorsal stripe + the turret's front arc (not a cross saddle).
Value groups from above: dark warm armour, darker paint2 skirts/turret sides, black treads, two light steel barrels
running past the prow, team stripe, ochre hazard prow chevron.
Coordinates are ENGINE/global: X right, Y up, Z forward."""
import math

UNIT = dict(
    wreck=dict(seed=47, drop=['barrel2'], remove=['tracks2', 'tracks3', 'tracks4'], pose={'turret': (0, 28, 0), 'sleeve1': (8, 0, 0)}),
    preview_pose={'turret': (0, -18, 0), 'tracks2': 'hide', 'tracks3': 'hide', 'tracks4': 'hide'},
)
XI, XO = 10.4, 16.8


def tracks(k, name, mat):
    t = k.piece(name)
    belt = [(-17.6, -4.2), (15.4, -4.2), (18.6, -1.2), (17.8, 3.4), (-18.6, 3.4), (-20.6, -0.6)]
    t.prism(XI, XO, belt, mat, bevel=0.16, mirror=True)


def build(k):
    for i, mat in enumerate(('tread', 'tread2', 'tread3', 'tread4'), 1):
        tracks(k, f'tracks{i}', mat)
    for i, r in ((1, 3.2), (2, 1.7)):
        w = k.piece(f'wheels{i}'); W = w.at
        w.cyl(W(XO - 0.05, 0, 0), W(XO + 0.4, 0, 0), r, 12, 'dark', bevel=0.05, mirror=True)
        w.cyl(W(XO + 0.4, 0, 0), W(XO + 0.6, 0, 0), r * 0.42, 8, 'steel', mirror=True)
        w.cyl(W(XO + 0.4, r * 0.66, 0), W(XO + 0.58, r * 0.66, 0), r * 0.16, 6, 'black', mirror=True)
    for i in (3, 5, 7):
        k.clone(f'wheels{i}', 'wheels1')
    for i in (4, 6):
        k.clone(f'wheels{i}', 'wheels2')

    b = k.piece('body')
    # lower hull between the tracks
    b.prism(-10.6, 10.6, [(-20.4, 2.4), (18.4, 2.4), (21.6, 5.2), (20.6, 8.0), (-20.2, 8.0), (-21.4, 5.0)], 'paint2', bevel=0.16)
    # raked armour skirts over the tracks (darker), with Core saw-tooth lower edge
    b.hull([(10.0, 9.6, -19.6), (17.6, 8.6, -19.2), (17.6, 8.6, 16.6), (10.0, 9.6, 17.6),
            (10.0, 7.6, 22.2), (16.8, 6.8, 20.2), (10.0, 7.8, -21.8), (16.8, 7.0, -21.2),
            (10.0, 6.4, -20.2), (18.2, 5.4, -19.6), (18.2, 5.4, 17.2), (10.0, 6.4, 18.4)], 'paint2', bevel=0.16, mirror=True)
    for z in (-15.0, -7.0, 1.0, 9.0):
        b.hull([(18.0, 5.6, z - 3.0), (18.0, 5.6, z + 3.0), (17.8, 3.6, z - 1.2), (17.8, 3.6, z + 1.2),
                (18.6, 5.0, z)], 'dark', bevel=0.05, mirror=True)
    # main armour: a long faceted wedge with a pointed prow (crosses x = 0)
    b.hull([(x * sx, y, z) for sx in (-1, 1) for x, y, z in
            [(10.6, 8.0, -21.2), (10.6, 8.0, 17.0), (0.0, 7.4, 23.4),
             (9.6, 13.0, -20.2), (9.6, 13.0, 6.0), (4.0, 11.4, 18.6), (0.0, 11.0, 21.6), (8.0, 14.2, -14.0), (8.0, 14.2, 2.0)]],
           'paint', bevel=0.2)
    # ochre prow chevron
    b.hull([(x * sx, y, z) for sx in (-1, 1) for x, y, z in
            [(3.6, 11.56, 18.4), (0.0, 11.14, 21.4), (3.6, 11.7, 18.5), (0.0, 11.28, 21.5)]] + [(0.0, 11.9, 17.0)], 'hazard', bevel=0.03)
    # dorsal team stripe from the turret to the prow
    b.hull([(x * sx, y, z) for sx in (-1, 1) for x, y, z in
            [(5.6, 13.1, 4.4), (4.6, 12.0, 13.0), (5.6, 13.24, 4.4), (4.6, 12.14, 13.0)]], 'team', bevel=0.03)
    b.box((-4.0, 14.2, -15.4), (4.0, 14.36, -13.4), 'team', bevel=0.03)
    # team plates on the skirt-top fronts (forward of the teeth: not full-length T1 fender bands)
    b.hull([(x, y, z) for x, y in ((11.0, 9.62), (16.8, 8.78)) for z in (8.0, 15.0)] +
           [(x, y + 0.14, z) for x, y in ((11.0, 9.62), (16.8, 8.78)) for z in (8.0, 15.0)], 'team', bevel=0.03, mirror=True)
    # turret ring
    b.cyl((0, 13.8, -8.92), (0, 14.7, -8.92), 7.6, 20, 'dark', bevel=0.06)
    # rear deck: louvres + twin exhausts angled out
    b.box((-7.4, 13.8, -19.8), (7.4, 14.4, -15.8), 'dark', bevel=0.08)
    for z in (-19.2, -18.2, -17.2):
        b.box((-7.0, 14.4, z), (-1.9, 14.52, z + 0.5), 'black', bevel=0.0)
        b.box((1.9, 14.4, z), (7.0, 14.52, z + 0.5), 'black', bevel=0.0)
    b.cyl((8.6, 11.4, -20.6), (10.4, 14.6, -21.8), 0.9, 10, 'dark', bevel=0.04, mirror=True)
    b.cyl((10.4, 14.6, -21.8), (10.5, 14.8, -21.9), 0.62, 10, 'black', mirror=True)
    # headlights in the prow flanks, tail
    b.box((5.6, 8.4, 19.6), (8.2, 9.6, 20.6), 'dark', bevel=0.06, mirror=True)
    b.box((5.8, 8.6, 20.55), (8.0, 9.4, 20.65), 'lightw', bevel=0.0, mirror=True)
    b.box((-9.0, 8.6, -21.6), (9.0, 12.2, -21.0), 'dark', bevel=0.06)
    b.box((7.2, 10.6, -21.7), (8.6, 11.4, -21.55), 'lightr', bevel=0.0, mirror=True)
    # antenna
    b.cyl((-12.0, 9.4, -18.6), (-12.0, 10.1, -18.6), 0.34, 8, 'dark')
    b.cyl((-12.0, 10.1, -18.6), (-12.0, 17.2, -18.6), 0.09, 6, 'steel', r2=0.045)
    b.cyl((-12.0, 17.2, -18.6), (-12.0, 17.4, -18.6), 0.15, 6, 'lightr')

    # ---------------------------------------------------------------- turret (origin 0, 17.85, -8.92; turns y)
    t = k.piece('turret'); A = t.at
    t.hull([A(x * sx, y, z) for sx in (-1, 1) for x, y, z in
            [(6.8, -3.1, -7.4), (7.6, -3.1, -1.0), (6.6, -3.1, 4.6), (3.6, -3.1, 7.0),
             (5.8, 2.6, -6.6), (6.6, 2.6, -1.0), (5.6, 2.6, 3.4), (3.0, 2.6, 5.4),
             (4.2, 3.6, -5.0), (4.6, 3.6, 1.0)]], 'paint', bevel=0.22)
    # team front arc on the roof
    t.hull([A(x * sx, y, z) for sx in (-1, 1) for x, y, z in
            [(5.7, 2.62, -1.0), (5.6, 2.62, 2.0), (4.8, 2.62, 3.6), (2.6, 2.62, 5.0), (4.4, 3.62, -3.0), (4.6, 3.62, 1.0)]] +
           [A(x * sx, y + 0.15, z) for sx in (-1, 1) for x, y, z in
            [(5.7, 2.62, -1.0), (5.6, 2.62, 2.0), (4.8, 2.62, 3.6), (2.6, 2.62, 5.0), (4.4, 3.62, -3.0), (4.6, 3.62, 1.0)]], 'team', bevel=0.03)
    # darker side blisters where the sleeves pivot
    t.hull([A(x, y, z) for x in (5.4, 7.9) for y, z in [(-2.4, -3.4), (2.0, -3.4), (-2.4, 3.6), (1.6, 3.0)]], 'paint2', bevel=0.12, mirror=True)
    # rear bustle with vent
    t.hull([A(x * sx, y, z) for sx in (-1, 1) for x, y, z in
            [(5.4, -2.4, -6.8), (4.8, 1.8, -6.4), (4.4, -2.0, -9.0), (4.0, 1.2, -8.8)]], 'paint2', bevel=0.12)
    t.box(A(-3.4, -1.0, -9.25), A(3.4, 0.8, -8.85), 'black', bevel=0.0)
    # commander sight (left of the roof centre)
    t.box(A(-2.6, 3.5, -4.0), A(-0.6, 4.6, -1.6), 'dark', bevel=0.06)
    t.box(A(-2.4, 3.7, -1.62), A(-0.8, 4.3, -1.5), 'lightc', bevel=0.0)

    # ---------------------------------------------------------------- sleeves (x -+2.81 from the turret axis; turn x)
    s = k.piece('sleeve1'); S = s.at
    s.cyl(S(-0.1, 0, -1.6), S(-0.1, 0, 10.6), 1.9, 10, 'paint2', r2=1.55, rot=math.pi / 10, bevel=0.08)
    s.cyl(S(-0.1, 0, 7.4), S(-0.1, 0, 8.2), 2.05, 10, 'dark', rot=math.pi / 10, bevel=0.04)
    s.cyl(S(0.6, 0, 0.0), S(-3.6, 0, 0.0), 1.6, 12, 'dark', bevel=0.05)
    k.clone('sleeve2', 'sleeve1', mirror_x=True)

    # ---------------------------------------------------------------- barrels (recoil 5; firepoint at local x 0.22, z 19.64)
    br = k.piece('barrel1'); B = br.at
    x0 = 0.0     # bore near the firepoint (local x 0.22)
    br.cyl(B(x0, 0, -0.6), B(x0, 0, 17.0), 0.95, 12, 'steel')
    br.cyl(B(x0, 0, 8.0), B(x0, 0, 9.4), 1.3, 12, 'dark', bevel=0.05)
    br.cyl(B(x0, 0, 16.8), B(x0, 0, 19.6), 1.35, 8, 'steel', rot=math.pi / 8, bevel=0.06)
    br.cyl(B(x0, 0, 19.58), B(x0, 0, 19.66), 0.6, 8, 'black')
    br.box(B(x0 - 1.7, -0.5, 17.4), B(x0 - 1.3, 0.5, 18.8), 'black', bevel=0.0)
    k.clone('barrel2', 'barrel1', mirror_x=True)
