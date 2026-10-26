"""Skimmer (ARM_T1_HOV_Skimmer) - Arm scout hovercraft. Catamaran: two long kite-shaped pontoons on black skirts with
an open water gap between them, a slim needle fuselage down the middle carrying a tiny laser turret, twin swept
tail fins and one big vertical pusher propeller in a ring at the stern (the scout's signature from above).
Pieces (TA 3DO, COB drives them): GP (empty ground plate), Base (rocks x/z), Turret (turn y + x), Flare (empty),
Wake1..8 (empty emit points).
Value groups from above: black skirts as two rails, light Arm pontoon decks, dark-blue paint2 fuselage with a team
spine stripe, team fin tops, dark prop ring with light blades.
Coordinates are ENGINE/global: X right, Y up, Z forward. mirror=True builds the -X twin sharing UVs."""
import math

UNIT = dict(
    res=1024,
    wreck=dict(seed=9, pose={'Turret': (0, 50, 0)}),
    preview_pose={'Turret': (0, -25, 0)},
)

KITE = [(4.3, -20.5), (9.4, -15.8), (12.4, -6.0), (17.1, 0.0), (13.7, 11.5), (4.3, 20.5)]


def kite(y, grow=0.0, shrink=0.0):
    cx = 10.0
    out = []
    for x, z in KITE:
        dx, dz = x - cx, z
        L = math.hypot(dx, dz) or 1
        s = grow - shrink
        out.append((x + dx / L * s, y, z + dz / L * s))
    return out


