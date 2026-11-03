"""Underwater Metal Storage (CORE_T1_SEAECO_UWMetalStorage) - Core seabed metal storage (no waterline: sits on the sea
bed under at least 40 elmo of water). The land storage's tall bulging hooped ingot tank, now centred on a dark long
plinth between two horizontal ballast cylinders (+-x) wrapped in light steel rib bands (the land spine's ribs); the tank
lid is a light steel cross-hatch inside a team ring, and the ballast cylinders carry team saddle straps.
Identity from above (through the water): a dark round tank with a team ring and a light lid between two long dark
cylinders with light rib bands and team straps - a dark 'H' (the Core UW energy storage is a six-finned star).
Pieces (COB): groundplane (empty root), base - static.
res 1024: seen only through 40 elmo of water.
Coordinates are ENGINE/global: X right, Y up, Z forward."""
import math

UNIT = dict(
    res=1024,
    preview_water=40.0,
    wreck=dict(seed=241),
)

BX, BY, BR, BL = 25.0, 11.0, 8.6, 20.0      # ballast cylinders: axis x (+-), height, radius, half length (along z)


def ngon(n, r, rot=0.0):
    return [(r * math.cos(rot + i * 2 * math.pi / n), r * math.sin(rot + i * 2 * math.pi / n)) for i in range(n)]


def build(k):
    b = k.piece('base')
    b.plan(0.0, 3.0, [(-36.0, -18.0), (36.0, -18.0), (38.0, -15.0), (38.0, 15.0), (36.0, 18.0), (-36.0, 18.0),
                      (-38.0, 15.0), (-38.0, -15.0)], 'paint2', bevel=0.35, top_inset=1.0)
    # central bulging decagonal tank, hooped
    D = ngon(10, 1.0, math.pi / 10)
    prof = [(13.0, 2.8), (15.6, 12.0), (16.2, 24.0), (15.0, 36.0), (12.0, 41.0)]
    b.hull([(x * r, y, z * r) for r, y in prof for x, z in D], 'paint', bevel=0.4)
    for r, y in ((15.9, 10.0), (16.4, 22.0), (15.6, 32.0)):
        b.hull([(x * rr, yy, z * rr) for x, z in D for rr in (r, r + 0.35) for yy in (y, y + 1.8)], 'dark',
               bevel=0.0)
    b.hull([(x * rr, yy, z * rr) for x, z in D for rr, yy in ((13.4, 39.6), (11.0, 41.6), (12.2, 41.0), (13.9, 39.2))],
           'team', bevel=0.0)
    b.plan(40.8, 42.0, [(x * 9.6, z * 9.6) for x, z in D], 'steel', bevel=0.1)
    for w in (-4.0, 0.0, 4.0):
        b.box((-8.6, 41.9, w - 0.6), (8.6, 42.6, w + 0.6), 'dark', bevel=0.0)
        b.box((w - 0.6, 42.5, -8.6), (w + 0.6, 43.2, 8.6), 'dark', bevel=0.0)
    b.box((-1.6, 30.0, 15.3), (1.6, 31.2, 15.7), 'lightc', bevel=0.0)
    # ballast cylinders (+x built, mirrored)
    b.cyl((BX, BY, -BL), (BX, BY, BL), BR, 12, 'paint', rot=math.pi / 12, bevel=0.35, mirror=True)
    for sz in (-1, 1):
        b.cyl((BX, BY, BL * sz), (BX, BY, (BL + 3.0) * sz), BR - 0.3, 12, 'paint2', r2=3.6, rot=math.pi / 12,
              mirror=True)
    for z in (-15.0, -9.0, 9.0, 15.0):
        b.cyl((BX, BY, z - 1.0), (BX, BY, z + 1.0), BR + 0.3, 12, 'steel', rot=math.pi / 12, mirror=True)
    b.cyl((BX, BY, -4.0), (BX, BY, 4.0), BR + 0.18, 12, 'team', rot=math.pi / 12, mirror=True)
    for z in (-14.0, 0.0, 14.0):                     # saddles tying the cylinders to the tank
        b.hull([(x, y, zz) for x in (14.0, 22.0) for y in (2.8, 9.0) for zz in (z - 2.0, z + 2.0)], 'dark',
               bevel=0.2, mirror=True)
