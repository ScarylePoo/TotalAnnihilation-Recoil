"""Energy Storage (ARM_T1_ECO_EnergyStorage) - Arm energy storage. A tall light tapered octagonal capacitor tank on a
dark skirt, four heavy diagonal buttress fins, dark coil bands, and a wide flat roof with a team ring round a big
glowing cyan capacitor core.
Identity from above: light octagon with a bright cyan centre inside a team ring and four light fins at the corners
(the Core storage is a dark round cog of ten fins round an orange dome; the Arm metal storage is a long vault).
Pieces (Lua script, third-party S3O layout kept): base only (origin 0, 3, 0).
Coordinates are ENGINE/global: X right, Y up, Z forward."""
import math

UNIT = dict(
    wreck=dict(seed=17),
    preview_pose={},
)


def octagon(r, rot=math.pi / 8):
    return [(r * math.cos(rot + i * math.pi / 4), r * math.sin(rot + i * math.pi / 4)) for i in range(8)]


def build(k):
    b = k.piece('base')
    # skirt and tank
    b.plan(0.0, 3.6, octagon(22.4), 'paint2', bevel=0.25, top_inset=1.2)
    b.plan(3.5, 36.0, octagon(19.0), 'paint', bevel=0.35, top_inset=3.2)
    # coil bands (dark) - slightly proud of the taper
    for y in (10.0, 18.0, 26.0):
        r = 19.0 - (y - 3.5) / 32.5 * 3.2 + 0.35
        b.plan(y, y + 2.2, octagon(r), 'dark', bevel=0.1, top_inset=0.2)
    # roof: rim, team ring, recessed glowing core
    b.plan(35.9, 38.2, octagon(15.6), 'paint2', bevel=0.2, top_inset=0.6)
    b.cyl((0, 38.0, 0), (0, 38.45, 0), 13.6, 16, 'team', rot=math.pi / 16)
    b.cyl((0, 38.2, 0), (0, 38.7, 0), 9.4, 16, 'dark', rot=math.pi / 16)
    b.cyl((0, 38.5, 0), (0, 40.6, 0), 7.2, 16, 'lightc', r2=6.0, rot=math.pi / 16)
    # buttress fins on the four diagonals (built on -x, mirrored)
    for sz in (-1, 1):
        d = (-math.sqrt(0.5), sz * math.sqrt(0.5)); p = (-d[1], d[0])
        P = lambda u, v, y: (d[0] * u + p[0] * v, y, d[1] * u + p[1] * v)
        prof = [(14.0, 0.0), (26.0, 0.0), (26.0, 3.0), (20.6, 14.0), (17.4, 38.6), (14.0, 38.6)]
        b.hull([P(u, v, y) for u, y in prof for v in (-2.4, 2.4)], 'paint', bevel=0.25, mirror=True)
        b.hull([P(u, v, y) for u, y in ((14.4, 38.6), (17.2, 38.6), (14.4, 38.9), (17.0, 38.9)) for v in (-1.8, 1.8)],
               'team', bevel=0.0, mirror=True)
        b.hull([P(u, v, y) for u, y in ((21.0, 0.0), (26.6, 0.0), (21.0, 1.6), (26.6, 1.6)) for v in (-3.4, 3.4)],
               'dark', bevel=0.12, mirror=True)
        b.hull([P(u, v, y) for u, y in ((20.8, 14.6), (20.9, 15.8), (19.5, 25.0), (19.6, 26.2)) for v in (-0.6, 0.6)],
               'lightc', bevel=0.0, mirror=True)
    # hazard-striped access hatch on the front and a dark one at the back
    for sz, mat in ((1, 'hazard'), (-1, 'dark')):
        ap = lambda y: (19.0 - (y - 3.5) / 32.5 * 3.2) * math.cos(math.pi / 8)
        b.hull([(x, y, sz * (ap(y) + dd)) for x in (-4.0, 4.0) for y in (4.0, 9.4) for dd in (0.05, 0.35)], mat,
               bevel=0.0)
