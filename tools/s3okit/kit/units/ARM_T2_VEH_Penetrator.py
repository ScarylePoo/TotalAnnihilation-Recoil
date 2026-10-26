"""Penetrator (ARM_T2_VEH_Penetrator) - Arm mobile energy weapon. TA's odd silhouette exaggerated: a low wide tracked
chassis with a tall tapered pylon rising from its rear half, carrying a big turret ~37 elmos up with one very long
heavy beam cannon reaching far past the nose, and a sensor pod on the turret's right cheek.
The pylon height is the identity: from the game camera the turret floats over the chassis and casts its own block.
Value groups from above: light turret (largest light block, team roof), darker paint2 chassis deck, dark pylon and
treads, long steel barrel with dark coil rings. Barrel and Sensor have odd 3DO origins (deep below their geometry);
they never move on their own (only explode), so geometry is placed in global coordinates where the 3DO had it.
Coordinates are ENGINE/global: X right, Y up, Z forward. mirror=True builds the -X twin sharing UVs."""
import math

UNIT = dict(
    wreck=dict(seed=13, drop=['Barrel'], pose={'Turret': (0, 50, 0), 'Sleeve': (10, 0, 0)}),
    preview_pose={'Turret': (0, -18, 0), 'Sleeve': (-4, 0, 0)},
)


