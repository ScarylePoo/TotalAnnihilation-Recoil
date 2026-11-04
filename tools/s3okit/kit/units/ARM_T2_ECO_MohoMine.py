"""Moho Mine (ARM_T2_ECO_MohoMine) - Arm moho mine. A big two-tier light octagonal pad over the metal spot with four
dark loading bays, a tall tapered drill column, and a huge three-armed spinning extractor frame on top: each arm a
light box beam with a team top, ending in a dark drill leg that drops back toward the pad (an open loop with its
inner brace).
Identity from above: wide light octagon (much bigger than the T1 mex) under a three-armed team-striped 'Y' frame
with dark drill heads at its tips (the T1 Arm mex is a two-armed bar; the Core moho is a dark hexagon with a lid).
Pieces (COB): base, extractor (spin y; origin 0.06, 44.76, 1.52).
Coordinates are ENGINE/global: X right, Y up, Z forward."""
import math

UNIT = dict(
    wreck=dict(seed=31, drop=['extractor']),
    preview_pose={'extractor': (0, 20, 0)},
)


def octagon(r, rot=math.pi / 8):
    return [(r * math.cos(rot + i * math.pi / 4), r * math.sin(rot + i * math.pi / 4)) for i in range(8)]


def radial(ang, c=(0.0, 0.0)):
    a = math.radians(ang); d = (math.cos(a), math.sin(a)); p = (-d[1], d[0])
    return lambda u, v, y: (c[0] + d[0] * u + p[0] * v, y, c[1] + d[1] * u + p[1] * v)


def build(k):
    b = k.piece('base')
    b.plan(0.0, 4.0, octagon(40.0), 'paint2', bevel=0.35, top_inset=1.2)
    b.plan(3.9, 15.0, octagon(36.5), 'paint', bevel=0.4, top_inset=7.0)
    b.plan(14.9, 19.0, octagon(24.0), 'paint2', bevel=0.3, top_inset=1.6)
    # team plates on the four diagonal slopes (faces centred on 45/135/...)
    for ang in (45, 135, 225, 315):
        a = math.radians(ang); ox, oz = math.cos(a), math.sin(a); px, pz = -oz, ox
        ap = lambda y: (36.5 - (y - 3.9) / 11.1 * 7.0) * math.cos(math.pi / 8)
        b.hull([(ox * (ap(y) + d) + px * v, y + d * 0.6, oz * (ap(y) + d) + pz * v) for y in (5.0, 14.0)
                for v in (-9.0, 9.0) for d in (0.08, 0.35)], 'team', bevel=0.0)
    # team ring on the collar deck (team octagon under a smaller dark one)
    b.plan(18.95, 19.25, octagon(21.6), 'team', bevel=0.0)
    b.plan(19.2, 19.5, octagon(16.8), 'dark', bevel=0.0)
    # dark loading bays on the four cardinal faces
    for ang in (0, 90, 180, 270):
        P = radial(ang)
        b.hull([P(u, v, y) for (u, y) in ((25.0, 3.9), (40.0, 3.9), (40.0, 6.0), (28.0, 13.0), (25.0, 13.0))
                for v in (-6.0, 6.0)], 'paint2', bevel=0.3)
        b.hull([P(u, v, y) for (u, y) in ((39.9, 4.6), (40.2, 4.6), (39.9, 5.6), (40.2, 5.6)) for v in (-5.0, 5.0)],
               'hazard', bevel=0.0)
    # drill column
    b.cyl((0, 18.9, 1.52), (0, 41.0, 1.52), 9.6, 8, 'paint', r2=6.4, rot=math.pi / 8, bevel=0.25)
    for y in (24.0, 30.0, 36.0):
        r = 9.6 - (y - 18.9) / 22.1 * 3.2
        b.cyl((0, y, 1.52), (0, y + 1.6, 1.52), r + 0.4, 8, 'dark', rot=math.pi / 8, bevel=0.05)
    b.cyl((0, 40.8, 1.52), (0, 42.6, 1.52), 7.4, 12, 'dark', rot=math.pi / 12, bevel=0.1)
    b.box((-1.4, 1.0, 35.8), (1.4, 2.6, 36.9), 'lightc', bevel=0.0)

    # ------------------------------------------------------------------ extractor: three-armed loop frame
    e = k.piece('extractor'); E = e.at
    c = (k.P['extractor'][0], k.P['extractor'][2])
    yb = k.P['extractor'][1]
    e.cyl((c[0], yb - 2.4, c[1]), (c[0], yb + 4.0, c[1]), 7.0, 6, 'paint2', rot=math.pi / 6, bevel=0.2)
    e.cyl((c[0], yb + 3.9, c[1]), (c[0], yb + 5.0, c[1]), 4.0, 6, 'lightc', rot=math.pi / 6)
    for ang in (90, 210, 330):         # the origin is 0.06 off x = 0, so no mirroring: three arms built
        P = radial(ang, c); m = False
        e.hull([P(u, v, y) for u in (5.0, 33.0) for v in (-3.0, 3.0) for y in (yb - 1.6, yb + 2.6)], 'paint', bevel=0.3,
               mirror=m)
        e.hull([P(u, v, y) for u in (7.0, 30.0) for v in (-2.2, 2.2) for y in (yb + 2.55, yb + 2.85)], 'team', bevel=0.0,
               mirror=m)
        # drill leg at the tip, dropping toward the pad, and the inner brace closing the loop
        e.hull([P(u, v, y) for (u, y) in ((29.0, yb - 1.0), (35.0, yb + 2.6), (35.0, yb - 16.0), (31.0, yb - 18.0))
                for v in (-3.4, 3.4)], 'dark', bevel=0.25, mirror=m)
        e.cyl(P(33.0, 0, yb - 17.0), P(32.0, 0, yb - 21.0), 2.6, 8, 'steel', r2=0.8, mirror=m)
        e.hull([P(u, v, y) for (u, y) in ((9.0, yb - 1.4), (12.0, yb - 1.4), (30.0, yb - 15.0), (30.0, yb - 12.0))
                for v in (-1.2, 1.2)], 'paint2', bevel=0.12, mirror=m)
        e.hull([P(u, v, y) for (u, y) in ((34.9, yb - 4.0), (35.2, yb - 4.0), (34.9, yb - 8.0), (35.2, yb - 8.0))
                for v in (-1.0, 1.0)], 'lightc', bevel=0.0, mirror=m)
