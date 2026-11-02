"""Vehicle Plant (CORE_T1_LAB_VehiclePlant) - Core T1 vehicle factory, built to the third-party rotunda remodel's piece
layout (its COB drives it). Closed: a dark armoured rotunda (r 29, centre z 15.5) in three tiers - a walled drum
(bottom1/2/3), an ochre-banded sloping ring (mid1/2/3) and a team cap (top1/2/3) - between two tall back towers and
two front pylons. Open (`Open`, called from Activate): each tier turns on y (top -90, mid +90, bottom 180) and splits,
so the outer slices of all three tiers reassemble as two half-rotundas sliding apart to x +-(21..42) and the centre
slices stack into a spine sliding back to z -44..-3; the bays on the mid spine swing out and the four nano heads aim
at the pad, which moves forward 10 on StartBuilding.
Core lab family: dark warm armour, corner pylons/towers with team caps, near-black lane with ochre hazard edges, light
steel pad disc, warm lights. Identity from above (open): two dark half-domes with team caps and ochre rings either
side of a dark lane and a light disc (the Arm vehicle plant is a light hall whose halves lie flat).
Every tier slice is a convex frustum slice (`dome_slice`) clipped to its piece's rest region.
Pieces: base (empty root), body (static), bottom/mid/top (empty tier pivots), bottom1..3, mid1..3, top1..3, fan1..3
(spin), door1/2, bay1a/1b/2a/2b, turret1..4, nano1..4, beam1..4 (empty emit points), strobe (empty), pad (QueryBuildInfo).
Preview: OPEN + building (Open end state, pad +10; COB z turns and x moves negated for the engine frame).
Coordinates are ENGINE/global: X right, Y up, Z forward."""
import math

UNIT = dict(
    res=2048,
    hazard_period=5.0,
    flipped=[],
    always_visible=['bay1a', 'bay1b', 'bay2a', 'bay2b', 'turret1', 'turret2', 'turret3', 'turret4',
                    'nano1', 'nano2', 'nano3', 'nano4', 'door1', 'door2', 'pad'],
    wreck=dict(seed=64, drop=['top1']),
    preview_pose={
        'top': (0, -90, 0), 'mid': (0, 90, 0), 'bottom': (0, 180, 0),
        'top1': {'move': (0, 0, 13.0)}, 'top3': {'move': (0, 0, -13.0)}, 'top2': {'move': (-30.869, 0, 0)},
        'mid1': {'move': (0, 0, -13.0)}, 'mid3': {'move': (0, 0, 13.0)}, 'mid2': {'move': (30.869, 0, 0)},
        'bottom1': {'move': (13.0, 0, 0)}, 'bottom3': {'move': (-13.0, 0, 0)}, 'bottom2': {'move': (0, 0, 30.869)},
        'bay1a': {'move': (0, 0, 7.777), 'rot': (0, -90, 0)}, 'bay2a': {'move': (0, 0, -7.777), 'rot': (0, 90, 0)},
        'door1': (0, -180, 0), 'door2': (0, 180, 0),
        'turret1': {'move': (0, 0, 6.0)}, 'turret4': {'move': (0, 0, -6.0)},
        'bay1b': (0, -135, 0), 'bay2b': (0, 135, 0),
        'turret2': {'move': (-2.4, 0, 0)}, 'turret3': {'move': (-2.4, 0, 0)},
        'nano2': (0, 90, 10), 'nano3': (0, -90, 10), 'nano1': (15, 0, 0), 'nano4': (-15, 0, 0),
        'pad': {'move': (0, 0, 10.0)},
    },
)

CZ = 15.5            # rotunda centre z
B0, B1 = 0.1, 10.6   # bottom tier
M0, M1 = 10.6, 20.0  # mid tier
T0, T1 = 20.0, 24.7  # top tier
R0, RM, RT = 29.0, 23.0, 14.0


def _clip(poly, a, b, c):
    """keep the part of a convex polygon [(x, z)] with a*x + b*z <= c"""
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
    return [(r * math.cos(2 * math.pi * i / n), CZ + r * math.sin(2 * math.pi * i / n)) for i in range(n)]


def dome_slice(bld, y0, y1, r0, r1, planes, mat, bevel=0.2, n=40):
    """convex frustum slice of the rotunda between y0 (radius r0) and y1 (radius r1), clipped by half-planes
    (a, b, c): a*x + b*z <= c, all in global rest coordinates"""
    lo, hi = ring(r0, n), ring(r1, n)
    for pl in planes:
        lo, hi = _clip(lo, *pl), _clip(hi, *pl)
    if len(lo) < 3 or len(hi) < 3:
        return
    bld.hull([(x, y0, z) for x, z in lo] + [(x, y1, z) for x, z in hi], mat, bevel=bevel)


