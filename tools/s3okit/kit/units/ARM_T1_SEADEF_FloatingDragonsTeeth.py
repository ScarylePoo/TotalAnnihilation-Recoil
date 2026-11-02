"""Floating Dragon's Teeth (ARM_T1_SEADEF_FloatingDragonsTeeth) - Arm naval wall piece. Waterline 4 (the water surface
is model y = 4). Kept bold and cheap like the land teeth: a dark octagonal float (3 elmo freeboard, light rub ring at
the waterline), four big light pyramid spikes leaning out to the four DIAGONALS (the land teeth point along the axes)
and a tall centre spike with a small team cap; a plain ballast keel cone hangs underneath.
Identity from above: a light X-shaped star on a dark octagon ringed light - low team colour on purpose (wall piece).
One piece (base); the feature reuses this same model, so there is no separate wreck.
Coordinates are ENGINE/global: X right, Y up, Z forward."""
import math

WL = 4.0
UNIT = dict(res=1024, ground=False, water=WL)


def build(k):
    b = k.piece('Base')
    oct8 = [(12.0 * math.cos(i * math.pi / 4), 12.0 * math.sin(i * math.pi / 4)) for i in range(8)]
    b.hull([(x * 0.8, -3.0, z * 0.8) for x, z in oct8] + [(x, 2.0, z) for x, z in oct8]
           + [(x * 0.95, 7.0, z * 0.95) for x, z in oct8], 'paint2', bevel=0.3)
    b.hull([(x * s, y, z * s) for x, z in oct8 for s in (1.0, 1.04) for y in (3.0, 5.0)], 'paint', bevel=0.1)
    b.plan(6.8, 8.6, [(x * 0.7, z * 0.7) for x, z in oct8], 'paint2', bevel=0.2, top_inset=2.4)
    # four outward-leaning spikes to the diagonals
    for ang in (45, 135, 225, 315):
        c, s = math.cos(math.radians(ang)), math.sin(math.radians(ang))
        R = lambda u, y, w: (c * u - s * w, y, s * u + c * w)
        b.hull([R(u, 6.4, w) for u in (2.8, 10.4) for w in (-3.8, 3.8)] + [R(16.8, 15.0, 0.0)], 'paint', bevel=0.25)
    # centre spike, taller, with a team cap
    b.hull([(x, 6.8, z) for x in (-4.0, 4.0) for z in (-4.0, 4.0)] + [(0, 22.0, 0)], 'paint', bevel=0.25)
    b.hull([(x, 16.4, z) for x in (-1.75, 1.75) for z in (-1.75, 1.75)] + [(0, 22.3, 0)], 'team', bevel=0.0)
    # ballast keel (always submerged)
    b.cyl((0, -3.2, 0), (0, -15.0, 0), 6.0, 8, 'dark', r2=1.0, rot=math.pi / 8)
