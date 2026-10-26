"""Crock (CORE_T2_VEH_Crock) - Core amphibious tank (AMPHTANK). A low, wide boat-hulled tank on tracks with a compact
twin-gun turret. Piece layout is the third-party S3O's (the COB drives it): `main` bobs (move y) and rocks in water;
the bow plate `nose` drops 90 deg (turn x) to expose two lift fans (nosefan1/2 spin y, children of the nose); the
stern doors door1/door2 swing open 105 deg (turn y) over the propeller tunnels, mainfan1/2 (props, spin z) turn
inside them, and the rudders rud1/2 slide back 3 and out 2.25. Turret turns y, sleeve x, barrel1/2 recoil;
tracks1..4 frame-cycled (tread..tread4); wheels1..7 hub discs (spin x).
Value groups from above: dark warm boat hull with a pointed paint bow plate carrying a broad team chevron (the
amphibious read: a ship's bow on a tank), darker paint2 side sponsons, black treads, light steel twin barrels on a
small turret with a team roof, ochre hazard on the stern door edges.
Coordinates are ENGINE/global: X right, Y up, Z forward."""
import math

UNIT = dict(
    wreck=dict(seed=67, drop=['barrel2'], remove=['tracks2', 'tracks3', 'tracks4'], pose={'turret': (0, 40, 0), 'nose': (30, 0, 0)}),
    preview_pose={'turret': (0, -15, 0), 'tracks2': 'hide', 'tracks3': 'hide', 'tracks4': 'hide'},
)
XI, XO = 10.6, 15.6


def tracks(k, name, mat):
    t = k.piece(name)
    belt = [(-14.4, 0.0), (10.4, 0.0), (12.2, 2.0), (11.4, 4.4), (-14.8, 4.4), (-16.0, 2.2)]
    t.prism(XI, XO, belt, mat, bevel=0.14, mirror=True)


