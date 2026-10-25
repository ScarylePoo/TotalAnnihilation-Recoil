"""Construction Vehicle (CORE_T1_VEH_Constructor) - Core T1 builder. Tall armoured box hull: a single centre track
under the nose (wheels1..3) and two wide side tracks under the rear (wheels4..7); roof bay closed by two doors.
Piece layout is the third-party remodel's (the COB drives it). On StartBuilding the doors swing open (turn z 60 deg),
the `lift` platform rises 12.5 elmo inside the bay, the `turret` column rises another 5.5 and turns, the `cradle`
elevates the nano head: `nano` (projector barrel, slides out 3.5) opens four petal panels (panel_t/b/l/r turn 60 deg)
around the emitter, `rear` (counterweight) slides back 3; `firepoint` (empty) is the nano emit point.
tracks1..4 are frame-cycled with tread..tread4; wheels hub discs spin x.
Value groups from above: dark warm hull walls, darker paint2 doors with wide team stripes (the spine), black tracks,
light steel side-track fenders and nose ram, light steel nano head + petals (construction gear reads light on Core).
Coordinates are ENGINE/global: X right, Y up, Z forward."""
import math

UNIT = dict(
    res=1024,
    wreck=dict(seed=13, remove=['tracks2', 'tracks3', 'tracks4'], pose={'door2': (0, 0, -30)}),
    preview_pose={'tracks2': 'hide', 'tracks3': 'hide', 'tracks4': 'hide'},
)

S_XI, S_XO = 10.0, 16.0          # side tracks


def tracks(k, name, mat):
    t = k.piece(name)
    t.prism(S_XI, S_XO, [(-18.0, 0.0), (6.4, 0.0), (8.4, 3.0), (7.4, 7.0), (-18.6, 7.0), (-19.9, 3.0)], mat, bevel=0.15, mirror=True)
    # centre nose track (crosses x = 0)
    t.prism(-3.0, 3.0, [(7.0, 0.0), (24.6, 0.0), (26.6, 3.2), (25.6, 7.0), (6.2, 7.0), (5.4, 3.2)], mat, bevel=0.15)


