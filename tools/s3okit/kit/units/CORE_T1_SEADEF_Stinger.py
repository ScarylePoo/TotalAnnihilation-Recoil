"""Stinger (CORE_T1_SEADEF_Stinger) - Core floating missile tower. Waterline 20 (the water surface is model y = 20).
A heavy dark cross of four box pontoons (team tops, 4 elmo of freeboard) round an octagonal hub, a short tapering
ribbed tower and neck, and the land Pulverizer's big rounded helmet turret with three light steel missile tubes in a
triangle in its face (each tube kicks back 3 elmo on fire), team flanks and an ochre crest.
Identity from above: a dark plus sign with team arm ends and a big dark helmet with team flanks and three light tube
mouths at its centre (the Pulverizer stands on a tall obelisk; the Core Thunderbolt is a low raft with an offset
laser on its left side; the Arm sea Defender is four light drums round an X).
Pieces (Lua script): base (RockUnit turns x/z), turret (turn y, turn x; origin 0, 38, -3.75), barrel1 (top centre),
barrel2/3 (low sides; move z recoil), flare1..3 (emit, empty).
Coordinates are ENGINE/global: X right, Y up, Z forward."""
import math

WL = 20.0
UNIT = dict(
    res=1024,                  # 4x4, but 1024 like the land T1 defences (shared 2-core machine: 4096 bakes too slow)
    ground=False, water=WL,
    wreck=dict(seed=141, drop=['barrel2'], pose={'turret': (20, 40, 0)}),
    preview_pose={'turret': (-12, -25, 0)},
)


def build(k):
    b = k.piece('base')
    # four box pontoons (+x / -x mirrored, +z / -z built whole)
    def pontoon(R, mirror):
        b.hull([R(u, y, w) for u, y in ((9.0, 10.0), (26.0, 13.0), (9.0, 24.0), (27.5, 24.0), (28.0, 18.0))
                for w in (-8.6, 8.6)], 'paint', bevel=0.4, mirror=mirror)
        b.hull([R(u, y, w) for u in (21.0, 26.4) for y in (23.95, 24.2) for w in (-5.6, 5.6)], 'team', bevel=0.0,
               mirror=mirror)
        b.hull([R(u, y, w) for u in (12.0, 15.6) for y in (23.9, 24.6) for w in (-7.6, 7.6)], 'steel', bevel=0.1,
               mirror=mirror)
        b.hull([R(u, y, w) for u in (27.6, 28.3) for y in (19.4, 21.0) for w in (-9.0, 9.0)], 'dark', bevel=0.0,
               mirror=mirror)
    pontoon(lambda u, y, w: (u, y, w), True)
    for s in (-1, 1):
        pontoon(lambda u, y, w, s=s: (w, y, u * s), False)
    for s in (-1, 1):
        b.box((27.9 * s - 0.2, 21.8, -1.2), (27.9 * s + 0.2, 22.8, 1.2), 'lightr', bevel=0.0)
    # hub and tapering tower with dark corner ribs
    oct8 = [(13.0 * math.cos(math.pi / 8 + i * math.pi / 4), 13.0 * math.sin(math.pi / 8 + i * math.pi / 4))
            for i in range(8)]
    b.plan(8.0, 26.0, oct8, 'paint2', bevel=0.35, top_inset=1.5)
    b.plan(25.8, 35.0, [(-8.0, -8.0), (8.0, -8.0), (8.0, 8.0), (-8.0, 8.0)], 'paint', bevel=0.3, top_inset=2.4)
    for sx in (-1, 1):
        for sz in (-1, 1):
            b.hull([(x * sx, y, z * sz) for x, y, z in
                    [(6.6, 26.0, 6.6), (9.8, 26.0, 9.8), (9.4, 26.0, 6.6), (6.6, 26.0, 9.4),
                     (5.0, 34.0, 5.0), (6.0, 34.0, 6.0), (6.0, 34.0, 5.0), (5.0, 34.0, 6.0)]], 'dark', bevel=0.12)
    b.cyl((0, 34.6, -3.75), (0, 38.4, -3.75), 6.0, 8, 'paint2', r2=5.0, rot=math.pi / 8, bevel=0.15)
    b.cyl((0, 37.6, -3.75), (0, 38.3, -3.75), 7.0, 12, 'dark')
    b.box((-2.0, 28.0, 7.65), (2.0, 29.0, 7.95), 'lightr', bevel=0.0)
    b.cyl((0, 0.0, 0), (0, 8.2, 0), 4.0, 8, 'dark', r2=8.0, rot=math.pi / 8)        # ballast keel

    # ---------------------------------------------------------------- turret: helmet (origin 0, 38, -3.75)
    t = k.piece('turret'); A = t.at
    prof = [(-11.4, 0.0, 9.6), (-11.8, 7.6, 10.6), (-9.4, 13.4, 8.2), (-3.4, 15.6, 5.0),
            (9.2, 0.0, 9.6), (11.0, 7.6, 10.6), (10.8, 13.0, 8.2), (7.4, 15.2, 4.2)]
    t.hull([A(x * sx, y, z) for sx in (-1, 1) for (z, y, x) in prof], 'paint', bevel=0.35)
    for sx in (-1, 1):
        t.hull([A(sx * x, y, z) for (x, y) in ((9.8, 13.1), (4.6, 15.35)) for z in (-8.0, 6.4)] +
               [A(sx * (x + 0.12), y + 0.2, z) for (x, y) in ((9.8, 13.1), (4.6, 15.35)) for z in (-8.0, 6.4)],
               'team', bevel=0.0)
    t.hull([A(x, y, z) for x in (-1.8, 1.8) for z in (-3.0, 6.6) for y in (15.5, 15.75)], 'hazard', bevel=0.0)
    t.hull([A(x * sx, y, z) for sx in (-1, 1) for x, y, z in
            [(10.0, 0.6, 11.0), (10.0, 13.6, 9.0), (9.6, 0.8, 12.2), (9.6, 13.2, 10.2)]], 'paint2', bevel=0.15)
    t.box(A(-11.4, 6.0, -6.0), A(11.4, 9.0, 2.0), 'paint2', bevel=0.2)
    t.box(A(-0.8, 14.1, -7.6), A(0.8, 14.6, -6.4), 'lightr', bevel=0.0)
    t.box(A(-8.0, 1.0, -11.6), A(8.0, 7.0, -11.2), 'black', bevel=0.0)

    # ---------------------------------------------------------------- tubes (barrel1 top centre, 2/3 low sides)
    g = k.piece('barrel1'); G = g.at
    g.cyl(G(0, 0, -1.6), G(0, 0, 8.0), 3.1, 8, 'steel', rot=math.pi / 8, bevel=0.08)
    g.cyl(G(0, 0, 4.8), G(0, 0, 5.8), 3.4, 8, 'dark', rot=math.pi / 8, bevel=0.05)
    g.cyl(G(0, 0, 7.98), G(0, 0, 8.1), 2.2, 8, 'black')
    g.cyl(G(0, 0, 2.0), G(0, 0, 3.0), 3.3, 8, 'hazard', rot=math.pi / 8)
    k.clone('barrel2', 'barrel1')
    k.clone('barrel3', 'barrel1')
