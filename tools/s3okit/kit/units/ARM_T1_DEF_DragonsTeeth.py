"""Dragon's Teeth (ARM_T1_DEF_DragonsTeeth) - Arm wall piece. Kept bold and cheap: a low octagonal concrete plinth
with four big light pyramid spikes leaning outward to the four sides and a tall centre spike (the TA crown shape).
Identity from above: a light four-pointed star on a dark octagon, with a small team cap on the centre spike.
One piece (base); the feature `_dead` reuses this same model, so there is no separate wreck.
Coordinates are ENGINE/global: X right, Y up, Z forward."""
import math

UNIT = dict(res=1024)


def build(k):
    b = k.piece('base')
    oct8 = [(10.4 * math.cos(math.pi / 8 + i * math.pi / 4), 10.4 * math.sin(math.pi / 8 + i * math.pi / 4)) for i in range(8)]
    b.plan(0.0, 5.2, oct8, 'paint2', bevel=0.3, top_inset=0.8)
    b.plan(5.0, 7.4, [(x * 0.86, z * 0.86) for x, z in oct8], 'paint2', bevel=0.2, top_inset=3.0)   # low cap between the spikes
    # four outward-leaning spikes (pyramids from the plinth top to a point beyond the plinth)
    for ax, s in (('x', 1), ('x', -1), ('z', 1), ('z', -1)):
        def P(u, y, w):
            return (u * s, y, w) if ax == 'x' else (w, y, u * s)
        b.hull([P(u, 4.6, w) for u in (2.6, 9.6) for w in (-3.6, 3.6)] + [P(15.4, 13.4, 0.0)], 'paint', bevel=0.25)
    # centre spike, taller
    b.hull([(x, 4.6, z) for x in (-3.8, 3.8) for z in (-3.8, 3.8)] + [(0, 17.6, 0)], 'paint', bevel=0.25)
    b.hull([(x, 13.0, z) for x in (-1.15, 1.15) for z in (-1.15, 1.15)] + [(0, 17.75, 0)], 'team', bevel=0.0)
