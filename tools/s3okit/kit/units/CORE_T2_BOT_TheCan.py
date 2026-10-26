"""The Can (CORE_T2_BOT_TheCan) - Core T2 heavy armoured assault unit. By the user's decision it rolls on TRACKS
instead of TA's stubby legs: the leg pieces are dropped (skeleton=None, skeleton_opts drop) and a tracked lower hull
is added as four animation frames (tracks1..4, shown one at a time like the Instigator's, link pattern advanced a
quarter link per frame via tread..tread4). On the tracks sit TA's wide trapezoid belly, the armoured torso block and a
small offset gun turret (head + gun). Script ported to scripts/CORE_T2_BOT_TheCan.lua (aim/fire/death from the COB, no
walk). Coordinates are ENGINE/global: X right, Y up, Z forward.
Top view (what makes it The Can): a fat square slab - widest Core T2 bot - dark warm armour with team bands on the
sloped fenders, a dark torso block with a hazard bar, and a short light steel gun offset left on a tiny turret."""
import math

UNIT = dict(
    skeleton_opts=dict(drop=['rthigh', 'rleg', 'rfoot', 'lthigh', 'lleg', 'lfoot'],
                       add={'tracks1': ('pelvis', (0, 0, 0.5)), 'tracks2': ('pelvis', (0, 0, 0.5)),
                            'tracks3': ('pelvis', (0, 0, 0.5)), 'tracks4': ('pelvis', (0, 0, 0.5))}),
    res=1024,
    wreck=dict(seed=21, drop=['gun'], remove=['tracks2', 'tracks3', 'tracks4'], pose={'head': (0, 30, 0)}),
    preview_pose={'head': (0, -20, 0), 'tracks2': 'hide', 'tracks3': 'hide', 'tracks4': 'hide'},
)


def tracks(k, name, mat):
    t = k.piece(name); T = t.at                         # origin (0, 0, 0.5)
    belt = [(-12.6, 0.0), (11.8, 0.0), (14.6, 2.8), (13.8, 6.6), (-13.4, 6.6), (-14.8, 3.0)]
    t.prism(9.2, 15.0, [(z + 0.5, y) for z, y in belt], mat, bevel=0.16, mirror=True)


