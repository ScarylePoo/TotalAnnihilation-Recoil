"""Galactic Gate (CORE_GalacticGate) - Core campaign objective, a static "space teleporter". TA's layout kept: a
hexagonal core block braced by four splayed outrigger legs on heavy feet, a dark neck carrying a horizontal steel
drum with glowing cyan field panels front and back and a team deck on top, and a long steel projector cone pointing
forward with a cyan emitter tip.
Identity from above: a dark X of four legs with team-capped feet round a team bar (the drum deck) and a bright cone
pointing forward (the Arm gate is a light dome with a block in front).
Pieces (TA corgate): base (block + drum), legs (outriggers, static structure, not a walker), gun (neck + projector),
beam (empty emit point at the tip), arms (drum end caps), platform (top deck), disha/dishb (rear/front field panels).
No baseplate. Coordinates are ENGINE/global: X right, Y up, Z forward."""
import math

UNIT = dict(
    wreck=dict(seed=107, drop=['platform']),
    preview_pose={},
    hazard_period=5,
)

DRY, DRR = 29.5, 6.6     # drum axis height and radius (axis along X)
DRX = 11.5               # drum half length (end caps beyond)


def rot2(cx, cz, w, l, ang):
    """rectangle w (across) x l (along) centred at (cx, cz), long axis at angle ang (radians, from +X toward +Z)"""
    ux, uz = math.cos(ang), math.sin(ang)
    vx, vz = -uz, ux
    return [(cx + ux * a + vx * b_, cz + uz * a + vz * b_) for (a, b_) in
            ((-l / 2, -w / 2), (l / 2, -w / 2), (l / 2, w / 2), (-l / 2, w / 2))]


