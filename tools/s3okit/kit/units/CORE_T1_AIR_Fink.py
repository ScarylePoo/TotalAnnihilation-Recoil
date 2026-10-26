"""Fink (CORE_T1_AIR_Fink) - Core air scout. The lightest Core plane: a thin needle fuselage with a big sensor
ball under the nose (light steel with a red eye, the scout's tell), short STRAIGHT wings (unswept - unlike the
Avenger's arrow) to the hinge at x +-12.5, and tip panels (winga/wingb) that stand up when landed and fold out
90 deg in flight, giving a long straight 48-elmo span: from above a thin plus sign. One tall dark fin at the tail.
Pieces (TA layout): base, winga/wingb (tip panels; winga = mirrored clone of wingb), thrusta1/thrusta2/thrustb
(empty engine emit points).
Value groups from above: dark warm armour, darker paint2 fin + flaps, light steel dorsal sensor pod, sensor ball and
wing-root booms, team on the inner (flight-top) face of the tip panels and a cross band over the wing roots.
Coordinates are ENGINE/global: X right, Y up, Z forward. mirror=True builds the -X twin sharing UVs."""
import math

UNIT = dict(
    res=1024,
    wreck=dict(seed=23, drop=['wingb'], pose={'winga': (0, 0, 30)}),
    preview_pose={'winga': (0, 0, 90.0), 'wingb': (0, 0, -90.0)},    # flight: tip panels folded out
)

WY = 1.3


def build(k):
    b = k.piece('base')
    # ------------------------------------------------------------------ needle fuselage (crosses x = 0)
    b.hull([(x * sx, y, z) for sx in (-1, 1) for x, y, z in
            [(0.25, 2.2, 19.4), (0.25, 1.7, 19.0), (1.2, 1.0, 14.0), (1.3, 3.6, 13.0),
             (2.6, 0.4, 3.0), (2.4, 4.6, 3.0), (2.6, 0.4, -10.0), (2.2, 4.4, -10.0),
             (1.6, 0.8, -16.6), (1.2, 3.4, -16.4)]], 'paint', bevel=0.14)
    # canopy
    b.hull([(x * sx, y, z) for sx in (-1, 1) for x, y, z in
            [(1.0, 3.4, 11.4), (1.8, 4.4, 7.4), (1.6, 4.8, 3.6), (0.6, 5.7, 6.4), (0.6, 5.6, 4.0)]], 'glass', bevel=0.07)
    # sensor ball under the nose, with a red eye
    b.cyl((0, 1.4, 12.6), (0, 0.6, 12.6), 0.9, 10, 'dark')
    b.sphere((0, 0.0, 12.8), 2.0, 'steel', segs=14, rings=8)
    b.cyl((0, 0.0, 14.6), (0, 0.0, 14.95), 1.0, 12, 'lightr', r2=0.7)
    b.cyl((0, 1.6, 10.0), (0, 1.6, 15.0), 0.22, 6, 'steel')
    # dorsal sensor pod: light steel cigar on a pylon behind the canopy (the scout's light-on-dark tell from above)
    b.box((-0.5, 4.6, -9.0), (0.5, 5.6, -2.0), 'dark', bevel=0.05)
    b.cyl((0, 6.3, 1.0), (0, 6.3, -11.6), 1.25, 12, 'steel', bevel=0.05)
    b.cyl((0, 6.3, 1.0), (0, 6.3, 2.6), 1.25, 12, 'steel', r2=0.4)
    b.cyl((0, 6.3, 2.55), (0, 6.3, 2.75), 0.45, 10, 'lightr')
    b.cyl((0, 6.3, -11.6), (0, 6.3, -12.4), 1.25, 12, 'dark', r2=0.6)
    # ------------------------------------------------------------------ straight wing (mirrored)
    pts = []
    for x, zl, zt, t in ((2.4, 3.2, -9.6, 0.5), (12.5, 1.4, -9.7, 0.38)):
        for z, tt in ((zl, 0.1), (zl - 1.4, t), (zt + 1.0, t * 0.8), (zt, 0.08)):
            pts += [(x, WY + tt, z), (x, WY - tt, z)]
    b.hull(pts, 'paint', bevel=0.06, mirror=True)
    b.hull([(x, WY + d, z) for x in (3.4, 12.0) for z in (-7.8, -9.6) for d in (0.36, 0.45)], 'paint2', bevel=0.0, mirror=True)
    # team plates across the inner wings
    b.hull([(x, WY + d, z) for x in (2.8, 10.6) for z in (-1.4, -4.8) for d in (0.44, 0.54)], 'team', bevel=0.02, mirror=True)
    # light steel boom pods at the wing hinges
    b.cyl((12.0, WY, 3.0), (12.0, WY, -12.0), 0.75, 10, 'steel', r2=0.55, rot=math.pi / 10, mirror=True)
    b.cyl((12.0, WY, 3.4), (12.0, WY, 2.98), 0.45, 10, 'lightw', r2=0.75, mirror=True)
    # ------------------------------------------------------------------ tail: single tall fin + engines
    b.hull([(x, y, z) for x in (-0.7, 0.7) for y, z in ((4.4, -9.0), (3.4, -17.4), (11.0, -13.1), (11.0, -18.4))],
           'paint2', bevel=0.08)
    b.box((-0.75, 10.4, -18.2), (0.75, 11.4, -16.6), 'lightr', bevel=0.0)
    b.hull([(2.0, 1.8, -12.0), (2.0, 1.8, -17.0), (7.6, 1.8, -16.0), (7.6, 1.8, -18.2),
            (2.0, 2.3, -12.0), (2.0, 2.3, -17.0), (7.6, 2.1, -16.0), (7.6, 2.1, -18.2)], 'paint', bevel=0.05, mirror=True)
    for x in (5.5,):
        b.cyl((x, 0.6, 0.0), (x, 0.6, -6.0), 1.2, 10, 'paint2', r2=1.0, bevel=0.04, mirror=True)   # belly lift jets
        b.cyl((x, 0.0, -2.0), (x, -0.2, -2.0), 0.85, 10, 'lightr', mirror=True)
    b.cyl((0, 2.6, -16.4), (0, 2.6, -18.0), 1.0, 10, 'dark', r2=0.8, bevel=0.03)
    b.cyl((0, 2.6, -17.95), (0, 2.6, -18.1), 0.6, 10, 'lightr')

    # ------------------------------------------------------------------ tip panel (wingb at +x; winga = mirror)
    w = k.piece('wingb'); W = w.at
    out = [(0.0, 5.3), (0.0, -5.8), (12.0, -4.6), (10.8, -0.1)]
    w.hull([W(x, y, z) for y, z in out for x in (-0.6, -0.05)], 'paint2', bevel=0.06)   # outer face = underside in flight
    w.hull([W(x, y, z) for y, z in [(1.0, 3.6), (1.0, -4.6), (9.6, -3.9), (9.6, -0.7)] for x in (-0.68, -0.55)], 'team', bevel=0.02)
    w.cyl(W(-0.3, -0.3, -6.0), W(-0.3, -0.3, 5.4), 0.5, 8, 'dark')          # hinge barrel
    k.clone('winga', 'wingb', mirror_x=True)
