"""Copperhead (CORE_T2_VEH_Copperhead) - Core mobile flak. Two tall triangular track units (the rear idler rides high,
wheels2 at y 14) either side of a low hull; a jointed three-segment pylon (a1, a2, neck: static, explode only) lifts a
rounded flak head ~32 elmos up; the head (turret, turn y) carries a cross-beam (guns, turn x) with a heavy gun pod at
each end and two very long barrels (barrel1/2 at x +-12.5; the COB snaps each back 30 elmo on firing, so most of the
barrel is housed in its pod and only the slim front tube is exposed when it slides).
Piece layout is the third-party S3O's (the COB drives it): tracks1..4 frame-cycled (tread..tread4), wheels1..7 hub
discs (spin x), aim/flare1/flare2 empty emit points.
Value groups from above: the high flak head with two light steel barrels and a team crown is the read (a wide
"T" over the hull); dark warm track units with paint2 side armour, dark pylon, black treads, ochre pylon band.
Coordinates are ENGINE/global: X right, Y up, Z forward."""
import math

UNIT = dict(
    wreck=dict(seed=53, drop=['barrel1'], remove=['tracks2', 'tracks3', 'tracks4'], pose={'turret': (0, 40, 0), 'guns': (25, 0, 0)}),
    preview_pose={'turret': (0, -18, 0), 'guns': (-15, 0, 0), 'tracks2': 'hide', 'tracks3': 'hide', 'tracks4': 'hide'},
)
XI, XO = 11.6, 19.0


def tracks(k, name, mat):
    t = k.piece(name)
    # triangular run: low front wheel, low rear wheel, high rear idler
    prof = [(-15.4, 1.0), (16.8, 0.0), (18.6, 3.6), (14.8, 8.4), (-6.2, 18.2), (-11.0, 18.4), (-16.6, 9.0)]
    t.prism(XI, XO, prof, mat, bevel=0.16, mirror=True)


