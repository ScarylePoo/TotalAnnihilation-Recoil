"""Underwater Metal Extractor (ARM_T1_SEAECO_UWMetalExtractor) - Arm seabed mex (no waterline: it sits on the sea bed,
minimum 19 elmo of water over it). The land Arm mex's stepped light octagon pad and tapering drill column, but the rotor
is a three-armed 'Y' (arms, spins on y while extracting) whose arms end in tall steel vent stacks: the ore slurry
bubbles out of their tops (emit1..3).
Identity from above (through the water): a light octagon with a dark collar, a team 'Y' with three team stack heads at
its tips and a light hub (the land Arm mex is a straight two-drill bar; the Core sea mex is a dark hex dome with a fan
under an arched cage).
Pieces (Lua script): base, arms (spin y; origin 0, 15.05, 0), emit1/2/3 (bubble emit points, empty; at the stack tops).
Coordinates are ENGINE/global: X right, Y up, Z forward."""
import math

UNIT = dict(
    res=1024,
    preview_water=19.0,
    wreck=dict(seed=81),
    preview_pose={'arms': (0, 15, 0)},
)


def octagon(r, rot=math.pi / 8):
    return [(r * math.cos(rot + i * math.pi / 4), r * math.sin(rot + i * math.pi / 4)) for i in range(8)]


def build(k):
    b = k.piece('base')
    b.plan(0.0, 3.0, octagon(23.5), 'paint2', bevel=0.3, top_inset=1.0)
    b.plan(2.8, 9.4, octagon(19.0), 'paint', bevel=0.35, top_inset=4.2)
    b.plan(9.2, 10.8, octagon(11.4), 'dark', bevel=0.15, top_inset=0.6)
    b.cyl((0, 10.6, 0), (0, 15.2, 0), 6.4, 8, 'paint2', r2=5.2, rot=math.pi / 8, bevel=0.15)
    # four ore intake hoods on the pad skirt (diagonals) and lights
    for ang in (45, 135, 225, 315):
        c, s = math.cos(math.radians(ang)), math.sin(math.radians(ang))
        R = lambda u, y, w: (c * u - s * w, y, s * u + c * w)
        b.hull([R(u, y, w) for u, y in ((14.5, 2.9), (14.5, 6.0), (20.5, 2.9), (19.0, 4.0)) for w in (-3.2, 3.2)],
               'dark', bevel=0.15)
        b.hull([R(u, y, w) for u, y in ((19.9, 3.0), (20.8, 3.0), (19.6, 3.9)) for w in (-2.4, 2.4)], 'black',
               bevel=0.0)
    for sz in (-1, 1):
        b.box((-1.0, 5.0, 14.9 * sz - 0.2), (1.0, 6.0, 14.9 * sz + 0.2), 'lightc', bevel=0.0)

    # ---------------------------------------------------------------- arms: three-arm rotor (origin 0, 15.05, 0)
    a = k.piece('arms')
    a.cyl((0, 14.9, 0), (0, 19.6, 0), 7.2, 12, 'paint', r2=6.4, bevel=0.25)
    a.sphere((0, 19.5, 0), 4.6, 'paint', segs=12, rings=6, scale=(1, 0.55, 1))
    a.cyl((0, 21.6, 0), (0, 22.3, 0), 1.4, 8, 'lightc')

    def arm(ang, mirror):
        c, s = math.cos(math.radians(ang)), math.sin(math.radians(ang))
        R = lambda u, y, w: (c * u - s * w, y, s * u + c * w)
        a.hull([R(u, y, w) for u in (5.0, 17.0) for y in (15.6, 19.2) for w in (-3.0, 3.0)]
               + [R(19.0, y, w) for y in (16.0, 18.8) for w in (-2.2, 2.2)], 'paint', bevel=0.25, mirror=mirror)
        a.hull([R(u, y, w) for u in (5.8, 17.4) for y in (19.15, 19.45) for w in (-2.85, 2.85)], 'team', bevel=0.0,
               mirror=mirror)
        cx, cz = c * 19.4, s * 19.4
        a.cyl((cx, 14.0, cz), (cx, 24.6, cz), 2.6, 10, 'steel', bevel=0.06, mirror=mirror)
        a.cyl((cx, 24.4, cz), (cx, 26.0, cz), 3.6, 10, 'team', bevel=0.08, mirror=mirror)
        a.cyl((cx, 25.9, cz), (cx, 26.1, cz), 1.9, 10, 'black', mirror=mirror)
        a.cyl((cx, 20.2, cz), (cx, 21.4, cz), 3.0, 10, 'dark', mirror=mirror)
    arm(90, False); arm(330, True)
