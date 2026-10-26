"""Construction Aircraft (ARM_T1_AIR_Constructor) - Arm T1 air builder. A stubby, boxy flying van: square fuselage
with a blunt glazed nose, a hazard-striped nano projector on the left cheek (the build beam starts at the base's
first vertex, the front-left corner, as in TA), a dorsal equipment deck and a wide V-tail. The short wings are stowed
under the belly and slide out sideways on take-off (COB move x), so the flying plan is a short fat cross.
The TA model's body is centred at x -4; the new body is centred at x 0 so it mirrors, and the two wings are built
separately (wing1 extends 2.7 elmo inboard of its origin) so that both slide out to the same span either side
(flight roots at +-8, tips at +-22).
Pieces (TA layout): base, wing1 (+x side, slides +11.25), wing2 (-x side, slides -14.6), rearthrust (empty).
Value groups from above: light Arm hull and wings, dark paint2 equipment deck and wing roots, near-black vents,
team on the tail fins, the deck centre and the wing tips; yellow hazard on the nano projector.
Coordinates are ENGINE/global: X right, Y up, Z forward. mirror=True builds the -X twin sharing UVs."""
import math

UNIT = dict(
    res=1024,
    wreck=dict(seed=14, remove=['wing1']),
    preview_pose={'wing1': {'move': (11.25, 0, 0)}, 'wing2': {'move': (-14.625, 0, 0)}},
)


def wing(k, name, x_in, x_out, yc):
    """flat stub wing between local x_in and x_out (sign gives the side), team tip, dark root. yc = local mid-plane
    height: the two wings overlap under the belly when stowed, so they sit at different heights."""
    w = k.piece(name)

    def W(x, y, z):
        return w.at(x, y + yc, z)
    s = 1 if x_out > x_in else -1
    pts = []
    for x, zl, zt, t in ((x_in, 9.0, -9.6, 0.34), (x_out, 3.4, -8.4, 0.22)):
        for z, tt in ((zl, 0.12), (zl - 1.6, t), (zt + 1.0, t * 0.8), (zt, 0.08)):
            pts += [W(x, tt, z), W(x, -tt, z)]
    w.hull(pts, 'paint', bevel=0.05)
    xt = x_out - s * 4.6
    w.hull([W(x, dy, z) for x in (xt, x_out - s * 0.5) for dy in (0.26, 0.34) for z in (2.4, -7.6)], 'team', bevel=0.02)
    xr = x_in + s * 2.8
    w.hull([W(x, dy, z) for x in (x_in + s * 0.4, xr) for dy in (0.36, 0.44) for z in (7.0, -8.6)], 'paint2', bevel=0.02)
    w.cyl(W(x_out, 0, 2.6), W(x_out, 0, -8.6), 0.5, 8, 'dark', r2=0.4)
    w.cyl(W(x_out, 0, 3.0), W(x_out, 0, 2.58), 0.3, 8, 'lightw', r2=0.5)


