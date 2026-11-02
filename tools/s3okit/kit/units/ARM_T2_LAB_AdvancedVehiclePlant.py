"""Advanced Vehicle Plant (ARM_T2_LAB_AdvancedVehiclePlant) - Arm T2 vehicle factory. Closed: a light domed rotunda
over the pad - a walled drum (cylinder1/2), a sloping team ring (cylinder3/4) and a hazard-crowned crest (cylinder5/6),
each split down the middle - between four leaning corner pylons. On activation the halves of all three tiers slide
~27 apart (move x), the cap halves swing ~100 deg round on their pivots (turn y) and the nano arms (nano1/nano2) swing
out of the mid ring's cut faces to aim over the pad.
Arm lab family (T2 = taller, more parts): light chamfered blocks, team bands, dark lane with hazard edges, light round
pad, cyan lights. Identity from above (open): two light half-domes with team rings either side of a dark lane and a
wide light disc (the T1 vehicle plant is a hall whose halves lie flat as hazard-framed team slabs).
Every tier slice is a convex frustum slice of the rotunda (centre x 0.85, z -8.5) clipped at the split plane.
The script parks the open halves 5 elmo inside the yardmap lane edge (x +-32), as in TA; the pad area is clear.
Pieces (COB): base, cylinder1..6 (move x; 5/6 also turn y), nano1/2 (turn z), beam1/2 (empty nano emit points),
pad (spin y; QueryBuildInfo). Side 2 pieces are mirror clones of side 1.
Preview: OPEN (activatescr end state; COB z turns and x moves negated for the engine frame).
Coordinates are ENGINE/global: X right, Y up, Z forward."""
import math

UNIT = dict(
    res=2048,
    hazard_period=5.0,
    always_visible=['nano1', 'nano2'],
    wreck=dict(seed=75, drop=['cylinder6']),
    preview_pose={
        'cylinder1': {'move': (-27.125, 0, 0)}, 'cylinder2': {'move': (25.875, 0, 0)},
        'cylinder3': {'move': (-27.375, 0, 0)}, 'cylinder4': {'move': (26.375, 0, 0)},
        'cylinder5': {'move': (-27.25, 0, 0), 'rot': (0, 96.75, 0)},
        'cylinder6': {'move': (25.875, 0, 0), 'rot': (0, 100.34, 0)},
        'nano1': (0, 0, 117.0), 'nano2': (0, 0, -117.0),
    },
)

CX, CZ = 0.85, -8.5  # rotunda centre
R0 = 25.5


def _clip(poly, a, b, c):
    out = []
    for i in range(len(poly)):
        p, q = poly[i], poly[(i + 1) % len(poly)]
        fp, fq = a * p[0] + b * p[1] - c, a * q[0] + b * q[1] - c
        if fp <= 0:
            out.append(p)
        if fp * fq < 0:
            t = fp / (fp - fq)
            out.append((p[0] + t * (q[0] - p[0]), p[1] + t * (q[1] - p[1])))
    return out


def ring(r, n=40):
    return [(CX + r * math.cos(2 * math.pi * (i + 0.5) / n), CZ + r * math.sin(2 * math.pi * (i + 0.5) / n))
            for i in range(n)]


def slice_(bld, y0, y1, r0, r1, mat, bevel=0.25, n=40, cut=CX - 0.15, zband=None):
    """the -x half (x <= cut) of a frustum of the rotunda, optionally limited to a z band (z0, z1)"""
    lo, hi = _clip(ring(r0, n), 1, 0, cut), _clip(ring(r1, n), 1, 0, cut)
    if zband:
        for pl in ((0, 1, zband[1]), (0, -1, -zband[0])):
            lo, hi = _clip(lo, *pl), _clip(hi, *pl)
    bld.hull([(x, y0, z) for x, z in lo] + [(x, y1, z) for x, z in hi], mat, bevel=bevel)


