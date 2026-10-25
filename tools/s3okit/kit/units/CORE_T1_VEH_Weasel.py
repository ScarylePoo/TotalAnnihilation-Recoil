"""Weasel (CORE_T1_VEH_Weasel) - Core fast scout. Six-wheeled armoured buggy: wedge nose, wide rear over big
rear wheels, a small pyramid turret at the back with one light gun.
Piece layout is the third-party remodel's (the COB drives it): base (body), turret (turn y), barrel (query/aim point:
its exported emit vertices keep the original fire position), rwheel / mwheel / fwheel = one piece per axle, both
wheels in each (spin x). Wheels are exaggerated chunky discs so the 6-wheel stance reads from above.
Value groups from above: dark warm wedge armour, darker paint2 side pods, black tyres, team plates on the rear
mudguards and the turret faces, light steel gun, centre-line team stripe down the nose.
Coordinates are ENGINE/global: X right, Y up, Z forward. mirror=True builds the -X twin sharing UVs."""
import math

UNIT = dict(
    res=1024,
    wreck=dict(seed=11, drop=['fwheel'], pose={'turret': (0, 60, 0)}),
    preview_pose={'turret': (0, -20, 0)},
)


def wheel(k, name, x0, x1, r):
    w = k.piece(name); W = w.at
    w.cyl(W(x0, 0, 0), W(x1, 0, 0), r, 14, 'tread', rot=math.pi / 14, bevel=0.25, mirror=True)
    w.cyl(W(x1, 0, 0), W(x1 + 0.3, 0, 0), r * 0.55, 10, 'dark', bevel=0.05, mirror=True)
    w.cyl(W(x1 + 0.3, 0, 0), W(x1 + 0.5, 0, 0), r * 0.22, 8, 'steel', mirror=True)


