"""Luger (ARM_T2_VEH_Luger) - Arm mobile artillery. Narrow central chassis on four separate track pods (two front,
two rear: TA's layout), a tall twin-post yoke at the rear and a long heavy howitzer riding high above it (sleeve
turns x; barrel recoils 6 elmo back into the sleeve), muzzle well past the nose.
Value groups from above: four light track pods at the corners (big light blocks with a dark gap cross between them),
paint2 central spine, dark yoke, the long gun as a light steel line with a dark cradle and team band on the cradle top
(the unit's read: a long thin cross-shaped mass), team plates on the rear pods.
Coordinates are ENGINE/global: X right, Y up, Z forward. mirror=True builds the -X twin sharing UVs."""
import math

UNIT = dict(
    wreck=dict(seed=17, drop=['barrel'], pose={'turret': (0, 28, 0), 'sleeve': (12, 0, 0)}),
    preview_pose={'turret': (0, -12, 0), 'sleeve': (-14, 0, 0)},
)


def pod(b, z0, z1, top, team):
    xi, xo = 11.0, 20.6
    zc = (z0 + z1) / 2
    belt = [(z0 + 2.4, 0.0), (z1 - 2.4, 0.0), (z1, 2.8), (z1 - 0.8, 5.6), (z0 + 0.8, 5.6), (z0, 2.8)]
    b.prism(xi + 1.2, xo - 0.6, belt, 'tread', bevel=0.16, mirror=True)
    for z in (z0 + 3.6, zc, z1 - 3.6):
        b.cyl((xo - 0.6, 2.4, z), (xo - 0.15, 2.4, z), 1.8, 12, 'dark', mirror=True)
        b.cyl((xo - 0.15, 2.4, z), (xo + 0.15, 2.4, z), 0.7, 8, 'steel', mirror=True)
    # armoured pod housing
    b.hull([(xi, top, z0 + 1.4), (xo, top, z0 + 1.4), (xo, top, z1 - 1.4), (xi, top, z1 - 1.4),
            (xi, 5.2, z0 - 0.4), (xo, 5.2, z0 - 0.4), (xi, 5.2, z1 + 0.4), (xo, 5.2, z1 + 0.4),
            (xi, top - 1.6, z0), (xo + 0.4, top - 1.6, z0), (xi, top - 1.6, z1), (xo + 0.4, top - 1.6, z1)],
           'paint', bevel=0.18, mirror=True)
    if team:
        b.box((xi + 1.6, top, z0 + 2.4), (xo - 1.6, top + 0.2, z1 - 2.4), 'team', bevel=0.04, mirror=True)
    else:
        b.box((xi + 1.6, top, z0 + 2.4), (xo - 1.6, top + 0.5, z1 - 2.4), 'dark', bevel=0.06, mirror=True)
        for z in range(int(z0 + 3.4), int(z1 - 2.4), 2):
            b.box((xi + 2.0, top + 0.5, z), (xo - 2.0, top + 0.62, z + 0.8), 'black', bevel=0.0, mirror=True)


