"""M-515 (CORE_T1_DEF_Mine5) - Core large mine (second pattern). Mines are tiny 1x1 cloaked buildings: kept small, low and cheap, but every type has
its own plan shape and accent so a mine field can be read. Studded: a low wide octagonal dome with eight small dark anchor studs round it, ochre ring and team cap.
Pieces: ground (empty: the TA flat footprint quad is dropped), base. No corpse. Coordinates are ENGINE/global: X right, Y up, Z forward."""
import math

UNIT = dict(res=1024)


def ngon(r, n, rot=0.0):
    return [(r * math.cos(rot + i * 2 * math.pi / n), r * math.sin(rot + i * 2 * math.pi / n)) for i in range(n)]


def build(k):
    b = k.piece('base')
    b.plan(0.0, 1.2, ngon(6.4, 8, math.pi / 8), 'paint2', bevel=0.15, top_inset=0.5)
    b.plan(1.1, 3.4, ngon(5.4, 8, math.pi / 8), 'paint', bevel=0.15, top_inset=2.6)
    b.cyl((0, 1.15, 0), (0, 1.45, 0), 5.5, 8, 'hazard', r2=5.3, rot=math.pi / 8)
    b.cyl((0, 3.3, 0), (0, 3.8, 0), 1.9, 8, 'team', r2=1.4, rot=math.pi / 8)
    for x, z in ngon(8.6, 8):
        b.hull([(x + dx, 0.0, z + dz) for dx in (-0.8, 0.8) for dz in (-0.8, 0.8)] + [(x, 1.4, z)], 'dark', bevel=0.05)