def build(k):
    for i, mat in enumerate(('tread', 'tread2', 'tread3', 'tread4'), 1):
        tracks(k, f'tracks{i}', mat)
    # centre track hubs (both faces), side track hubs (outer face)
    w = k.piece('wheels1'); W = w.at
    w.cyl(W(2.95, 0, 0), W(3.35, 0, 0), 2.5, 12, 'dark', bevel=0.04, mirror=True)
    w.cyl(W(3.35, 0, 0), W(3.55, 0, 0), 1.0, 8, 'steel', mirror=True)
    k.clone('wheels2', 'wheels1'); k.clone('wheels3', 'wheels1')
    w = k.piece('wheels4'); W = w.at
    w.cyl(W(S_XO - 0.05, 0, 0), W(S_XO + 0.35, 0, 0), 2.6, 12, 'dark', bevel=0.04, mirror=True)
    w.cyl(W(S_XO + 0.35, 0, 0), W(S_XO + 0.55, 0, 0), 1.05, 8, 'steel', mirror=True)
    for i in (5, 6, 7):
        k.clone(f'wheels{i}', 'wheels4')

    # ------------------------------------------------------------------ body
    b = k.piece('body')
    # chassis pan between the tracks
    b.prism(-10.0, 10.0, [(-24.4, 1.6), (4.6, 1.6), (5.6, 4.0), (5.6, 8.4), (-24.8, 8.4), (-25.4, 4.4)], 'paint2', bevel=0.15)
    b.prism(-3.4, 3.4, [(4.0, 7.0), (24.4, 7.0), (25.2, 8.8), (4.0, 8.8)], 'paint2', bevel=0.1)
    # fenders over the side tracks with team plates
    b.hull([(9.4, 8.6, -20.6), (16.8, 8.6, -20.6), (9.4, 8.6, 8.8), (16.8, 8.6, 8.8),
            (9.4, 7.0, -21.4), (16.8, 7.0, -21.4), (9.4, 7.0, 9.6), (16.8, 7.0, 9.6)], 'steel', bevel=0.12, mirror=True)
    # tall hull walls around the bay (inner face x 7.7 = door hinge), sloped outer faces
    b.hull([(7.7, 8.4, -25.0), (12.8, 8.4, -25.0), (7.7, 8.4, 19.0), (12.8, 8.4, 19.0),
            (7.7, 21.0, -23.6), (9.2, 21.0, -23.6), (7.7, 21.0, 15.4), (9.2, 21.0, 15.4)], 'paint', bevel=0.16, mirror=True)
    # front block (cab) and rear block, closing the bay
    b.hull([(x * sx, y, z) for sx in (-1, 1) for x, y, z in
            [(7.8, 8.4, 13.0), (7.8, 8.4, 24.4), (6.8, 11.4, 25.2), (7.8, 21.0, 13.0), (7.2, 18.6, 19.6)]], 'paint', bevel=0.16)
    b.hull([(x * sx, y, z) for sx in (-1, 1) for x, y, z in
            [(7.8, 8.4, -25.4), (7.8, 8.4, -20.6), (7.8, 21.0, -20.6), (7.4, 20.0, -24.0)]], 'paint', bevel=0.16)
    b.box((-7.7, 8.4, -20.6), (7.7, 9.6, 13.0), 'dark', bevel=0.0)      # bay floor
    # windscreen, hazard band across the cab front, headlights
    b.hull([(x * sx, y, z) for sx in (-1, 1) for x, y, z in
            [(4.8, 19.6, 18.1), (4.8, 20.4, 16.4), (4.8, 19.74, 18.16), (4.8, 20.54, 16.46)]], 'glass', bevel=0.03)
    # light steel nose plate over the centre track (construction ram)
    b.hull([(x * sx, y, z) for sx in (-1, 1) for x, y, z in
            [(6.6, 11.6, 25.18), (6.8, 14.4, 23.2), (6.6, 11.74, 25.32), (6.8, 14.54, 23.34)]], 'steel', bevel=0.04)
    b.box((4.0, 9.0, 24.4), (6.2, 10.4, 25.2), 'dark', bevel=0.06, mirror=True)
    b.box((4.2, 9.2, 25.18), (6.0, 10.2, 25.28), 'lightw', bevel=0.0, mirror=True)
    # rear: grille, tail lights, exhausts, beacon, antenna
    b.box((-5.6, 10.4, -25.9), (5.6, 17.0, -25.2), 'dark', bevel=0.06)
    for y in (11.0, 12.4, 13.8, 15.2):
        b.box((-5.2, y, -26.05), (5.2, y + 0.6, -25.8), 'black', bevel=0.0)
    b.box((6.2, 18.0, -24.9), (7.4, 18.8, -24.6), 'lightr', bevel=0.0, mirror=True)
    b.cyl((10.4, 12.0, -22.8), (10.4, 23.0, -22.8), 0.7, 10, 'dark', mirror=True)
    b.cyl((10.4, 23.0, -22.8), (10.4, 23.15, -22.8), 0.5, 10, 'black', mirror=True)
    b.cyl((8.4, 21.0, 17.0), (8.4, 21.8, 17.0), 0.9, 10, 'dark')
    b.cyl((8.4, 21.8, 17.0), (8.4, 22.6, 17.0), 0.62, 10, 'lightw')
    b.cyl((-8.4, 21.0, 17.0), (-8.4, 21.6, 17.0), 0.34, 8, 'dark')
    b.cyl((-8.4, 21.6, 17.0), (-8.4, 27.0, 17.0), 0.09, 6, 'steel', r2=0.045)
    b.cyl((-8.4, 27.0, 17.0), (-8.4, 27.2, 17.0), 0.14, 6, 'lightr')

    # ---------------------------------------------------------------- doors (door1 hinge x -7.74, y 20.97; door2 mirror)
    d = k.piece('door1'); D = d.at

    def ys(x):
        return 0.0 + 2.2 * x / 7.7
    d.hull([D(x, ys(x) + dy, z) for x in (0.05, 7.7) for z in (-20.6, 13.0) for dy in (0.0, -0.6)], 'paint2', bevel=0.08)
    d.hull([D(x, ys(x) + dy, z) for x in (2.2, 6.6) for z in (-17.0, 8.6) for dy in (0.07, 0.2)], 'team', bevel=0.03)
    d.cyl(D(0.0, -0.1, -20.0), D(0.0, -0.1, 12.4), 0.5, 8, 'dark')
    k.clone('door2', 'door1', mirror_x=True)

    # ---------------------------------------------------------------- lift (platform in the bay; origin 0,0,0)
    l = k.piece('lift')
    l.box((-6.9, 11.8, -18.9), (6.9, 13.0, 11.3), 'paint2', bevel=0.08)
    for z0 in (-18.6, 9.2):
        l.box((-6.6, 13.0, z0), (6.6, 13.14, z0 + 1.8), 'hazard', bevel=0.02)
    l.cyl((0, 8.1, -10.0), (0, 11.8, -10.0), 1.6, 10, 'steel', rot=math.pi / 10)        # ram

    # ---------------------------------------------------------------- turret column (origin 0, 17.5, -10)
    t = k.piece('turret'); A = t.at
    t.cyl(A(0, -4.5, 0), A(0, -3.9, 0), 3.4, 16, 'dark', bevel=0.05)
    t.cyl(A(0, -10.5, 0), A(0, -4.5, 0), 1.5, 10, 'steel', rot=math.pi / 10)
    t.cyl(A(0, -3.9, 0), A(0, -0.6, 0), 2.8, 8, 'paint', rot=math.pi / 8, bevel=0.1)
    t.hull([A(x * sx, y, 0) for sx in (-1, 1) for x, y in ((2.4, -0.6), (2.4, 0.6))] +
           [A(x * sx, y, z) for sx in (-1, 1) for x, y, z in ((2.4, -0.6, 1.4), (2.4, -0.6, -1.4))], 'dark', bevel=0.06)

    # ---------------------------------------------------------------- cradle (elevating yoke)
    c = k.piece('cradle'); C = c.at
    c.cyl(C(-3.0, 0, 0), C(3.0, 0, 0), 1.3, 12, 'dark', bevel=0.05)
    c.hull([C(x, y, z) for x in (2.0, 3.0) for y, z in ((-1.6, -2.0), (2.6, -2.0), (-1.2, 3.4), (2.6, 3.4))], 'paint2', bevel=0.08, mirror=True)
    c.box(C(-2.0, 2.0, -4.0), C(2.0, 4.4, 3.0), 'paint', bevel=0.12)
    c.box(C(-1.6, 4.4, -3.4), C(1.6, 4.58, 2.4), 'team', bevel=0.03)

    # ---------------------------------------------------------------- rear (counterweight; slides back)
    r = k.piece('rear'); Rr = r.at
    r.box(Rr(-1.7, 0.4, -4.4), Rr(1.7, 3.2, 0.6), 'dark', bevel=0.1)
    for z in (-3.6, -2.4, -1.2):
        r.box(Rr(-1.5, 3.2, z), Rr(1.5, 3.32, z + 0.6), 'black', bevel=0.0)

    # ---------------------------------------------------------------- nano head (barrel + 4 petals around the emitter)
    n = k.piece('nano'); N = n.at
    n.cyl(N(0, 2.0, 3.0), N(0, 2.0, 8.7), 1.8, 10, 'steel', rot=math.pi / 10)
    for z in (4.6, 6.6):
        n.cyl(N(0, 2.0, z), N(0, 2.0, z + 0.6), 2.15, 10, 'dark', rot=math.pi / 10)
    n.cyl(N(0, 2.0, 8.6), N(0, 2.0, 10.6), 1.0, 10, 'lightc', r2=0.5)       # emitter inside the petal cone
    # petals: closed they form a 4-sided pyramid nose (hinge edges at z 8.7, tip at the firepoint z 14.1); the
    # script swings each one 60 deg outward about its hinge to expose the emitter.
    L, H = 5.6, 0.32                      # petal length to near the tip, plate thickness
    pt = k.piece('panel_t'); T = pt.at
    pt.hull([T(-1.9, 0, 0), T(1.9, 0, 0), T(-1.9, H, 0), T(1.9, H, 0),
             T(-0.3, -1.4, L), T(0.3, -1.4, L), T(-0.3, -1.4 + H, L), T(0.3, -1.4 + H, L)], 'steel', bevel=0.05)
    pt.hull([T(-1.3, H + 0.02, 0.6), T(1.3, H + 0.02, 0.6), T(-1.3, H + 0.15, 0.6), T(1.3, H + 0.15, 0.6),
             T(-0.9, H - 0.25, 2.2), T(0.9, H - 0.25, 2.2), T(-0.9, H - 0.12, 2.2), T(0.9, H - 0.12, 2.2)], 'hazard', bevel=0.0)
    pb = k.piece('panel_b'); Bp = pb.at
    pb.hull([Bp(-1.9, 0, 0), Bp(1.9, 0, 0), Bp(-1.9, -H, 0), Bp(1.9, -H, 0),
             Bp(-0.3, 1.4, L), Bp(0.3, 1.4, L), Bp(-0.3, 1.4 - H, L), Bp(0.3, 1.4 - H, L)], 'steel', bevel=0.05)
    pr = k.piece('panel_r'); Rp = pr.at
    pr.hull([Rp(0, -1.2, 0), Rp(0, 1.2, 0), Rp(-H, -1.2, 0), Rp(-H, 1.2, 0),
             Rp(2.0, -0.3, L), Rp(2.0, 0.3, L), Rp(2.0 - H, -0.3, L), Rp(2.0 - H, 0.3, L)], 'steel', bevel=0.05)
    k.clone('panel_l', 'panel_r', mirror_x=True)
