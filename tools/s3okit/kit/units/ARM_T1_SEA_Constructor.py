"""Construction Ship (ARM_T1_SEA_Constructor) - Arm naval builder. Light pointed hull carrying a big gable-roofed
hangar amidships-aft: its two roof halves (door1/door2) swing up about the eaves and slide down the walls, then a
lift platform (plate) rises 9.25 out of the hangar and the folded nano crane (turret > arm > nano) stands up.
Forward: a stepped bridge with a tall mast block; aft of the hangar a light stern deckhouse.
From above: light hull ring around a DARK hangar roof with a wide team stripe along the ridge (the builder's tell:
no gun, one long dark box), hazard-striped crane arm when deployed, team roof on the bridge.
Pieces (TA layout): base, plate (move y/z), turret (turn y), arm (turn x, move y), nano (turn x), beam (empty nano
emit point), door1/door2 (turn z, move y: door2 = mirrored clone of door1), wake1/2 (empty).
Floater, waterline 4 (water surface at model y = 4).
Coordinates are ENGINE/global: X right, Y up, Z forward. mirror=True builds the -X twin sharing UVs."""
import math

UNIT = dict(
    res=1024,
    # the crane pieces sit inside the closed hangar at rest; the script raises them, so give them full texture
    always_visible=['plate', 'turret', 'arm', 'nano'],
    wreck=dict(seed=2, drop=['door2'], pose={'door1': (0, 0, -30)}),
    preview_pose={},
)

WL = 4.0
DECK = 7.4
OUT = [(0.0, 39.6), (2.6, 34.5), (9.2, 23.0), (14.1, 9.6), (15.6, 4.0), (15.6, -12.2), (14.1, -28.3), (6.6, -39.6)]
HX0, HX1, HZ0, HZ1 = -7.7, 8.2, -28.2, -0.8          # hangar walls (the doors' hinge lines), as the 3DO


def ring(pts, y, sx=1.0, sz=1.0, dz=0.0, sheer=0.0):
    out = []
    for x, z in pts:
        yy = y + sheer * max(0.0, (z - 12.0) / 27.6) ** 1.5
        for s in ((-1, 1) if x > 0 else (1,)):
            out.append((x * sx * s, yy, z * sz + dz))
    return out


