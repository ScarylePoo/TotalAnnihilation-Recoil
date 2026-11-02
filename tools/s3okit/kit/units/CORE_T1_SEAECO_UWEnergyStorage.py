"""Underwater Energy Storage (CORE_T1_SEAECO_UWEnergyStorage) - Core seabed energy storage (no waterline: sits on the
sea bed under at least 31 elmo of water). The land storage's dark finned accumulator drum pressed down into a wide low
pressure bell: a dark decagonal dome with six heavy radial anchor fins sweeping down to the sea bed (team-topped), a
team shoulder ring, and on the crown a glowing warm cell band (glowingpart) under a light steel cap.
Identity from above (through the water): a dark six-pointed star of fins round a dark disc with a team ring, an orange
glowing ring and a light centre (the land storage is a ten-toothed cog round a dome; the Core UW metal storage is a
tall hooped tank flanked by ballast cylinders).
Pieces (COB): groundplane (empty root), base, glowingpart - at the origin, static.
res 1024: seen only through 30+ elmo of water.
Coordinates are ENGINE/global: X right, Y up, Z forward."""
import math

UNIT = dict(
    res=1024,
    preview_water=31.0,
    wreck=dict(seed=221),
)


def ngon(n, r, rot=0.0):
    return [(r * math.cos(rot + i * 2 * math.pi / n), r * math.sin(rot + i * 2 * math.pi / n)) for i in range(n)]


def build(k):
    b = k.piece('base')
    D = ngon(10, 1.0, math.pi / 10)
    b.hull([(x * 24.0, 0.0, z * 24.0) for x, z in D] + [(x * 22.5, 9.0, z * 22.5) for x, z in D]
           + [(x * 17.0, 18.0, z * 17.0) for x, z in D] + [(x * 10.0, 23.0, z * 10.0) for x, z in D], 'paint',
           bevel=0.4)
    # team shoulder ring (follows the dome slope between y 15 and 20)
    for i in range(10):
        p, q = D[i], D[(i + 1) % 10]
        pts = []
        for f, y in ((19.0, 15.6), (14.2, 20.2)):
            for (x, z) in (p, q):
                pts += [(x * (f + 0.25), y + 0.15, z * (f + 0.25)), (x * (f + 0.05), y - 0.05, z * (f + 0.05))]
        b.hull(pts, 'team', bevel=0.0)
    b.hull([(x * s, y, z * s) for x, z in D for s in (22.9, 23.5) for y in (5.0, 6.8)], 'dark', bevel=0.0)
    # six anchor fins (radial)
    for i in range(6):
        a = math.pi / 2 + i * math.pi / 3
        c, s = math.cos(a), math.sin(a)
        R = lambda u, y, w: (c * u - s * w, y, s * u + c * w)
        mir = i in (1, 2)          # fins at 150/210 deg mirror the ones at 30/330: built once
        if i in (4, 5):
            continue
        b.hull([R(u, y, w) for u, y in ((14.0, 21.0), (17.0, 21.0), (31.0, 3.0), (31.0, 0.0), (20.0, 0.0))
                for w in (-2.4, 2.4)], 'paint2', bevel=0.3, mirror=mir)
        b.hull([R(u + du, y + 0.25, w) for u, y in ((15.0, 21.0), (30.0, 3.4)) for du in (0.0, 0.3)
                for w in (-1.7, 1.7)], 'team', bevel=0.0, mirror=mir)
        b.box(R(30.9, 0.6, -0.8), R(31.3, 1.6, 0.8), 'lightc', bevel=0.0, mirror=mir)

    # ---------------------------------------------------------------- glowingpart: cell band + cap
    g = k.piece('glowingpart')
    g.cyl((0, 22.6, 0), (0, 26.0, 0), 9.4, 10, 'lightc', r2=8.6, rot=math.pi / 10)
    g.cyl((0, 25.9, 0), (0, 28.0, 0), 9.0, 10, 'steel', r2=6.0, rot=math.pi / 10, bevel=0.3)
    g.cyl((0, 27.9, 0), (0, 29.2, 0), 3.4, 10, 'dark', rot=math.pi / 10)
    for i in range(10):
        a = math.pi / 10 + i * math.pi / 5
        g.box((9.0 * math.cos(a) - 0.6, 22.6, 9.0 * math.sin(a) - 0.6),
              (9.0 * math.cos(a) + 0.6, 26.2, 9.0 * math.sin(a) + 0.6), 'dark', bevel=0.0)
