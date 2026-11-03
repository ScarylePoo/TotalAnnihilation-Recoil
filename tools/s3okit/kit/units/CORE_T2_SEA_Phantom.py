"""Phantom (CORE_T2_SEA_Phantom) - Core radar jammer ship. A low stealth hull with four sponson lobes (narrow waist:
from above a double-pinched outline nothing else in the fleet has), no guns, and the tell: one huge bright two-tine
jammer fork spinning on the starboard side, running far forward over a dark channel.
Pieces (TA layout): base, fork (spin z, tines 3.8 from the axis: deck below it stays under y 4.1), wake1/2 (empty).
Value groups from above: dark deck (paint), darker lobes and spine sides (paint2), black channel/vents, bright steel
fork, team on the long port emitter box, the spine roof and the aft lobes.
Floater, no waterline (water surface at model y = 0).
Coordinates are ENGINE/global: X right, Y up, Z forward. mirror=True builds the -X twin sharing UVs."""

UNIT = dict(
    res=1024,
    wreck=dict(seed=23, drop=['fork']),
    preview_pose={'fork': (0, 0, 55)},
)

DECK = 3.4
WL = [(0.0, 36.0), (6.1, 34.9), (11.0, 22.0), (11.0, -30.9), (6.7, -34.9)]
TOP = [(0.0, 30.0), (4.8, 28.6), (11.7, 20.4), (11.7, -30.9), (6.0, -34.6)]


def ring(pts, y, sx=1.0, sz=1.0, dz=0.0):
    return [(x * sx * s, y, z * sz + dz) for x, z in pts for s in ((-1, 1) if x > 0 else (1,))]


