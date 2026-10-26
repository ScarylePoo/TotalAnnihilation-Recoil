"""Hunter (CORE_T2_AIR_Hunter) - Core T2 airborne sonar. A long, narrow armoured fuselage (56 elmo) with a needle nose
and a canted V-tail (Ltail/Rtail splay 45 deg in flight), and two enormous Core wings (Lwing/Rwing, 24 elmo span each)
that stand up like sails when landed and fold out 90 deg in flight (COB turn z). Each wing carries a 15-elmo sonar
disc (Lsonar/Rsonar) on its outer face; in flight the COB runs the discs 16 elmo out along the span to the wing tips
(move y) and spins them (spin x), so the flying Hunter is a 60-elmo thin cross with a big light disc at each tip -
a dumbbell from above, unlike the Arm Seahawk's discs inboard ahead of the wing.
Pieces (TA layout): base (wake1/wake2 empty emit points), Lwing (+x) / Rwing (-x; mirrored clone of Lwing),
Lsonar/Rsonar (discs, children of the wings; Rsonar = mirrored clone), Ltail/Rtail (V-tail; Rtail = mirrored clone).
Value groups from above: dark warm fuselage, paint wings with darker paint2 spars, light steel sonar discs with dark
spokes and a team rim, team on the outer half of the wings' inner face (= top in flight).
Coordinates are ENGINE/global: X right, Y up, Z forward. mirror=True builds the -X twin sharing UVs."""
import math

UNIT = dict(
    res=1024,
    wreck=dict(seed=51, drop=['Rwing'], pose={'Lwing': (0, 0, -40)}),
    always_visible=['Lsonar', 'Rsonar'],
    # flight pose: wings folded out (engine z = -COB z), V-tail splayed, discs run out to the tips
    preview_pose={'Lwing': (0, 0, -90.0), 'Rwing': (0, 0, 90.0), 'Ltail': (0, 0, -45.27), 'Rtail': (0, 0, 45.27),
                  'Lsonar': {'move': (0, 16.25, 0), 'rot': (30, 0, 0)}, 'Rsonar': {'move': (0, 16.25, 0), 'rot': (30, 0, 0)}},
)


