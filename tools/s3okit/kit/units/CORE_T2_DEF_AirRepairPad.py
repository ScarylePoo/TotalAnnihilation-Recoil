"""Air Repair Pad (CORE_T2_DEF_AirRepairPad) - Core aircraft repair pad. A heavy octagonal skirt with four buttress
blocks carrying a raised square landing pedestal, and two tall angled nano towers (guns) on the left and right.
No moving parts.
Identity from above: a dark octagon with a lighter steel landing square, a team octagon ring on it and ochre-black
landing-zone chevrons, two tall light nano towers either side - octagonal where the Arm pad is square.
Pieces (COB): base, guns (both nano towers), beam1/beam2 (nano emit points, empty), pedistal (the landing deck),
pad (landing point, empty).
Coordinates are ENGINE/global: X right, Y up, Z forward."""
import math

UNIT = dict(
    res=2048, bake_res=2048,          # no 2x supersampling: machine time (see the batch report)
    wreck=dict(seed=61, drop=['guns']),
)

SK, PD = 12.4, 18.7      # skirt top, pedestal top


def octagon(r, rot=math.pi / 8):
    return [(r * math.cos(rot + i * math.pi / 4), r * math.sin(rot + i * math.pi / 4)) for i in range(8)]


def build(k):
    # ------------------------------------------------------------------ base: octagonal skirt + buttresses
    b = k.piece('base')
    b.plan(0.0, 2.8, octagon(36.4), 'paint2', bevel=0.3, top_inset=1.0)
    b.plan(2.6, SK, octagon(33.6), 'paint', bevel=0.35, top_inset=3.0)
    for ux, uz in ((0, 1), (0, -1)):
        b.hull([(x, y, uz * u) for x in (-6.0, 6.0) for u, y in ((28.0, 0.0), (35.0, 0.0), (35.0, 7.0), (28.0, 11.0))], 'paint2', bevel=0.25)
        b.box((-4.0, 2.0, uz * 34.4 - 0.5 if uz > 0 else -35.0), (4.0, 6.0, 35.0 if uz > 0 else -34.4 + 0.5), 'dark', bevel=0.06)
    b.box((-0.8, 7.6, 34.5), (0.8, 8.8, 35.1), 'lightr', bevel=0.0)

    # ------------------------------------------------------------------ pedistal: landing deck
    p = k.piece('pedistal')
    p.plan(SK - 0.2, PD, [(-24.0, -24.0), (24.0, -24.0), (24.0, 24.0), (-24.0, 24.0)], 'steel', bevel=0.35, top_inset=1.2)
    ro, ri = octagon(19.4), octagon(11.8)
    for i in range(8):
        j = (i + 1) % 8
        p.hull([(x, y, z) for x, z in (ro[i], ro[j], ri[i], ri[j]) for y in (PD - 0.1, PD + 0.22)], 'team', bevel=0.0)
    p.plan(PD - 0.1, PD + 0.18, octagon(5.0), 'dark', bevel=0.0)
    for sx in (-1, 1):
        for sz in (-1, 1):
            p.hull([(sx * x, y, sz * z) for x, z in ((21.2, 21.2), (13.6, 21.2), (21.2, 13.6), (18.2, 18.2), (13.6, 18.2), (18.2, 13.6))
                    for y in (PD - 0.1, PD + 0.26)], 'hazard', bevel=0.02)

    # ------------------------------------------------------------------ guns: two angled nano towers (origin 0, 0, 0)
    g = k.piece('guns')
    for sx in (1,):          # mirrored to -x (shared UVs)
        g.hull([(sx * x, y, z) for x, y, z in
                [(28.6, 0.0, -5.6), (36.6, 0.0, -5.6), (28.6, 0.0, 5.6), (36.6, 0.0, 5.6),
                 (26.6, 26.0, -4.0), (31.4, 28.6, -4.0), (26.6, 26.0, 4.0), (31.4, 28.6, 4.0)]], 'paint2', bevel=0.3, mirror=True)
        g.hull([(sx * x, y, z) for x, y, z in
                [(27.2, 26.1, -3.2), (30.8, 28.05, -3.2), (27.2, 26.1, 3.2), (30.8, 28.05, 3.2),
                 (27.2, 26.35, -3.2), (30.8, 28.3, -3.2), (27.2, 26.35, 3.2), (30.8, 28.3, 3.2)]], 'team', bevel=0.0, mirror=True)
        g.cyl((sx * 27.4, 23.75, 0), (sx * 21.0, 23.75, 0), 2.4, 8, 'steel', r2=1.6, bevel=0.05, mirror=True)    # nozzle toward the deck
        g.box((sx * 21.2 - 0.3, 23.15, -0.6), (sx * 21.2 + 0.3, 24.35, 0.6), 'lightr', bevel=0.0, mirror=True)
        for y in (8.0, 16.0):
            g.hull([(sx * x, yy, z) for x in (35.6 - y * 0.2, 36.8 - y * 0.2) for yy in (y, y + 1.6) for z in (-5.2, 5.2)], 'dark', bevel=0.05, mirror=True)
