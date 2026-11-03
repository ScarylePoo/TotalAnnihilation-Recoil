"""Piranha (ARM_T2_SEA_Piranha) - Arm sub killer. The needle: the longest, narrowest Arm hull, a sharp spear point with
torpedo shoulders behind it, a pinched waist with a tall dark sail and thin swept planes, and a square stern block.
From above: a long light spike, team spearhead (a solid arrow on the raised forecastle), dark sail cross at the
waist, team-capped dark stern. Solid centre line and no wide parts, unlike the Lurker's hammerhead and the Fibber's slit.
Pieces (TA layout): base, flare1/2 (empty: torpedo points in the shoulders), wake (empty emit point at the stern).
The 3DO is slightly asymmetric (flare1 x 6.49, flare2 x -5.26); the hull is symmetric, tubes centred on them on average.
Submarine: def has waterline 40 and SHIP_SUBMARINE, no floater; run.py resolves water=40 from the movement class.
Coordinates are ENGINE/global: X right, Y up, Z forward. mirror=True builds the -X twin sharing UVs."""
import math

UNIT = dict(
    res=1024,
    wreck=dict(seed=26),
    preview_pose={},
)


def sect(z, r, h, yc=6.8):
    return [(math.cos(a) * r, yc + math.sin(a) * h, z) for a in [i * math.pi / 4 + math.pi / 8 for i in range(8)]]


def sym(pts):
    return [(x * s, y, z) for s in (-1, 1) for x, y, z in pts]


def build(k):
    b = k.piece('base')
    # ------------------------------------------------------------------ hull: pinched at the waist, spear bow
    b.hull(sect(-26.0, 5.6, 5.0) + sect(-6.0, 5.2, 5.0), 'paint', bevel=0.2)
    b.hull(sect(-6.0, 5.2, 5.0) + sect(9.0, 6.4, 5.4) + sect(26.0, 2.2, 2.0, 5.6) + sect(31.0, 0.4, 0.4, 5.2), 'paint', bevel=0.2)
    # torpedo shoulders (light, tubes dark)
    b.hull([(x, y, z) for x, y, z in
            [(4.6, 2.6, 7.0), (8.8, 3.4, 10.0), (8.8, 9.4, 10.0), (4.6, 10.6, 7.0),
             (5.0, 3.8, 25.6), (7.8, 5.0, 23.6), (7.8, 8.2, 23.6), (5.0, 8.8, 25.6)]], 'paint', bevel=0.2, mirror=True)
    b.cyl((5.9, 6.9, 24.2), (5.9, 6.9, 25.2), 1.15, 10, 'black', mirror=True)
    # spearhead: a solid raised forecastle wedge (narrower than the shoulders, which stay light) with a team arrow on top
    W = [(5.9, 10.2), (5.0, 21.0), (0.0, 29.6)]
    b.hull(sym([(x, 11.6 - (z - 10.2) * 0.26, z) for x, z in W] + [(0.0, 12.5, 7.6), (4.0, 5.0, 10.2), (2.0, 4.6, 26.0)]), 'paint', bevel=0.12)
    T = [(5.0, 11.2), (4.2, 20.6), (0.0, 27.6), (0.0, 9.0)]
    b.hull([(x, 11.6 - (z - 10.2) * 0.26 + (0.25 if x == 0.0 and z < 10 else 0.0) + dy, z) for dy in (0.02, 0.24) for x, z in T], 'team', bevel=0.03, mirror=True)
    # waist strake: a dark line down each flank between sail and stern
    b.hull([(x, y, z) for x, y, z in [(4.2, 9.6, -24.0), (5.8, 7.0, -24.0), (4.0, 9.6, -7.0), (5.4, 7.0, -7.0),
                                      (4.5, 9.9, -24.0), (6.1, 7.1, -24.0), (4.3, 9.9, -7.0), (5.7, 7.1, -7.0)]], 'paint2', bevel=0.05, mirror=True)
    # ------------------------------------------------------------------ sail: dark, tall, swept planes through it
    b.hull(sym([(3.2, 10.8, -9.0), (3.8, 11.0, 0.6), (2.4, 11.0, 5.4), (2.2, 15.8, -7.4), (2.6, 15.8, 0.0), (1.4, 15.8, 2.6)]), 'dark', bevel=0.18)
    b.hull([(x, y, z) for x, y, z in [(2.6, 13.0, 2.2), (11.4, 13.4, -4.2), (11.4, 13.4, -7.0), (2.6, 13.0, -4.0),
                                      (2.6, 14.2, 2.2), (11.4, 14.0, -4.2), (11.4, 14.0, -7.0), (2.6, 14.2, -4.0)]], 'paint2', bevel=0.1, mirror=True)
    b.cyl((0, 15.8, -3.4), (0, 18.6, -3.8), 0.4, 8, 'dark', r2=0.3)
    b.cyl((0, 18.6, -3.8), (0, 18.9, -3.8), 0.3, 6, 'lightc')
    # ------------------------------------------------------------------ stern block: square, dark, team top
    b.hull(sym([(5.6, 1.2, -25.0), (5.4, 11.4, -24.0), (8.2, 1.6, -26.0), (8.2, 13.2, -26.0), (8.2, 1.6, -30.8), (8.2, 13.2, -30.8)]), 'paint2', bevel=0.2)
    b.hull(sym([(7.4, 13.15, -26.6), (7.4, 13.15, -30.0), (7.4, 13.4, -26.6), (7.4, 13.4, -30.0)]), 'team', bevel=0.04)
    b.cyl((0, 6.5, -30.7), (0, 6.5, -31.1), 4.4, 12, 'black')
    b.box((8.15, 7.0, -29.0), (8.5, 8.4, -27.8), 'lightc', bevel=0.0, mirror=True)