def build(k):
    b = k.piece('base')
    # ------------------------------------------------------------------ hull (crosses x = 0)
    b.hull(ring(OUT, 0.3, 0.55, 0.88, -1.5) + ring(OUT, WL + 0.3, 0.93, 0.975), 'paint2', bevel=0.2)
    b.hull(ring(OUT, WL, 0.93, 0.975) + ring(OUT, DECK, sheer=1.6), 'paint', bevel=0.2)
    # dark gunwale line (deck edge walkway)
    b.hull([(14.4, DECK - 0.05, -26.0), (15.0, DECK - 0.05, -12.0), (15.0, DECK - 0.05, 4.0), (13.6, DECK - 0.05, 9.6),
            (14.4, DECK + 0.2, -26.0), (15.0, DECK + 0.2, -12.0), (15.0, DECK + 0.2, 4.0), (13.6, DECK + 0.2, 9.6)],
           'dark', bevel=0.03, mirror=True)
    # ------------------------------------------------------------------ hangar: hollow walls (open when the roof opens)
    yb, yt = DECK - 0.1, 16.88
    b.box((HX0 - 1.0, yb, HZ0), (HX0, yt, HZ1), 'paint', bevel=0.12)          # left wall
    b.box((HX1, yb, HZ0), (HX1 + 1.0, yt, HZ1), 'paint', bevel=0.12)          # right wall
    b.box((HX0 - 1.0, yb, HZ0 - 1.0), (HX1 + 1.0, yt, HZ0), 'paint', bevel=0.12)   # aft wall
    b.box((HX0 - 1.0, yb, HZ1), (HX1 + 1.0, yt, HZ1 + 1.0), 'paint', bevel=0.12)   # forward wall
    # gable end caps above the walls (triangles up to the ridge), dark
    for z0, z1 in ((HZ0 - 1.0, HZ0), (HZ1, HZ1 + 1.0)):
        b.hull([(x, y, z) for z in (z0, z1) for x, y in ((HX0 - 1.0, yt), (HX1 + 1.0, yt), (0.25, 19.9))], 'paint2', bevel=0.1)
    # hangar floor well (dark) the lift platform sits in
    b.box((HX0, DECK - 0.2, HZ0), (HX1, DECK, HZ1), 'black', bevel=0.0)
    # sliding-door rails along the outside of the walls (the roof halves slide down here)
    for x0, x1 in ((HX0 - 1.6, HX0 - 1.0), (HX1 + 1.0, HX1 + 1.6)):
        b.box((x0, DECK, HZ0 + 1.0), (x1, 9.4, HZ1 - 1.0), 'dark', bevel=0.06)
    # yellow side lights on the hangar corners
    b.box((HX1 + 0.95, 15.2, HZ1 + 0.6), (HX1 + 1.2, 15.8, HZ1 + 1.0), 'lightw', bevel=0.0)
    b.box((HX0 - 1.2, 15.2, HZ1 + 0.6), (HX0 - 0.95, 15.8, HZ1 + 1.0), 'lightw', bevel=0.0)
    # ------------------------------------------------------------------ forward bridge (stepped) + mast block
    b.hull([(x * s, y, z) for s in (-1, 1) for x, y, z in
            [(9.6, DECK, 8.4), (8.8, DECK, 18.4), (9.4, 13.8, 8.6), (8.6, 13.8, 12.2)]], 'paint', bevel=0.18)
    b.hull([(x * s, y, z) for s in (-1, 1) for x, y, z in
            [(8.4, 11.6, 15.6), (8.95, 11.6, 14.4), (8.1, 13.4, 12.6), (8.6, 13.4, 12.2),
             (8.2, 11.6, 15.9), (7.9, 13.4, 12.9)]], 'glass', bevel=0.0)
    b.hull([(x * s, y, z) for s in (-1, 1) for x, y, z in
            [(6.2, DECK, -0.2), (6.2, DECK, 8.6), (6.2, 13.8, -0.2), (6.2, 13.8, 8.6), (3.8, 15.6, 0.4), (3.8, 15.6, 8.0)]], 'paint', bevel=0.16)
    b.hull([(x * s, y, z) for s in (-1, 1) for x, y, z in
            [(8.4, 13.75, 9.0), (8.0, 13.75, 12.0), (8.3, 13.95, 9.1), (7.9, 13.95, 11.9)]], 'team', bevel=0.03)
    b.hull([(x * s, y, z) for s in (-1, 1) for x, y, z in
            [(3.4, 15.55, 0.8), (3.4, 15.55, 7.6), (3.3, 15.75, 0.9), (3.3, 15.75, 7.5)]], 'team', bevel=0.03)
    b.box((-1.6, 15.6, 1.0), (2.0, 19.0, 6.6), 'paint2', bevel=0.14)
    b.cyl((0.2, 19.0, 3.8), (0.2, 24.0, 3.8), 0.35, 8, 'dark', r2=0.22)
    b.box((-2.4, 22.0, 3.5), (2.8, 22.5, 4.1), 'dark', bevel=0.04)
    b.cyl((0.2, 24.0, 3.8), (0.2, 24.3, 3.8), 0.26, 6, 'lightr')
    # bow: dark capstan pair + hazard bow plate (builder: yellow-black work markings)
    b.cyl((-2.4, DECK + 0.7, 26.0), (-2.4, DECK + 1.5, 26.0), 0.9, 10, 'dark', mirror=False)
    b.cyl((2.4, DECK + 0.7, 26.0), (2.4, DECK + 1.5, 26.0), 0.9, 10, 'dark', mirror=False)
    # ------------------------------------------------------------------ stern deckhouse
    b.hull([(x * s, y, z) for s in (-1, 1) for x, y, z in
            [(6.4, DECK, -29.2), (4.8, DECK, -36.4), (6.0, 13.2, -29.2), (4.4, 12.4, -35.6)]], 'paint', bevel=0.16)
    b.box((-4.0, 13.1, -34.0), (4.0, 13.4, -30.4), 'dark', bevel=0.04)
    b.box((-1.4, 5.6, -39.4), (1.4, 6.4, -39.1), 'lightr', bevel=0.0)

    # ------------------------------------------------------------------ roof halves (door1 origin -7.7, 16.88, -15)
    d = k.piece('door1'); D = d.at
    d.hull([D(x, y, z) for z in (-13.7, 14.2) for x, y in ((-0.7, -0.6), (-0.7, 0.25), (7.95, 2.95), (7.95, 2.3))],
           'paint2', bevel=0.12)
    d.hull([D(x, y + 0.05, z) for z in (-12.2, 12.8) for x, y in ((4.0, 1.5), (7.8, 2.72))] +
           [D(x, y + 0.24, z) for z in (-12.2, 12.8) for x, y in ((4.0, 1.5), (7.8, 2.72))], 'team', bevel=0.03)
    for z in (-6.0, 0.6, 7.2):
        d.hull([D(x, y + 0.06, z + dz) for dz in (0.0, 0.7) for x, y in ((0.4, 0.38), (3.4, 1.32))] +
               [D(x, y + 0.22, z + dz) for dz in (0.0, 0.7) for x, y in ((0.4, 0.38), (3.4, 1.32))], 'dark', bevel=0.0)
    k.clone('door2', 'door1', mirror_x=True)

    # ------------------------------------------------------------------ lift platform (origin 0, 7.5, -14)
    p = k.piece('plate'); Pl = p.at
    p.box(Pl(-7.4, -0.5, -13.9), Pl(7.9, 0.0, 13.5), 'paint2', bevel=0.1)
    for x in (-5.6, 6.1):
        p.box(Pl(x - 0.6, 0.0, -13.0), Pl(x + 0.6, 0.18, 12.6), 'hazard', bevel=0.0)

    # ------------------------------------------------------------------ crane: turret (origin -0.23, 7.37, -4.64)
    t = k.piece('turret'); T = t.at
    t.cyl(T(0, 0, 0), T(0, 0.6, 0), 3.0, 12, 'dark', bevel=0.04)
    t.hull([T(x * s, y, z) for s in (-1, 1) for x, y, z in
            [(2.8, 0.5, 1.6), (2.8, 0.5, -2.8), (2.2, 3.0, 1.2), (2.2, 3.0, -2.4)]], 'paint', bevel=0.14)
    t.box(T(-1.9, 2.95, -2.0), T(1.9, 3.1, 0.8), 'team', bevel=0.02)
    # arm (origin -0.23, 10.39, -4.64): long boom back along -z, hazard striped
    a = k.piece('arm'); A = a.at
    a.box(A(-1.6, -1.4, -18.4), A(1.6, 1.8, 1.0), 'hazard', bevel=0.12)
    a.cyl(A(-2.0, 0, 0), A(2.0, 0, 0), 1.4, 10, 'dark')
    a.box(A(-1.0, 1.75, -16.0), A(1.0, 2.1, -2.0), 'dark', bevel=0.04)
    # nano head (origin -0.44, 10.85, -21.48): body + emitter dish with cyan glow
    n = k.piece('nano'); N = n.at
    n.cyl(N(-1.9, 0, 0), N(2.2, 0, 0), 1.3, 10, 'dark')
    n.hull([N(x * s + 0.2, y, z) for s in (-1, 1) for x, y, z in
            [(2.2, 1.0, 1.2), (2.2, 1.0, -4.0), (2.6, 6.2, -2.0), (1.6, 7.6, -3.6), (2.4, 4.4, 1.6)]], 'paint', bevel=0.14)
    n.cyl(N(0.2, 4.6, 3.0), N(0.2, 5.3, 12.6), 1.0, 8, 'steel', r2=0.6)
    n.cyl(N(0.2, 5.3, 12.6), N(0.2, 5.4, 13.4), 1.3, 10, 'dark', bevel=0.03)
    n.cyl(N(0.2, 5.4, 13.35), N(0.2, 5.4, 13.5), 0.8, 10, 'lightc')
