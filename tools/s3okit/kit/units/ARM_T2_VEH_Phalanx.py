"""Phalanx (ARM_T2_VEH_Phalanx) - Arm mobile flak. Six big wheels (wheel1..6 spin x) under a long armoured wedge
body that rises to a central pylon; on top a compact flak mount (turret turns y AND x: the whole mount elevates)
carrying four recoiling barrels in a diamond: two outer low (gun1/gun4), two inner high (gun2/gun3).
Value groups from above: light wedge body with a team chevron on the nose deck, darker paint2 pylon/mount,
four light steel barrels fanned on a dark gun frame with team cheek plates, black tyres outboard.
Coordinates are ENGINE/global: X right, Y up, Z forward. mirror=True builds the -X twin sharing UVs."""
import math

UNIT = dict(
    wreck=dict(seed=23, drop=['gun1'], pose={'turret': (20, 30, 0)}),
    preview_pose={'turret': (-25, -15, 0)},
)


def build(k):
    # ------------------------------------------------------------------ wheels: build wheel4 (+X), clone the rest
    w = k.piece('wheel4'); W = w.at
    w.cyl(W(-2.6, 0, 0), W(2.6, 0, 0), 4.0, 16, 'tread', rot=math.pi / 16, bevel=0.16)
    w.cyl(W(2.6, 0, 0), W(3.0, 0, 0), 2.4, 12, 'dark', bevel=0.05)
    w.cyl(W(3.0, 0, 0), W(3.3, 0, 0), 1.0, 8, 'steel')
    for i in (5, 6):
        k.clone(f'wheel{i}', 'wheel4')
    for i in (1, 2, 3):
        k.clone(f'wheel{i}', 'wheel4', mirror_x=True)

    # ------------------------------------------------------------------ base (origin 0, 6, 0)
    b = k.piece('base')
    # chassis between the wheels
    b.prism(-7.4, 7.4, [(-20.4, 1.0), (19.6, 1.0), (22.6, 3.6), (21.8, 6.8), (-20.6, 6.8), (-21.8, 3.4)], 'paint2', bevel=0.16)
    # wheel arches/fenders: light plates over the wheels, sloping down at both ends
    b.hull([(7.2, 9.2, -16.4), (14.4, 9.2, -16.4), (7.2, 9.2, 14.4), (14.4, 9.2, 14.4),
            (7.2, 6.6, 19.4), (13.6, 6.6, 18.6), (7.2, 7.0, -19.6), (13.6, 7.0, -19.0),
            (7.2, 7.4, -16.4), (14.6, 7.4, -16.4), (14.6, 7.4, 14.4), (7.2, 7.4, 14.4)], 'paint', bevel=0.16, mirror=True)
    b.hull([(14.5, 7.6, -16.0), (15.1, 7.6, -15.6), (15.1, 7.6, 14.2), (14.5, 7.6, 14.6),
            (14.4, 6.0, -15.0), (15.0, 6.0, -14.6), (15.0, 6.0, 13.2), (14.4, 6.0, 13.6)], 'paint2', bevel=0.08, mirror=True)
    b.box((9.0, 9.2, -14.6), (13.2, 9.42, -6.0), 'dark', bevel=0.06, mirror=True)
    # upper wedge body: long glacis to a pylon block under the turret (crosses x = 0)
    b.hull([(x * sx, y, z) for sx in (-1, 1) for x, y, z in
            [(7.6, 6.8, -20.8), (7.6, 6.8, 19.0), (6.0, 6.2, 22.0),
             (6.8, 10.6, -19.6), (5.4, 11.0, 4.0), (4.4, 8.8, 18.0)]], 'paint', bevel=0.18)
    # team chevron on the glacis
    b.hull([(x * sx, y, z) for sx in (-1, 1) for x, y, z in
            [(0.0, 9.15, 16.4), (4.2, 8.98, 17.0), (4.6, 10.18, 10.6), (0.0, 10.58, 9.2)]] +
           [(0.0, 9.3, 16.4), (0.0, 10.72, 9.2)], 'team', bevel=0.03)
    # pylon: tapered block rising to just under the flak mount (turret origin y 19.5)
    b.hull([(x * sx, y, z) for sx in (-1, 1) for x, y, z in
            [(5.4, 10.4, -16.4), (5.4, 10.4, 0.0), (3.4, 17.0, -12.4), (3.4, 17.0, -3.6)]], 'paint2', bevel=0.16)
    b.cyl((0, 16.8, -8.0), (0, 17.5, -8.0), 3.6, 16, 'dark', bevel=0.05)
    b.box((5.0, 11.4, -12.0), (5.6, 13.0, -4.6), 'dark', bevel=0.03, mirror=True)
    # radar/targeting box at the rear deck
    b.box((-4.2, 10.6, -20.0), (4.2, 12.2, -16.6), 'dark', bevel=0.1)
    b.box((-3.6, 11.0, -16.62), (3.6, 11.8, -16.5), 'lightc', bevel=0.0)
    # headlights + rear lights
    b.box((-4.8, 5.4, 21.2), (4.8, 6.6, 21.9), 'dark', bevel=0.05)
    b.box((-4.4, 5.6, 21.88), (4.4, 6.4, 21.98), 'lightw', bevel=0.0)
    b.box((5.0, 4.4, -21.0), (6.6, 5.4, -20.8), 'lightr', bevel=0.0, mirror=True)
    # antenna, left rear fender
    b.cyl((-12.0, 9.2, -17.0), (-12.0, 9.9, -17.0), 0.32, 8, 'dark')
    b.cyl((-12.0, 9.9, -17.0), (-12.0, 15.4, -17.0), 0.09, 6, 'steel', r2=0.045)
    b.cyl((-12.0, 15.4, -17.0), (-12.0, 15.6, -17.0), 0.14, 6, 'lightc')

    # ---------------------------------------------------------------- turret (origin 0, 19.5, -8; turns y and x)
    t = k.piece('turret'); A = t.at
    t.cyl(A(0, -2.0, 0), A(0, 0.6, 0), 2.6, 14, 'dark', bevel=0.05)
    # central armoured cradle
    t.hull([A(x * sx, y, z) for sx in (-1, 1) for x, y, z in
            [(2.0, -1.8, -6.0), (2.0, 2.2, -6.0), (2.2, -1.8, 3.8), (2.0, 2.4, 3.6), (1.6, 0.0, 6.4)]], 'paint2', bevel=0.12)
    t.box(A(-1.5, 2.2, -5.0), A(1.5, 2.44, 2.4), 'team', bevel=0.03)
    # outer gun cheeks (house gun1/gun4 at x +-5, y -1.5)
    t.hull([A(x, y, z) for x in (3.6, 6.6) for y, z in
            [(-3.0, -4.6), (0.0, -4.6), (-3.0, 6.0), (-0.2, 5.6), (-1.6, 7.6)]], 'paint', bevel=0.12, mirror=True)
    t.box(A(4.0, -0.02, -3.6), A(6.2, 0.2, 4.0), 'team', bevel=0.03, mirror=True)
    # inner gun bridges (gun2/gun3 at x +-3, y 0.5)
    t.box(A(2.0, -0.6, 0.4), A(4.0, 1.6, 4.6), 'dark', bevel=0.08, mirror=True)
    # ammunition drums behind
    t.cyl(A(1.0, 0.4, -6.4), A(5.6, 0.4, -6.4), 1.6, 12, 'dark', bevel=0.05, mirror=True)
    # targeting optic on top
    t.box(A(-0.8, 2.4, -2.4), A(0.8, 3.4, 0.4), 'dark', bevel=0.06)
    t.box(A(-0.6, 2.6, 0.38), A(0.6, 3.2, 0.5), 'lightc', bevel=0.0)

    # ---------------------------------------------------------------- guns (recoil z)
    g = k.piece('gun1'); G = g.at
    g.cyl(G(0, 0.25, -1.0), G(0, 0.25, 13.4), 0.62, 10, 'steel')
    g.cyl(G(0, 0.25, 0.4), G(0, 0.25, 2.4), 0.95, 10, 'dark', bevel=0.04)
    g.cyl(G(0, 0.25, 12.6), G(0, 0.25, 14.8), 0.9, 8, 'dark', rot=math.pi / 8, bevel=0.05)
    g.cyl(G(0, 0.25, 14.78), G(0, 0.25, 14.86), 0.42, 8, 'black')
    for i in (2, 3, 4):
        k.clone(f'gun{i}', 'gun1')
