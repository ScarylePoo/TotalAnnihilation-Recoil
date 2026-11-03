"""Escort (ARM_T2_SEA_Escort) - Arm radar jammer ship. Small light hull with a tall stepped deckhouse aft and the
jammer: a long twin-prong antenna (fork) cantilevered forward from the deckhouse face over the whole foredeck, which
spins about its own long axis while jamming. From above: a short light hull, a dark stepped tower with a team roof,
and the thin dark spike of the antenna with light emitter tips running to the bow over a team foredeck chevron.
Pieces (TA layout): base, fork (spin z; origin 0.06, 14.11, -7.4, extends 32.7 forward), wake1/2 (empty).
Value groups from above: light hull, dark (paint2) tower and lower hull, near-black antenna, team tower roof, side
decks and bow chevron.
Floater, no waterline (water surface at model y = 0).
Coordinates are ENGINE/global: X right, Y up, Z forward. mirror=True builds the -X twin sharing UVs."""
import math

UNIT = dict(
    res=1024,
    wreck=dict(seed=11, pose={'fork': (25, 10, 0)}),
    preview_pose={'fork': (0, 0, 30)},
)

DECK = 6.0
OUT = [(0.0, 32.4), (4.0, 26.0), (9.6, 14.0), (12.8, 2.0), (13.6, -10.0), (13.4, -24.0), (11.0, -31.0), (6.0, -32.4)]


def ring(pts, y, sx=1.0, sz=1.0, dz=0.0, sheer=0.0):
    out = []
    for x, z in pts:
        yy = y + sheer * max(0.0, (z - 8.0) / 24.4) ** 1.5
        for s in ((-1, 1) if x > 0 else (1,)):
            out.append((x * sx * s, yy, z * sz + dz))
    return out


def build(k):
    b = k.piece('base')
    # ------------------------------------------------------------------ hull
    b.hull(ring(OUT, -1.4, 0.62, 0.9, -1.0) + ring(OUT, 2.0, 0.95, 0.98), 'paint2', bevel=0.2)
    b.hull(ring(OUT, 2.0, 0.95, 0.98) + ring(OUT, DECK), 'paint', bevel=0.2)
    # team side decks either side of the deckhouse (real top of the convex hull aft of the sheer: DECK)
    b.hull([(x, y, z) for y in (DECK + 0.08, DECK + 0.24) for x, z in ((9.0, -26.0), (12.0, -24.0), (12.6, -6.0), (9.0, -6.0))],
           'team', bevel=0.03, mirror=True)
    # foredeck chevron in team colour (under the antenna): points forward. Hull top rises with the sheer.
    def dy(z):
        return DECK
    for (x0, z0), (x1, z1) in (((0.0, 24.0), (7.4, 10.0)),):
        pts = []
        for x, z in ((0.0, 25.0), (0.0, 18.0), (8.4, 9.0), (8.4, 3.0)):
            pts += [(x, dy(z) + 0.1, z), (x, dy(z) + 0.26, z)]
        b.hull(pts, 'team', bevel=0.03, mirror=True)
    # dark rim lines and a bow light
    b.hull([(x, DECK + d, z) for d in (-0.05, 0.18) for x, z in ((11.6, -26.0), (12.9, -14.0), (12.4, 0.0))],
           'dark', bevel=0.03, mirror=True)
    b.cyl((0, dy(29.0) + 0.0, 29.0), (0, dy(29.0) + 0.6, 29.0), 0.35, 6, 'lightr')
    b.box((-1.6, 4.6, -32.2), (1.6, 5.4, -31.9), 'lightr', bevel=0.0)
    # ------------------------------------------------------------------ stepped deckhouse (aft): lower block + tower
    b.hull([(x * s, y, z) for s in (-1, 1) for x, y, z in
            [(8.4, DECK - 0.2, -4.0), (8.4, DECK - 0.2, -30.0), (7.6, 11.0, -6.0), (7.6, 11.0, -29.0)]], 'paint2', bevel=0.2)
    b.hull([(x * s, y, z) for s in (-1, 1) for x, y, z in
            [(6.2, 10.8, -8.4), (6.2, 10.8, -27.0), (5.0, 18.2, -10.6), (5.0, 18.2, -25.2), (5.6, 14.0, -7.2)]],
           'paint2', bevel=0.2)
    b.hull([(x * s, y, z) for s in (-1, 1) for x, y, z in
            [(4.3, 18.15, -11.4), (4.3, 18.15, -24.4), (4.2, 18.36, -11.3), (4.2, 18.36, -24.3)]], 'team', bevel=0.03)
    # team roof of the lower block (aft shoulders), light trim on the front face
    b.hull([(x, y, z) for y in (11.0, 11.18) for x, z in ((1.0, -28.6), (7.2, -28.6), (7.2, -24.0), (1.0, -24.0))],
           'team', bevel=0.03, mirror=True)
    b.hull([(x * s, y, z) for s in (-1, 1) for x, y, z in
            [(5.0, 16.0, -8.4), (5.0, 16.8, -9.4), (4.9, 16.0, -8.2), (4.9, 16.8, -9.2)]], 'glass', bevel=0.0)
    # antenna mount on the tower face: a dark ring the fork's hub turns in
    b.cyl((0.06, 14.11, -8.6), (0.06, 14.11, -7.0), 3.0, 12, 'dark', bevel=0.08)
    # jammer dishes / masts on the roof
    b.cyl((0, 18.3, -20.0), (0, 23.4, -20.0), 0.5, 8, 'dark', r2=0.3)
    b.cyl((0, 23.4, -20.0), (0, 23.8, -20.0), 0.32, 6, 'lightr')
    b.cyl((-2.6, 18.3, -14.2), (-2.6, 19.4, -14.2), 1.4, 10, 'paint', bevel=0.05)
    b.cyl((2.6, 18.3, -14.2), (2.6, 19.4, -14.2), 1.4, 10, 'paint', bevel=0.05)
    # stern: depth-charge rack / vents
    b.box((-5.0, DECK, -31.6), (5.0, DECK + 1.2, -30.0), 'dark', bevel=0.08)

    # ------------------------------------------------------------------ fork: spinning twin-prong jammer antenna
    f = k.piece('fork'); F = f.at
    f.cyl(F(0, 0, 0.6), F(0, 0, 4.0), 2.4, 12, 'dark', r2=1.8, bevel=0.06)      # hub
    f.cyl(F(0, 0, 4.0), F(0, 0, 31.0), 0.9, 8, 'dark', r2=0.6)                  # central boom
    # two prongs (y +-3.6) joined to the hub by a light yoke; light emitter pods at the tips
    for s in (-1, 1):
        f.hull([F(x, y * s, z) for x in (-0.75, 0.75) for y, z in ((0.0, 3.0), (0.0, 6.0), (3.8, 7.8), (3.8, 5.4))],
               'paint', bevel=0.08)
        f.hull([F(x, y * s, z) for x in (-0.7, 0.7) for y, z in ((3.2, 6.8), (4.2, 6.8), (3.2, 28.0), (4.2, 26.6))],
               'dark', bevel=0.08)
        f.cyl(F(0, 3.7 * s, 26.0), F(0, 3.7 * s, 30.6), 1.0, 8, 'paint', r2=0.6, bevel=0.04)
        f.cyl(F(0, 3.7 * s, 30.55), F(0, 3.7 * s, 30.9), 0.5, 8, 'lightc')
    f.cyl(F(0, 0, 30.8), F(0, 0, 32.6), 0.9, 8, 'lightc', r2=0.3)
