"""Enforcer (CORE_T1_SEA_Enforcer) - Core destroyer. Broad tumblehome hull (much wider at the waterline than at the
deck: from above a wide dark skirt ring around a narrower deck), long raised aft deckhouse, and at the stern a
heavy turret flanked by two huge armoured gun housings whose very long light cannons run forward over half the
ship. Four missile-cell domes amidships, a small forward bridge with a team roof, twin aerial posts on the turret.
Pieces (TA layout): base, turret (turn y), sleeves (turn x: both gun housings), barrel1/2 (recoil 6 along z),
flarea1/2 (empty muzzles), flareb (empty, secondary weapon point), wake1/2 (empty).
Value groups from above: dark Core deck (paint), darker paint2 skirt ring and deckhouse sides, light steel cannons
(the tell: two long bright bars), team on the gun-housing tops, turret roof and bridge roof, ochre hazard bands on
the cannon muzzles. Floater, waterline 1 (water surface at model y = 1).
Coordinates are ENGINE/global: X right, Y up, Z forward. mirror=True builds the -X twin sharing UVs."""
import math

UNIT = dict(
    res=1024,
    wreck=dict(seed=11, drop=['barrel2'], pose={'turret': (0, -35, 0)}),
    preview_pose={'turret': (0, 15, 0), 'sleeves': (-5, 0, 0)},
)

WL = 1.0
DECK = 7.0
WATER = [(0.0, 41.0), (1.4, 40.4), (14.2, 24.6), (17.3, 6.7), (17.3, -14.2), (14.7, -33.4), (8.6, -40.4)]
DECKO = [(0.0, 31.8), (0.3, 31.2), (9.5, 19.4), (11.6, 5.0), (11.6, -14.2), (9.3, -31.5), (5.1, -36.1)]


def ring(pts, y, sx=1.0, sz=1.0, dz=0.0):
    return [(x * sx * s, y, z * sz + dz) for x, z in pts for s in ((-1, 1) if x > 0 else (1,))]


