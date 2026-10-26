"""M-515 (CORE_T1_DEF_Mine3) - Core large mine. Mines are tiny 1x1 cloaked buildings: kept small, low and cheap, but every type has
its own plan shape and accent so a mine field can be read. Large: a broad square pyramid frustum with an ochre top band and a short team detonator post.
Pieces: ground (empty: the TA flat footprint quad is dropped), base. No corpse. Coordinates are ENGINE/global: X right, Y up, Z forward."""
import math

UNIT = dict(res=1024)


def ngon(r, n, rot=0.0):
    return [(r * math.cos(rot + i * 2 * math.pi / n), r * math.sin(rot + i * 2 * math.pi / n)) for i in range(n)]


def build(k):
    b = k.piece('base')
    b.plan(0.0, 4.6, [(-7.6, -7.6), (7.6, -7.6), (7.6, 7.6), (-7.6, 7.6)], 'paint', bevel=0.2, top_inset=3.4)
    b.hull([(x, y, z) for x, z in [(-4.6, -4.6), (4.6, -4.6), (4.6, 4.6), (-4.6, 4.6)] for y in (4.6, 4.8)], 'hazard', bevel=0.0)
    b.hull([(x, y, z) for x, z in [(-3.2, -3.2), (3.2, -3.2), (3.2, 3.2), (-3.2, 3.2)] for y in (4.75, 4.95)], 'paint2', bevel=0.0)
    b.box((-0.9, 4.8, -0.9), (0.9, 7.6, 0.9), 'dark', bevel=0.1)
    b.box((-1.1, 7.5, -1.1), (1.1, 8.1, 1.1), 'team', bevel=0.08)
