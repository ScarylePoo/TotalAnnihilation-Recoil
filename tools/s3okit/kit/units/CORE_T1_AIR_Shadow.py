"""Shadow (CORE_T1_AIR_Shadow) - Core T1 bomber. Long heavy fuselage with a pointed glazed nose, two big engine
nacelles on the rear wing roots with tall fins on top, and the largest Core T1 wing: the inner wing reaches the
hinge at x +-14 and the huge tip panels (winga/wingb, 27 x 18.7 elmo) stand up when landed and fold out 90 deg in
flight (COB Go/Stop), making a broad 65-elmo trapezoid with a deep, less swept inner wing - wide and blunt where the Avenger is a narrow
arrow.
A dark bomb bay runs along the belly between the nacelles (bombay = drop point).
Pieces (TA layout): base, bombay (empty), winga/wingb (tip panels; winga = mirrored clone of wingb),
thrusta1/thrusta2/thrustb (empty engine emit points).
Value groups from above: dark warm armour, two big light steel engine nacelles (the bomber's twin light bars),
darker paint2 fins, dark intakes and nozzles,
an ochre hazard band across the nose, team on the inner (flight-top) face of the tip panels plus a broad spine plate.
Coordinates are ENGINE/global: X right, Y up, Z forward. mirror=True builds the -X twin sharing UVs."""
import math

UNIT = dict(
    res=1024,
    wreck=dict(seed=25, drop=['winga'], pose={'wingb': (0, 0, -55)}),
    preview_pose={'winga': (0, 0, 90.0), 'wingb': (0, 0, -90.0)},   # flight: tip panels folded out
)

WY = 3.0