def build(k):
    # ------------------------------------------------------------------ base: lane, corner pylons
    b = k.piece('base')
    b.box((-32.0, 0.0, -48.0), (32.0, 0.3, 48.0), 'paint2', bevel=0.05)
    b.box((-32.0, 0.0, -48.0), (-28.6, 0.45, 48.0), 'hazard', bevel=0.04, mirror=True)
    b.box((-48.0, 0.0, -36.0), (-32.0, 0.35, 20.0), 'dark', bevel=0.05, mirror=True)        # slide beds
    for zs in (1, -1):
        zc = 40.0 * zs
        b.hull([(x, 0.0, z) for x in (-48.0, -35.0) for z in (zc - 7.0, zc + 7.0)]
               + [(x, 18.0, z) for x in (-46.0, -37.0) for z in (zc - 5.0, zc + 5.0)], 'paint', bevel=0.35, mirror=True)
        b.box((-45.6, 17.9, zc - 4.6), (-37.4, 18.5, zc + 4.6), 'team', bevel=0.06, mirror=True)
        b.box((-35.6, 7.0, zc - 2.0), (-35.2, 8.4, zc + 2.0), 'lightc', bevel=0.0, mirror=True)
    for x in (-24.0, -12.0, 0.0, 12.0, 24.0):
        b.box((x - 1.0, 0.25, 47.4), (x + 1.0, 0.6, 47.8), 'lightc', bevel=0.0)

    # ------------------------------------------------------------------ rotunda halves (built for side 1, -x)
    c1 = k.piece('cylinder1')                                                 # drum
    slice_(c1, 0.0, 2.2, R0 + 0.8, R0 + 0.8, 'paint2', bevel=0.15)
    slice_(c1, 2.2, 19.0, R0, R0, 'paint', bevel=0.35)
    slice_(c1, 9.0, 10.4, R0 + 0.2, R0 + 0.2, 'lightc', bevel=0.0)
    c1.box((CX - 0.5, 2.0, CZ - 16.0), (CX - 0.1, 17.0, CZ + 16.0), 'hazard', bevel=0.05)    # cut face stripes
    c3 = k.piece('cylinder3')                                                 # sloping ring
    slice_(c3, 18.9, 20.0, R0, R0 - 0.8, 'paint', bevel=0.2)
    slice_(c3, 20.0, 30.0, R0 - 0.8, 16.5, 'team', bevel=0.2)
    c5 = k.piece('cylinder5')                                 # cap: a crest strip (turns ~100 deg to lie along z)
    ZB = (-18.0, 0.0)
    slice_(c5, 29.9, 33.5, 16.5, 13.0, 'paint', bevel=0.25, zband=ZB)
    slice_(c5, 33.5, 37.5, 13.0, 6.0, 'hazard', bevel=0.15, zband=ZB)
    c5.cyl((-6.0, 37.4, -9.0), (-6.0, 39.0, -9.0), 1.4, 8, 'lightc')
    for a, bb in (('cylinder2', 'cylinder1'), ('cylinder4', 'cylinder3'), ('cylinder6', 'cylinder5')):
        k.clone(a, bb, mirror_x=True)
    # nano arm (nano1 origin -9.4, 30, -9.25) hangs inside the ring at rest; beam1 at (-1.97, -8.17, 0)
    n = k.piece('nano1'); N = n.at
    n.box(N(-1.6, -2.6, -3.0), N(9.0, 0.0, 3.0), 'dark', bevel=0.25)
    n.box(N(-0.6, -0.1, -2.4), N(8.4, 0.3, 2.4), 'hazard', bevel=0.04)
    n.box(N(-3.0, -7.0, -2.6), N(1.6, -2.4, 2.6), 'steel', bevel=0.3)
    n.cyl(N(-1.4, -6.8, 0), N(-1.97, -8.17, 0), 1.2, 10, 'lightc')
    k.clone('nano2', 'nano1', mirror_x=True)

    # ------------------------------------------------------------------ pad (origin 0, 0.5, -10)
    p = k.piece('pad'); Pp = p.at
    p.cyl(Pp(0, -0.2, 0), Pp(0, 0.35, 0), 25.0, 44, 'dark', bevel=0.12)
    p.cyl(Pp(0, 0.35, 0), Pp(0, 0.47, 0), 22.8, 44, 'paint')
    p.cyl(Pp(0, 0.45, 0), Pp(0, 0.55, 0), 4.2, 16, 'paint2')
    for a in range(8):                                     # direction ticks round the rim
        t = a * math.pi / 4
        p.box(Pp(20.0 * math.cos(t) - 0.8, 0.45, 20.0 * math.sin(t) - 0.8),
              Pp(20.0 * math.cos(t) + 0.8, 0.6, 20.0 * math.sin(t) + 0.8), 'paint2', bevel=0.0)