def build(k):
    b = k.piece('base')
    # ------------------------------------------------------------------ box fuselage (crosses x = 0)
    b.hull([(x * sx, y, z) for sx in (-1, 1) for x, y, z in
            [(6.6, 1.4, 15.4), (7.6, 1.6, 9.0), (7.8, 1.6, -12.0), (5.6, 3.0, -22.0),
             (6.2, 9.4, 15.0), (7.4, 10.4, 9.0), (7.4, 10.6, -12.0), (5.2, 9.8, -22.0),
             (4.4, 3.2, 21.0), (4.2, 7.6, 20.4)]], 'paint', bevel=0.2, seg=2)
    # blunt glazed nose
    b.hull([(x * sx, y, z) for sx in (-1, 1) for x, y, z in
            [(2.8, 7.6, 20.1), (3.6, 9.4, 16.6), (2.6, 10.3, 14.4)]] +
           [(x * sx, y + 0.14, z + 0.12) for sx in (-1, 1) for x, y, z in
            [(2.8, 7.6, 20.1), (3.6, 9.4, 16.6), (2.6, 10.3, 14.4)]], 'glass', bevel=0.05)
    # yellow hazard band across the nose: construction unit tell
    b.hull([(x * sx, y, z) for sx in (-1, 1) for x, y, z in
            [(4.4, 6.9, 20.6), (5.0, 8.4, 19.0)]] +
           [(x * sx, y + 0.14, z + 0.12) for sx in (-1, 1) for x, y, z in
            [(4.4, 6.9, 20.6), (5.0, 8.4, 19.0)]], 'hazard', bevel=0.02)
    b.box((-2.2, 2.6, 21.0), (2.2, 3.4, 21.3), 'lightw', bevel=0.0)
    # dorsal equipment deck: dark raised block with team centre panel and vents
    b.hull([(x * sx, y, z) for sx in (-1, 1) for x, y, z in
            [(5.8, 10.4, 10.0), (5.8, 10.4, -14.0), (5.0, 12.6, 8.6), (5.0, 12.6, -13.0)]], 'paint2', bevel=0.14)
    b.hull([(x * sx, y, z) for sx in (-1, 1) for x, y, z in
            [(4.2, 12.58, 7.6), (4.2, 12.58, -4.4), (4.2, 12.74, 7.6), (4.2, 12.74, -4.4)]], 'team', bevel=0.03)
    for z in (-6.0, -8.0, -10.0):
        b.box((-4.0, 12.6, z - 0.5), (4.0, 12.75, z + 0.5), 'black', bevel=0.0)
    b.cyl((-3.6, 12.6, -12.0), (-3.6, 13.2, -12.0), 0.9, 10, 'dark', bevel=0.03)
    b.cyl((-3.6, 13.2, -12.0), (-3.6, 13.45, -12.0), 0.5, 8, 'lightw')
    # V-tail: two big canted fins with team tops
    b.hull([(2.4, 9.6, -12.0), (2.6, 9.4, -22.0), (12.4, 15.6, -19.4), (12.6, 15.6, -24.0),
            (2.0, 9.6, -12.0), (2.2, 9.4, -22.0), (12.1, 15.9, -19.4), (12.3, 15.9, -24.0)], 'paint', bevel=0.07, mirror=True)
    b.hull([(8.6, 13.24, -17.0), (8.8, 13.18, -23.0), (12.5, 15.62, -19.5), (12.6, 15.62, -23.9),
            (8.4, 13.5, -17.0), (8.6, 13.44, -23.0), (12.3, 15.92, -19.5), (12.4, 15.92, -23.9)], 'team', bevel=0.0, mirror=True)
    b.box((12.0, 15.6, -23.8), (12.9, 16.1, -23.0), 'lightr', bevel=0.0, mirror=True)
    # rear engine (rearthrust at -4, 8.2, -23.4 -> -28)
    b.hull([(x * sx, y, z) for sx in (-1, 1) for x, y, z in
            [(5.4, 3.2, -18.0), (5.4, 9.4, -18.0), (5.0, 3.6, -23.0), (5.0, 9.2, -23.0)]], 'paint2', bevel=0.12)
    for x in (-3.0, 3.0):
        b.cyl((x, 6.4, -22.6), (x, 6.4, -24.4), 1.9, 12, 'dark', r2=1.6, bevel=0.04)
        b.cyl((x, 6.4, -24.35), (x, 6.4, -24.5), 1.2, 12, 'lightc')
    # belly wing well (the wings rest here) and side intakes
    b.box((-7.0, 0.95, -10.4), (7.0, 1.5, 13.0), 'dark', bevel=0.1)
    b.box((7.4, 4.0, 4.0), (8.0, 8.4, 9.0), 'black', bevel=0.0, mirror=True)
    # nano projector on the left cheek, aimed at the build-beam origin (front-left corner)
    b.box((-8.4, 3.6, 9.4), (-7.4, 6.8, 14.6), 'dark', bevel=0.1)
    b.cyl((-8.0, 5.2, 12.0), (-10.4, 4.6, 15.0), 1.3, 10, 'hazard', r2=1.1, bevel=0.04)
    b.cyl((-10.4, 4.6, 15.0), (-11.6, 4.3, 16.5), 1.1, 10, 'dark', r2=0.7)
    b.cyl((-11.6, 4.3, 16.5), (-11.9, 4.22, 16.9), 0.65, 10, 'lightc')

    # ------------------------------------------------------------------ wings (separate geometry: different origins)
    wing(k, 'wing1', -2.7, 11.2, 0.6)      # flight: x 8.05 .. 21.95
    wing(k, 'wing2', 0.0, -14.1, -0.25)      # flight: x -7.9 .. -22.0