def build(k):
    b = k.piece('base')
    # ------------------------------------------------------------------ fuselage (crosses x = 0)
    b.hull([(x * sx, y, z) for sx in (-1, 1) for x, y, z in
            [(0.4, 3.0, 28.0), (0.4, 2.4, 27.2), (2.2, 1.6, 23.0), (2.2, 5.6, 22.0),
             (4.6, 1.2, 14.0), (4.0, 8.0, 12.0), (5.2, 1.2, -14.0), (4.0, 9.0, -14.0),
             (3.4, 1.6, -22.0), (2.2, 6.4, -22.0)]], 'paint', bevel=0.2, seg=2)
    # glazed bomb-aimer nose
    b.hull([(x * sx, y, z) for sx in (-1, 1) for x, y, z in
            [(1.2, 2.6, 27.0), (2.4, 4.4, 22.4), (1.8, 5.8, 21.0), (2.0, 2.0, 24.4)]] +
           [(x * sx, y + 0.12, z + 0.12) for sx in (-1, 1) for x, y, z in [(1.2, 2.6, 27.0), (2.4, 4.4, 22.4), (1.8, 5.8, 21.0)]],
           'glass', bevel=0.05)
    # cockpit
    b.hull([(x * sx, y, z) for sx in (-1, 1) for x, y, z in
            [(2.0, 7.4, 15.4), (2.6, 8.2, 11.4), (1.2, 9.4, 12.2), (1.2, 9.4, 9.6), (2.6, 8.6, 8.0)]], 'glass', bevel=0.07)
    # ochre hazard band across the nose
    b.hull([(x * sx, y, z) for sx in (-1, 1) for x, y, z in
            [(2.6, 5.4, 20.4), (2.0, 6.0, 20.4), (3.3, 6.5, 17.6), (2.6, 7.2, 17.6)]] +
           [(x * sx, y + 0.12, z) for sx in (-1, 1) for x, y, z in [(2.6, 5.4, 20.4), (3.3, 6.5, 17.6), (2.0, 6.0, 20.4), (2.6, 7.2, 17.6)]],
           'hazard', bevel=0.02)
    # team spine plate
    b.hull([(x * sx, y, z) for sx in (-1, 1) for x, y, z in
            [(2.4, 9.02, 4.0), (2.4, 9.02, -12.0), (2.4, 9.2, 4.0), (2.4, 9.2, -12.0)]], 'team', bevel=0.03)
    b.box((-1.0, 8.9, 6.0), (1.0, 9.6, 7.4), 'dark', bevel=0.04)
    b.cyl((0, 9.6, 6.7), (0, 9.9, 6.7), 0.4, 8, 'lightr')
    # bomb bay along the belly
    b.box((-3.0, 0.7, -14.0), (3.0, 1.3, 6.0), 'black', bevel=0.06)
    for z in (-12.0, -6.0, 0.0):
        b.box((-3.2, 0.5, z), (3.2, 0.9, z + 0.8), 'dark', bevel=0.0)

    # ------------------------------------------------------------------ broad inner wing (mirrored)
    pts = []
    for x, zl, zt, t in ((4.4, 17.0, -24.4, 0.9), (14.0, 8.0, -24.6, 0.55)):
        for z, tt in ((zl, 0.12), (zl - 2.0, t), (zt + 1.2, t * 0.8), (zt, 0.1)):
            pts += [(x, WY + tt, z), (x, WY - tt, z)]
    b.hull(pts, 'paint', bevel=0.08, mirror=True)
    b.hull([(x, WY + d, z) for x in (12.8, 14.0) for z in (-0.4, -24.2) for d in (0.5, 0.62)], 'paint2', bevel=0.0, mirror=True)

    # ------------------------------------------------------------------ engine nacelles with tall fins (mirrored)
    b.hull([(x, y, z) for x, y, z in
            [(6.2, 1.6, -3.0), (12.0, 1.6, -5.0), (6.2, 7.0, -4.0), (11.6, 6.8, -6.0), (9.0, 7.6, -5.0),
             (6.2, 1.6, -24.6), (12.2, 1.6, -25.2), (6.2, 7.0, -23.6), (11.6, 7.0, -24.0), (9.0, 7.8, -24.0)]],
           'steel', bevel=0.18, mirror=True)
    b.hull([(x, y, z) for x, y, z in [(7.6, 7.3, -8.0), (10.6, 7.2, -8.0), (7.6, 7.3, -15.0), (10.6, 7.2, -15.0)]] +
           [(x, y + 0.14, z) for x, y, z in [(7.6, 7.3, -8.0), (10.6, 7.2, -8.0), (7.6, 7.3, -15.0), (10.6, 7.2, -15.0)]],
           'dark', bevel=0.0, mirror=True)     # dark access panel on the nacelle top
    b.cyl((9.1, 4.3, -2.6), (9.1, 4.3, -5.0), 2.4, 14, 'dark', r2=2.6, bevel=0.06, mirror=True)
    b.cyl((9.1, 4.3, -2.55), (9.1, 4.3, -2.7), 1.7, 14, 'black', mirror=True)
    b.cyl((9.1, 4.3, -24.0), (9.1, 4.3, -26.6), 2.4, 14, 'dark', r2=2.0, bevel=0.05, mirror=True)
    b.cyl((9.1, 4.3, -26.55), (9.1, 4.3, -26.7), 1.4, 14, 'lightr', mirror=True)
    b.hull([(8.7, 7.4, -16.0), (8.7, 7.4, -25.0), (8.9, 15.8, -22.2), (8.9, 15.8, -27.6),
            (9.7, 7.4, -16.0), (9.7, 7.4, -25.0), (9.5, 15.8, -22.2), (9.5, 15.8, -27.6)], 'paint2', bevel=0.08, mirror=True)
    b.box((8.75, 15.6, -27.4), (9.65, 16.1, -26.4), 'lightr', bevel=0.0, mirror=True)
    # centre tail cone
    b.cyl((0, 4.0, -21.8), (0, 4.0, -24.0), 1.6, 10, 'dark', r2=1.2, bevel=0.03)
    b.cyl((0, 4.0, -23.95), (0, 4.0, -24.1), 0.9, 10, 'lightr')

    # ------------------------------------------------------------------ tip panel (wingb at +x; winga = mirror)
    w = k.piece('wingb'); W = w.at
    out = [(0.0, 12.5), (0.0, -11.7), (18.7, -14.5), (17.7, -3.5)]
    w.hull([W(x, y, z) for y, z in out for x in (-0.9, -0.05)], 'paint2', bevel=0.08)   # outer face = underside in flight
    w.hull([W(x, y, z) for y, z in [(1.6, 9.6), (1.6, -10.4), (16.6, -12.8), (16.0, -4.4)] for x in (-1.0, -0.84)], 'team', bevel=0.03)
    w.hull([W(x, y, z) for y, z in [(0.6, -10.6), (0.6, -11.6), (18.4, -14.4), (18.4, -13.2)] for x in (-0.98, -0.86)], 'dark', bevel=0.0)
    w.cyl(W(-0.5, 18.4, -3.0), W(-0.5, 18.4, -14.6), 0.6, 8, 'dark', r2=0.45)
    w.cyl(W(-0.5, 18.4, -2.5), W(-0.5, 18.4, -3.02), 0.38, 8, 'lightw', r2=0.6)
    w.cyl(W(-0.5, -0.4, -11.4), W(-0.5, -0.4, 12.0), 0.7, 8, 'dark')          # hinge barrel
    k.clone('winga', 'wingb', mirror_x=True)
