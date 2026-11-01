"""Metal Storage (CORE_T1_ECO_MetalStorage) - Core metal storage. A heavy dark decagonal plinth carrying a tall bulging
decagonal ingot tank (the 'knot', hooped) set off-centre, a sloped buttress spine on its -x flank topped by a stack
of light steel cooling ribs, and a hazard-framed loading door at the front right.
Identity from above: big dark decagon with a team ring and a light steel cross-hatch lid, a ribbed light spine arm
sticking out to the left (the Core energy storage is a ten-toothed cog with a dome).
Pieces (COB): base, knot, door, spine, ribs - all at the origin, explode only. Asymmetric (no mirrors).
Coordinates are ENGINE/global: X right, Y up, Z forward."""
import math

UNIT = dict(
    wreck=dict(seed=20, drop=['ribs']),
    preview_pose={},
)

CX, CZ = 5.4, -7.2


def deca(r, cx=CX, cz=CZ):
    return [(cx + r * math.cos(math.pi / 10 + i * math.pi / 5), cz + r * math.sin(math.pi / 10 + i * math.pi / 5))
            for i in range(10)]


def build(k):
    b = k.piece('base')
    b.plan(0.0, 4.0, deca(31.0), 'paint2', bevel=0.3, top_inset=1.0)
    b.plan(3.9, 21.0, deca(27.0), 'paint', bevel=0.35, top_inset=2.4)
    b.plan(20.9, 23.0, deca(24.4), 'paint2', bevel=0.2, top_inset=0.8)
    b.plan(22.9, 28.4, deca(19.0), 'dark', bevel=0.2, top_inset=0.0)
    b.box((CX - 1.2, 1.0, CZ + 30.0), (CX + 1.2, 2.6, CZ + 30.4), 'lightr', bevel=0.0)

    # ------------------------------------------------------------------ knot: the tank
    t = k.piece('knot')
    t.hull([(x, 27.6, z) for x, z in deca(19.6)] + [(x, 40.0, z) for x, z in deca(25.2)], 'paint', bevel=0.3)
    t.hull([(x, 39.9, z) for x, z in deca(25.2)] + [(x, 60.0, z) for x, z in deca(25.2)], 'paint', bevel=0.3)
    t.hull([(x, 59.9, z) for x, z in deca(25.2)] + [(x, 64.2, z) for x, z in deca(21.6)], 'paint', bevel=0.3)
    for y in (43.0, 49.0, 55.0):
        t.plan(y, y + 1.8, deca(25.6), 'dark', bevel=0.08, top_inset=0.0)
    # lid: team ring, dark centre, light steel cross-hatch
    t.cyl((CX, 64.1, CZ), (CX, 64.5, CZ), 20.6, 20, 'team', rot=math.pi / 20)
    t.cyl((CX, 64.3, CZ), (CX, 65.0, CZ), 14.6, 20, 'dark', rot=math.pi / 20, bevel=0.05)
    t.box((CX - 12.0, 64.8, CZ - 2.6), (CX + 12.0, 66.4, CZ + 2.6), 'steel', bevel=0.2)
    t.box((CX - 2.6, 64.8, CZ - 12.0), (CX + 2.6, 66.4, CZ + 12.0), 'steel', bevel=0.2)
    t.cyl((CX, 66.3, CZ), (CX, 67.0, CZ), 2.0, 8, 'lightc')

    # ------------------------------------------------------------------ spine: sloped buttress on the -x flank
    s = k.piece('spine')
    s.hull([(x, y, z) for z in (-26.4, -7.4) for (x, y) in
            ((-41.0, 0.0), (-16.0, 0.0), (-16.0, 44.0), (-30.0, 44.0))], 'paint2', bevel=0.3)
    s.hull([(x, y, z) for z in (-24.6, -9.2) for (x, y) in ((-40.6, 1.0), (-39.2, 1.0), (-29.3, 41.0), (-30.7, 41.0))],
           'hazard', bevel=0.0)
    s.box((-41.4, 0.0, -27.2), (-34.0, 2.4, -6.6), 'dark', bevel=0.15)

    # ------------------------------------------------------------------ ribs: steel cooling fins atop the spine
    r = k.piece('ribs')
    for i in range(5):
        y = 44.0 + i * 4.4
        x0 = -32.4 + i * 0.6
        r.hull([(x, yy, z) for z in (-23.4, -8.0) for (x, yy) in
                ((x0, y), (-14.0, y), (-14.0, y + 2.2), (x0 + 1.6, y + 2.2))], 'steel', bevel=0.15)
    r.box((-24.0, 42.0, -18.0), (-16.0, 66.0, -13.4), 'dark', bevel=0.15)

    # ------------------------------------------------------------------ door: loading bay at the front right
    d = k.piece('door')
    d.hull([(x, y, z) for y in (0.5, 16.0) for (x, z) in ((7.6, 18.0), (16.0, 28.6), (27.0, 18.6), (19.0, 11.4))],
           'paint2', bevel=0.3)
    d.hull([(16.0 + 11.0 * tt + 0.67 * dd, y, 28.6 - 10.0 * tt + 0.74 * dd) for y in (1.0, 13.0) for tt in (0.18, 0.82)
            for dd in (-0.1, 0.3)], 'dark', bevel=0.0)
    d.hull([(x, y, z) for y in (15.9, 16.25) for (x, z) in ((10.0, 18.6), (16.0, 26.0), (24.0, 18.8), (18.4, 13.4))],
           'hazard', bevel=0.0)
