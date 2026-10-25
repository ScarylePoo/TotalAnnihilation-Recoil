"""Instigator (CORE_T1_VEH_Instigator) - Core light laser tank. Low angular hull on wide tracks, compact turret with
one laser cannon offset to the right. Coordinates are ENGINE/global: X right, Y up, Z forward.

Piece layout is the MRD remodel's (the COB drives it): base (empty, aim), body, turret (turn y), sleeve (no turn),
barrel (recoil, move z), firepoint (emit), tracks1..4 (shown one at a time to animate the treads: identical shapes,
link pattern advanced a quarter link per frame via tread/tread2/tread3/tread4).
Value groups seen from above: dark warm armour (paint), darker lower hull/pods (paint2), black tracks, team plates on
the fender tops and turret roof, light steel barrel against the dark hull, ochre hazard glacis."""
import math

UNIT = dict(
    res=1024,
    wreck=dict(seed=4, drop=['barrel'], remove=['tracks2', 'tracks3', 'tracks4'], pose={'turret': (0, 35, 0)}),
    preview_pose={'turret': (0, -20, 0), 'tracks2': 'hide', 'tracks3': 'hide', 'tracks4': 'hide'},
)


def tracks(k, name, mat):
    t = k.piece(name)
    xi, xo = 6.0, 10.6
    belt = [(-12.6, 0.0), (11.0, 0.0), (13.3, 1.5), (12.6, 3.3), (-13.2, 3.3), (-14.4, 1.5)]
    t.prism(xi, xo, belt, mat, bevel=0.15, mirror=True)


