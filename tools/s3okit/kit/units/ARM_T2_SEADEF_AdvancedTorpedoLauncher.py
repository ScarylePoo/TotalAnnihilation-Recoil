"""Advanced Torpedo Launcher (ARM_T2_SEADEF_AdvancedTorpedoLauncher) - Arm T2 torpedo launcher. Waterline 25 (the water
surface is model y = 25). As in TA the whole thing hangs from a float: a light octagonal float (5 elmo freeboard, team
deck ring, cyan beacon) carries a turntable from which the turret, a wide yoke, hangs: a crossbeam just under the
surface and two legs down to the trunnions of a long twin-tube launcher deep under water (recoils 10 back on firing).
Identity from above: a light octagon with a team ring over a long dark cross-beam and a long light twin tube with a team
spine under the water (the T1 Arm launcher is a ring frame on legs with one tube and a small marker float).
Pieces (Lua script): base (float), turret (turn y; origin 0, 23.73, 0; hangs below), launcher (move z; origin
0, 6.97, -22.29, tubes run +z), flare/bubbles (emit, empty).
Coordinates are ENGINE/global: X right, Y up, Z forward."""
import math

WL = 25.0
UNIT = dict(
    res=1024,                  # 4x4, but 1024 like the land T1 defences (shared 2-core machine: 4096 bakes too slow)
    ground=False, water=WL,
    wreck=dict(seed=131, pose={'turret': (0, 30, 0)}),
    preview_pose={'turret': (0, -25, 0)},
)


def octagon(r, rot=math.pi / 8):
    return [(r * math.cos(rot + i * math.pi / 4), r * math.sin(rot + i * math.pi / 4)) for i in range(8)]


def build(k):
    b = k.piece('base')
    b.hull([(x * 0.8, 24.0, z * 0.8) for x, z in octagon(15.0)] + [(x, 26.5, z) for x, z in octagon(15.0)]
           + [(x * 0.95, 30.0, z * 0.95) for x, z in octagon(15.0)], 'paint', bevel=0.4)
    b.hull([(x * s, y, z * s) for x, z in octagon(15.0) for s in (0.99, 1.03) for y in (25.6, 27.0)], 'dark',
           bevel=0.0)
    O = octagon(13.2)
    for i in range(8):           # team deck ring (segments: a hull of the whole ring would fill its hole)
        p, q = O[i], O[(i + 1) % 8]
        b.hull([(x * s, y, z * s) for (x, z) in (p, q) for s in (1.0, 0.75) for y in (29.95, 30.2)], 'team',
               bevel=0.0)
    b.cyl((0, 29.9, 0), (0, 31.6, 0), 6.0, 8, 'paint2', r2=5.0, rot=math.pi / 8, bevel=0.2)
    b.cyl((0, 31.5, 0), (0, 33.6, 0), 1.3, 8, 'steel')
    b.cyl((0, 33.4, 0), (0, 34.6, 0), 1.7, 8, 'lightc')
    for sz in (-1, 1):
        b.box((-1.2, 27.6, 14.4 * sz - 0.2), (1.2, 28.6, 14.4 * sz + 0.2), 'lightc', bevel=0.0)
    b.cyl((0, 23.9, 0), (0, 24.2, 0), 7.0, 12, 'dark')                          # turntable race

    # ---------------------------------------------------------------- turret: hanging yoke (origin 0, 23.73, 0)
    t = k.piece('turret'); T = t.at
    t.cyl(T(0, -1.6, 0), T(0, 0.2, 0), 6.6, 12, 'dark', bevel=0.1)
    t.hull([T(x, y, z) for x in (-23.0, 23.0) for y in (-4.4, -1.4) for z in (-4.2, 4.2)]
           + [T(x, -2.2, z) for x in (-24.4, 24.4) for z in (-3.0, 3.0)], 'paint2', bevel=0.3)
    t.hull([T(x, y, z) for x in (-21.5, 21.5) for y in (-1.5, -1.2) for z in (-2.2, 2.2)], 'dark', bevel=0.0)
    # legs down to the trunnions (x = +-12), braced
    for sx in (-1, 1):       # turret origin x is -0.00004: no mirror=True, both legs built
        t.hull([T(sx * x, y, z) for x, y in ((14.0, -4.0), (19.0, -4.0), (10.6, -17.0), (13.6, -17.0))
                for z in (-3.0, 3.0)], 'paint', bevel=0.25)
        t.cyl(T(sx * 8.2, -16.76, 0), T(sx * 13.8, -16.76, 0), 3.0, 10, 'dark', bevel=0.08)
        t.hull([T(sx * x, y, z) for x, y in ((14.6, -6.0), (16.0, -6.0), (21.0, -3.6), (22.0, -4.3))
                for z in (-1.0, 1.0)], 'dark', bevel=0.05)
    for sx in (-1, 1):
        t.box(T(23.2 * sx - 0.3, -3.4, -1.0), T(23.2 * sx + 0.3, -2.4, 1.0), 'lightc', bevel=0.0)

    # ---------------------------------------------------------------- launcher: twin tube (origin 0, 6.97, -22.29)
    l = k.piece('launcher'); L = l.at
    l.hull([L(x, y, z) for x in (-8.4, 8.4) for y in (-4.4, 3.8) for z in (3.0, 34.0)]
           + [L(x, y, z) for x in (-7.0, 7.0) for y in (-3.4, 5.6) for z in (6.0, 30.0)]
           + [L(x, y, 0.0) for x in (-6.0, 6.0) for y in (-3.0, 3.0)], 'paint', bevel=0.35)
    l.hull([L(x, y, z) for x in (-2.6, 2.6) for y in (5.55, 5.85) for z in (8.0, 28.0)], 'team', bevel=0.0)
    for sx in (-1, 1):
        l.cyl(L(4.2 * sx, -0.99, 33.0), L(4.2 * sx, -0.99, 43.6), 3.6, 12, 'steel', bevel=0.06)
        l.cyl(L(4.2 * sx, -0.99, 43.4), L(4.2 * sx, -0.99, 44.3), 2.7, 12, 'black')
        l.cyl(L(4.2 * sx, -0.99, 37.0), L(4.2 * sx, -0.99, 38.6), 4.0, 12, 'dark')
    l.box(L(-8.6, -2.0, 12.0), L(8.6, 3.0, 13.6), 'dark', bevel=0.05)
    l.box(L(-8.6, -2.0, 24.0), L(8.6, 3.0, 25.6), 'dark', bevel=0.05)
    l.box(L(-5.0, -3.2, -1.0), L(5.0, 2.8, 1.0), 'dark', bevel=0.1)
