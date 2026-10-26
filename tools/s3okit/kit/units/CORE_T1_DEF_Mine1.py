"""M-104 (CORE_T1_DEF_Mine1) - Core light mine. Mines are tiny 1x1 cloaked buildings: kept small, low and cheap, but every type has
its own plan shape and accent so a mine field can be read. Small: a low dark dome on a square plate, ochre ring and team crown.
Pieces: ground (empty: the TA flat footprint quad is dropped), base. No corpse. Coordinates are ENGINE/global: X right, Y up, Z forward."""
import math

UNIT = dict(res=1024)


def ngon(r, n, rot=0.0):
    return [(r * math.cos(rot + i * 2 * math.pi / n), r * math.sin(rot + i * 2 * math.pi / n)) for i in range(n)]


def build(k):
    b = k.piece('base')
    b.box((-5.6, 0.0, -5.6), (5.6, 0.9, 5.6), 'paint2', bevel=0.15)
    b.sphere((0, 0.6, 0), 4.2, 'paint', segs=10, rings=5, scale=(1, 0.75, 1))
    b.cyl((0, 3.0, 0), (0, 3.4, 0), 2.2, 10, 'hazard')
    b.cyl((0, 3.3, 0), (0, 3.9, 0), 1.2, 10, 'team', r2=0.8)
