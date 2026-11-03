"""Krogoth (CORE_T3_BOT_Krogoth) - Core's experimental walker, the biggest biped in the game (~70 elmos tall, a Peewee
is 20). Standard biped skeleton (H 28, TA hips at 25-30, massive backwards legs); script ported to scripts/CORE_T3_BOT_Krogoth.lua.
Identity from above, taken from the TA model and exaggerated: a very wide cross - two huge team-roofed shoulder blocks
either side of a narrow armoured chest, a long horned head wedge running front to back along the centre line (light
steel crest, red eye), two missile silos with team caps standing behind the shoulders. Cannon arms hang down at rest
and swing forward and out to fire (luparm z 45, larm x -90), so the steel barrels stick out ahead of the body in combat.
Pieces (COB): torso turns for the cannons, head turns alone for the Annihilator beam (head hangs off pelvis, not the
torso, as in TA), r/lmissle2 lift 15 and tilt out 15 deg. Flare/emit pieces stay empty; 3xGround, the old hips, toes
and heels are dropped. Coordinates are ENGINE/global: X right, Y up, Z forward."""

UNIT = dict(
    skeleton='biped',
    skeleton_opts=dict(height=28.0, hipx=7.5, drop=['rheel', 'lheel', '3xGround']),
    res=2048,
    wreck=dict(seed=91, drop=['ruparm'], pose={'torso': (0, -18, 0), 'head': (24, 25, 0), 'luparm': (35, 0, 20),
                                               'lmissle2': (0, 0, -25), 'rmissle2': (30, 0, 15)}),
    preview_pose={},
    preview_zoom=1.2,
)


def sym(pts):
    return [(x * s, y, z) for s in (-1, 1) for x, y, z in pts]


