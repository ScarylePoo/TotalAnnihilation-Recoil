"""Targeting Facility (ARM_T2_DEF_TargetingFacility) - Arm automatic radar targeting. A broad low cross-shaped deck with
a tall slim central mast topped by a white beacon, two radar domes on opposite corners joined by a conduit, and four
sensor posts lying flat on the deck arms. Switched on, the four posts swing up to vertical pylons (turn 90 deg) and
their cyan beacons slide out of the tips.
Identity from above: a light square deck with four team corner plates, a dark cross of posts (closed) or four
cyan-tipped pylons on the compass points (open), white dot in the middle, two light domes on a diagonal.
Pieces (COB): base, centerlight, post1..4 (turn x/z), light1..4 (move along the post). The preview shows the OPEN
state (posts up, beacons out).
Coordinates are ENGINE/global: X right, Y up, Z forward."""
import math

UNIT = dict(
    res=2048, bake_res=2048,          # no 2x supersampling: machine time (see the batch report)
    wreck=dict(seed=55, drop=['post2']),
    preview_pose={'post1': (-90, 0, 0), 'post2': (90, 0, 0), 'post3': (0, 0, 90), 'post4': (0, 0, -90),
                  'light1': {'move': (0, 0, 5.0)}, 'light2': {'move': (0, 0, -5.0)},
                  'light3': {'move': (5.125, 0, 0)}, 'light4': {'move': (-4.75, 0, 0)}},
)


def octagon(r, rot=math.pi / 8, cx=0.0, cz=0.0):
    return [(cx + r * math.cos(rot + i * math.pi / 4), cz + r * math.sin(rot + i * math.pi / 4)) for i in range(8)]


def post(k, name, light, u, sgn):
    """post lying flat on its deck arm: hinge at the outer end (piece origin), body toward the centre (u = 'x'|'z',
    sgn = direction from the hinge to the centre). Box 10 wide, 9 thick, 20 long; beacon at the tip."""
    p = k.piece(name); P = p.at

    def Q(a, y, w):        # a = along the post (toward centre), w = across
        return P(sgn * a, y, w) if u == 'x' else P(w, y, sgn * a)
    p.hull([Q(a, y, w) for a in (0.4, 19.6) for y in (0.2, 9.0) for w in (-4.6, 4.6)], 'paint', bevel=0.3)
    for a in (5.0, 12.0):
        p.hull([Q(aa, y, w) for aa in (a, a + 1.6) for y in (0.0, 9.2) for w in (-4.8, 4.8)], 'dark', bevel=0.06)
    p.hull([Q(a, y, w) for a in (2.0, 17.0) for y in (9.1, 9.3) for w in (-2.4, 2.4)], 'dark', bevel=0.0)
    p.cyl(Q(0.0, 4.6, -5.2), Q(0.0, 4.6, 5.2), 2.4, 8, 'steel', bevel=0.04)
    l = k.piece(light); L = l.at

    def R(a, y, w):
        return L(sgn * a, y, w) if u == 'x' else L(w, y, sgn * a)
    l.hull([R(a, y, w) for a in (-3.0, 4.2) for y in (-2.8, 2.8) for w in (-3.6, 3.6)], 'dark', bevel=0.15)
    l.hull([R(a, y, w) for a in (4.1, 5.2) for y in (-2.0, 2.0) for w in (-2.6, 2.6)], 'lightc', bevel=0.0)


def build(k):
    # ------------------------------------------------------------------ base: deck, mast, domes
    b = k.piece('base')
    b.plan(0.0, 2.2, [(-31.0, -26.0), (-26.0, -31.0), (26.0, -31.0), (31.0, -26.0), (31.0, 26.0), (26.0, 31.0),
                      (-26.0, 31.0), (-31.0, 26.0)], 'paint', bevel=0.3, top_inset=1.0)
    # deck arms (darker) under the posts
    for ux, uz in ((1, 0), (-1, 0), (0, 1), (0, -1)):
        lo = (min(ux * 6.0, ux * 30.0) if ux else -6.6, 2.0, min(uz * 6.0, uz * 30.0) if uz else -6.6)
        hi = (max(ux * 6.0, ux * 30.0) if ux else 6.6, 2.6, max(uz * 6.0, uz * 30.0) if uz else 6.6)
        b.box(lo, hi, 'paint2', bevel=0.12)
    # team corner plates
    for sx in (-1, 1):
        for sz in (-1, 1):
            b.hull([(sx * x, y, sz * z) for x, z in ((8.4, 8.4), (26.4, 8.4), (8.4, 26.4), (24.6, 17.4), (17.4, 24.6))
                    for y in (2.0, 2.45)], 'team', bevel=0.04)
    # central mast
    b.plan(2.0, 8.0, octagon(7.0), 'paint2', bevel=0.2, top_inset=1.2)
    b.hull([(x, y, z) for y, r in ((7.6, 4.6), (30.0, 3.4)) for x, z in octagon(r)], 'paint', bevel=0.2)
    for y in (14.0, 22.0):
        b.hull([(x, yy, z) for yy in (y, y + 1.6) for x, z in octagon(4.6 - (y - 7.6) * 0.054)], 'dark', bevel=0.06)
    # radar domes on the diagonal corners and the conduit between them via the mast
    for cx, cz in ((25.0, -25.0), (-25.0, 25.0)):
        b.plan(2.0, 4.0, octagon(6.0, cx=cx, cz=cz), 'dark', bevel=0.15)
        b.sphere((cx, 4.0, cz), 5.2, 'paint', segs=12, rings=5, scale=(1, 0.8, 1))
        b.cyl((cx, 7.9, cz), (cx, 8.25, cz), 2.0, 10, 'team')
        ex, ez = cx * 0.36, cz * 0.36
        b.cyl((cx - math.copysign(4.0, cx), 3.0, cz - math.copysign(4.0, cz)), (ex, 3.0, ez), 1.2, 6, 'dark')

    # ------------------------------------------------------------------ centerlight: white beacon on the mast
    c = k.piece('centerlight')
    c.hull([(x, 30.0, z) for x, z in octagon(3.4)] + [(0.0, 37.6, 0.0)], 'lightw', bevel=0.0)

    # ------------------------------------------------------------------ posts (hinges at the deck arm ends)
    post(k, 'post1', 'light1', 'z', 1)      # origin (0, 0, -25): lies toward +z
    post(k, 'post2', 'light2', 'z', -1)     # origin (0, 0, 25)
    post(k, 'post3', 'light3', 'x', 1)      # origin (-25, 0, 0)
    post(k, 'post4', 'light4', 'x', -1)     # origin (25, 0, 0)
