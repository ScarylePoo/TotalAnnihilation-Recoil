"""Underwater Metal Extractor (CORE_T1_SEAECO_UWMetalExtractor) - Core seabed mex (no waterline: sits on the sea bed
under at least 10 elmo of water). The land Core mex's low dark hexagonal pyramid with team facets; instead of a
rising claw, a heavy ring (drive) turns round the pyramid's waist with three intake scoops whose funnels vent the ore
slurry (emit1..3), and on top a light three-blade impeller (fan) spins under a light steel cross-arched cage.
Identity from above (through the water): a dark hexagon with three team facets, a light steel '+' of arches with a
light whirl under it at the centre, three light funnel heads round the rim (the Arm UW mex is a light octagon with a
team 'Y' and three tall stacks).
Pieces (COB): base, drive (spin y; origin 0, 8.5, 0), fan (spin y; origin 0, 15, 0), emit1..3 (children of drive,
empty: the funnel mouths).
Coordinates are ENGINE/global: X right, Y up, Z forward."""
import math

UNIT = dict(
    res=1024,
    preview_water=10.0,
    wreck=dict(seed=231, drop=['fan']),
    preview_pose={'drive': (0, 10, 0), 'fan': (0, 30, 0)},
)


def hexagon(r, rot=0.0):
    return [(r * math.cos(rot + i * math.pi / 3), r * math.sin(rot + i * math.pi / 3)) for i in range(6)]


def build(k):
    b = k.piece('base')
    H = hexagon(1.0, math.pi / 6)
    b.plan(0.0, 3.0, [(x * 25.5, z * 25.5) for x, z in H], 'paint2', bevel=0.3, top_inset=0.8)
    b.hull([(x * 23.0, 2.8, z * 23.0) for x, z in H] + [(x * 11.0, 12.0, z * 11.0) for x, z in H], 'paint', bevel=0.3)
    b.plan(11.8, 14.0, [(x * 9.0, z * 9.0) for x, z in H], 'dark', bevel=0.15, top_inset=0.6)
    # team facets on three alternate faces (slope from r 23 @ 2.8 to r 11 @ 12)
    for i in (0, 2, 4):
        p, q = H[i], H[(i + 1) % 6]
        pts = []
        for f, y in ((21.0, 4.4), (13.0, 10.6)):
            for (x, z) in (p, q):
                for lift in (0.08, 0.3):
                    t = 0.82 if f > 15 else 0.7
                    mx, mz = (p[0] + q[0]) / 2, (p[1] + q[1]) / 2
                    xx, zz = mx + (x - mx) * t, mz + (z - mz) * t
                    pts.append((xx * (f + lift), y + lift * 0.8, zz * (f + lift)))
        b.hull(pts, 'team', bevel=0.0)
    # cross-arched cage over the fan (both arches cross x = 0: built whole)
    arch = [(12.6, 11.0), (12.0, 16.0), (9.6, 19.6), (5.0, 21.4), (0.0, 22.0)]
    for axis in ('x', 'z'):
        for sg in (-1, 1):
            for (r0, y0), (r1, y1) in zip(arch, arch[1:]):
                P = (lambda r, y, w: (sg * r, y, w)) if axis == 'x' else (lambda r, y, w: (w, y, sg * r))
                b.hull([P(r, y + dy, w) for r, y in ((r0, y0), (r1, y1)) for dy in (-1.0, 1.0) for w in (-1.2, 1.2)],
                       'steel', bevel=0.12)
    b.box((-1.4, 22.6, -1.4), (1.4, 23.6, 1.4), 'dark', bevel=0.1)
    b.box((-0.6, 23.5, -0.6), (0.6, 23.9, 0.6), 'lightc', bevel=0.0)

    # ---------------------------------------------------------------- drive: waist ring + three scoops
    d = k.piece('drive')
    n = 18                         # waist ring as segments (a cylinder would be a solid disc hiding the pyramid)
    for i in range(n):
        a0, a1 = 2 * math.pi * i / n, 2 * math.pi * (i + 1) / n
        P = lambda r, a, y: (r * math.cos(a), y, r * math.sin(a))
        d.hull([P(r, a, y) for r in (14.0, 17.4) for a in (a0, a1) for y in (6.4, 10.0)], 'paint2', bevel=0.1)
        d.hull([P(r, a, y) for r in (14.5, 16.9) for a in (a0, a1) for y in (9.95, 10.2)], 'team', bevel=0.0)
    for i in range(3):
        a = math.radians(90 + 120 * i)
        c, s = math.cos(a), math.sin(a)
        R = lambda u, y, w: (c * u - s * w, y, s * u + c * w)
        d.hull([R(u, y, w) for u in (15.0, 21.0) for y in (6.0, 11.0) for w in (-3.4, 3.4)], 'paint', bevel=0.3)
        d.hull([R(u, y, w) for u in (15.6, 18.0) for y in (10.95, 11.2) for w in (-2.6, 2.6)], 'team', bevel=0.0)
        d.cyl(R(19.4, 10.0, 0.0), R(19.4, 12.6, 0.0), 2.0, 10, 'steel', r2=3.0, bevel=0.06)
        d.cyl(R(19.4, 12.5, 0.0), R(19.4, 12.65, 0.0), 2.3, 10, 'black')

    # ---------------------------------------------------------------- fan: three-blade impeller
    f = k.piece('fan'); F = f.at
    f.cyl(F(0, -1.2, 0), F(0, 1.6, 0), 2.6, 10, 'dark', bevel=0.1)
    for i in range(3):
        a = math.radians(90 + 120 * i)
        c, s = math.cos(a), math.sin(a)
        R = lambda u, y, w: F(c * u - s * w, y, s * u + c * w)
        f.hull([R(2.0, -0.4, -1.8), R(2.0, 1.0, 1.8), R(8.8, -0.2, -1.4), R(8.8, 0.8, 1.6),
                R(2.0, 0.0, -1.8), R(2.0, 1.4, 1.8), R(8.8, 0.1, -1.4), R(8.8, 1.1, 1.6)], 'steel', bevel=0.1)
