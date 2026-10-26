"""Construction Ship (CORE_T1_SEA_Constructor) - Core naval builder. Wide dark hull; the middle of the ship is a
sloped-wall hangar whose two roof halves (door1/door2) flip right over the eaves (190 deg) onto the side decks to
open it; inside lies a folded nano crane: a turret post, a long two-pronged fork (fork pitches up 77 deg) and the
nano gun head (gun). A tall angular bridge tower at the stern and a raised ramp forecastle at the bow.
Opposite layout to the Arm builder (Arm: hangar aft + bridge forward). From above: dark hull, light steel ramp and
tower roof, wide team bands on both roof halves, ochre hazard on the fork.
Pieces (TA layout): base, door1/door2 (turn z; door2 = mirrored clone), turret (turn y), fork (turn x), gun (turn x),
beam (empty nano emit point), wake1/2 (empty). Floater, no waterline (water surface at model y = 0).
Coordinates are ENGINE/global: X right, Y up, Z forward. mirror=True builds the -X twin sharing UVs."""
import math

UNIT = dict(
    res=1024,
    always_visible=['turret', 'fork', 'gun'],      # enclosed at rest, raised by the build script
    wreck=dict(seed=5, drop=['door1'], pose={'door2': (0, 0, 120)}),
    preview_pose={},
)

DECK = 5.5
WATER = [(0.0, 40.6), (5.7, 40.1), (13.7, 29.2), (16.6, 14.3), (16.6, -15.9), (16.6, -33.2), (10.2, -39.8)]
DECKO = [(0.0, 30.6), (2.4, 30.2), (8.0, 22.6), (9.7, 11.5), (9.7, -30.0), (4.8, -35.1)]
HZ0, HZ1 = -15.9, 11.5


def ring(pts, y, sx=1.0, sz=1.0, dz=0.0):
    return [(x * sx * s, y, z * sz + dz) for x, z in pts for s in ((-1, 1) if x > 0 else (1,))]


