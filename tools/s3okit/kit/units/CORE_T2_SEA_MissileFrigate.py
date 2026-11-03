"""Missile Frigate (CORE_T2_SEA_MissileFrigate) - Core T2 missile ship. A broad hull whose whole middle is a long launch
bay between wide raised rails: when activated (always, activatewhenbuilt) four doors slide away fore and aft, a platform
rises out of the bay and a rack stands two huge bright cruise missiles upright. Aft a winged bridge tower with a
big radar dish, forward a small box launcher turret. The tell from above: wide team rails framing the dark raised bay
with two bright missiles standing in it.
Pieces (TA layout): base, dish (spin y), platform (move y 11.625), stand (move y 11), hamper (turn x -90), rocket1/2
(hidden after firing, query points), turret (turn y), gun (turn x), missile1-3 (empty), wake1/2 (empty), door1a/1b/2a/2b
(slide: y -0.5 each, and b is a child of a, so an open b door sits at y 8.67 under a at y 9.17).
The main hull is cut down to y 8.4 between the rails (DECK 9.7) because the open doors sink below deck level and would
vanish inside a solid hull. The aft doors slide under the tower, the forward ones stop in front of the raised foredeck.
Closed, platform, rack and rockets are all inside the hull below the doors (their faces are never seen there).
Value groups from above: dark bay/platform (paint2, dark), mid deck + bridge (paint), bright steel missiles and dish,
team on the rails, platform plates, forward door, tower wing tips, gun roof.
Floater, no waterline (water surface at model y = 0).
Coordinates are ENGINE/global: X right, Y up, Z forward. mirror=True builds the -X twin sharing UVs."""
import math

OPEN = {
    'door1a': {'move': (0, -0.5, -10.75)}, 'door1b': {'move': (0, -0.5, -9.25)},
    'door2a': {'move': (0, -0.5, 9.875)}, 'door2b': {'move': (0, -0.5, 9.0)},
    'platform': {'move': (0, 11.625, 0)}, 'stand': {'move': (0, 11.0, 0)}, 'hamper': (-90, 0, 0),
}

UNIT = dict(
    res=2048,
    wreck=dict(seed=37, remove=['rocket2'], drop=['dish'], pose={'turret': (0, 40, 0)}),
    preview_pose=dict(OPEN, gun=(-8, 0, 0)),
)

DECK = 9.7
FLOOR = 8.4
WL = [(0.0, 56.3), (5.0, 55.8), (17.5, 32.8), (21.2, 13.0), (21.2, -28.0), (17.5, -47.8), (8.8, -55.0)]
TOP = [(0.0, 47.8), (3.7, 47.1), (13.6, 28.8), (16.5, 10.5), (16.5, -26.4), (13.6, -42.7), (6.6, -49.0)]


def ring(pts, y, sx=1.0, sz=1.0, dz=0.0):
    return [(x * sx * s, y, z * sz + dz) for x, z in pts for s in ((-1, 1) if x > 0 else (1,))]


