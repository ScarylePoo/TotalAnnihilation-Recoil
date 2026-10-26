"""HE Area Mine (ARM_T1_DEF_Mine4) - Arm wide-area mine, heavy charge. Mines are tiny 1x1 cloaked buildings: kept small, low and cheap, but every type has
its own plan shape and accent so a mine field can be read. Bell: a tall light bell with a team top and four low dark fins, hazard band round the waist.
Pieces: Base (single piece, named so in the BOTA 3DO). No corpse. Coordinates are ENGINE/global: X right, Y up, Z forward."""
import math

UNIT = dict(res=1024)


def ngon(r, n, rot=0.0):
    return [(r * math.cos(rot + i * 2 * math.pi / n), r * math.sin(rot + i * 2 * math.pi / n)) for i in range(n)]


def build(k):
    b = k.piece('Base')
    b.cyl((0, 0.0, 0), (0, 1.2, 0), 5.0, 8, 'paint2', rot=math.pi / 8, bevel=0.12)
    b.cyl((0, 1.2, 0), (0, 6.6, 0), 4.2, 8, 'paint', r2=2.0, rot=math.pi / 8, bevel=0.15)
    b.cyl((0, 2.6, 0), (0, 3.4, 0), 3.85, 8, 'hazard', r2=3.55, rot=math.pi / 8)
    b.cyl((0, 6.5, 0), (0, 7.0, 0), 2.1, 8, 'team', r2=1.6, rot=math.pi / 8)
    for x, z in ngon(1.0, 4):
        b.hull([(x * 3.0 + z * w, 0.0, z * 3.0 - x * w) for w in (-0.5, 0.5)] +
               [(x * 3.0 + z * w, 3.6, z * 3.0 - x * w) for w in (-0.5, 0.5)] +
               [(x * 9.0 + z * w, 0.0, z * 9.0 - x * w) for w in (-0.5, 0.5)], 'dark', bevel=0.06)