def build(k):
    wheel(k, 'rwheel', 10.0, 14.0, 5.2)
    wheel(k, 'mwheel', 6.6, 9.6, 3.5)
    wheel(k, 'fwheel', 5.6, 8.6, 3.5)

    b = k.piece('base')
    # belly pan (crosses x = 0)
    b.prism(-5.4, 5.4, [(-17.6, 4.9), (17.6, 4.9), (19.4, 6.6), (18.6, 8.0), (-17.8, 8.0), (-18.1, 6.2)], 'paint2', bevel=0.14)
    # main wedge: narrow pointed nose, wide flat rear deck
    b.hull([(x * sx, y, z) for sx in (-1, 1) for x, y, z in
            [(5.4, 7.6, 19.0), (2.6, 7.4, 19.4), (5.6, 7.6, 2.0), (9.6, 7.6, -2.0), (9.8, 7.6, -17.4),
             (2.0, 9.2, 18.4), (4.4, 11.8, 4.0), (8.6, 12.4, -4.0), (8.6, 12.4, -16.6), (5.0, 13.6, -14.6), (5.0, 13.6, -4.0)]],
           'paint', bevel=0.16)
    # hazard nose tip
    b.hull([(x * sx, y, z) for sx in (-1, 1) for x, y, z in
            [(1.8, 9.24, 17.8), (3.2, 10.6, 10.6), (1.8, 9.38, 17.84), (3.2, 10.74, 10.64)]], 'paint2', bevel=0.03)
    # driver slit
    b.hull([(x * sx, y, z) for sx in (-1, 1) for x, y, z in
            [(3.0, 11.3, 6.6), (3.4, 12.3, 3.4), (3.0, 11.44, 6.64), (3.4, 12.44, 3.44)]], 'dark', bevel=0.03)
    # centre-line team stripe down the nose deck (the Weasel's top-view mark)
    b.hull([(x * sx, y, z) for sx in (-1, 1) for x, y, z in
            [(1.5, 9.56, 16.6), (2.0, 11.0, 8.4), (2.2, 11.85, 3.6),
             (1.5, 9.72, 16.62), (2.0, 11.16, 8.42), (2.2, 12.01, 3.62)]], 'team', bevel=0.03)
    # rear mudguards over the big wheels: flat team tops (main team read)
    b.hull([(9.4, 10.6, -13.6), (14.6, 10.6, -13.6), (9.4, 10.6, -1.4), (14.6, 10.6, -1.4),
            (9.4, 11.6, -11.8), (14.4, 11.6, -11.8), (9.4, 11.6, -3.2), (14.4, 11.6, -3.2)], 'paint', bevel=0.12, mirror=True)
    b.box((10.2, 11.6, -11.2), (13.6, 11.76, -3.8), 'team', bevel=0.04, mirror=True)
    # side pods between mid/front wheels (fuel tanks), darker
    b.hull([(4.6, 7.8, 0.4), (6.8, 7.8, 0.4), (4.6, 7.8, 15.6), (6.8, 7.8, 15.0),
            (4.6, 9.8, 1.0), (6.2, 9.8, 1.0), (4.6, 9.8, 14.6), (6.2, 9.8, 14.2)], 'paint2', bevel=0.1, mirror=True)
    # headlights
    b.box((3.4, 7.0, 18.0), (5.0, 8.0, 18.8), 'dark', bevel=0.05, mirror=True)
    b.box((3.55, 7.15, 18.78), (4.85, 7.85, 18.88), 'lightw', bevel=0.0, mirror=True)
    # rear: engine grille, exhausts, tail lights
    b.box((-4.4, 9.0, -18.0), (4.4, 12.6, -17.4), 'dark', bevel=0.06)
    for y in (9.5, 10.5, 11.5):
        b.box((-4.0, y, -18.15), (4.0, y + 0.45, -17.9), 'black', bevel=0.0)
    b.cyl((6.6, 8.0, -17.4), (6.6, 8.8, -19.4), 0.55, 10, 'dark', mirror=True)
    b.cyl((6.6, 8.8, -19.4), (6.6, 8.85, -19.55), 0.38, 10, 'black', mirror=True)
    b.box((7.2, 10.8, -17.75), (8.6, 11.6, -17.55), 'lightr', bevel=0.0, mirror=True)
    # long whip antenna (scout tell), left rear
    b.cyl((-6.8, 12.4, -15.4), (-6.8, 13.1, -15.4), 0.34, 8, 'dark')
    b.cyl((-6.8, 13.1, -15.4), (-6.8, 21.0, -15.4), 0.1, 6, 'steel', r2=0.045)
    b.cyl((-6.8, 21.0, -15.4), (-6.8, 21.2, -15.4), 0.15, 6, 'lightr')

    # ---------------------------------------------------------------- turret (origin 0, 14.91, -8.75)
    t = k.piece('turret'); A = t.at
    t.cyl(A(0, -1.4, 0), A(0, -0.9, 0), 4.2, 16, 'dark', bevel=0.05)
    # low pyramid
    t.hull([A(x * sx, y, z) for sx in (-1, 1) for x, y, z in
            [(4.8, -0.9, -4.6), (4.8, -0.9, 3.6), (1.6, 2.0, -1.4), (1.6, 2.0, 0.6), (3.4, -0.9, 4.6)]], 'paint', bevel=0.12)
    # team panels on the two sloped side faces
    for sx in (1,):
        pts = [(4.0, -0.5, -3.6), (4.0, -0.5, 2.8), (1.9, 1.6, -1.3), (1.9, 1.6, 0.5)]
        nrm = (0.81, 0.58)
        t.hull([A(x + nrm[0] * d, y + nrm[1] * d, z) for x, y, z in pts for d in (0.06, 0.2)], 'team', bevel=0.02, mirror=True)
    t.box(A(-0.9, 1.9, -1.1), A(0.9, 2.3, 0.4), 'paint2', bevel=0.05)
    t.box(A(-0.6, 1.95, 0.38), A(0.6, 2.2, 0.48), 'lightc', bevel=0.0)

    # ---------------------------------------------------------------- barrel (origin 0, 15.25, -5.08)
    br = k.piece('barrel'); B = br.at
    br.box(B(-1.2, -0.9, 0.0), B(1.2, 0.9, 2.6), 'paint2', bevel=0.1)
    br.cyl(B(0, 0, 2.4), B(0, 0, 10.6), 0.62, 10, 'steel')
    br.cyl(B(0, 0, 4.4), B(0, 0, 6.6), 0.85, 10, 'steel', rot=math.pi / 10, bevel=0.03)
    br.cyl(B(0, 0, 9.8), B(0, 0, 10.8), 0.85, 8, 'steel', rot=math.pi / 8, bevel=0.04)
    br.cyl(B(0, 0, 10.78), B(0, 0, 10.84), 0.36, 8, 'black')
