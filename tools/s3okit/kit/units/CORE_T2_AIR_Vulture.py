"""Vulture (CORE_T2_AIR_Vulture) - Core T2 radar plane. A compact, heavy fuselage on a broad armoured centre wing,
crowned by a big TILTED parabolic radar dish on a mast (radar, spun by the COB in flight, spin y): a light steel rim
around a dark mesh bowl, facing forward-up - from above a sweeping light ellipse in the middle, where the Arm Eagle
shows a flat dark disc with a bar. The Core tip panels (Lwing/Rwing, 15 elmo) stand up when landed and fold out 90 deg
in flight (COB turn z) for a 59-elmo span.
Pieces (TA layout): base, Lwing (+x) / Rwing (-x; mirrored clone of Lwing), radar (dish + mast; spins y).
Value groups from above: dark warm armour, darker paint2 nacelles/spine, the light steel dish rim and mast over a dark
bowl, team on the outer part of the panels' inner face (= top in flight) + plates near the centre-wing tips.
Coordinates are ENGINE/global: X right, Y up, Z forward. mirror=True builds the -X twin sharing UVs."""
import math

UNIT = dict(
    res=1024,
    wreck=dict(seed=53, drop=['radar'], pose={'Lwing': (0, 0, -50)}),
    preview_pose={'Lwing': (0, 0, -90.0), 'Rwing': (0, 0, 90.0), 'radar': (0, 25, 0)},    # flight: panels out
)

WY = 1.85


