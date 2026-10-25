"""Raider (CORE_T1_VEH_Raider) - Core medium assault tank. Broad slab hull with angular fender skirts over wide tracks,
a squat faceted turret centred aft with a heavy short cannon (Core: light steel gun on dark armour).
Piece layout is the third-party remodel's (the COB drives it): base (empty), body, turret (turn y), sleeve (turn x),
barrel (recoil move z), firepoint (emit), tracks1..4 (shown one at a time; identical shapes, link pattern advanced a
quarter link per frame via tread..tread4), wheels1..5 (spin x): hub discs on the outer track faces, seen through
the skirt gap.
Value groups from above: dark warm armour (paint), darker paint2 lower hull/skirts/mantlet, black tracks, team plates
on the fender tops + turret roof, light steel barrel, ochre hazard glacis wedge.
Coordinates are ENGINE/global: X right, Y up, Z forward."""
import math

UNIT = dict(
    res=1024,
    wreck=dict(seed=8, drop=['barrel'], remove=['tracks2', 'tracks3', 'tracks4'], pose={'turret': (0, -40, 0)}),
    preview_pose={'turret': (0, -20, 0), 'tracks2': 'hide', 'tracks3': 'hide', 'tracks4': 'hide'},
)

XI, XO = 9.0, 15.5


def tracks(k, name, mat):
    t = k.piece(name)
    belt = [(-11.4, 0.0), (7.6, 0.0), (10.6, 2.4), (9.8, 5.6), (-12.6, 5.6), (-14.2, 2.6)]
    t.prism(XI, XO, belt, mat, bevel=0.15, mirror=True)


