"""Deleter (CORE_T2_VEH_Deleter) - Core mobile radar jammer. Long low tracked hull with a tall armoured cabin at the
rear (turret: static, explode only) and the jammer projector: a long forward spear (fork, spins about Z = its long
axis when active) that splits into two wide prongs carrying emitter plates (TA's tuning fork, exaggerated).
Distinct from the Arm Jammer (four-vane rotor on a short boom): a long fork reaching well past the nose, prongs as
two parallel light plates with ochre tips and a red emitter glow, the hub ringed with dark coils.
Value groups from above: dark warm hull, darker paint2 cabin with a team roof, the long light-steel fork (the read: a
light "Y" over a dark hull), black treads, team colour also on a nose plate.
Coordinates are ENGINE/global: X right, Y up, Z forward. mirror=True builds the -X twin sharing UVs."""
import math

UNIT = dict(
    wreck=dict(seed=73, drop=['fork']),
    preview_pose={},
)


def build(k):
    b = k.piece('base')
    xi, xo = 7.4, 13.0
    belt = [(-20.6, 0.0), (16.6, 0.0), (19.8, 2.6), (19.0, 5.4), (-21.6, 5.4), (-23.4, 2.6)]
    b.prism(xi, xo, belt, 'tread', bevel=0.15, mirror=True)
    for z in (-16.4, -9.6, -2.8, 4.0, 10.8):
        b.cyl((xo, 2.0, z), (xo + 0.4, 2.0, z), 1.7, 12, 'dark', mirror=True)
        b.cyl((xo + 0.4, 2.0, z), (xo + 0.65, 2.0, z), 0.7, 8, 'steel', mirror=True)
    # track guards with Core saw-tooth edge
    b.hull([(7.0, 7.4, -22.0), (13.4, 7.4, -22.0), (13.4, 7.4, 13.6), (7.0, 7.4, 13.6),
            (7.0, 5.6, 21.0), (13.0, 5.4, 20.0), (7.0, 5.4, -24.0), (13.0, 5.4, -23.4)], 'paint2', bevel=0.14, mirror=True)
    for z in (-17.0, -9.0, -1.0, 7.0):
        b.hull([(13.3, 7.0, z - 2.6), (13.3, 7.0, z + 2.6), (13.3, 5.4, z - 1.6), (13.3, 5.4, z + 1.6), (14.2, 6.2, z)],
               'dark', bevel=0.05, mirror=True)
    # hull (crosses x = 0): long, wedge nose
    b.prism(-7.4, 7.4, [(-23.0, 2.2), (19.4, 2.2), (23.0, 5.0), (21.4, 8.0), (-22.6, 8.0), (-24.0, 5.0)], 'paint', bevel=0.16)
    b.hull([(x * sx, y, z) for sx in (-1, 1) for x, y, z in
            [(7.0, 8.0, -22.8), (7.0, 8.0, 18.0), (5.0, 11.6, -21.4), (5.0, 11.6, 6.0), (3.2, 9.6, 18.0)]], 'paint', bevel=0.16)
    b.hull([(x * sx, y, z) for sx in (-1, 1) for x, y, z in
            [(3.6, 9.72, 16.6), (3.6, 11.62, 7.4), (3.6, 9.86, 16.7), (3.6, 11.76, 7.5)]], 'team', bevel=0.03)
    # fork bearing pedestal in front of the cabin
    b.hull([(x * sx, y, z) for sx in (-1, 1) for x, y, z in
            [(3.0, 11.6, -9.8), (3.0, 11.6, -3.6), (2.2, 15.4, -8.6), (2.2, 15.4, -5.4)]], 'dark', bevel=0.1)
    b.box((-4.0, 4.4, 21.4), (4.0, 5.6, 22.2), 'dark', bevel=0.05)
    b.box((-3.6, 4.6, 22.15), (3.6, 5.4, 22.25), 'lightw', bevel=0.0)
    b.box((-6.0, 3.0, -24.3), (6.0, 7.0, -23.7), 'dark', bevel=0.05)
    b.box((4.4, 5.0, -24.4), (5.6, 5.8, -24.25), 'lightr', bevel=0.0, mirror=True)

    # ---------------------------------------------------------------- turret: cabin (origin 0, 11.5, -16.5; static)
    t = k.piece('turret'); A = t.at
    t.hull([A(x * sx, y, z) for sx in (-1, 1) for x, y, z in
            [(7.4, 0.0, -6.8), (7.4, 0.0, 3.8), (5.6, 0.0, 6.6), (6.4, 6.4, -6.2), (6.4, 6.4, 3.0), (4.6, 6.4, 5.4),
             (4.4, 9.6, -5.0), (4.4, 9.6, 2.0), (3.4, 8.4, 4.6)]], 'paint2', bevel=0.2)
    t.hull([A(x * sx, y, z) for sx in (-1, 1) for x, y, z in
            [(3.8, 9.58, -4.4), (3.8, 9.58, 1.6), (3.75, 9.74, -4.35), (3.75, 9.74, 1.55)]], 'team', bevel=0.04)
    t.hull([A(x * sx, y, z) for sx in (-1, 1) for x, y, z in
            [(4.2, 6.6, 5.2), (3.2, 8.2, 4.5), (4.2, 6.72, 5.32), (3.2, 8.32, 4.62)]], 'glass', bevel=0.03)
    # whip aerials on the cabin
    for x in (-3.0, 3.0):
        t.cyl(A(x, 9.6, -4.0), A(x, 10.2, -4.0), 0.3, 8, 'dark')
        t.cyl(A(x, 10.2, -4.0), A(x, 15.4, -4.0), 0.09, 6, 'steel', r2=0.045)
        t.cyl(A(x, 15.4, -4.0), A(x, 15.6, -4.0), 0.14, 6, 'lightr')

    # ---------------------------------------------------------------- fork: jammer spear (spins z)
    f = k.piece('fork'); F = f.at
    f.cyl(F(0, 0, 0.0), F(0, 0, 14.0), 1.0, 10, 'steel')
    for z in (1.6, 3.6, 5.6):
        f.cyl(F(0, 0, z), F(0, 0, z + 0.9), 2.2, 10, 'dark', rot=math.pi / 10, bevel=0.05)
    # yoke where the prongs split
    f.hull([F(x, y, z) for x in (-4.4, 4.4) for y in (-1.0, 1.0) for z in (13.0, 15.6)], 'dark', bevel=0.1)
    # prongs: wide flat emitter plates, light, ochre tips, red glow strip on the inner face
    for z0, z1 in ((15.4, 23.2), (23.2, 30.2)):
        f.box(F(2.6, -2.4, z0), F(4.4, 2.4, z1), 'steel', bevel=0.12, mirror=True)
    f.box(F(2.7, -2.3, 30.0), F(4.3, 2.3, 31.4), 'hazard', bevel=0.06, mirror=True)
    f.box(F(2.45, -1.2, 17.0), F(2.6, 1.2, 29.0), 'lightr', bevel=0.0, mirror=True)
