"""Wind Generator (CORE_T1_ECO_WindGenerator) - Core wind. A squat dark square power house with four corner pylons,
carrying a tall vertical-axis 'eggbeater' rotor: a steel mast and three bowed light-steel blades (spins on y).
Identity from above: dark square with team pylon caps and a team rim round the deck, a light three-armed rotor star
over it (the Arm wind is a slim tower with a horizontal three-blade propeller).
Pieces (COB, third-party S3O layout kept): base, blades (spin y; origin 0, 32, 0).
Coordinates are ENGINE/global: X right, Y up, Z forward."""
import math

UNIT = dict(
    wreck=dict(seed=16, drop=['blades']),
    preview_pose={'blades': (0, 25, 0)},
)

H = 84.0          # rotor height above the blades origin
RB = 22.0         # blade bow radius


def build(k):
    # ------------------------------------------------------------------ base: square power house
    b = k.piece('base')
    sq = lambda h: [(-h, -h), (h, -h), (h, h), (-h, h)]
    b.plan(0.0, 4.0, sq(30.5), 'paint2', bevel=0.3, top_inset=1.0)
    b.plan(3.9, 27.0, sq(27.4), 'paint', bevel=0.35, top_inset=5.0)
    b.plan(26.9, 29.4, sq(22.2), 'paint2', bevel=0.2, top_inset=0.6)
    # team rim band round the deck
    for z0, z1 in ((-21.4, -18.2), (18.2, 21.4)):
        b.box((-21.4, 29.3, z0), (21.4, 29.65, z1), 'team', bevel=0.0)
    b.box((-21.4, 29.3, -18.2), (-18.2, 29.65, 18.2), 'team', bevel=0.0, mirror=True)
    # bearing housing
    b.cyl((0, 29.3, 0), (0, 33.0, 0), 8.6, 12, 'dark', r2=6.6, rot=math.pi / 12, bevel=0.15)
    # corner pylons with team caps
    for sz in (-1, 1):
        lo = (-29.0, 3.8, min(sz * 21.0, sz * 29.0)); hi = (-21.0, 33.0, max(sz * 21.0, sz * 29.0))
        b.box(lo, hi, 'paint', bevel=0.3, mirror=True)
        b.box((-28.4, 32.9, lo[2] + 0.6), (-21.6, 33.3, hi[2] - 0.6), 'team', bevel=0.0, mirror=True)
        b.box((-29.15, 24.0, lo[2] + 2.0), (-28.9, 25.4, hi[2] - 2.0), 'lightc', bevel=0.0, mirror=True)
    # front/back generator doors and side louvres
    for sz in (-1, 1):
        zf = sz * (27.4 - 1.0 / 23.1 * 5.0 * 0 + 0.0)
        b.hull([(x, y, sz * (27.4 - (y - 3.9) / 23.1 * 5.0 / math.sqrt(2) + d)) for x in (-8.0, 8.0) for y in (4.6, 16.0)
                for d in (0.05, 0.4)], 'dark', bevel=0.05)
        b.hull([(x, y, sz * (27.4 - (y - 3.9) / 23.1 * 5.0 / math.sqrt(2) + d)) for x in (-6.4, 6.4) for y in (13.0, 14.4)
                for d in (0.38, 0.5)], 'hazard', bevel=0.0)
    for i in range(3):
        y = 9.0 + i * 4.0
        b.hull([(-(27.4 - (yy - 3.9) / 23.1 * 5.0 / math.sqrt(2) + d), yy, z) for z in (-10.0, 10.0) for yy in (y, y + 1.6)
                for d in (0.05, 0.35)], 'black', bevel=0.0, mirror=True)

    # ------------------------------------------------------------------ blades: mast + three bowed blades (origin 0,32,0)
    r = k.piece('blades'); R = r.at
    r.cyl(R(0, 0.0, 0), R(0, H + 4.0, 0), 2.4, 10, 'steel', rot=math.pi / 10)
    r.cyl(R(0, 0.0, 0), R(0, 6.0, 0), 5.6, 6, 'paint', r2=3.4, rot=math.pi / 6, bevel=0.15)
    r.cyl(R(0, H - 4.0, 0), R(0, H + 2.0, 0), 3.4, 6, 'paint', r2=5.0, rot=math.pi / 6, bevel=0.15)
    r.cyl(R(0, H + 4.0, 0), R(0, H + 5.0, 0), 1.6, 8, 'lightr')
    for y in (30.0, 56.0):
        r.cyl(R(0, y, 0), R(0, y + 1.6, 0), 3.2, 10, 'dark', rot=math.pi / 10)

    def blade(ang, mirror=False):
        a = math.radians(ang); d = (math.cos(a), math.sin(a)); p = (-d[1], d[0])
        N = 9
        pts = []
        for i in range(N + 1):
            t = i / N
            y = 4.0 + (H - 8.0) * t
            rad = 4.0 + RB * math.sin(math.pi * t)
            pts.append((rad, y))
        for i in range(N):
            (r0, y0), (r1, y1) = pts[i], pts[i + 1]
            sec = []
            for rr, yy in ((r0, y0), (r1, y1)):
                for dr in (-1.3, 1.3):
                    for c in (-3.2, 3.2):
                        sec.append(R(d[0] * (rr + dr) + p[0] * c, yy, d[1] * (rr + dr) + p[1] * c))
            mid = 0.25 < (i + 0.5) / N < 0.75
            r.hull(sec, 'steel', bevel=0.1, mirror=mirror)
            if mid:   # team strip on the outer face of the bow (sweeps a team ring when spinning)
                sec2 = []
                for rr, yy in ((r0, y0), (r1, y1)):
                    for c in (-2.2, 2.2):
                        for dr in (1.32, 1.6):
                            sec2.append(R(d[0] * (rr + dr) + p[0] * c, yy, d[1] * (rr + dr) + p[1] * c))
                r.hull(sec2, 'team', bevel=0.0, mirror=mirror)
        # struts from the mast to the blade near its ends
        for t in (0.12, 0.88):
            y = 4.0 + (H - 8.0) * t; rad = 4.0 + RB * math.sin(math.pi * t)
            r.cyl(R(d[0] * 2.0, y, d[1] * 2.0), R(d[0] * rad, y, d[1] * rad), 0.9, 6, 'dark', mirror=mirror)
    blade(90)
    blade(-30, mirror=True)