def build(k):
    # ------------------------------------------------------------------ tracks (4 animation frames)
    for i, mat in enumerate(('tread', 'tread2', 'tread3', 'tread4'), 1):
        tracks(k, f'tracks{i}', mat)

    # ------------------------------------------------------------------ body
    b = k.piece('body')
    # lower hull between the tracks (crosses x=0)
    b.prism(-6.1, 6.1, [(-14.0, 2.2), (12.6, 2.2), (15.0, 4.4), (14.2, 6.0), (-14.6, 6.0), (-15.0, 4.0)], 'paint2', bevel=0.15)
    # road-wheel hubs between belt runs, seen through the gap under the fenders
    for z in (-9.5, -4.0, 1.5, 7.0):
        b.cyl((6.0, 1.7, z), (5.6, 1.7, z), 1.25, 12, 'dark', mirror=True)
    # fenders over the tracks: wide, flat, sloping down at the nose
    b.hull([(5.4, 5.4, -14.6), (11.4, 5.4, -14.2), (11.4, 5.4, 10.6), (5.4, 5.4, 11.0),
            (5.4, 4.2, 14.4), (10.6, 4.2, 13.8),
            (5.4, 3.5, -14.8), (11.6, 3.5, -14.4), (11.6, 3.5, 11.0), (5.4, 3.5, 11.6), (5.4, 3.0, 14.6), (10.6, 3.0, 14.0)],
           'paint', bevel=0.14, mirror=True)
    # angled side skirt below the fender edge (Core spikiness, darker band)
    b.hull([(11.3, 3.6, -13.6), (12.1, 4.6, -13.0), (12.1, 4.6, 9.8), (11.3, 3.6, 10.6),
            (10.9, 2.4, -12.8), (11.6, 3.3, -12.4), (11.6, 3.3, 9.4), (10.9, 2.4, 10.0)], 'paint2', bevel=0.1, mirror=True)
    # team plates along the fender tops (the main read of team colour from above)
    b.hull([(7.0, 5.42, -12.6), (10.4, 5.42, -12.3), (10.4, 5.42, 9.8), (7.0, 5.42, 10.1),
            (7.05, 5.56, -12.5), (10.35, 5.56, -12.2), (10.35, 5.56, 9.7), (7.05, 5.56, 10.0)], 'team', bevel=0.04, mirror=True)
    # ochre hazard chevron on the fender noses
    b.hull([(5.8, 4.28, 13.9), (10.2, 4.28, 13.3), (5.8, 5.46, 11.3), (10.8, 5.46, 10.8),
            (5.8, 4.4, 13.85), (10.2, 4.4, 13.25), (5.8, 5.56, 11.25), (10.8, 5.56, 10.75)], 'hazard', bevel=0.03, mirror=True)
    # upper hull: wedge rising from the glacis to the turret deck (crosses x=0)
    b.hull([(x * sx, y, z) for sx in (-1, 1) for x, y, z in
            [(5.6, 5.4, -14.8), (5.6, 5.4, 12.0), (4.6, 4.9, 14.8),
             (4.8, 8.9, -13.6), (4.8, 8.9, 4.6), (3.4, 7.2, 11.6)]], 'paint', bevel=0.16)
    # glacis hazard plate (front read: Core ochre)
    b.hull([(x * sx, y, z) for sx in (-1, 1) for x, y, z in
            [(3.9, 5.1, 14.55), (2.9, 7.0, 11.95), (3.9, 5.22, 14.67), (2.9, 7.12, 12.07)]], 'hazard', bevel=0.03)
    # headlights and a dark sensor slot either side of the glacis
    b.box((4.0, 4.6, 14.2), (5.3, 5.3, 14.9), 'dark', bevel=0.06, mirror=True)
    b.box((4.15, 4.72, 14.88), (5.15, 5.18, 14.98), 'lightw', bevel=0.0, mirror=True)
    # rear engine deck: dark grille block with slats, exhaust stacks
    b.box((-4.0, 8.4, -13.4), (4.0, 9.25, -9.2), 'dark', bevel=0.1)
    for z in (-12.8, -12.0, -11.2, -10.4):
        b.box((-3.6, 9.25, z), (3.6, 9.4, z + 0.4), 'black', bevel=0.0)
    b.cyl((4.4, 8.6, -13.8), (4.4, 10.8, -14.4), 0.55, 10, 'dark', bevel=0.04, mirror=True)
    b.cyl((4.4, 10.8, -14.4), (4.4, 10.95, -14.45), 0.38, 10, 'black', mirror=True)
    # rear plate with tail lights
    b.box((-5.0, 5.6, -15.15), (5.0, 8.2, -14.75), 'paint2', bevel=0.06)
    b.box((3.6, 6.9, -15.25), (4.6, 7.5, -15.1), 'lightr', bevel=0.0, mirror=True)
    # hatch on the front deck, offset left (asymmetric detail)
    b.cyl((-2.4, 8.2, 7.0), (-2.4, 8.55, 7.0), 1.15, 14, 'paint2', bevel=0.05)
    b.box((-2.9, 8.55, 6.85), (-1.9, 8.7, 7.15), 'dark', bevel=0.0)
    # short antenna, rear left
    b.cyl((-5.0, 8.9, -12.2), (-5.0, 9.6, -12.2), 0.3, 8, 'dark')
    b.cyl((-5.0, 9.6, -12.2), (-5.0, 14.0, -12.2), 0.08, 6, 'steel', r2=0.04)
    b.cyl((-5.0, 14.0, -12.2), (-5.0, 14.2, -12.2), 0.13, 6, 'lightr')

    # ---------------------------------------------------------------- turret (origin 0, 9, -5; turns about Y)
    t = k.piece('turret'); A = t.at
    t.cyl(A(0, -0.1, 0), A(0, 0.5, 0), 3.9, 18, 'dark', bevel=0.06)
    # angular faceted turret, nose narrow, wider at the rear
    t.hull([A(x * sx, y, z) for sx in (-1, 1) for x, y, z in
            [(3.6, 0.45, -4.8), (4.0, 0.45, -0.8), (3.0, 0.45, 3.4), (1.4, 0.45, 5.0),
             (2.9, 3.2, -4.2), (3.1, 3.2, -0.8), (2.1, 3.2, 2.8), (0.9, 3.2, 3.8)]], 'paint', bevel=0.13)
    # team roof plate
    t.hull([A(x * sx, y, z) for sx in (-1, 1) for x, y, z in
            [(2.3, 3.18, -3.7), (2.5, 3.18, -0.8), (1.6, 3.18, 2.2), (0.6, 3.18, 3.0),
             (2.25, 3.32, -3.65), (2.45, 3.32, -0.8), (1.55, 3.32, 2.15), (0.55, 3.32, 2.95)]], 'team', bevel=0.03)
    # sensor block on the roof, rear left, with a warm lens
    t.hull([A(x, y, z) for x, y, z in
            [(-2.1, 3.3, -3.4), (-0.7, 3.3, -3.4), (-2.1, 3.3, -1.9), (-0.7, 3.3, -1.9),
             (-1.95, 4.1, -3.25), (-0.85, 4.1, -3.25), (-1.95, 4.1, -2.1), (-0.85, 4.1, -2.1)]], 'paint2', bevel=0.07)
    t.box(A(-1.75, 3.55, -1.95), A(-1.05, 3.9, -1.82), 'lightc', bevel=0.0)
    # turret bustle (rear stowage), darker
    t.hull([A(x * sx, y, z) for sx in (-1, 1) for x, y, z in
            [(2.6, 0.7, -4.6), (2.6, 2.7, -4.3), (2.3, 0.9, -5.7), (2.2, 2.4, -5.5)]], 'paint2', bevel=0.09)
    # cheek housing around the right-hand gun mount
    t.hull([A(x, y, z) for x, y, z in
            [(0.2, 0.6, 2.0), (3.0, 0.6, 2.0), (0.4, 0.6, 4.4), (2.7, 0.6, 4.4),
             (0.3, 2.7, 1.8), (2.8, 2.7, 1.8), (0.5, 2.5, 4.0), (2.6, 2.5, 4.0)]], 'paint2', bevel=0.1)

    # ---------------------------------------------------------------- sleeve (gun mount at x 1.57, y 10.5, z 0)
    sv = k.piece('sleeve'); S = sv.at
    sv.cyl(S(0, 0, 3.6), S(0, 0, 5.5), 1.35, 10, 'dark', r2=1.0, rot=math.pi / 10, bevel=0.05)
    sv.cyl(S(0, 0, 4.4), S(0, 0, 4.75), 1.42, 10, 'steel', rot=math.pi / 10)
    # power cable from the turret into the mount
    sv.cyl(S(-1.25, -0.6, 2.3), S(-0.95, -0.5, 4.6), 0.3, 8, 'black')

    # ---------------------------------------------------------------- barrel (laser emitter, recoils along z)
    br = k.piece('barrel'); B = br.at
    br.cyl(B(0, 0, -0.6), B(0, 0, 8.2), 0.5, 10, 'steel')
    for z in (1.0, 1.7, 2.4, 3.1):                    # cooling fins
        br.cyl(B(0, 0, z), B(0, 0, z + 0.32), 0.88, 10, 'dark', rot=math.pi / 10, bevel=0.03)
    br.cyl(B(0, 0, 6.2), B(0, 0, 6.6), 0.7, 10, 'dark', bevel=0.04)
    br.cyl(B(0, 0, 8.1), B(0, 0, 8.85), 0.72, 8, 'dark', r2=0.62, rot=math.pi / 8, bevel=0.04)
    br.cyl(B(0, 0, 8.84), B(0, 0, 8.9), 0.38, 10, 'lightr')    # emitter lens
