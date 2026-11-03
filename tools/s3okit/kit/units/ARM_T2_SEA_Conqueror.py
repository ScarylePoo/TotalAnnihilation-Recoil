"""Conqueror (ARM_T2_SEA_Conqueror) - Arm T2 cruiser. A fast waisted hull with one huge twin gun on a very tall hex
pedestal amidships. The turret carries broad swept wings far beyond the hull sides, so from above the ship is a cross:
a long light hull with a dark raised citadel, and across it the team-coloured wing span and turret roof with two long
guns reaching past the bow. Forward a small dome mount, aft a radar yard and the depth-charge launcher (flare3).
Pieces (TA layout): base, turret (turn y), barrel1/2 (turn x, recoil 6; barrel2 = clone), flare1/2/3 (empty),
wake1/2 (empty).
Value groups from above: light hull side decks + turret body, dark citadel + pedestal, near-black guns and vents, team on
the wings, turret roof and bow.
Floater, no waterline (water surface at model y = 0). Flat decks with no sheer: real deck tops are DECK and CIT.
Coordinates are ENGINE/global: X right, Y up, Z forward. mirror=True builds the -X twin sharing UVs."""
import math

UNIT = dict(
    wreck=dict(seed=31, drop=['barrel2'], pose={'turret': (0, 50, 0), 'barrel1': (22, 0, 0)}),
    preview_pose={},
)