def build(k):
    b = k.piece('base')
    hexa = lambda r: [(r * math.cos(i * math.pi / 3), r * math.sin(i * math.pi / 3)) for i in range(6)]
    b.plan(0.0, 6.0, hexa(16.0), 'paint2', bevel=0.35, top_inset=1.0)
    b.plan(5.9, 13.0, hexa(14.0), 'paint', bevel=0.35, top_inset=3.5)
    # drum
    b.cyl((-DRX, DRY, 0.0), (DRX, DRY, 0.0), DRR, 16, 'steel', rot=math.pi / 16, bevel=0.15)
    for x in (-6.0, 0.0, 6.0):
        b.cyl((x - 0.6, DRY, 0.0), (x + 0.6, DRY, 0.0), DRR + 0.35, 16, 'dark', rot=math.pi / 16)
    b.box((-1.4, 1.2, -16.0 * math.sin(math.pi / 3) - 0.3), (1.4, 2.8, -16.0 * math.sin(math.pi / 3) + 0.1), 'lightr',
          bevel=0.0)

    # ------------------------------------------------------------------ outrigger legs + feet (built -x, mirrored)
    lg = k.piece('legs')
    for sz in (-1, 1):
        ang = math.atan2(sz * 20.0, -25.0)
        fx, fz = -25.5, sz * 20.0
        hx, hz = -9.0, sz * 7.0
        # tapering strut from the block to the foot
        pts = []
        for (x, z, y0, y1, w) in ((hx, hz, 2.0, 10.0, 4.2), (fx * 0.85, fz * 0.85, 1.0, 6.5, 3.0)):
            ux, uz = -math.sin(ang), math.cos(ang)
            for v in (-w, w):
                for y in (y0, y1):
                    pts.append((x + ux * v, y, z + uz * v))
        lg.hull(pts, 'paint2', bevel=0.3, mirror=True)
        # warning band across the strut
        mx, mz = (hx + fx * 0.85) / 2 - 1.5, (hz + fz * 0.85) / 2 + sz * 1.2
        lg.plan(1.0, 9.0, rot2(mx, mz, 7.6, 3.2, ang), 'hazard', bevel=0.1, top_inset=0.6, mirror=True)
        # foot
        lg.plan(0.0, 7.0, rot2(fx, fz, 9.0, 10.5, ang), 'paint', bevel=0.35, top_inset=1.8, mirror=True)
        lg.plan(6.95, 7.4, rot2(fx, fz, 6.0, 7.0, ang), 'team', bevel=0.0, mirror=True)
        lg.plan(0.0, 2.2, rot2(fx, fz, 10.6, 12.0, ang), 'dark', bevel=0.2, mirror=True)

    # ------------------------------------------------------------------ neck + projector cone (gun)
    g = k.piece('gun')
    g.cyl((0.0, 12.0, 0.0), (0.0, DRY - DRR + 1.0, 0.0), 5.4, 6, 'dark', rot=math.pi / 6, bevel=0.2)
    g.cyl((0.0, 15.0, -1.0), (0.0, 23.0, -1.0), 6.6, 6, 'paint2', r2=5.8, rot=math.pi / 6, bevel=0.2)
    g.cyl((0.0, 19.5, 4.0), (0.0, 19.5, 9.0), 6.2, 8, 'paint2', rot=math.pi / 8, bevel=0.2)
    g.cyl((0.0, 19.5, 8.9), (0.0, 19.5, 26.5), 5.2, 8, 'steel', r2=1.7, rot=math.pi / 8, bevel=0.1)
    for a in (0, 90, 180, 270):          # four fins along the cone
        ar = math.radians(a + 45)
        ux, uy = math.cos(ar), math.sin(ar)
        pts = []
        for (z, r0, r1) in ((9.5, 4.0, 8.4), (20.0, 2.6, 3.6)):
            for (r, t) in ((r0, -0.5), (r0, 0.5), (r1, -0.5), (r1, 0.5)):
                pts.append((ux * r - uy * t, 19.5 + uy * r + ux * t, z))
        g.hull(pts, 'dark', bevel=0.0)
    g.cyl((0.0, 19.5, 6.0), (0.0, 19.5, 7.6), 6.9, 8, 'lightc', rot=math.pi / 8)
    g.cyl((0.0, 19.5, 26.4), (0.0, 19.5, 28.4), 1.9, 8, 'lightc', r2=0.9, rot=math.pi / 8)

    # ------------------------------------------------------------------ drum end caps (arms; origin x = -13)
    a = k.piece('arms')
    for sx in (-1, 1):
        a.cyl((sx * (DRX - 0.2), DRY, 0.0), (sx * (DRX + 1.6), DRY, 0.0), DRR + 1.2, 8, 'paint', rot=math.pi / 8,
              bevel=0.25)
        a.cyl((sx * (DRX + 1.5), DRY, 0.0), (sx * (DRX + 2.2), DRY, 0.0), 3.4, 8, 'lightc', rot=math.pi / 8)

    # ------------------------------------------------------------------ top deck (platform)
    p = k.piece('platform')
    p.box((-DRX + 0.5, DRY + DRR - 1.0, -4.6), (DRX - 0.5, DRY + DRR + 0.9, 4.6), 'paint', bevel=0.3)
    p.box((-DRX + 1.5, DRY + DRR + 0.85, -3.8), (DRX - 1.5, DRY + DRR + 1.25, 3.8), 'team', bevel=0.0)

    # ------------------------------------------------------------------ field panels on the drum (disha rear, dishb front)
    for name, sz in (('disha', -1), ('dishb', 1)):
        f = k.piece(name)
        for x0 in (-10.0, 1.0):
            f.hull([(x, y, sz * z) for x in (x0, x0 + 9.0) for (y, z) in ((DRY - 4.2, DRR - 1.4), (DRY + 3.6, DRR - 1.4),
                                                                         (DRY - 4.2, DRR + 0.6), (DRY + 3.6, DRR + 0.6))],
                   'dark', bevel=0.15)
            f.hull([(x, y, sz * (DRR + 0.75)) for x in (x0 + 1.0, x0 + 8.0) for y in (DRY - 3.2, DRY + 2.6)] +
                   [(x, y, sz * (DRR + 0.55)) for x in (x0 + 1.0, x0 + 8.0) for y in (DRY - 3.2, DRY + 2.6)],
                   'lightc', bevel=0.0)