def build(k):
    b = k.piece('base')
    # ------------------------------------------------------------------ hull: wide flared, dark
    # built in three lengthwise segments: hull-length chamfer strips pack badly (long diagonal UV slivers)
    def cut(pts, z0, z1):
        P = sorted({z: x for x, z in pts}.items())          # (z, x) ascending z, half-width outline
        zs = [z for z, _ in P]; xs = [x for _, x in P]
        def xat(z):
            for i in range(len(zs) - 1):
                if zs[i] <= z <= zs[i + 1]:
                    t = (z - zs[i]) / (zs[i + 1] - zs[i]); return xs[i] + t * (xs[i + 1] - xs[i])
            return xs[0] if z < zs[0] else xs[-1]
        lo, hi = max(z0, zs[0]), min(z1, zs[-1])
        return [(xat(z), z) for z in sorted({lo, hi} | {z for z in zs if lo < z < hi})]
    for z0, z1 in ((11.5, 41.0), (-15.9, 11.5), (-41.0, -15.9)):
        w, d = cut(WATER, z0, z1), cut(DECKO, z0, z1)
        k_ = [(x * 0.6, z * 0.85 - 1.0 if z > 0 else z * 0.85 + 1.0) for x, z in w]
        b.hull(ring(k_, -2.2) + ring(w, 0.0), 'paint2', bevel=0.2)
        b.hull(ring(w, 0.0) + ring(d, DECK), 'paint', bevel=0.22)
    # side decks outboard of the hangar: darker strips (the flipped roof halves land here)
    b.box((9.4, DECK - 0.1, -14.8), (14.6, DECK + 0.25, 10.4), 'paint2', bevel=0.06, mirror=True)
    # bulwark rails at the side-deck edges
    b.box((13.6, DECK + 0.2, -14.0), (14.0, DECK + 1.0, 9.6), 'dark', bevel=0.04, mirror=True)
    # ------------------------------------------------------------------ hangar: sloped side walls + gable ends (open top)
    for s in (1,):
        b.hull([(x, y, z) for z in (HZ0, HZ1) for x, y in ((9.7, DECK), (6.5, 11.72), (5.7, 11.72), (8.8, DECK))],
               'paint', bevel=0.12, mirror=True)
    for z0, z1 in ((HZ0 - 0.9, HZ0), (HZ1, HZ1 + 0.9)):
        b.hull([(x, y, z) for z in (z0, z1) for x, y in
                ((-9.7, DECK), (9.7, DECK), (-6.5, 11.72), (6.5, 11.72), (0.0, 13.5))], 'paint', bevel=0.12)
    b.box((-8.8, DECK - 0.2, HZ0), (8.8, DECK + 0.05, HZ1), 'black', bevel=0.0)
    b.box((9.0, 7.4, HZ1 + 0.85), (9.3, 8.0, HZ1 + 1.0), 'lightw', bevel=0.0, mirror=True)
    # ------------------------------------------------------------------ bow: raised ramp forecastle (light steel top)
    b.hull([(x * s, y, z) for s in (-1, 1) for x, y, z in
            [(3.8, DECK, 11.5), (1.2, DECK, 26.6), (3.8, 8.8, 11.5), (1.2, 8.8, 26.6)]], 'paint', bevel=0.16)
    b.hull([(x * s, y, z) for s in (-1, 1) for x, y, z in
            [(3.2, 8.75, 12.4), (1.0, 8.75, 25.0), (3.1, 8.95, 12.5), (0.95, 8.95, 24.9)]], 'steel', bevel=0.03)
    b.hull([(x, y, z) for x, y, z in
            [(4.0, DECK, 12.0), (7.2, DECK, 12.0), (4.0, DECK, 22.4), (6.0, DECK, 22.4),
             (4.4, 7.2, 12.4), (5.6, 7.4, 12.4), (4.4, 7.2, 20.4), (4.9, 7.4, 20.4)]], 'dark', bevel=0.1, mirror=True)
    b.cyl((0, 8.9, 25.4), (0, 9.4, 25.4), 0.35, 6, 'lightr')
    # ------------------------------------------------------------------ stern bridge tower (tall, angular)
    b.hull([(x * s, y, z) for s in (-1, 1) for x, y, z in
            [(5.0, DECK, -15.9), (2.6, DECK, -28.8), (5.0, 16.2, -16.6), (2.8, 16.2, -27.0)]], 'paint', bevel=0.18)
    b.hull([(x * s, y, z) for s in (-1, 1) for x, y, z in
            [(4.4, 16.15, -17.2), (2.5, 16.15, -26.4), (4.3, 16.35, -17.3), (2.45, 16.35, -26.3)]], 'steel', bevel=0.03)
    b.hull([(x * s, y, z) for s in (-1, 1) for x, y, z in
            [(4.9, 13.2, -16.55), (4.9, 15.4, -16.6), (4.8, 13.2, -16.35), (4.8, 15.4, -16.4)]], 'lightc', bevel=0.0)
    # wide aft deckhouse the tower stands on
    b.hull([(x * s, y, z) for s in (-1, 1) for x, y, z in
            [(6.2, DECK, -21.2), (8.8, DECK, -24.4), (5.0, DECK, -32.5),
             (6.2, 13.8, -21.2), (8.8, 13.8, -24.4), (5.0, 13.8, -32.5)]], 'paint2', bevel=0.16)
    b.cyl((-2.0, 16.3, -22.0), (-2.0, 21.4, -22.2), 0.35, 8, 'dark', r2=0.22)
    b.box((-4.4, 19.6, -22.5), (0.4, 20.1, -21.8), 'steel', bevel=0.04)
    b.cyl((-2.0, 21.4, -22.2), (-2.0, 21.7, -22.2), 0.26, 6, 'lightr')
    b.box((-1.4, 4.2, -35.4), (1.4, 5.0, -35.1), 'lightr', bevel=0.0)

    # ------------------------------------------------------------------ roof halves (door1 origin -6.52, 11.72, -2.47)
    d = k.piece('door1'); D = d.at
    d.hull([D(x, y, z) for z in (-13.45, 14.0) for x, y in ((-0.15, -0.55), (-0.15, 0.25), (6.55, 2.05), (6.55, 1.2))],
           'paint', bevel=0.12)
    d.hull([D(x, y + 0.06, z) for z in (-11.6, 12.2) for x, y in ((1.2, 0.55), (5.0, 1.57))] +
           [D(x, y + 0.24, z) for z in (-11.6, 12.2) for x, y in ((1.2, 0.55), (5.0, 1.57))], 'team', bevel=0.03)
    k.clone('door2', 'door1', mirror_x=True)

    # ------------------------------------------------------------------ crane post (turret origin 0, 5.5, 4.5)
    t = k.piece('turret'); T = t.at
    t.cyl(T(0, 0, 0), T(0, 0.6, 0), 4.0, 12, 'dark', bevel=0.04)
    for s in (-1, 1):
        t.hull([T(x * s, y, z) for x, y, z in
                [(2.0, 0.5, -2.9), (4.5, 0.5, -2.9), (2.0, 0.5, 3.2), (4.5, 0.5, 3.2),
                 (2.0, 5.0, -2.3), (3.5, 5.0, -2.3), (2.0, 5.0, 2.5), (3.5, 5.0, 2.5)]], 'paint', bevel=0.12)
    t.box(T(-2.0, 0.5, -2.7), T(2.0, 2.0, 3.0), 'paint2', bevel=0.1)
    # fork (origin 0, 9.0, 4.5): trunnion + two prongs reaching aft, ochre hazard
    f = k.piece('fork'); F = f.at
    f.cyl(F(-2.0, 0, 2.6), F(2.0, 0, 2.6), 1.1, 10, 'dark')
    for s in (1,):
        f.hull([F(x, y, z) for x, y, z in
                [(0.2, -0.9, 0.4), (1.9, -0.9, 0.4), (3.6, -0.9, -8.9), (5.3, -0.9, -8.9),
                 (0.2, 1.0, 0.4), (1.9, 1.0, 0.4), (3.6, 1.0, -8.9), (5.3, 1.0, -8.9)]], 'hazard', bevel=0.1, mirror=True)
        f.box(F(3.5, -0.9, -14.6), F(5.3, 1.0, -8.6), 'steel', bevel=0.1, mirror=True)
    # gun = nano head (origin 0, 9.12, -12.12): between the prong tips, emitter dish pointing at beam
    g = k.piece('gun'); G = g.at
    g.cyl(G(-3.4, 0, 0), G(3.4, 0, 0), 0.9, 10, 'dark')
    g.hull([G(x * s, y, z) for s in (-1, 1) for x, y, z in
            [(3.0, -3.4, -3.2), (3.0, 2.2, -3.2), (2.2, -2.6, 0.4), (2.2, 2.6, 0.4), (2.4, -0.6, 3.0)]], 'steel', bevel=0.14)
    g.cyl(G(0, -0.2, 2.0), G(0, -0.3, 9.4), 0.9, 8, 'dark', r2=0.55)
    g.cyl(G(0, -0.3, 9.4), G(0, -0.3, 10.2), 1.25, 10, 'dark', bevel=0.03)
    g.cyl(G(0, -0.3, 10.15), G(0, -0.3, 10.3), 0.8, 10, 'lightc')