def build(k):
    b = k.piece('base')
    # ------------------------------------------------------------------ hull: keel, waist, deck (crosses x = 0)
    b.hull(ring(WL, -2.0, 0.7, 0.9, -1.0) + ring(WL, 0.1), 'paint2', bevel=0.15)
    b.hull(ring(WL, 0.1) + ring(TOP, DECK - 0.5, 1.0, 1.0), 'paint2', bevel=0.15)
    b.hull(ring(TOP, DECK - 0.5) + ring(TOP, DECK, 0.985, 0.99), 'paint', bevel=0.1)
    # four sponson lobes (separate hulls so the waist stays pinched)
    b.hull([(x, 0.1, z) for x, z in [(10.0, -28.0), (17.0, -24.4), (17.0, -6.6), (10.0, -2.0)]] +
           [(x, -1.6, z) for x, z in [(10.0, -24.0), (14.0, -22.0), (14.0, -9.0), (10.0, -6.0)]] +
           [(x, 3.0, z) for x, z in [(11.2, -26.8), (11.2, -4.1)]], 'paint2', bevel=0.14, mirror=True)
    b.hull([(x, 0.1, z) for x, z in [(10.0, 5.4), (15.2, 7.8), (15.2, 24.0), (10.0, 27.0)]] +
           [(x, -1.6, z) for x, z in [(10.0, 9.0), (12.6, 10.0), (12.6, 22.0), (10.0, 24.0)]] +
           [(x, 3.0, z) for x, z in [(11.2, 7.0), (11.2, 20.0)]], 'paint2', bevel=0.14, mirror=True)
    # team panels on the aft lobes' slopes (lobe slope (17.0, 0.1) -> (11.2, 3.0); offset along its normal)
    nx, ny = 0.447, 0.894
    b.hull([(17.0 - 5.8 * f + nx * d, 0.1 + 2.9 * f + ny * d, z) for f in (0.08, 0.85) for z in (-22.8, -9.4)
            for d in (0.1, 0.24)], 'team', bevel=0.03, mirror=True)
    # forward lobes: dark vents + a small emitter dome each
    b.cyl((13.0, 0.9, 15.8), (13.0, 2.2, 15.8), 1.7, 10, 'dark', r2=1.2, bevel=0.05, mirror=True)
    b.cyl((13.0, 2.18, 15.8), (13.0, 2.34, 15.8), 0.8, 8, 'lightc', mirror=True)

    # ------------------------------------------------------------------ port emitter box (long, team roof)
    b.hull([(x, y, z) for y, xs, zs in [(DECK - 0.2, (-9.7, -3.6), (-15.5, 19.3)), (5.9, (-9.3, -4.0), (-11.1, 14.3))]
            for x in xs for z in zs], 'paint', bevel=0.14)
    b.hull([(x, y, z) for y in (5.96, 6.12) for x in (-9.0, -4.3) for z in (-10.8, 14.0)], 'team', bevel=0.03)
    # ------------------------------------------------------------------ starboard fork channel (dark, stays low)
    b.box((1.2, DECK - 0.2, -3.6), (7.9, 3.62, 22.0), 'black', bevel=0.0)
    for z in (-1.0, 6.0, 13.0, 21.0):
        b.box((1.0, 3.5, z), (8.1, 3.72, z + 1.0), 'dark', bevel=0.0)
    b.box((8.4, 3.3, -2.0), (10.6, 3.66, 22.0), 'paint2', bevel=0.05)
    b.box((10.3, 3.5, 4.0), (10.7, 3.82, 12.0), 'lightc', bevel=0.0)

    # ------------------------------------------------------------------ superstructure: aft bridge + starboard spine
    b.hull([(x, y, z) for x, z in [(-10.0, -26.6), (10.0, -26.6), (10.0, -21.8), (-10.0, -21.8)] for y in (DECK - 0.2, 6.5)],
           'paint2', bevel=0.14)
    b.hull([(x, y, z) for x, z in [(-5.1, -27.0), (2.0, -27.0), (2.0, -21.6), (-5.1, -21.6)] for y in (6.2, 9.5)],
           'paint', bevel=0.14)
    b.box((-4.2, 8.6, -21.7), (1.2, 9.2, -21.45), 'lightw', bevel=0.0)
    for x in (-3.8, -1.0):
        b.box((x, 9.46, -26.0), (x + 2.0, 9.68, -22.6), 'black', bevel=0.0)
    # spine: wide base then a roofed armoured ridge to the fork hub
    b.hull([(x, y, z) for x, z in [(-1.2, -21.8), (10.0, -21.8), (10.0, -4.0), (-1.2, -4.0)] for y in (DECK - 0.2, 6.5)],
           'paint2', bevel=0.14)
    b.hull([(x, 6.4, z) for x, z in [(-0.2, -26.6), (9.2, -26.6), (9.2, -3.6), (-0.2, -3.6)]] +
           [(x, 10.5, z) for x, z in [(1.6, -26.6), (7.2, -26.6), (7.2, -4.4), (1.6, -4.4)]], 'paint', bevel=0.16)
    b.hull([(x, y, z) for y in (10.56, 10.72) for x in (1.9, 6.9) for z in (-25.6, -5.2)], 'team', bevel=0.03)
    b.cyl((4.54, 7.98, -4.6), (4.54, 7.98, -3.4), 2.9, 12, 'dark', bevel=0.05)
    b.box((-1.3, 4.6, -14.0), (-1.0, 5.4, -8.0), 'lightc', bevel=0.0)
    # stern: red light, deck vents
    b.box((-2.2, 1.6, -34.9), (2.2, 2.3, -34.6), 'lightr', bevel=0.0)
    b.box((-8.0, 3.3, -33.0), (8.0, 3.58, -28.4), 'dark', bevel=0.04)
    for x in (-6.5, -3.0, 0.5, 4.0):
        b.box((x, 3.5, -32.2), (x + 2.2, 3.7, -29.2), 'black', bevel=0.0)
    # bow: anchor plate
    b.hull([(x * s, 3.46, z) for s in (-1, 1) for x, z in [(0.8, 28.0), (3.8, 27.0), (3.8, 22.0), (0.8, 22.0)]] +
           [(x * s, 3.62, z) for s in (-1, 1) for x, z in [(0.8, 28.0), (3.8, 27.0), (3.8, 22.0), (0.8, 22.0)]], 'dark', bevel=0.03)

    # ------------------------------------------------------------------ fork: hub + two thick tines (spin z)
    f = k.piece('fork'); F = f.at
    f.cyl(F(0, 0, 0.1), F(0, 0, 3.4), 1.8, 10, 'dark', bevel=0.06)
    for s in (-1, 1):
        f.hull([F(x, s * y, z) for x in (-1.0, 1.0) for y, z in [(0.2, 2.6), (2.0, 2.6), (2.0, 4.8), (3.8, 7.3), (2.1, 7.8), (0.2, 5.3)]],
               'steel', bevel=0.06)
        f.hull([F(x, s * y, z) for x in (-1.25, 1.25) for y, z in [(3.8, 7.3), (2.1, 7.8), (3.8, 25.1), (2.1, 27.3)]],
               'steel', bevel=0.08)
        f.hull([F(x, s * y, z) for x in (-1.3, 1.3) for y, z in [(3.86, 23.0), (2.04, 24.2), (3.86, 25.0), (2.04, 26.2)]],
               'lightc', bevel=0.0)
