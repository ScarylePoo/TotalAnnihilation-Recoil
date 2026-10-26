"""Phoenix (ARM_T2_AIR_Phoenix) - Arm T2 strategic bomber. Much heavier than the T1 Thunder: a fat humped fuselage
(26 elmo wide wing-glove slab, 11 elmo spine) with a glazed bomb-aimer nose, FOUR engines in two big twin nacelles
on the glove, a canted twin tail and a ventral defence turret. The wings (wing1/wing2) are stowed INSIDE the glove
slab when landed and slide out 17 elmo on take-off (COB move x, z), so the flying Phoenix is a 68-elmo broad swept
wing with team-coloured outer panels - a wide heavy cross from above, where the Thunder is a light W.
Pieces (TA layout): base (bombdrop/thrust empty children), wing1/wing2 (sliding wings; wing1 = mirrored clone of
wing2 - note wing1 sits at +x when stowed and slides to the LEFT side), gun (ventral turret, turns x/y),
flare1/flare2 (empty gun emit points, muzzle-flash polygons dropped).
Value groups from above: light Arm fuselage and wings, dark paint2 twin nacelles + flap strips, black intakes and
bomb bay, team on the outer wing panels + a broad saddle across the spine.
Coordinates are ENGINE/global: X right, Y up, Z forward. mirror=True builds the -X twin sharing UVs."""
import math

UNIT = dict(
    res=1024,
    wreck=dict(seed=35, remove=['wing1'], drop=[]),
    always_visible=['wing1', 'wing2'],        # stowed inside the glove at rest
    # flight pose: wings slid out (engine x = -COB x)
    preview_pose={'wing1': {'move': (-16.875, 0, -4.375)}, 'wing2': {'move': (17.375, 0, -4.625)}},
)


