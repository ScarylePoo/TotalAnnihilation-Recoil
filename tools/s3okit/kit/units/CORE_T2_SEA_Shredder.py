"""Shredder (CORE_T2_SEA_Shredder) - Core T2 anti-air ship. Slim hull with a midship sponson bulge; the tell is the tall
slim column amidships carrying a wide flak head with two very long bright guns, high above the deck, and two big SAM
boxes on yokes at bow and stern, both facing forward.
Pieces (TA layout): groundplane (empty root), wakeL/R (empty), base, turretA/B (turn y), boxA/B (turn x), emitterA/B
(empty), platformA, turretgun (column), turret2 (flak head, turn x + y), turret1 (cap, static), guns/guns2 (recoil 6
along z), flareR/L (empty).
Value groups from above: dark deck (paint), darker sponsons/column/yokes (paint2, dark), black launcher faces, bright
steel flak barrels, team on the box roofs, head shoulders and cap, sponson tops.
Floater, no waterline (water surface at model y = 0). Deck is flat at y 7 (no sheer: the plates sit on real heights).
Coordinates are ENGINE/global: X right, Y up, Z forward. mirror=True builds the -X twin sharing UVs."""

UNIT = dict(
    res=1024,
    wreck=dict(seed=31, drop=['boxB'], pose={'turret2': (12, 40, 0), 'turretA': (0, -30, 0)}),
    preview_pose={'turret2': (-6, 0, 0), 'boxA': (-10, 0, 0), 'boxB': (-10, 0, 0)},
)

DECK = 7.0
WL = [(0.0, 42.0), (2.5, 41.2), (11.2, 26.9), (15.0, 10.0), (15.0, -18.1), (12.5, -36.2), (7.5, -40.6)]
TOP = [(0.0, 37.6), (0.3, 37.2), (7.5, 25.4), (11.3, 8.2), (11.3, -16.7), (8.7, -34.2), (6.0, -36.6)]


def ring(pts, y, sx=1.0, sz=1.0, dz=0.0):
    return [(x * sx * s, y, z * sz + dz) for x, z in pts for s in ((-1, 1) if x > 0 else (1,))]


def sam_turret(k, tn, bn):
    t = k.piece(tn); T = t.at
    t.cyl(T(0, -0.9, -2.6), T(0, 0.8, -2.6), 7.2, 14, 'dark', r2=6.6, bevel=0.06)
    for s in (-1, 1):       # origin x = -0.12: built whole
        t.hull([T(s * x, y, z) for x in (5.9, 8.0) for y, z in [(0.2, -6.8), (0.2, 1.3), (6.4, 2.0), (8.0, -0.2), (8.0, -4.2), (6.4, -6.6)]],
               'paint2', bevel=0.12)
    t.box(T(-8.2, 5.4, -1.4), T(8.2, 6.8, 1.4), 'dark', bevel=0.08)
    bx = k.piece(bn); B = bx.at
    pf = [(-4.9, -4.2), (4.9, -4.0), (5.2, 6.5), (4.0, 7.8), (-0.6, 9.2), (-1.5, 6.5)]
    bx.hull([B(x, y, z) for x in (-5.6, 5.6) for y, z in pf], 'paint', bevel=0.16)
    # black launcher face on the slanted nose, six tube mouths
    bx.hull([B(x, y, z) for x in (-4.8, 4.8) for y, z in [(3.6, 7.98), (-0.2, 9.22), (3.6, 8.2), (-0.2, 9.44)]], 'black', bevel=0.0)
    for x in (-3.2, 0.0, 3.2):
        for y, z in ((2.7, 8.5), (0.7, 9.15)):
            bx.cyl(B(x, y, z), B(x, y + 0.06, z + 0.25), 0.8, 8, 'steel')
    # team roof
    bx.hull([B(x, y, z) for x in (-4.8, 4.8) for y, z in [(4.96, -3.3), (5.26, 5.9), (5.14, -3.3), (5.44, 5.9)]], 'team', bevel=0.03)
    bx.box(B(-6.2, -1.4, -1.6), B(6.2, 1.4, 1.6), 'dark', bevel=0.1)      # trunnion block
    bx.box(B(-3.6, -3.4, -4.7), B(3.6, 2.4, -4.1), 'dark', bevel=0.05)    # rear hatch