DECK = 9.6      # side decks
CIT = 13.9      # citadel roof
# half outlines (half-width, z), bow to stern; the waist step at z -16.2 / -23.3 makes the plan concave
WATER = [(0.5, 49.8), (11.7, 29.4), (18.0, 12.1), (20.1, 4.8), (20.1, -16.2), (15.7, -23.3), (15.7, -43.5), (8.8, -51.7)]
DOUT = [(3.5, 44.3), (11.7, 29.4), (18.0, 12.1), (20.1, 4.8), (20.1, -16.2), (15.7, -23.3), (15.7, -43.5), (8.8, -51.7)]
SEGS = ((12.1, 50.0), (-16.2, 12.1), (-23.3, -16.2), (-52.0, -23.3))


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
    # ------------------------------------------------------------------ hull in segments (crosses x = 0)
    for z0, z1 in SEGS:
        w, d = cut(WATER, z0, z1), cut(DOUT, z0, z1)
        b.hull(ring([(x * 0.8, z) for x, z in w], -1.6) + ring(w, 3.4), 'paint2', bevel=0.2)
        b.hull(ring(w, 3.4) + ring(d, DECK), 'paint', bevel=0.2)
    # ------------------------------------------------------------------ dark citadel (long raised deck)
    b.hull([(x * s, y, z) for s in (-1, 1) for x, y, z in
            [(3.6, DECK - 0.2, 36.2), (15.8, DECK - 0.2, 4.8), (15.7, DECK - 0.2, -21.5), (1.5, CIT, 36.2), (13.7, CIT, 4.8),
             (13.6, CIT, -21.5)]], 'paint2', bevel=0.22)
    b.hull([(x * s, y, z) for s in (-1, 1) for x, y, z in
            [(15.6, DECK - 0.2, -21.5), (15.5, DECK - 0.2, -43.5), (8.9, DECK - 0.2, -51.0), (13.7, CIT, -21.5),
             (13.6, CIT, -43.5), (8.3, CIT, -49.4)]], 'paint2', bevel=0.22)
    # dark gunwale line on the wide side decks + a bow plate
    b.hull([(x, y, z) for y in (DECK - 0.05, DECK + 0.2) for x, z in ((17.8, -14.0), (19.2, -12.0), (19.2, 4.0), (17.0, 11.0))],
           'dark', bevel=0.03, mirror=True)
    # team spearhead on the bow deck (the deck is flat at DECK)
    b.hull([(x, y, z) for y in (DECK + 0.08, DECK + 0.26) for x, z in ((0.0, 37.6), (0.0, 42.8), (3.0, 42.0), (9.6, 29.4), (5.4, 27.0))],
           'team', bevel=0.03, mirror=True)
    b.cyl((0, DECK, 43.4), (0, DECK + 0.8, 43.4), 0.42, 6, 'lightr')
    # team bands on the stern deck edges of the citadel roof
    b.hull([(x, y, z) for y in (CIT + 0.08, CIT + 0.26) for x, z in ((9.6, -36.0), (13.0, -36.0), (13.0, -22.0), (9.6, -22.0))],
           'team', bevel=0.03, mirror=True)
    # ------------------------------------------------------------------ dome mount forward of the pedestal
    b.hull([(x * s, y, z) for s in (-1, 1) for x, y, z in
            [(5.1, CIT, 16.9), (7.2, CIT, 11.8), (5.1, CIT, 6.7), (4.3, 17.2, 16.1), (6.1, 17.2, 11.8), (4.3, 17.2, 7.5),
             (2.9, 19.6, 14.7), (4.1, 19.6, 11.8), (2.9, 19.6, 8.9)]], 'paint', bevel=0.15)
    b.cyl((0, 19.5, 11.8), (0, 20.3, 11.8), 1.5, 8, 'black')
    # side vents either side of the pedestal
    for z0, z1 in ((-1.0, 2.2), (-7.1, -4.0)):
        b.box((9.3, CIT - 0.1, z0), (11.9, 16.0, z1), 'dark', bevel=0.1, mirror=True)
        b.box((9.8, 16.0, z0 + 0.5), (11.4, 16.14, z1 - 0.5), 'black', bevel=0.0, mirror=True)
    # ------------------------------------------------------------------ very tall hex pedestal (crosses x = 0)
    b.hull([(x * s, y, z) for s in (-1, 1) for x, y, z in
            [(4.0, CIT - 0.1, 7.1), (8.1, CIT - 0.1, -3.2), (8.1, CIT - 0.1, -17.1), (4.0, CIT - 0.1, -22.0),
             (2.3, 24.5, -6.1), (4.7, 24.5, -10.2), (2.3, 24.5, -14.2)]], 'paint2', bevel=0.2)
    # ------------------------------------------------------------------ radar yard: post + spar wider than the waist
    b.hull([(x * s, y, z) for s in (-1, 1) for x, y, z in
            [(2.4, CIT - 0.1, -26.8), (2.4, CIT - 0.1, -33.7), (1.8, 20.7, -27.6), (1.8, 20.7, -33.2)]], 'paint', bevel=0.12)
    b.hull([(x * s, y, z) for s in (-1, 1) for x, y, z in
            [(3.2, 17.0, -29.2), (3.2, 17.0, -33.4), (18.4, 17.1, -31.8), (18.4, 17.1, -34.0), (18.4, 17.9, -31.8),
             (18.4, 17.9, -34.0), (3.2, 18.0, -29.2), (3.2, 18.0, -33.4)]], 'dark', bevel=0.08)
    b.cyl((18.3, 17.2, -32.9), (18.9, 17.2, -32.9), 0.5, 6, 'lightr', mirror=True)
    # ------------------------------------------------------------------ depth-charge launcher (flare3 at y 19)
    b.box((-9.0, CIT - 0.1, -46.0), (9.0, 14.6, -39.0), 'dark', bevel=0.1)
    b.hull([(x * s, y, z) for s in (-1, 1) for x, y, z in
            [(4.5, 14.5, -39.0), (4.5, 14.5, -47.5), (4.5, 19.0, -39.8), (4.5, 19.0, -47.0), (3.0, 19.0, -40.4), (3.0, 19.0, -46.4)]],
           'paint', bevel=0.12)
    b.cyl((0, 18.9, -43.5), (0, 19.3, -43.5), 2.1, 10, 'black')
    b.box((-2.4, 6.6, -51.9), (2.4, 7.6, -51.4), 'lightr', bevel=0.0)

    # ------------------------------------------------------------------ turret body: long light block, dark mantlet
    t = k.piece('turret'); T = t.at
    t.hull([T(x * s, y, z) for s in (-1, 1) for x, y, z in
            [(8.3, 0.0, 9.0), (8.3, 0.0, -10.3), (8.3, 7.1, 5.8), (8.3, 7.1, -10.3), (8.3, 11.0, -1.1), (8.3, 11.0, -8.5)]],
           'paint', bevel=0.25)
    # dark gun-house front (the guns' slots) between the cheeks
    t.hull([T(x * s, y, z) for s in (-1, 1) for x, y, z in
            [(6.4, 0.7, 10.1), (6.4, 7.0, 10.1), (6.4, 0.7, 7.0), (6.4, 8.2, 5.8)]], 'dark', bevel=0.12)
    t.box(T(-5.0, 2.2, 9.98), T(-1.0, 3.8, 10.3), 'black', bevel=0.0)
    t.box(T(1.0, 2.2, 9.98), T(5.0, 3.8, 10.3), 'black', bevel=0.0)
    # rear ammo bustle
    t.box(T(-5.6, 0.1, -13.1), T(5.6, 6.7, -9.8), 'dark', bevel=0.15)
    # team roof: the top is flat at 11.0, the rear deck at 7.1
    t.hull([T(x * s, y, z) for s in (-1, 1) for x, y, z in
            [(7.5, 11.08, -1.6), (7.5, 11.08, -8.0), (7.5, 11.26, -1.6), (7.5, 11.26, -8.0)]], 'team', bevel=0.03)
    # sloped front roof in team too (plate parallel to the slope between y 7.1 and y 11)
    t.hull([T(x * s, y, z) for s in (-1, 1) for x, y, z in
            [(7.5, 7.5, 5.4), (7.5, 10.9, -0.9), (7.5, 7.68, 5.5), (7.5, 11.08, -0.8)]], 'team', bevel=0.03)
    # ------------------------------------------------------------------ swept wings (the ship's cross silhouette)
    # the turret origin is a hair off x = 0, so no mirror=True: each wing is built outright
    for s in (-1, 1):
        t.hull([T(x * s, y, z) for x, y, z in
                [(8.0, 5.0, 2.4), (8.0, 5.0, -7.4), (8.0, 6.2, 2.4), (8.0, 6.2, -7.4),
                 (25.8, 5.3, -2.0), (25.8, 5.3, -6.6), (25.8, 6.0, -2.0), (25.8, 6.0, -6.6)]], 'team', bevel=0.08)
        # dark leading edge spar and light tip block
        t.hull([T(x * s, y, z) for x, y, z in
                [(8.0, 4.9, 2.7), (8.0, 6.3, 2.7), (8.0, 4.9, 1.9), (8.0, 6.3, 1.9), (25.8, 5.2, -1.7), (25.8, 6.1, -1.7),
                 (25.8, 5.2, -2.3), (25.8, 6.1, -2.3)]], 'dark', bevel=0.05)
        t.box(T(min(25.4 * s, 27.4 * s), 5.0, -7.0), T(max(25.4 * s, 27.4 * s), 6.4, -1.6), 'paint', bevel=0.1)
    # sensors on the roof: drum, mast (not mirrored: the mast stands at local x -4)
    t.cyl(T(4.2, 11.2, -4.8), T(4.2, 13.1, -4.8), 2.0, 8, 'dark', r2=1.6, bevel=0.05)
    t.cyl(T(4.2, 13.1, -4.8), T(4.2, 13.3, -4.8), 1.0, 8, 'lightc')
    t.cyl(T(-4.0, 11.2, -4.8), T(-4.0, 12.4, -4.8), 1.3, 8, 'dark', r2=1.0)
    t.cyl(T(-4.0, 12.4, -4.8), T(-4.0, 24.6, -4.8), 0.55, 8, 'dark', r2=0.28)
    t.cyl(T(-4.0, 24.6, -4.8), T(-4.0, 25.1, -4.8), 0.3, 6, 'lightr')

    # ------------------------------------------------------------------ barrels (recoil 6 back into the gun house)
    br = k.piece('barrel1'); B = br.at
    br.cyl(B(0, 0, -6.4), B(0, 0, 9.2), 1.7, 10, 'dark', r2=1.45)
    br.cyl(B(0, 0, 9.2), B(0, 0, 25.0), 1.15, 10, 'steel', r2=1.0)
    br.cyl(B(0, 0, 25.0), B(0, 0, 28.4), 1.5, 8, 'dark', r2=1.35, rot=math.pi / 8, bevel=0.05)
    br.cyl(B(0, 0, 28.38), B(0, 0, 28.46), 0.7, 8, 'black')
    k.clone('barrel2', 'barrel1')