def build(k):
    for i, mat in enumerate(('tread', 'tread2', 'tread3', 'tread4'), 1):
        tracks(k, f'tracks{i}', mat)

    # ------------------------------------------------------------------ belly (0, 12.5, 0.5): hull + fenders
    b = k.piece('belly'); B = b.at
    b.hull([B(x * sx, y, z) for sx in (-1, 1) for x, y, z in                            # lower hull between the tracks
            [(9.2, -10.6, -11.0), (9.2, -10.6, 11.0), (9.2, -4.2, -12.6), (9.2, -4.2, 13.6), (7.0, -11.4, -9.0),
             (7.0, -11.4, 9.0)]], 'paint2', bevel=0.2)
    for sx in (-1, 1):                                                                  # road wheel hubs on the hull side
        for z in (-8.0, -2.4, 3.2, 8.8):
            b.cyl(B(sx * 9.2, -9.2, z), B(sx * 8.8, -9.2, z), 1.6, 12, 'dark')
    b.hull([B(x * sx, y, z) for sx in (-1, 1) for x, y, z in                            # trapezoid armour body
            [(15.4, -4.8, -12.0), (15.4, -4.8, 13.4), (15.4, -3.4, -12.2), (15.4, -3.4, 13.8),
             (10.6, 4.6, -9.0), (10.6, 4.6, 10.8), (6.0, -4.6, 15.0), (6.0, -0.8, 15.6)]], 'paint', bevel=0.26)
    for sx in (-1, 1):                                                                  # team bands on the sloped fenders
        b.hull([(sx * x, y, z) for x, y, z in
                [(11.6, 15.5, -8.4), (14.6, 10.52, -9.4), (11.6, 15.5, 10.2), (14.6, 10.52, 11.2),
                 (11.6, 15.66, -8.35), (14.6, 10.68, -9.35), (11.6, 15.66, 10.15), (14.6, 10.68, 11.15)]],
               'team', bevel=0.04)
    b.hull([B(x * sx, y, z) for sx in (-1, 1) for x, y, z in                            # hazard glacis lip
            [(5.6, -4.3, 15.05), (5.6, -1.1, 15.65), (5.6, -4.3, 15.25), (5.6, -1.1, 15.85)]], 'hazard', bevel=0.04)
    for sx in (-1, 1):
        b.box(B(sx * 8.0 - 1.0, -2.2, 14.6), B(sx * 8.0 + 1.0, -1.2, 15.0), 'lightw', bevel=0.0)   # headlights
    for sx in (-1, 1):                                                                  # rear exhausts
        b.cyl(B(sx * 6.0, 1.0, -9.4), B(sx * 6.0, 1.0, -12.8), 1.3, 10, 'dark', bevel=0.06)
        b.cyl(B(sx * 6.0, 1.0, -12.75), B(sx * 6.0, 1.0, -12.9), 0.85, 10, 'black')

    # ------------------------------------------------------------------ torso (0, 20, 0): armoured block
    t = k.piece('torso'); A = t.at
    t.hull([A(x * sx, y, z) for sx in (-1, 1) for x, y, z in
            [(8.6, -2.6, -8.6), (8.6, -2.6, 8.6), (10.2, 1.0, -7.6), (10.2, 1.0, 7.6), (7.4, 5.0, -7.0), (7.4, 5.0, 6.2),
             (5.0, 1.0, 9.8)]], 'paint2', bevel=0.24)
    t.hull([A(x * sx, y, z) for sx in (-1, 1) for x, y, z in                            # hazard bar across the front top
            [(6.6, 5.02, 4.0), (6.6, 5.02, 5.6), (6.6, 5.18, 4.05), (6.6, 5.18, 5.55)]], 'hazard', bevel=0.02)
    for x in (-5.6, 5.6):                                                               # roof vent blocks
        t.box(A(x - 1.4, 4.9, -6.0), A(x + 1.4, 5.6, -1.0), 'dark', bevel=0.06)
    for sx in (-1, 1):                                                                  # side armour cheeks
        t.hull([A(sx * x, y, z) for x, y, z in
                [(10.0, -2.0, -5.0), (10.0, -2.0, 5.0), (11.2, 0.0, -4.2), (11.2, 0.0, 4.2), (10.0, 2.6, -4.6), (10.0, 2.6, 4.6)]],
               'paint', bevel=0.12)

    # ------------------------------------------------------------------ head (0.5, 25, -2.5): small turret
    h = k.piece('head'); H = h.at
    h.hull([H(x * sx, y, z) for sx in (-1, 1) for x, y, z in
            [(3.6, 0.0, -3.6), (3.6, 0.0, 3.8), (2.8, 3.6, -3.0), (2.8, 3.6, 3.0), (2.0, 1.4, 4.8)]], 'paint', bevel=0.16)
    h.box(H(-1.6, 3.55, -2.2), H(1.6, 3.75, 1.8), 'team', bevel=0.03)
    h.box(H(2.2, 1.6, 3.6), H(3.0, 2.4, 4.0), 'lightw', bevel=0.0)                      # sensor lamp, right side

    # ------------------------------------------------------------------ gun (-2, 28, -4): barrel to firept (-1.68, 0, 12.5)
    g = k.piece('gun'); G = g.at
    g.hull([G(x, y, z) for x in (-3.3, -0.1) for y in (-1.5, 1.5) for z in (-2.6, 3.6)], 'dark', bevel=0.12)
    g.cyl(G(-1.68, 0, 3.0), G(-1.68, 0, 11.6), 0.85, 10, 'steel')
    g.cyl(G(-1.68, 0, 11.2), G(-1.68, 0, 12.6), 1.15, 8, 'dark', rot=math.pi / 8, bevel=0.04)
    g.cyl(G(-1.68, 0, 12.55), G(-1.68, 0, 12.7), 0.55, 8, 'black')
