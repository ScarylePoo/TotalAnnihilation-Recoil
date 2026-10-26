"""EG-6 (ARM_T1_DEF_Mine6) - Arm nuclear mine. Mines are tiny 1x1 cloaked buildings: kept small, low and cheap, but every type has
its own plan shape and accent so a mine field can be read. Nuclear: a squat light canister on two dark side arms, glowing red core windows, a hazard collar and a team cap.
Pieces: Base (single piece, named so in the BOTA 3DO). No corpse. Coordinates are ENGINE/global: X right, Y up, Z forward."""
import math

UNIT = dict(res=1024)


def ngon(r, n, rot=0.0):
    return [(r * math.cos(rot + i * 2 * math.pi / n), r * math.sin(rot + i * 2 * math.pi / n)) for i in range(n)]


def build(k):
    b = k.piece('Base')
    b.cyl((0, 0.0, 0), (0, 1.2, 0), 6.2, 12, 'paint2', bevel=0.12)
    b.cyl((0, 1.1, 0), (0, 7.4, 0), 4.0, 12, 'paint', bevel=0.15)
    b.cyl((0, 5.4, 0), (0, 6.4, 0), 4.15, 12, 'hazard')
    b.cyl((0, 7.3, 0), (0, 7.8, 0), 2.8, 12, 'team')
    b.box((-1.4, 2.4, 3.9), (1.4, 4.6, 4.15), 'lightr', bevel=0.0)
    b.box((-1.4, 2.4, -4.15), (1.4, 4.6, -3.9), 'lightr', bevel=0.0)
    for s in (-1, 1):
        b.hull([(s * 3.6, y, z) for y in (1.2, 6.0) for z in (-1.2, 1.2)] + [(s * 9.0, 0.0, z) for z in (-1.4, 1.4)] +
               [(s * 9.0, 1.4, z) for z in (-1.2, 1.2)], 'dark', bevel=0.1)
