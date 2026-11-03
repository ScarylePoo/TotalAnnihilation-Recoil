"""Archer (ARM_T2_SEA_Archer) - Arm T2 anti-air ship. A long light cruiser hull whose whole fore half is a raised
dark launcher platform carrying two big boxy SAM launchers in line (the read from above: two light boxes with black
tube faces on a dark strip, team edges), and a squat flak tower aft: a round light turret with a team roof and a
twin-barrel mantlet (tertiary gun, recoil 6) firing forward over the launchers.
Pieces (TA layout): GROUNDPLANE (empty root), base, Base_Gun (tower pedestal), TurretGun1 (turn y), TurretGun2
(turn x), GunBarrel1/2 (move z -6), Flare1/2 (empty), Platform, TURRETmis1/2 (launcher posts, static),
MissileBox1/2 (turn y + x), MissileEmitt1/2 (empty), Wake1/2 (empty).
Value groups from above: light hull + launchers + turret, dark platform / pedestal / lower hull, black tube faces and
vents, team on the platform side bands, the launcher roofs and the turret roof.
Floater, no waterline (water surface at model y = 0).
Coordinates are ENGINE/global: X right, Y up, Z forward. mirror=True builds the -X twin sharing UVs."""
import math

UNIT = dict(
    res=1024,
    wreck=dict(seed=7, pose={'TurretGun1': (0, 35, 0), 'MissileBox1': (20, -30, 0), 'MissileBox2': (-15, 50, 0)}),
    preview_pose={'TurretGun2': (-8, 0, 0)},
)

DECK = 7.0
OUT = [(0.0, 42.0), (4.2, 35.0), (10.6, 22.0), (15.2, 8.0), (16.4, -2.0), (16.4, -24.0), (14.4, -36.0), (9.0, -41.6)]


def ring(pts, y, sx=1.0, sz=1.0, dz=0.0, sheer=0.0):
    out = []
    for x, z in pts:
        yy = y + sheer * max(0.0, (z - 14.0) / 28.0) ** 1.5
        for s in ((-1, 1) if x > 0 else (1,)):
            out.append((x * sx * s, yy, z * sz + dz))
    return out