def build(k):
    for i, mat in enumerate(('tread', 'tread2', 'tread3', 'tread4'), 1):
        tracks(k, f'tracks{i}', mat)
    for i, r in ((1, 3.4), (4, 2.6)):
        w = k.piece(f'wheels{i}'); W = w.at
        w.cyl(W(XO - 0.05, 0, 0), W(XO + 0.4, 0, 0), r, 12, 'dark', bevel=0.05, mirror=True)
        w.cyl(W(XO + 0.4, 0, 0), W(XO + 0.6, 0, 0), r * 0.42, 8, 'steel', mirror=True)
        w.cyl(W(XO + 0.4, r * 0.66, 0), W(XO + 0.58, r * 0.66, 0), r * 0.16, 6, 'black', mirror=True)
    for i in (2, 3):
        k.clone(f'wheels{i}', 'wheels1')
    for i in (5, 6):
        k.clone(f'wheels{i}', 'wheels4')

    b = k.piece('base')
    # armour plate on the inner side of each track unit (paint2), with a team triangle on top
    b.hull([(x, y, z) for x in (10.0, 11.6) for y, z in
            [(2.4, -14.4), (2.4, 16.4), (7.8, 14.4), (17.2, -6.6), (17.2, -10.6), (8.8, -15.4)]], 'paint2', bevel=0.12, mirror=True)
    # top cover over the high rear part of each track unit (light armour, team plate)
    b.hull([(x, y, z) for x in (11.2, 19.4) for y, z in
            [(18.6, -11.6), (18.6, -5.6), (19.4, -10.8), (19.4, -6.4)]], 'paint', bevel=0.12, mirror=True)
    b.box((12.4, 19.4, -10.4), (18.2, 19.62, -6.8), 'team', bevel=0.04, mirror=True)
    # armour skirt over the upper part of each tread triangle (outer face), so the units are not all tread
    b.hull([(x, y, z) for x in (19.5, 20.2) for z, y in
            [(-14.8, 11.6), (-12.0, 19.0), (-5.6, 18.8), (15.4, 8.6), (13.2, 6.4)]], 'paint', bevel=0.12, mirror=True)
    # front fender over the low front wheel
    b.hull([(x, y, z) for x in (11.2, 19.4) for y, z in
            [(8.6, 10.6), (8.6, 17.8), (10.0, 11.4), (9.2, 17.0), (6.4, 19.4)]], 'paint', bevel=0.12, mirror=True)
    b.hull([(x, y, z) for x in (12.4, 18.2) for y, z in
            [(9.16, 15.6), (7.46, 18.6), (9.3, 15.6), (7.6, 18.6)]], 'hazard', bevel=0.02, mirror=True)
    # low hull between the track units (crosses x = 0)
    b.prism(-10.2, 10.2, [(-15.6, 1.6), (16.6, 1.6), (18.6, 4.6), (17.4, 8.6), (-15.0, 9.6), (-16.4, 5.0)], 'paint', bevel=0.18)
    b.hull([(x * sx, y, z) for sx in (-1, 1) for x, y, z in
            [(9.6, 9.4, -14.2), (9.6, 8.6, 15.6), (7.4, 11.4, -12.4), (7.4, 11.4, 4.0), (6.0, 10.2, 13.6)]], 'paint2', bevel=0.16)
    b.cyl((0, 11.0, -2.05), (0, 11.8, -2.05), 5.4, 16, 'dark', bevel=0.06)       # pylon base ring
    b.box((-5.0, 6.4, 17.0), (5.0, 7.8, 17.9), 'dark', bevel=0.05)
    b.box((-4.6, 6.6, 17.88), (4.6, 7.6, 17.98), 'lightw', bevel=0.0)
    b.box((-7.0, 4.0, -16.0), (7.0, 8.4, -15.4), 'dark', bevel=0.05)
    b.box((5.2, 6.4, -16.1), (6.4, 7.2, -15.95), 'lightr', bevel=0.0, mirror=True)

    # ---------------------------------------------------------------- pylon segments (static)
    a1 = k.piece('a1')
    a1.hull([(x * sx, y, z) for sx in (-1, 1) for x, y, z in
             [(3.8, 11.4, -4.2), (3.8, 11.4, 1.0), (3.2, 20.4, -8.8), (3.2, 20.4, -4.0)]], 'dark', bevel=0.14)
    a1.hull([(x * sx, y, z) for sx in (-1, 1) for x, y, z in
             [(4.0, 13.4, -4.4), (4.0, 14.4, -5.4), (4.0, 13.4, 0.4), (4.0, 14.4, -0.4)]], 'hazard', bevel=0.04)
    a2 = k.piece('a2')
    a2.cyl((-4.6, 18.2, -6.4), (4.6, 18.2, -6.4), 2.6, 14, 'paint2', bevel=0.08)
    a2.hull([(x * sx, y, z) for sx in (-1, 1) for x, y, z in
             [(3.6, 18.2, -9.0), (3.6, 18.2, -4.0), (3.0, 27.6, -4.4), (3.0, 27.6, 0.0)]], 'dark', bevel=0.14)
    a2.cyl((-6.0, 18.2, -6.4), (-4.6, 18.2, -6.4), 1.6, 12, 'steel')
    a2.cyl((4.6, 18.2, -6.4), (6.0, 18.2, -6.4), 1.6, 12, 'steel')
    nk = k.piece('neck')
    nk.cyl((-3.8, 26.6, -2.6), (3.8, 26.6, -2.6), 2.4, 14, 'paint2', bevel=0.08)
    nk.hull([(x * sx, y, z) for sx in (-1, 1) for x, y, z in
             [(3.2, 26.6, -4.6), (3.2, 26.6, 0.4), (2.8, 31.0, -4.4), (2.8, 31.0, -0.4)]], 'dark', bevel=0.12)

    # ---------------------------------------------------------------- turret: flak head (origin 0, 31.61, -2.46)
    t = k.piece('turret'); A = t.at
    t.cyl(A(0, -0.6, 0), A(0, 0.2, 0), 4.6, 16, 'dark', bevel=0.06)
    t.hull([A(x * sx, y, z) for sx in (-1, 1) for x, y, z in
            [(5.8, 0.0, -11.0), (7.4, 0.0, -2.0), (6.4, 0.0, 6.6), (3.4, 0.0, 10.4),
             (5.2, 7.4, -10.0), (6.4, 7.4, -2.0), (5.4, 7.4, 5.4), (2.8, 7.4, 8.6),
             (3.6, 9.4, -7.6), (4.0, 9.4, -1.0), (2.4, 9.4, 4.0)]], 'paint', bevel=0.22)
    # team crown
    t.hull([A(x * sx, y, z) for sx in (-1, 1) for x, y, z in
            [(3.4, 9.38, -7.0), (3.8, 9.38, -1.0), (2.2, 9.38, 3.4), (3.35, 9.54, -6.95), (3.75, 9.54, -1.0), (2.15, 9.54, 3.35)]],
           'team', bevel=0.03)
    # radar eye on the nose
    t.cyl(A(0, 4.4, 9.4), A(0, 4.4, 10.8), 2.0, 12, 'dark', bevel=0.06)
    t.cyl(A(0, 4.4, 10.8), A(0, 4.4, 11.0), 1.3, 12, 'lightr')
    t.box(A(-4.0, 1.0, -11.6), A(4.0, 6.4, -10.6), 'paint2', bevel=0.08)

    # ---------------------------------------------------------------- guns: cross beam + two gun pods (turn x)
    g = k.piece('guns'); G = g.at
    g.cyl(G(-10.0, 0, 0), G(10.0, 0, 0), 1.7, 12, 'steel')
    px = 12.5
    g.hull([G(x, y, z) for x in (px - 3.2, px + 3.2) for y, z in
            [(-4.2, -11.4), (3.6, -11.4), (-4.6, 2.0), (4.0, 2.0), (-2.6, 9.6), (2.6, 9.6)]], 'steel', bevel=0.18, mirror=True)
    g.box(G(px - 2.4, 3.9, -9.6), G(px + 2.4, 4.16, 1.4), 'team', bevel=0.04, mirror=True)
    g.box(G(px + 3.1, -2.4, -9.0), G(px + 3.5, 2.0, 0.0), 'dark', bevel=0.05, mirror=True)       # ammo feed
    g.cyl(G(px, -0.3, 9.4), G(px, -0.3, 12.2), 2.3, 12, 'dark', bevel=0.06, mirror=True)        # barrel shroud mouth

    # ---------------------------------------------------------------- barrels (long; recoil 30 into the pod)
    br = k.piece('barrel1'); B = br.at
    br.cyl(B(0, 0, 0.4), B(0, 0, 33.2), 1.45, 10, 'steel')
    for z in (12.0, 22.0):
        br.cyl(B(0, 0, z), B(0, 0, z + 1.2), 1.9, 10, 'dark', bevel=0.04)
    br.cyl(B(0, 0, 31.4), B(0, 0, 35.2), 2.0, 8, 'dark', rot=math.pi / 8, bevel=0.06)
    br.cyl(B(0, 0, 35.18), B(0, 0, 35.26), 0.7, 8, 'black')
    k.clone('barrel2', 'barrel1', mirror_x=True)
