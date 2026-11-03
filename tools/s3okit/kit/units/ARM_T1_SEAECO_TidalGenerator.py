"""Tidal Generator (ARM_T1_SEAECO_TidalGenerator) - Arm tidal power. Waterline 16 (the water surface is model y = 16).
The land wind generator's parts rearranged for the sea: a light nacelle-shaped float riding 5 elmo above the water
with a tall tail fin and a glowing cyan generator dome on its roof, a crossbar float behind it, and under the water a
big three-blade rotor (wheel, spins on y) hanging from the nacelle's nose just under the surface.
Identity from above: a long light nacelle with a team roof stripe and team crossbar ends, a cyan dot, and a wide
three-blade star with team tips under the surface in front (the Core tidal is a dark power house beside a vertical
eggbeater rotor).
Pieces (Lua script): base, wheel (spin y; origin -0.31, 0.25, 6.43: the blades ride 11-14 up its shaft, just under
the surface, so they read through the water; the nacelle ends at the rotor bearing).
Coordinates are ENGINE/global: X right, Y up, Z forward."""
import math

WL = 16.0
UNIT = dict(
    res=1024,
    ground=False, water=WL,
    wreck=dict(seed=71, drop=['wheel']),
    preview_pose={'wheel': (0, 20, 0)},
)

WX, WZ = -0.31, 6.43


def build(k):
    b = k.piece('base')
    # nacelle float along z (crosses x = 0: whole)
    prof = [(-23.0, 16.5), (-21.0, 19.0), (-14.0, 21.2), (2.0, 21.2), (9.0, 20.4), (12.4, 17.6), (11.0, 14.6),
            (-20.0, 14.6)]
    b.hull([(x, y, z) for x in (-6.8, 6.8) for z, y in prof] + [(x, y, z) for x in (-5.0, 5.0) for z, y in
           ((-18.0, 14.4), (8.0, 14.4))], 'paint', bevel=0.4)
    b.hull([(x, y, z) for x in (-6.95, 6.95) for z, y in ((-22.0, 15.2), (11.6, 15.2), (-22.0, 16.8), (11.6, 16.8))],
           'dark', bevel=0.05)
    b.hull([(x, y, z) for x in (-2.6, 2.6) for y in (21.15, 21.4) for z in (-13.0, 0.0)], 'team', bevel=0.0)
    # generator dome on the roof (cyan) and its collar
    b.cyl((WX, 20.0, WZ), (WX, 22.4, WZ), 5.0, 12, 'paint2', bevel=0.15)
    b.sphere((WX, 22.3, WZ), 3.8, 'lightc', segs=12, rings=6, scale=(1, 0.6, 1))
    # tail fin
    b.hull([(x, y, z) for x in (-0.9, 0.9) for z, y in ((-21.0, 20.0), (-12.0, 21.0), (-19.5, 30.0), (-22.5, 29.5))],
           'paint2', bevel=0.2)
    b.box((-1.0, 28.6, -22.0), (1.0, 29.6, -20.2), 'lightc', bevel=0.0)
    # crossbar float behind the nacelle (outriggers)
    b.hull([(x, y, z) for x in (5.0, 18.5) for y in (13.0, 18.6) for z in (-19.0, -12.0)]
           + [(21.0, y, z) for y in (14.0, 17.6) for z in (-18.0, -13.0)], 'paint', bevel=0.35, mirror=True)
    b.hull([(x, y, z) for x in (12.0, 19.6) for y in (18.55, 18.8) for z in (-18.0, -13.0)], 'team', bevel=0.0,
           mirror=True)
    b.box((20.9, 16.0, -16.2), (21.6, 17.0, -14.8), 'lightc', bevel=0.0, mirror=True)
    b.cyl((WX, 14.0, WZ), (WX, 14.8, WZ), 4.6, 12, 'dark')          # bearing under the nose
    # ballast keel under the tail, down to the sea bed (outside the rotor sweep; the wreck rests on it)
    b.cyl((0, 0.0, -16.0), (0, 14.8, -16.0), 2.2, 8, 'dark', r2=3.6, rot=math.pi / 8)
    b.cyl((0, 0.0, -16.0), (0, 1.6, -16.0), 4.4, 8, 'dark', rot=math.pi / 8)

    # ---------------------------------------------------------------- wheel: three-blade rotor (origin WX, 0.25, WZ)
    w = k.piece('wheel'); W = w.at
    # shaft from the original hub height up to the blades, just under the surface (spin axis is vertical)
    w.cyl(W(0, 0.0, 0), W(0, 2.0, 0), 3.6, 12, 'dark', bevel=0.1)
    w.cyl(W(0, 1.8, 0), W(0, 10.6, 0), 1.8, 10, 'steel')
    w.cyl(W(0, 10.0, 0), W(0, 13.8, 0), 3.8, 12, 'dark', bevel=0.1)
    for i in range(3):
        a = math.radians(90 + 120 * i)
        c, s = math.cos(a), math.sin(a)
        R = lambda u, y, v: W(c * u - s * v, y, s * u + c * v)
        # blade: wide root, tapering, pitched (leading edge high)
        w.hull([R(3.0, 10.6, -1.8), R(3.0, 13.2, 2.0), R(3.0, 11.6, 2.0), R(3.0, 12.2, -1.8),
                R(13.0, 11.0, -3.4), R(13.0, 12.8, 3.2), R(13.0, 11.6, 3.2), R(13.0, 12.2, -3.4)], 'paint', bevel=0.15)
        w.hull([R(13.0, 11.0, -3.4), R(13.0, 12.8, 3.2), R(13.0, 11.6, 3.2), R(13.0, 12.2, -3.4),
                R(17.6, 11.3, -2.0), R(17.6, 12.4, 1.8), R(17.6, 11.8, 1.8), R(17.6, 12.0, -2.0)], 'team', bevel=0.1)
