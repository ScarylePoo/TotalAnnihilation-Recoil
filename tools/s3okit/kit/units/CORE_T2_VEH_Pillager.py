"""Pillager (CORE_T2_VEH_Pillager) - Core mobile artillery. Low wide hull on two big track pods with a waisted middle
(TA/remodel "dog-bone" plan), a tall drum turret rising from the centre with trunnion cheeks (outer/inner: static
under turret) and a long howitzer: sleeve (turn x) carries the cradle and breech (static), barrel recoils 6.
Piece layout is the third-party S3O's. Its COB never cycles tracks or spins wheels, so tracks1..4 would all be
visible at once: only tracks1 gets geometry (tracks2..4 stay empty); wheels1..8 are static hub discs.
Value groups from above: dark warm armour pods, darker paint2 waist deck, the light-steel howitzer + cradle as one
long light line from breech to muzzle (the artillery read), team colour on the two pod tops and the drum roof,
ochre hazard bands on the breech (backblast warning).
Coordinates are ENGINE/global: X right, Y up, Z forward."""
import math

UNIT = dict(
    wreck=dict(seed=59, drop=['barrel'], pose={'turret': (0, 35, 0), 'sleeve': (10, 0, 0)}),
    preview_pose={'turret': (0, -15, 0), 'sleeve': (-15, 0, 0)},
)
XI, XO = 12.4, 18.6


