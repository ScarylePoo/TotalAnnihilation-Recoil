"""Colossus (ARM_T2_SEA_Colossus) - Arm light carrier. The def has isairbase + builder (workertime 800, no build list, no
assist, no reclaim), the COB's QueryLandingPad alternates landpad1 / landpad2 and spins the radar: aircraft land and are
repaired on the two pads, at y 27.05, z -52.5 and z 37.5. So the deck is two broad flat flight decks either side of a
central pagoda island, each with a big hazard-striped pad ring exactly round its pad point; no guns anywhere.
From above: a broad blunt light hull ring, two big dark decks (the largest flat surfaces of any Arm ship), team bands along
the deck edges, yellow-black rings, and the wide team roof of the island with radar arrays out to the hull sides. The
Millenium is its opposite: pointed, light, tall, all turret and barrel.
Pieces (TA layout): base, landpad1/2 (empty; the aircraft's land points), radar (spin y), wake1/2 (empty).
Value groups from above: light hull ring + island waist, dark flight decks and lower island, near-black arrays, team on the
deck bands and island roof, hazard on the pads.
Floater, no waterline (water surface at model y = 0). The hull is not sheered: the deck tops are exactly DECK, a little under
the pad height so plates on them stay at or below the aircraft's land point.
Coordinates are ENGINE/global: X right, Y up, Z forward. mirror=True builds the -X twin sharing UVs."""
import math

UNIT = dict(
    wreck=dict(seed=48, remove=['radar']),
    preview_pose={},
)

HULLTOP = 14.4
DECK = 26.6     # flight deck top; pads at 27.05
PADR, PADI = 11.5, 7.0
PADS = (37.5, -52.5)     # z of landpad2, landpad1
WATER = [(7.2, 80.2), (25.4, 49.7), (28.3, 35.6), (29.0, -5.7), (28.3, -54.4), (14.3, -71.3)]
HOUT = [(12.0, 72.1), (25.4, 49.7), (28.3, 35.6), (29.0, -5.7), (28.3, -54.4), (14.3, -71.3)]
SEGS = ((35.6, 81.0), (2.5, 35.6), (-20.0, 2.5), (-54.4, -20.0), (-72.0, -54.4))


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


def pad(b, zc):
    """landing pad: one sector per wedge of the hazard ring (a convex hull of a ring would fill its hole),
    built on the +X side and mirrored, with a light centre disc."""
    y0, y1 = DECK + 0.06, DECK + 0.26
    n = 8
    for i in range(n):
        a0 = math.pi * i / n; a1 = math.pi * (i + 1) / n
        pts = []
        for a, r in ((a0, PADR), (a1, PADR), (a0, PADI), (a1, PADI)):
            for y in (y0, y1):
                pts.append((r * math.sin(a), y, zc + r * math.cos(a)))
        b.hull(pts, 'hazard', bevel=0.02, mirror=True)
    b.cyl((0, y0, zc), (0, y1, zc), PADI - 2.2, 16, 'paint', bevel=0.03)