def build(k):
    b = k.piece('base')
    # ------------------------------------------------------------------ wing-glove slab (crosses x = 0)
    b.hull([(x * sx, y, z) for sx in (-1, 1) for x, y, z in
            [(4.0, 0.6, 22.0), (4.0, 3.4, 22.0), (13.6, 0.6, 13.4), (13.6, 3.4, 12.8),
             (13.6, 0.6, -15.0), (13.6, 3.4, -15.0), (8.0, 0.8, -20.0), (8.0, 3.4, -20.0)]], 'paint', bevel=0.16)
    # humped fuselage on top of the glove
    b.hull([(x * sx, y, z) for sx in (-1, 1) for x, y, z in
            [(0.6, 3.0, 31.0), (0.6, 4.4, 30.6), (2.8, 2.4, 26.0), (2.6, 6.2, 25.0),
             (6.2, 3.0, 19.0), (5.2, 8.0, 18.0), (9.6, 3.2, 6.4), (8.0, 9.6, 6.4), (3.4, 11.4, 5.0),
             (9.6, 3.2, -11.5), (8.0, 9.6, -11.5), (3.4, 11.4, -11.5),
             (4.0, 3.2, -25.0), (3.0, 7.0, -25.0), (2.2, 3.4, -28.0), (1.8, 6.0, -28.0)]], 'paint', bevel=0.22, seg=2)
    # glazed bomb-aimer nose + cockpit
    b.hull([(x * sx, y, z) for sx in (-1, 1) for x, y, z in
            [(0.8, 3.2, 31.2), (2.6, 4.8, 26.4), (2.2, 6.4, 25.0), (1.0, 5.0, 30.0), (2.4, 2.8, 27.0)]], 'glass', bevel=0.06)
    b.hull([(x * sx, y, z) for sx in (-1, 1) for x, y, z in
            [(2.2, 8.0, 20.2), (3.6, 9.4, 15.0), (2.0, 11.2, 11.0), (1.0, 11.6, 13.0), (3.4, 10.4, 10.4)]], 'glass', bevel=0.08)
    b.cyl((0, 3.8, 31.0), (0, 3.8, 33.6), 0.45, 8, 'dark', r2=0.15)
    # team saddle across the spine (broad flat band, the fuselage's colour block)
    b.hull([(x * sx, y, z) for sx in (-1, 1) for x, y, z in
            [(3.6, 11.42, 3.0), (3.6, 11.42, -7.0), (6.6, 10.3, 3.0), (6.6, 10.3, -7.0),
             (3.6, 11.58, 3.0), (3.6, 11.58, -7.0), (6.6, 10.46, 3.0), (6.6, 10.46, -7.0)]], 'team', bevel=0.03)
    # dorsal sensor blister + beacon
    b.cyl((0, 11.2, -9.0), (0, 12.6, -9.0), 1.4, 12, 'dark', r2=1.0, bevel=0.06)
    b.cyl((0, 12.6, -9.0), (0, 13.0, -9.0), 0.5, 8, 'lightr')
    # twin engine nacelles on the glove (4 engines; dark paint2, the bomber's dark bars from above)
    for x in (11.0,):
        b.hull([(x + dx, y, z) for dx in (-2.6, 2.6) for y, z in ((3.2, 9.0), (3.2, -17.0), (7.4, 7.0), (7.4, -16.0))] +
               [(x, 8.4, 6.0), (x, 8.4, -15.0)], 'paint2', bevel=0.2, mirror=True)
        for dx in (-1.3, 1.3):
            b.cyl((x + dx, 5.4, 9.3), (x + dx, 5.4, 7.6), 1.2, 10, 'black', mirror=True)
            b.cyl((x + dx, 5.4, -16.8), (x + dx, 5.4, -18.6), 1.25, 10, 'dark', r2=1.05, bevel=0.03, mirror=True)
            b.cyl((x + dx, 5.4, -18.55), (x + dx, 5.4, -18.7), 0.75, 10, 'lightc', mirror=True)
        b.box((x - 0.5, 8.3, -12.0), (x + 0.5, 8.6, 2.0), 'dark', bevel=0.0, mirror=True)
    # bomb bay (bombdrop at 0, 0, 0)
    b.box((-3.4, 0.35, -10.0), (3.4, 0.7, 8.0), 'black', bevel=0.05)
    for z in (-8.0, -2.0, 4.0):
        b.box((-3.6, 0.2, z), (3.6, 0.45, z + 0.8), 'dark', bevel=0.0)
    # canted twin tail + stabilisers
    b.hull([(2.6, 6.4, -18.0), (2.6, 5.6, -28.0), (6.9, 14.4, -25.5), (7.5, 14.2, -29.6),
            (3.4, 6.4, -18.0), (3.4, 5.6, -28.0), (7.6, 14.4, -25.5), (8.2, 14.2, -29.6)], 'paint', bevel=0.08, mirror=True)
    b.hull([(x, y, z) for x, y, z in [(6.9, 13.4, -25.0), (6.95, 14.4, -25.5), (7.5, 14.2, -29.6), (7.2, 13.3, -29.0)]] +
           [(x + 0.75, y, z) for x, y, z in [(6.9, 13.4, -25.0), (6.95, 14.4, -25.5), (7.5, 14.2, -29.6), (7.2, 13.3, -29.0)]],
           'team', bevel=0.0, mirror=True)
    b.box((7.4, 14.2, -29.4), (8.3, 14.6, -28.4), 'lightr', bevel=0.0, mirror=True)
    b.hull([(3.0, 3.4, -21.0), (2.6, 3.4, -28.0), (12.0, 3.6, -27.0), (12.0, 3.6, -30.0),
            (3.0, 4.6, -21.0), (2.6, 4.6, -28.0), (12.0, 4.0, -27.0), (12.0, 4.0, -30.0)], 'paint', bevel=0.08, mirror=True)
    # centre tail nozzle (thrust emit 0.2, 4.5, -26.2 .. -32.2)
    b.cyl((0, 4.6, -26.6), (0, 4.6, -29.6), 1.9, 12, 'dark', r2=1.6, bevel=0.05)
    b.cyl((0, 4.6, -29.55), (0, 4.6, -29.7), 1.2, 12, 'lightc')
    # glove leading-edge lights
    b.box((13.0, 1.4, 12.2), (13.7, 2.4, 13.3), 'lightw', bevel=0.0, mirror=True)

    # ------------------------------------------------------------------ ventral turret (gun, origin 0.25, 0.5, -9.25)
    g = k.piece('gun'); G = g.at
    g.cyl(G(0, 0.1, 0), G(0, -1.4, 0), 3.6, 14, 'paint2', r2=3.0, bevel=0.1)
    g.sphere(G(0, -1.4, 0.4), 2.2, 'glass', scale=(1, 0.6, 1))
    for dx in (-2.26, 2.26):
        g.box(G(dx - 0.7, -1.9, 0.6), G(dx + 0.7, -0.6, 3.4), 'dark', bevel=0.08)
        g.cyl(G(dx, -1.26, 3.2), G(dx, -1.26, 9.3), 0.36, 8, 'steel')
        g.cyl(G(dx, -1.26, 8.6), G(dx, -1.26, 9.4), 0.52, 8, 'dark')

    # ------------------------------------------------------------------ wing2 (origin -3.75, 1.5, 2.25; slides to +x)
    w = k.piece('wing2'); W = w.at
    WY = 1.0
    pl = [(0.3, 15.6), (0.3, -12.4), (20.6, -17.6), (20.6, -10.6)]
    pts = []
    for x, z in pl:
        t = 0.95 - 0.55 * x / 20.6
        pts += [W(x, WY + t, z), W(x, WY - t, z)]
    w.hull(pts, 'paint', bevel=0.08)
    # big team panel on the outer wing
    tp = [(7.0, 6.2), (18.8, -9.2), (18.8, -14.8), (7.0, -12.0)]
    w.hull([W(x, WY + 0.95 - 0.55 * x / 20.6 + d, z) for x, z in tp for d in (0.02, 0.12)], 'team', bevel=0.03)
    # dark flap strip + root fairing
    w.hull([W(x, WY + 0.95 - 0.55 * x / 20.6 + d, z) for x, z in ((0.8, -10.4), (6.4, -11.9), (6.4, -13.5), (0.8, -12.0))
            for d in (0.02, 0.12)], 'paint2', bevel=0.0)
    # wing-tip pod with nav light
    w.cyl(W(20.6, WY, -5.0), W(20.6, WY, -18.2), 0.75, 8, 'dark', r2=0.55)
    w.cyl(W(20.6, WY, -4.5), W(20.6, WY, -5.02), 0.45, 8, 'lightw', r2=0.75)
    k.clone('wing1', 'wing2', mirror_x=True)