def build(k):
    for i, mat in enumerate(('tread', 'tread2', 'tread3', 'tread4'), 1):
        tracks(k, f'tracks{i}', mat)
    # wheels: hub caps on the outer track face (wheels1 / wheels5 = big sprocket / idler, 2-4 small road wheels)
    for i in (1, 2):
        w = k.piece(f'wheels{i}'); W = w.at
        r = 2.4 if i in (1, 5) else 1.45
        w.cyl(W(XO - 0.05, 0, 0), W(XO + 0.35, 0, 0), r, 12, 'dark', bevel=0.05, mirror=True)
        w.cyl(W(XO + 0.35, 0, 0), W(XO + 0.55, 0, 0), r * 0.45, 8, 'steel', mirror=True)
        if i in (1, 5):
            for a in range(4):
                an = a * math.pi / 2 + math.pi / 4
                w.box(W(XO + 0.35, 1.2 * math.cos(an) - 0.25, 1.2 * math.sin(an) - 0.25),
                      W(XO + 0.5, 1.2 * math.cos(an) + 0.25, 1.2 * math.sin(an) + 0.25), 'black', bevel=0.0, mirror=True)
    k.clone('wheels5', 'wheels1')
    k.clone('wheels3', 'wheels2')
    k.clone('wheels4', 'wheels2')

    # ------------------------------------------------------------------ body
    b = k.piece('body')
    # lower hull between the tracks (crosses x = 0)
    b.prism(-9.1, 9.1, [(-14.6, 2.7), (12.8, 2.7), (15.6, 5.0), (15.0, 7.0), (-15.0, 7.0), (-15.7, 4.6)], 'paint2', bevel=0.15)
    # fenders: wide flat slabs over the tracks, chisel nose
    b.hull([(8.4, 7.4, -15.4), (15.9, 7.4, -15.0), (15.9, 7.4, 10.8), (8.4, 7.4, 12.2),
            (8.4, 5.8, 15.8), (14.4, 5.8, 14.4),
            (8.4, 5.6, -15.6), (16.0, 5.6, -15.2), (16.0, 5.6, 11.0), (8.4, 5.6, 12.4), (8.4, 4.9, 16.0), (14.4, 4.9, 14.6)],
           'paint', bevel=0.14, mirror=True)
    # angular side skirt below the fender, leaves a slot for the wheel hubs
    b.hull([(15.6, 5.7, -14.4), (16.4, 6.8, -13.8), (16.4, 6.8, 9.8), (15.6, 5.7, 10.6),
            (15.4, 4.4, -13.0), (16.0, 5.2, -12.6), (16.0, 5.2, 8.6), (15.4, 4.4, 9.2)], 'paint2', bevel=0.1, mirror=True)
    # team plates on the fender tops
    b.hull([(9.6, 7.42, -13.8), (14.8, 7.42, -13.5), (14.8, 7.42, 9.6), (9.6, 7.42, 10.6),
            (9.65, 7.56, -13.7), (14.75, 7.56, -13.4), (14.75, 7.56, 9.5), (9.65, 7.56, 10.5)], 'team', bevel=0.04, mirror=True)
    # spiked hazard caps on the fender noses (Core spikiness)
    b.hull([(9.0, 5.0, 15.6), (13.8, 5.0, 14.4), (9.0, 7.42, 12.0), (14.8, 7.42, 10.8),
            (9.0, 5.12, 15.55), (13.8, 5.12, 14.35), (9.0, 7.56, 11.95), (14.8, 7.56, 10.75)], 'hazard', bevel=0.03, mirror=True)
    # upper hull: wedge rising to the turret deck at y 10 (crosses x = 0)
    b.hull([(x * sx, y, z) for sx in (-1, 1) for x, y, z in
            [(8.6, 7.0, -15.4), (8.6, 7.0, 12.6), (7.0, 6.6, 15.8),
             (7.4, 10.0, -14.6), (7.4, 10.0, 2.4), (5.0, 8.6, 11.6)]], 'paint', bevel=0.16)
    # glacis hazard wedge
    b.hull([(x * sx, y, z) for sx in (-1, 1) for x, y, z in
            [(4.8, 6.95, 15.2), (3.8, 8.5, 12.1), (4.8, 7.07, 15.32), (3.8, 8.62, 12.22)]], 'hazard', bevel=0.03)
    # headlights in dark housings
    b.box((5.4, 6.0, 15.2), (7.2, 6.9, 16.1), 'dark', bevel=0.07, mirror=True)
    b.box((5.6, 6.15, 16.08), (7.0, 6.75, 16.18), 'lightw', bevel=0.0, mirror=True)
    # rear engine deck: dark louvres, twin exhaust stacks
    b.box((-5.6, 9.6, -14.6), (5.6, 10.6, -10.8), 'dark', bevel=0.1)
    for z in (-14.0, -13.1, -12.2, -11.3):
        b.box((-5.1, 10.6, z), (5.1, 10.75, z + 0.45), 'black', bevel=0.0)
    b.cyl((6.6, 9.6, -14.6), (6.6, 12.2, -15.2), 0.65, 10, 'dark', bevel=0.04, mirror=True)
    b.cyl((6.6, 12.2, -15.2), (6.6, 12.35, -15.25), 0.46, 10, 'black', mirror=True)
    b.box((-6.0, 7.2, -15.75), (6.0, 9.6, -15.25), 'paint2', bevel=0.06)
    b.box((4.4, 8.2, -15.85), (5.6, 8.8, -15.7), 'lightr', bevel=0.0, mirror=True)
    # left-front hatch + antenna
    b.cyl((-3.4, 9.3, 6.2), (-3.4, 9.7, 6.2), 1.3, 14, 'paint2', bevel=0.05)
    b.box((-4.0, 9.7, 6.05), (-2.8, 9.86, 6.35), 'dark', bevel=0.0)
    b.cyl((-6.6, 10.0, -13.0), (-6.6, 10.7, -13.0), 0.34, 8, 'dark')
    b.cyl((-6.6, 10.7, -13.0), (-6.6, 15.4, -13.0), 0.09, 6, 'steel', r2=0.045)
    b.cyl((-6.6, 15.4, -13.0), (-6.6, 15.6, -13.0), 0.14, 6, 'lightr')

    # ---------------------------------------------------------------- turret (origin 0, 10, -5)
    t = k.piece('turret'); A = t.at
    t.cyl(A(0, -0.1, 0), A(0, 0.5, 0), 5.0, 18, 'dark', bevel=0.06)
    # low faceted hexagonal dome
    t.hull([A(x * sx, y, z) for sx in (-1, 1) for x, y, z in
            [(4.6, 0.45, -5.4), (5.6, 0.45, -1.4), (5.2, 0.45, 2.8), (2.6, 0.45, 5.4),
             (3.6, 3.6, -4.4), (4.3, 3.6, -1.2), (3.9, 3.6, 2.0), (1.8, 3.6, 3.8),
             (2.6, 4.6, -3.2), (2.8, 4.6, 1.4)]], 'paint', bevel=0.14)
    # team roof plate
    t.hull([A(x * sx, y, z) for sx in (-1, 1) for x, y, z in
            [(2.3, 4.58, -2.9), (2.5, 4.58, 1.2), (2.25, 4.72, -2.85), (2.45, 4.72, 1.15)]], 'team', bevel=0.03)
    # cupola, rear right, warm periscope
    t.cyl(A(1.6, 4.6, -1.6), A(1.6, 5.3, -1.6), 1.0, 10, 'paint2', bevel=0.05)
    t.box(A(1.1, 4.85, -0.65), A(2.1, 5.15, -0.55), 'lightc', bevel=0.0)
    # rear bustle
    t.hull([A(x * sx, y, z) for sx in (-1, 1) for x, y, z in
            [(3.6, 0.7, -5.2), (3.4, 3.0, -4.6), (3.0, 0.9, -6.6), (2.8, 2.6, -6.3)]], 'paint2', bevel=0.09)
    # side smoke launchers
    t.cyl(A(4.6, 2.2, 1.4), A(5.4, 2.6, 2.6), 0.45, 8, 'dark', mirror=True)

    # ---------------------------------------------------------------- sleeve (mantlet; origin 0, 12, -1.36)
    sv = k.piece('sleeve'); S = sv.at
    sv.hull([S(x * sx, y, z) for sx in (-1, 1) for x, y, z in
             [(1.9, -1.7, -0.6), (1.9, 1.7, -0.6), (1.6, -1.4, 2.2), (1.6, 1.4, 2.2)]], 'paint2', bevel=0.12)
    sv.cyl(S(0, 0, 2.0), S(0, 0, 8.2), 1.05, 10, 'steel', r2=0.82, rot=math.pi / 10)
    sv.cyl(S(0, 0, 4.0), S(0, 0, 4.5), 1.15, 10, 'dark', rot=math.pi / 10)

    # ---------------------------------------------------------------- barrel (origin 0, 12, 6.5; recoils)
    br = k.piece('barrel'); B = br.at
    br.cyl(B(0, 0, -1.4), B(0, 0, 6.2), 0.66, 10, 'steel')
    br.cyl(B(0, 0, 2.6), B(0, 0, 3.0), 0.8, 10, 'dark')
    br.cyl(B(0, 0, 6.0), B(0, 0, 7.3), 0.95, 8, 'steel', rot=math.pi / 8, bevel=0.05)
    br.cyl(B(0, 0, 7.28), B(0, 0, 7.36), 0.45, 8, 'black')
    for sx in (-1, 1):
        br.box(B(0.8 * sx, -0.25, 6.3), B(1.0 * sx, 0.25, 7.0), 'black', bevel=0.0)
