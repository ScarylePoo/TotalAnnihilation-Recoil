"""Area Mine (ARM_T1_DEF_Mine2) - Arm wide-area mine, light charge. Mines are tiny 1x1 cloaked buildings: kept small, low and cheap, but every type has
its own plan shape and accent so a mine field can be read. Wide: a light disc with four big outward hazard spikes (a cross) and a team hub.
Pieces: Base (single piece, named so in the BOTA 3DO). No corpse. Coordinates are ENGINE/global: X right, Y up, Z forward."""
import math

UNIT = dict(res=1024)


def ngon(r, n, rot=0.0):
    return [(r * math.cos(rot + i * 2 * math.pi / n), r * math.sin(rot + i * 2 * math.pi / n)) for i in range(n)]


def build(k):
    b = k.piece('Base')
    b.plan(0.0, 1.6, ngon(6.4, 8, math.pi / 8), 'paint', bevel=0.15, top_inset=0.8)
    b.cyl((0, 1.5, 0), (0, 2.8, 0), 2.8, 8, 'team', r2=2.2, rot=math.pi / 8, bevel=0.08)
    for x, z in ngon(1.0, 4):
        b.hull([(x * 2.6 + z * w, 1.0, z * 2.6 - x * w) for w in (-1.3, 1.3)] +
               [(x * 2.6 + z * w, 2.2, z * 2.6 - x * w) for w in (-0.9, 0.9)] + [(x * 10.6, 3.6, z * 10.6)], 'hazard', bevel=0.08)
