"""Typhoon (CORE_T1_SEAPL_Typhoon) - Core T1 torpedo seaplane. A pointed hull with two heavy engine pods aft and a long
light torpedo on its back. On the water four plates lie folded over and under the hull as one flat kite; in flight they
scissor apart (COB turn y): the upper pair (wing1, hinged at the tail) swing their tips forward and out, the lower pair
(wing2, hinged at the nose) swing their tips back and out. From above: a big X with a light bar in the middle, like
nothing else in the game.
Pieces (TA layout): base, wing1L/wing1R (R at +x; L = mirrored clone), wing2L/wing2R (R = +x; L = mirrored clone),
bombdrop, RearGun, flare1/flare2 (empty).
Value groups from above: dark warm hull and upper plates, darker paint2 lower plates and pods, steel torpedo, team on
the outer ends of all four blades.
Coordinates are ENGINE/global: X right, Y up, Z forward. mirror=True builds the -X twin sharing UVs."""
import math

UNIT = dict(
    res=1024,
    wreck=dict(seed=41, remove=['wing2L'], pose={'wing1R': (0, 12, 0), 'wing1L': (0, -6, 0)}),
    preview_pose={'wing1L': (0, -22.15, 0), 'wing1R': (0, 22.15, 0),
                  'wing2L': (0, 17.23, 0), 'wing2R': (0, -17.23, 0)},    # flight (COB activatescr)
)


def build(k):
    b = k.piece('base')
    # ------------------------------------------------------------------ hull (crosses x = 0)
    b.hull([(x * sx, y, z) for sx in (-1, 1) for x, y, z in
            [(0.3, 1.2, 22.2), (0.3, 1.8, 22.0), (2.0, 0.4, 11.0), (2.0, 3.6, 9.0),
             (3.2, 0.2, -5.0), (3.2, 5.0, -6.0), (3.2, 0.2, -20.0), (2.8, 4.8, -21.0)]], 'paint', bevel=0.14)
    # canopy
    b.hull([(x * sx, y, z) for sx in (-1, 1) for x, y, z in
            [(1.0, 3.2, 11.4), (2.0, 4.5, 5.8), (1.4, 5.0, 2.4), (1.4, 3.6, 2.4), (2.0, 3.0, 7.0), (0.6, 5.8, 5.0), (0.6, 5.8, 3.0)]], 'glass', bevel=0.05)
    # ------------------------------------------------------------------ engine pods (paint2), top intakes, nozzles
    b.hull([(3.6, 1.0, -3.0), (8.0, 1.2, -3.8), (3.6, 4.6, -3.0), (8.0, 4.4, -3.8), (3.6, 1.0, -21.6), (9.2, 1.2, -21.6),
            (3.6, 5.6, -21.0), (9.2, 5.4, -21.0), (9.2, 3.6, -8.0)], 'paint2', bevel=0.14, mirror=True)
    b.hull([(4.8, 5.1, -8.0), (8.4, 5.0, -8.0), (4.8, 5.7, -18.0), (8.4, 5.6, -18.0),
            (4.8, 5.36, -8.0), (8.4, 5.26, -8.0), (4.8, 5.96, -18.0), (8.4, 5.86, -18.0)], 'dark', bevel=0.0, mirror=True)
    b.cyl((6.4, 3.3, -21.4), (6.4, 3.3, -23.4), 2.1, 12, 'dark', r2=1.8, bevel=0.04, mirror=True)
    b.cyl((6.4, 3.3, -23.35), (6.4, 3.3, -23.5), 1.3, 12, 'lightr', mirror=True)
    # ------------------------------------------------------------------ torpedo on the back: long light bar
    b.cyl((0, 6.1, -20.0), (0, 6.1, -2.0), 1.5, 8, 'steel', rot=math.pi / 8)
    b.cyl((0, 6.1, -2.0), (0, 6.1, 1.4), 1.5, 8, 'steel', r2=0.35, rot=math.pi / 8)
    b.cyl((0, 6.1, -2.5), (0, 6.1, -1.9), 1.56, 8, 'lightr', rot=math.pi / 8)
    b.box((-2.2, 7.0, -20.0), (2.2, 7.15, -18.0), 'dark', bevel=0.0)       # tail vanes
    for z in (-15.0, -6.0):
        b.box((-1.8, 4.6, z - 0.8), (1.8, 7.75, z + 0.8), 'dark', bevel=0.06)   # clamps

    # ------------------------------------------------------------------ upper blades: hinge at the tail, tips go forward
    w = k.piece('wing1R'); W = w.at
    out = [(-4.5, 1.5), (2.0, 0.0), (8.2, 15.0), (0.8, 41.0), (-0.6, 38.0)]
    w.hull([W(x, y, z) for x, z in out for y in (0.45, 1.05)], 'paint', bevel=0.05)
    w.hull([W(x, y, z) for x, z in ((4.7, 22.4), (0.9, 40.2), (-0.1, 37.8), (-2.6, 22.4)) for y in (1.1, 1.26)], 'team', bevel=0.0)
    w.hull([W(x, y, z) for x, z in ((2.2, 2.0), (7.4, 14.4), (5.8, 15.6), (0.8, 3.6)) for y in (1.1, 1.22)], 'paint2', bevel=0.0)
    k.clone('wing1L', 'wing1R', mirror_x=True)
    # ------------------------------------------------------------------ lower blades: hinge at the nose, tips go aft
    v = k.piece('wing2R'); V = v.at
    out = [(-0.5, 0.0), (1.0, 0.0), (7.7, -38.0), (7.4, -43.5), (-1.0, -43.0)]
    v.hull([V(x, y, z) for x, z in out for y in (0.0, 0.6)], 'paint2', bevel=0.04)
    v.hull([V(x, y, z) for x, z in ((6.1, -30.0), (7.1, -38.0), (6.9, -43.0), (-0.6, -42.6), (-0.6, -30.0)) for y in (0.64, 0.8)], 'team', bevel=0.0)
    k.clone('wing2L', 'wing2R', mirror_x=True)
