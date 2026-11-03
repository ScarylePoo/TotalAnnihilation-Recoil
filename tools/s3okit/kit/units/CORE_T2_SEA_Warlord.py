"""Warlord (CORE_T2_SEA_Warlord) - Core battleship. A long narrow dagger of a hull with towering stepped armour: a fore
barbette carrying a rotary three-barrel cannon, and aft a stepped citadel topped by the enormous main turret (the whole
upper superstructure, with ear mounts and a tall mast), whose three bright barrels run forward over the fore turret.
The tell from above: three long bright bars and a bright rotary, stacked down the spine of a pointed hull, the
main turret as wide as the ship. The opposite read of the flat, wide Hive.
Pieces (TA layout): base, turreta (turn y), guna (rotary, turn z in 120 deg steps: built with 3-fold symmetry around z),
flarea (empty, top barrel's muzzle), turretb (turn y and x: the entire superstructure), sleeveb (static), barrelb1/2/3
(recoil 6 along z), flareb1/2/3 (empty), wake1/2 (empty).
Value groups from above: mid deck and main turret (paint), darker hull/barbette/citadel (paint2), near-black mounts and
jackets (dark), bright steel barrels, team on the main turret's wings, front wedge and tower roof, the spear tip ahead
of the fore turret, the waist strips, hull flare bands, citadel front, bow and stern plates.
Floater, no waterline (water surface at model y = 0). Deck is flat at y 21.2: overlays sit on that real height.
Coordinates are ENGINE/global: X right, Y up, Z forward. mirror=True builds the -X twin sharing UVs."""
import math

UNIT = dict(
    res=2048,
    wreck=dict(seed=53, drop=['barrelb3'], pose={'turreta': (0, 50, 0), 'turretb': (10, -25, 5), 'barrelb1': (12, 0, 0)}),
    preview_pose={'turretb': (-3, 0, 0)},
)

DECK = 21.2
WL = [(0.0, 69.2), (2.1, 68.8), (21.5, 42.0), (26.1, 11.6), (26.1, -23.6), (22.2, -56.1), (12.9, -68.1)]
TOP = [(0.0, 56.5), (0.5, 56.2), (15.2, 35.3), (18.5, 9.3), (18.5, -25.1), (14.8, -56.2), (8.2, -64.5)]


def half(pts, y, z0, z1, sx=1.0):
    """+x half of an outline clipped to z0 .. z1, with centre-line points: one hull section."""
    pts = sorted(pts, key=lambda p: p[1])
    def x_at(z):
        z = max(pts[0][1], min(pts[-1][1], z))
        for (xa, za), (xb, zb) in zip(pts, pts[1:]):
            if za <= z <= zb:
                return xa + (xb - xa) * (z - za) / ((zb - za) or 1.0)
    z0, z1 = max(z0, pts[0][1]), min(z1, pts[-1][1])
    q = [(x_at(z0), z0)] + [p for p in pts if z0 < p[1] < z1] + [(x_at(z1), z1)]
    return [(x * sx, y, z) for x, z in q] + [(0.0, y, z0), (0.0, y, z1)]