def build(k):
    # ------------------------------------------------------------------ Base: chassis
    b = k.piece('Base')
    xi, xo = 11.6, 19.2
    belt = [(-19.6, 0.0), (18.8, 0.0), (21.4, 2.8), (20.6, 6.4), (-19.0, 7.0), (-21.4, 3.2)]
    b.prism(xi, xo, belt, 'tread', bevel=0.18, mirror=True)
    for z in (-14.6, -7.3, 0.0, 7.3, 14.6):
        b.cyl((xi, 2.4, z), (xi - 0.5, 2.4, z), 2.0, 12, 'dark', mirror=True)
        b.cyl((xi - 0.5, 2.4, z), (xi - 0.8, 2.4, z), 0.8, 8, 'steel', mirror=True)
    # track guards: tall at the rear (counterweight blocks under the pylon), sloping to the nose
    b.hull([(11.2, 9.4, -20.6), (19.8, 9.4, -20.6), (19.8, 13.6, -16.4), (11.2, 13.6, -16.4),
            (19.8, 13.6, -4.0), (11.2, 13.6, -4.0), (19.8, 9.4, 12.0), (11.2, 9.4, 12.0),
            (19.8, 6.8, 21.2), (11.2, 6.8, 21.2), (11.2, 6.6, -21.4), (19.8, 6.6, -21.4)], 'paint', bevel=0.18, mirror=True)
    b.hull([(19.9, 6.8, -19.8), (20.6, 6.8, -19.4), (20.6, 6.8, 18.4), (19.9, 6.8, 18.8),
            (19.6, 3.2, -18.0), (20.3, 3.2, -17.6), (20.3, 3.2, 16.8), (19.6, 3.2, 17.2)], 'paint2', bevel=0.1, mirror=True)
    # team bands on the guard noses (front only: the turret roof is the main team read)
    b.hull([(12.4, 9.52, 11.4), (18.6, 9.52, 11.4), (12.4, 7.62, 18.6), (18.6, 7.62, 18.6),
            (12.4, 9.66, 11.5), (18.6, 9.66, 11.5), (12.4, 7.76, 18.7), (18.6, 7.76, 18.7)], 'team', bevel=0.03, mirror=True)
    b.box((13.0, 13.6, -15.0), (18.0, 14.2, -6.0), 'dark', bevel=0.08, mirror=True)
    for z in (-14.2, -12.6, -11.0, -9.4, -7.8):
        b.box((13.4, 14.2, z), (17.6, 14.32, z + 0.7), 'black', bevel=0.0, mirror=True)
    b.box((14.0, 5.8, 21.0), (17.0, 6.8, 21.6), 'dark', bevel=0.05, mirror=True)
    b.box((14.2, 5.95, 21.58), (16.8, 6.65, 21.68), 'lightw', bevel=0.0, mirror=True)
    # centre hull (crosses x = 0): low wedge in front, deck under the pylon
    b.prism(-11.4, 11.4, [(-20.4, 2.6), (19.6, 2.6), (21.8, 5.0), (20.4, 7.0), (-20.4, 8.0), (-21.0, 5.0)], 'paint2', bevel=0.16)
    b.hull([(x * sx, y, z) for sx in (-1, 1) for x, y, z in
            [(11.0, 7.8, -20.2), (11.0, 7.2, 19.8), (9.0, 11.2, -18.8), (9.0, 11.2, 4.0), (7.0, 8.8, 17.0)]], 'paint2', bevel=0.18)
    b.hull([(x * sx, y, z) for sx in (-1, 1) for x, y, z in
            [(5.6, 9.3, 15.8), (5.6, 9.86, 13.0), (5.6, 9.44, 15.9), (5.6, 10.0, 13.1)]], 'hazard', bevel=0.03)
    # pylon: tapered mast from the deck to the turret ring (crosses x = 0)
    b.hull([(x * sx, y, z) for sx in (-1, 1) for x, y, z in
            [(7.4, 11.0, -16.4), (7.4, 11.0, 2.0), (3.6, 34.0, -11.0), (3.6, 34.0, -4.0),
             (2.8, 36.8, -10.2), (2.8, 36.8, -5.2)]], 'dark', bevel=0.2)
    # light armour fins on the pylon flanks (break the dark mast into stripes from the side and above)
    b.hull([(x, y, z) for x in (7.0, 8.2) for y, z in
            [(11.0, -15.4), (11.0, 0.6), (24.0, -9.0), (26.0, -12.0)]], 'paint', bevel=0.1, mirror=True)
    # cables running up the back of the pylon
    b.cyl((2.4, 11.6, -17.4), (1.6, 33.6, -11.4), 0.55, 8, 'black', mirror=True)
    # rear plate + lights
    b.box((-10.4, 3.6, -21.2), (10.4, 7.4, -20.6), 'dark', bevel=0.06)
    b.box((8.6, 5.8, -21.3), (10.0, 6.6, -21.15), 'lightr', bevel=0.0, mirror=True)

    # ---------------------------------------------------------------- Turret (origin 0, 37.16, -8.21; turns y)
    t = k.piece('Turret'); A = t.at
    t.cyl(A(0, -0.6, 0), A(0, 0.2, 0), 5.2, 18, 'dark', bevel=0.06)
    t.hull([A(x * sx, y, z) for sx in (-1, 1) for x, y, z in
            [(7.6, 0.0, -8.6), (8.6, 0.0, -1.0), (7.2, 0.0, 5.6), (4.2, 0.0, 9.0),
             (6.6, 5.4, -7.8), (7.4, 5.4, -1.0), (6.0, 5.4, 4.6), (3.4, 5.4, 7.2)]], 'paint', bevel=0.2)
    t.hull([A(x * sx, y, z) for sx in (-1, 1) for x, y, z in
            [(5.0, 5.38, -6.6), (5.6, 5.38, -1.0), (4.4, 5.38, 3.4), (2.2, 5.38, 5.4),
             (4.95, 5.54, -6.55), (5.55, 5.54, -1.0), (4.35, 5.54, 3.35), (2.15, 5.54, 5.35)]], 'team', bevel=0.04)
    # dark rear heat sink with fins
    t.box(A(-6.0, 0.6, -10.6), A(6.0, 4.6, -8.2), 'dark', bevel=0.1)
    for y in (1.2, 2.2, 3.2):
        t.box(A(-5.6, y, -10.9), A(5.6, y + 0.5, -10.5), 'black', bevel=0.0)
    # roof mast + light (the 3DO's little aerial)
    t.cyl(A(-3.0, 5.5, -4.0), A(-3.0, 6.3, -4.0), 0.6, 8, 'dark')
    t.cyl(A(-3.0, 6.3, -4.0), A(-3.0, 11.6, -4.0), 0.12, 6, 'steel', r2=0.06)
    t.cyl(A(-3.0, 11.6, -4.0), A(-3.0, 11.85, -4.0), 0.2, 6, 'lightc')

    # ---------------------------------------------------------------- Sensor (right cheek pod, global placement)
    sn = k.piece('Sensor')
    sn.hull([(x, y, z) for x in (8.0, 12.2) for y, z in
             [(37.6, -6.4), (40.6, -6.4), (37.8, 1.6), (40.2, 1.2)]], 'paint2', bevel=0.14)
    sn.box((8.6, 40.6, -5.4), (11.6, 40.85, -0.4), 'team', bevel=0.04)
    sn.cyl((10.1, 39.1, 1.3), (10.1, 39.1, 2.4), 1.0, 12, 'dark', bevel=0.05)
    sn.cyl((10.1, 39.1, 2.4), (10.1, 39.1, 2.5), 0.7, 12, 'lightc')

    # ---------------------------------------------------------------- Sleeve (origin 0, 40.12, -3.65; turns x)
    s = k.piece('Sleeve'); S = s.at
    s.hull([S(x * sx, y, z) for sx in (-1, 1) for x, y, z in
            [(3.6, -2.8, 0.0), (3.6, 2.8, 0.0), (3.2, -2.4, 7.0), (3.2, 2.4, 7.0), (2.2, -1.6, 9.8), (2.2, 1.6, 9.8)]],
           'paint2', bevel=0.14)
    s.box(S(-2.6, 2.7, 0.6), S(2.6, 2.95, 6.4), 'dark', bevel=0.05)

    # ---------------------------------------------------------------- Barrel (static under Sleeve; global placement)
    br = k.piece('Barrel')
    y = 40.12
    br.cyl((0, y, 5.0), (0, y, 31.0), 1.3, 12, 'steel')
    for z in (8.0, 12.0, 16.0, 20.0, 24.0):
        br.cyl((0, y, z), (0, y, z + 1.0), 2.1, 12, 'dark', rot=math.pi / 12, bevel=0.06)
    br.cyl((0, y, 28.0), (0, y, 31.4), 2.4, 8, 'dark', r2=1.6, rot=math.pi / 8, bevel=0.07)
    br.cyl((0, y, 31.4), (0, y, 31.5), 1.3, 8, 'lightc')