def build(k):
    t1 = k.piece('tracks1')
    belt = [(-18.6, 0.0), (16.0, 0.0), (19.8, 2.6), (18.8, 5.0), (-19.4, 5.0), (-21.4, 2.4)]
    t1.prism(XI, XO, belt, 'tread', bevel=0.15, mirror=True)
    for i, r in ((1, 1.5), (2, 2.2)):
        w = k.piece(f'wheels{i}'); W = w.at
        w.cyl(W(XO - 0.05, 0, 0), W(XO + 0.35, 0, 0), r, 12, 'dark', bevel=0.05, mirror=True)
        w.cyl(W(XO + 0.35, 0, 0), W(XO + 0.55, 0, 0), r * 0.42, 8, 'steel', mirror=True)
    k.clone('wheels8', 'wheels1')
    for i in (3, 4, 5, 6, 7):
        k.clone(f'wheels{i}', 'wheels2')

    m = k.piece('main')
    # track pods: dark armour boxes, bevelled corners (the dog-bone ends)
    m.hull([(12.0, 9.6, -17.6), (19.4, 9.6, -17.6), (19.4, 9.6, 16.6), (12.0, 9.6, 16.6),
            (12.0, 6.8, 20.8), (19.0, 6.8, 20.0), (12.0, 7.0, -21.6), (19.0, 7.0, -20.8),
            (12.0, 5.0, -19.6), (19.8, 5.0, -19.2), (19.8, 5.0, 18.4), (12.0, 5.0, 18.8)], 'paint', bevel=0.18, mirror=True)
    m.box((13.6, 9.6, 4.0), (18.2, 9.82, 12.8), 'team', bevel=0.05, mirror=True)
    m.box((13.6, 9.6, -14.8), (18.2, 9.9, -8.0), 'dark', bevel=0.06, mirror=True)          # rear pod hatches
    m.box((-8.4, 9.0, -8.6), (8.4, 9.2, -6.6), 'team', bevel=0.04)                         # cross band behind the drum
    m.hull([(19.6, 5.2, -18.8), (20.2, 5.2, -18.4), (20.2, 5.2, 17.6), (19.6, 5.2, 18.0),
            (19.4, 3.0, -17.2), (20.0, 3.0, -16.8), (20.0, 3.0, 15.8), (19.4, 3.0, 16.2)], 'paint2', bevel=0.08, mirror=True)
    # Core saw-teeth on the pod noses
    for x in (13.4, 16.2):
        m.hull([(x, 6.8, 20.6), (x + 2.2, 6.8, 20.4), (x, 5.2, 21.0), (x + 2.2, 5.2, 20.8), (x + 1.1, 5.8, 22.6)], 'dark', bevel=0.04, mirror=True)
    # waist: narrower central hull (crosses x = 0)
    m.prism(-12.4, 12.4, [(-17.0, 2.0), (15.0, 2.0), (17.6, 4.6), (16.6, 7.6), (-16.4, 7.6), (-17.6, 4.6)], 'paint2', bevel=0.16)
    m.hull([(x * sx, y, z) for sx in (-1, 1) for x, y, z in
            [(10.4, 7.4, -13.0), (10.4, 7.4, 10.0), (8.6, 9.0, -11.6), (8.6, 9.0, 8.4), (6.0, 7.4, 15.0), (5.0, 8.6, 13.0)]], 'paint', bevel=0.16)
    m.cyl((0, 8.4, -2.5), (0, 9.2, -2.5), 7.6, 20, 'dark', bevel=0.06)
    m.box((-4.0, 6.0, 16.6), (4.0, 7.2, 17.4), 'dark', bevel=0.05)
    m.box((-3.6, 6.2, 17.38), (3.6, 7.0, 17.48), 'lightw', bevel=0.0)
    m.box((-8.0, 3.6, -17.6), (8.0, 7.0, -17.0), 'dark', bevel=0.05)
    m.box((6.2, 5.6, -17.7), (7.4, 6.4, -17.55), 'lightr', bevel=0.0, mirror=True)
    # ammunition racks on the rear waist deck
    for x in (-6.0, -3.6, 3.6, 6.0):
        m.cyl((x, 9.0, -14.6), (x, 9.0, -10.4), 0.9, 8, 'dark')
        m.cyl((x, 9.0, -10.4), (x, 9.0, -9.6), 0.9, 8, 'hazard', r2=0.3)
    m.cyl((-15.6, 9.6, -18.2), (-15.6, 10.3, -18.2), 0.34, 8, 'dark')
    m.cyl((-15.6, 10.3, -18.2), (-15.6, 16.0, -18.2), 0.09, 6, 'steel', r2=0.045)
    m.cyl((-15.6, 16.0, -18.2), (-15.6, 16.2, -18.2), 0.15, 6, 'lightr')

    # ---------------------------------------------------------------- turret: drum (origin 0, 8.5, -2.5)
    t = k.piece('turret'); A = t.at
    t.cyl(A(0, 0.6, 0), A(0, 4.6, 0), 6.8, 10, 'paint', r2=6.2, rot=math.pi / 10, bevel=0.16)
    t.cyl(A(0, 4.6, 0), A(0, 4.8, 0), 4.6, 10, 'team', rot=math.pi / 10)
    # trunnion uprights either side of the gun
    t.hull([A(x, y, z) for x in (3.2, 6.4) for y, z in [(4.4, -5.0), (4.4, 5.0), (9.6, -3.0), (9.6, 3.0)]], 'paint2', bevel=0.14, mirror=True)
    # trunnion bearings (outer, static) and the inner yoke ring
    o = k.piece('outer'); O = o.at
    o.cyl(O(-7.4, 0, 0), O(-6.2, 0, 0), 3.2, 14, 'dark', bevel=0.08)
    o.cyl(O(6.2, 0, 0), O(7.4, 0, 0), 3.2, 14, 'dark', bevel=0.08)
    o.cyl(O(-7.6, 0, 0), O(-7.4, 0, 0), 1.6, 12, 'steel')
    o.cyl(O(7.4, 0, 0), O(7.6, 0, 0), 1.6, 12, 'steel')
    i = k.piece('inner'); I = i.at
    i.cyl(I(-3.4, 0, -4.0), I(-3.0, 0, -4.0), 3.0, 14, 'steel', mirror=True)

    # ---------------------------------------------------------------- sleeve: cradle (turns x)
    s = k.piece('sleeve'); S = s.at
    s.cyl(S(-3.0, 0, 0), S(3.0, 0, 0), 2.2, 14, 'dark', bevel=0.06)
    s.hull([S(x * sx, y, z) for sx in (-1, 1) for x, y, z in
            [(2.8, -1.2, -9.6), (2.8, 5.2, -9.6), (2.8, -2.2, 6.0), (2.8, 5.6, 6.0), (2.0, 0.6, 14.4), (2.0, 5.0, 14.4)]],
           'steel', bevel=0.16)
    s.hull([S(x * sx, y, z) for sx in (-1, 1) for x, y, z in
            [(1.8, 5.5, -7.0), (1.8, 5.84, 5.0), (1.8, 5.64, -7.0), (1.8, 5.98, 5.0)]], 'team', bevel=0.03)
    s.cyl(S(-2.9, -1.6, -6.0), S(-2.9, 1.4, 12.0), 0.7, 8, 'dark')
    s.cyl(S(2.9, -1.6, -6.0), S(2.9, 1.4, 12.0), 0.7, 8, 'dark')
    # breech block (static child of sleeve), ochre backblast bands
    br = k.piece('breech'); R = br.at
    R0 = R
    br.box(R0(-2.2, -2.2, -0.8), R0(2.2, 1.8, 5.0), 'dark', bevel=0.12)
    br.box(R0(-2.3, -1.4, -0.9), R0(2.3, 1.0, 0.4), 'hazard', bevel=0.04)

    # ---------------------------------------------------------------- barrel (recoil 6)
    b = k.piece('barrel'); B = b.at
    b.cyl(B(0, 0, -2.0), B(0, 0, 15.6), 1.3, 12, 'steel')
    b.cyl(B(0, 0, 6.4), B(0, 0, 8.0), 1.75, 12, 'dark', bevel=0.05)
    b.cyl(B(0, 0, 15.2), B(0, 0, 18.0), 1.9, 8, 'dark', rot=math.pi / 8, bevel=0.07)
    b.cyl(B(0, 0, 17.98), B(0, 0, 18.06), 0.85, 8, 'black')
    for sx in (-1, 1):
        b.box(B(1.6 * sx, -0.55, 15.6), B(2.0 * sx, 0.55, 16.5), 'black', bevel=0.0)
        b.box(B(1.6 * sx, -0.55, 16.8), B(2.0 * sx, 0.55, 17.7), 'black', bevel=0.0)
