"""Seahawk (ARM_T2_AIR_Seahawk) - Arm T2 airborne sonar (maritime patrol). Same airframe family as the Eagle but read
differently from above: no rotodome; instead a deep flying-boat hull with a keel, two engines on the wing roots, a
T-tail, and TWO big sonar domes on booms under the wing (Sonarholder1/2 > Sonar1/2). In flight the COB slides the
outer wing panels (Lwing/Rwing) out 11.5 elmo and runs the booms 11 elmo FORWARD (move z), so the light, team-rimmed
sonar discs spin (spin y) ahead of the leading edge - two bright discs on the wing like a pair of eyes, where the
Eagle shows one dark disc in the middle.
Pieces (TA layout): base, Lwing (+x) / Rwing (-x; mirrored clone of Lwing), Sonarholder1/2 (booms, slide in z;
Sonarholder1 = mirrored clone of 2), Sonar1/Sonar2 (domes, spin y; Sonar1 = mirrored clone of 2).
Value groups from above: light Arm hull and wings, dark paint2 nacelles + keel + T-tail, light domes with dark
spokes, team on the dome rims, outer wing panels and the T-tail plane.
Coordinates are ENGINE/global: X right, Y up, Z forward. mirror=True builds the -X twin sharing UVs."""
import math

UNIT = dict(
    res=1024,
    wreck=dict(seed=49, drop=['Sonarholder1'], remove=['Rwing']),
    always_visible=['Lwing', 'Rwing', 'Sonarholder1', 'Sonarholder2', 'Sonar1', 'Sonar2'],
    # flight pose: outer panels out (engine x = -COB x), sonar booms forward (z unchanged)
    preview_pose={'Lwing': {'move': (11.5, 0, 0)}, 'Rwing': {'move': (-11.5, 0, 0)},
                  'Sonarholder1': {'move': (0, 0, 10.75)}, 'Sonarholder2': {'move': (0, 0, 11.0)}},
)

WY = 1.3


