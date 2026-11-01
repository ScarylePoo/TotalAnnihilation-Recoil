"""Decoy Commander (CORE_T2_BOT_DecoyCommander) - Core decoy that must pass for the Core Commander (CORE_Commander,
not remodelled yet: when it is, match it to this). The unit used a third-party S3O (preserved in tools/s3okit/ref/),
which shares the real commander's piece layout; remodelled to it as a commander-class biped: the tallest Core walker,
a massive angular chest with a ridged back pack, ball shoulders, a small helmet with a red visor, a D-gun as the right
forearm (r_dgun, pointing forward) and a heavy nano/laser gauntlet as the left (l_nano). Heavy legs. Standard biped
skeleton; script ported to scripts/CORE_T2_BOT_DecoyCommander.lua. Coordinates are ENGINE/global: X right, Y up, Z fwd.
Top view (commander read): a broad dark-warm chest with team shoulder plates and guards, two light steel shoulder balls, the long
light D-gun on the right and the ochre-striped gauntlet on the left, both reaching forward."""
import math

UNIT = dict(
    skeleton='biped',
    skeleton_opts=dict(hipx=6.8),
    res=1024,
    wreck=dict(seed=33, drop=['r_dgun'], remove=[]),
    preview_pose={},
)


def heavy_legs(k, width=1.6):
    """standard legs + T2 extras on the source (right) leg; the clones carry them to the left leg."""
    from mathutils import Vector
    k.standard_legs(width=width)
    H = k.P['pelvis'].y
    w = 0.11 * H * width
    kn = Vector(k.T['rleg']['off']); an = Vector(k.T['rfoot']['off'])
    t = k.piece('rthigh'); A = t.at
    t.hull([A(x, kn.y + dy, kn.z + dz) for x in (-1.2 * w, 1.2 * w) for dy, dz in
            [(1.4, -0.3), (0.3, -2.4), (-1.6, -1.8), (-1.8, 0.6), (0.6, 1.4)]], 'paint2', bevel=0.16)
    l = k.piece('rleg'); B = lambda x, y, z: Vector(l.at(x, y, z))
    d = an.normalized(); L = an.length
    l.cyl(B(-1.05 * w, 0, 0) + d * 0.18 * L, B(-1.05 * w, 0, 0) + d * 0.8 * L, 0.6, 8, 'steel')
    l.cyl(B(-1.05 * w, 0, 0) + d * 0.12 * L, B(-1.05 * w, 0, 0) + d * 0.42 * L, 0.95, 8, 'dark', bevel=0.05)
    n = Vector((0, d.z, -d.y))
    l.hull([B(x, 0, 0) + d * s * L + n * (0.06 * H + e) for x in (-0.75 * w, 0.75 * w) for s in (0.15, 0.78) for e in (0, 0.8)],
           'paint', bevel=0.16)
    f = k.piece('rfoot'); C = f.at
    g = -k.T['rfoot']['gpos'][1]
    for x in (-0.75 * w, 0.75 * w):
        f.hull([C(x + dx, y, z) for dx in (-0.35 * w, 0.35 * w) for y, z in
                [(g, 0.36 * H), (g, 0.52 * H), (g + 0.07 * H, 0.32 * H), (g + 0.03 * H, 0.5 * H)]], 'dark', bevel=0.08)
    f.hull([C(dx, y, z) for dx in (-0.4 * w, 0.4 * w) for y, z in
            [(g, -0.26 * H), (g, -0.42 * H), (g + 0.09 * H, -0.24 * H)]], 'dark', bevel=0.08)


