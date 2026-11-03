"""Thunderbolt (CORE_T1_SEADEF_Thunderbolt) - Core floating heavy laser tower. Waterline 15 (the water surface is model
y = 15). A low, wide dark octagonal raft barely awash (deck 1 elmo above the water) with four raised corner sponsons
(team tops) and an ochre-ringed turntable; on it a turret block (turret1) with a team-roofed generator on its right
and, on its left, the laser house (turret2, elevates) with two long light steel barrels stacked one high, one low
(each kicks back 7.5 on fire).
Identity from above: a dark octagon with four team corner squares, a dark turret with a team generator roof on the
right and a team-roofed laser house with two long light barrels on the LEFT (the Stinger is a dark plus of pontoons with a round helmet; the Arm
Stingray is a light hull with a symmetric two-pod yoke).
Pieces (COB): base (RockUnit turns x/z), turret1 (turn y; origin 0, 16, -3.5), turret2 (turn x; origin -4.62, 20.5,
-5.12), barrel1/2 (move z recoil), flare1/2 (emit, empty; the COB shows/hides them - harmless).
Coordinates are ENGINE/global: X right, Y up, Z forward."""
import math

WL = 15.0
UNIT = dict(
    res=1024,
    ground=False, water=WL,
    wreck=dict(seed=151, drop=['barrel2'], pose={'turret1': (0, 35, 0), 'turret2': (12, 0, 0)}),
    preview_pose={'turret1': (0, 20, 0), 'turret2': (-6, 0, 0)},
)


def build(k):
    b = k.piece('base')
    oct8 = [(21.5 * math.cos(math.pi / 8 + i * math.pi / 4), 21.5 * math.sin(math.pi / 8 + i * math.pi / 4))
            for i in range(8)]
    b.hull([(x * 0.8, 5.0, z * 0.8) for x, z in oct8] + [(x, 12.0, z) for x, z in oct8]
           + [(x * 0.97, 16.0, z * 0.97) for x, z in oct8], 'paint', bevel=0.4)
    b.hull([(x * s, y, z * s) for x, z in oct8 for s in (1.0, 1.03) for y in (13.0, 14.6)], 'dark', bevel=0.0)
    b.plan(15.9, 16.3, [(x * 0.62, z * 0.62) for x, z in oct8], 'paint2', bevel=0.0)
    # corner sponsons (diagonals), team tops
    for sz in (-1, 1):
        b.hull([(x, y, z * sz) for x, z in ((10.0, 15.5), (15.5, 10.0), (19.6, 14.6), (14.6, 19.6))
                for y in (10.0, 18.6)], 'paint2', bevel=0.3, mirror=True)
        b.hull([(x, y, z * sz) for x, z in ((11.3, 15.6), (15.6, 11.3), (18.4, 14.6), (14.6, 18.4))
                for y in (18.55, 18.8)], 'team', bevel=0.0, mirror=True)
        b.box((19.6, 16.0, 14.6 * sz - 0.8), (19.95, 16.8, 14.6 * sz + 0.8), 'lightr', bevel=0.0, mirror=True)
    # turntable with ochre ring
    b.cyl((0, 15.8, -3.5), (0, 16.5, -3.5), 11.6, 16, 'hazard')
    b.cyl((0, 0.0, 0), (0, 5.2, 0), 5.0, 8, 'dark', r2=12.0, rot=math.pi / 8)            # ballast keel

    # ---------------------------------------------------------------- turret1: block + generator (0, 16, -3.5)
    t = k.piece('turret1'); T = t.at
    t.cyl(T(0, 0.3, 0), T(0, 2.2, 0), 10.0, 12, 'dark', bevel=0.1)
    t.hull([T(x, y, z) for x in (-3.0, 9.6) for y in (2.0, 7.8) for z in (-10.6, 6.0)]
           + [T(x, 9.4, z) for x in (-1.6, 8.0) for z in (-9.0, 4.0)], 'paint', bevel=0.35)
    t.hull([T(x, y, z) for x in (-1.2, 7.6) for y in (9.35, 9.6) for z in (-8.6, 3.6)], 'team', bevel=0.0)
    for z in (-6.0, -3.0, 0.0):
        t.box(T(9.5, 3.6, z), T(9.9, 6.6, z + 1.6), 'black', bevel=0.0)
    t.hull([T(x, y, z) for x in (-4.0, -1.4) for y in (2.0, 6.0) for z in (-4.6, 2.6)], 'paint2', bevel=0.15)
    t.box(T(3.0, 9.4, 5.2), T(5.0, 9.7, 6.0), 'lightr', bevel=0.0)

    # ---------------------------------------------------------------- turret2: laser house (-4.62, 20.5, -5.12)
    h = k.piece('turret2'); H = h.at
    h.cyl(H(-0.6, 0, 0), H(0.8, 0, 0), 3.2, 10, 'dark', bevel=0.06)
    h.hull([H(x, y, z) for x in (-11.4, -1.0) for y in (-4.2, 4.6) for z in (-12.0, 12.0)]
           + [H(x, 6.0, z) for x in (-10.0, -2.4) for z in (-10.0, 9.0)]
           + [H(x, y, 15.6) for x in (-10.4, -2.0) for y in (-3.6, 3.4)], 'paint', bevel=0.35)
    h.hull([H(x, y, z) for x in (-9.2, -3.2) for y in (5.95, 6.2) for z in (-9.0, 7.6)], 'team', bevel=0.0)
    h.box(H(-11.5, -2.0, -13.0), H(-1.0, 3.0, -12.0), 'black', bevel=0.0)
    h.cyl(H(-8.31, -1.6, 15.0), H(-8.31, -1.6, 18.0), 2.2, 10, 'dark', bevel=0.05)
    h.cyl(H(-2.81, 0.72, 15.0), H(-2.81, 0.72, 21.0), 2.2, 10, 'dark', bevel=0.05)
    h.box(H(-6.4, 4.6, 13.0), H(-4.8, 5.0, 14.4), 'lightr', bevel=0.0)

    # ---------------------------------------------------------------- barrels (long light steel)
    g = k.piece('barrel1'); G = g.at
    g.cyl(G(0, 0, -6.0), G(0, 0, 14.4), 1.25, 10, 'steel', bevel=0.04)
    g.cyl(G(0, 0, 8.0), G(0, 0, 10.0), 1.7, 10, 'steel', bevel=0.04)
    g.cyl(G(0, 0, 14.2), G(0, 0, 14.9), 1.6, 10, 'lightr')
    k.clone('barrel2', 'barrel1')
