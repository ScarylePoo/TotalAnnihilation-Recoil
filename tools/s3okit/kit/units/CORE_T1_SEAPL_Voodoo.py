"""Voodoo (CORE_T1_SEAPL_Voodoo) - Core T1 seaplane fighter. A long waisted needle nose in front of a broad swept body,
with two sharp canted fins. Each wing is a tall panel that stands up on the water and folds out and DOWN 112 deg in
flight (COB turn z, inverted gull), with a long gun pod on its tip: from above a short delta with a needle and two
team panels hanging either side, each edged by a light steel gun.
Pieces (TA layout): groundplane (empty), base, wake1/wake2 (empty), wing1 (-x; wing2 = mirrored clone), emitter1/2 (empty).
The panel's inner face (wing1 local +x) becomes the top in flight, so team sits on it.
Value groups from above: dark warm body, darker paint2 fins and nose saddle, steel guns, team on the wing panels and a
body chevron, warm lights.
Coordinates are ENGINE/global: X right, Y up, Z forward. mirror=True builds the -X twin sharing UVs."""
import math

UNIT = dict(
    res=1024,
    wreck=dict(seed=43, drop=['wing2'], pose={'wing1': (0, 0, 40)}),
    preview_pose={'wing1': (0, 0, 112.5), 'wing2': (0, 0, -112.5)},       # flight (COB z values negated in the engine)
)


def build(k):
    b = k.piece('base')
    # ------------------------------------------------------------------ needle nose (crosses x = 0), waist at z 3
    b.hull([(x * sx, y, z) for sx in (-1, 1) for x, y, z in
            [(0.5, 3.0, 18.2), (0.5, 3.6, 18.0), (2.9, 1.2, 10.0), (2.9, 4.8, 9.6), (1.7, 1.2, 3.0), (1.7, 4.4, 3.0)]],
           'paint', bevel=0.12)
    # team-free dark saddle on the nose so the needle reads as two tones
    b.hull([(x * sx, y, z) for sx in (-1, 1) for x, y, z in
            [(1.6, 4.3, 12.8), (2.2, 4.86, 9.6), (1.2, 4.46, 3.2), (1.6, 4.5, 12.9), (2.2, 5.06, 9.7), (1.2, 4.66, 3.3)]],
           'paint2', bevel=0.02)
    # ------------------------------------------------------------------ delta body
    b.hull([(x * sx, y, z) for sx in (-1, 1) for x, y, z in
            [(1.8, 0.8, 3.4), (1.8, 4.6, 3.4), (4.2, 0.4, -2.0), (4.2, 5.8, -3.0),
             (9.2, 2.2, -9.4), (9.2, 5.6, -9.4), (9.2, 2.2, -16.8), (9.2, 5.6, -16.8), (1.8, 0.4, -18.0), (1.8, 6.6, -17.6)]],
           'paint', bevel=0.14)
    # canopy on the shoulder
    b.hull([(x * sx, y, z) for sx in (-1, 1) for x, y, z in
            [(1.2, 4.5, 3.2), (2.8, 5.8, -3.0), (1.4, 7.8, -2.4), (0.6, 7.2, 1.2), (2.2, 6.2, -7.0), (0.8, 7.6, -7.0)]], 'glass', bevel=0.06)
    # team chevron on the body shoulders
    b.hull([(4.2, 5.86, -4.2), (8.8, 5.68, -9.2), (3.0, 6.06, -9.6), (7.8, 5.68, -13.2),
            (4.2, 6.06, -4.2), (8.8, 5.88, -9.2), (3.0, 6.26, -9.6), (7.8, 5.88, -13.2)], 'team', bevel=0.0, mirror=True)
    # engine deck
    b.hull([(x * sx, y, z) for sx in (-1, 1) for x, y, z in
            [(2.4, 6.3, -10.4), (2.4, 6.6, -17.0), (2.4, 6.9, -10.4), (2.4, 7.2, -17.0)]], 'black', bevel=0.0)
    # nozzles (wake emit points at z -16.7)
    b.cyl((4.6, 3.8, -16.8), (4.6, 3.8, -18.6), 1.9, 10, 'dark', r2=1.6, bevel=0.03, mirror=True)
    b.cyl((4.6, 3.8, -18.55), (4.6, 3.8, -18.7), 1.2, 10, 'lightr', mirror=True)
    # ------------------------------------------------------------------ sharp canted fins
    b.hull([(2.0, 6.2, -6.4), (2.2, 6.2, -17.0), (2.8, 5.4, -6.4), (3.0, 5.4, -17.0),
            (8.2, 12.4, -19.4), (8.2, 12.4, -22.4), (8.7, 12.2, -19.4), (8.7, 12.2, -22.4)], 'paint2', bevel=0.06, mirror=True)
    b.box((8.5, 3.6, -16.4), (9.5, 5.5, -3.0), 'dark', bevel=0.08, mirror=True)

    # ------------------------------------------------------------------ wing panel (wing1 at -x; wing2 = mirror)
    w = k.piece('wing1'); W = w.at
    out = [(0.0, 8.8), (0.0, -8.6), (9.8, -8.4), (9.8, 8.6)]
    w.hull([W(x, y, z) for y, z in out for x in (-0.25, 0.3)], 'paint2', bevel=0.05)
    w.hull([W(x, y, z) for y, z in ((2.6, 7.8), (2.6, -3.0), (9.0, -3.0), (9.0, 7.8)) for x in (0.34, 0.5)], 'team', bevel=0.0)
    # gun pod along the tip (emitter1 at its nose)
    w.cyl(W(-0.1, 10.2, -9.2), W(-0.1, 10.2, 6.0), 1.25, 8, 'steel', rot=math.pi / 8)
    w.cyl(W(-0.1, 10.2, 6.0), W(-0.1, 10.2, 10.2), 0.8, 8, 'steel', r2=0.55, rot=math.pi / 8)
    w.cyl(W(-0.1, 10.2, 10.15), W(-0.1, 10.2, 10.4), 0.32, 8, 'black')
    w.cyl(W(-0.1, 10.2, -9.15), W(-0.1, 10.2, -9.4), 0.7, 8, 'lightr')
    w.cyl(W(-0.1, 0.0, -8.4), W(-0.1, 0.0, 8.6), 0.7, 8, 'dark')                       # hinge barrel
    k.clone('wing2', 'wing1', mirror_x=True)
