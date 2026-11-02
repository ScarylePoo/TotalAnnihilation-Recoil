"""Underwater Energy Storage (ARM_T1_SEAECO_UWEnergyStorage) - Arm seabed energy storage (no waterline: sits on the sea
bed under at least 30 elmo of water). The land storage's octagonal light tank squashed into a low, wide pressure dome on
a dark skirt, held down by four heavy dark anchor buttresses on the diagonals; on top, inside a team ring, the big
glowing cyan capacitor core (box) under a steel cage.
Identity from above (through the water): a wide light octagon with a team ring round a bright cyan centre and four
dark corner blocks (the land storage is a tall tank with four light fins; the Arm UW metal storage is two long
ingot cylinders).
Pieces (Lua script): gp (empty root), base, box (core) - all at the origin, explode only.
res 1024: seen only through 30+ elmo of water.
Coordinates are ENGINE/global: X right, Y up, Z forward."""
import math

UNIT = dict(
    res=1024,
    preview_water=30.0,
    wreck=dict(seed=91),
)


def octagon(r, rot=math.pi / 8):
    return [(r * math.cos(rot + i * math.pi / 4), r * math.sin(rot + i * math.pi / 4)) for i in range(8)]


def build(k):
    b = k.piece('Base')
    b.plan(0.0, 3.2, octagon(30.0), 'paint2', bevel=0.35, top_inset=1.0)
    b.hull([(x, 3.0, z) for x, z in octagon(26.5)] + [(x, 11.0, z) for x, z in octagon(23.5)]
           + [(x, 18.0, z) for x, z in octagon(17.0)], 'paint', bevel=0.4)
    b.cyl((0, 18.4, 0), (0, 18.75, 0), 16.3, 8, 'team', rot=math.pi / 8)
    b.cyl((0, 18.6, 0), (0, 19.2, 0), 10.6, 8, 'paint2', rot=math.pi / 8)
    # dark coil band round the dome
    b.hull([(x * s, y, z * s) for x, z in octagon(25.3) for s in (1.0, 1.03) for y in (6.0, 8.0)], 'dark', bevel=0.0)
    # four anchor buttresses on the diagonals
    for ang in (45,):     # +x side built, mirrored to -x
        c, s = math.cos(math.radians(ang)), math.sin(math.radians(ang))
        for sg in (1, -1):
            R = lambda u, y, w: (sg * (c * u - s * w), y, sg * (s * u + c * w))
            b.hull([R(u, y, w) for u, y in ((19.0, 3.0), (31.0, 3.0), (31.0, 6.5), (20.0, 15.0), (17.0, 15.0))
                    for w in (-3.6, 3.6)], 'paint2', bevel=0.3, mirror=True)
            b.hull([R(u, y, w) for u, y in ((24.0, 6.6), (30.0, 6.6), (29.0, 7.2), (25.0, 7.2)) for w in (-2.4, 2.4)],
                   'lightc', bevel=0.0, mirror=True)
            b.hull([R(u, y + 0.3, w) for u, y in ((20.0, 15.0), (31.0, 6.5)) for w in (-1.9, 1.9)]
                   + [R(u, y + 0.05, w) for u, y in ((20.0, 15.0), (31.0, 6.5)) for w in (-1.9, 1.9)], 'team',
                   bevel=0.0, mirror=True)

    # ---------------------------------------------------------------- box: capacitor core
    x = k.piece('Box')
    x.cyl((0, 18.8, 0), (0, 25.5, 0), 8.6, 12, 'lightc', r2=7.8)
    x.cyl((0, 25.4, 0), (0, 26.6, 0), 9.4, 12, 'dark', r2=8.6, bevel=0.1)
    x.cyl((0, 26.5, 0), (0, 27.4, 0), 7.0, 12, 'lightc', r2=5.6)          # open glowing crown, seen from above
    x.cyl((0, 27.3, 0), (0, 28.0, 0), 2.0, 8, 'steel')
    for i in range(4):
        a = math.pi / 4 + i * math.pi / 2
        x.box((9.0 * math.cos(a) - 0.7, 18.8, 9.0 * math.sin(a) - 0.7),
              (9.0 * math.cos(a) + 0.7, 26.0, 9.0 * math.sin(a) + 0.7), 'steel', bevel=0.1)
