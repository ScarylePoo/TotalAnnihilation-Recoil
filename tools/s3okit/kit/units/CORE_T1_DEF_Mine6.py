"""M-610 (CORE_T1_DEF_Mine6) - Core nuclear mine. Mines are tiny 1x1 cloaked buildings: kept small, low and cheap, but every type has
its own plan shape and accent so a mine field can be read. Nuclear: a wide ribbed armoured hump (the TA beetle shape) with three dark ribs, red glowing slits and team spine plates.
Pieces: ground (empty: the TA flat footprint quad is dropped), base. No corpse. Coordinates are ENGINE/global: X right, Y up, Z forward."""
import math

UNIT = dict(res=1024)


def ngon(r, n, rot=0.0):
    return [(r * math.cos(rot + i * 2 * math.pi / n), r * math.sin(rot + i * 2 * math.pi / n)) for i in range(n)]


def build(k):
    b = k.piece('base')
    b.box((-8.6, 0.0, -6.4), (8.6, 1.2, 6.4), 'paint2', bevel=0.15)
    b.prism(-7.4, 7.4, [(-5.6, 1.0), (5.6, 1.0), (4.6, 3.6), (2.0, 4.6), (-2.0, 4.6), (-4.6, 3.6)], 'paint', bevel=0.15)
    for x in (-5.0, 0.0, 5.0):
        b.prism(x - 0.7, x + 0.7, [(-6.0, 0.8), (6.0, 0.8), (5.0, 3.9), (2.2, 5.0), (-2.2, 5.0), (-5.0, 3.9)], 'dark', bevel=0.08)
    for x in (-2.5, 2.5):
        b.box((x - 1.4, 2.6, 4.75), (x + 1.4, 3.2, 4.95), 'lightr', bevel=0.0)
        b.box((x - 1.4, 2.6, -4.95), (x + 1.4, 3.2, -4.75), 'lightr', bevel=0.0)
        b.box((x - 1.6, 4.55, -1.4), (x + 1.6, 4.75, 1.4), 'team', bevel=0.0)
