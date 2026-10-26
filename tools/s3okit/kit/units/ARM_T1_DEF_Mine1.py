"""Tiny (ARM_T1_DEF_Mine1) - Arm light mine. Mines are tiny 1x1 cloaked buildings: kept small, low and cheap, but every type has
its own plan shape and accent so a mine field can be read. Small: an octagonal light dome with a team cap and a ring of six short dark prongs.
Pieces: Base (single piece, named so in the BOTA 3DO). No corpse. Coordinates are ENGINE/global: X right, Y up, Z forward."""
import math

UNIT = dict(res=1024)


def ngon(r, n, rot=0.0):
    return [(r * math.cos(rot + i * 2 * math.pi / n), r * math.sin(rot + i * 2 * math.pi / n)) for i in range(n)]


def build(k):
    b = k.piece('Base')
    b.plan(0.0, 1.4, ngon(5.6, 8, math.pi / 8), 'paint2', bevel=0.15, top_inset=0.4)
    b.plan(1.3, 3.6, ngon(4.4, 8, math.pi / 8), 'paint', bevel=0.15, top_inset=1.6)
    b.cyl((0, 3.5, 0), (0, 3.9, 0), 1.6, 8, 'team', rot=math.pi / 8)
    for x, z in ngon(4.2, 6):
        b.cyl((x * 0.8, 2.2, z * 0.8), (x * 1.35, 3.6, z * 1.35), 0.5, 6, 'dark', r2=0.2)
