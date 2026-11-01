"""Metal Storage (ARM_T1_ECO_MetalStorage) - Arm metal storage. A tall light chamfered vault block, longer than wide,
with dark loading ramps running up its front and back faces and roof machinery: a dark gantry rail with a crane
trolley and two big hexagonal ingot-silo hatches.
Identity from above: a long light rectangle (the only tall box in the Arm eco set) split by a team cross-band, two
dark hex hatches with team caps on one side, a dark gantry on the other (the Arm energy storage is an octagon).
Pieces (Lua script): base, pieces1 (roof machinery), pieces2 (ramps) - all at the origin, explode only.
Coordinates are ENGINE/global: X right, Y up, Z forward."""
import math

UNIT = dict(
    wreck=dict(seed=19, drop=['pieces1']),
    preview_pose={},
)

HX, HZ, HY = 21.0, 27.0, 54.0


def build(k):
    b = k.piece('base')
    ch = 5.0
    rect = lambda hx, hz, c: [(-hx + c, -hz), (hx - c, -hz), (hx, -hz + c), (hx, hz - c), (hx - c, hz), (-hx + c, hz),
                              (-hx, hz - c), (-hx, -hz + c)]
    b.plan(0.0, 2.6, rect(26.0, 31.0, 6.0), 'paint2', bevel=0.25, top_inset=0.8)
    b.plan(2.5, HY - 2.0, rect(HX, HZ, ch), 'paint', bevel=0.4, top_inset=1.6)
    b.plan(HY - 2.1, HY, rect(HX - 1.6, HZ - 1.6, ch - 0.6), 'paint', bevel=0.3, top_inset=0.8)
    # dark horizontal reinforcing bands on the long sides
    for y in (18.0, 34.0):
        b.box((-HX - 0.35 + (y - 2.5) / (HY - 4.5) * 1.6, y, -HZ + ch), (-HX + 1.0, y + 2.2, HZ - ch), 'dark',
              bevel=0.08, mirror=True)
    # team cross-band over the roof (across x) and down the long sides
    b.box((-HX + 2.0, HY - 0.05, -6.0), (HX - 2.0, HY + 0.3, 6.0), 'team', bevel=0.0)
    b.box((-17.4, HY - 0.05, -HZ + 3.4), (-6.8, HY + 0.25, HZ - 3.4), 'team', bevel=0.0)   # gantry bed
    b.box((-HX - 0.4 + (40.0 - 2.5) / (HY - 4.5) * 1.6, 38.0, -4.0), (-HX + 1.0, HY - 2.4, 4.0), 'team',
          bevel=0.0, mirror=True)
    b.box((-HX - 0.5 + 0.6, 6.0, -1.4), (-HX + 0.4, 7.4, 1.4), 'lightc', bevel=0.0, mirror=True)

    # ------------------------------------------------------------------ pieces1: roof machinery
    p = k.piece('pieces1')
    for sz in (-1, 1):                    # two hex silo hatches on the +x side
        cz = sz * 15.0
        p.cyl((10.0, HY - 0.1, cz), (10.0, HY + 3.6, cz), 7.4, 6, 'dark', rot=math.pi / 6, bevel=0.15)
        p.cyl((10.0, HY + 3.5, cz), (10.0, HY + 4.4, cz), 5.4, 6, 'team', rot=math.pi / 6, bevel=0.05)
        p.cyl((10.0, HY + 4.3, cz), (10.0, HY + 5.4, cz), 2.6, 6, 'steel', rot=math.pi / 6, bevel=0.05)
    # gantry on the -x side: two dark rails along z, trolley box
    for x in (-15.6, -8.6):
        p.box((x - 1.2, HY - 0.1, -HZ + 3.0), (x + 1.2, HY + 2.4, HZ - 3.0), 'dark', bevel=0.12)
    p.box((-17.6, HY + 2.3, 4.6), (-6.6, HY + 7.0, 13.0), 'paint2', bevel=0.3)
    p.box((-16.4, HY + 6.9, 5.8), (-7.8, HY + 7.2, 11.8), 'hazard', bevel=0.0)
    p.cyl((-12.1, HY + 2.3, 8.8), (-12.1, HY - 0.5, 8.8), 0.9, 6, 'steel')
    # ingot hopper in the middle
    p.hull([(x, y, z) for x, z in ((-4.0, -9.0), (4.0, -9.0), (-4.0, 9.0), (4.0, 9.0)) for y in (HY - 0.1,)] +
           [(x, HY + 4.0, z) for x, z in ((-2.4, -7.0), (2.4, -7.0), (-2.4, 7.0), (2.4, 7.0))], 'paint2', bevel=0.2)

    # ------------------------------------------------------------------ pieces2: loading ramps front and back
    r = k.piece('pieces2')
    for sz in (-1, 1):
        r.hull([(x, y, sz * z) for x in (-10.4, 10.4) for (y, z) in
                ((0.0, HZ + 9.0), (0.0, HZ - 1.0), (33.0, HZ - 1.0), (33.0, HZ + 0.6))], 'paint2', bevel=0.25)
        for i in range(5):
            y0 = 4.0 + i * 5.6
            zz = HZ + 0.6 + (33.0 - y0) / 33.0 * 8.4
            r.hull([(x, y, sz * (zz + d - (y - y0) / 33.0 * 8.4)) for x in (-9.0, 9.0) for y in (y0, y0 + 1.2)
                    for d in (0.0, 0.4)], 'dark', bevel=0.0)
        r.box((-9.6, 33.0, sz * (HZ - 0.6) - 0.8), (9.6, 34.0, sz * (HZ - 0.6) + 0.8), 'hazard', bevel=0.0)
