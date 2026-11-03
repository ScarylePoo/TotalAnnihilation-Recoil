"""Ranger (ARM_T2_SEA_Ranger) - Arm T2 missile ship. A long pointed hull whose whole aft half is a vertical launch bay:
a low gabled hangar with two team-coloured sliding roof halves. On activation the roofs slide outward over the side
decks (door1/door2 move x), the lift (plate) rises 10.875 and the launcher cradle stands straight up with its two big
cruise missiles. Forward stands a dark arrow-shaped deckhouse with a light pyramid mast carrying the AA missile box
high above the ship (launcher2, tubes on the front face, team roof).
From above: light hull, dark arrowhead, two broad team roof panels aft (the ship's tell: no gun, one long team hangar),
open = black bay with the white missiles between the panels.
Pieces (TA layout): base, plate (move y), turret1 (static post), launcher1 (turn x, -90 when up), rocket1/2 (hide on
fire, shown again by Go), door1/door2 (door2 = mirrored clone), turret2 (static), launcher2 (turn y + x), flare1/2
(empty), wake1/2 (empty). The preview shows the OPEN state; the ship rests closed.
Value groups from above: light hull / mast / missile box, dark deckhouse and door flanks, near-black bay, team roofs.
Floater, no waterline (water surface at model y = 0). The hull is built in flat-decked segments with no sheer, so the
deck top is exactly DECK and overlay plates sit at DECK + 0.08.
Coordinates are ENGINE/global: X right, Y up, Z forward. mirror=True builds the -X twin sharing UVs."""
import math

UNIT = dict(
    # the launcher sits under the closed roofs at rest; the script raises it, so give it full texture
    always_visible=['plate', 'turret1', 'launcher1', 'rocket1', 'rocket2'],
    wreck=dict(seed=23, drop=['door2'], pose={'launcher2': (10, 40, 0), 'door1': (0, 0, -18)}),
    preview_pose={'door1': {'move': (-10.5, 0, 0)}, 'door2': {'move': (10.875, 0, 0)},
                  'plate': {'move': (0, 10.875, 0)}, 'launcher1': (-90, 0, 0)},
)

DECK = 12.4
BAY = (10.5, -47.2, -11.2)      # bay half width, aft and forward wall (as the 3DO)
# half outlines (half-width, z), bow to stern: at the water, at the flare, at deck level
WATER = [(0.5, 56.0), (13.6, 31.6), (20.9, 13.0), (23.4, 4.8), (23.4, -37.8), (20.9, -53.6), (10.0, -59.9)]
FLARE = [(0.5, 53.9), (12.7, 31.7), (19.6, 13.0), (21.8, 5.0), (21.8, -37.7), (19.6, -50.5), (9.3, -56.4)]
DOUT = [(2.5, 51.1), (12.7, 31.7), (19.6, 13.0), (21.8, 5.0), (21.8, -37.7), (19.6, -50.5), (9.3, -56.4)]


def cut(pts, z0, z1):
    """outline pts between stations z0 and z1, with the end stations interpolated"""
    P = sorted({z: x for x, z in pts}.items())
    zs = [z for z, _ in P]; xs = [x for _, x in P]

    def xat(z):
        for i in range(len(zs) - 1):
            if zs[i] <= z <= zs[i + 1]:
                t = (z - zs[i]) / (zs[i + 1] - zs[i]); return xs[i] + t * (xs[i + 1] - xs[i])
        return xs[0] if z < zs[0] else xs[-1]
    lo, hi = max(z0, zs[0]), min(z1, zs[-1])
    return [(xat(z), z) for z in sorted({lo, hi} | {z for z in zs if lo < z < hi})]


def ring(o, y):
    return [(x * s, y, z) for x, z in o for s in (-1, 1)]


