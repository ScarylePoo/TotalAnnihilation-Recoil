"""Advanced Radar Tower (CORE_T2_DEF_AdvancedRadar) - Core long-range radar. A tall tapered pylon on a wide footing; on
top a spinning collar carries a bent crane arm that swings out to the right and holds a big octagonal dish on a
side axle above the pylon. Switched on, the collar spins (y) and the dish tumbles on its axle (spin x).
Identity from above: a big light steel octagon (the dish face) with a team hub, a dark crooked arm beside it, over a
dark square footing with team corner pads - taller and heavier than the T1 Core radar's stepped mast.
Pieces (COB): base, turret (spin y), dish (spin x). The preview tilts the dish 55 deg so its face shows from above
(it tumbles in game, so both faces get a team hub).
Coordinates are ENGINE/global: X right, Y up, Z forward."""
import math

UNIT = dict(
    res=1024,
    wreck=dict(seed=23, drop=['dish']),
    preview_pose={'turret': (0, -20, 0), 'dish': (-55, 0, 0)},
)


def octagon(r, rot=math.pi / 8):
    return [(r * math.cos(rot + i * math.pi / 4), r * math.sin(rot + i * math.pi / 4)) for i in range(8)]


def build(k):
    # ------------------------------------------------------------------ base: footing + tapered pylon
    b = k.piece('base')
    b.plan(0.0, 2.4, [(-15.4, -15.4), (15.4, -15.4), (15.4, 15.4), (-15.4, 15.4)], 'paint2', bevel=0.25, top_inset=0.8)
    b.plan(2.2, 8.0, [(-12.4, -12.4), (12.4, -12.4), (12.4, 12.4), (-12.4, 12.4)], 'paint', bevel=0.3, top_inset=3.2)
    # team corner pads on the footing
    for s in (-1, 1):
        for t in (-1, 1):
            b.box((min(10.0 * s, 14.6 * s), 2.0, min(10.0 * t, 14.6 * t)), (max(10.0 * s, 14.6 * s), 3.2, max(10.0 * t, 14.6 * t)),
                  'team', bevel=0.06)
    # pylon (octagonal, tapering) with dark corner ribs
    b.hull([(x, y, z) for y, r in ((7.0, 9.4), (50.0, 5.4)) for x, z in octagon(r)], 'paint', bevel=0.3)
    for i in range(4):
        a = math.pi / 4 + i * math.pi / 2
        c, s_ = math.cos(a), math.sin(a)
        b.hull([(c * r + (-s_) * w, y, s_ * r + c * w) for y, r in ((7.0, 9.6), (49.0, 5.7)) for w in (-1.2, 1.2)] +
               [(c * (r - 1.6), y, s_ * (r - 1.6)) for y, r in ((7.0, 9.6), (49.0, 5.7))], 'dark', bevel=0.06)
    # bracing bands and the head collar
    for y in (20.0, 34.0):
        r = 9.4 - (y - 7.0) / 43.0 * 4.0 + 0.5
        b.hull([(x, yy, z) for yy in (y, y + 2.0) for x, z in octagon(r)], 'paint2', bevel=0.12)
    b.hull([(x, y, z) for y, r in ((49.0, 6.6), (55.8, 6.0)) for x, z in octagon(r)], 'paint2', bevel=0.15)
    b.box((-1.0, 28.0, 7.2), (1.0, 29.6, 7.8), 'lightr', bevel=0.0)

    # ------------------------------------------------------------------ turret: spinning collar + crane arm (origin 0, 56, 0)
    t = k.piece('turret'); A = t.at
    t.cyl(A(0, -1.0, 0), A(0, 3.4, 0), 7.4, 12, 'dark', bevel=0.1)
    t.cyl(A(0, 3.4, 0), A(0, 5.0, 0), 5.4, 12, 'paint2', bevel=0.08)
    # arm: three segments, up and out to the right, then up to the axle at x 18.5
    def seg(p0, p1, w, h, mat):
        (x0, y0), (x1, y1) = p0, p1
        t.hull([A(x, y + dy, z) for x, y in ((x0, y0), (x1, y1)) for dy in (-h, h) for z in (-w, w)], mat, bevel=0.2)
    seg((0.0, 4.0), (10.0, 12.0), 3.2, 2.4, 'paint')
    seg((9.0, 11.0), (21.0, 23.0), 2.8, 2.2, 'paint')
    t.hull([A(x, y, z) for x, y in ((18.6, 20.0), (23.6, 21.4), (18.8, 33.4), (23.0, 33.4)) for z in (-2.6, 2.6)], 'paint', bevel=0.2)
    # team strip along the top of the middle segment
    t.hull([A(x, y + dy, z) for x, y in ((10.6, 13.9), (19.8, 23.2)) for dy in (0.0, 0.2) for z in (-2.0, 2.0)], 'team', bevel=0.0)
    t.cyl(A(9.6, 11.6, -3.6), A(9.6, 11.6, 3.6), 2.6, 8, 'steel', bevel=0.05)        # elbow
    t.box(A(23.0, 30.0, -0.6), A(24.2, 31.4, 0.6), 'lightr', bevel=0.0)

    # ------------------------------------------------------------------ dish (origin 18.5, 87, 0): axle + octagon at local x -20.5
    d = k.piece('dish'); D = d.at
    d.cyl(D(1.0, 0, 0), D(-7.6, 0, 0), 1.8, 8, 'steel', bevel=0.04)
    cx = -20.5
    ring = octagon(14.2); inner = octagon(11.6); hub = octagon(7.8)
    d.hull([D(cx + x, y, z) for x, y in ring for z in (-1.4, 1.4)], 'dark', bevel=0.15)                  # rim
    d.hull([D(cx + x, y, z) for x, y in inner for z in (1.25, 1.9)], 'steel', bevel=0.1)                  # front face
    d.hull([D(cx + x, y, z) for x, y in inner for z in (-1.9, -1.25)], 'paint2', bevel=0.1)               # back face
    d.hull([D(cx + x, y, z) for x, y in hub for z in (1.8, 2.05)], 'team', bevel=0.0)                     # team hubs
    d.hull([D(cx + x, y, z) for x, y in hub for z in (-2.05, -1.8)], 'team', bevel=0.0)
    # feed horn on the front face
    d.cyl(D(cx, 0, 2.0), D(cx, 0, 7.6), 1.4, 8, 'dark', r2=0.9, bevel=0.04)
    d.box(D(cx - 0.7, -0.7, 7.5), D(cx + 0.7, 0.7, 8.1), 'lightr', bevel=0.0)
    # axle boss on the dish rim
    d.cyl(D(-5.8, 0, 0), D(-7.8, 0, 0), 2.8, 8, 'dark', bevel=0.06)
