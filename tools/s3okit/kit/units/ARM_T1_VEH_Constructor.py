"""Construction Vehicle (ARM_T1_VEH_Constructor) - Arm T1 builder. Tall trapezoid body on four separate track pods;
a roof bay closed by two sloped doors (door1/door2 turn z + drop). When building, the doors open, the `plate`
lift rises 11 elmo to deck level and the folding `arm` swings up 90 deg from the turret, then the `nano` lathe tilts
forward; `beam` (empty) is the nano emit point. Every piece keeps the TA origin; the bay is open-topped under the
doors so the folded arm + lathe fit inside.
Value groups from above: light Arm side walls, darker paint2 doors with wide team stripes (the spine), dark track
pods with light fenders + team plates; hazard plate edges and lathe tip read as construction gear when open.
Coordinates are ENGINE/global: X right, Y up, Z forward. mirror=True builds the -X twin sharing UVs."""
import math

UNIT = dict(
    res=1024,
    wreck=dict(seed=3, pose={'door1': (0, 0, -25), 'turret': (0, 30, 0)}),
    preview_pose={},
)


def build(k):
    b = k.piece('base')
    # ------------------------------------------------------------------ four track pods
    for z0, z1 in ((5.0, 23.5), (-23.5, -5.0)):
        zc = (z0 + z1) / 2; h = (z1 - z0) / 2
        belt = [(zc - h + 2.2, 0.0), (zc + h - 2.2, 0.0), (zc + h, 2.6), (zc + h - 0.6, 6.4),
                (zc - h + 0.6, 6.4), (zc - h, 2.6)]
        b.prism(15.6, 21.8, belt, 'tread', bevel=0.15, mirror=True)
        for z in (zc - h + 3.2, zc, zc + h - 3.2):
            b.cyl((21.8, 2.6, z), (22.2, 2.6, z), 1.6, 12, 'dark', mirror=True)
            b.cyl((22.2, 2.6, z), (22.4, 2.6, z), 0.65, 8, 'steel', mirror=True)
        # fender housing over the pod
        b.hull([(15.0, 6.2, z0 - 0.4), (22.6, 6.2, z0 - 0.4), (15.0, 6.2, z1 + 0.4), (22.6, 6.2, z1 + 0.4),
                (15.0, 9.6, z0 + 0.6), (22.4, 9.6, z0 + 0.6), (15.0, 9.6, z1 - 0.6), (22.4, 9.6, z1 - 0.6)],
               'paint', bevel=0.14, mirror=True)
        b.box((16.6, 9.6, z0 + 2.4), (21.0, 9.9, z1 - 2.4), 'dark', bevel=0.06, mirror=True)   # pod hatch
        # pivot boss joining the pod to the hull
        b.cyl((13.6, 5.0, zc), (15.2, 5.0, zc), 2.0, 12, 'dark', bevel=0.06, mirror=True)

    # ------------------------------------------------------------------ lower hull (crosses x = 0)
    b.prism(-15.0, 15.0, [(-23.0, 3.0), (22.0, 3.0), (24.4, 7.0), (23.4, 11.2), (-22.6, 11.2), (-24.0, 7.0)], 'paint2', bevel=0.15)
    # bay floor (seen when the plate is raised)
    b.box((-5.3, 11.1, -17.5), (5.3, 13.3, 15.0), 'dark', bevel=0.0)

    # ------------------------------------------------------------------ superstructure around the roof bay
    # side walls: trapezoid section, vertical inner face at x 5.3 (bay wall)
    b.hull([(5.3, 11.0, -20.0), (15.2, 11.0, -20.0), (5.3, 11.0, 18.0), (15.2, 11.0, 18.0),
            (5.3, 24.8, -17.5), (7.6, 24.8, -17.5), (5.3, 24.8, 15.0), (7.6, 24.8, 15.0)], 'paint', bevel=0.16, mirror=True)
    # nose block: sloped glacis in front of the bay
    b.hull([(x * sx, y, z) for sx in (-1, 1) for x, y, z in
            [(14.8, 11.0, 15.0), (14.0, 11.0, 23.0), (7.6, 24.8, 15.0), (7.0, 24.8, 16.6), (6.8, 13.0, 24.0)]], 'paint', bevel=0.16)
    # tail block
    b.hull([(x * sx, y, z) for sx in (-1, 1) for x, y, z in
            [(14.8, 11.0, -17.5), (14.0, 11.0, -22.6), (7.6, 24.8, -17.5), (7.0, 24.8, -19.0)]], 'paint', bevel=0.16)
    # top rails along the bay edge (paint2 strip separates doors from walls)
    b.box((5.3, 24.8, -17.5), (7.4, 25.1, 15.0), 'paint2', bevel=0.06, mirror=True)
    # shoulder detail
    nx, ny = 0.876, 0.482                     # outward normal of the shoulder slope (7.6,24.8)-(15.2,11.0)
    sl = [(7.6 + 7.6 * t, 24.8 - 13.8 * t) for t in (0.14, 0.72)]
    for z0, z1 in ((-14.5, -11.5), (-9.5, -6.5)):     # dark engine vents on the shoulders (rear half)
        b.hull([(x + nx * d, y + ny * d, z) for (x, y) in sl for z in (z0, z1) for d in (0.07, 0.25)],
               'dark', bevel=0.03, mirror=True)
    # cab windows
    b.hull([(x * sx, y, z) for sx in (-1, 1) for x, y, z in
            [(6.4, 20.4, 18.0), (6.0, 23.4, 16.2), (6.4, 20.52, 18.12), (6.0, 23.52, 16.32)]], 'glass', bevel=0.03)
    # headlights
    b.box((9.8, 11.6, 22.6), (12.6, 13.0, 23.6), 'dark', bevel=0.07, mirror=True)
    b.box((10.0, 11.8, 23.55), (12.4, 12.8, 23.65), 'lightw', bevel=0.0, mirror=True)
    # tail: exhaust grille, lights, amber work beacon on the right tail
    b.box((-6.0, 13.0, -21.4), (6.0, 19.0, -20.6), 'dark', bevel=0.06)
    for y in (13.6, 14.8, 16.0, 17.2):
        b.box((-5.6, y, -21.55), (5.6, y + 0.5, -21.3), 'black', bevel=0.0)
    b.box((9.0, 12.0, -22.9), (11.0, 12.9, -22.5), 'lightr', bevel=0.0, mirror=True)
    b.cyl((10.4, 21.6, -19.2), (10.4, 22.6, -19.2), 0.9, 10, 'dark', bevel=0.04)
    b.cyl((10.4, 22.6, -19.2), (10.4, 23.4, -19.2), 0.6, 10, 'lightw', bevel=0.0)
    # antenna, left rear
    b.cyl((-10.4, 21.6, -19.2), (-10.4, 22.3, -19.2), 0.34, 8, 'dark')
    b.cyl((-10.4, 22.3, -19.2), (-10.4, 28.5, -19.2), 0.09, 6, 'steel', r2=0.045)
    b.cyl((-10.4, 28.5, -19.2), (-10.4, 28.7, -19.2), 0.14, 6, 'lightc')

    # ---------------------------------------------------------------- doors (door1 hinge at x -5.3; door2 = mirror)
    dr = k.piece('door1'); D = dr.at

    def ys(x):       # door top surface: rises from the hinge to the centre ridge
        return 0.05 + 1.6 * (x - 0.1) / 5.15
    dr.hull([D(x, ys(x) + dy, z) for x in (0.1, 5.25) for z in (-17.4, 14.9) for dy in (0.0, -0.55)], 'paint2', bevel=0.08)
    dr.hull([D(x, ys(x) + dy, z) for x in (1.1, 4.6) for z in (-15.4, 12.8) for dy in (0.07, 0.2)], 'team', bevel=0.03)
    dr.cyl(D(0.0, -0.05, -17.0), D(0.0, -0.05, 14.5), 0.45, 8, 'dark')       # hinge pin
    k.clone('door2', 'door1', mirror_x=True)

    # ---------------------------------------------------------------- plate (lift platform, rises to the deck)
    p = k.piece('plate'); Pp = p.at
    p.box(Pp(-5.15, -0.9, -17.3), Pp(5.15, 0.0, 14.8), 'paint2', bevel=0.08)
    for z0, z1 in ((12.6, 14.6), (-17.1, -15.1)):
        p.box(Pp(-4.9, 0.0, z0), Pp(4.9, 0.14, z1), 'hazard', bevel=0.02)
    for z in (-11.0, -6.0, -1.0):
        p.box(Pp(-4.0, 0.0, z), Pp(4.0, 0.12, z + 0.8), 'dark', bevel=0.0)

    # ---------------------------------------------------------------- turret (swivel on the plate)
    t = k.piece('turret'); A = t.at
    t.cyl(A(0, 0.0, 0), A(0, 0.6, 0), 3.4, 16, 'dark', bevel=0.06)
    t.cyl(A(0, 0.6, 0), A(0, 2.9, 0), 2.8, 8, 'paint', rot=math.pi / 8, bevel=0.1)
    t.cyl(A(0, 2.9, 0), A(0, 3.05, 0), 2.2, 8, 'team', rot=math.pi / 8)

    # ---------------------------------------------------------------- arm (hinge at the turret top; stowed along -z)
    a = k.piece('arm'); R = a.at
    a.cyl(R(-1.9, 0, 0), R(1.9, 0, 0), 1.3, 12, 'dark', bevel=0.05)
    a.hull([R(x, y, z) for x in (-1.5, 1.6) for y, z in [(-1.2, 0.6), (1.6, 0.6), (-1.3, -15.6), (1.5, -15.6)]], 'paint', bevel=0.12)
    a.hull([R(x, y, z) for x in (-1.45, 1.55) for y, z in [(1.55, -1.6), (1.75, -1.6), (1.55, -4.6), (1.75, -4.6)]], 'hazard', bevel=0.02)
    a.cyl(R(1.8, -0.6, -1.8), R(1.8, -0.2, -12.5), 0.45, 8, 'steel')   # hydraulic ram
    a.cyl(R(1.8, -0.6, -1.8), R(1.8, -0.55, -6.0), 0.62, 8, 'dark')
    a.hull([R(x, y, z) for x in (-1.3, 1.4) for y, z in [(-1.2, -15.0), (1.4, -15.0), (-0.9, -17.9), (1.0, -17.9)]], 'dark', bevel=0.08)

    # ---------------------------------------------------------------- nano lathe (beam emit at 0.47, 4.65, 13.03)
    n = k.piece('nano'); N = n.at
    n.cyl(N(-2.2, 0, 0), N(2.6, 0, 0), 1.15, 12, 'dark', bevel=0.05)
    n.hull([N(x, y, z) for x in (-2.0, 2.9) for y, z in [(-0.6, -2.6), (-0.6, 2.0), (5.6, -3.4), (5.6, 1.6), (2.0, -5.2), (4.6, -5.2)]],
           'paint2', bevel=0.12)
    n.box(N(-1.7, 5.6, -2.6), N(2.6, 5.76, 0.8), 'hazard', bevel=0.02)
    # projector: tapered barrel with emitter coils, cyan tip at the beam point
    bx, by = 0.47, 4.65
    n.cyl(N(bx, by - 0.4, 0.8), N(bx, by, 11.9), 1.3, 10, 'dark', r2=0.75, rot=math.pi / 10)
    for z in (3.4, 5.6, 7.8):
        n.cyl(N(bx, by - 0.25, z), N(bx, by - 0.22, z + 0.8), 1.45, 10, 'steel', rot=math.pi / 10)
    n.cyl(N(bx, by, 11.8), N(bx, by, 12.95), 0.95, 10, 'lightc', r2=0.55)
