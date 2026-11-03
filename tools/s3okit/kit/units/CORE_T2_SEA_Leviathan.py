"""Leviathan (CORE_T2_SEA_Leviathan) - Core battle sub. A 3x3 footprint cannot read big, so it reads as a shape nothing else
in the water has: a trident. Two long light outrigger hulls far out on broad dark swept wings, a heavy central hull with a
raised bow arrowhead, and one thick team stripe (the sealed spine doors) running nearly its whole length.
From above: the widest sub, two light steel bars, dark wings between them, a team spine, nearly as wide as long.
Pieces (TA layout): base, door1/door2 (spine hatches, explode only: door2 = mirrored clone), btmcover (keel plate, explode
only), bubbles1/2 and torp1/2 (empty emit and torpedo points).
Submarine: def has waterline 40 and SHIP_SUBMARINE, no floater; run.py resolves water=40 from the movement class.
Coordinates are ENGINE/global: X right, Y up, Z forward. mirror=True builds the -X twin sharing UVs."""

UNIT = dict(
    res=1024,
    wreck=dict(seed=29, drop=['door2'], pose={'door1': (0, 0, 35)}),
    preview_pose={},
)

DY = 10.01          # door top height in the 3DO


def sym(pts):
    return [(x * s, y, z) for s in (-1, 1) for x, y, z in pts]


def build(k):
    b = k.piece('base')
    # ------------------------------------------------------------------ central hull: heavy, dark, stepped spine on top
    b.hull(sym([(6.0, 0.4, -24.0), (8.6, 4.0, -22.0), (5.0, 9.8, -24.0),
                (6.0, 0.4, 16.0), (8.0, 4.0, 16.0), (5.0, 9.8, 16.0)]), 'paint', bevel=0.22)
    # raised spine: the doors sit on it
    b.hull(sym([(5.0, 8.6, -27.0), (5.0, 8.6, 20.0), (3.9, DY - 0.1, -26.4), (3.9, DY - 0.1, 19.6)]), 'paint2', bevel=0.12)
    # ------------------------------------------------------------------ neck and raised bow arrowhead (light steel plates)
    b.hull(sym([(5.0, 1.0, 14.0), (5.0, 9.4, 14.0), (4.6, 1.0, 21.0), (4.6, 9.0, 21.0)]), 'paint', bevel=0.18)
    b.hull(sym([(5.0, 0.6, 19.4), (11.4, 4.8, 21.2), (4.0, 0.6, 32.0), (4.0, 1.5, 32.2), (5.0, 5.2, 19.4)]), 'paint', bevel=0.2)
    b.hull(sym([(5.0, 11.0, 19.4), (0.0, 12.0, 19.4), (5.0, 5.0, 19.4), (11.7, 6.6, 21.4), (11.7, 5.0, 21.4),
                (4.3, 3.0, 32.5), (4.3, 1.4, 32.5)]), 'steel', bevel=0.14)
        # ------------------------------------------------------------------ broad swept wings (the darkest mass)
    b.hull([(x, y, z) for y in (3.2, 5.8) for x, z in [(7.2, 10.0), (20.6, 2.0), (20.6, -15.0), (7.2, -15.0)]], 'dark', bevel=0.18, mirror=True)
    b.hull([(x, y, z) for x, y, z in [(9.0, 5.75, 2.0), (18.6, 5.75, -3.0), (18.6, 5.75, -9.0), (9.0, 5.75, -9.0),
                                      (9.0, 5.95, 2.0), (18.6, 5.95, -3.0), (18.6, 5.95, -9.0), (9.0, 5.95, -9.0)]], 'team', bevel=0.04, mirror=True)
    # ------------------------------------------------------------------ outriggers: long, light, tubes forward
    pod = [(x, y, z) for z in (-22.0, -2.0) for x, y in ((20.0, 2.0), (27.6, 2.0), (28.2, 8.0), (27.0, 9.6), (20.8, 9.6), (19.4, 8.0))]
    pod += [(x, y, 4.4) for x, y in ((21.6, 3.2), (26.0, 3.2), (26.0, 7.6), (21.6, 7.6))]
    pod += [(x, y, -26.4) for x, y in ((21.8, 4.0), (25.8, 4.0), (25.8, 7.4), (21.8, 7.4))]
    b.hull(pod, 'steel', bevel=0.22, mirror=True)
    b.cyl((23.8, 5.4, 4.3), (23.8, 5.4, 4.9), 1.7, 10, 'black', mirror=True)
    b.cyl((23.8, 5.4, -26.2), (23.8, 5.4, -26.8), 1.7, 10, 'lightr', mirror=True)
    # ------------------------------------------------------------------ twin stern nacelles + inner fins
    nac = [(x, y, z) for z in (-18.0, -29.0) for x, y in ((3.4, 1.2), (10.4, 1.2), (11.0, 5.0), (10.0, 8.8), (4.0, 8.8), (3.0, 5.0))]
    nac += [(5.4, 3.0, -32.0), (8.6, 3.0, -32.0), (8.6, 7.0, -32.0), (5.4, 7.0, -32.0)]
    b.hull(nac, 'paint2', bevel=0.2, mirror=True)
    b.cyl((7.0, 5.1, -31.8), (7.0, 5.1, -32.4), 1.6, 10, 'black', mirror=True)
    # ------------------------------------------------------------------ spine hatches: the single thick team stripe
    d = k.piece('door1')
    d.box((-3.53, DY - 0.45, -26.2), (-0.03, DY + 0.3, 19.3), 'team', bevel=0.05)
    k.clone('door2', 'door1', mirror_x=True)
    # keel plate: small and unseen
    k.piece('btmcover').box((-3.6, 0.0, -26.4), (3.6, 0.3, 3.6), 'dark', bevel=0.0)
