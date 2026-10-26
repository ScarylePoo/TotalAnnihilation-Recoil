"""Advanced Construction Vehicle (ARM_T2_VEH_AdvancedConstructor) - Arm T2 builder. The T1 constructor's family
(tall superstructure with a roof bay under two doors) grown into a heavier machine: long continuous tracks under
big angled side armour (TA's trapezoid wings), a taller tower with a raked cab, and a heavier crane.
Build sequence (COB activatescr): doors turn z +-65 deg and sink 7.7, `plate` rises 9.5 to deck level, `arm` swings
up 86 deg, `nano` tilts -70 deg; `turret` (on the plate) traverses; `beam` (empty) is the nano emit point.
The bay is x -7.13..6.47 (off-centre by 0.33 as in TA), z -20..15, so the bay walls are built per side, not mirrored.
Value groups from above: light side wings, a darker paint2 tower with two team-coloured doors (a wide team spine,
broader than the T1's door stripes), hazard trims on the wing noses (construction unit), black tracks.
Coordinates are ENGINE/global: X right, Y up, Z forward. mirror=True builds the -X twin sharing UVs."""
import math

UNIT = dict(
    wreck=dict(seed=41, pose={'door1': (0, 0, -30), 'turret': (0, 40, 0)}),
    preview_pose={},
)
XL, XR = -7.13, 6.47          # bay walls (door hinges)


