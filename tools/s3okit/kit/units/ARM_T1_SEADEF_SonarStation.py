"""Sonar Station (ARM_T1_SEADEF_SonarStation) - Arm sonar buoy. Waterline 33 (the water surface is model y = 33).
A three-legged anchor frame on the sea bed and a light float drum (bouy) whose deck rides 2.5 elmo above the water.
The base carries a rotor over the deck - a hub with two arms ending in light hydrophone paddles (the land radar's 'T'
of paddles, laid flat on the water) - and the beacon mast (light) that drops 3.4 into the hub when switched off.
The script spins base +1 and bouy -1, so the float stays still while the rotor turns over it.
Identity from above: a light disc with a thin team ring and a long dark bar with two light paddles crossing it, a cyan
dot in the middle (the Core sonar is a dark tripod buoy with a spinning twin-pod array under it).
Pieces (Lua script): base (spin y), bouy (spin y, opposite), light (move y: -3.4 off, 0 on).
Preview: ON (light at 0).
Coordinates are ENGINE/global: X right, Y up, Z forward."""
import math

WL = 33.0
UNIT = dict(
    res=1024,
    ground=False, water=WL,
    wreck=dict(seed=52, drop=['light']),
    preview_pose={'base': (0, 30, 0), 'bouy': (0, -30, 0)},
)


def build(k):
    b = k.piece('base')
    # anchor tripod (always deep under water: plain)
    for a in (90, 210, 330):
        c, s = math.cos(math.radians(a)), math.sin(math.radians(a))
        R = lambda r, w, y: (c * r - s * w, y, s * r + c * w)
        b.hull([R(r, w, y) for r, y in ((3.0, 20.0), (5.0, 20.0)) for w in (-1.6, 1.6)]
               + [R(r, w, y) for r, y in ((12.0, 1.5), (14.5, 1.5)) for w in (-2.0, 2.0)], 'paint2', bevel=0.15)
        b.hull([R(r, w, y) for r in (10.5, 16.0) for w in (-3.0, 3.0) for y in (0.0, 1.8)], 'dark', bevel=0.1)
    b.cyl((0, 14.0, 0), (0, 21.0, 0), 5.2, 8, 'dark', rot=math.pi / 8, bevel=0.1)
    # rotor over the float deck: hub, two arms, two hydrophone paddles
    b.cyl((0, 35.2, 0), (0, 39.2, 0), 3.6, 8, 'dark', r2=3.0, rot=math.pi / 8, bevel=0.1)
    b.hull([(x, y, z) for x in (2.5, 11.5) for y in (36.0, 37.8) for z in (-1.3, 1.3)], 'paint2', bevel=0.12,
           mirror=True)
    b.hull([(x, y, z) for x in (10.8, 16.2) for y in (35.8, 38.4) for z in (-4.6, 4.6)]
           + [(x, 38.9, z) for x in (11.6, 15.4) for z in (-3.8, 3.8)], 'paint', bevel=0.25, mirror=True)
    b.hull([(x, y, z) for x in (12.3, 14.7) for y in (38.85, 39.05) for z in (-3.0, 3.0)], 'team', bevel=0.0,
           mirror=True)
    b.box((16.15, 36.6, -0.6), (16.45, 37.6, 0.6), 'lightc', bevel=0.0, mirror=True)

    # ---------------------------------------------------------------- bouy: float drum
    f = k.piece('bouy')
    f.cyl((0, 19.0, 0), (0, 24.0, 0), 5.0, 12, 'paint2', r2=10.0, bevel=0.2)
    f.cyl((0, 23.9, 0), (0, 35.6, 0), 10.0, 16, 'paint', r2=9.2, rot=math.pi / 16, bevel=0.35)
    f.cyl((0, 32.4, 0), (0, 33.6, 0), 10.25, 16, 'dark', rot=math.pi / 16)
    f.cyl((0, 35.5, 0), (0, 35.8, 0), 8.6, 16, 'team', rot=math.pi / 16)
    f.cyl((0, 35.75, 0), (0, 36.0, 0), 6.9, 16, 'paint2', rot=math.pi / 16)
    for a in (45, 135, 225, 315):
        c, s = math.cos(math.radians(a)), math.sin(math.radians(a))
        f.box((c * 9.3 - 0.5, 34.0, s * 9.3 - 0.5), (c * 9.3 + 0.5, 35.0, s * 9.3 + 0.5), 'lightc', bevel=0.0)

    # ---------------------------------------------------------------- light: beacon mast (moves y)
    l = k.piece('light')
    l.cyl((0, 38.0, 0), (0, 40.4, 0), 1.3, 8, 'steel')
    l.cyl((0, 40.3, 0), (0, 41.6, 0), 1.6, 8, 'lightc')