def build(k):
    b = k.piece('base')
    # ------------------------------------------------------------------ flying-boat hull (crosses x = 0)
    b.hull([(x * sx, y, z) for sx in (-1, 1) for x, y, z in
            [(0.6, 2.4, 25.8), (0.8, 4.0, 25.2), (3.4, 0.8, 20.0), (3.6, 5.0, 19.0),
             (5.4, 0.6, 12.0), (4.8, 7.0, 10.0), (5.4, 0.6, -10.0), (4.6, 7.2, -12.0),
             (3.0, 2.4, -24.0), (2.8, 6.4, -24.6), (1.4, 4.0, -28.0), (1.4, 5.6, -28.0)]], 'paint', bevel=0.2, seg=2)
    # dark keel / planing step along the belly
    b.hull([(x * sx, y, z) for sx in (-1, 1) for x, y, z in
            [(0.4, -0.4, 18.0), (3.0, 0.9, 19.0), (0.4, -0.6, -4.0), (3.6, 0.7, -4.0), (0.4, 1.0, -16.0), (3.0, 1.6, -16.0)]],
           'paint2', bevel=0.12)
    b.hull([(x * sx, y, z) for sx in (-1, 1) for x, y, z in
            [(1.8, 4.6, 22.8), (3.4, 6.0, 18.0), (2.8, 7.6, 12.0), (1.2, 8.2, 14.4), (1.2, 8.0, 11.6), (2.2, 5.4, 21.2)]],
           'glass', bevel=0.07)
    # dorsal spine stripe: team runs from the cockpit to the fin
    b.hull([(x * sx, y, z) for sx in (-1, 1) for x, y, z in
            [(1.6, 7.28, 8.0), (1.6, 7.3, -12.0), (1.6, 7.44, 8.0), (1.6, 7.46, -12.0)]], 'team', bevel=0.02)

    # ------------------------------------------------------------------ straight fixed wing on the hull top (mirrored)
    HY = 5.6       # high wing
    b.hull([(x, HY + t, z) for x, z0, z1, tt in ((4.0, 10.0, -9.0, 0.9), (18.4, 4.0, -9.0, 0.55))
            for z, t in ((z0, 0.0), (z0 - 1.6, tt), (z0 - 1.6, -tt), (z1 + 1.0, tt * 0.8), (z1 + 1.0, -tt * 0.8), (z1, 0.0))],
           'paint', bevel=0.08, mirror=True)
    b.hull([(x, HY + d, z) for x in (5.0, 17.6) for z in (-6.4, -8.6) for d in (0.66, 0.76)], 'paint2', bevel=0.0, mirror=True)
    # engine nacelles on the wing roots
    b.cyl((7.6, HY + 1.8, 9.0), (7.6, HY + 1.8, -9.6), 2.2, 12, 'paint2', r2=1.8, rot=math.pi / 12, bevel=0.08, mirror=True)
    b.cyl((7.6, HY + 1.8, 9.2), (7.6, HY + 1.8, 8.9), 1.5, 12, 'black', mirror=True)
    b.cyl((7.6, HY + 1.8, -9.55), (7.6, HY + 1.8, -9.75), 1.1, 12, 'lightc', mirror=True)
    # wing struts down to the boom roots (the sonar booms run under the wing)
    b.hull([(x, y, z) for x in (10.6, 12.4) for y in (0.6, 1.4) for z in (-14.8, -0.6)], 'dark', bevel=0.08, mirror=True)
    b.hull([(11.2, 1.2, -6.0), (11.8, 1.2, -6.0), (11.2, 1.2, -9.0), (11.8, 1.2, -9.0),
            (11.2, HY - 0.6, -6.0), (11.8, HY - 0.6, -6.0), (11.2, HY - 0.6, -9.0), (11.8, HY - 0.6, -9.0)], 'dark', bevel=0.04, mirror=True)
    b.box((17.8, HY - 0.4, 3.4), (18.6, HY + 0.5, 4.4), 'lightw', bevel=0.0, mirror=True)
    # T-tail
    b.hull([(x, y, z) for x in (-0.45, 0.45) for y, z in ((6.4, -16.0), (5.4, -27.6), (13.0, -23.4), (13.0, -28.6))],
           'paint2', bevel=0.07)
    b.hull([(x * sx, y, z) for sx in (-1, 1) for x, y, z in
            [(9.0, 12.8, -26.6), (9.0, 12.8, -29.0), (0.8, 12.6, -22.8), (0.8, 12.6, -28.8),
             (9.0, 13.3, -26.6), (9.0, 13.3, -29.0), (0.8, 13.5, -22.8), (0.8, 13.5, -28.8)]], 'paint', bevel=0.06)
    b.hull([(x * sx, y, z) for sx in (-1, 1) for x, y, z in
            [(8.2, 13.34, -26.8), (8.2, 13.34, -28.6), (1.2, 13.52, -23.6), (1.2, 13.52, -28.4),
             (8.2, 13.44, -26.8), (8.2, 13.44, -28.6), (1.2, 13.64, -23.6), (1.2, 13.64, -28.4)]], 'team', bevel=0.02)
    b.box((8.6, 12.8, -29.0), (9.4, 13.3, -28.0), 'lightr', bevel=0.0, mirror=True)

    # ------------------------------------------------------------------ Lwing (origin 5, 0.5, -7.5; slides +11.5)
    w = k.piece('Lwing'); W = w.at
    ly = HY - 0.5          # outer panel at the fixed wing's height (piece origin y 0.5)
    pl = [(-1.5, 9.4), (-1.5, -2.0), (12.8, -1.0), (12.8, 3.2)]
    pts = []
    for x, z in pl:
        t = 0.6 - 0.25 * (x + 1.5) / 14.3
        pts += [W(x, ly + t, z + 1.0), W(x, ly - t, z + 1.0)]
    w.hull(pts, 'paint', bevel=0.06)
    tp = [(3.6, 7.4), (12.0, 3.0), (12.0, 0.4), (3.6, -0.8)]
    w.hull([W(x, ly + 0.6 - 0.25 * (x + 1.5) / 14.3 + d, z + 1.0) for x, z in tp for d in (0.04, 0.14)], 'team', bevel=0.02)
    w.box(W(12.6, ly - 0.4, 1.2), W(13.2, ly + 0.4, 2.4), 'lightw', bevel=0.0)
    k.clone('Rwing', 'Lwing', mirror_x=True)

    # ------------------------------------------------------------------ sonar boom (Sonarholder2, origin 11.5, -0.5, -13.62)
    h = k.piece('Sonarholder2'); H = h.at
    h.hull([H(x, y, z) for x in (-0.9, 0.9) for y, z in ((0.6, -1.0), (2.2, -1.0), (2.2, 11.4), (0.6, 13.0))],
           'paint2', bevel=0.1)
    h.cyl(H(0, 1.4, -1.0), H(0, 1.4, -2.2), 0.8, 8, 'dark', r2=0.45)
    # dome (Sonar2, origin = boom + (0.08, -1.09, 12.37)); spins y
    s = k.piece('Sonar2'); S = s.at
    # the dome sits ON the boom (Sonar origin is 1.6 below ground): local y 1.8 .. 3.7
    s.cyl(S(0, 1.8, 0), S(0, 2.8, 0), 5.0, 24, 'paint', r2=6.2, bevel=0.06)
    s.cyl(S(0, 2.8, 0), S(0, 3.7, 0), 6.2, 24, 'paint', r2=5.6, bevel=0.08)
    s.cyl(S(0, 2.85, 0), S(0, 3.55, 0), 6.32, 24, 'team', r2=5.8, bevel=0.0)       # team rim
    for a in (0, 120, 240):
        t = math.radians(a)
        c, n = (math.cos(t), math.sin(t)), (-math.sin(t), math.cos(t))
        s.hull([S(c[0] * r + n[0] * o, y, c[1] * r + n[1] * o) for r in (1.0, 5.0) for o in (-0.5, 0.5)
                for y in (3.72, 3.9)], 'dark', bevel=0.0)                          # spokes (show the spin)
    s.cyl(S(0, 3.7, 0), S(0, 4.3, 0), 1.3, 12, 'dark', r2=0.9, bevel=0.03)
    k.clone('Sonarholder1', 'Sonarholder2', mirror_x=True)
    k.clone('Sonar1', 'Sonar2', mirror_x=True)
