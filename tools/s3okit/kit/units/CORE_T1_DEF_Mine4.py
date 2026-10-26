"""M-420 (CORE_T1_DEF_Mine4) - Core heavy mine. Mines are tiny 1x1 cloaked buildings: kept small, low and cheap, but every type has
its own plan shape and accent so a mine field can be read. Ring: a flat dark ten-sided ring with ochre studs, joined by one bar to a team-capped centre.
Pieces: ground (empty: the TA flat footprint quad is dropped), base. No corpse. Coordinates are ENGINE/global: X right, Y up, Z forward."""
import math

UNIT = dict(res=1024)


def ngon(r, n, rot=0.0):
    return [(r * math.cos(rot + i * 2 * math.pi / n), r * math.sin(rot + i * 2 * math.pi / n)) for i in range(n)]


def build(k):
    b = k.piece('base')
    for i in range(10):
        a0, a1 = i * math.pi / 5, (i + 1) * math.pi / 5
        pts = [(r * math.cos(a), y, r * math.sin(a)) for a in (a0, a1) for r in (5.2, 7.4) for y in (0.0, 1.5)]
        b.hull(pts, 'paint2', bevel=0.08)
        if i % 2 == 0:
            am = (a0 + a1) / 2
            b.box((6.3 * math.cos(am) - 0.4, 1.4, 6.3 * math.sin(am) - 0.4), (6.3 * math.cos(am) + 0.4, 1.75, 6.3 * math.sin(am) + 0.4), 'hazard', bevel=0.0)
    b.box((0.0, 0.0, -0.8), (5.4, 1.1, 0.8), 'paint', bevel=0.1)
    b.cyl((0, 0.0, 0), (0, 2.2, 0), 2.6, 10, 'paint', r2=1.8, bevel=0.1)
    b.cyl((0, 2.1, 0), (0, 2.6, 0), 1.7, 10, 'team', r2=1.2)
