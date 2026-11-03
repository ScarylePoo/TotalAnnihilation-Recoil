"""Executioner (CORE_T2_SEA_Executioner) - Core T2 cruiser. Tall slab-sided hull with a pointed bow; amidships a long dark
deckhouse carrying one very large turret (rear ammunition racks, tall mast) whose twin bright guns reach forward over a
small bridge. The tell from above: double team chevrons on the foredeck pointing at the enemy, one big turret.
Pieces (TA layout): base, turret (turn y), sleeves (static long gun jackets), barrel1/2 (turn x each, recoil 6 along z),
flare1/2 (empty), wake1/2 (empty), box (depth-charge mortar, turn y: its origin is the ship's centre, so it orbits the
deck like the original), chrgflare (empty).
Value groups from above: mid deck + turret (paint), dark deckhouse, side bars and stern block (paint2, dark), bright steel
guns, team on the two chevrons, the waist bands, the turret roof and rear slope, and the stern plates.
Floater, no waterline (water surface at model y = 0). Deck is flat at y 14.7: overlays sit on that real height.
Coordinates are ENGINE/global: X right, Y up, Z forward. mirror=True builds the -X twin sharing UVs."""

UNIT = dict(
    res=2048,
    wreck=dict(seed=43, drop=['barrel2'], pose={'turret': (0, -40, 0), 'barrel1': (10, 0, 0)}),
    preview_pose={'barrel1': (-6, 0, 0), 'barrel2': (-6, 0, 0)},
)

DECK = 14.7
WL = [(0.0, 55.6), (1.6, 55.2), (16.8, 38.9), (20.3, 27.2), (20.3, -2.7), (17.5, -44.7), (10.0, -54.3)]
MID = [(0.0, 53.8), (1.4, 53.4), (15.0, 36.8), (18.2, 24.9), (18.2, -2.8), (15.9, -45.0), (9.1, -53.6)]
TOP = [(0.0, 39.9), (0.5, 39.5), (10.2, 28.3), (12.3, 20.4), (16.0, -3.1), (15.0, -13.7), (14.0, -40.0), (8.0, -47.6)]


def ring(pts, y, sx=1.0, sz=1.0, dz=0.0):
    return [(x * sx * s, y, z * sz + dz) for x, z in pts for s in ((-1, 1) if x > 0 else (1,))]


