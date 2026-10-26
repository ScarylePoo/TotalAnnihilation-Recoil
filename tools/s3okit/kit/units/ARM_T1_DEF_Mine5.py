"""EG-5 (ARM_T1_DEF_Mine5) - Arm large mine. Mines are tiny 1x1 cloaked buildings: kept small, low and cheap, but every type has
its own plan shape and accent so a mine field can be read. Large: a broad stepped octagonal drum, dark sides with ribs, a light top with a team ring.
Pieces: Base (single piece, named so in the BOTA 3DO). No corpse. Coordinates are ENGINE/global: X right, Y up, Z forward."""
import math

UNIT = dict(res=1024)


def ngon(r, n, rot=0.0):
    return [(r * math.cos(rot + i * 2 * math.pi / n), r * math.sin(rot + i * 2 * math.pi / n)) for i in range(n)]


def build(k):
    b = k.piece('Base')
    b.plan(0.0, 3.2, ngon(7.2, 8, math.pi / 8), 'paint2', bevel=0.2, top_inset=0.6)
    b.plan(3.1, 5.4, ngon(6.0, 8, math.pi / 8), 'paint', bevel=0.18, top_inset=1.4)
    b.cyl((0, 5.3, 0), (0, 5.6, 0), 3.4, 8, 'team', rot=math.pi / 8)
    b.cyl((0, 5.55, 0), (0, 6.2, 0), 1.6, 8, 'dark', rot=math.pi / 8)
    for x, z in ngon(6.8, 8, math.pi / 8):
        b.box((x - 0.4, 0.3, z - 0.4), (x + 0.4, 2.8, z + 0.4), 'dark', bevel=0.0)
