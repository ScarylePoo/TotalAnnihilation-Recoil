"""Defender - Naval Series (ARM_T1_SEADEF_Defender) - Arm floating missile tower. Waterline 15 (the water surface is
model y = 15). A four-drum raft: four light float drums at the corners (team tops, 4 elmo proud of the water) braced by
a dark X deck just above the surface, a central hub collar and a tall column carrying the land Defender's head - a
yoke turret, a long light missile box and a fat revolving three-tube drum (barrel turns on z between shots). Under the
surface only a plain ballast keel (always submerged: kept simple, little texture).
Identity from above: four team discs at the corners of a dark X with the long light launcher across the middle (the
land Defender stands on a four-legged pylon over a square pad; the Arm Stingray is a solid hexagonal hull).
Pieces (Lua script): base (RockUnit turns x/z), turret (turn y), gun (turn x), barrel (turn z), flare (emit, empty).
Coordinates are ENGINE/global: X right, Y up, Z forward."""
import math

WL = 15.0
UNIT = dict(
    res=2048,
    ground=False, water=WL,
    wreck=dict(seed=21, drop=['barrel'], pose={'turret': (0, 40, 0), 'gun': (12, 0, 0)}),
    preview_pose={'turret': (0, -25, 0), 'gun': (-12, 0, 0)},
)

D = 17.5          # drum centres (+-D, +-D)


