"""Leveler (CORE_T1_VEH_Leveler) - Core riot tank. Squat hull on wide tracks, a big crested turret with armoured side
wings and one very fat short riot cannon (exaggerated bore: the unit's tell from above).
Piece layout is the third-party remodel's (the COB drives it): base (empty), body, turret (turn y), sleeve (turn x),
barrel (recoil move z), firepoint (emit), tracks1..4 (frame-cycled with tread..tread4), wheels1..6 (spin x: hub discs
on the outer track faces).
Value groups from above: dark warm armour, darker paint2 wings/skirts, black tracks, team plates on the fender tops and
the turret wing tops, light steel cannon, ochre hazard crest stripe.
Coordinates are ENGINE/global: X right, Y up, Z forward."""
import math

UNIT = dict(
    res=1024,
    wreck=dict(seed=9, drop=['barrel'], remove=['tracks2', 'tracks3', 'tracks4'], pose={'turret': (0, 45, 0)}),
    preview_pose={'turret': (0, -20, 0), 'tracks2': 'hide', 'tracks3': 'hide', 'tracks4': 'hide'},
)

XI, XO = 6.6, 13.5


def tracks(k, name, mat):
    t = k.piece(name)
    belt = [(-15.6, 0.0), (13.4, 0.0), (16.4, 2.6), (15.4, 6.6), (-16.6, 6.6), (-18.0, 3.0)]
    t.prism(XI, XO, belt, mat, bevel=0.15, mirror=True)