def build(k):
    heavy_legs(k, width=1.2)

    # ------------------------------------------------------------------ pelvis (0, 34, 0)
    p = k.piece('pelvis'); Q = p.at
    p.hull([Q(x * sx, y, z) for sx in (-1, 1) for x, y, z in
            [(8.6, -7.6, -6.4), (8.6, -7.6, 6.2), (9.8, -1.0, -7.4), (9.8, -1.0, 7.4), (6.4, 0.2, -6.8), (6.4, 0.2, 6.8),
             (4.6, -10.0, -4.0), (4.6, -10.0, 4.4)]], 'paint2', bevel=0.3)
    p.hull([Q(x * sx, y, z) for sx in (-1, 1) for x, y, z in                            # ochre codpiece
            [(2.6, -9.4, 5.4), (3.2, -2.0, 7.6), (2.6, -9.2, 5.7), (3.2, -2.0, 7.9), (1.2, -10.4, 4.6)]], 'hazard', bevel=0.1)

    # ------------------------------------------------------------------ chest (0, 36.46, 0.73)
    c = k.piece('chest'); C = c.at
    c.hull([C(x * sx, y, z) for sx in (-1, 1) for x, y, z in
            [(7.8, -2.2, -7.6), (7.8, -2.2, 6.8), (11.6, 5.0, -9.0), (11.6, 5.0, 8.4), (10.6, 11.4, -8.4), (9.4, 11.4, 6.6),
             (5.0, 13.4, -7.0), (5.0, 13.4, 5.0), (5.4, 4.0, 9.8)]], 'paint', bevel=0.34)
    c.hull([C(x * sx, y, z) for sx in (-1, 1) for x, y, z in                            # chest plate (darker)
            [(4.0, 0.0, 8.6), (4.8, 7.6, 8.4), (4.0, 0.0, 8.9), (4.8, 7.6, 8.7), (0.0, -0.8, 9.6), (0.0, -0.6, 9.9)]],
           'paint2', bevel=0.08)
    c.box(C(-1.4, 2.4, 9.4), C(1.4, 4.6, 9.75), 'lightr', bevel=0.0)
    for sx in (-1, 1):                                                                  # team shoulder plates
        c.hull([C(sx * x, y, z) for x, y, z in
                [(5.6, 13.3, -5.8), (5.6, 13.3, 3.8), (9.6, 11.6, -6.6), (9.0, 11.6, 4.8),
                 (5.6, 13.46, -5.75), (5.6, 13.46, 3.75), (9.6, 11.76, -6.55), (9.0, 11.76, 4.75)]], 'team', bevel=0.03)
    c.box(C(-4.2, 13.42, -6.4), C(4.2, 13.58, -3.0), 'team', bevel=0.03)              # team plate behind the head
    for x in (-3.6, 0.0, 3.6):                                                          # ridged back pack
        c.hull([C(x + dx, y, z) for dx in (-1.2, 1.2) for y, z in [(1.0, -8.6), (11.0, -8.0), (9.6, -12.4), (2.4, -12.4)]],
               'paint2', bevel=0.14)
    for x in (-2.4, 2.4):
        c.cyl(C(x, 11.0, -10.6), C(x, 15.4, -11.4), 0.9, 8, 'dark', bevel=0.04)          # exhaust stacks
        c.cyl(C(x, 15.3, -11.38), C(x, 15.5, -11.42), 0.6, 8, 'black')

    # ------------------------------------------------------------------ head (0, 45.46, 1.77)
    h = k.piece('head'); H = h.at
    h.hull([H(x * sx, y, z) for sx in (-1, 1) for x, y, z in
            [(3.6, 0.4, -4.0), (3.6, 0.4, 3.0), (3.2, 5.0, -3.6), (3.0, 5.6, 2.0), (2.2, 6.8, -1.6), (2.6, 2.6, 3.8)]],
           'paint2', bevel=0.2)
    h.hull([H(x * sx, y, z) for sx in (-1, 1) for x, y, z in
            [(2.8, 2.2, 3.5), (2.6, 3.8, 3.2), (2.8, 2.2, 3.8), (2.6, 3.8, 3.5)]], 'lightr', bevel=0.0)
    h.hull([H(x, y, z) for x in (-0.6, 0.6) for y, z in [(6.6, 1.6), (7.4, -0.6), (7.0, -3.8), (6.0, -4.2)]], 'hazard', bevel=0.06)

    # ------------------------------------------------------------------ shoulders (ball joints + guards)
    for name, sx in (('l_sho', 1), ('r_sho', -1)):
        s = k.piece(name); S = lambda x, y, z: s.at(sx * x, y, z)
        s.sphere(S(0.0, 0.0, 0.0), 4.6, 'steel', segs=12, rings=8)
        s.hull([S(x, y, z) for x, y, z in
                [(-2.0, 3.0, -4.8), (-2.0, 3.0, 4.6), (3.8, 1.4, -4.6), (3.8, 1.4, 4.4), (-3.6, 5.0, -3.8), (-3.6, 5.0, 3.6),
                 (2.6, 4.4, -3.6), (2.6, 4.4, 3.4)]], 'paint2', bevel=0.16)
        s.hull([S(x, y + dy, z) for dy in (0.06, 0.22) for x, y, z in                    # team plate on the guard
                [(-3.0, 4.94, -3.0), (-3.0, 4.94, 2.9), (2.0, 4.46, -2.8), (2.0, 4.46, 2.7)]], 'team', bevel=0.03)
        s.hull([S(x, y, z) for x, y, z in [(-0.6, -2.0, -2.0), (0.6, -2.0, -2.0), (-0.6, -2.0, 2.0), (0.6, -2.0, 2.0),
                                           (-0.4, -8.6, -1.6), (0.4, -8.6, -1.6), (-0.4, -8.6, 1.6), (0.4, -8.6, 1.6)]],
               'dark', bevel=0.1)

    # ------------------------------------------------------------------ left gauntlet (l_nano, 14.4, 34.42, 0.15)
    n = k.piece('l_nano'); N = n.at                    # laser mlasflsh (0.27, 0, 15.99), spray (-0.27, 0, 16.26)
    n.cyl(N(-2.6, 0, 0), N(2.6, 0, 0), 2.4, 10, 'dark', bevel=0.06)
    n.hull([N(x * sx, y, z) for sx in (-1, 1) for x, y, z in
            [(4.6, -4.4, -0.8), (4.6, 4.6, -0.8), (5.6, -5.2, 6.0), (5.6, 5.4, 6.0), (4.0, -3.6, 12.8), (4.0, 3.8, 12.8)]],
           'paint', bevel=0.3)
    for z in (3.0, 8.0):
        n.hull([N(x * sx, y, zz) for sx in (-1, 1) for x, y, zz in
                [(5.0, 5.0, z), (5.0, 5.0, z + 1.4), (5.25, 5.2, z), (5.25, 5.2, z + 1.4)]], 'hazard', bevel=0.02)
    n.hull([N(x, y + dy, z) for x in (-3.2, 3.2) for dy in (0.08, 0.22) for y, z in [(4.75, 0.5), (5.4, 6.0), (4.22, 11.0)]],
           'team', bevel=0.03)                                                           # team top of the gauntlet
    n.cyl(N(0, 0, 12.6), N(0, 0, 15.6), 2.0, 10, 'steel', r2=1.2)
    n.cyl(N(0, 0, 15.5), N(0, 0, 16.4), 1.0, 10, 'lightc')

    # ------------------------------------------------------------------ D-gun (r_dgun, -14.4, 34.42, 0.15)
    g = k.piece('r_dgun'); G = g.at                    # muzzle bigflsh at (0, 4.24, 23.39)
    g.cyl(G(-2.4, 0, 0), G(2.4, 0, 0), 2.4, 10, 'dark', bevel=0.06)
    g.hull([G(x * sx, y, z) for sx in (-1, 1) for x, y, z in
            [(3.4, -2.2, -0.8), (3.4, 6.4, -0.8), (3.4, -2.0, 9.0), (3.4, 6.4, 9.0), (2.4, -1.0, 12.0), (2.4, 6.0, 12.0)]],
           'paint2', bevel=0.24)
    g.box(G(-2.2, 6.38, 0.5), G(2.2, 6.54, 6.0), 'team', bevel=0.03)                 # team plate on the D-gun housing
    g.cyl(G(0, 4.24, 8.0), G(0, 4.24, 22.4), 2.0, 12, 'steel')
    for z in (13.0, 17.0):
        g.cyl(G(0, 4.24, z), G(0, 4.24, z + 1.0), 2.45, 12, 'dark')
    g.cyl(G(0, 4.24, 22.2), G(0, 4.24, 23.4), 2.6, 12, 'dark', bevel=0.06)
    g.cyl(G(0, 4.24, 23.35), G(0, 4.24, 23.5), 1.6, 12, 'black')
