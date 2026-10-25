"""Stumpy (ARM_T1_VEH_Stumpy) - Arm medium assault tank. Broad low hull on wide tracks, turret offset to the
left with one long cannon mounted on its right cheek (TA layout: the barrel piece carries the whole gun housing
and both elevates (turn x) and recoils (move z)).
Value groups from above: light Arm armour (fenders, glacis, turret), darker paint2 lower hull / gun housing,
dark mechanics and treads, team bands on the fenders + turret roof, dark heavy barrel against the light hull.
Coordinates are ENGINE/global: X right, Y up, Z forward. mirror=True builds the -X twin sharing UVs."""
import math

UNIT = dict(
    res=1024,
    wreck=dict(seed=5, pose={'turret': (0, 38, 0), 'barrel': (8, 0, 0)}),
    preview_pose={'turret': (0, -20, 0)},
)


def build(k):
    # ------------------------------------------------------------------ base
    b = k.piece('base')
    xi, xo = 9.4, 14.8
    belt = [(-14.6, 0.0), (14.6, 0.0), (17.4, 2.0), (17.2, 3.8), (15.4, 5.3), (-15.4, 5.3), (-17.4, 3.6), (-17.2, 1.8)]
    b.prism(xi, xo, belt, 'tread', bevel=0.15, mirror=True)
    for z in (-11.0, -5.5, 0.0, 5.5, 11.0):
        b.cyl((xi, 1.7, z), (xi - 0.45, 1.7, z), 1.45, 12, 'dark', mirror=True)
        b.cyl((xi - 0.45, 1.7, z), (xi - 0.7, 1.7, z), 0.6, 8, 'steel', mirror=True)
    # fenders: wide flat light plates over the tracks, nose and tail sloping down
    b.hull([(9.0, 6.6, -14.6), (15.3, 6.6, -14.2), (15.3, 6.6, 13.2), (9.0, 6.6, 13.6),
            (9.0, 5.3, 17.6), (14.8, 5.3, 17.0), (9.0, 5.3, -17.4), (14.8, 5.3, -17.0),
            (9.0, 5.1, -14.6), (15.3, 5.1, -14.2), (15.3, 5.1, 13.2), (9.0, 5.1, 13.6)], 'paint', bevel=0.14, mirror=True)
    # side skirt (darker band below the fender edge)
    b.hull([(15.0, 5.2, -15.0), (15.6, 5.2, -14.6), (15.6, 5.2, 13.8), (15.0, 5.2, 14.2),
            (14.8, 2.6, -13.4), (15.4, 2.6, -13.0), (15.4, 2.6, 12.4), (14.8, 2.6, 12.8)], 'paint2', bevel=0.1, mirror=True)
    # team bands along the fender tops
    b.hull([(10.4, 6.6, -12.8), (14.2, 6.6, -12.5), (14.2, 6.6, 11.8), (10.4, 6.6, 12.1),
            (10.45, 6.76, -12.7), (14.15, 6.76, -12.4), (14.15, 6.76, 11.7), (10.45, 6.76, 12.0)], 'team', bevel=0.04, mirror=True)
    # hazard chevrons on the fender noses
    b.hull([(9.6, 5.42, 17.2), (14.3, 5.42, 16.6), (9.6, 6.62, 14.4), (14.6, 6.62, 13.8),
            (9.6, 5.55, 17.15), (14.3, 5.55, 16.55), (9.6, 6.75, 14.35), (14.6, 6.75, 13.75)], 'hazard', bevel=0.03, mirror=True)
    # stowage boxes on the rear fenders (dark blocks break the long plate)
    b.box((10.6, 6.6, -16.0), (13.8, 7.7, -13.4), 'dark', bevel=0.1, mirror=True)
    # lower hull between the tracks (crosses x = 0)
    b.prism(-9.5, 9.5, [(-16.0, 2.4), (14.8, 2.4), (17.6, 5.2), (16.0, 7.0), (-15.6, 7.0), (-17.0, 5.0)], 'paint2', bevel=0.15)
    # upper hull: sloped glacis rising to the turret deck
    b.hull([(x * sx, y, z) for sx in (-1, 1) for x, y, z in
            [(9.0, 6.8, -16.0), (9.0, 6.8, 13.6), (8.2, 6.2, 17.4),
             (8.0, 9.5, -15.0), (8.0, 9.5, 6.6), (6.6, 8.2, 13.6)]], 'paint', bevel=0.16)
    # glacis hazard plate + headlights
    b.hull([(x * sx, y, z) for sx in (-1, 1) for x, y, z in
            [(4.6, 6.6, 16.75), (4.0, 8.0, 14.45), (4.6, 6.73, 16.87), (4.0, 8.13, 14.57)]], 'hazard', bevel=0.03)
    b.box((5.6, 5.6, 16.7), (7.4, 6.5, 17.7), 'dark', bevel=0.07, mirror=True)
    b.box((5.8, 5.75, 17.68), (7.2, 6.35, 17.78), 'lightw', bevel=0.0, mirror=True)
    # driver's vision block on the glacis, right of centre (left is under the turret overhang)
    b.box((2.2, 9.2, 8.0), (5.2, 10.1, 10.2), 'paint2', bevel=0.08)
    b.box((2.5, 9.4, 10.18), (4.9, 9.85, 10.28), 'lightc', bevel=0.0)
    # rear engine deck: dark louvre block, slats, exhausts
    b.box((-6.0, 9.4, -15.0), (6.0, 10.2, -11.0), 'dark', bevel=0.1)
    for z in (-14.4, -13.5, -12.6, -11.7):
        b.box((-5.5, 10.2, z), (5.5, 10.35, z + 0.45), 'black', bevel=0.0)
    b.cyl((7.0, 9.0, -15.4), (7.0, 11.2, -15.9), 0.6, 10, 'dark', bevel=0.04, mirror=True)
    b.cyl((7.0, 11.2, -15.9), (7.0, 11.35, -15.95), 0.42, 10, 'black', mirror=True)
    # rear plate + tail lights
    b.box((-6.5, 6.8, -16.4), (6.5, 9.2, -15.9), 'paint2', bevel=0.06)
    b.box((4.8, 8.0, -16.5), (5.9, 8.6, -16.35), 'lightr', bevel=0.0, mirror=True)
    # whip antenna, rear right
    b.cyl((8.0, 9.5, -13.6), (8.0, 10.2, -13.6), 0.34, 8, 'dark')
    b.cyl((8.0, 10.2, -13.6), (8.0, 15.0, -13.6), 0.09, 6, 'steel', r2=0.045)
    b.cyl((8.0, 15.0, -13.6), (8.0, 15.2, -13.6), 0.14, 6, 'lightc')

    # ---------------------------------------------------------------- turret (origin -0.5, 13, -6.5; turns about Y)
    t = k.piece('turret'); A = t.at
    t.cyl(A(-1.6, -3.7, -0.5), A(-1.6, -3.2, -0.5), 4.6, 18, 'dark', bevel=0.06)
    # faceted body: wide at the rear, narrow nose, gun cheek on its right
    t.hull([A(x, y, z) for x, y, z in
            [(-6.4, -3.25, -7.6), (1.8, -3.25, -7.6), (-6.8, -3.25, 1.0), (1.9, -3.25, 1.6), (-4.6, -3.25, 6.2), (0.6, -3.25, 6.4),
             (-5.6, 0.2, -6.8), (1.2, 0.2, -6.8), (-5.9, 0.2, 0.6), (1.3, 0.2, 1.2), (-3.8, 0.0, 4.8), (0.1, 0.0, 5.0)]],
           'paint', bevel=0.14)
    # team roof plate
    t.hull([A(x, y, z) for x, y, z in
            [(-4.7, 0.18, -5.6), (0.4, 0.18, -5.6), (-4.9, 0.18, 0.4), (0.5, 0.18, 0.8), (-3.2, 0.1, 3.8), (-0.4, 0.1, 3.9),
             (-4.65, 0.33, -5.55), (0.35, 0.33, -5.55), (-4.85, 0.33, 0.4), (0.45, 0.33, 0.8), (-3.15, 0.25, 3.75), (-0.45, 0.25, 3.85)]],
           'team', bevel=0.03)
    # commander's cupola, left rear, with a cyan vision slot
    t.cyl(A(-3.6, 0.2, -3.8), A(-3.6, 1.1, -3.8), 1.35, 12, 'paint2', bevel=0.07)
    t.cyl(A(-3.6, 1.1, -3.8), A(-3.6, 1.3, -3.8), 0.95, 12, 'dark')
    t.box(A(-4.4, 0.55, -2.55), A(-2.8, 0.85, -2.4), 'lightc', bevel=0.0)
    # rear bustle (darker stowage)
    t.hull([A(x, y, z) for x, y, z in
            [(-5.4, -2.9, -7.4), (0.8, -2.9, -7.4), (-5.4, -0.4, -7.2), (0.8, -0.4, -7.2),
             (-5.0, -2.7, -8.8), (0.4, -2.7, -8.8), (-5.0, -0.7, -8.6), (0.4, -0.7, -8.6)]], 'paint2', bevel=0.09)
    # sensor mast on the left flank
    t.box(A(-7.4, -2.6, -2.4), A(-6.2, -0.6, 1.2), 'dark', bevel=0.08)

    # ---------------------------------------------------------------- barrel (origin 1.5, 11.5, -7: elevates + recoils)
    br = k.piece('barrel'); B = br.at
    gx, gy = 2.2, -0.2               # bore axis, from the flare offset
    # gun housing (trunnion block) seated on the turret's right cheek
    br.hull([B(x, y, z) for x, y, z in
             [(0.2, -1.5, -3.4), (4.2, -1.5, -3.4), (0.2, 1.6, -3.4), (4.2, 1.6, -3.4),
              (0.4, -1.3, 4.0), (4.0, -1.3, 4.0), (0.6, 1.2, 4.6), (3.8, 1.2, 4.6)]], 'paint2', bevel=0.12)
    br.box(B(1.0, 1.55, -2.6), B(3.4, 1.75, 2.8), 'team', bevel=0.04)
    br.cyl(B(gx, gy, 4.4), B(gx, gy, 6.4), 1.15, 10, 'dark', r2=0.9, rot=math.pi / 10, bevel=0.05)
    # long heavy tube (exaggerated: 0.62 radius) with a thermal sleeve and a muzzle brake
    br.cyl(B(gx, gy, 6.0), B(gx, gy, 22.0), 0.62, 10, 'dark')
    br.cyl(B(gx, gy, 9.0), B(gx, gy, 14.0), 0.78, 10, 'dark', rot=math.pi / 10, bevel=0.04)
    br.cyl(B(gx, gy, 21.8), B(gx, gy, 23.3), 0.9, 8, 'dark', rot=math.pi / 8, bevel=0.05)
    br.cyl(B(gx, gy, 23.28), B(gx, gy, 23.36), 0.42, 8, 'black')
    for sx in (-1, 1):
        br.box(B(gx + 0.75 * sx, gy - 0.3, 22.15), B(gx + 0.95 * sx, gy + 0.3, 22.95), 'black', bevel=0.0)
