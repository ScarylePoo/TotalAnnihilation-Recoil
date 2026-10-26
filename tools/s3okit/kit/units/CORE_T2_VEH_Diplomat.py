"""Diplomat (CORE_T2_VEH_Diplomat) - Core long-range rocket launcher (Merl counterpart). A broad tracked carrier split
lengthwise: on the right a big rounded armoured hump (crew/reload compartment), on the left an open launch trough
(`bay`, static) holding one huge missile on an erector (`gantry`, pivot at the rear, turns x -90 to stand the missile
up; clamp1/2 static grips, STROBE_RED and smokemit empty emit points). The COB hides/shows `missle` on fire/reload.
Piece layout is the third-party S3O's. Its COB never touches tracks or wheels, so all four track pieces would be
visible together: only tracks1 gets geometry; wheels1..6 are static hub discs.
Distinct from the Merl (Arm: centred team lids over a closed bay, wheels): asymmetric, open trough, a light missile
with an ochre warhead lying in a dark rail, the hump as the dominant dark mass.
Value groups from above: dark warm hump + carrier, black trough interior, the light steel missile body (the read: a long
light bar along the left side), team colour on the hump roof ribs and the trough rims.
Coordinates are ENGINE/global: X right, Y up, Z forward."""
import math

UNIT = dict(
    wreck=dict(seed=61, remove=['missle'], pose={'gantry': (-30, 0, 0)}),
    preview_pose={},
)
XI, XO = 15.0, 21.6