def build(k):
    b = k.piece('base')
    # ------------------------------------------------------------------ hull: below-water keel, flared skirt, deck
    b.hull(ring(WATER, -2.4, 0.6, 0.85, -1.0) + ring(WATER, WL, 1.0, 1.0), 'paint2', bevel=0.2)
    b.hull(ring(WATER, WL, 1.0, 1.0) + ring(WATER, WL + 1.0, 0.985, 0.985) + ring(DECKO, DECK), 'paint2', bevel=0.22)
    b.hull(ring(DECKO, DECK - 0.4, 1.0, 1.0) + ring(DECKO, DECK + 0.3, 0.97, 0.97), 'paint', bevel=0.14)
    # rub strake: a lighter band at the skirt's mid-height reads as the hull outline
    b.hull([(x, y, z) for x, z in [(15.4, 19.0), (17.0, 6.0), (17.0, -14.0), (14.6, -30.0)] for y in (3.0, 3.6)] +
           [(x - 0.6, y, z) for x, z in [(15.4, 19.0), (17.0, 6.0), (17.0, -14.0), (14.6, -30.0)] for y in (3.0, 3.6)],
           'dark', bevel=0.04, mirror=True)
    # ------------------------------------------------------------------ forward bridge (small, team roof)
    b.hull([(x * s, y, z) for s in (-1, 1) for x, y, z in
            [(4.0, 7.2, 10.2), (4.0, 7.2, 18.0), (2.4, 7.2, 21.4),
             (3.0, 11.2, 11.4), (3.0, 11.2, 17.4), (1.6, 11.2, 19.8)]], 'paint', bevel=0.16)
    b.hull([(x * s, y, z) for s in (-1, 1) for x, y, z in
            [(3.15, 9.6, 17.6), (1.75, 9.6, 20.4), (2.95, 10.7, 17.2), (1.6, 10.7, 19.6),
             (3.4, 9.6, 16.4), (3.15, 10.7, 16.2)]], 'black', bevel=0.0)
    b.hull([(x * s, y, z) for s in (-1, 1) for x, y, z in
            [(2.5, 11.15, 12.0), (2.5, 11.15, 16.9), (1.2, 11.15, 18.9),
             (2.45, 11.32, 12.05), (2.45, 11.32, 16.85), (1.15, 11.32, 18.8)]], 'team', bevel=0.03)
    b.cyl((0, 11.2, 13.0), (0, 16.0, 13.0), 0.35, 8, 'dark', r2=0.22)
    b.cyl((0, 16.0, 13.0), (0, 16.3, 13.0), 0.26, 6, 'lightr')
    # bow: dark anchor deck plate with a hazard chevron pointing forward
    for s in (-1, 1):
        q = [(0.0, 28.6), (1.4, 28.6), (6.6, 22.0), (4.6, 22.0)]
        b.hull([(x * s, DECK + h, z) for x, z in q for h in (0.28, 0.42)], 'hazard', bevel=0.03)
    # ------------------------------------------------------------------ four missile-cell domes amidships
    for x0, z0 in ((7.5, 4.6), (7.5, -3.8)):
        b.cyl((x0, DECK + 0.2, z0), (x0, DECK + 1.1, z0), 2.6, 12, 'paint2', r2=2.2, bevel=0.06, mirror=True)
        b.sphere((x0, DECK + 1.1, z0), 1.7, 'steel', segs=12, rings=5, scale=(1, 0.45, 1), mirror=True)
    # flareb launcher deck between the domes: dark grille
    b.box((-4.6, DECK + 0.2, -6.4), (4.6, DECK + 0.6, 7.6), 'dark', bevel=0.08)
    for z in (-5.0, -3.0, -1.0, 1.0, 3.0, 5.0):
        b.box((-4.0, DECK + 0.58, z), (4.0, DECK + 0.72, z + 0.7), 'black', bevel=0.0)
    # ------------------------------------------------------------------ long aft deckhouse + turret pylon
    b.hull([(x * s, y, z) for s in (-1, 1) for x, y, z in
            [(8.4, 7.0, -7.4), (8.4, 7.0, -32.2), (6.6, 7.0, -34.0),
             (7.6, 9.8, -11.4), (7.6, 9.8, -30.0), (5.8, 9.8, -31.4)]], 'paint2', bevel=0.18)
    b.hull([(x * s, y, z) for s in (-1, 1) for x, y, z in
            [(7.1, 9.75, -12.0), (7.1, 9.75, -29.6), (7.0, 9.95, -12.1), (7.0, 9.95, -29.5)]], 'paint', bevel=0.06)
    b.hull([(x * s, y, z) for s in (-1, 1) for x, y, z in
            [(5.6, 9.8, -13.0), (5.6, 9.8, -28.8), (3.0, 12.8, -17.0), (3.0, 12.8, -25.6)]], 'paint', bevel=0.16)
    b.box((8.3, 8.0, -28.0), (8.55, 8.6, -14.0), 'lightc', bevel=0.0, mirror=True)
    # stern: depth-charge rails and a red stern light
    for x in (3.4,):
        b.box((x - 0.7, DECK + 0.2, -35.0), (x + 0.7, DECK + 1.0, -31.4), 'dark', bevel=0.06, mirror=True)
    b.box((-1.4, 5.6, -36.3), (1.4, 6.4, -36.0), 'lightr', bevel=0.0)

    # ------------------------------------------------------------------ turret (origin 0, 15.3, -22.43)
    t = k.piece('turret'); A = t.at
    t.cyl(A(0, -2.6, -0.6), A(0, 0.0, -0.6), 4.2, 16, 'dark', bevel=0.06)
    t.hull([A(x * s, y, z) for s in (-1, 1) for x, y, z in
            [(4.7, -0.3, 6.8), (4.7, -0.3, -5.2), (4.7, 1.6, 6.8), (4.7, 3.0, 4.8), (4.7, 3.0, -5.2)]], 'paint', bevel=0.16)
    # raised command block on top, team roof
    t.hull([A(x * s, y, z) for s in (-1, 1) for x, y, z in
            [(3.5, 2.9, 3.4), (3.5, 2.9, -4.2), (1.6, 7.4, 3.0), (3.4, 9.2, -4.2), (1.6, 2.9, 3.4)]], 'paint', bevel=0.16)
    t.hull([A(x * s, y, z) for s in (-1, 1) for x, y, z in
            [(1.4, 7.42, 2.6), (2.95, 9.05, -3.8), (1.35, 7.6, 2.5), (2.9, 9.22, -3.7)]], 'team', bevel=0.03)
    t.hull([A(x * s, y, z) for s in (-1, 1) for x, y, z in
            [(1.5, 3.3, 3.45), (1.5, 6.6, 3.2), (1.42, 3.3, 3.6), (1.42, 6.6, 3.35)]], 'lightc', bevel=0.0)
    # twin aerial posts (TA's two masts), dark with red tips
    for x in (-3.4, 3.4):
        t.cyl(A(x, 3.0, -2.2), A(x, 12.4, -2.4), 0.55, 8, 'dark', r2=0.35)
        t.cyl(A(x, 12.4, -2.4), A(x, 12.7, -2.4), 0.3, 6, 'lightr')

    # ------------------------------------------------------------------ sleeves: two armoured gun housings (origin 0, 16.03, -19.88)
    sv = k.piece('sleeves'); S = sv.at
    sv.hull([S(x, y, z) for x, y, z in
             [(4.7, -3.3, 9.8), (11.4, -3.3, 6.9), (4.7, -3.3, -8.4), (11.4, -3.3, -8.4),
              (4.7, 2.2, 7.0), (11.4, 2.2, 4.2), (4.7, 3.5, 2.4), (8.6, 3.5, 1.0),
              (4.7, 3.5, -8.4), (8.6, 3.5, -8.4), (11.4, 2.2, -8.4)]], 'paint2', bevel=0.18, mirror=True)
    sv.hull([S(x, y, z) for x, y, z in
             [(5.2, 3.48, 1.8), (8.2, 3.48, 0.6), (5.2, 3.48, -7.6), (8.2, 3.48, -7.6),
              (5.2, 3.66, 1.8), (8.2, 3.66, 0.6), (5.2, 3.66, -7.6), (8.2, 3.66, -7.6)]], 'team', bevel=0.03, mirror=True)
    sv.cyl(S(-4.8, 0, 0), S(4.8, 0, 0), 1.6, 12, 'dark')
    sv.box(S(11.3, -1.6, -6.0), S(11.55, -0.8, 2.0), 'lightw', bevel=0.0, mirror=True)

    # ------------------------------------------------------------------ barrels: very long light cannons (barrel1 origin -8.2, 15.66, -24.35)
    br = k.piece('barrel1'); B = br.at
    br.cyl(B(0, 0.1, -5.0), B(0, 0.1, 33.6), 1.15, 10, 'steel', rot=math.pi / 10)
    for z in (16.0, 24.0):
        br.cyl(B(0, 0.1, z), B(0, 0.1, z + 1.0), 1.4, 10, 'dark', rot=math.pi / 10, bevel=0.04)
    br.cyl(B(0, 0.1, 30.6), B(0, 0.1, 32.0), 1.42, 10, 'hazard', rot=math.pi / 10)
    br.cyl(B(0, 0.1, 32.0), B(0, 0.1, 35.2), 1.75, 8, 'steel', r2=1.55, rot=math.pi / 8, bevel=0.06)
    br.cyl(B(0, 0.1, 35.18), B(0, 0.1, 35.26), 0.8, 8, 'black')
    k.clone('barrel2', 'barrel1', mirror_x=True)
