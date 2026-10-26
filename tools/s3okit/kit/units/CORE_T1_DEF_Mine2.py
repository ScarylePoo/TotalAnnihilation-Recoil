"""M-303 (CORE_T1_DEF_Mine2) - Core land mine. Mines are tiny 1x1 cloaked buildings: kept small, low and cheap, but every type has
its own plan shape and accent so a mine field can be read. Flat cluster: a small team-capped hub with four low dark warhead blocks round it (an X), no base plate.
Pieces: ground (empty: the TA flat footprint quad is dropped), base. No corpse. Coordinates are ENGINE/global: X right, Y up, Z forward."""
import math

UNIT = dict(res=1024)


def ngon(r, n, rot=0.0):
    return [(r * math.cos(rot + i * 2 * math.pi / n), r * math.sin(rot + i * 2 * math.pi / n)) for i in range(n)]


def build(k):
    b = k.piece('base')
    b.cyl((0, 0.0, 0), (0, 1.8, 0), 1.9, 8, 'paint', r2=1.4, rot=math.pi / 8, bevel=0.1)
    b.cyl((0, 1.75, 0), (0, 2.2, 0), 1.2, 8, 'team', rot=math.pi / 8)
    for x, z in ngon(1.0, 4, math.pi / 4):
        b.hull([(x * 3.0 + z * w, 0.0, z * 3.0 - x * w) for w in (-1.6, 1.6)] +
               [(x * 6.6 + z * w, 0.0, z * 6.6 - x * w) for w in (-1.8, 1.8)] +
               [(x * 3.2 + z * w, 1.6, z * 3.2 - x * w) for w in (-1.2, 1.2)] +
               [(x * 6.0 + z * w, 1.2, z * 6.0 - x * w) for w in (-1.4, 1.4)], 'paint2', bevel=0.12)
        b.box((x * 5.2 - 0.5, 1.3, z * 5.2 - 0.5), (x * 5.2 + 0.5, 1.55, z * 5.2 + 0.5), 'hazard', bevel=0.0)