def build(k):
    t1 = k.piece('tracks1')
    belt = [(-23.2, 0.0), (17.4, 0.0), (20.0, 3.0), (19.0, 6.0), (-24.4, 6.0), (-26.0, 3.0)]
    t1.prism(XI, XO, belt, 'tread', bevel=0.16, mirror=True)
    w = k.piece('wheels1'); W = w.at
    w.cyl(W(XO - 0.05, 0, 0), W(XO + 0.35, 0, 0), 2.5, 12, 'dark', bevel=0.05, mirror=True)
    w.cyl(W(XO + 0.35, 0, 0), W(XO + 0.55, 0, 0), 1.05, 8, 'steel', mirror=True)
    for i in range(2, 7):
        k.clone(f'wheels{i}', 'wheels1')

    b = k.piece('base')
    # track guards (flat dark plates) with Core teeth on the front
    b.hull([(14.4, 8.6, -25.0), (22.6, 8.6, -25.0), (22.6, 8.6, 18.6), (14.4, 8.6, 18.6),
            (14.4, 6.4, 22.4), (22.0, 6.4, 21.6), (14.4, 6.0, -26.6), (22.0, 6.0, -26.2)], 'paint2', bevel=0.16, mirror=True)
    for x in (15.6, 18.8):
        b.hull([(x, 6.6, 22.0), (x + 2.6, 6.6, 21.6), (x, 5.0, 22.2), (x + 2.6, 5.0, 21.8), (x + 1.3, 5.6, 24.2)], 'dark', bevel=0.04, mirror=True)
    # chassis deck (crosses x = 0)
    b.prism(-15.0, 15.0, [(-25.4, 3.6), (19.6, 3.6), (22.4, 6.4), (21.4, 9.0), (-25.0, 9.0), (-26.4, 6.0)], 'paint2', bevel=0.16)
    # right hump: big rounded armoured compartment (x 2.4 .. 15)
    b.hull([(x, y, z) for x, y, z in
            [(2.6, 9.0, -25.4), (15.0, 9.0, -25.4), (2.6, 9.0, 21.6), (15.0, 9.0, 21.6),
             (3.4, 19.4, -22.4), (14.0, 19.4, -22.4), (3.4, 19.4, 10.0), (14.0, 19.4, 10.0),
             (5.6, 21.8, -20.0), (11.8, 21.8, -20.0), (5.6, 21.8, 6.0), (11.8, 21.8, 6.0),
             (3.0, 14.6, 20.8), (14.6, 14.6, 20.8), (4.6, 18.6, 15.6), (13.0, 18.6, 15.6)]], 'paint', bevel=0.24)
    # team ribs across the hump roof
    for z in (-16.0, -6.0, 2.0):
        b.box((5.4, 21.8, z), (12.0, 22.02, z + 3.0), 'team', bevel=0.04)
    # vision block + light on the hump nose
    b.box((5.4, 16.0, 19.0), (12.2, 17.6, 20.2), 'dark', bevel=0.06)
    b.box((5.8, 16.3, 20.15), (11.8, 17.2, 20.25), 'lightc', bevel=0.0)
    # exhaust stacks at the hump rear
    b.cyl((13.0, 16.0, -24.8), (13.0, 23.2, -25.6), 1.0, 10, 'dark', bevel=0.05)
    b.cyl((13.0, 23.2, -25.6), (13.0, 23.35, -25.65), 0.7, 10, 'black')
    # front/rear plates of the trough side
    b.box((-14.6, 9.0, 11.6), (2.6, 12.4, 22.0), 'paint', bevel=0.14)
    b.hull([(x, y, z) for x in (-13.6, 1.6) for y, z in [(12.46, 20.4), (12.46, 18.6), (12.6, 20.4), (12.6, 18.6)]], 'hazard', bevel=0.02)
    b.box((-14.6, 9.0, -26.0), (2.6, 12.8, -20.2), 'paint', bevel=0.14)
    b.box((-12.0, 7.2, 22.0), (-2.0, 8.4, 22.7), 'dark', bevel=0.05)
    b.box((-11.6, 7.4, 22.68), (-2.4, 8.2, 22.78), 'lightw', bevel=0.0)
    b.box((-12.0, 6.0, -26.6), (12.0, 8.6, -26.0), 'dark', bevel=0.05)
    for x in (-10.8, 9.6):
        b.box((x, 7.0, -26.7), (x + 1.2, 7.8, -26.55), 'lightr', bevel=0.0)

    # ---------------------------------------------------------------- bay: launch trough walls (static)
    by = k.piece('bay')
    for xa, xb in ((-14.2, -11.8), (0.0, 2.4)):
        by.hull([(x, y, z) for x in (xa, xb) for y, z in [(9.0, -20.0), (9.0, 11.6), (16.4, -19.0), (16.4, 10.6)]], 'paint', bevel=0.12)
        by.box((xa + 0.3, 16.4, -18.0), (xb - 0.3, 16.62, 9.6), 'team', bevel=0.03)
    by.box((-11.8, 9.0, -20.0), (0.0, 9.6, 11.6), 'black', bevel=0.0)          # trough floor
    for z in (-14.0, -6.0, 2.0):                                               # stiffening ribs inside
        by.box((-11.8, 9.6, z), (0.0, 10.4, z + 1.0), 'dark', bevel=0.0)

    # ---------------------------------------------------------------- gantry: erector rail (pivot 1.0, 12.5, -17)
    g = k.piece('gantry'); G = g.at
    g.cyl(G(-10.4, 0, 0), G(0.4, 0, 0), 1.6, 12, 'dark', bevel=0.05)
    for z0, z1 in ((0.0, 9.2), (9.2, 18.4), (18.4, 27.4)):
        g.box(G(-6.6, -2.85, z0), G(-1.2, -2.25, z1), 'dark', bevel=0.06)
    g.box(G(-9.0, -1.6, 24.6), G(0.6, 1.6, 26.6), 'dark', bevel=0.08)        # front cross-head
    # clamps (static) grip the missile midway
    c = k.piece('clamp1'); C = c.at
    c.hull([C(x, y, z) for x in (-5.8, 1.0) for y, z in [(1.0, -1.4), (2.0, -1.4), (1.0, 0.8), (2.0, 0.8)]], 'paint2', bevel=0.06)
    c2 = k.piece('clamp2'); C2 = c2.at
    c2.hull([C2(x, y, z) for x in (-5.8, 1.0) for y, z in [(-2.0, -0.8), (-1.0, -0.8), (-2.0, 1.4), (-1.0, 1.4)]], 'paint2', bevel=0.06)

    # ---------------------------------------------------------------- missle (centre -3.88, 12.5, -4.15; along z)
    m = k.piece('missle'); M = m.at
    m.cyl(M(0, 0, -13.6), M(0, 0, 9.6), 2.2, 12, 'steel')
    m.cyl(M(0, 0, 9.6), M(0, 0, 14.4), 2.2, 12, 'hazard', r2=0.4)
    m.cyl(M(0, 0, -2.0), M(0, 0, 0.6), 2.28, 12, 'team')
    m.cyl(M(0, 0, -14.4), M(0, 0, -13.6), 1.4, 10, 'dark', r2=1.9)
    for a in range(4):
        ang = a * math.pi / 2 + math.pi / 4
        dx, dy = math.cos(ang), math.sin(ang)
        m.hull([M(dx * rr + (-dy) * tt, dy * rr + dx * tt, z) for rr in (1.9, 3.4) for tt in (-0.18, 0.18) for z in (-13.4, -9.6)],
               'dark', bevel=0.0)
