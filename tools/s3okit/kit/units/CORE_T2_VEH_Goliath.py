"""Goliath (CORE_T2_VEH_Goliath) - Core very heavy assault tank, the biggest tank of the family. A massive tall hull
on very wide tracks with stepped armour sponsons, and a huge low turret set back carrying ONE enormous short cannon
in a bulbous mantlet (TA's Goliath: the fat gun is the tell). Piece layout is the third-party S3O's (the COB drives
it): body, turret1 (turn y), sleeve1 (turn x), barrel1 (recoil move z -5), firepoint1 (emit), tracks1..3 (shown one
at a time: a 3-frame cycle, so UNIT tread_step = 1/3), wheels1..6 (hub discs, spin x, both sides in one piece).
turret2/sleeve2/gun2 are not driven by the script (turret2 is a child of body standing on turret1's axis), so turret2
is a rotationally symmetric sensor cupola on that axis (looks right at any turret1 angle); sleeve2/gun2 stay empty.
Value groups from above: dark warm armour, darker paint2 sponson steps, black treads, the huge light-steel cannon and
mantlet ring against the dark hull, team colour in a broad saddle across the turret roof and on the sponson steps,
ochre hazard only on the glacis bumper.
Coordinates are ENGINE/global: X right, Y up, Z forward."""
import math

UNIT = dict(
    tread_step=1 / 3,
    wreck=dict(seed=43, drop=['barrel1'], remove=['tracks2', 'tracks3'], pose={'turret1': (0, -30, 0), 'sleeve1': (8, 0, 0)}),
    preview_pose={'turret1': (0, -18, 0), 'tracks2': 'hide', 'tracks3': 'hide'},
)
XI, XO = 14.6, 24.0


def tracks(k, name, mat):
    t = k.piece(name)
    belt = [(-22.6, 0.0), (20.4, 0.0), (23.4, 3.0), (22.6, 7.2), (-23.6, 7.2), (-25.6, 3.4)]
    t.prism(XI, XO, belt, mat, bevel=0.18, mirror=True)