def build(k):
    for i, mat in enumerate(('tread', 'tread2', 'tread3', 'tread4'), 1):
        tracks(k, f'tracks{i}', mat)
    for i, r in ((1, 1.3), (2, 1.75)):
        w = k.piece(f'wheels{i}'); W = w.at
        w.cyl(W(XO - 0.05, 0, 0), W(XO + 0.3, 0, 0), r, 12, 'dark', bevel=0.04, mirror=True)
        w.cyl(W(XO + 0.3, 0, 0), W(XO + 0.48, 0, 0), r * 0.42, 8, 'steel', mirror=True)
    k.clone('wheels7', 'wheels1')
    for i in (3, 4, 5, 6):
        k.clone(f'wheels{i}', 'wheels2')

    m = k.piece('main')
    # sponsons over the tracks (darker), flat tops, rounded bow ends like floats
    m.hull([(10.2, 6.8, -15.4), (16.2, 6.8, -15.4), (16.2, 6.8, 9.6), (10.2, 6.8, 9.6),
            (10.2, 5.0, 13.2), (15.8, 5.0, 12.6), (10.2, 5.0, -17.4), (15.8, 5.0, -17.0),
            (10.2, 4.4, -15.6), (16.6, 4.4, -15.4), (16.6, 4.4, 10.8), (10.2, 4.4, 11.4)], 'paint2', bevel=0.16, mirror=True)
    m.box((11.2, 6.8, -13.6), (15.2, 7.0, 7.4), 'paint', bevel=0.04, mirror=True)
    # hull tub between the tracks: boat section, flat deck (crosses x = 0)
    m.prism(-10.6, 10.6, [(-16.4, 1.4), (7.0, 1.0), (10.4, 2.4), (10.0, 6.0), (-16.6, 6.6), (-17.4, 3.4)], 'paint', bevel=0.16)
    m.hull([(x * sx, y, z) for sx in (-1, 1) for x, y, z in
            [(10.2, 6.4, -16.0), (10.2, 6.0, 6.4), (8.6, 7.8, -14.6), (8.6, 7.8, 4.6)]], 'paint', bevel=0.16)
    # bow well the nose folds out of (dark recess)
    m.box((-6.4, 1.6, 6.4), (6.4, 2.0, 12.6), 'black', bevel=0.0)
    # propeller tunnel mouths at the stern (inside the doors)
    for x in (-3.0, 3.0):
        m.cyl((x, 4.78, -14.6), (x, 4.78, -16.2), 1.9, 12, 'black', mirror=False)
    m.box((-6.6, 6.6, -17.4), (6.6, 7.6, -16.0), 'dark', bevel=0.06)          # stern lintel above the doors
    # turret ring + deck vents
    m.cyl((0, 7.6, -7.58), (0, 8.1, -7.58), 4.6, 16, 'dark', bevel=0.05)
    for z in (0.0, 1.4, 2.8):
        m.box((-6.4, 7.8, z), (-2.6, 7.95, z + 0.7), 'black', bevel=0.0)
        m.box((2.6, 7.8, z), (6.4, 7.95, z + 0.7), 'black', bevel=0.0)
    m.cyl((-8.6, 7.8, -14.4), (-8.6, 8.4, -14.4), 0.32, 8, 'dark')
    m.cyl((-8.6, 8.4, -14.4), (-8.6, 13.2, -14.4), 0.09, 6, 'steel', r2=0.045)
    m.cyl((-8.6, 13.2, -14.4), (-8.6, 13.4, -14.4), 0.14, 6, 'lightr')
    m.box((12.0, 4.6, 12.4), (14.6, 5.4, 13.1), 'lightw', bevel=0.0, mirror=True)

    # ---------------------------------------------------------------- nose: bow plate (pivot 0, 4.38, 9.02)
    n = k.piece('nose'); N = n.at
    n.hull([N(x * sx, y, z) for sx in (-1, 1) for x, y, z in
            [(6.2, -2.4, -0.2), (6.2, 2.6, -0.2), (5.0, -2.2, 2.6), (3.6, 2.0, 3.4), (0.0, -1.8, 4.6), (0.0, 1.6, 4.8)]],
           'paint', bevel=0.16)
    n.hull([N(x * sx, y, z) for sx in (-1, 1) for x, y, z in
            [(5.6, 2.62, 0.4), (3.2, 2.06, 3.0), (0.0, 1.66, 4.2), (5.6, 2.76, 0.4), (3.2, 2.2, 3.0), (0.0, 1.8, 4.2)]],
           'team', bevel=0.03)
    n.cyl(N(-6.4, 0, 0), N(6.4, 0, 0), 0.8, 10, 'dark')                          # hinge
    # fan shrouds under the plate (seen when it is down)
    for x in (-3.0, 3.0):
        n.cyl(N(x, -2.0, -0.4), N(x, 0.6, -0.4), 1.9, 12, 'dark', bevel=0.04)
    fan = k.piece('nosefan1'); F = fan.at
    fan.cyl(F(0, 0.4, 0), F(0, 0.7, 0), 1.4, 10, 'steel')
    for a in range(3):
        ang = a * 2 * math.pi / 3
        c, s = math.cos(ang), math.sin(ang)
        fan.hull([F(c * r - s * t, y, s * r + c * t) for r in (0.3, 1.3) for t in (-0.3, 0.3) for y in (0.7, 0.9)], 'dark', bevel=0.0)
    k.clone('nosefan2', 'nosefan1', mirror_x=True)

    # ---------------------------------------------------------------- props (spin z) at the tunnel mouths
    p = k.piece('mainfan1'); Pp = p.at
    p.cyl(Pp(0, 0, -10.0), Pp(0, 0, -9.0), 0.5, 8, 'steel')
    for a in range(3):
        ang = a * 2 * math.pi / 3 + 0.3
        c, s = math.cos(ang), math.sin(ang)
        p.hull([Pp(c * r - s * t, s * r + c * t, z) for r in (0.3, 1.4) for t in (-0.32, 0.32) for z in (-9.9, -9.4)], 'steel', bevel=0.0)
    k.clone('mainfan2', 'mainfan1', mirror_x=True)

    # ---------------------------------------------------------------- stern doors (door1 hinge at x -6; turn y)
    d = k.piece('door1'); D = d.at
    d.hull([D(x, y, z) for x in (0.0, 6.0) for y, z in [(0.2, -0.4), (4.8, -0.4), (0.2, 0.6), (4.8, 0.6)]], 'paint2', bevel=0.1)
    d.box(D(4.8, 0.4, -0.5), D(5.9, 4.6, 0.7), 'hazard', bevel=0.03)
    d.cyl(D(0.0, 0.0, 0.0), D(0.0, 5.0, 0.0), 0.45, 8, 'dark')
    k.clone('door2', 'door1', mirror_x=True)

    # ---------------------------------------------------------------- rudders (slide back + out)
    r = k.piece('rud1'); R = r.at
    r.hull([R(x, y, z) for x in (-0.2, 0.2) for y, z in [(0.0, 2.2), (0.0, -2.4), (-3.0, -3.8), (-3.0, 0.6)]], 'dark', bevel=0.04)
    k.clone('rud2', 'rud1', mirror_x=True)

    # ---------------------------------------------------------------- turret (origin 0, 7.5, -7.58; turns y)
    t = k.piece('turret'); A = t.at
    t.hull([A(x * sx, y, z) for sx in (-1, 1) for x, y, z in
            [(4.6, 0.2, -7.6), (4.8, 0.2, 1.0), (3.4, 0.2, 4.8), (3.6, 4.2, -6.6), (3.8, 4.2, 0.4), (2.4, 4.2, 3.2)]],
           'paint', bevel=0.16)
    t.hull([A(x * sx, y, z) for sx in (-1, 1) for x, y, z in
            [(3.4, 4.18, -5.8), (3.5, 4.18, 0.2), (2.2, 4.18, 2.6), (3.35, 4.34, -5.75), (3.45, 4.34, 0.2), (2.15, 4.34, 2.55)]],
           'team', bevel=0.03)
    t.box(A(-1.8, 4.4, -6.4), A(-0.2, 5.4, -4.6), 'dark', bevel=0.05)
    t.box(A(-1.6, 4.6, -4.62), A(-0.4, 5.2, -4.5), 'lightc', bevel=0.0)

    # ---------------------------------------------------------------- sleeve (turns x) + barrels (recoil)
    s = k.piece('sleeve'); S = s.at
    s.hull([S(x * sx, y, z) for sx in (-1, 1) for x, y, z in
            [(3.2, -1.6, 0.0), (3.2, 1.6, 0.0), (3.0, -1.4, 5.4), (3.0, 1.4, 5.4)]], 'paint2', bevel=0.12)
    br = k.piece('barrel1'); B = br.at
    br.cyl(B(0, 0, -0.6), B(0, 0, 8.6), 0.62, 10, 'steel')
    br.cyl(B(0, 0, 3.0), B(0, 0, 3.8), 0.85, 10, 'dark', bevel=0.04)
    br.cyl(B(0, 0, 8.4), B(0, 0, 9.9), 0.85, 8, 'steel', rot=math.pi / 8, bevel=0.04)
    br.cyl(B(0, 0, 9.88), B(0, 0, 9.94), 0.4, 8, 'black')
    k.clone('barrel2', 'barrel1', mirror_x=True)