def build(k):
    b = k.piece('base')
    pod(b, 6.0, 24.6, 11.4, False)      # front pods: engine grilles
    pod(b, -25.0, -6.4, 12.6, True)     # rear pods: team plates
    # axle beams between pods and spine (dark, read as the gap cross)
    for z in (15.3, -15.7):
        b.box((-11.2, 4.0, z - 2.2), (11.2, 7.6, z + 2.2), 'dark', bevel=0.12)
    # central spine (crosses x = 0)
    b.prism(-7.6, 7.6, [(-24.4, 3.6), (22.4, 3.6), (25.0, 6.4), (23.6, 10.6), (-23.4, 13.0), (-25.0, 8.0)], 'paint2', bevel=0.18)
    b.hull([(x * sx, y, z) for sx in (-1, 1) for x, y, z in
            [(7.2, 10.4, 21.6), (7.2, 12.6, -2.0), (5.4, 15.8, -4.0), (5.4, 15.8, -20.2), (7.2, 12.6, -23.4), (5.6, 11.0, 23.8)]],
           'paint', bevel=0.18)
    # hazard nose (artillery: front warning plate)
    b.hull([(x * sx, y, z) for sx in (-1, 1) for x, y, z in
            [(5.0, 10.64, 22.6), (5.0, 12.0, 15.0), (5.0, 10.78, 22.7), (5.0, 12.14, 15.1)]], 'hazard', bevel=0.03)
    # outrigger stabiliser jacks folded on the spine flanks
    b.box((7.4, 6.2, -4.0), (9.2, 9.2, 4.0), 'dark', bevel=0.1, mirror=True)
    b.cyl((8.3, 6.2, -2.6), (8.3, 2.0, -2.6), 0.55, 8, 'steel', mirror=True)
    b.box((7.4, 1.4, -4.0), (9.6, 2.0, -1.2), 'dark', bevel=0.06, mirror=True)
    # ammunition hatch + shell racks behind the yoke
    b.box((-4.4, 15.8, -22.4), (4.4, 16.6, -16.8), 'dark', bevel=0.08)
    for x in (-3.0, -1.0, 1.0, 3.0):
        b.cyl((x, 16.6, -21.6), (x, 17.4, -21.6), 0.7, 8, 'hazard')
    b.box((-6.0, 6.0, -25.6), (6.0, 11.0, -25.0), 'dark', bevel=0.06)
    b.box((4.4, 9.4, -25.7), (5.6, 10.2, -25.55), 'lightr', bevel=0.0, mirror=True)
    b.box((-3.6, 9.2, 23.6), (3.6, 10.4, 24.4), 'dark', bevel=0.05)
    b.box((-3.2, 9.4, 24.38), (3.2, 10.2, 24.5), 'lightw', bevel=0.0)
    # antenna, rear right pod
    b.cyl((18.6, 12.6, -23.2), (18.6, 13.3, -23.2), 0.34, 8, 'dark')
    b.cyl((18.6, 13.3, -23.2), (18.6, 19.0, -23.2), 0.1, 6, 'steel', r2=0.05)
    b.cyl((18.6, 19.0, -23.2), (18.6, 19.2, -23.2), 0.15, 6, 'lightc')

    # ---------------------------------------------------------------- turret: yoke (origin 0, 15.98, -10.94)
    t = k.piece('turret'); A = t.at
    t.cyl(A(0, -0.2, 0), A(0, 1.0, 0), 5.6, 18, 'dark', bevel=0.08)
    t.cyl(A(0, 1.0, 0), A(0, 1.8, 0), 4.6, 18, 'paint', bevel=0.06)
    # two posts up to the trunnions at y +7
    t.hull([A(x, y, z) for x in (4.6, 6.4) for y, z in
            [(1.4, -3.6), (1.4, 3.0), (8.4, -1.6), (8.4, 1.4)]], 'paint', bevel=0.14, mirror=True)
    t.box(A(4.4, 1.8, -2.6), A(6.6, 2.0, 2.2), 'team', bevel=0.03, mirror=True)
    # elevation rams
    t.cyl(A(5.2, 1.8, 2.2), A(5.2, 5.6, 5.4), 0.55, 8, 'steel', mirror=True)

    # ---------------------------------------------------------------- sleeve: cradle (origin y 22.98, turns x)
    s = k.piece('sleeve'); S = s.at
    s.cyl(S(-6.6, 0, 0), S(6.6, 0, 0), 1.2, 12, 'steel')
    s.hull([S(x * sx, y, z) for sx in (-1, 1) for x, y, z in
            [(4.4, -3.6, -9.4), (4.4, 3.4, -9.4), (4.4, -3.8, 4.0), (4.4, 3.8, 4.0),
             (2.8, -2.4, 8.6), (2.8, 2.4, 8.6)]], 'paint2', bevel=0.16)
    s.hull([S(x * sx, y, z) for sx in (-1, 1) for x, y, z in
            [(3.0, 3.66, -7.6), (3.0, 3.86, 3.4), (3.0, 3.52, -7.6), (3.0, 3.72, 3.4), (2.2, 2.72, 7.6), (2.2, 2.58, 7.6)]],
           'team', bevel=0.03)
    s.box(S(-4.0, -3.2, -10.4), S(4.0, 3.0, -9.4), 'dark', bevel=0.08)            # breech block
    s.cyl(S(-4.6, -2.8, -6.0), S(-4.6, -2.8, 7.0), 0.6, 8, 'steel')            # recuperator rods
    s.cyl(S(4.6, -2.8, -6.0), S(4.6, -2.8, 7.0), 0.6, 8, 'steel')

    # ---------------------------------------------------------------- barrel (origin 12.47 behind the sleeve)
    br = k.piece('barrel'); B = br.at
    br.cyl(B(0, 0, 10.0), B(0, 0, 44.0), 1.6, 12, 'steel')
    br.cyl(B(0, 0, 17.0), B(0, 0, 21.6), 2.1, 12, 'dark', r2=1.7, bevel=0.06)          # barrel collar at the cradle mouth
    br.cyl(B(0, 0, 27.6), B(0, 0, 29.6), 1.95, 12, 'dark', bevel=0.06)           # fume extractor
    br.cyl(B(0, 0, 43.6), B(0, 0, 47.4), 2.2, 8, 'dark', rot=math.pi / 8, bevel=0.08)    # muzzle brake
    br.cyl(B(0, 0, 47.38), B(0, 0, 47.46), 1.0, 8, 'black')
    for sx in (-1, 1):
        br.box(B(1.9 * sx, -0.6, 44.2), B(2.3 * sx, 0.6, 45.3), 'black', bevel=0.0)
        br.box(B(1.9 * sx, -0.6, 45.8), B(2.3 * sx, 0.6, 46.9), 'black', bevel=0.0)