def build(k):
    b = k.piece('base')
    # ------------------------------------------------------------------ hull (crosses x = 0)
    b.hull(ring(WL, -2.0, 0.65, 0.9, -1.0) + ring(WL, 0.0), 'paint2', bevel=0.18)
    b.hull(ring(WL, 0.0) + ring(TOP, DECK - 0.5), 'paint2', bevel=0.18)
    b.hull(ring(TOP, DECK - 0.5) + ring(TOP, DECK, 0.985, 0.99), 'paint', bevel=0.12)
    # midship sponson bulge: its own hull (raised, so never coplanar with the deck)
    b.hull([(x, 0.0, z) for x, z in [(12.0, 11.0), (18.1, 6.2), (18.1, -13.1), (12.0, -19.0)]] +
           [(x, -1.6, z) for x, z in [(11.0, 7.0), (15.0, 3.0), (15.0, -10.0), (11.0, -14.0)]] +
           [(x, 7.4, z) for x, z in [(9.6, 8.8), (14.1, 4.8), (14.1, -12.0), (9.6, -16.7)]], 'paint2', bevel=0.16, mirror=True)
    b.hull([(x, y, z) for y in (7.46, 7.62) for x, z in [(9.9, 7.4), (13.7, 4.4), (13.7, -11.6), (9.9, -15.4)]], 'team', bevel=0.03, mirror=True)
    b.box((14.0, 5.0, -8.0), (14.5, 5.7, 1.0), 'lightc', bevel=0.0, mirror=True)
    # raised forecastle wedge (separate hull: leaves the main deck flat), anchor plate, bow light
    b.hull([(x * s, y, z) for s in (-1, 1) for x, y, z in
            [(3.0, 6.8, 31.5), (2.0, 6.8, 34.6), (3.0, 7.4, 31.5), (1.4, 8.0, 36.2), (0.2, 6.8, 37.0), (0.2, 8.0, 37.0)]], 'dark', bevel=0.05)
    b.cyl((0, 7.9, 35.8), (0, 8.5, 35.8), 0.34, 6, 'lightr')
    # aft deck vents, stern light, bollards
    for x in (-4.0, -1.2, 1.6):
        b.box((x, DECK - 0.05, -36.0), (x + 2.2, DECK + 0.2, -33.0), 'black', bevel=0.0)
    b.box((-2.0, 4.6, -36.8), (2.0, 5.3, -36.45), 'lightr', bevel=0.0)
    # walkway plates between launchers and platform (lighter steel-capped rails give the deck a value step)
    b.box((-3.2, DECK - 0.05, 8.0), (3.2, DECK + 0.26, 17.6), 'dark', bevel=0.05)
    for z in (9.4, 11.8, 14.2):
        b.box((-2.4, DECK + 0.2, z), (2.4, DECK + 0.38, z + 1.2), 'black', bevel=0.0)
    b.box((-3.2, DECK - 0.05, -21.2), (3.2, DECK + 0.26, -16.8), 'dark', bevel=0.05)

    # ------------------------------------------------------------------ SAM boxes on yokes
    sam_turret(k, 'turretA', 'boxA')
    k.clone('turretB', 'turretA')
    k.clone('boxB', 'boxA')

    # ------------------------------------------------------------------ platform + column
    pa = k.piece('platformA')
    pa.hull([(x, 6.9, z) for x, z in [(9.4, -14.6), (9.4, 8.5), (6.9, 11.0), (-6.9, 11.0), (-9.4, 8.5), (-9.4, -14.6), (-6.9, -17.1), (6.9, -17.1)]] +
            [(x, 9.4, z) for x, z in [(7.4, -13.8), (7.4, 7.7), (6.0, 9.0), (-6.0, 9.0), (-7.4, 7.7), (-7.4, -13.8), (-6.0, -15.1), (6.0, -15.1)]],
            'paint', bevel=0.14)
    pa.box((9.0, 7.6, -8.0), (9.3, 8.2, 2.0), 'lightw', bevel=0.0, mirror=True)
    c = k.piece('turretgun')
    c.hull([(x, 9.0, z) for x, z in [(0.0, -7.2), (5.8, -1.0), (0.0, 5.2), (-5.8, -1.0)]] +
           [(x, 23.1, z) for x, z in [(0.0, -4.4), (3.1, -0.9), (0.0, 2.5), (-3.1, -0.9)]], 'dark', bevel=0.16)
    c.cyl((0, 9.2, -1.0), (0, 11.0, -1.0), 6.0, 12, 'paint2', r2=4.8, bevel=0.08)

    # ------------------------------------------------------------------ flak head (turn x + y about its own origin)
    h = k.piece('turret2'); H = h.at
    h.hull([H(x * s, y, z) for s in (-1, 1) for x, y, z in
            [(5.2, -2.6, 3.2), (6.7, -1.8, -3.0), (3.3, 0.0, -10.8), (3.3, 2.6, -10.9), (6.7, 4.9, -5.1), (6.7, 4.9, 3.2),
             (4.7, 7.0, -3.1), (2.4, 7.0, -7.2)]], 'paint', bevel=0.18)
    # gun pods: wide dark blocks (the crossbar that reads from above)
    h.hull([H(x, y, z) for x in (5.0, 10.3) for y, z in [(-1.5, -5.7), (-1.5, 4.4), (0.3, 8.0), (2.9, 8.0), (4.3, 4.4), (4.3, -5.7)]],
           'paint2', bevel=0.16, mirror=True)
    h.hull([H(x, y, z) for y in (4.36, 4.52) for x, z in [(6.0, -5.0), (9.7, -5.0), (9.7, 3.9), (6.0, 3.9)]], 'team', bevel=0.03, mirror=True)
    h.box(H(-3.8, 3.2, -11.0), H(3.8, 4.2, -10.75), 'lightw', bevel=0.0)
    # cap (static child): command dome, team roof
    t1 = k.piece('turret1'); C = t1.at
    t1.hull([C(x * s, y, z) for s in (-1, 1) for x, y, z in
             [(5.1, -2.0, -4.5), (5.1, -1.0, 1.9), (2.5, -1.0, 6.3), (5.1, 2.0, 1.9), (5.1, 2.0, -4.5), (2.5, 2.0, 6.3),
              (3.6, 3.6, -4.5), (3.6, 3.6, 0.4), (1.8, 3.6, 3.5)]], 'paint', bevel=0.16)
    t1.hull([C(x * s, y, z) for s in (-1, 1) for x, y, z in
             [(3.2, 3.66, -4.0), (3.2, 3.66, 0.2), (1.5, 3.66, 3.1), (3.2, 3.82, -4.0), (3.2, 3.82, 0.2), (1.5, 3.82, 3.1)]], 'team', bevel=0.03)
    t1.hull([C(x * s, y, z) for s in (-1, 1) for x, y, z in
             [(2.2, 0.0, 6.36), (4.8, 0.0, 2.0), (2.2, 1.6, 6.36), (4.8, 1.6, 2.0), (2.2, 0.0, 6.5), (2.2, 1.6, 6.5)]], 'black', bevel=0.0)

    # ------------------------------------------------------------------ barrels (recoil 6)
    g = k.piece('guns'); G = g.at
    g.cyl(G(0, -0.1, -6.2), G(0, -0.1, 19.0), 0.95, 10, 'steel')
    for z in (12.0, 16.0):
        g.cyl(G(0, -0.1, z), G(0, -0.1, z + 0.8), 1.2, 10, 'dark', bevel=0.04)
    g.cyl(G(0, -0.1, 18.8), G(0, -0.1, 20.6), 1.35, 8, 'hazard', r2=1.2, bevel=0.04)
    g.cyl(G(0, -0.1, 20.58), G(0, -0.1, 20.66), 0.6, 8, 'black')
    k.clone('guns2', 'guns', mirror_x=True)
