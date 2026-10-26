"""Lancet (ARM_T2_AIR_Lancet) - Arm T2 torpedo bomber. A long flat diamond lifting body (35 elmo across at the waist)
with a needle nose, a narrow raised spine and canopy, and two heavy dark torpedoes with hazard-yellow warheads
recessed along its flanks - the torpedo bomber's mark from above. On take-off the COB slides the wings (wing1/wing2)
out AND 13 elmo back (move x, z), so they reappear as a second, swept delta behind the body: a double-delta arrow.
The twin canted fins (tail1/tail2) slide apart 5 elmo at the same time (move x).
Pieces (TA layout): base (bombdrop/thrust empty), wing1/wing2 (sliding wings; wing1 = mirrored clone of wing2),
tail1/tail2 (sliding fins; tail1 = mirrored clone of tail2).
Value groups from above: light Arm body and wings, dark paint2 spine and engine block, near-black torpedoes and
intakes, team chevron bands along the body's leading edges + outer wing panels + fins.
Coordinates are ENGINE/global: X right, Y up, Z forward. mirror=True builds the -X twin sharing UVs."""
import math

BODY = [(0.0, 1.4, 33.6), (0.0, 2.8, 33.4), (4.2, 0.4, 22.5), (4.2, 4.0, 22.5),
        (17.6, 1.6, -1.0), (17.6, 2.6, -1.0), (8.0, 0.4, -12.5), (8.0, 4.0, -12.5),
        (0.0, 0.4, -12.5), (0.0, 4.2, -12.5), (0.0, 0.2, 22.0), (0.0, 4.4, 22.0)]


def top_y(pts, x, z):
    """height of the convex hull of pts above (x, z) (for decals that must sit just above a hull's top)."""
    from scipy.spatial import ConvexHull
    h = ConvexHull(pts)
    return min(-(a * x + c * z + d) / b for a, b, c, d in h.equations if b > 1e-6)

UNIT = dict(
    res=1024,
    wreck=dict(seed=43, remove=['wing1'], drop=['tail2']),
    always_visible=['wing1', 'wing2'],
    # flight pose: wings out and back, fins apart (engine x = -COB x)
    preview_pose={'wing1': {'move': (-6.5, 0, -12.75)}, 'wing2': {'move': (6.75, 0, -13.0)},
                  'tail1': {'move': (-4.625, 0, 0)}, 'tail2': {'move': (5.0, 0, 0)}},
)