def build(k):
    b = k.piece('base')
    # ------------------------------------------------------------------ compact heavy fuselage (crosses x = 0)
    b.hull([(x * sx, y, z) for sx in (-1, 1) for x, y, z in
            [(0.6, 0.8, 23.4), (0.6, 2.0, 23.2), (3.8, 0.4, 17.0), (3.6, 4.6, 16.0),
             (5.4, 0.4, 10.5), (5.2, 6.4, 8.4), (5.6, 0.4, -15.4), (5.0, 6.6, -15.4),
             (3.4, 0.8, -23.0), (2.6, 5.0, -23.0)]], 'paint', bevel=0.2, seg=2)
    b.hull([(x * sx, y, z) for sx in (-1, 1) for x, y, z in
            [(1.4, 2.2, 21.0), (3.0, 4.4, 16.4), (2.6, 6.2, 11.0), (1.0, 7.0, 13.0), (1.0, 6.9, 10.6), (1.8, 3.4, 19.4)]],
           'glass', bevel=0.07)
    b.cyl((0, 1.4, 23.2), (0, 1.4, 25.8), 0.4, 8, 'dark', r2=0.14)
    # dark spine with the radar mast base
    b.hull([(x * sx, y, z) for sx in (-1, 1) for x, y, z in
            [(3.2, 6.4, 6.0), (3.6, 6.6, -16.0), (2.4, 7.6, 4.0), (2.6, 7.6, -14.0), (2.0, 5.4, -21.0)]], 'paint2', bevel=0.14)
    b.cyl((0, 7.4, -6.0), (0, 7.8, -6.0), 2.4, 14, 'dark', bevel=0.04)
    # ------------------------------------------------------------------ broad centre wing (mirrored)
    b.hull([(x, WY + t, z) for x, z0, z1, tt in ((5.0, 9.0, -17.0, 1.15), (14.1, 2.2, -15.6, 0.95))
            for z, t in ((z0, 0.0), (z0 - 1.8, tt), (z0 - 1.8, -tt), (z1 + 1.0, tt * 0.8), (z1 + 1.0, -tt * 0.8), (z1, 0.0))],
           'paint', bevel=0.1, mirror=True)
    b.hull([(x, WY + d, z) for x, z in ((10.4, -2.0), (13.6, -1.8), (13.6, -11.4), (10.4, -11.4)) for d in (0.98, 1.08)],
           'team', bevel=0.02, mirror=True)
    b.box((13.3, 0.7, -15.6), (14.15, 3.2, 2.4), 'paint2', bevel=0.08, mirror=True)       # panel hinge rails
    # engine nacelles under/along the wing roots
    b.hull([(x, y, z) for x in (5.4, 9.6) for y, z in ((0.6, 6.0), (4.4, 5.0), (0.6, -16.0), (4.4, -16.0))] +
           [(7.5, 5.0, -2.0), (7.5, 5.0, -15.0)], 'paint2', bevel=0.18, mirror=True)
    b.cyl((7.5, 2.4, 6.2), (7.5, 2.4, 5.6), 1.5, 12, 'black', mirror=True)
    b.cyl((7.5, 2.4, -16.0), (7.5, 2.4, -17.8), 1.8, 12, 'dark', r2=1.5, bevel=0.04, mirror=True)
    b.cyl((7.5, 2.4, -17.75), (7.5, 2.4, -17.9), 1.1, 12, 'lightr', mirror=True)
    # tail: twin low fins
    b.hull([(2.4, 5.0, -15.0), (2.4, 4.4, -23.0), (4.6, 11.0, -21.0), (4.8, 11.0, -25.0),
            (3.2, 5.0, -15.0), (3.2, 4.4, -23.0), (5.4, 11.0, -21.0), (5.6, 11.0, -25.0)], 'paint2', bevel=0.07, mirror=True)
    b.box((4.6, 10.9, -24.8), (5.6, 11.3, -23.8), 'lightr', bevel=0.0, mirror=True)
    b.box((13.6, 1.2, 1.8), (14.3, 2.4, 2.5), 'lightw', bevel=0.0, mirror=True)

    # ------------------------------------------------------------------ tilted radar dish (radar, origin 0, 7.5, -6)
    r = k.piece('radar'); R = r.at
    r.cyl(R(0, 0.2, 0), R(0, 4.2, 0), 0.9, 10, 'steel', r2=0.7, bevel=0.03)              # mast
    r.box(R(-1.6, 3.4, -1.2), R(1.6, 4.6, 0.8), 'dark', bevel=0.08)                      # tilt yoke
    tilt = math.radians(55)                       # dish normal 55 deg from vertical, facing forward-up
    C = (0.0, 5.6, 0.6)
    N = (0.0, math.cos(tilt), math.sin(tilt))
    U = (1.0, 0.0, 0.0)
    V = (0.0, -math.sin(tilt), math.cos(tilt))
    Rr, depth, seg = 9.0, 1.8, 16

    def P(rad, a, off):
        bowl = depth * (rad / Rr) ** 2 + off          # parabolic: rim higher along N than the centre
        return R(C[0] + rad * (math.cos(a) * U[0] + math.sin(a) * V[0]) + bowl * N[0],
                 C[1] + rad * (math.cos(a) * U[1] + math.sin(a) * V[1]) + bowl * N[1],
                 C[2] + rad * (math.cos(a) * U[2] + math.sin(a) * V[2]) + bowl * N[2])
    for i in range(seg):
        a0, a1 = 2 * math.pi * i / seg, 2 * math.pi * (i + 1) / seg
        # dark mesh bowl sector (thin shell)
        r.hull([P(rad, a, off) for rad in (0.6, 7.8) for a in (a0, a1) for off in (-0.25, 0.0)], 'dark', bevel=0.0)
        # light steel rim sector
        r.hull([P(rad, a, off) for rad in (7.7, 9.0) for a in (a0, a1) for off in (-0.45, 0.25)], 'steel', bevel=0.04)
    # feed horn on a tripod at the focus
    F = tuple(C[j] + N[j] * 5.2 for j in range(3))
    r.cyl(R(*F), R(*tuple(F[j] - N[j] * 1.2 for j in range(3))), 0.9, 10, 'dark', r2=0.6)
    r.cyl(R(*F), R(*tuple(F[j] + N[j] * 0.15 for j in range(3))), 0.5, 8, 'lightr')
    for a in (math.pi / 2, math.pi / 2 + 2.1, math.pi / 2 - 2.1):
        r.cyl(R(*tuple(P(7.0, a, 0.0)[j] - R(0, 0, 0)[j] for j in range(3))), R(*F), 0.18, 6, 'steel')

    # ------------------------------------------------------------------ tip panel (Lwing at +x; Rwing = mirror)
    w = k.piece('Lwing'); W = w.at
    # landed: vertical; local y = span (0 at hinge, 15.3 at tip); local x 0 = inner face (top in flight)
    out = [(0.0, 3.1), (0.0, -14.4), (12.3, -7.1), (15.3, -5.9), (15.3, 0.0), (14.1, 0.4)]
    w.hull([W(x, y, z) for y, z in out for x in (0.05, 1.4)], 'paint', bevel=0.08)
    w.hull([W(x, y, z) for y, z in [(5.6, 1.6), (5.6, -10.6), (12.2, -6.6), (14.6, -5.6), (14.6, -0.6), (13.6, -0.2)]
            for x in (-0.08, 0.1)], 'team', bevel=0.03)
    w.hull([W(x, y, z) for y, z in [(0.6, 2.2), (0.6, 0.8), (4.6, 0.6), (4.6, 2.0)] for x in (-0.04, 0.1)], 'steel', bevel=0.0)
    w.cyl(W(0.7, -0.3, -14.4), W(0.7, -0.3, 3.0), 0.75, 8, 'dark')                 # hinge barrel
    w.cyl(W(0.7, 15.5, 0.4), W(0.7, 15.5, -6.2), 0.5, 8, 'dark', r2=0.38)
    w.cyl(W(0.7, 15.5, 0.9), W(0.7, 15.5, 0.38), 0.32, 8, 'lightw', r2=0.5)
    k.clone('Rwing', 'Lwing', mirror_x=True)