def build(k):
    b = k.piece('base')
    # ------------------------------------------------------------------ hull (crosses x = 0): flare, then a vertical wall
    # Mirrored halves in three z sections that only touch: long hull sides pack badly (see the Hive) and share UVs this way.
    for z0, z1 in ((-80.0, -23.6), (-23.6, 11.6), (11.6, 80.0)):
        b.hull(half(WL, -2.6, z0, z1, 0.65) + half(WL, -0.2, z0, z1), 'paint2', bevel=0.0, mirror=True)
        b.hull(half(WL, -0.2, z0, z1) + half(TOP, 11.4, z0, z1), 'paint2', bevel=0.0, mirror=True)
        b.hull(half(TOP, 11.4, z0, z1) + half(TOP, DECK - 0.5, z0, z1, 0.99), 'paint2', bevel=0.0, mirror=True)
        b.hull(half(TOP, DECK - 0.5, z0, z1, 0.99) + half(TOP, DECK, z0, z1, 0.975), 'paint', bevel=0.0, mirror=True)
    # armour belt: dark strake at the knuckle, cyan lights above
    b.hull([(x, y, z) for x, z in [(15.9, 33.0), (19.2, 9.3), (19.2, -25.1), (16.5, -48.0)] for y in (10.9, 12.0)] +
           [(x - 1.0, y, z) for x, z in [(15.9, 33.0), (19.2, 9.3), (19.2, -25.1), (16.5, -48.0)] for y in (10.9, 12.0)], 'dark', bevel=0.05, mirror=True)
    b.box((18.42, 16.0, -18.0), (18.85, 17.0, 4.0), 'lightc', bevel=0.0, mirror=True)
    # waist strips outboard of the citadel (real top = DECK)
    b.hull([(x, y, z) for y in (DECK + 0.06, DECK + 0.22) for x, z in [(14.9, -50.0), (15.9, -50.0), (17.8, -25.0), (17.8, -12.0), (14.9, -12.0)]],
           'team', bevel=0.03, mirror=True)
    # team band on the wide hull flare amidships (flare plane (26.1, -0.2) -> (18.5, 11.4), offset along its normal)
    nx, ny = 0.836, 0.548
    b.hull([(26.1 - 7.6 * f + nx * d, -0.2 + 11.6 * f + ny * d, z) for f in (0.2, 0.75) for z in (-21.0, 8.0) for d in (0.08, 0.24)],
           'team', bevel=0.03, mirror=True)
    # bow: team deck plate, bow light
    b.hull([(x * s, y, z) for s in (-1, 1) for x, z in [(0.8, 53.0), (3.4, 49.0), (6.8, 44.2), (0.8, 44.2)] for y in (DECK + 0.06, DECK + 0.2)], 'team', bevel=0.03)
    b.cyl((0, DECK, 51.8), (0, DECK + 0.9, 51.8), 0.42, 6, 'lightr')

    # ------------------------------------------------------------------ fore barbette: long tapered pyramid under turreta
    b.hull([(x * s, y, z) for s in (-1, 1) for x, y, z in
            [(3.9, DECK - 0.2, 46.0), (8.0, DECK - 0.2, 31.9), (12.7, DECK - 0.2, 26.8), (14.8, DECK - 0.2, 8.9), (6.5, DECK - 0.2, 0.9),
             (3.0, 26.4, 40.6), (6.2, 26.4, 29.6), (9.9, 26.4, 25.7), (11.5, 26.4, 11.7)]], 'paint2', bevel=0.2)
    # team spear tip ahead of the fore turret (top of the barbette: real height 26.4)
    b.hull([(x * s, y, z) for s in (-1, 1) for x, z in [(2.5, 39.6), (5.6, 29.8), (5.6, 28.2), (2.5, 28.2)] for y in (26.46, 26.62)], 'team', bevel=0.03)
    # side mounts: hexagonal pedestals with steel domes
    for pts in ([(16.1, 0.9), (14.8, 8.9), (11.3, 4.9), (6.5, 0.9), (8.4, -5.5), (14.3, -5.5)],):
        b.hull([(x, DECK - 0.2, z) for x, z in pts] + [(11.3 + (x - 11.3) * 0.72, 28.0, 1.0 + (z - 1.0) * 0.72) for x, z in pts], 'paint', bevel=0.14, mirror=True)
    b.cyl((11.3, 27.9, 1.0), (11.3, 29.0, 1.0), 2.8, 10, 'dark', bevel=0.05, mirror=True)
    b.sphere((11.3, 29.0, 1.0), 2.1, 'steel', segs=10, rings=4, scale=(1, 0.65, 1), mirror=True)

    # ------------------------------------------------------------------ citadel: two steps up to the main turret's ring
    b.hull([(x * s, y, z) for s in (-1, 1) for x, y, z in
            [(14.6, DECK - 0.2, -51.0), (14.6, DECK - 0.2, -10.6), (14.2, 30.0, -50.4), (13.7, 30.0, -18.4), (8.0, 28.0, -11.4)]], 'paint2', bevel=0.24)
    b.hull([(x * s, y, z) for s in (-1, 1) for x, y, z in
            [(14.2, 29.9, -50.4), (14.2, 29.9, -18.4), (12.7, 36.1, -48.7), (12.7, 36.1, -20.2)]], 'dark', bevel=0.2)
    b.box((14.5, 26.0, -46.0), (14.85, 27.0, -22.0), 'lightw', bevel=0.0, mirror=True)
    # team on the citadel's front slope, under the main guns (trapezoid (13.7, 30, -18.4) -> (8, 28, -11.4), along its normal)
    b.hull([(x * s, y + 0.96 * d, z + 0.27 * d) for s in (-1, 1) for x, y, z in [(13.13, 29.8, -17.7), (8.57, 28.2, -12.1)] for d in (0.1, 0.26)],
           'team', bevel=0.03)
    # ------------------------------------------------------------------ stern block: team plate, off-centre funnel bank
    b.hull([(x * s, y, z) for s in (-1, 1) for x, z in [(9.3, -50.4), (9.3, -63.1)] for y in (DECK - 0.2, 26.7)], 'paint', bevel=0.16)
    b.hull([(x, y, z) for x in (-8.7, 8.7) for z in (-52.0, -62.5) for y in (26.76, 26.92)], 'team', bevel=0.03)
    b.box((-4.0, 5.0, -66.6), (4.0, 6.0, -66.1), 'lightr', bevel=0.0)
    b.box((-3.0, 8.0, -60.0), (3.0, 8.8, -59.5), 'lightr', bevel=0.0)

    # ------------------------------------------------------------------ fore turret: armoured half dome behind the rotary
    t = k.piece('turreta'); A = t.at
    t.cyl(A(0, -0.4, 0), A(0, 0.4, 0), 9.8, 16, 'dark', bevel=0.05)
    t.hull([A(x * s, y, z) for s in (-1, 1) for x, y, z in
            [(9.2, 0.0, 0.0), (7.7, 0.0, -4.6), (5.7, 0.0, -7.1), (4.1, 0.0, 6.9), (9.2, 8.4, 0.0), (7.7, 7.3, -4.6), (5.7, 5.3, -7.1),
             (5.1, 13.7, 0.0), (3.8, 12.6, -4.6), (1.8, 10.6, -7.1)]], 'paint', bevel=0.2)
    t.hull([A(x * s, y, z) for s in (-1, 1) for x, y, z in [(4.5, 13.76, -0.4), (3.3, 12.8, -4.0), (4.5, 13.92, -0.4), (3.3, 12.96, -4.0)]], 'team', bevel=0.03)

    # ------------------------------------------------------------------ rotary cannon (turn z, 120 deg per shot: 3-fold symmetric)
    g = k.piece('guna'); G = g.at
    g.cyl(G(0, 0, -0.2), G(0, 0, 3.8), 5.6, 12, 'dark', bevel=0.08)
    g.cyl(G(0, 0, 3.6), G(0, 0, 11.0), 2.2, 9, 'dark')
    for i in range(3):
        a = math.pi / 2 + i * 2 * math.pi / 3
        x, y = 3.26 * math.cos(a), 3.26 * math.sin(a)
        g.cyl(G(x, y, 3.0), G(x, y, 12.0), 1.85, 10, 'steel')
        g.cyl(G(x, y, 7.2), G(x, y, 8.0), 2.15, 10, 'dark', bevel=0.04)
        g.cyl(G(x, y, 12.0), G(x, y, 14.9), 2.2, 8, 'hazard', r2=2.0, bevel=0.05)
        g.cyl(G(x, y, 14.88), G(x, y, 14.96), 1.1, 8, 'black')
    # disc holding the three barrels together at their ends
    g.cyl(G(0, 0, 10.6), G(0, 0, 11.4), 3.6, 9, 'dark', bevel=0.04)

    # ------------------------------------------------------------------ main turret: the whole superstructure (origin 0, 36.92, -41.21)
    m = k.piece('turretb'); M = m.at
    m.cyl(M(0, -0.8, 2.0), M(0, 0.2, 2.0), 14.0, 16, 'dark', bevel=0.06)
    # lower wedge, wide wings at z 0, tapering to the gun mantlet
    m.hull([M(x * s, y, z) for s in (-1, 1) for x, y, z in
            [(17.0, -0.2, -0.1), (9.7, -0.2, 22.3), (8.5, -0.2, -12.3), (17.0, 6.6, -0.1), (9.7, 6.6, 22.3), (8.5, 6.6, -12.3)]], 'paint2', bevel=0.22)
    # upper deck with the wings
    m.hull([M(x * s, y, z) for s in (-1, 1) for x, y, z in
            [(16.6, 6.4, -0.1), (9.5, 6.4, 21.0), (8.5, 6.4, -12.3), (15.2, 13.4, -0.2), (9.7, 13.4, 16.8), (8.5, 13.4, 7.2),
             (17.0, 15.6, -0.1), (8.5, 15.6, -12.3), (8.5, 15.6, 7.2)]], 'paint', bevel=0.22)
    # team: wing tips (real top 15.6), front wedge plate (its plane runs from y 15.6 at z 7.2 to y 13.4 at z 16.8)
    m.hull([M(x, y, z) for y in (15.66, 15.82) for x, z in [(9.0, 6.2), (9.0, -11.6), (16.2, -0.1)]], 'team', bevel=0.03, mirror=True)
    m.hull([M(x * s, y + d, z) for s in (-1, 1) for x, y, z in [(7.9, 15.35, 8.2), (8.9, 13.5, 16.3)] for d in (0.08, 0.24)], 'team', bevel=0.03)
    # command tower (asymmetric, as the original: leans to port), team roof
    m.hull([M(x, y, z) for x, y, z in
            [(-14.4, 15.4, -3.1), (-8.2, 15.4, -12.0), (-8.2, 15.4, 2.6), (4.2, 15.4, -12.0), (4.2, 15.4, 0.8),
             (-13.4, 20.5, -3.1), (-7.9, 20.5, -11.0), (-7.9, 20.5, 1.7), (3.2, 20.5, -11.0), (3.2, 20.5, -0.2)]], 'paint', bevel=0.18)
    m.hull([M(x, y, z) for y in (20.56, 20.72) for x, z in [(-12.4, -3.0), (-7.6, -10.2), (2.6, -10.2), (2.6, -0.9), (-7.6, 0.9)]], 'team', bevel=0.03)
    m.hull([M(x, y, z) for x in (-11.0, 2.0) for y, z in [(16.8, 2.46), (19.3, 1.2), (16.8, 2.7), (19.3, 1.44)]], 'black', bevel=0.0)
    # rear block, aerial housing, tall mast
    m.hull([M(x, y, z) for x, z in [(-7.3, -12.0), (8.3, -12.0), (7.1, -16.6), (-6.1, -16.6)] for y in (5.9, 10.9)] +
           [M(x, 12.9, -12.0) for x in (-7.3, 8.3)], 'dark', bevel=0.14)
    m.hull([M(x, y, z) for x, z in [(1.8, -8.2), (6.7, -8.2), (6.7, -3.2), (1.8, -3.2)] for y in (15.4, 19.6)], 'dark', bevel=0.1)
    m.cyl(M(4.25, 19.4, -5.7), M(4.25, 37.4, -5.7), 1.0, 8, 'dark', r2=0.5)
    m.box(M(-0.6, 30.0, -6.2), M(9.1, 30.8, -5.2), 'dark', bevel=0.05)
    m.cyl(M(4.25, 37.4, -5.7), M(4.25, 37.9, -5.7), 0.45, 6, 'lightr')
    # ear mounts: side struts with short pods (the original's outrigger guns)
    m.hull([M(x, y, z) for x, z in [(9.0, -10.4), (21.0, -10.0), (21.0, -3.8), (14.6, -2.2)] for y in (1.6, 5.6)], 'dark', bevel=0.12, mirror=True)
    m.box(M(20.7, 0.2, -10.6), M(23.6, 7.1, -3.4), 'paint', bevel=0.14, mirror=True)
    m.box(M(20.9, 7.0, -9.9), M(23.3, 7.2, -4.2), 'lightw', bevel=0.0, mirror=True)
    # mantlet: three dark gun ports
    for x0, x1 in ((-9.1, -3.8), (-2.7, 2.6), (3.7, 9.0)):
        m.box(M(x0, 0.1, 20.2), M(x1, 10.1, 25.6), 'dark', bevel=0.12)

    # ------------------------------------------------------------------ jackets + barrels
    v = k.piece('sleeveb'); V = v.at
    for x in (-6.53, 0.0, 6.32):
        v.cyl(V(x, 0, 0.2), V(x, 0, 9.7), 2.9, 10, 'dark', r2=2.5, bevel=0.05)
    br = k.piece('barrelb1'); B = br.at
    br.cyl(B(0, 0, -6.2), B(0, 0, 11.6), 2.1, 10, 'steel')
    br.cyl(B(0, 0, 6.0), B(0, 0, 6.9), 2.4, 10, 'dark', bevel=0.04)
    br.cyl(B(0, 0, 11.4), B(0, 0, 15.3), 2.6, 8, 'hazard', r2=2.35, bevel=0.06)
    br.cyl(B(0, 0, 15.28), B(0, 0, 15.36), 1.3, 8, 'black')
    k.clone('barrelb2', 'barrelb1')
    k.clone('barrelb3', 'barrelb1')