def build(k):
    b = k.piece('base')
    # ------------------------------------------------------------------ long armoured fuselage (crosses x = 0)
    b.hull([(x * sx, y, z) for sx in (-1, 1) for x, y, z in
            [(0.3, 0.6, 29.0), (0.3, 1.4, 28.8), (3.3, 0.2, 15.3), (2.6, 6.4, 15.3), (4.2, 3.3, 15.3),
             (4.6, 0.4, 0.0), (4.4, 7.4, -2.0), (4.4, 0.6, -24.0), (4.2, 7.2, -26.0), (2.4, 2.0, -28.6), (2.4, 6.4, -28.6)]],
           'paint', bevel=0.18)
    # dark spine / wing-root saddle (wings hinge at x +-3.1, y 7.12)
    b.hull([(x * sx, y, z) for sx in (-1, 1) for x, y, z in
            [(2.4, 6.6, 12.0), (3.2, 7.6, 10.0), (3.2, 7.6, -22.0), (2.4, 9.1, 8.0), (2.4, 9.1, -24.0), (2.0, 7.0, -28.2)]],
           'paint2', bevel=0.14)
    b.box((2.6, 6.0, -22.4), (3.3, 8.0, 12.6), 'dark', bevel=0.08, mirror=True)        # hinge rails
    # cockpit
    b.hull([(x * sx, y, z) for sx in (-1, 1) for x, y, z in
            [(1.4, 3.2, 23.0), (2.6, 5.4, 18.0), (2.2, 7.0, 13.0), (1.0, 7.8, 15.0), (1.0, 7.6, 12.6), (1.6, 4.0, 21.4)]],
           'glass', bevel=0.07)
    b.cyl((0, 1.0, 28.8), (0, 1.0, 31.6), 0.4, 8, 'dark', r2=0.14)
    # team plate on the spine
    b.hull([(x * sx, y, z) for sx in (-1, 1) for x, y, z in
            [(2.0, 9.12, 4.0), (2.0, 9.12, -10.0), (2.0, 9.26, 4.0), (2.0, 9.26, -10.0)]], 'team', bevel=0.02)
    # twin engines in the tail (wake emits at y 3.5, z -28.3)
    b.cyl((3.0, 3.6, -24.0), (3.0, 3.6, -29.6), 1.9, 12, 'steel', r2=1.6, bevel=0.05, mirror=True)
    b.cyl((3.0, 3.6, -29.55), (3.0, 3.6, -29.7), 1.1, 12, 'lightr', mirror=True)
    b.box((-1.0, 9.05, -14.0), (1.0, 9.4, -12.8), 'lightr', bevel=0.0)

    # ------------------------------------------------------------------ wing (Lwing at +x; Rwing = mirror)
    w = k.piece('Lwing'); W = w.at
    # landed: vertical sail; local y = span (0 at hinge, 24 at tip), local z = chord, local x 0 = inner face (top in flight)
    out = [(0.0, 15.4), (0.0, -16.1), (12.0, -16.1), (24.0, -5.2), (24.0, 0.9), (12.0, 9.8)]
    w.hull([W(x, y, z) for y, z in out for x in (0.05, 1.2)], 'paint', bevel=0.08)
    w.hull([W(x, y, z) for y, z in [(15.0, 6.0), (15.0, -11.9), (23.2, -5.0), (23.2, 0.2)]
            for x in (-0.08, 0.1)], 'team', bevel=0.03)
    for y, z0, z1 in ((3.0, 12.4, -15.4), (7.0, 9.2, -15.4)):
        w.box(W(-0.04, y - 0.6, z1), W(0.1, y + 0.6, z0), 'paint2', bevel=0.0)       # dark spar strips
    w.hull([W(x, y, z) for y, z in [(0.6, -15.2), (0.6, -16.0), (12.0, -16.0), (12.0, -15.2)] for x in (-0.04, 0.1)],
           'dark', bevel=0.0)
    w.cyl(W(0.6, -0.3, -16.0), W(0.6, -0.3, 15.0), 0.8, 8, 'dark')                    # hinge barrel
    w.box(W(0.0, 23.8, -5.2), W(1.2, 24.5, -4.0), 'lightw', bevel=0.0)
    w.box(W(1.1, 3.0, -3.2), W(3.25, 23.6, -0.4), 'paint2', bevel=0.1)              # sonar track on the outer face
    k.clone('Rwing', 'Lwing', mirror_x=True)

    # ------------------------------------------------------------------ sonar disc (Lsonar, origin = Lwing + (3.28, 9.88, -1.74))
    s = k.piece('Lsonar'); S = s.at
    # disc in the wing plane on its outer face; axis = local x (spin x); face at local x 0 is the top in flight
    s.cyl(S(0.25, 0, 0), S(1.8, 0, 0), 7.7, 28, 'steel', r2=7.7, bevel=0.0)
    s.cyl(S(1.8, 0, 0), S(2.6, 0, 0), 7.7, 28, 'steel', r2=6.6, bevel=0.08)
    s.cyl(S(0.25, 0, 0), S(-0.1, 0, 0), 7.7, 28, 'team', r2=7.2, bevel=0.0)          # team rim (top in flight)
    s.cyl(S(-0.1, 0, 0), S(-0.2, 0, 0), 5.9, 28, 'steel', r2=5.6, bevel=0.0)
    for a in (0, 60, 120):
        t = math.radians(a)
        c, n = (math.cos(t), math.sin(t)), (-math.sin(t), math.cos(t))
        s.hull([S(x, c[0] * r + n[0] * o, c[1] * r + n[1] * o) for r in (-6.6, 6.6) for o in (-0.5, 0.5)
                for x in (-0.12, -0.32)], 'dark', bevel=0.0)                           # spokes
    s.cyl(S(-0.2, 0, 0), S(-0.9, 0, 0), 1.6, 12, 'dark', r2=1.1, bevel=0.03)
    k.clone('Rsonar', 'Lsonar', mirror_x=True)

    # ------------------------------------------------------------------ V-tail fin (Ltail, origin 2.17, 9.12, -19.21)
    t = k.piece('Ltail'); T = t.at
    t.hull([T(x, y, z) for x in (-0.4, 0.4) for y, z in ((0.0, 6.3), (0.0, -5.6), (10.9, -3.5), (10.9, -8.9))],
           'paint2', bevel=0.07)
    t.hull([T(x, y, z) for x in (-0.52, -0.42) for y, z in ((7.4, -1.6), (7.4, -6.6), (10.4, -3.8), (10.4, -8.4))],
           'team', bevel=0.0)
    t.box(T(-0.45, 10.8, -8.8), T(0.45, 11.2, -7.8), 'lightr', bevel=0.0)
    k.clone('Rtail', 'Ltail', mirror_x=True)