def build(k):
    for i, mat in enumerate(('tread', 'tread2', 'tread3', 'tread4'), 1):
        tracks(k, f'tracks{i}', mat)
    for i in (1, 2):
        w = k.piece(f'wheels{i}'); W = w.at
        r = 2.8 if i == 1 else 1.9
        w.cyl(W(XO - 0.05, 0, 0), W(XO + 0.35, 0, 0), r, 12, 'dark', bevel=0.05, mirror=True)
        w.cyl(W(XO + 0.35, 0, 0), W(XO + 0.55, 0, 0), r * 0.42, 8, 'steel', mirror=True)
    k.clone('wheels6', 'wheels1')
    for i in (3, 4, 5):
        k.clone(f'wheels{i}', 'wheels2')

    # ------------------------------------------------------------------ body (origin 0, 9.5, -3.74)
    b = k.piece('body')
    b.prism(-6.7, 6.7, [(-17.4, 3.0), (14.6, 3.0), (17.6, 5.6), (16.6, 8.0), (-16.8, 8.0), (-17.8, 5.4)], 'paint2', bevel=0.15)
    # fenders
    b.hull([(6.0, 8.2, -17.6), (14.6, 8.2, -17.2), (14.6, 8.2, 12.4), (6.0, 8.2, 13.6),
            (6.0, 6.6, 17.6), (13.4, 6.6, 16.6),
            (6.0, 6.5, -17.8), (14.8, 6.5, -17.4), (14.8, 6.5, 12.6), (6.0, 6.5, 13.8), (6.0, 5.8, 17.8), (13.4, 5.8, 16.8)],
           'paint', bevel=0.14, mirror=True)
    b.hull([(14.4, 6.6, -16.6), (15.1, 7.7, -16.0), (15.1, 7.7, 11.6), (14.4, 6.6, 12.4),
            (14.2, 5.1, -15.0), (14.8, 5.9, -14.6), (14.8, 5.9, 10.4), (14.2, 5.1, 11.0)], 'paint2', bevel=0.1, mirror=True)
    # team cross band across the rear of the fenders (behind the turret: never covered by it)
    b.box((6.4, 8.2, -16.6), (14.2, 8.36, -12.4), 'team', bevel=0.04, mirror=True)
    # dozer-like dark wedge plates on the fender noses (riot tank: blunt, heavy front)
    b.hull([(6.6, 5.9, 17.4), (12.8, 5.9, 16.4), (6.6, 8.22, 13.6), (13.6, 8.22, 12.6),
            (6.6, 6.02, 17.35), (12.8, 6.02, 16.35), (6.6, 8.36, 13.55), (13.6, 8.36, 12.55)], 'paint2', bevel=0.03, mirror=True)
    # upper hull to the turret ring at y 11.5
    b.hull([(x * sx, y, z) for sx in (-1, 1) for x, y, z in
            [(6.2, 8.0, -17.6), (6.2, 8.0, 14.0), (5.4, 7.6, 18.6),
             (5.8, 11.5, -16.6), (5.8, 11.5, 3.0), (4.4, 9.6, 14.2)]], 'paint', bevel=0.16)
    b.box((4.6, 6.8, 17.6), (6.0, 7.8, 18.6), 'dark', bevel=0.06, mirror=True)
    b.box((4.75, 6.95, 18.58), (5.85, 7.65, 18.68), 'lightw', bevel=0.0, mirror=True)
    b.box((-4.4, 11.1, -16.4), (4.4, 12.0, -13.0), 'dark', bevel=0.1)
    for z in (-15.9, -15.0, -14.1):
        b.box((-4.0, 12.0, z), (4.0, 12.15, z + 0.45), 'black', bevel=0.0)
    b.box((-5.0, 8.4, -17.95), (5.0, 11.0, -17.45), 'paint2', bevel=0.06)
    b.box((3.6, 9.4, -18.05), (4.6, 10.0, -17.9), 'lightr', bevel=0.0, mirror=True)

    # ---------------------------------------------------------------- turret (origin 0, 11.5, -6.01)
    t = k.piece('turret'); A = t.at
    t.cyl(A(0, -0.1, 0), A(0, 0.5, 0), 5.4, 18, 'dark', bevel=0.06)
    # central block (crest rises to the rear)
    t.hull([A(x * sx, y, z) for sx in (-1, 1) for x, y, z in
            [(4.6, 0.45, -10.8), (5.0, 0.45, -2.0), (3.6, 0.45, 4.6),
             (3.4, 5.0, -10.2), (3.6, 5.4, -3.0), (2.6, 4.4, 2.6),
             (1.6, 8.3, -9.6), (1.6, 7.4, -4.4)]], 'paint', bevel=0.15)
    # dark crest spine on top
    t.hull([A(x * sx, y, z) for sx in (-1, 1) for x, y, z in
            [(1.1, 8.28, -9.3), (1.1, 7.42, -4.6), (1.1, 8.42, -9.3), (1.1, 7.56, -4.6)]], 'paint2', bevel=0.02)
    # armoured side wings (ammo boxes), team tops
    t.hull([A(x, y, z) for x, y, z in
            [(4.4, 1.0, -7.2), (14.0, 1.0, -6.0), (4.4, 1.0, 0.8), (14.0, 1.0, -0.4),
             (4.4, 4.6, -6.6), (12.8, 3.6, -5.6), (4.4, 4.6, 0.2), (12.8, 3.6, -0.8)]], 'paint2', bevel=0.12, mirror=True)
    t.hull([A(x, y, z) for x, y, z in
            [(5.2, 4.42, -6.0), (12.2, 3.66, -5.2), (5.2, 4.42, -0.4), (12.2, 3.66, -1.1),
             (5.2, 4.58, -6.0), (12.2, 3.82, -5.2), (5.2, 4.58, -0.4), (12.2, 3.82, -1.1)]], 'team', bevel=0.03, mirror=True)
    t.box(A(12.8, 1.6, -0.55), A(13.6, 2.8, -0.35), 'lightw', bevel=0.0, mirror=True)
    # front cheeks around the sleeve
    t.hull([A(x, y, z) for x, y, z in
            [(2.6, 0.6, 0.0), (4.2, 0.6, 0.0), (2.6, 0.6, 4.4), (3.6, 0.6, 4.0),
             (2.6, 5.2, -0.4), (3.8, 4.4, -0.4), (2.6, 4.6, 3.2), (3.4, 4.0, 3.0)]], 'paint2', bevel=0.1, mirror=True)
    # periscope block on the crest
    t.box(A(-1.0, 7.2, -5.0), A(1.0, 8.0, -3.8), 'dark', bevel=0.06)
    t.box(A(-0.8, 7.35, -3.82), A(0.8, 7.8, -3.72), 'lightc', bevel=0.0)

    # ---------------------------------------------------------------- sleeve (origin 0, 14.28, -6.01; elevates)
    sv = k.piece('sleeve'); S = sv.at
    sv.cyl(S(-2.3, 0, 0), S(2.3, 0, 0), 2.3, 12, 'dark', bevel=0.06)
    sv.hull([S(x * sx, y, z) for sx in (-1, 1) for x, y, z in
             [(2.4, -2.6, 0.0), (2.4, 2.6, 0.0), (2.2, -2.3, 9.2), (2.2, 2.3, 9.2)]], 'paint2', bevel=0.14)
    sv.box(S(-1.6, 2.6, 1.4), S(1.6, 2.76, 7.6), 'team', bevel=0.03)

    # ---------------------------------------------------------------- barrel (fat riot gun, recoils)
    br = k.piece('barrel'); B = br.at
    br.cyl(B(0, 0, -0.6), B(0, 0, 10.6), 1.7, 12, 'steel', rot=math.pi / 12)
    for z in (2.0, 5.0):
        br.cyl(B(0, 0, z), B(0, 0, z + 0.9), 1.95, 12, 'dark', rot=math.pi / 12, bevel=0.05)
    br.cyl(B(0, 0, 10.4), B(0, 0, 12.4), 2.5, 8, 'steel', r2=2.2, rot=math.pi / 8, bevel=0.08)
    br.cyl(B(0, 0, 9.6), B(0, 0, 10.4), 2.0, 12, 'hazard', rot=math.pi / 12)     # muzzle warning ring
    br.cyl(B(0, 0, 12.38), B(0, 0, 12.46), 1.3, 12, 'black')