def build(k):
    k.standard_legs(width=1.6)

    # ------------------------------------------------------------------ pelvis (0, 28, 0): hip block + armoured skirt
    p = k.piece('pelvis')
    p.hull(sym([(10.5, 23.5, -6.0), (10.5, 23.5, 5.5), (11.5, 30.0, -7.5), (11.5, 30.0, 7.0), (7.0, 33.0, -6.5),
                (7.0, 33.0, 6.0), (5.5, 21.0, -3.5), (5.5, 21.0, 4.0)]), 'paint2', bevel=0.35)
    p.hull(sym([(4.4, 21.6, 4.3), (4.4, 29.5, 7.9), (2.6, 19.8, 3.6), (2.6, 30.0, 8.3)]), 'dark', bevel=0.2)

    # ------------------------------------------------------------------ torso (0, 30, -1.25): barrel chest
    t = k.piece('torso')
    t.hull(sym([(8.0, 30.5, -6.0), (8.0, 30.5, 5.0), (10.5, 38.0, -8.0), (10.5, 38.0, 7.0)]), 'dark', bevel=0.3)
    t.hull(sym([(10.5, 37.0, -8.5), (10.5, 37.0, 7.6), (13.8, 46.0, -10.5), (13.8, 46.0, 10.2), (13.0, 53.0, -9.0),
                (13.0, 53.0, 8.0), (7.5, 55.0, -6.5), (7.5, 55.0, 6.0)]), 'paint', bevel=0.45)
    t.hull([(4.0, 39.0, 8.2), (4.0, 39.0, 8.9), (10.5, 43.0, 9.6), (10.5, 43.0, 10.5), (11.5, 50.5, 9.0),
            (11.5, 50.5, 9.9), (4.0, 53.0, 7.7), (4.0, 53.0, 8.4)], 'paint2', bevel=0.15, mirror=True)
    t.hull(sym([(3.2, 41.0, 9.0), (3.2, 41.0, 9.7), (3.2, 50.0, 8.9), (3.2, 50.0, 9.9), (1.6, 39.2, 8.9),
                (1.6, 39.2, 9.4)]), 'dark', bevel=0.1)
    t.hull(sym([(2.2, 43.0, 9.6), (2.2, 43.0, 10.05), (2.2, 48.0, 9.6), (2.2, 48.0, 10.05)]), 'lightr', bevel=0.05)

    # ------------------------------------------------------------------ head (0, 51, 0): long wedge, horns, crest
    h = k.piece('head')
    h.hull(sym([(6.5, 54.0, -7.0), (6.5, 54.0, 6.0), (7.6, 59.0, -8.0), (7.0, 59.0, 8.0), (5.0, 63.5, -7.0),
                (3.4, 63.0, 6.0), (2.4, 58.0, 12.5), (2.0, 60.5, 12.0)]), 'paint2', bevel=0.3)
    h.hull(sym([(1.7, 63.2, 6.5), (1.7, 63.7, 6.5), (3.0, 63.8, -6.0), (3.0, 64.5, -6.0), (2.6, 60.9, 11.8),
                (2.6, 60.5, 12.4)]), 'steel', bevel=0.08)
    h.hull([(3.0, 61.0, -5.0), (6.5, 60.0, -5.0), (5.0, 64.0, -6.5), (3.0, 64.0, -5.0), (5.5, 70.0, -19.0),
            (6.2, 68.0, -20.0)], 'team', bevel=0.12, mirror=True)
    h.hull([(3.0, 56.0, -7.0), (7.0, 56.0, -7.0), (3.0, 60.0, -9.0), (7.0, 60.0, -9.0), (4.5, 61.0, -17.0),
            (5.5, 58.5, -16.0)], 'dark', bevel=0.12, mirror=True)
    h.box((-5.8, 54.0, -2.0), (-3.0, 55.0, 2.0), 'dark', bevel=0.05, mirror=True)
    # ------------------------------------------------------------------ eyegun: the Annihilator beam socket
    e = k.piece('eyegun')
    e.cyl((0, 60.0, 6.0), (0, 60.0, 11.5), 3.0, 12, 'dark', r2=3.3)
    e.cyl((0, 60.0, 11.4), (0, 60.0, 13.2), 2.1, 12, 'lightr')

    # ------------------------------------------------------------------ left shoulder (12.5, 45, 1.25)
    u = k.piece('luparm'); U = u.at
    u.cyl(U(-1.5, 0, 0), U(3.0, 0, 0), 6.5, 12, 'dark')
    u.hull([U(x, y, z) for x, y, z in
            [(1.0, -9.5, -9.0), (1.0, -9.5, 8.0), (12.5, -11.0, -9.0), (12.5, -11.0, 8.5), (14.0, 3.0, -12.0),
             (14.0, 3.0, 11.0), (1.0, 3.0, -12.0), (1.0, 3.0, 10.0), (1.0, 9.0, -8.5), (1.0, 9.0, 7.5), (12.0, 9.0, -9.0),
             (12.0, 9.0, 8.0)]], 'paint', bevel=0.5)
    u.hull([U(x, y, z) for x, y, z in                                           # roof: the big team blocks of the cross
            [(2.2, 9.03, -7.4), (2.2, 9.03, 6.4), (10.8, 9.03, -7.6), (10.8, 9.03, 6.6),
             (2.2, 9.25, -7.4), (2.2, 9.25, 6.4), (10.8, 9.25, -7.6), (10.8, 9.25, 6.6)]], 'team', bevel=0.04)
    u.hull([U(x, y, z) for x, y, z in                                           # outer pauldron rim
            [(14.0, 2.0, -12.4), (14.0, 2.0, 11.4), (14.4, 4.0, -12.4), (14.4, 4.0, 11.4), (15.6, -8.0, -9.0),
             (15.6, -8.0, 8.5), (15.6, -3.0, -11.0), (15.6, -3.0, 10.5)]], 'paint2', bevel=0.2)
    k.clone('ruparm', 'luparm', mirror_x=True)

    # ------------------------------------------------------------------ left forearm + cannon (16.25, 38.5, 1.25)
    # barrel axis through lgunflare (-0.72, -26.11, 4.35). Local -y = forward when aiming, local +z = up.
    a = k.piece('larm'); A = a.at
    a.cyl(A(-3.6, 0, 0), A(8.4, 0, 0), 4.4, 12, 'dark')
    a.hull([A(x, y, z) for x, y, z in
            [(-3.4, 2.0, -5.0), (-3.4, 2.0, 5.0), (8.4, 2.0, -5.0), (8.4, 2.0, 5.0), (-3.4, -14.0, -9.0),
             (-3.4, -14.0, 8.2), (8.4, -14.0, -9.0), (8.4, -14.0, 8.2)]], 'paint2', bevel=0.4)
    a.hull([A(x, y, z) for x, y, z in
            [(7.6, -2.0, 6.6), (7.6, -13.2, 8.25), (0.0, -2.0, 6.6), (0.0, -13.2, 8.25), (7.6, -2.0, 6.85),
             (7.6, -13.2, 8.45), (0.0, -13.2, 8.45), (0.0, -2.0, 6.85)]], 'team', bevel=0.03)
    a.hull([A(x, y, z) for x, y, z in                                            # underslung fin
            [(1.0, -4.0, -6.5), (5.0, -4.0, -6.5), (1.0, -13.0, -8.5), (5.0, -13.0, -8.5), (2.0, -13.0, -14.0),
             (4.0, -13.0, -14.0)]], 'dark', bevel=0.2)
    a.cyl(A(-0.72, -12.0, 4.35), A(-0.72, -25.0, 4.35), 2.7, 10, 'steel', bevel=0.1)
    a.cyl(A(-0.72, -12.0, 4.35), A(-0.72, -16.0, 4.35), 3.6, 10, 'dark')
    a.cyl(A(-0.72, -23.0, 4.35), A(-0.72, -26.1, 4.35), 3.3, 10, 'steel', r2=2.9, bevel=0.1)
    a.cyl(A(-0.72, -26.05, 4.35), A(-0.72, -26.25, 4.35), 1.8, 10, 'black')
    k.clone('rarm', 'larm', mirror_x=True)

    # ------------------------------------------------------------------ backpack (0, 42.5, -11)
    m = k.piece('mpack')
    m.hull(sym([(11.5, 30.0, -11.0), (11.5, 30.0, -8.5), (13.0, 44.0, -14.5), (13.0, 44.0, -9.0), (11.0, 56.0, -15.0),
                (11.0, 56.0, -8.0), (6.0, 60.0, -13.0), (6.0, 60.0, -8.0)]), 'paint2', bevel=0.35)
    m.box((-2.6, 42.0, -16.0), (2.6, 58.0, -14.0), 'dark', bevel=0.2)
    m.box((-14.5, 33.0, -17.0), (-4.5, 37.0, -13.0), 'dark', bevel=0.2, mirror=True)      # silo clamps

    # ------------------------------------------------------------------ left missile silo (10, 26.75, -21.75)
    s = k.piece('lmissle2'); S = s.at
    s.cyl(S(0, 0, 0), S(0, 5.0, 0), 5.3, 8, 'dark', r2=5.6, rot=0.39)
    s.cyl(S(0, 5.0, 0), S(0, 28.0, 0), 5.6, 8, 'paint', rot=0.39, bevel=0.2)
    s.cyl(S(0, 15.0, 0), S(0, 18.0, 0), 5.9, 8, 'dark', rot=0.39)
    s.cyl(S(0, 28.0, 0), S(0, 28.6, 0), 5.1, 8, 'team', rot=0.39)
    for dx, dz in ((-1.9, -1.9), (1.9, -1.9), (-1.9, 1.9), (1.9, 1.9)):
        s.cyl(S(dx, 28.5, dz), S(dx, 28.75, dz), 1.2, 8, 'black')
    k.clone('rmissle2', 'lmissle2', mirror_x=True)