def build(k):
    b = k.piece('base')
    # ------------------------------------------------------------------ tracks (long, continuous)
    xi, xo = 11.0, 17.4
    belt = [(-20.6, 0.0), (19.6, 0.0), (22.6, 2.8), (21.8, 6.4), (-21.6, 6.4), (-23.6, 2.8)]
    b.prism(xi, xo, belt, 'tread', bevel=0.16, mirror=True)
    for z in (-16.0, -9.6, -3.2, 3.2, 9.6, 16.0):
        b.cyl((xo, 2.4, z), (xo + 0.45, 2.4, z), 1.8, 12, 'dark', mirror=True)
        b.cyl((xo + 0.45, 2.4, z), (xo + 0.7, 2.4, z), 0.7, 8, 'steel', mirror=True)
    # angled side armour (the wings): sloping from the tower shoulder out over the tracks
    b.hull([(10.6, 15.6, -19.6), (10.6, 15.6, 16.6), (17.8, 9.6, -21.0), (17.8, 9.6, 18.6),
            (17.8, 6.4, -22.6), (17.8, 6.4, 20.4), (10.6, 6.4, -23.0), (10.6, 6.4, 22.6),
            (10.6, 10.6, 23.6), (17.4, 7.6, 22.0), (10.6, 11.0, -23.8), (17.4, 8.0, -23.0)], 'paint', bevel=0.18, mirror=True)
    # hazard trims on the wing noses
    nx, ny = 0.64, 0.77
    b.hull([(x + nx * d, y + ny * d, z) for x, y in ((11.4, 14.9), (16.8, 10.4)) for z in (14.6, 16.4) for d in (0.06, 0.2)],
           'hazard', bevel=0.02, mirror=True)
    # team plates on the wing slopes (front half)
    b.hull([(x + nx * d, y + ny * d, z) for x, y in ((11.6, 14.77), (16.6, 10.6)) for z in (1.6, 12.6) for d in (0.06, 0.2)],
           'team', bevel=0.02, mirror=True)
    # vents on the wing slopes (rear)
    for z0, z1 in ((-17.4, -13.4), (-11.4, -7.4)):
        b.hull([(x + nx * d, y + ny * d, z) for x, y in ((12.0, 14.4), (16.0, 11.1)) for z in (z0, z1) for d in (0.06, 0.3)],
               'dark', bevel=0.03, mirror=True)
    # ------------------------------------------------------------------ lower hull (crosses x = 0)
    b.prism(-11.0, 11.0, [(-22.6, 2.6), (21.6, 2.6), (24.0, 6.4), (23.0, 11.6), (-22.6, 11.6), (-24.0, 6.4)], 'paint2', bevel=0.16)
    b.box((XL + 0.2, 11.4, -19.8), (XR - 0.2, 12.6, 14.8), 'dark', bevel=0.0)            # bay floor
    # ------------------------------------------------------------------ tower around the bay (per side)
    for xin, xout in ((XR, 10.8), (XL, -10.8)):
        lo, hi = min(xin, xout), max(xin, xout)
        sh = xin + (0.9 if xin > 0 else -0.9)
        b.hull([(xin, 11.4, -21.2), (xin, 11.4, 17.0), (xout, 11.4, -21.2), (xout, 11.4, 17.0),
                (xin, 25.2, -20.0), (xin, 25.2, 15.0), (sh, 25.2, -20.0), (sh, 25.2, 15.0),
                (xout, 15.6, -20.4), (xout, 15.6, 16.6)], 'paint2', bevel=0.16)
        b.box((min(xin, sh), 25.2, -19.6), (max(xin, sh), 25.45, 14.6), 'dark', bevel=0.04)     # bay rail
    # cab: raked nose block ahead of the bay (crosses x = 0)
    b.hull([(x, y, z) for x, y, z in
            [(-10.8, 11.4, 15.0), (10.8, 11.4, 15.0), (-10.4, 11.4, 23.2), (10.4, 11.4, 23.2),
             (-7.6, 25.2, 15.0), (7.0, 25.2, 15.0), (-7.4, 25.2, 17.0), (6.8, 25.2, 17.0),
             (-7.0, 14.0, 24.4), (6.4, 14.0, 24.4)]], 'paint', bevel=0.18)
    b.hull([(x, y, z) for x, y, z in
            [(-6.2, 22.4, 19.2), (5.6, 22.4, 19.2), (-6.0, 24.6, 17.4), (5.4, 24.6, 17.4),
             (-6.2, 22.52, 19.32), (5.6, 22.52, 19.32), (-6.0, 24.72, 17.52), (5.4, 24.72, 17.52)]], 'glass', bevel=0.03)
    b.box((-6.8, 25.2, 15.4), (6.2, 25.4, 16.8), 'hazard', bevel=0.03)
    # tail block behind the bay
    b.hull([(x, y, z) for x, y, z in
            [(-10.8, 11.4, -20.0), (10.8, 11.4, -20.0), (-10.4, 11.4, -23.4), (10.4, 11.4, -23.4),
             (-7.6, 25.2, -20.0), (7.0, 25.2, -20.0), (-7.4, 25.2, -21.6), (6.8, 25.2, -21.6)]], 'paint', bevel=0.16)
    b.box((-6.0, 13.6, -23.9), (6.0, 20.4, -23.2), 'dark', bevel=0.06)
    for y in (14.2, 15.6, 17.0, 18.4):
        b.box((-5.6, y, -24.05), (5.6, y + 0.6, -23.8), 'black', bevel=0.0)
    b.box((8.0, 12.4, -24.0), (9.8, 13.4, -23.6), 'lightr', bevel=0.0, mirror=True)
    b.box((7.6, 12.4, 23.2), (9.8, 13.8, 24.0), 'dark', bevel=0.06, mirror=True)
    b.box((7.8, 12.6, 23.95), (9.6, 13.6, 24.05), 'lightw', bevel=0.0, mirror=True)
    # amber work beacons on the tail corners + antenna
    for x in (-5.2, 4.6):
        b.cyl((x, 25.2, -21.0), (x, 26.0, -21.0), 0.9, 10, 'dark', bevel=0.04)
        b.cyl((x, 26.0, -21.0), (x, 26.8, -21.0), 0.6, 10, 'lightw')
    b.cyl((-9.2, 15.6, -19.0), (-9.2, 16.2, -19.0), 0.34, 8, 'dark')
    b.cyl((-9.2, 16.2, -19.0), (-9.2, 30.0, -19.0), 0.1, 6, 'steel', r2=0.05)
    b.cyl((-9.2, 30.0, -19.0), (-9.2, 30.2, -19.0), 0.15, 6, 'lightc')

    # ---------------------------------------------------------------- doors (door1 hinge at x -7.13; door2 mirrored)
    dr = k.piece('door1'); D = dr.at
    w = XR - XL
    half = w / 2 - 0.1

    def ys(x):
        return 0.05 + 2.6 * (x - 0.1) / (half - 0.1)
    for z0, z1 in ((-17.4, -5.6), (-5.6, 6.2), (6.2, 17.4)):
        dr.hull([D(x, ys(x) + dy, z) for x in (0.1, half) for z in (z0 + 0.05, z1 - 0.05) for dy in (0.0, -0.6)], 'paint2', bevel=0.08)
    dr.hull([D(x, ys(x) + dy, z) for x in (0.8, 3.0) for z in (-15.6, 15.4) for dy in (0.07, 0.2)], 'team', bevel=0.03)
    dr.cyl(D(0.0, -0.05, -17.0), D(0.0, -0.05, 17.0), 0.5, 8, 'dark')
    k.clone('door2', 'door1', mirror_x=True)

    # ---------------------------------------------------------------- plate (lift, rises 9.5)
    p = k.piece('plate'); Pp = p.at
    for z0, z1 in ((-17.3, -5.6), (-5.6, 6.1), (6.1, 17.3)):
        p.box(Pp(-6.3, -1.0, z0), Pp(6.8, 0.0, z1), 'paint2', bevel=0.08)
    for z0, z1 in ((15.0, 17.0), (-17.0, -15.0)):
        p.box(Pp(-6.0, 0.0, z0), Pp(6.5, 0.14, z1), 'hazard', bevel=0.02)

    # ---------------------------------------------------------------- turret (swivel)
    t = k.piece('turret'); A = t.at
    t.cyl(A(0, 0.0, 0), A(0, 0.6, 0), 3.6, 16, 'dark', bevel=0.06)
    t.cyl(A(0, 0.6, 0), A(0, 3.0, 0), 3.0, 8, 'paint', rot=math.pi / 8, bevel=0.1)
    t.cyl(A(0, 3.0, 0), A(0, 3.15, 0), 2.4, 8, 'team', rot=math.pi / 8)

    # ---------------------------------------------------------------- arm (stowed along -z; heavier twin-beam boom)
    a = k.piece('arm'); R = a.at
    a.cyl(R(-2.2, 0, 0), R(2.4, 0, 0), 1.5, 12, 'dark', bevel=0.05)
    for x0, x1 in ((-1.8, -0.5), (0.7, 2.0)):
        a.hull([R(x, y, z) for x in (x0, x1) for y, z in [(-1.4, 0.8), (1.8, 0.8), (-1.4, -16.2), (1.6, -16.2)]], 'paint', bevel=0.1)
    a.box(R(-0.5, -0.4, -14.0), R(0.7, 0.8, -2.0), 'dark', bevel=0.05)
    a.hull([R(x, y, z) for x in (-1.75, 1.95) for y, z in [(1.75, -1.6), (1.92, -1.6), (1.65, -4.8), (1.82, -4.8)]], 'hazard', bevel=0.02)
    a.cyl(R(2.2, -0.8, -1.8), R(2.2, -0.3, -13.0), 0.5, 8, 'steel')
    a.cyl(R(2.2, -0.8, -1.8), R(2.2, -0.7, -6.4), 0.7, 8, 'dark')
    a.hull([R(x, y, z) for x in (-1.6, 1.8) for y, z in [(-1.4, -15.4), (1.6, -15.4), (-1.0, -18.0), (1.2, -18.0)]], 'dark', bevel=0.08)

    # ---------------------------------------------------------------- nano lathe (beam emit at 0.47, 4.65, 13.03)
    n = k.piece('nano'); N = n.at
    n.cyl(N(-2.6, 0, 0), N(3.0, 0, 0), 1.3, 12, 'dark', bevel=0.05)
    n.hull([N(x, y, z) for x in (-2.4, 3.3) for y, z in [(-0.7, -2.8), (-0.7, 2.2), (6.0, -3.6), (6.0, 1.8), (2.2, -5.4), (5.0, -5.4)]],
           'paint2', bevel=0.12)
    n.box(N(-2.1, 6.0, -2.8), N(3.0, 6.16, 1.0), 'hazard', bevel=0.02)
    bx, by = 0.47, 4.65
    n.cyl(N(bx, by - 0.4, 0.8), N(bx, by, 11.9), 1.45, 10, 'dark', r2=0.85, rot=math.pi / 10)
    for z in (3.0, 5.0, 7.0, 9.0):
        n.cyl(N(bx, by - 0.25, z), N(bx, by - 0.22, z + 0.8), 1.65, 10, 'steel', rot=math.pi / 10)
    n.cyl(N(bx, by, 11.8), N(bx, by, 12.95), 1.05, 10, 'lightc', r2=0.6)