def build(k):
    b = k.piece('Base')
    # ------------------------------------------------------------------ pontoons (+X built, mirrored)
    b.hull(kite(1.0, 0.4) + kite(4.0, 2.2) + kite(7.2, 1.8) + kite(8.6, 0.8), 'tread', bevel=0.25, mirror=True)
    b.hull(kite(8.2, -0.6) + kite(11.0, -0.6) + kite(15.1, -2.0), 'paint', bevel=0.2, mirror=True)
    b.hull(kite(8.4, -0.3) + kite(9.8, -0.3), 'paint2', bevel=0.08, mirror=True)
    # lift fan in each pontoon, aft
    x, z = 9.4, -7.6
    b.cyl((x, 14.2, z), (x, 15.4, z), 3.6, 14, 'dark', bevel=0.1, mirror=True)
    b.cyl((x, 15.4, z), (x, 15.45, z), 2.8, 14, 'black', mirror=True)
    for i in range(3):
        a = i * 2 * math.pi / 3 + 0.2
        ca, sa = math.cos(a), math.sin(a)
        pts = []
        for d in (0.7, 2.6):
            for s in (-0.5, 0.5):
                px, pz = x + ca * d - sa * s, z + sa * d + ca * s
                pts += [(px, 15.15, pz), (px, 15.45, pz)]
        b.hull(pts, 'steel', bevel=0.0, mirror=True)
    # sensor bulge + headlight at each pontoon bow
    b.hull([(6.4, 13.0, 15.6), (9.6, 13.0, 13.4), (6.0, 15.0, 13.0), (8.8, 15.0, 11.6), (6.4, 11.0, 17.4), (9.6, 11.0, 15.0)],
           'dark', bevel=0.1, mirror=True)
    b.box((6.8, 11.4, 17.0), (8.6, 12.4, 17.4), 'lightw', bevel=0.0, mirror=True)
    # cross beams joining the pontoons to the fuselage (dark)
    b.box((2.4, 11.6, -12.0), (5.8, 13.6, -8.6), 'dark', bevel=0.1, mirror=True)
    b.box((2.4, 11.6, 4.0), (5.8, 13.6, 7.0), 'dark', bevel=0.1, mirror=True)
    # ------------------------------------------------------------------ needle fuselage (crosses x = 0)
    b.hull([(x * sx, y, z) for sx in (-1, 1) for x, y, z in
            [(3.0, 11.0, -14.6), (3.2, 11.0, 4.0), (1.6, 11.2, 16.4), (0.6, 12.6, 19.4),
             (3.0, 18.1, -11.0), (3.0, 18.1, 3.3), (1.5, 17.0, 10.0), (0.8, 15.0, 15.0)]], 'paint2', bevel=0.2)
    b.hull([(x * sx, y, z) for sx in (-1, 1) for x, y, z in
            [(1.8, 18.0, -11.0), (1.8, 18.0, 1.9), (1.2, 20.0, -9.0), (1.2, 20.0, 1.0)]], 'paint', bevel=0.14)
    # team spine stripe on the fuselage nose
    b.hull([(x * sx, y, z) for sx in (-1, 1) for x, y, z in
            [(1.2, 17.2, 9.6), (1.95, 18.18, 3.2), (0.6, 15.3, 14.6),
             (1.2, 17.34, 9.62), (1.95, 18.32, 3.22), (0.6, 15.44, 14.62)]], 'team', bevel=0.03)
    # canopy
    b.hull([(x * sx, y, z) for sx in (-1, 1) for x, y, z in
            [(1.5, 18.1, 3.4), (1.2, 17.3, 7.4), (1.0, 19.2, 2.4), (0.6, 18.4, 5.6)]], 'glass', bevel=0.06)
    # twin swept tail fins with team tops
    b.hull([(1.6, 18.0, -13.8), (2.4, 18.0, -8.6), (7.2, 22.0, -12.0), (7.6, 22.0, -9.6),
            (1.6, 18.6, -13.8), (2.2, 18.6, -8.6), (7.2, 22.6, -12.0), (7.6, 22.6, -9.6)], 'paint', bevel=0.08, mirror=True)
    b.hull([(5.4, 21.2, -11.6), (5.8, 21.2, -9.4), (7.6, 22.6, -12.1), (7.9, 22.6, -9.5),
            (5.4, 21.5, -11.6), (5.8, 21.5, -9.4), (7.6, 22.95, -12.1), (7.9, 22.95, -9.5)], 'team', bevel=0.03, mirror=True)
    # ------------------------------------------------------------------ stern pusher prop in a ring
    pz = -17.2
    b.box((-1.2, 11.4, -16.0), (1.2, 14.0, -13.6), 'dark', bevel=0.08)
    b.cyl((0, 15.2, pz - 1.6), (0, 15.2, pz + 1.6), 6.8, 18, 'dark', bevel=0.12)
    b.cyl((0, 15.2, pz - 1.65), (0, 15.2, pz - 1.6), 5.8, 18, 'black')
    b.cyl((0, 15.2, pz + 1.6), (0, 15.2, pz + 1.65), 5.8, 18, 'black')
    for i in range(4):
        a = i * math.pi / 2 + 0.4
        ca, sa = math.cos(a), math.sin(a)
        pts = []
        for d in (0.9, 5.5):
            for s in (-0.75, 0.75):
                px, py = ca * d - sa * s, 15.2 + sa * d + ca * s
                pts += [(px, py, pz - 1.9), (px, py, pz - 1.6)]
        b.hull(pts, 'steel', bevel=0.0)
    b.cyl((0, 15.2, pz - 2.6), (0, 15.2, pz - 1.6), 1.2, 10, 'paint', r2=0.5)
    b.box((-6.1, 21.2, pz - 0.8), (6.1, 22.3, pz + 0.8), 'paint', bevel=0.08)
    b.box((-0.6, 21.9, pz - 0.6), (0.6, 22.6, pz + 0.6), 'lightr', bevel=0.0)
    # long whip antenna (scout tell), left
    b.cyl((-1.4, 20.0, -6.0), (-1.4, 20.8, -6.0), 0.3, 8, 'dark')
    b.cyl((-1.4, 20.8, -6.0), (-1.4, 29.0, -6.0), 0.09, 6, 'steel', r2=0.04)
    b.cyl((-1.4, 29.0, -6.0), (-1.4, 29.2, -6.0), 0.14, 6, 'lightc')

    # ---------------------------------------------------------------- Turret (origin 0, 20.07, -2.61): laser
    t = k.piece('Turret'); A = t.at
    t.cyl(A(0, -0.1, -1.2), A(0, 0.5, -1.2), 2.0, 12, 'dark', bevel=0.05)
    t.hull([A(x * sx, y, z) for sx in (-1, 1) for x, y, z in
            [(1.7, 0.4, -3.4), (1.7, 0.4, 1.4), (1.2, 2.5, -2.8), (1.1, 2.5, 0.8)]], 'paint', bevel=0.12)
    t.box(A(-0.9, 2.45, -2.4), A(0.9, 2.6, 0.4), 'team', bevel=0.02)
    t.cyl(A(0, 1.14, 1.0), A(0, 1.14, 8.8), 0.45, 10, 'steel')
    t.cyl(A(0, 1.14, 2.0), A(0, 1.14, 4.0), 0.75, 10, 'dark', bevel=0.03)
    t.cyl(A(0, 1.14, 8.6), A(0, 1.14, 9.2), 0.62, 10, 'dark')
    t.cyl(A(0, 1.14, 9.18), A(0, 1.14, 9.24), 0.3, 10, 'lightr')
