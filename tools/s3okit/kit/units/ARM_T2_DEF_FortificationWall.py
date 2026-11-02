"""Fortification Wall (ARM_T2_DEF_FortificationWall) - Arm T2 wall block. Kept cheap and bold like the Dragon's Teeth
(team colour low on purpose): five tall light pylons with pointed caps - one in the centre and one on each axis - tied
together by three tiers of dark girders, the TA cross plan. Taller and heavier than the Arm Dragon's Teeth, and the
only Arm wall that reads as a '+' from above.
Identity from above: a light plus sign of five pointed pylon tops on dark girders, a small team cap on the centre
pylon only. One piece (Base); the feature `_dead` reuses this same model, so there is no separate wreck.
Coordinates are ENGINE/global: X right, Y up, Z forward."""
import math

UNIT = dict(res=1024)


def pylon(b, cx, cz, r, h, cap, mat='paint'):
    """square pylon with chamfered corners and a pyramid cap"""
    sq = [(cx + x, cz + z) for x, z in ((-r, -r * 0.6), (-r * 0.6, -r), (r * 0.6, -r), (r, -r * 0.6),
                                        (r, r * 0.6), (r * 0.6, r), (-r * 0.6, r), (-r, r * 0.6))]
    b.plan(0.0, h, sq, mat, bevel=0.2, top_inset=r * 0.18)
    b.hull([(x, h - 0.1, z) for x, z in [(cx + (xx - cx) * 0.86, cz + (zz - cz) * 0.86) for xx, zz in sq]] +
           [(cx, h + cap, cz)], mat, bevel=0.15)


def build(k):
    b = k.piece('Base')
    # dark footing cross under everything
    for ax in ('x', 'z'):
        lo, hi = ((-16.0, -3.4), (16.0, 3.4)) if ax == 'x' else ((-3.4, -16.0), (3.4, 16.0))
        b.box((lo[0], 0.0, lo[1]), (hi[0], 2.2, hi[1]), 'paint2', bevel=0.2)
    # girders: three tiers along both axes (dark, chunky so they read between the pylons)
    for y in (8.0, 17.0, 26.0):
        b.box((-14.0, y, -1.4), (14.0, y + 2.6, 1.4), 'dark', bevel=0.15)
        b.box((-1.4, y, -14.0), (1.4, y + 2.6, 14.0), 'dark', bevel=0.15)
    # pylons: centre tallest, the four arms a little lower
    pylon(b, 0.0, 0.0, 4.2, 30.0, 8.0)
    for cx, cz in ((14.2, 0.0), (-14.2, 0.0), (0.0, 14.2), (0.0, -14.2)):
        pylon(b, cx, cz, 3.0, 27.0, 7.0)
        # buttress fins at the foot of each outer pylon, along the arm
        ux, uz = (1 if cx > 0 else -1 if cx < 0 else 0), (1 if cz > 0 else -1 if cz < 0 else 0)
        px, pz = -uz, ux
        b.hull([(cx + px * w, 0.0, cz + pz * w) for w in (-6.4, 6.4)] + [(cx + px * w, 9.0, cz + pz * w) for w in (-2.4, 2.4)] +
               [(cx + px * w + ux * 1.6, y, cz + pz * w + uz * 1.6) for w in (-6.4, 6.4) for y in (0.0,)] +
               [(cx + px * w - ux * 1.6, y, cz + pz * w - uz * 1.6) for w in (-6.4, 6.4) for y in (0.0,)], 'paint2', bevel=0.15)
    # team cap on the centre pylon only (walls stay low on team colour)
    b.hull([(x, 32.6, z) for x in (-2.7, 2.7) for z in (-2.7, 2.7)] + [(0.0, 38.3, 0.0)], 'team', bevel=0.0)