def build(k):
    for i, mat in enumerate(('tread', 'tread2', 'tread3'), 1):
        tracks(k, f'tracks{i}', mat)
    for i in (1, 2):
        w = k.piece(f'wheels{i}'); W = w.at
        r = 3.6 if i == 1 else 2.6
        w.cyl(W(XO - 0.05, 0, 0), W(XO + 0.4, 0, 0), r, 14, 'dark', bevel=0.06, mirror=True)
        w.cyl(W(XO + 0.4, 0, 0), W(XO + 0.65, 0, 0), r * 0.4, 8, 'steel', mirror=True)
        for a in range(4):          # bolts: make the spin visible
            ang = a * math.pi / 2
            w.cyl(W(XO + 0.4, r * 0.68 * math.sin(ang), r * 0.68 * math.cos(ang)),
                  W(XO + 0.6, r * 0.68 * math.sin(ang), r * 0.68 * math.cos(ang)), 0.32, 6, 'black', mirror=True)
    k.clone('wheels6', 'wheels1')
    for i in (3, 4, 5):
        k.clone(f'wheels{i}', 'wheels2')

    # ------------------------------------------------------------------ body
    b = k.piece('body')
    b.prism(-14.8, 14.8, [(-25.6, 3.0), (23.4, 3.0), (26.6, 6.6), (25.6, 10.4), (-25.2, 10.4), (-27.4, 6.4)], 'paint2', bevel=0.2)
    # stepped sponsons over the tracks: lower wide step, upper narrower step
    b.hull([(14.2, 10.6, -26.6), (24.8, 10.6, -26.0), (24.8, 10.6, 21.6), (14.2, 10.6, 23.6),
            (14.2, 7.8, 28.6), (24.0, 7.6, 26.6), (14.2, 8.0, -28.6), (24.0, 7.8, -27.6),
            (14.2, 7.2, -26.6), (25.4, 7.2, -26.0), (25.4, 7.2, 22.0), (14.2, 7.2, 24.0)], 'paint2', bevel=0.18, mirror=True)
    b.hull([(14.0, 14.0, -24.6), (20.6, 14.0, -24.0), (20.6, 14.0, 14.6), (14.0, 14.0, 17.0),
            (14.0, 10.5, -26.0), (21.4, 10.5, -25.4), (21.4, 10.5, 20.0), (14.0, 10.5, 22.6)], 'paint', bevel=0.18, mirror=True)
    # team plates on the lower sponson steps
    b.box((21.0, 10.6, 4.6), (24.2, 10.82, 12.6), 'team', bevel=0.05, mirror=True)
    b.box((21.0, 10.6, -20.6), (24.2, 10.82, 2.6), 'dark', bevel=0.05, mirror=True)
    # spiked armour skirts (Core teeth) on the outer sponson edge
    for z in (-20.0, -12.0, -4.0, 4.0, 12.0):
        b.hull([(24.9, 10.4, z - 2.8), (24.9, 10.4, z + 2.8), (24.9, 7.6, z - 2.2), (24.9, 7.6, z + 2.2),
                (25.9, 9.2, z)], 'dark', bevel=0.06, mirror=True)
    # upper hull: tall armoured block with a long sloped glacis
    b.hull([(x * sx, y, z) for sx in (-1, 1) for x, y, z in
            [(14.6, 10.4, -27.4), (14.6, 10.4, 24.6), (12.8, 9.4, 28.8),
             (13.2, 21.4, -25.8), (13.2, 21.4, 4.0), (10.6, 15.6, 22.6)]], 'paint', bevel=0.22)
    # ochre bumper bar across the nose
    b.box((-12.4, 8.2, 28.0), (12.4, 10.0, 29.6), 'hazard', bevel=0.1)
    # glacis: dark armour bands (break the long slope into steps from above)
    for t0 in (0.18, 0.55):
        z0 = 22.6 - (22.6 - 4.0) * t0; z1 = z0 - 3.0
        y0 = 15.6 + (21.4 - 15.6) * t0; y1 = 15.6 + (21.4 - 15.6) * (t0 + 3.0 / 18.6)
        b.hull([(x * sx, y, z) for sx in (-1, 1) for x, y, z in
                [(9.6, y0 + 0.05, z0), (9.6, y1 + 0.05, z1), (9.6, y0 + 0.4, z0), (9.6, y1 + 0.4, z1)]], 'paint2', bevel=0.06)
    # driver's vision slits + headlights
    b.box((-6.0, 17.2, 17.0), (-2.0, 18.3, 18.4), 'dark', bevel=0.06)
    b.box((-5.7, 17.45, 18.35), (-2.3, 18.0, 18.5), 'lightc', bevel=0.0)
    b.box((8.6, 9.4, 27.2), (12.0, 11.0, 28.0), 'dark', bevel=0.06, mirror=True)
    b.box((8.9, 9.6, 27.95), (11.7, 10.8, 28.05), 'lightw', bevel=0.0, mirror=True)
    # turret ring
    b.cyl((0, 20.9, -9.8), (0, 21.7, -9.8), 11.4, 24, 'dark', bevel=0.08)
    # engine deck: big grille + twin exhaust stacks
    b.box((-9.4, 21.4, -25.0), (9.4, 22.4, -20.4), 'dark', bevel=0.1)
    for z in (-24.4, -23.2, -22.0, -20.8):
        b.box((-9.0, 22.4, z), (9.0, 22.55, z + 0.6), 'black', bevel=0.0)
    b.cyl((11.4, 19.0, -26.4), (11.4, 24.6, -27.0), 1.2, 12, 'dark', bevel=0.06, mirror=True)
    b.cyl((11.4, 24.6, -27.0), (11.4, 24.8, -27.05), 0.85, 12, 'black', mirror=True)
    # rear plate + tail lights
    b.box((-12.6, 11.0, -27.9), (12.6, 19.4, -27.2), 'paint2', bevel=0.08)
    b.box((10.0, 16.8, -28.0), (11.8, 17.8, -27.85), 'lightr', bevel=0.0, mirror=True)
    # antenna, rear left sponson
    b.cyl((-17.4, 14.0, -22.4), (-17.4, 14.8, -22.4), 0.42, 8, 'dark')
    b.cyl((-17.4, 14.8, -22.4), (-17.4, 23.0, -22.4), 0.11, 6, 'steel', r2=0.05)
    b.cyl((-17.4, 23.0, -22.4), (-17.4, 23.2, -22.4), 0.18, 6, 'lightr')

    # ---------------------------------------------------------------- turret1 (origin 0, 21.51, -9.81; turns y)
    t = k.piece('turret1'); A = t.at
    t.hull([A(x * sx, y, z) for sx in (-1, 1) for x, y, z in
            [(11.0, 0.2, -11.0), (12.4, 0.2, -3.0), (11.4, 0.2, 4.6), (7.6, 0.2, 8.0),
             (9.6, 7.4, -10.2), (10.6, 7.4, -3.0), (9.4, 7.4, 3.2), (6.4, 7.4, 5.6),
             (7.4, 9.6, -8.6), (8.0, 9.6, -3.0), (6.6, 9.6, 1.8)]], 'paint', bevel=0.22)
    # team roof plate: the whole flat top of the turret (the Goliath's main team read)
    t.hull([A(x * sx, y, z) for sx in (-1, 1) for x, y, z in
            [(6.8, 9.58, -7.8), (7.4, 9.58, -3.0), (6.0, 9.58, 1.2),
             (6.8, 9.74, -7.8), (7.4, 9.74, -3.0), (6.0, 9.74, 1.2)]], 'team', bevel=0.04)
    # cheek armour blocks (paint2) either side of the mantlet
    t.hull([A(x, y, z) for x in (5.6, 11.2) for y, z in
            [(0.6, 2.6), (6.6, 2.6), (0.6, 7.4), (5.4, 6.0)]], 'paint2', bevel=0.14, mirror=True)
    # bustle with ammo racks
    t.hull([A(x * sx, y, z) for sx in (-1, 1) for x, y, z in
            [(9.4, 1.0, -10.6), (9.0, 6.8, -10.0), (8.4, 1.4, -14.0), (8.0, 6.0, -13.6)]], 'paint2', bevel=0.14)
    for x in (-6.0, -2.0, 2.0, 6.0):
        t.box(A(x - 1.4, 6.3, -13.4), A(x + 1.4, 6.9, -10.8), 'dark', bevel=0.06)
    # periscopes
    t.box(A(-6.6, 9.7, 0.2), A(-4.6, 10.5, 1.4), 'dark', bevel=0.05)
    t.box(A(-6.4, 9.75, 1.38), A(-4.8, 10.2, 1.5), 'lightc', bevel=0.0)

    # ---------------------------------------------------------------- turret2: sensor cupola on the turret axis
    c = k.piece('turret2'); C = c.at
    c.cyl(C(0, -1.4, 0), C(0, 2.6, 0), 2.6, 16, 'paint2', bevel=0.1)
    c.cyl(C(0, 2.6, 0), C(0, 3.6, 0), 1.8, 16, 'dark', r2=1.4, bevel=0.06)
    c.cyl(C(0, 3.6, 0), C(0, 4.1, 0), 1.0, 12, 'lightr', r2=0.6)

    # ---------------------------------------------------------------- sleeve1 (origin y 24.64; turns x)
    s = k.piece('sleeve1'); S = s.at
    s.cyl(S(-5.6, 0, 0), S(5.6, 0, 0), 4.6, 16, 'dark', bevel=0.12)            # trunnion drum
    s.hull([S(x * sx, y, z) for sx in (-1, 1) for x, y, z in
            [(5.0, -4.2, 1.0), (5.0, 4.2, 1.0), (4.6, -3.6, 9.0), (4.6, 3.6, 9.0), (3.4, -2.8, 13.0), (3.4, 2.8, 13.0)]],
           'paint2', bevel=0.18)
    s.cyl(S(0, 0, 12.6), S(0, 0, 13.8), 3.4, 16, 'steel', bevel=0.08)           # mantlet collar ring (light)
    s.box(S(-3.0, 3.9, 2.0), S(3.0, 4.3, 8.0), 'team', bevel=0.05)

    # ---------------------------------------------------------------- barrel1 (recoils 5; firepoint at +4.66)
    br = k.piece('barrel1'); B = br.at
    br.cyl(B(0, 0, -4.6), B(0, 0, 4.8), 2.3, 14, 'steel')
    br.cyl(B(0, 0, -0.6), B(0, 0, 0.4), 2.7, 14, 'dark', bevel=0.06)
    br.cyl(B(0, 0, 4.4), B(0, 0, 8.0), 3.1, 8, 'steel', rot=math.pi / 8, bevel=0.1)     # huge muzzle brake
    br.cyl(B(0, 0, 7.98), B(0, 0, 8.08), 1.5, 8, 'black')
    for sx in (-1, 1):
        br.box(B(2.7 * sx, -0.9, 4.9), B(3.25 * sx, 0.9, 5.9), 'black', bevel=0.0)
        br.box(B(2.7 * sx, -0.9, 6.3), B(3.25 * sx, 0.9, 7.3), 'black', bevel=0.0)