def build(k):
    # ------------------------------------------------------------------ base: raft
    b = k.piece('base')
    for sz in (-1, 1):
        c = (D, 0, D * sz)
        b.cyl((c[0], 7.0, c[2]), (c[0], 19.0, c[2]), 7.2, 16, 'paint', rot=math.pi / 16, bevel=0.3, mirror=True)
        b.cyl((c[0], 18.9, c[2]), (c[0], 19.35, c[2]), 3.9, 16, 'team', rot=math.pi / 16, mirror=True)
        b.cyl((c[0], 13.6, c[2]), (c[0], 15.6, c[2]), 7.55, 16, 'dark', rot=math.pi / 16, mirror=True)   # rub ring
        b.cyl((c[0], 3.0, c[2]), (c[0], 7.2, c[2]), 5.0, 8, 'paint2', r2=6.6, rot=math.pi / 8, mirror=True)
        b.box((c[0] - 1.0, 17.0, c[2] - 7.6 * sz - 0.15), (c[0] + 1.0, 18.0, c[2] - 7.6 * sz + 0.15), 'lightc',
              bevel=0.0, mirror=True)
    # dark X deck between the drums (two diagonal beams), just above the water
    w = 3.4
    for sz in (-1, 1):
        b.hull([(x, y, x * sz + s * w * sz) for x in (0.0, D - 4.0) for y in (15.4, 18.2) for s in (-1, 1)]
               + [(0.0, 15.4, 0.0)], 'paint2', bevel=0.2, mirror=True)
        b.hull([(x, 18.1, x * sz + s * 1.0 * sz) for x in (4.0, D - 6.0) for s in (-1, 1)]
               + [(x, 18.45, x * sz + s * 1.0 * sz) for x in (4.0, D - 6.0) for s in (-1, 1)], 'dark', bevel=0.0,
               mirror=True)
    # hub collar and column (cross x = 0: built whole)
    b.cyl((0, 14.0, 0), (0, 21.5, 0), 9.2, 8, 'paint', r2=7.6, rot=math.pi / 8, bevel=0.3)
    b.cyl((0, 21.4, 0), (0, 22.2, 0), 7.4, 8, 'dark', rot=math.pi / 8, bevel=0.05)
    b.cyl((0, 21.0, 0), (0, 41.0, 0), 4.6, 8, 'paint2', r2=3.7, rot=math.pi / 8, bevel=0.15)
    b.cyl((0, 27.5, 0), (0, 32.0, 0), 6.4, 8, 'paint', r2=5.4, rot=math.pi / 8, bevel=0.2)
    for y in (34.0, 37.5):
        b.cyl((0, y, 0), (0, y + 1.0, 0), 4.6, 8, 'dark', rot=math.pi / 8, bevel=0.05)
    b.box((-1.2, 29.0, 5.7), (1.2, 30.4, 6.05), 'lightc', bevel=0.0)
    # ballast keel (always submerged)
    b.cyl((0, 0.0, 0), (0, 14.2, 0), 4.0, 8, 'dark', r2=6.0, rot=math.pi / 8)

    # ---------------------------------------------------------------- turret: yoke (origin 0, 40.7, -0.3)
    t = k.piece('turret'); A = t.at
    t.cyl(A(0, 0, 0), A(0, 1.6, 0), 6.4, 12, 'dark', bevel=0.1)
    t.hull([A(x * sx, y, z) for sx in (-1, 1) for x, y, z in
            [(5.6, 1.6, -5.0), (5.6, 1.6, 5.0), (4.6, 4.5, -4.4), (4.6, 4.5, 4.4)]], 'paint', bevel=0.15)
    t.hull([A(x, y, z) for x, y, z in
            [(4.4, 4.0, -3.4), (8.6, 4.0, -3.4), (4.4, 4.0, 3.4), (8.6, 4.0, 3.4),
             (5.6, 12.4, -2.6), (8.2, 12.4, -2.6), (5.6, 12.4, 2.6), (8.2, 12.4, 2.6)]], 'paint2', bevel=0.15, mirror=True)
    t.hull([A(x, y, z) for x, y, z in
            [(5.9, 12.35, -2.3), (7.9, 12.35, -2.3), (5.9, 12.65, -2.3), (7.9, 12.65, -2.3),
             (5.9, 12.35, 2.3), (7.9, 12.35, 2.3), (5.9, 12.65, 2.3), (7.9, 12.65, 2.3)]], 'team', bevel=0.0, mirror=True)
    t.cyl(A(8.2, 9.9, 1.1), A(9.4, 9.9, 1.1), 2.2, 10, 'dark', bevel=0.06, mirror=True)

    # --------------------------------------------------------------- gun: long missile box (origin 0, 50.6, 0.8)
    g = k.piece('gun'); L = g.at
    g.hull([L(x * sx, y, z) for sx in (-1, 1) for x, y, z in
            [(5.4, -3.6, -22.0), (5.4, -3.6, 15.0), (5.4, 4.2, -21.0), (5.4, 4.2, 14.4),
             (4.2, 5.6, -20.0), (4.2, 5.6, 13.6), (4.0, -4.6, -20.4), (4.0, -4.6, 14.8)]], 'paint', bevel=0.2)
    # roof: team stripe along the box, dark hatch rows either side
    g.hull([L(x * sx, y, z) for sx in (-1, 1) for x, y, z in
            [(2.4, 5.62, -18.0), (2.4, 5.62, 11.0), (2.2, 5.78, -17.8), (2.2, 5.78, 10.8)]], 'team', bevel=0.0)
    for z in (-15.0, -9.0, -3.0, 3.0):
        g.box(L(2.9, 5.0, z), L(4.0, 5.6, z + 4.6), 'dark', bevel=0.05, mirror=True)
    g.box(L(-4.6, -3.0, -24.6), L(4.6, 3.8, -21.6), 'dark', bevel=0.15)
    g.box(L(5.3, -2.2, -16.0), L(6.0, 3.0, 8.0), 'paint2', bevel=0.1, mirror=True)
    g.cyl(L(0, 3.3, 14.4), L(0, 3.3, 18.0), 6.2, 12, 'dark', bevel=0.1)
    g.box(L(-1.0, 5.6, 11.8), L(1.0, 5.75, 13.2), 'lightr', bevel=0.0)

    # --------------------------------------------------------------- barrel: revolving 3-tube drum (origin 0, 53.9, 19.5)
    br = k.piece('barrel'); B = br.at
    br.cyl(B(0, 0, -0.6), B(0, 0, 10.0), 2.4, 10, 'dark', bevel=0.05)
    for i in range(3):
        a = math.radians(90 + 120 * i)
        cx, cy = 4.3 * math.cos(a), 4.3 * math.sin(a)
        br.cyl(B(cx, cy, -0.4), B(cx, cy, 10.4), 2.75, 10, 'paint2', bevel=0.08)
        br.cyl(B(cx, cy, 10.4), B(cx, cy, 10.95), 2.0, 10, 'steel')
        br.cyl(B(cx, cy, 10.9), B(cx, cy, 11.05), 1.5, 10, 'black')
    br.cyl(B(0, 0, 3.6), B(0, 0, 5.2), 7.4, 12, 'dark', bevel=0.08)
    br.cyl(B(0, 0, 10.0), B(0, 0, 10.8), 1.4, 8, 'hazard')
