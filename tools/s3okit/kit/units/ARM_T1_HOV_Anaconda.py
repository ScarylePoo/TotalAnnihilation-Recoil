"""Anaconda (ARM_T1_HOV_Anaconda) - Arm hovertank. Broad octagonal hull on a thick black rubber skirt, four big
lift fans in the corners of the deck, a tall hexagonal turret set back from centre with ONE long cannon on its
left side (TA layout: the sleeve/barrel sit at x -4.8).
Pieces (TA 3DO, COB drives them): base (rocks x/z), turret (turn y), sleeve (turn x, gun mantlet), barrel (recoil
move z -6), flare (empty emit), wake1..8 (empty emit points on the skirt).
Value groups from above: black skirt ring around everything (reads "hover"), light Arm hull + turret, four dark
fan discs with light blades, dark-blue paint2 deck band and mantlet, team: turret roof + a front-glacis chevron.
Coordinates are ENGINE/global: X right, Y up, Z forward. mirror=True builds the -X twin sharing UVs."""
import math

UNIT = dict(
    res=1024,
    wreck=dict(seed=5, drop=['barrel'], pose={'turret': (0, 40, 0)}),
    preview_pose={'turret': (0, -25, 0), 'sleeve': (-4, 0, 0)},
)


def octo(rx, rz, c, y, zc=0.0):
    """octagon outline (x, y, z) with corner chamfer c"""
    return [(rx, y, zc + rz - c), (rx - c, y, zc + rz), (-rx + c, y, zc + rz), (-rx, y, zc + rz - c),
            (-rx, y, zc - rz + c), (-rx + c, y, zc - rz), (rx - c, y, zc - rz), (rx, y, zc - rz + c)]


def fan(b, x, z, y0, y1, r):
    """lift fan: dark housing ring, black well, light radial blades + hub (readable disc from above)"""
    b.cyl((x, y0, z), (x, y1, z), r + 0.9, 16, 'dark', bevel=0.12, mirror=True)
    b.cyl((x, y1, z), (x, y1 + 0.05, z), r, 16, 'black', mirror=True)
    for i in range(5):
        a = i * 2 * math.pi / 5 + 0.3
        ca, sa = math.cos(a), math.sin(a)
        pa, pb = 1.0, r - 0.25
        w = 0.55
        pts = []
        for d in (pa, pb):
            for s in (-w, w):
                px, pz = x + ca * d - sa * s, z + sa * d + ca * s
                pts += [(px, y1 - 0.25, pz), (px, y1 + 0.05, pz)]
        b.hull(pts, 'steel', bevel=0.0, mirror=True)
    b.cyl((x, y1 - 0.2, z), (x, y1 + 0.35, z), 1.2, 10, 'paint', bevel=0.06, mirror=True)