def build(k):
    b = k.piece('base')
    # ------------------------------------------------------------------ diamond lifting body (mirrored halves)
    b.hull(BODY, 'paint', bevel=0.14, mirror=True)
    # tail boom
    b.hull([(x * sx, y, z) for sx in (-1, 1) for x, y, z in
            [(4.0, 0.6, -10.0), (4.0, 4.0, -10.0), (2.0, 1.0, -21.0), (2.0, 4.0, -21.0)]], 'paint', bevel=0.14)
    # raised spine + canopy (dark paint2 spine: a narrow dark line through the light diamond)
    b.hull([(x * sx, y, z) for sx in (-1, 1) for x, y, z in
            [(3.0, 4.0, 22.0), (3.2, 6.4, 18.0), (3.0, 6.6, -3.0), (1.4, 6.0, -16.4), (1.8, 4.0, -18.0), (3.6, 4.0, -3.0)]],
           'paint2', bevel=0.14)
    b.hull([(x * sx, y, z) for sx in (-1, 1) for x, y, z in
            [(1.4, 4.4, 27.0), (2.8, 6.4, 21.0), (2.4, 7.4, 13.0), (1.0, 8.0, 15.6), (1.0, 7.9, 12.6), (2.0, 5.2, 25.0)]],
           'glass', bevel=0.08)
    b.cyl((0, 2.1, 33.4), (0, 2.1, 36.2), 0.4, 8, 'dark', r2=0.14)
    # team chevron bands along the body's leading edges
    b.hull([(x, top_y(BODY, x, z) + d, z) for x, z in ((5.0, 20.6), (15.6, 1.4), (13.0, 0.6), (4.6, 16.6))
            for d in (0.07, 0.17)], 'team', bevel=0.02, mirror=True)
    # intakes beside the spine
    b.hull([(3.4, 4.0, 4.0), (6.4, 3.6, 3.0), (3.4, 5.8, 3.0), (6.0, 4.8, 2.0),
            (3.4, 4.0, -10.0), (6.4, 3.6, -10.0), (3.4, 5.4, -10.0), (6.0, 4.6, -10.0)], 'paint2', bevel=0.12, mirror=True)
    b.hull([(3.6, 4.1, 4.1), (6.2, 3.7, 3.1), (3.6, 5.6, 3.1), (5.9, 4.7, 2.1),
            (3.6, 4.1, 3.8), (6.2, 3.7, 2.8), (3.6, 5.6, 2.8), (5.9, 4.7, 1.8)], 'black', bevel=0.0, mirror=True)
    # flank torpedoes, recessed into the body sides (dark bodies, hazard warheads, dark fins)
    tx, ty = 8.4, 3.6
    b.cyl((tx, ty, -6.0), (tx, ty, 11.0), 1.5, 12, 'dark', bevel=0.04, mirror=True)
    b.cyl((tx, ty, 11.0), (tx, ty, 14.4), 1.5, 12, 'hazard', r2=0.6, bevel=0.03, mirror=True)
    b.cyl((tx, ty, -6.0), (tx, ty, -8.0), 1.5, 12, 'dark', r2=0.7, mirror=True)
    b.box((tx - 2.0, ty - 0.08, -8.2), (tx + 2.0, ty + 0.08, -6.6), 'dark', bevel=0.0, mirror=True)
    b.box((tx - 0.08, ty - 1.4, -8.2), (tx + 0.08, ty + 2.0, -6.6), 'dark', bevel=0.0, mirror=True)
    # engine block + nozzle at the boom end (thrust emit 0, 2.5, -12.7 .. -25.8)
    b.hull([(x * sx, y, z) for sx in (-1, 1) for x, y, z in
            [(3.0, 0.8, -14.0), (3.0, 5.0, -14.0), (3.0, 0.8, -22.0), (3.0, 5.0, -22.0), (1.8, 5.8, -16.0)]],
           'paint2', bevel=0.18)
    b.cyl((0, 2.8, -21.8), (0, 2.8, -24.0), 2.3, 12, 'dark', r2=2.0, bevel=0.04)
    b.cyl((0, 2.8, -23.95), (0, 2.8, -24.1), 1.5, 12, 'lightc')
    # wing-tip lights on the diamond, belly torpedo bay (bombdrop 0, 0, 2.5)
    b.box((17.2, 1.6, -1.6), (17.9, 2.6, -0.4), 'lightw', bevel=0.0, mirror=True)
    b.box((-2.6, 0.05, -6.0), (2.6, 0.4, 10.0), 'black', bevel=0.04)

    # ------------------------------------------------------------------ wing2 (origin 4.75, 0.25, 8.25; slides out/back)
    w = k.piece('wing2'); W = w.at
    pl = [(1.0, 4.6), (4.7, 5.7), (17.4, -16.6), (17.4, -18.4), (6.0, -15.2), (1.0, -10.0)]
    w.hull([W(x, y, z) for x, z in pl for y in ((1.3, 2.8) if x < 6 else (1.75, 2.45))], 'paint', bevel=0.06)
    w.hull([W(x, y, z) for x, z, t in ((6.2, 2.4, 2.8), (16.6, -15.8, 2.46), (16.6, -17.6, 2.46), (8.0, -15.0, 2.6),
                                        (5.4, -10.4, 2.8)) for y in (t + 0.04, t + 0.14)], 'team', bevel=0.02)
    w.hull([W(x, y, z) for x, z in ((1.4, -9.0), (5.4, -13.4), (5.6, -14.6), (1.4, -10.6)) for y in (2.8, 2.9)],
           'paint2', bevel=0.0)
    w.cyl(W(17.4, 2.1, -10.0), W(17.4, 2.1, -19.6), 0.6, 8, 'dark', r2=0.45)
    w.cyl(W(17.4, 2.1, -9.5), W(17.4, 2.1, -10.02), 0.38, 8, 'lightw', r2=0.6)
    k.clone('wing1', 'wing2', mirror_x=True)

    # ------------------------------------------------------------------ tail2 (origin 1.25, 0.25, -12.5; slides +5)
    t = k.piece('tail2'); T = t.at
    t.hull([T(x, y, z) for x, y, z in
            [(-0.4, 3.8, -6.0), (-0.4, 3.0, -19.0), (0.6, 3.8, -6.0), (0.6, 3.0, -19.0),
             (3.5, 10.2, -17.5), (3.7, 10.2, -21.5), (4.3, 10.2, -17.5), (4.5, 10.2, -21.5)]], 'paint', bevel=0.07)
    t.hull([T(x, y, z) for x, y, z in [(2.7, 8.4, -15.8), (3.5, 10.2, -17.5), (3.7, 10.2, -21.5), (2.8, 8.2, -20.6)]] +
           [T(x + 0.8, y - 0.3, z) for x, y, z in [(2.7, 8.4, -15.8), (3.5, 10.2, -17.5), (3.7, 10.2, -21.5), (2.8, 8.2, -20.6)]],
           'team', bevel=0.0)
    t.box(T(3.6, 10.1, -21.3), T(4.5, 10.5, -20.3), 'lightr', bevel=0.0)
    k.clone('tail1', 'tail2', mirror_x=True)
