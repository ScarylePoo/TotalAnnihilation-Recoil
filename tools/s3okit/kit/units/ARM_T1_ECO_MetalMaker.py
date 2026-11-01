"""Metal Maker (ARM_T1_ECO_MetalMaker) - Arm metal maker. A hexagonal reactor housing holding a glowing cyan converter
sphere (rises 7 elmo out of its cradle when switched on), braced by three tall bent light pylons arching over to the
ground and three low dark capacitor blocks between them.
Identity from above: a six-spoke star - three long light spokes with team tops alternating with three short dark
ones - round a bright cyan dot (the Core maker is a dark block with a light arch over a glowing crystal).
Pieces (Lua script): base, sphere (move y -7 when off), pieces (capacitor blocks, explode only).
Preview: ON (sphere at 0).
Coordinates are ENGINE/global: X right, Y up, Z forward."""
import math

UNIT = dict(
    res=1024,
    wreck=dict(seed=21, drop=['sphere']),
    preview_pose={},
)


def radial(ang):
    a = math.radians(ang); d = (math.cos(a), math.sin(a)); p = (-d[1], d[0])
    return lambda u, v, y: (d[0] * u + p[0] * v, y, d[1] * u + p[1] * v)


def build(k):
    b = k.piece('base')
    hexa = lambda r: [(r * math.cos(i * math.pi / 3), r * math.sin(i * math.pi / 3)) for i in range(6)]
    b.plan(0.0, 2.4, hexa(12.0), 'paint2', bevel=0.2, top_inset=0.6)
    b.plan(2.3, 14.0, hexa(9.4), 'paint', bevel=0.3, top_inset=1.4)
    b.cyl((0, 13.9, 0), (0, 15.4, 0), 7.4, 12, 'dark', rot=math.pi / 12, bevel=0.1)
    b.cyl((0, 15.3, 0), (0, 15.6, 0), 5.4, 12, 'black')
    # three bent pylons (270 = -z built whole, 30 mirrored to 150)
    for ang, m in ((270, False), (30, True)):
        P = radial(ang)
        b.hull([P(u, v, y) for (u, y) in ((5.0, 14.0), (5.0, 21.0), (19.0, 23.6), (21.6, 21.6), (17.0, 15.6))
                for v in (-3.0, 3.0)], 'paint', bevel=0.3, mirror=m)
        b.hull([P(u, v, y) for (u, y) in ((16.8, 18.0), (22.4, 21.0), (24.4, 0.0), (19.0, 0.0)) for v in (-2.6, 2.6)],
               'paint', bevel=0.3, mirror=m)
        b.hull([P(u, v, 21.0 + (u - 5.0) * 2.6 / 14.0 + dy) for u in (6.6, 18.4) for v in (-2.2, 2.2)
                for dy in (0.08, 0.32)], 'team', bevel=0.0, mirror=m)
        b.hull([P(u, v, y) for (u, y) in ((18.4, 0.0), (25.6, 0.0), (18.4, 1.4), (25.6, 1.4)) for v in (-3.6, 3.6)],
               'dark', bevel=0.12, mirror=m)
        b.hull([P(u, v, y) for (u, y) in ((22.9, 6.0), (23.3, 6.0), (22.4, 14.0), (22.8, 14.0)) for v in (-0.7, 0.7)],
               'lightc', bevel=0.0, mirror=m)

    # ------------------------------------------------------------------ pieces: three low capacitor blocks
    p = k.piece('pieces')
    for ang, m in ((90, False), (330, True)):
        P = radial(ang)
        p.hull([P(u, v, y) for (u, y) in ((7.0, 0.0), (17.0, 0.0), (17.0, 3.0), (15.6, 11.0), (7.0, 12.0))
                for v in (-4.4, 4.4)], 'paint2', bevel=0.3, mirror=m)
        for u0 in (10.0, 13.2):
            p.hull([P(u, v, y) for u in (u0, u0 + 1.2) for v in (-4.7, 4.7) for y in (2.0, 11.2 - (u - 7.0) * 0.1)],
                   'dark', bevel=0.05, mirror=m)
        p.hull([P(u, v, y) for (u, y) in ((16.95, 4.0), (17.2, 4.0), (16.95, 7.0), (17.2, 7.0)) for v in (-2.4, 2.4)],
               'hazard', bevel=0.0, mirror=m)

    # ------------------------------------------------------------------ sphere: glowing converter in a cradle
    s = k.piece('sphere')
    s.sphere((0, 20.4, 0), 5.6, 'lightc', segs=12, rings=8)
    s.cyl((0, 14.8, 0), (0, 17.0, 0), 4.8, 12, 'dark', r2=5.6, rot=math.pi / 12, bevel=0.06)
    for ang, m in ((270, False), (30, True)):
        P = radial(ang)
        s.hull([P(u, v, y) for (u, y) in ((3.6, 16.0), (6.4, 16.0), (6.4, 21.4), (5.0, 23.4)) for v in (-0.9, 0.9)],
               'steel', bevel=0.1, mirror=m)