def build(k):
    # ------------------------------------------------------------------ body: static floor, towers, pylons
    b = k.piece('body')
    b.box((-50.0, 0.0, -50.0), (50.0, 0.2, 50.0), 'dark', bevel=0.05)
    b.box((-24.0, 0.0, -9.0), (24.0, 0.32, 52.0), 'paint2', bevel=0.05)                       # lane floor
    b.box((-24.0, 0.0, -9.0), (-20.4, 0.46, 52.0), 'hazard', bevel=0.04, mirror=True)        # lane edges
    b.box((-8.6, 0.0, -48.0), (8.6, 0.3, -9.0), 'paint2', bevel=0.05)                        # spine channel
    # back towers either side of the spine channel
    b.plan(0.0, 16.0, [(-23.0, -49.0), (-10.0, -49.0), (-10.0, -15.0), (-23.0, -15.0)], 'paint', bevel=0.35,
           top_inset=1.4, mirror=True)
    b.hull([(x, y, z) for x, z in ((-21.6, -47.0), (-11.4, -47.0), (-11.4, -18.0), (-21.6, -18.0)) for y in (15.0,)]
           + [(x, 28.4, z) for x, z in ((-20.0, -45.0), (-13.0, -45.0), (-13.0, -21.0), (-20.0, -21.0))],
           'paint', bevel=0.3, mirror=True)
    b.box((-19.6, 28.3, -44.6), (-13.4, 28.9, -21.4), 'team', bevel=0.1, mirror=True)
    b.box((-10.1, 6.0, -44.0), (-9.8, 7.2, -20.0), 'lightw', bevel=0.0, mirror=True)
    # outer back blocks (o cells behind the half-domes)
    b.plan(0.0, 9.0, [(-40.0, -40.0), (-25.0, -40.0), (-25.0, -20.0), (-40.0, -20.0)], 'paint2', bevel=0.3,
           top_inset=1.0, mirror=True)
    b.box((-38.6, 8.9, -38.6), (-26.4, 9.4, -21.4), 'team', bevel=0.08, mirror=True)
    # front pylons (strobe light at -44.3, 14.5, 32.9)
    b.plan(0.0, 12.0, [(-50.0, 33.0), (-38.0, 33.0), (-38.0, 48.0), (-50.0, 48.0)], 'paint', bevel=0.3,
           top_inset=1.4, mirror=True)
    b.hull([(x, 11.0, z) for x, z in ((-48.6, 34.4), (-39.4, 34.4), (-39.4, 46.6), (-48.6, 46.6))]
           + [(x, 24.0, z) for x, z in ((-47.0, 37.0), (-41.0, 37.0), (-41.0, 44.0), (-47.0, 44.0))],
           'paint', bevel=0.3, mirror=True)
    b.box((-46.6, 23.9, 37.4), (-41.4, 24.5, 43.6), 'team', bevel=0.08, mirror=True)
    b.box((-46.0, 13.8, 32.6), (-42.6, 15.2, 33.0), 'lightr', bevel=0.0, mirror=True)

    # ------------------------------------------------------------------ rotunda slices
    X_HI, X_LO = (1, 0, 7.8), (-1, 0, 7.8)           # x <= 7.8, x >= -7.8
    Z_FRONT, Z_BACK = (0, -1, -23.3), (0, 1, 7.7)    # z >= 23.3, z <= 7.7
    Z_MID = [(0, 1, 23.3), (0, -1, -7.7)]

    def drum(piece, planes):
        p = k.piece(piece)
        dome_slice(p, B0, 2.0, R0 + 0.6, R0 + 0.6, planes, 'paint2', bevel=0.15)             # plinth ring
        dome_slice(p, 2.0, B1, R0, R0, planes, 'paint', bevel=0.3)
        dome_slice(p, 6.4, 7.6, R0 + 0.15, R0 + 0.15, planes, 'lightw', bevel=0.0)            # warm light band
        return p

    def ring_tier(piece, planes):
        p = k.piece(piece)
        dome_slice(p, M0, 13.0, R0, R0 - 1.5, planes, 'paint', bevel=0.2)
        dome_slice(p, 13.0, 17.6, R0 - 1.5, RM + 1.5, planes, 'hazard', bevel=0.1)
        dome_slice(p, 17.6, M1, RM + 1.5, RM, planes, 'paint', bevel=0.2)
        return p

    def cap(piece, planes):
        p = k.piece(piece)
        dome_slice(p, T0, 22.0, RM, RM - 2.0, planes, 'paint', bevel=0.2)
        dome_slice(p, 22.0, T1, RM - 2.0, RT, planes, 'team', bevel=0.15)
        return p

    drum('bottom1', [(-1, 0, -7.8)])
    k.clone('bottom3', 'bottom1', mirror_x=True)
    drum('bottom2', [X_HI, X_LO, (0, -1, -3.1)])
    ring_tier('mid1', [Z_BACK])
    ring_tier('mid3', [Z_FRONT])
    m2 = ring_tier('mid2', Z_MID + [(-1, 0, 1.9)])
    m2.box((-12.6, M0, 7.7), (-12.4, M1, 23.3), 'black', bevel=0.0)                          # bay backdrop
    cap('top1', [Z_FRONT])
    cap('top3', [Z_BACK])
    cap('top2', Z_MID + [(1, 0, 12.4)])

    # fans: vent discs on the drum walls (fan1 on bottom1's outer wall, spin x; fan2 on bottom2's front, spin z)
    f = k.piece('fan1'); F = f.at
    f.cyl(F(10.6, 0, 0), F(11.7, 0, 0), 4.0, 16, 'black')
    for a in range(3):
        t = a * math.pi / 3
        f.box(F(11.6, -3.6 * math.cos(t) - 0.5, -3.6 * math.sin(t) - 0.5), F(11.9, 3.6 * math.cos(t) + 0.5,
              3.6 * math.sin(t) + 0.5), 'steel', bevel=0.0)
    k.clone('fan3', 'fan1', mirror_x=True)
    g = k.piece('fan2'); G = g.at
    g.cyl(G(0, 0, 28.8), G(0, 0, 29.9), 4.0, 16, 'black')
    for a in range(3):
        t = a * math.pi / 3
        g.box(G(-3.8 * math.cos(t) - 0.5, -3.8 * math.sin(t) - 0.5, 29.8),
              G(3.8 * math.cos(t) + 0.5, 3.8 * math.sin(t) + 0.5, 30.1), 'steel', bevel=0.0)

    # doors: walls of the bay slot
    for nm, z0, z1 in (('door1', 5.9, 7.6), ('door2', 23.4, 25.1)):
        d = k.piece(nm)
        d.box((-7.4, 11.0, z0), (7.4, 19.6, z1), 'paint2', bevel=0.15)

    # bays (fill the slot x -12.4..-1.9 of the mid spine)
    for nm, z0, z1 in (('bay1a', 7.8, 11.55), ('bay1b', 11.65, 15.45), ('bay2a', 19.45, 23.2), ('bay2b', 15.55, 19.35)):
        d = k.piece(nm)
        d.box((-12.3, 10.8, z0), (-2.0, 19.8, z1), 'dark', bevel=0.2)
        d.box((-11.8, 19.7, z0 + 0.4), (-2.5, 20.1, z1 - 0.4), 'hazard', bevel=0.05)

    # turrets + nano heads
    for nm, z in (('turret1', 0.0), ('turret4', 31.0)):
        t = k.piece(nm)
        t.cyl((0, 10.9, z), (0, 14.0, z), 1.9, 10, 'dark', bevel=0.1)
    for nm, sz in (('nano1', 1), ('nano4', -1)):
        n = k.piece(nm); N = n.at
        n.box(N(-1.8, -1.6, -1.8), N(1.8, 1.6, 1.8), 'steel', bevel=0.25)
        n.cyl(N(0, 0, 1.6 * sz), N(0, 0, 4.6 * sz), 1.2, 10, 'dark', r2=0.9)
        n.cyl(N(0, 0, 4.5 * sz), N(0, 0, 5.5 * sz), 0.95, 10, 'lightc')
    for nm in ('turret2', 'turret3'):
        t = k.piece(nm); T = t.at
        t.box(T(-1.9, -1.9, -1.9), T(1.9, 1.9, 1.9), 'dark', bevel=0.2)
    for nm in ('nano2', 'nano3'):
        n = k.piece(nm); N = n.at
        n.box(N(-2.4, -1.9, -2.2), N(1.8, 1.9, 2.2), 'steel', bevel=0.25)
        n.cyl(N(-2.2, 0, 0), N(-6.4, 0, 0), 1.3, 10, 'dark', r2=0.9)
        n.cyl(N(-6.3, 0, 0), N(-7.5, 0, 0), 1.0, 10, 'lightc')

    # pad (origin 0, 0, 24.5): flat build disc, moves +10 forward while building
    p = k.piece('pad'); Pp = p.at
    p.cyl(Pp(0, 0.2, 0), Pp(0, 0.6, 0), 16.0, 36, 'dark', bevel=0.1)
    p.cyl(Pp(0, 0.6, 0), Pp(0, 0.72, 0), 14.0, 36, 'steel')
    for a in range(4):
        t = math.radians(a * 90 + 45)
        p.hull([Pp(r * math.cos(t + dt), yy, r * math.sin(t + dt)) for r in (14.1, 15.7) for dt in (-0.2, 0.2)
                for yy in (0.55, 0.7)], 'hazard', bevel=0.0)