def build(k):
    b = k.piece('base')
    # ------------------------------------------------------------------ hull: keel, sides up to the bay floor
    b.hull(ring(WL, -2.2, 0.65, 0.9, -1.0) + ring(WL, 0.0), 'paint2', bevel=0.22)
    b.hull(ring(WL, 0.0) + ring(TOP, FLOOR, 1.03, 1.02), 'paint2', bevel=0.22)
    # rails either side of the bay, foredeck and afterdeck: all with their real top at DECK
    # (they only touch end to end: overlapping hulls with coplanar tops get both tops culled)
    rail = [(12.9, -31.0), (15.68, -31.0), (16.5, -26.4), (16.5, 10.5), (14.8, 21.2), (12.9, 21.2)]
    b.plan(FLOOR - 0.3, DECK, rail, 'paint', bevel=0.12, mirror=True)
    fore = [(0.0, 47.8), (3.7, 47.1), (13.6, 28.8), (14.8, 21.2), (-14.8, 21.2), (-13.6, 28.8), (-3.7, 47.1)]
    b.plan(FLOOR - 0.3, DECK, fore, 'paint', bevel=0.14)
    aft = [(15.68, -31.0), (13.6, -42.7), (6.6, -49.0), (-6.6, -49.0), (-13.6, -42.7), (-15.68, -31.0)]
    b.plan(FLOOR - 0.3, DECK, aft, 'paint', bevel=0.14)
    # wide team bands on the rails (plan sides are vertical here: the real top is DECK)
    b.hull([(x, y, z) for y in (DECK + 0.06, DECK + 0.22) for x, z in [(13.2, -29.0), (15.6, -27.0), (15.6, 8.0), (13.2, 10.0)]],
           'team', bevel=0.03, mirror=True)
    b.box((16.6, 6.4, -14.0), (17.05, 7.2, -2.0), 'lightc', bevel=0.0, mirror=True)
    # point-defence domes on the rail forward of the band
    b.cyl((14.3, DECK - 0.1, 16.2), (14.3, DECK + 1.4, 16.2), 1.5, 10, 'dark', r2=1.2, bevel=0.05, mirror=True)
    b.sphere((14.3, DECK + 1.4, 16.2), 1.05, 'steel', segs=10, rings=4, scale=(1, 0.75, 1), mirror=True)
    # bow: anchor deck, chain cable, bow light
    b.hull([(x * s, y, z) for s in (-1, 1) for x, z in [(1.2, 45.6), (3.4, 44.8), (5.8, 38.8), (1.2, 38.8)] for y in (DECK + 0.06, DECK + 0.2)],
           'dark', bevel=0.03)
    b.cyl((0, DECK + 0.1, 44.6), (0, DECK + 0.8, 44.6), 0.36, 6, 'lightr')
    # afterdeck vents, stern light
    for x in (-4.6, -1.5, 1.6):
        b.box((x, DECK - 0.1, -47.4), (x + 2.6, DECK + 0.2, -44.0), 'black', bevel=0.0)
    b.box((-3.0, 5.6, -50.0), (3.0, 6.5, -49.6), 'lightr', bevel=0.0)

    # ------------------------------------------------------------------ bridge tower + wings
    b.hull([(x * s, y, z) for s in (-1, 1) for x, y, z in
            [(8.5, FLOOR, -29.8), (5.6, FLOOR, -44.0), (8.5, 25.0, -30.2), (4.8, 25.0, -43.0)]], 'paint2', bevel=0.2)
    b.hull([(x * s, y, z) for s in (-1, 1) for x, y, z in
            [(10.9, 13.8, -33.4), (13.3, 13.8, -38.2), (3.6, 13.8, -47.8), (10.9, 18.8, -33.4), (13.3, 18.8, -38.2), (3.6, 18.8, -47.8)]],
           'paint', bevel=0.18)
    b.hull([(x, y, z) for y in (18.86, 19.02) for x, z in [(9.3, -34.0), (10.9, -34.0), (13.0, -38.2), (9.3, -43.2)]], 'team', bevel=0.03, mirror=True)
    # tower top: team roof, twin aerial pods flanking it
    b.hull([(x * s, y, z) for s in (-1, 1) for x, y, z in [(7.8, 25.06, -30.8), (4.5, 25.06, -42.2), (7.8, 25.22, -30.8), (4.5, 25.22, -42.2)]], 'team', bevel=0.03)
    b.hull([(x, y, z) for y in (24.8, 28.5) for x, z in [(5.5, -40.7), (7.3, -34.7), (9.1, -37.3), (8.2, -40.3)]], 'paint', bevel=0.1, mirror=True)
    b.hull([(x * s, y, z) for s in (-1, 1) for x, y, z in
            [(8.3, 21.0, -29.82), (8.3, 23.4, -29.9), (8.3, 21.0, -30.1), (8.3, 23.4, -30.1), (0.0, 21.0, -29.82), (0.0, 23.4, -29.9)]], 'lightc', bevel=0.0)
    b.cyl((-1.5, 25.0, -32.0), (-1.5, 25.8, -32.0), 1.7, 8, 'dark', bevel=0.04)

    # ------------------------------------------------------------------ big radar dish (spin y; origin x = -1.5, whole)
    d = k.piece('dish'); D = d.at
    d.cyl(D(0, 0, 0), D(0, 9.5, 0), 0.65, 8, 'dark')
    d.hull([D(x, y, z) for x, y, z in
            [(-6.6, 4.2, 2.5), (6.6, 4.2, 2.5), (-6.6, 8.2, 2.5), (6.6, 8.2, 2.5), (-3.0, 2.8, 0.6), (3.0, 2.8, 0.6), (-3.0, 9.6, 0.6), (3.0, 9.6, 0.6),
             (-1.0, 5.2, -0.5), (1.0, 5.2, -0.5), (-1.0, 7.2, -0.5), (1.0, 7.2, -0.5)]], 'steel', bevel=0.08)
    d.cyl(D(0, 9.5, 0), D(0, 9.8, 0), 0.4, 6, 'lightr')

    # ------------------------------------------------------------------ platform (rises out of the bay)
    p = k.piece('platform'); P = p.at
    p.hull([P(x, y, z) for x, y, z in
            [(s * 12.5, -0.9, zz) for s in (-1, 1) for zz in (-20.2, 16.8)] + [(s * 10.0, 3.4, zz) for s in (-1, 1) for zz in (-19.7, 13.0)]],
           'dark', bevel=0.16)
    p.hull([P(x * s, y, z) for s in (-1, 1) for x, y, z in
            [(9.0, 3.2, 2.2), (9.0, 3.2, 7.2), (9.0, 5.7, 2.2), (9.0, 5.7, 7.2), (6.5, 9.2, 1.2), (6.5, 9.2, 8.2), (6.5, 3.2, 1.2), (6.5, 3.2, 8.2)]],
           'paint', bevel=0.16)
    p.hull([P(x * s, y, z) for s in (-1, 1) for x, y, z in [(5.9, 9.26, 1.7), (5.9, 9.26, 7.7), (5.9, 9.42, 1.7), (5.9, 9.42, 7.7)]], 'team', bevel=0.03)
    # team plates aft and fore of the launcher
    p.hull([P(x * s, y, z) for s in (-1, 1) for y in (3.46, 3.62) for x, z in [(9.2, -18.9), (9.2, -11.0)]], 'team', bevel=0.03)
    p.hull([P(x * s, y, z) for s in (-1, 1) for y in (3.46, 3.62) for x, z in [(9.2, 8.9), (9.2, 12.4)]], 'team', bevel=0.03)
    # hazard edge either side of the launcher well (missile blast: means keep clear)
    p.hull([P(x, y, z) for y in (3.46, 3.62) for x, z in [(4.4, -10.2), (9.2, -10.2), (9.2, 0.8), (4.4, 0.8)]], 'hazard', bevel=0.03, mirror=True)
    p.box(P(-3.6, 3.4, -10.2), P(3.6, 3.56, 0.8), 'black', bevel=0.0)
    st = k.piece('stand'); S = st.at
    st.box(S(-1.5, 0.0, -1.8), S(1.5, 11.7, 1.8), 'steel', bevel=0.08)

    # ------------------------------------------------------------------ rack (turns -90: +z goes up, +y goes aft)
    h = k.piece('hamper'); H = h.at
    h.box(H(-7.7, -0.6, -1.5), H(7.7, 0.4, 1.5), 'dark', bevel=0.06)
    h.hull([H(x, y, z) for x in (-1.2, 1.2) for y, z in [(0.4, -13.0), (0.4, 14.0), (2.9, 11.5), (5.6, 9.5), (5.6, -13.0)]], 'dark', bevel=0.08)
    h.hull([H(x, y, z) for x in (-9.5, 9.5) for y, z in [(0.4, -14.0), (0.4, -13.0), (6.1, -14.0), (6.1, -13.0)]], 'paint2', bevel=0.08)
    h.hull([H(x, y, z) for x in (-3.8, 3.8) for y, z in [(0.4, 9.0), (0.4, 11.5), (2.9, 9.0), (2.9, 11.5)]], 'paint2', bevel=0.06)
    # rockets: thick bright bodies, hazard noses, cross fins
    r = k.piece('rocket1'); R = r.at
    r.cyl(R(0, 0, -17.2), R(0, 0, 6.0), 1.75, 10, 'steel')
    r.cyl(R(0, 0, 6.0), R(0, 0, 10.0), 1.75, 10, 'hazard', r2=1.2)
    r.cyl(R(0, 0, 10.0), R(0, 0, 14.1), 1.2, 10, 'hazard', r2=0.2)
    r.cyl(R(0, 0, -17.6), R(0, 0, -17.1), 1.4, 10, 'black')
    for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
        a = (3.8 * dx, 3.8 * dy); n = (0.22 * dy, 0.22 * dx)
        r.hull([R(u + m * n[0], v + m * n[1], z) for m in (-1, 1) for u, v, z in
                [(1.4 * dx, 1.4 * dy, -17.1), (1.4 * dx, 1.4 * dy, -8.0), (a[0], a[1], -17.1), (a[0], a[1], -13.0)]], 'dark', bevel=0.0)
    k.clone('rocket2', 'rocket1')

    # ------------------------------------------------------------------ box launcher turret (forward)
    t = k.piece('turret'); T = t.at
    t.hull([T(x * s, y, z) for s in (-1, 1) for x, y, z in
            [(8.8, -0.2, -7.5), (8.8, -0.2, 6.2), (6.2, 6.2, -5.5), (6.2, 6.2, 2.8)]], 'paint', bevel=0.16)
    t.cyl(T(0, -0.2, -0.6), T(0, 0.0, -0.6), 9.4, 14, 'dark', bevel=0.03)
    g = k.piece('gun'); G = g.at
    g.hull([G(x * s, y, z) for s in (-1, 1) for x, y, z in
            [(2.5, -1.7, -2.5), (2.5, 1.7, -2.5), (4.5, -2.7, 0.0), (4.5, 2.7, 0.0), (4.5, -2.7, 11.5), (4.5, 2.7, 8.0)]], 'paint2', bevel=0.14)
    # slanted launcher face (nose runs from y 2.7 at z 8 to y -2.7 at z 11.5), three tube mouths at the missile points
    nz, ny = 3.5 / math.hypot(3.5, 5.4), 5.4 / math.hypot(3.5, 5.4)
    g.hull([G(x, y + d * nz, z + d * ny) for x in (-4.0, 4.0) for y, z in [(2.2, 8.32), (-2.2, 11.18)] for d in (0.02, 0.08)], 'black', bevel=0.0)
    for x in (-2.5, 0.0, 2.5):
        g.cyl(G(x, 0.25, 9.5), G(x + 0.0, 0.25 + 0.09, 9.5 + 0.16), 1.0, 8, 'steel')
    g.hull([G(x * s, y, z) for s in (-1, 1) for x, y, z in [(3.9, 2.76, 0.4), (3.9, 2.76, 7.5), (3.9, 2.92, 0.4), (3.9, 2.92, 7.5)]], 'team', bevel=0.03)

    # ------------------------------------------------------------------ doors: thin plates; a doors carry team, b dark
    h = 0.15
    d1a = k.piece('door1a'); A = d1a.at
    d1a.box(A(-12.0, 0, 0), A(13.0, h, 10.15), 'paint', bevel=0.03)
    d1a.box(A(-9.0, h - 0.03, 1.4), A(10.0, h + 0.09, 8.8), 'team', bevel=0.0)
    d1b = k.piece('door1b'); B = d1b.at
    d1b.box(B(-12.5, 0, 0), B(12.5, h, 8.8), 'paint2', bevel=0.03)
    d2a = k.piece('door2a'); C = d2a.at
    d2a.box(C(-12.0, 0, -9.5), C(13.0, h, 0), 'paint', bevel=0.03)
    d2a.box(C(-9.0, h - 0.03, -8.2), C(10.0, h + 0.09, -1.3), 'team', bevel=0.0)
    d2b = k.piece('door2b'); E = d2b.at
    d2b.box(E(-12.4, 0, -8.5), E(12.6, h, 0), 'paint2', bevel=0.03)
