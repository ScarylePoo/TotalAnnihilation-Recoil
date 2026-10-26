"""Pulverizer (CORE_T1_DEF_Pulverizer) - Core missile tower. A tall tapering ribbed tower (TA's plain obelisk) topped by
a big rounded helmet turret with three missile tubes in a triangle in its face (each tube kicks back 3 elmo on fire).
Not a pop-up: the Lua script only turns the turret (x + y) and recoils gun1..3.
Identity from above: a large dark dome-roofed head with an ochre crest and team-coloured flanks, three light tube
mouths forward, on a narrow dark tower with team-coloured corner ribs - a lollipop where the Gaat Gun is a box on a stick.
Pieces (Lua): base, turret (turn x+y), gun1..3 (move z), rocket1..3 (emit, empty).
Coordinates are ENGINE/global: X right, Y up, Z forward."""
import math

UNIT = dict(
    res=1024,
    wreck=dict(seed=31, drop=['gun1'], pose={'turret': (20, 40, 0)}),
    preview_pose={'turret': (-12, -25, 0)},
)


def build(k):
    # ------------------------------------------------------------------ base: obelisk
    b = k.piece('base')
    b.plan(0.0, 2.0, [(-15.6, -11), (-11, -15.6), (11, -15.6), (15.6, -11), (15.6, 11), (11, 15.6), (-11, 15.6), (-15.6, 11)],
           'paint2', bevel=0.2, top_inset=0.5)
    # tapering square tower
    b.plan(1.8, 38.0, [(-11.0, -11.0), (11.0, -11.0), (11.0, 11.0), (-11.0, 11.0)], 'paint', bevel=0.3, top_inset=4.0)
    # corner ribs: sloped buttress strips on the four corners, dark, with team tops
    for sx in (-1, 1):
        for sz in (-1, 1):
            b.hull([(x * sx, y, z * sz) for x, y, z in
                    [(9.6, 1.8, 9.6), (13.4, 1.8, 13.4), (12.4, 1.8, 9.6), (9.6, 1.8, 12.4),
                     (7.2, 30.0, 7.2), (8.6, 30.0, 8.6), (8.4, 30.0, 7.2), (7.2, 30.0, 8.4)]], 'team', bevel=0.15)
            b.hull([(x * sx, y, z * sz) for x, y, z in
                    [(9.6, 2.0, 9.6), (12.6, 2.0, 12.6), (9.6, 2.16, 9.6), (12.6, 2.16, 12.6),
                     (14.6, 2.0, 11.4), (11.4, 2.0, 14.6), (14.6, 2.16, 11.4), (11.4, 2.16, 14.6)]], 'team', bevel=0.0)
    # neck + collar
    b.cyl((0, 37.6, 0), (0, 46.6, 0), 6.0, 8, 'paint2', r2=4.6, rot=math.pi / 8, bevel=0.15)
    b.cyl((0, 46.4, 0), (0, 48.1, 0), 7.2, 12, 'dark', bevel=0.1)
    for y in (12.0, 24.0):
        b.box((-2.0, y, 10.6 - (y - 1.8) / 36.2 * 4.0 - 0.1), (2.0, y + 1.0, 10.9 - (y - 1.8) / 36.2 * 4.0), 'lightr', bevel=0.0)
    b.box((-3.0, 2.0, 10.8), (3.0, 9.0, 11.1), 'black', bevel=0.0)

    # ---------------------------------------------------------------- turret: helmet (origin 0, 48, 0)
    t = k.piece('turret'); A = t.at
    # octagonal helmet: wide flat sides, domed top, flat face at z ~ +10
    prof = [(-11.0, 0.0, 9.4), (-11.4, 7.6, 10.4), (-9.0, 13.4, 8.0), (-3.0, 15.4, 5.0),
            (8.0, 0.0, 9.4), (9.6, 7.6, 10.4), (9.4, 13.0, 8.0), (6.0, 15.2, 4.2)]
    t.hull([A(x * sx, y, z) for sx in (-1, 1) for (z, y, x) in prof], 'paint', bevel=0.35)
    # team flanks (top-facing upper slopes) and ochre crest
    for sx in (-1, 1):
        t.hull([A(sx * x, y, z) for (x, y) in ((9.6, 13.1), (4.6, 15.15)) for z in (-7.6, 5.0) for _ in (0,)] +
               [A(sx * (x + 0.12), y + 0.2, z) for (x, y) in ((9.6, 13.1), (4.6, 15.15)) for z in (-7.6, 5.0)],
               'team', bevel=0.0)
    t.hull([A(x, y, z) for x in (-1.8, 1.8) for z in (-2.6, 5.4) for y in (15.3, 15.55)], 'hazard', bevel=0.0)
    # dark face plate holding the tubes, side lamps
    t.hull([A(x * sx, y, z) for sx in (-1, 1) for x, y, z in
            [(9.6, 0.6, 9.6), (9.6, 13.6, 7.8), (9.2, 0.8, 10.8), (9.2, 13.2, 9.0)]], 'paint2', bevel=0.15)
    t.box(A(-11.0, 6.0, -6.0), A(11.0, 9.0, 2.0), 'paint2', bevel=0.2)       # side ammo cheeks
    t.box(A(-0.8, 15.2, -8.2), A(0.8, 15.6, -7.0), 'lightr', bevel=0.0)
    t.box(A(-8.0, 1.0, -11.0), A(8.0, 7.0, -10.6), 'black', bevel=0.0)

    # ---------------------------------------------------------------- tubes (gun1 top centre, gun2/3 low sides)
    g = k.piece('gun1'); G = g.at
    g.cyl(G(0, 0, -2.0), G(0, 0, 7.6), 3.1, 8, 'steel', rot=math.pi / 8, bevel=0.08)
    g.cyl(G(0, 0, 4.6), G(0, 0, 5.6), 3.4, 8, 'dark', rot=math.pi / 8, bevel=0.05)
    g.cyl(G(0, 0, 7.58), G(0, 0, 7.7), 2.2, 8, 'black')
    g.cyl(G(0, 0, 2.0), G(0, 0, 3.0), 3.3, 8, 'hazard', rot=math.pi / 8)
    k.clone('gun2', 'gun1')
    k.clone('gun3', 'gun1')