def build(k):
    b = k.piece('base')
    # ------------------------------------------------------------------ hull (crosses x = 0)
    b.hull(ring(OUT, -1.6, 0.6, 0.9, -1.0) + ring(OUT, 2.4, 0.95, 0.98), 'paint2', bevel=0.2)
    b.hull(ring(OUT, 2.4, 0.95, 0.98) + ring(OUT, DECK, sheer=1.6), 'paint', bevel=0.2)
    # dark walkway lines along the main-deck rims
    b.hull([(x, DECK + d, z) for d in (-0.05, 0.2) for x, z in ((14.2, -30.0), (15.4, -20.0), (15.4, -4.0), (14.2, 6.0))],
           'dark', bevel=0.03, mirror=True)
    # quarterdeck: bollards, stern light, depth-charge rails
    b.cyl((6.0, DECK, -37.0), (6.0, DECK + 1.2, -37.0), 0.7, 8, 'dark', mirror=True)
    b.box((-2.0, 5.6, -41.4), (2.0, 6.4, -41.1), 'lightr', bevel=0.0)
    # bow: anchor deck plate (dark) and a red bow light
    b.hull([(x * s, y, z) for s in (-1, 1) for x, y, z in
            [(3.6, DECK + 0.1, 31.0), (1.2, DECK + 0.5, 37.6), (3.6, DECK + 0.45, 31.0), (1.2, DECK + 0.85, 37.6)]],
           'dark', bevel=0.04)
    b.cyl((0, DECK + 0.8, 38.6), (0, DECK + 1.4, 38.6), 0.35, 6, 'lightr')

    # ------------------------------------------------------------------ launcher platform (raised dark deck, fore)
    pl = [(0.0, 33.4), (5.0, 31.0), (10.6, 22.0), (11.4, 10.0), (11.4, -20.0), (8.0, -22.4)]
    b_pl = k.piece('Platform')
    b_pl.plan(DECK - 0.3, 9.6, pl + [(-x, z) for x, z in reversed(pl[1:])], 'paint2', bevel=0.15,
              top_inset=1.0)
    # team side bands along the platform top (convex plan: real top at 9.6)
    b_pl.hull([(x, y, z) for y in (9.66, 9.82) for x, z in ((7.0, -18.0), (10.0, -18.0), (10.0, 18.0), (7.0, 21.0))],
              'team', bevel=0.03, mirror=True)
    # light centre catwalk between the launchers + vents
    b_pl.box((-2.2, 9.6, -16.0), (2.2, 9.85, 0.0), 'paint', bevel=0.05)
    for z in (-12.0, -8.0, -4.0):
        b_pl.box((-1.6, 9.8, z - 0.6), (1.6, 10.0, z + 0.6), 'black', bevel=0.0)
    b_pl.box((10.9, 8.2, 2.0), (11.25, 8.8, 6.0), 'lightc', bevel=0.0, mirror=True)
    # launcher posts (static; the boxes turn on them)
    for n in ('TURRETmis1', 'TURRETmis2'):
        t = k.piece(n); A = t.at
        t.cyl(A(0, -3.4, 0), A(0, 0.4, 0), 3.0, 12, 'dark', r2=2.4, bevel=0.06)
        t.cyl(A(0, -3.4, 0), A(0, -2.8, 0), 4.2, 12, 'paint', bevel=0.05)

    # ------------------------------------------------------------------ SAM launchers (identical boxes)
    m = k.piece('MissileBox1'); M = m.at
    m.hull([M(x * s, y, z) for s in (-1, 1) for x, y, z in
            [(6.2, -1.6, 6.0), (6.2, -1.6, -6.6), (6.2, 3.4, 6.0), (6.2, 3.4, -5.2), (5.2, 4.4, 4.8), (5.2, 4.4, -4.6)]],
           'paint', bevel=0.18)
    # two black 2x2 tube faces on the front
    for x in (-3.0, 3.0):
        m.box(M(x - 2.4, -1.0, 5.95), M(x + 2.4, 3.0, 6.25), 'black', bevel=0.0)
        for xx in (x - 1.2, x + 1.2):
            for yy in (0.0, 2.0):
                m.cyl(M(xx, yy, 6.2), M(xx, yy, 6.4), 0.62, 8, 'steel')
    # team roof plate and a dark cheek block (side armour that holds the trunnion)
    m.hull([M(x * s, y, z) for s in (-1, 1) for x, y, z in [(4.4, 4.45, 3.8), (4.4, 4.45, -3.8), (4.4, 4.62, 3.8), (4.4, 4.62, -3.8)]],
           'team', bevel=0.03)
    m.box(M(-6.6, -1.2, -2.6), M(6.6, 1.6, 1.6), 'dark', bevel=0.12)
    m.box(M(-3.2, -1.6, -6.9), M(3.2, 2.4, -6.4), 'dark', bevel=0.06)
    k.clone('MissileBox2', 'MissileBox1')

    # ------------------------------------------------------------------ flak tower pedestal (aft)
    g = k.piece('Base_Gun')
    g.hull([(x * s, y, z) for s in (-1, 1) for x, y, z in
            [(10.4, DECK - 0.2, -14.0), (10.4, DECK - 0.2, -34.0), (6.0, DECK - 0.2, -37.0), (6.0, DECK - 0.2, -11.0),
             (8.0, 16.2, -17.0), (8.0, 16.2, -31.0), (4.6, 16.2, -32.6), (4.6, 16.2, -15.4)]], 'paint2', bevel=0.2)
    g.box((10.1, 11.0, -27.0), (10.35, 11.6, -21.0), 'lightc', bevel=0.0, mirror=True)
    # radar mast on the pedestal's rear shoulder
    g.cyl((0, 16.0, -32.0), (0, 23.0, -32.4), 0.5, 8, 'dark', r2=0.3)
    g.box((-3.6, 21.0, -32.7), (3.6, 21.6, -31.9), 'dark', bevel=0.05)
    g.cyl((0, 23.0, -32.4), (0, 23.4, -32.4), 0.32, 6, 'lightr')

    # ------------------------------------------------------------------ turret (round, team roof)
    t = k.piece('TurretGun1'); T = t.at
    t.cyl(T(0, 0, 0), T(0, 4.6, 0), 8.6, 16, 'paint', r2=7.4, bevel=0.2)
    t.cyl(T(0, 4.6, 0), T(0, 4.85, 0), 6.0, 16, 'team', bevel=0.03)
    t.box(T(-5.4, 0.6, -9.2), T(5.4, 3.6, -7.4), 'dark', bevel=0.1)   # rear ammo hopper
    t.box(T(-3.6, 4.6, -6.4), T(3.6, 5.2, -5.0), 'black', bevel=0.0)
    # mantlet (turn x): dark gun housing with light cheeks
    s2 = k.piece('TurretGun2'); S = s2.at
    s2.hull([S(x * s, y, z) for s in (-1, 1) for x, y, z in
             [(4.2, -2.4, -2.6), (4.2, 2.4, -2.6), (4.0, -2.0, 11.4), (4.0, 1.8, 11.4), (3.4, 2.8, 3.0)]], 'dark', bevel=0.18)
    for s in (-1, 1):       # origin x = 0.57: no mirror
        s2.hull([S(x * s, y, z) for x in (4.0, 5.0) for y, z in ((-1.8, -2.0), (2.0, -2.0), (1.4, 6.0), (-1.4, 6.0))],
                'paint', bevel=0.1)
    # barrels (recoil 6 back into the housing)
    br = k.piece('GunBarrel1'); B = br.at
    br.cyl(B(0, 0, -6.4), B(0, 0, 10.0), 0.72, 10, 'steel')
    br.cyl(B(0, 0, 7.4), B(0, 0, 10.6), 0.98, 8, 'dark', r2=0.85, rot=math.pi / 8, bevel=0.04)
    br.cyl(B(0, 0, 10.58), B(0, 0, 10.66), 0.45, 8, 'black')
    k.clone('GunBarrel2', 'GunBarrel1')