def build(k):
    b = k.piece('base')
    bx, bz0, bz1 = BAY
    # ------------------------------------------------------------------ lower hull under everything (crosses x = 0)
    for z0, z1 in ((13.0, 60.0), (-37.7, 13.0), (-60.0, -37.7)):
        b.hull(ring(cut(WATER, z0, z1), -1.6) + ring(cut(WATER, z0, z1), 0.7), 'paint2', bevel=0.2)
    # ------------------------------------------------------------------ freeboard ahead of the bay (crosses x = 0)
    for z0, z1 in ((13.0, 60.0), (bz1, 13.0)):
        b.hull(ring(cut(WATER, z0, z1), 0.7) + ring(cut(FLARE, z0, z1), 6.8), 'paint2', bevel=0.2)
        b.hull(ring(cut(FLARE, z0, z1), 6.8) + ring(cut(DOUT, z0, z1), DECK), 'paint', bevel=0.2)
    # stern block behind the bay
    for z0, z1 in ((-60.0, bz0),):
        b.hull(ring(cut(WATER, z0, z1), 0.7) + ring(cut(FLARE, z0, z1), 6.8), 'paint2', bevel=0.2)
        b.hull(ring(cut(FLARE, z0, z1), 6.8) + ring(cut(DOUT, z0, z1), DECK), 'paint', bevel=0.2)
    # side blocks either side of the bay: their inner faces are the bay walls
    wo = cut(WATER, bz0, bz1); fo = cut(FLARE, bz0, bz1); deck = cut(DOUT, bz0, bz1)
    b.hull([(x, 0.7, z) for x, z in wo] + [(bx, 0.7, bz0), (bx, 0.7, bz1)]
           + [(x, 6.8, z) for x, z in fo] + [(bx, 6.8, bz0), (bx, 6.8, bz1)], 'paint2', bevel=0.2, mirror=True)
    b.hull([(x, 6.8, z) for x, z in fo] + [(bx, 6.8, bz0), (bx, 6.8, bz1)]
           + [(x, DECK, z) for x, z in deck] + [(bx, DECK, bz0), (bx, DECK, bz1)], 'paint', bevel=0.2, mirror=True)
    # bay floor (only seen with the lift up)
    b.box((-bx, 0.7, bz0), (bx, 0.9, bz1), 'black', bevel=0.0)
    # dark door tracks along the bay edge, running out over the side decks (the roofs slide on them)
    for z in (-44.0, -30.5, -15.0):
        b.box((bx + 0.3, DECK, z - 1.2), (21.2, DECK + 0.26, z + 1.2), 'dark', bevel=0.04, mirror=True)
    # gunwale walkway
    b.hull([(x, y, z) for y in (DECK - 0.05, DECK + 0.2) for x, z in ((18.2, -48.0), (20.4, -37.7), (20.4, 5.0), (18.6, 12.0))],
           'dark', bevel=0.03, mirror=True)
    # stern: light, bollards, team transom plate
    b.box((-3.4, 8.4, -56.9), (3.4, 9.6, -56.0), 'lightr', bevel=0.0)
    b.cyl((6.0, DECK, -53.0), (6.0, DECK + 1.4, -53.0), 0.8, 8, 'dark', mirror=True)
    b.hull([(x, y, z) for y in (DECK + 0.08, DECK + 0.26) for x, z in ((0.0, -49.2), (9.6, -49.2), (8.6, -53.6), (0.0, -55.6))],
           'team', bevel=0.03, mirror=True)
    # ------------------------------------------------------------------ dark arrowhead deckhouse (crosses x = 0)
    b.hull([(x * s, y, z) for s in (-1, 1) for x, y, z in
            [(3.9, DECK - 0.2, 39.1), (17.5, DECK - 0.2, 5.0), (11.9, DECK - 0.2, -11.0),
             (4.8, 19.5, 31.1), (15.2, 19.5, 5.0), (9.6, 19.5, -11.0),
             (4.8, 22.7, 29.8), (14.3, 22.7, 5.0), (8.6, 22.7, -11.0)]], 'paint2', bevel=0.25)
    # bridge glazing on the arrow's shoulders
    b.hull([(x, y, z) for x, y, z in ((5.6, 20.4, 28.4), (14.4, 20.4, 7.0), (5.5, 21.6, 28.0), (14.1, 21.6, 6.8),
                                      (5.3, 21.0, 28.0), (14.0, 21.0, 6.6))], 'glass', bevel=0.0, mirror=True)
    # team chevrons on the arrow roof (the roof is flat at 22.7)
    b.hull([(x, y, z) for y in (22.78, 22.96) for x, z in ((5.0, 27.0), (7.0, 22.5), (13.2, 6.4), (10.6, 6.4))],
           'team', bevel=0.03, mirror=True)
    # light pyramid mast up to the missile box
    b.hull([(x * s, y, z) for s in (-1, 1) for x, y, z in
            [(7.4, 22.6, 20.0), (7.4, 22.6, -7.0), (5.4, 28.8, 12.0), (5.4, 28.8, -4.0), (4.5, 32.2, 5.7), (4.5, 32.2, -1.5)]],
           'paint', bevel=0.2)
    b.cyl((0, 22.6, -9.2), (0, 31.0, -9.2), 0.6, 8, 'dark', r2=0.32)
    b.box((-4.4, 28.2, -9.6), (4.4, 28.8, -8.8), 'dark', bevel=0.05)
    b.cyl((0, 31.0, -9.2), (0, 31.4, -9.2), 0.34, 6, 'lightr')
    # foredeck: team spearhead, anchor plate, bow light
    b.hull([(x, y, z) for y in (DECK + 0.08, DECK + 0.26) for x, z in ((0.0, 38.2), (0.0, 48.0), (2.6, 47.0), (9.0, 33.8), (5.0, 30.0))],
           'team', bevel=0.03, mirror=True)
    b.cyl((0, DECK, 49.2), (0, DECK + 0.8, 49.2), 0.5, 6, 'lightr')

    # ------------------------------------------------------------------ sliding hangar roof halves (door2 = clone)
    d = k.piece('door1'); D = d.at
    IN = 11.6       # inner edge in local x: leaves a seam of 0.05 with the shifted mirrored twin
    d.hull([D(x, y, z) for x, y in ((0.0, 0.0), (2.3, 6.8), (3.2, 10.2), (IN, 10.2), (IN, 0.0)) for z in (-18.9, 19.3)],
           'paint2', bevel=0.2)
    # team roof panel: the flat top is at 10.2
    d.hull([D(x, y, z) for y in (10.28, 10.46) for x, z in ((3.9, -16.8), (IN - 0.3, -16.8), (IN - 0.3, 17.8), (3.9, 17.8))],
           'team', bevel=0.03)
    # dark ribs over the panel so the roof reads as two long sliding plates
    for z in (-6.0, 7.0):
        d.box(D(3.5, 10.2, z - 0.7), D(IN, 10.66, z + 0.7), 'dark', bevel=0.04)
    # outer roller boxes (they hang over the side decks when open)
    for z0, z1 in ((5.8, 16.4), (-12.7, -2.1)):
        d.box(D(-3.2, -0.2, z0), D(1.6, 4.2, z1), 'dark', bevel=0.12)
    k.clone('door2', 'door1', mirror_x=True)

    # ------------------------------------------------------------------ lift platform and launcher post
    p = k.piece('plate'); PP = p.at
    p.box(PP(-10.0, 0.9, -16.8), PP(10.0, 1.6, 18.4), 'dark', bevel=0.1)
    for s in (-1, 1):
        p.box(PP(s * 8.0 - 1.0, 1.6, -15.0), PP(s * 8.0 + 1.0, 2.0, 17.0), 'paint2', bevel=0.05)
    t = k.piece('turret1'); T = t.at
    t.box(T(-3.0, 0.5, -3.0), T(3.0, 4.6, 3.2), 'paint2', bevel=0.15)
    # ------------------------------------------------------------------ launcher cradle: spine, cross arms, rear bed
    l = k.piece('launcher1'); L = l.at
    l.box(L(-1.6, 0.2, -9.2), L(1.6, 4.4, 22.4), 'dark', bevel=0.15)
    l.box(L(-8.8, 0.0, -9.2), L(8.8, 1.2, 6.6), 'paint', bevel=0.12)
    l.box(L(-7.2, 0.8, 9.4), L(7.2, 2.5, 12.9), 'paint2', bevel=0.1)
    l.box(L(-7.2, 0.8, 18.4), L(7.2, 2.0, 21.0), 'paint2', bevel=0.1)
    # ------------------------------------------------------------------ cruise missile (rocket2 = clone)
    r = k.piece('rocket1'); R = r.at
    r.cyl(R(0, 0, -14.8), R(0, 0, 8.4), 1.7, 10, 'paint', bevel=0.05)
    r.cyl(R(0, 0, 8.4), R(0, 0, 15.1), 1.7, 10, 'lightr', r2=0.2)
    r.cyl(R(0, 0, -15.1), R(0, 0, -14.6), 1.1, 8, 'black')
    r.hull([R(x * s, y, z) for s in (-1, 1) for x, y, z in ((1.2, 0.0, -9.0), (3.3, 0.0, -13.2), (3.3, 0.0, -14.8), (1.2, 0.0, -14.8))]
           + [R(0, 0.25, -11.0), R(0, -0.25, -11.0)], 'dark', bevel=0.0)
    r.hull([R(x, y * s, z) for s in (-1, 1) for x, y, z in ((0.0, 1.2, -9.0), (0.0, 2.2, -13.2), (0.0, 2.2, -14.8), (0.0, 1.2, -14.8))]
           + [R(0.25, 0, -11.0), R(-0.25, 0, -11.0)], 'dark', bevel=0.0)
    r.cyl(R(0, 0, 3.0), R(0, 0, 5.4), 1.76, 10, 'team')
    k.clone('rocket2', 'rocket1')

    # ------------------------------------------------------------------ mast post and AA missile box
    t2 = k.piece('turret2'); T2 = t2.at
    t2.cyl(T2(0, -0.2, 0), T2(0, 4.2, 0), 2.6, 10, 'dark', r2=2.0, bevel=0.05)
    m = k.piece('launcher2'); M = m.at
    CX = 0.5        # the box is centred on local x = 0.5 (flares at -2.75 and 3.75)
    m.hull([M(CX + x * s, y, z) for s in (-1, 1) for x, y, z in
            [(5.4, 0.0, 8.0), (5.4, 0.0, -7.0), (8.7, 2.0, 8.0), (8.7, 2.0, -7.0), (8.7, 3.0, 8.0), (8.7, 3.0, -7.0),
             (5.4, 5.0, 8.0), (5.4, 5.0, -7.0)]], 'paint', bevel=0.18)
    m.hull([M(CX + x * s, y, z) for s in (-1, 1) for x, y, z in
            [(4.6, 5.06, 6.4), (4.6, 5.06, -5.6), (4.6, 5.24, 6.4), (4.6, 5.24, -5.6)]], 'team', bevel=0.03)
    # black tube face with two launch tubes in front of the flares
    m.box(M(CX - 6.4, 0.7, 7.95), M(CX + 6.4, 4.3, 8.25), 'black', bevel=0.0)
    for x in (-2.75, 3.75):
        m.cyl(M(x, 2.25, 8.2), M(x, 2.25, 8.42), 1.5, 10, 'steel')
    m.box(M(CX - 8.9, 1.9, -5.6), M(CX + 8.9, 3.1, 4.6), 'dark', bevel=0.08)