def build(k):
    b = k.piece('base')
    # ------------------------------------------------------------------ skirt: thick black rubber ring
    b.hull(octo(23.6, 23.6, 8.6, 0.0) + octo(25.2, 25.2, 9.0, 2.6) + octo(24.6, 24.6, 8.8, 5.2) +
           octo(22.6, 22.6, 8.2, 7.2), 'tread', bevel=0.3)
    # ------------------------------------------------------------------ hull
    b.hull(octo(22.8, 22.8, 8.2, 6.8) + octo(19.8, 19.8, 7.0, 15.4), 'paint', bevel=0.2)
    # dark-blue band round the hull wall just above the skirt (separates hull from skirt in side view)
    b.hull(octo(23.2, 23.2, 8.3, 7.0) + octo(22.6, 22.6, 8.1, 8.9), 'paint2', bevel=0.1)
    # deck plate on top, slightly raised, light
    b.hull(octo(18.8, 18.8, 6.6, 15.3) + octo(18.2, 18.2, 6.4, 16.4), 'paint', bevel=0.12)
    # central spine (dark blue) the turret ring sits on, running to the nose
    b.box((-5.0, 16.2, -15.5), (5.0, 17.0, 16.2), 'paint2', bevel=0.12)
    # four big lift fans
    for z in (-9.6, 5.2):
        fan(b, 12.6, z, 15.8, 17.4, 4.4)
    # front glacis team chevron (Anaconda's mark from above: arrow on the nose)
    for sx in (1,):
        b.hull([(x, y, z) for x, y, z in
                [(1.2, 16.42, 18.6), (12.4, 16.42, 12.4), (12.4, 16.42, 9.8), (1.2, 16.42, 15.8),
                 (1.2, 16.56, 18.6), (12.4, 16.56, 12.4), (12.4, 16.56, 9.8), (1.2, 16.56, 15.8)]],
               'team', bevel=0.03, mirror=True)
    # nose: headlights + sensor block
    b.box((-3.6, 12.4, 21.4), (3.6, 15.4, 22.0), 'dark', bevel=0.08)
    b.box((-3.0, 13.0, 21.95), (3.0, 14.8, 22.1), 'lightc', bevel=0.0)
    b.box((7.8, 11.0, 20.4), (10.6, 12.6, 21.2), 'dark', bevel=0.06, mirror=True)
    b.box((8.1, 11.2, 21.15), (10.3, 12.4, 21.28), 'lightw', bevel=0.0, mirror=True)
    # rear: twin thrust ducts (dark cylinders) with black bores + red lights
    for x in (6.5,):
        b.cyl((x, 12.6, -20.6), (x, 12.6, -23.8), 3.0, 14, 'dark', bevel=0.1, mirror=True)
        b.cyl((x, 12.6, -23.8), (x, 12.6, -23.9), 2.2, 14, 'black', mirror=True)
    b.box((14.0, 12.4, -20.2), (16.0, 13.4, -19.6), 'lightr', bevel=0.0, mirror=True)
    # antenna rear left
    b.cyl((-15.6, 16.4, -11.8), (-15.6, 17.2, -11.8), 0.4, 8, 'dark')
    b.cyl((-15.6, 17.2, -11.8), (-15.6, 24.0, -11.8), 0.1, 6, 'steel', r2=0.05)
    b.cyl((-15.6, 24.0, -11.8), (-15.6, 24.2, -11.8), 0.16, 6, 'lightc')

    # ---------------------------------------------------------------- turret (origin 0, 20.25, -5; turns y)
    t = k.piece('turret'); A = t.at
    t.cyl(A(0, -3.9, 0), A(0, 0.2, 0), 7.6, 18, 'dark', bevel=0.1)
    hexb = [(0.0, -12.2), (8.0, -8.8), (9.8, 0.0), (8.0, 8.0), (0.0, 12.0)]
    hext = [(0.0, -10.4), (6.4, -7.6), (7.8, 0.0), (6.2, 6.4), (0.0, 9.0)]
    t.hull([A(x * sx, y, z) for sx in (-1, 1) for (x, z), y in
            [(p, 0.0) for p in hexb] + [(p, 5.4) for p in hext]], 'paint', bevel=0.18)
    # team roof plate (hex)
    t.hull([A(x * sx, y, z) for sx in (-1, 1) for (x, z) in
            [(0.0, -8.6), (5.0, -6.4), (6.2, 0.0), (5.0, 5.0), (0.0, 7.2)] for y in (5.42, 5.56)], 'team', bevel=0.03)
    # commander's cupola, right, with cyan vision block
    t.cyl(A(3.6, 5.4, -3.2), A(3.6, 6.6, -3.2), 1.6, 12, 'paint2', bevel=0.08)
    t.box(A(2.9, 5.9, -1.75), A(4.3, 6.3, -1.55), 'lightc', bevel=0.0)
    # rear bustle box, dark
    t.hull([A(x * sx, y, z) for sx in (-1, 1) for x, y, z in
            [(5.6, 0.6, -10.6), (5.6, 4.0, -10.0), (4.6, 0.8, -13.6), (4.4, 3.6, -13.2)]], 'paint2', bevel=0.12)

    # ---------------------------------------------------------------- sleeve (pivot 0, 22.65, -9.59): mantlet
    sv = k.piece('sleeve')
    gx, gy = -4.84, 23.65
    sv.box((gx - 2.4, gy - 2.1, 2.4), (gx + 2.4, gy + 2.1, 6.4), 'paint2', bevel=0.22)
    sv.cyl((gx, gy, 6.2), (gx, gy, 8.2), 1.5, 12, 'dark', r2=1.25, bevel=0.06)

    # ---------------------------------------------------------------- barrel (origin -4.84, 23.65, 5.04; recoil z)
    br = k.piece('barrel'); B = br.at
    br.cyl(B(0, 0, 1.0), B(0, 0, 20.4), 0.95, 12, 'steel')
    br.cyl(B(0, 0, 8.0), B(0, 0, 12.0), 1.25, 12, 'dark', bevel=0.05)        # fume extractor
    br.cyl(B(0, 0, 20.2), B(0, 0, 22.6), 1.45, 8, 'dark', rot=math.pi / 8, bevel=0.06)   # muzzle brake
    br.cyl(B(0, 0, 22.58), B(0, 0, 22.66), 0.65, 10, 'black')
    for sx in (-1, 1):
        br.box(B(1.3 * sx, -0.4, 20.8), B(1.55 * sx, 0.4, 21.6), 'black', bevel=0.0)