def build(k):
    b = k.piece('base')
    # ------------------------------------------------------------------ hull: keel, slab sides, deck (crosses x = 0)
    b.hull(ring(WL, -2.4, 0.65, 0.9, -1.0) + ring(WL, 0.0), 'paint2', bevel=0.22)
    b.hull(ring(WL, 0.0) + ring(MID, 5.9), 'paint2', bevel=0.2)
    b.hull(ring(MID, 5.9) + ring(TOP, DECK - 0.6), 'paint2', bevel=0.2)
    b.hull(ring(TOP, DECK - 0.6) + ring(TOP, DECK, 0.985, 0.99), 'paint', bevel=0.14)
    # rub strake and side lights
    b.hull([(x, y, z) for x, z in [(17.8, 24.0), (18.8, 22.0), (18.8, -2.8), (17.0, -30.0)] for y in (5.6, 6.3)], 'dark', bevel=0.05, mirror=True)
    b.box((15.6, 11.0, -30.0), (16.05, 11.7, -14.0), 'lightc', bevel=0.0, mirror=True)
    # ------------------------------------------------------------------ foredeck: two team chevrons (real top = DECK)
    for q in ([(0.25, 34.4), (9.6, 25.0), (10.4, 20.2), (0.25, 28.8)],
              [(0.25, 13.2), (13.4, 3.2), (13.9, -2.0), (0.25, 7.2)]):
        b.hull([(x, y, z) for x, z in q for y in (DECK + 0.06, DECK + 0.22)], 'team', bevel=0.03, mirror=True)
    # paired point-defence domes between the chevrons, bow plate, bow light
    b.cyl((6.2, DECK - 0.1, 19.0), (6.2, DECK + 1.2, 19.0), 2.0, 10, 'dark', r2=1.6, bevel=0.06, mirror=True)
    b.sphere((6.2, DECK + 1.2, 19.0), 1.35, 'steel', segs=10, rings=4, scale=(1, 0.8, 1), mirror=True)
    b.cyl((0, DECK, 36.6), (0, DECK + 0.7, 36.6), 0.42, 6, 'lightr')
    # ------------------------------------------------------------------ deckhouse + bridge
    b.hull([(x * s, y, z) for s in (-1, 1) for x, y, z in
            [(8.6, DECK - 0.2, -34.0), (8.6, DECK - 0.2, -9.0), (7.0, 23.9, -31.7), (7.0, 23.9, -11.1)]], 'paint2', bevel=0.2)
    b.hull([(x * s, y, z) for s in (-1, 1) for x, y, z in
            [(4.8, DECK - 0.2, -9.6), (4.8, DECK - 0.2, -3.4), (4.8, 17.9, -9.6), (4.8, 17.9, -3.4)]], 'paint2', bevel=0.14)
    b.hull([(x * s, y, z) for s in (-1, 1) for x, y, z in
            [(5.9, 17.6, -3.8), (5.9, 17.6, 0.8), (5.9, 19.5, -3.8), (5.9, 19.5, 0.8), (4.4, 22.3, -3.2), (4.4, 22.3, -0.6), (5.9, 17.6, -10.0), (5.9, 19.5, -10.0)]],
           'paint', bevel=0.16)
    b.hull([(x * s, y, z) for s in (-1, 1) for x, y, z in
            [(5.75, 19.0, 0.86), (4.5, 21.6, -0.5), (5.75, 19.0, 1.0), (4.5, 21.6, -0.34)]], 'black', bevel=0.0)
    # side bars (light AA mounts) crossing the deckhouse, dark so the cross shape reads
    b.box((-11.8, 18.6, -27.6), (11.8, 20.0, -21.5), 'dark', bevel=0.1)
    b.cyl((10.4, 20.0, -24.5), (10.4, 20.9, -24.5), 1.3, 8, 'paint', bevel=0.04, mirror=True)
    # ------------------------------------------------------------------ stern block, funnel, team plates
    st = [(14.0, -39.0), (8.0, -47.6), (-8.0, -47.6), (-14.0, -39.0)]
    b.plan(DECK - 0.3, 17.1, st, 'paint2', bevel=0.14)
    b.hull([(x, y, z) for y in (17.16, 17.32) for x, z in [(1.2, -39.5), (13.0, -39.5), (7.6, -46.8), (1.2, -46.8)]], 'team', bevel=0.03)
    b.hull([(-x, y, z) for y in (17.16, 17.32) for x, z in [(7.2, -39.5), (13.0, -39.5), (7.6, -46.8), (7.2, -46.8)]], 'team', bevel=0.03)
    b.box((-6.6, 16.9, -46.8), (0.4, 20.0, -41.3), 'dark', bevel=0.1)
    for x in (-5.6, -3.0):
        b.box((x, 19.9, -46.0), (x + 2.2, 20.15, -42.2), 'black', bevel=0.0)
    b.box((-3.0, 8.6, -48.1), (3.0, 9.5, -47.7), 'lightr', bevel=0.0)
    # team bands along the whole waist, framing the dark deckhouse
    b.hull([(x, y, z) for y in (DECK + 0.06, DECK + 0.22) for x, z in [(9.4, -38.0), (13.4, -38.0), (14.4, -13.7), (14.6, -6.0), (9.4, -6.0)]], 'team', bevel=0.03, mirror=True)

    # ------------------------------------------------------------------ turret (origin 0, 24.1, -18.07)
    t = k.piece('turret'); T = t.at
    t.cyl(T(0, -0.6, -1.4), T(0, 0.6, -1.4), 8.6, 16, 'dark', bevel=0.06)
    t.hull([T(x * s, y, z) for s in (-1, 1) for x, y, z in
            [(9.9, 0.0, -0.4), (7.9, 0.0, 4.2), (6.2, 0.0, 7.0), (3.9, 0.0, 8.4), (6.0, 0.0, -10.8),
             (9.7, 3.9, -1.5), (6.0, 3.9, -11.1), (9.7, 8.1, -1.5), (6.0, 8.1, -11.1),
             (6.2, 6.5, 5.0), (3.9, 7.6, 6.4), (6.0, 11.1, -0.4), (3.9, 11.1, -6.2)]], 'paint', bevel=0.2)
    # team: roof, rear slope (trapezoid (6.0,-11.1,8.1)-(3.9,-6.2,11.1), offset along its normal)
    t.hull([T(x * s, y, z) for s in (-1, 1) for x, z in [(5.2, -1.1), (3.5, -5.7)] for y in (11.16, 11.32)], 'team', bevel=0.03)
    t.hull([T(x * s, y + 0.86 * d, z - 0.51 * d) for s in (-1, 1) for x, y, z in [(5.1, 8.42, -10.55), (3.75, 10.82, -6.65)] for d in (0.08, 0.22)],
           'team', bevel=0.03)
    # rear racks: three ammunition blocks with black mouths
    for x0, x1 in ((-5.3, -2.8), (-1.3, 1.1), (2.8, 5.2)):
        t.box(T(x0, 0.8, -14.9), T(x1, 6.9, -10.4), 'dark', bevel=0.1)
        t.box(T(x0 + 0.5, 1.6, -14.98), T(x1 - 0.5, 6.1, -14.86), 'black', bevel=0.0)
    # mast
    t.cyl(T(-4.5, 8.0, -8.3), T(-4.5, 24.2, -8.3), 0.8, 8, 'dark', r2=0.45)
    t.box(T(-7.0, 18.0, -8.7), T(-2.0, 18.6, -7.9), 'dark', bevel=0.05)
    t.cyl(T(-4.5, 24.2, -8.3), T(-4.5, 24.6, -8.3), 0.36, 6, 'lightr')
    t.box(T(-5.0, 9.4, 3.1), T(5.0, 10.0, 3.4), 'lightc', bevel=0.0)

    # ------------------------------------------------------------------ static gun jackets (origin 0, 27.97, -18.47)
    sv = k.piece('sleeves'); S = sv.at
    sv.box(S(-3.9, -2.1, 0.0), S(3.9, 2.2, 7.6), 'dark', bevel=0.1)
    for x in (-2.01, 2.01):
        sv.cyl(S(x, -0.9, 3.0), S(x, -0.9, 14.2), 2.0, 10, 'steel')
        sv.cyl(S(x, -0.9, 13.0), S(x, -0.9, 14.3), 2.2, 10, 'dark', bevel=0.05)

    # ------------------------------------------------------------------ barrels (turn x, recoil 6 into the jackets)
    br = k.piece('barrel1'); B = br.at
    br.cyl(B(0, 0, -6.2), B(0, 0, 8.2), 1.45, 10, 'steel')
    br.cyl(B(0, 0, 8.0), B(0, 0, 9.9), 1.8, 8, 'hazard', r2=1.65, bevel=0.05)
    br.cyl(B(0, 0, 9.88), B(0, 0, 9.96), 0.85, 8, 'black')
    k.clone('barrel2', 'barrel1')

    # ------------------------------------------------------------------ mortar box (turn y about the ship's centre)
    x = k.piece('box'); X = x.at
    x.hull([X(u * s, y, z) for s in (-1, 1) for u, y, z in
            [(2.8, 5.8, 11.4), (2.8, 5.8, 17.0), (1.8, 5.8, 19.3), (2.8, 7.7, 11.4), (2.8, 7.7, 17.0), (1.8, 7.7, 19.3),
             (1.9, 8.9, 12.9), (1.9, 8.9, 17.0), (1.2, 8.9, 18.6)]], 'paint2', bevel=0.12)
    x.cyl(X(0, 8.8, 14.9), X(0, 9.1, 14.9), 1.25, 10, 'steel')
    x.cyl(X(0, 9.08, 14.9), X(0, 9.16, 14.9), 0.75, 8, 'black')