def build(k):
    b = k.piece('base')
    # ------------------------------------------------------------------ broad hull in segments (crosses x = 0)
    for z0, z1 in SEGS:
        w, h = cut(WATER, z0, z1), cut(HOUT, z0, z1)
        b.hull(ring([(x * 0.9, min(z, 76.0)) for x, z in w], -1.6) + ring(w, 3.6), 'paint2', bevel=0.25)
        b.hull(ring(w, 3.6) + ring(h, HULLTOP), 'paint', bevel=0.25)
    # dark gunwale walkway on the light hull ring
    b.hull([(x, y, z) for y in (HULLTOP - 0.05, HULLTOP + 0.22) for x, z in ((27.0, 30.0), (27.8, -5.0), (27.0, -50.0), (26.0, -50.0), (26.8, -5.0), (26.0, 30.0))],
           'dark', bevel=0.03, mirror=True)
    # bow and stern lights
    b.cyl((0, HULLTOP, 69.8), (0, HULLTOP + 0.8, 69.8), 0.6, 6, 'lightr')
    b.box((-5.0, 9.0, -71.3), (5.0, 10.4, -70.7), 'lightr', bevel=0.0)
    # ------------------------------------------------------------------ fore flight deck (dark, sloped flanks)
    b.hull(ring([(10.0, 70.0), (25.0, 40.0), (25.0, 2.6)], HULLTOP - 0.1) + ring([(7.5, 65.0), (20.0, 40.0), (20.0, 2.6)], DECK),
           'paint2', bevel=0.3)
    # ------------------------------------------------------------------ aft flight deck, extended to clear the pad ring
    b.hull(ring([(22.5, -20.0), (22.5, -58.0), (14.0, -69.0)], HULLTOP - 0.1) + ring([(17.5, -20.0), (17.5, -58.0), (12.0, -66.0)], DECK),
           'paint2', bevel=0.3)
    # team bands along the deck edges (flat deck: real top = DECK)
    # two hulls: the band bends inward at the bow, and one convex hull would fill that bend across the pad ring
    b.hull([(x, y, z) for y in (DECK + 0.06, DECK + 0.26) for x, z in ((12.6, 4.0), (19.2, 4.0), (19.2, 40.2), (12.6, 46.0))],
           'team', bevel=0.03, mirror=True)
    b.hull([(x, y, z) for y in (DECK + 0.06, DECK + 0.26) for x, z in ((12.6, 46.0), (19.2, 40.2), (9.4, 59.6), (6.6, 58.0))],
           'team', bevel=0.03, mirror=True)
    b.hull([(x, y, z) for y in (DECK + 0.06, DECK + 0.26) for x, z in ((12.0, -21.4), (16.8, -21.4), (16.8, -57.0), (12.0, -57.0))],
           'team', bevel=0.03, mirror=True)
    # light centre line between the pads and the island, and deck lift hatches
    b.box((-1.2, DECK, 3.4), (1.2, DECK + 0.26, 24.0), 'paint', bevel=0.04)
    b.box((-1.2, DECK, -39.0), (1.2, DECK + 0.26, -21.0), 'paint', bevel=0.04)
    b.box((-1.0, DECK, 50.6), (1.0, DECK + 0.26, 61.0), 'paint', bevel=0.04)
    for zc, dz in ((14.0, 5.6), (-30.0, 4.8)):
        b.box((4.0, DECK, zc - dz), (11.8, DECK + 0.14, zc + dz), 'black', bevel=0.0, mirror=True)
    # deck-edge lights
    for z in (8.0, 24.0, 38.0):
        b.box((19.6, DECK + 0.02, z - 0.5), (19.95, DECK + 0.2, z + 0.5), 'lightc', bevel=0.0, mirror=True)
    # the two pads, centred on the land points
    for z in PADS:
        pad(b, z)
    # ------------------------------------------------------------------ midship reactor deck between the flight decks
    for z in (-4.0, -13.0):
        b.cyl((18.6, HULLTOP - 0.1, z), (18.6, HULLTOP + 2.6, z), 3.4, 12, 'dark', r2=2.8, bevel=0.06, mirror=True)
        b.cyl((18.6, HULLTOP + 2.6, z), (18.6, HULLTOP + 2.72, z), 2.1, 12, 'lightc', mirror=True)
    # ------------------------------------------------------------------ pagoda island (crosses x = 0)
    b.box((-12.5, HULLTOP - 0.1, -20.0), (12.5, 26.8, 2.5), 'paint2', bevel=0.25)
    b.hull([(x * s, y, z) for s in (-1, 1) for x, y, z in
            [(12.2, 26.7, 2.2), (12.2, 26.7, -19.7), (8.8, 42.6, -3.8), (8.8, 42.6, -13.5)]], 'paint', bevel=0.25)
    # flared bridge head and its team roof
    b.hull([(x * s, y, z) for s in (-1, 1) for x, y, z in
            [(8.8, 42.4, -3.8), (8.8, 42.4, -13.5), (12.5, 43.2, 2.5), (12.5, 43.2, -20.0), (12.5, 47.5, 2.5), (12.5, 47.5, -20.0)]],
           'paint2', bevel=0.2)
    b.hull([(x * s, y, z) for s in (-1, 1) for x, y, z in
            [(11.9, 47.46, 1.9), (11.9, 47.46, -19.4), (7.5, 52.5, -2.5), (7.5, 52.5, -15.0)]], 'team', bevel=0.12)
    # bridge windows round the head
    b.box((-10.5, 44.6, 2.48), (10.5, 46.0, 2.62), 'glass', bevel=0.0)
    b.box((12.48, 44.6, -18.0), (12.62, 46.0, 0.5), 'glass', bevel=0.0, mirror=True)
    # radar arrays: three stacked tiers out to the hull sides, tip lights on the widest
    for y0, y1, r0, r1, xt, t0, t1 in ((31.3, 32.9, -3.4, -14.8, 30.3, -6.6, -10.9), (35.0, 36.2, -4.5, -13.5, 25.4, -7.2, -11.0),
                                       (38.4, 39.6, -5.2, -12.8, 22.2, -7.4, -10.8)):
        b.hull([(x, y, z) for y in (y0, y1) for x, z in ((9.0, r0), (9.0, r1), (xt, t0), (xt, t1))], 'dark', bevel=0.08, mirror=True)
    b.cyl((30.2, 32.1, -8.7), (31.0, 32.1, -8.7), 0.9, 8, 'lightr', mirror=True)

    # ------------------------------------------------------------------ radar (spin y): wide light bar on a dark drum
    r = k.piece('radar'); R = r.at
    r.cyl(R(0, -0.1, 0), R(0, 1.4, 0), 3.8, 12, 'dark', r2=2.8, bevel=0.05)
    r.hull([R(x * s, y, z) for s in (-1, 1) for x, y, z in
            [(10.4, 1.2, 6.2), (10.4, 5.0, 6.2), (10.4, 1.2, 4.2), (10.4, 5.0, 4.2), (3.8, 0.8, 2.6), (3.8, 6.2, 2.6),
             (3.8, 0.8, -1.4), (3.8, 6.2, -1.4)]], 'paint', bevel=0.12)
    r.box(R(-9.0, 1.7, 6.14), R(9.0, 4.5, 6.3), 'black', bevel=0.0)
