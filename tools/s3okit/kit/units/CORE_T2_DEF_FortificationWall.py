"""Fortification Wall (CORE_T2_DEF_FortificationWall) - Core T2 wall block. Kept cheap and bold like the Dragon's Teeth
(team colour low on purpose): a dark square-pyramid spire on a diamond base plate, bristling with three tiers of
fat light steel spikes along both axes - the TA 'spiked spire'.
Identity from above: a light steel cross of spikes reaching past a dark diamond plate, team tabs on the plate tips,
a small team cap on the spire. The Arm wall is a '+' of five light pylons instead.
One piece (wallbase2); the feature `_dead` reuses this same model, so there is no separate wreck.
Coordinates are ENGINE/global: X right, Y up, Z forward."""
import math

UNIT = dict(res=1024)


def build(k):
    b = k.piece('wallbase2')
    # diamond base plate (rotated square), two steps
    dia = lambda r: [(r, 0.0), (0.0, r), (-r, 0.0), (0.0, -r)]
    b.plan(0.0, 2.4, dia(19.0), 'paint2', bevel=0.3, top_inset=1.0)
    b.plan(2.2, 4.4, dia(14.0), 'paint', bevel=0.25, top_inset=1.6)
    # team tabs on the four plate tips (the only team besides the spire cap)
    for ux, uz in ((1, 0), (-1, 0), (0, 1), (0, -1)):
        px, pz = -uz, ux
        b.hull([(ux * u + px * w, y, uz * u + pz * w) for u, hw in ((14.2, 3.4), (17.4, 1.0)) for w in (-hw, hw)
                for y in (2.0, 2.55)], 'team', bevel=0.04)
    # spire: square pyramid frustum aligned to the axes
    b.plan(4.0, 33.0, [(-7.2, -7.2), (7.2, -7.2), (7.2, 7.2), (-7.2, 7.2)], 'paint', bevel=0.3, top_inset=6.4)
    # dark corner ribs on the spire
    for s in (-1, 1):
        for t in (-1, 1):
            b.hull([(x * s, y, z * t) for x, y, z in
                    ((7.6, 4.2, 6.0), (6.0, 4.2, 7.6), (7.6, 4.2, 7.6), (2.9, 32.0, 2.2), (2.2, 32.0, 2.9), (2.9, 32.0, 2.9))],
                   'dark', bevel=0.06)
    b.box((-2.6, 32.6, -2.6), (2.6, 35.0, 2.6), 'dark', bevel=0.2)
    b.hull([(x, 34.9, z) for x in (-2.0, 2.0) for z in (-2.0, 2.0)] + [(0.0, 37.1, 0.0)], 'team', bevel=0.0)
    # spikes: three tiers, along x on one tier set and z on the other, light steel with dark collars
    for y, ax in ((9.0, 'x'), (14.0, 'z'), (19.0, 'x'), (24.0, 'z'), (29.0, 'x')):
        r_out = 17.6 - (y - 9.0) * 0.18
        for sg in (-1, 1):
            p0 = (sg * 3.0, y, 0.0) if ax == 'x' else (0.0, y, sg * 3.0)
            p1 = (sg * r_out, y, 0.0) if ax == 'x' else (0.0, y, sg * r_out)
            p2 = (sg * (r_out + 3.4), y, 0.0) if ax == 'x' else (0.0, y, sg * (r_out + 3.4))
            b.cyl(p0, p1, 1.9, 6, 'steel', rot=math.pi / 6)
            b.cyl(p1, p2, 1.9, 6, 'steel', r2=0.25, rot=math.pi / 6)
            pc = (sg * 6.6, y, 0.0) if ax == 'x' else (0.0, y, sg * 6.6)
            pc1 = (sg * 8.4, y, 0.0) if ax == 'x' else (0.0, y, sg * 8.4)
            b.cyl(pc, pc1, 2.5, 6, 'dark', rot=math.pi / 6)
