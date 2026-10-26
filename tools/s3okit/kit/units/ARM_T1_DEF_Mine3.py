"""EG-3 (ARM_T1_DEF_Mine3) - Arm land mine. Mines are tiny 1x1 cloaked buildings: kept small, low and cheap, but every type has
its own plan shape and accent so a mine field can be read. Flat: a thin light pressure plate with a dark inner ring, a team trigger button and four short side tabs.
Pieces: Base (single piece, named so in the BOTA 3DO). No corpse. Coordinates are ENGINE/global: X right, Y up, Z forward."""
import math

UNIT = dict(res=1024)


def ngon(r, n, rot=0.0):
    return [(r * math.cos(rot + i * 2 * math.pi / n), r * math.sin(rot + i * 2 * math.pi / n)) for i in range(n)]


def build(k):
    b = k.piece('Base')
    b.cyl((0, 0.0, 0), (0, 0.9, 0), 6.0, 12, 'paint', r2=5.4, bevel=0.12)
    b.cyl((0, 0.85, 0), (0, 1.15, 0), 4.4, 12, 'dark')
    b.cyl((0, 1.1, 0), (0, 1.7, 0), 1.6, 10, 'team', r2=1.2)
    for x, z in ngon(1.0, 4, math.pi / 4):
        b.box((x * 6.0 - 1.0, 0.0, z * 6.0 - 1.0), (x * 6.0 + 1.0, 0.6, z * 6.0 + 1.0), 'paint2', bevel=0.1)
