"""Stingray (ARM_T1_SEADEF_Stingray) - Arm floating heavy laser tower. Waterline 4 (the water surface is model y = 4).
A solid octagonal float hull (light flared sides, 5 elmo of freeboard) with a dark deck, a stepped light armoured
drum on it, a column (turret) and a wide Y-yoke carrying two big laser pods far out to the sides - the land
Sentinel's 'tuning fork' head on a boat-like hull instead of a blockhouse.
Identity from above: a light octagonal ring round a dark deck with two team side plates, a light drum in the middle and
two long light pods with team backs and cyan lenses across it (the Arm sea Defender is four drums round a dark X).
Pieces (Lua script): base, turret (turn y; origin at 0,0,0), gun (turn x), barrel1/barrel2 (aim points; carry the
pods, barrel2 = barrel1 mirrored: origins are at x -8.75 / +8.25), flare1/flare2 (emit, empty).
Coordinates are ENGINE/global: X right, Y up, Z forward."""
import math

WL = 4.0
UNIT = dict(
    res=1024,                  # 4x4, but 1024 like the land T1 defences (shared 2-core machine: 4096 bakes too slow)
    ground=False, water=WL,
    wreck=dict(seed=33, drop=['barrel2'], pose={'turret': (0, 35, 0), 'gun': (10, 0, 0)}),
    preview_pose={'turret': (0, -20, 0), 'gun': (-8, 0, 0)},
)

OCT = [(-12.0, -25.0), (12.0, -25.0), (24.0, -13.0), (24.0, 13.0), (12.0, 25.0), (-12.0, 25.0), (-24.0, 13.0),
       (-24.0, -13.0)]


def scaled(poly, s, dz=0.0):
    return [(x * s, z * s + dz) for x, z in poly]


def build(k):
    # ------------------------------------------------------------------ base: float hull + deck + drum
    b = k.piece('base')
    b.hull([(x, 0.0, z) for x, z in scaled(OCT, 0.78)] + [(x, 4.0, z) for x, z in scaled(OCT, 0.93)]
           + [(x, 9.0, z) for x, z in OCT], 'paint', bevel=0.35)
    b.plan(8.9, 9.6, scaled(OCT, 0.86), 'paint2', bevel=0.15)                        # dark deck
    # team side plates on the deck (port/starboard), rub strake at the waterline
    b.hull([(x, y, z) for x in (13.0, 19.6) for y in (9.55, 9.75) for z in (-9.5, 9.5)]
           + [(13.0, y, z) for y in (9.55, 9.75) for z in (-14.0, 14.0)], 'team', bevel=0.0, mirror=True)
    b.hull([(x * s, y, z * s) for x, z in OCT for s in (0.955, 0.975) for y in (5.2, 6.4)], 'dark', bevel=0.0)
    # bow / stern bollards and lights
    for sz in (-1, 1):
        b.cyl((6.0, 9.5, 21.0 * sz), (6.0, 11.4, 21.0 * sz), 1.3, 8, 'dark', mirror=True)
        b.box((-1.2, 7.0, 24.85 * sz - 0.2), (1.2, 8.2, 24.85 * sz + 0.2), 'lightc', bevel=0.0)
    # stepped armoured drum
    b.cyl((0, 9.4, 0), (0, 17.5, 0), 13.0, 8, 'paint', r2=11.0, rot=math.pi / 8, bevel=0.4)
    b.cyl((0, 17.3, 0), (0, 18.4, 0), 11.6, 8, 'dark', rot=math.pi / 8, bevel=0.1)
    b.cyl((0, 18.2, 0), (0, 25.5, 0), 9.6, 8, 'paint2', r2=7.4, rot=math.pi / 8, bevel=0.3)
    b.cyl((0, 25.3, 0), (0, 28.6, 0), 6.6, 8, 'paint', r2=6.0, rot=math.pi / 8, bevel=0.2)
    for a in (0, 90, 180, 270):          # four vent louvres on the drum shoulders
        c, s = math.cos(math.radians(a)), math.sin(math.radians(a))
        b.hull([(c * r - s * w, y, s * r + c * w) for r in (10.9, 11.8) for w in (-2.4, 2.4) for y in (12.0, 15.6)],
               'black', bevel=0.0)

    # ---------------------------------------------------------------- turret: column (origin 0,0,0)
    t = k.piece('turret')
    t.cyl((0, 28.4, -0.6), (0, 39.6, -0.6), 4.2, 8, 'paint2', r2=3.6, rot=math.pi / 8, bevel=0.15)
    t.cyl((0, 30.0, -0.6), (0, 31.4, -0.6), 5.2, 8, 'dark', rot=math.pi / 8, bevel=0.05)
    t.box((-1.0, 34.0, 2.9), (1.0, 35.2, 3.25), 'lightc', bevel=0.0)

    # ---------------------------------------------------------------- gun: Y yoke (origin 0, 41.16, -0.6)
    g = k.piece('gun'); G = g.at
    g.cyl(G(-3.0, 0, 0), G(3.0, 0, 0), 3.4, 10, 'dark', bevel=0.08)                  # trunnion
    g.hull([G(x, y, z) for x, y, z in
            [(1.5, -2.6, -3.0), (1.5, 2.6, -3.0), (1.5, -2.6, 3.0), (1.5, 2.6, 3.0),
             (8.0, 2.6, 1.0), (8.0, 6.4, 1.0), (8.0, 2.6, 6.0), (8.0, 6.4, 6.0)]], 'paint2', bevel=0.2, mirror=True)
    g.hull([G(x, y, z) for x, y, z in
            [(0.0, 2.4, -2.4), (0.0, 3.4, -2.4), (0.0, 2.4, 2.4), (0.0, 3.4, 2.4),
             (5.0, 4.4, -0.2), (5.0, 5.6, -0.2), (5.0, 4.4, 4.0), (5.0, 5.6, 4.0)]], 'paint', bevel=0.1, mirror=True)

    # ---------------------------------------------------------------- barrel1: laser pod (origin -8.75, 46.17, 10.88)
    p = k.piece('barrel1'); B = p.at
    p.hull([B(x, y, z) for x in (-3.4, 3.4) for y in (-2.6, 2.6) for z in (-11.0, 4.0)]
           + [B(x, y, 6.5) for x in (-2.4, 2.4) for y in (-2.0, 2.0)], 'paint', bevel=0.3)
    p.hull([B(x, y, z) for x in (-2.0, 2.0) for y in (2.55, 2.85) for z in (-10.0, 3.2)], 'team', bevel=0.0)
    p.box(B(-3.5, -1.0, -11.6), B(3.5, 1.6, -10.6), 'dark', bevel=0.1)
    p.cyl(B(0, 0, 6.0), B(0, 0, 11.0), 1.3, 10, 'steel', bevel=0.04)
    p.cyl(B(0, 0, 10.8), B(0, 0, 11.6), 1.8, 10, 'dark')
    p.cyl(B(0, 0, 6.4), B(0, 0, 6.9), 2.3, 10, 'lightc')
    for x in (-3.45, 3.45):
        p.box(B(x - 0.25, -1.2, -7.5), B(x + 0.25, 1.2, 1.5), 'dark', bevel=0.0)
    k.clone('barrel2', 'barrel1', mirror_x=True)
