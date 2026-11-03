"""Core Commander (CORE_Commander) - the Core's most important unit. Remodelled to the third-party S3O's piece layout (kept in
tools/s3okit/ref/, the script drives those pieces). Commander-class biped, the tallest Core walker: a massive square chest
with a ridged back pack and stacks behind a raised collar, light steel ball shoulders, red-visored small helmet, a long
D-gun as the right forearm (r_dgun) and a heavy nano/laser gauntlet as the left (l_nano), both reaching FORWARD (the Arm's hang).
Standard biped skeleton; script ported to scripts/CORE_Commander.lua (no corpse: commanders explode). The decoy
(units/CORE_T2_BOT_DecoyCommander.py) loads this spec, so the two cannot drift apart.
Coordinates are ENGINE/global: X right, Y up, Z fwd.
Top view: broad dark-warm chest with team shoulder plates and guards, two light steel balls, long light D-gun on the right and,
on the left, a gauntlet whose front half is the only hazard block (nano side), smaller than a pure constructor's."""
import math

UNIT = dict(
    skeleton='biped',
    skeleton_opts=dict(hipx=6.8),
    res=2048,
    hazard_period=2.5,                # stripes must show on the deliberately small gauntlet plate
    wreck=dict(seed=33, drop=['r_dgun'], remove=[]),        # unused while the def has no corpse
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
    p.hull([Q(x * sx, y, z) for sx in (-1, 1) for x, y, z in                            # codpiece
            [(2.6, -9.4, 5.4), (3.2, -2.0, 7.6), (2.6, -9.2, 5.7), (3.2, -2.0, 7.9), (1.2, -10.4, 4.6)]], 'paint', bevel=0.1)

    # ------------------------------------------------------------------ chest (0, 36.46, 0.73)
    c = k.piece('chest'); C = c.at
    # a square box (the Arm's chest is rounded), its top a trench: the helmet sits low between two shoulder blocks
    c.hull([C(x * sx, y, z) for sx in (-1, 1) for x, y, z in
            [(7.8, -2.2, -7.6), (7.8, -2.2, 6.8), (11.6, 4.0, -9.2), (11.6, 4.0, 8.6), (11.6, 9.4, -9.2), (11.6, 9.4, 8.6)]],
           'paint', bevel=0.3)
    for sx in (-1, 1):
        c.hull([C(sx * x, y, z) for x, y, z in
                [(4.6, 9.0, -9.0), (4.6, 9.0, 8.2), (11.4, 9.0, -9.0), (11.4, 9.0, 8.2),
                 (4.8, 14.2, -8.4), (4.8, 14.2, 7.0), (11.0, 13.4, -8.4), (11.0, 13.4, 7.0)]], 'paint', bevel=0.26)
        c.hull([C(sx * x, y + dy, z) for dy in (0.08, 0.24) for x, y, z in                # team plate on the block's top
                [(5.5, 14.15, -7.0), (5.5, 14.15, 6.3), (10.3, 13.53, -7.0), (10.3, 13.53, 6.3)]], 'team', bevel=0.03)
    c.hull([C(x * sx, y, z) for sx in (-1, 1) for x, y, z in                            # chest plate (darker) with the X brace
            [(7.0, 0.6, 8.7), (7.0, 8.4, 8.7), (7.0, 0.6, 9.0), (7.0, 8.4, 9.0)]], 'paint2', bevel=0.08)
    for sx in (-1, 1):
        c.hull([C(sx * x, y, z) for x, y, z in
                [(6.2, 1.0, 9.0), (4.6, 1.0, 9.0), (6.2, 1.0, 9.3), (4.6, 1.0, 9.3),
                 (-4.6, 8.0, 9.0), (-6.2, 8.0, 9.0), (-4.6, 8.0, 9.3), (-6.2, 8.0, 9.3)]], 'dark', bevel=0.03)
    c.box(C(-1.5, 3.3, 9.25), C(1.5, 5.7, 9.5), 'lightr', bevel=0.0)
    c.hull([C(x * sx, y, z) for sx in (-1, 1) for x, y, z in                            # steel collar closing the trench behind the helmet
            [(4.4, 9.2, -3.4), (4.4, 9.2, -8.6), (4.2, 16.6, -5.2), (4.2, 16.6, -7.6), (4.4, 13.0, -3.0)]], 'steel', bevel=0.14)
    for x in (-5.4, 0.0, 5.4):                                                          # ridged back pack, team-capped
        c.hull([C(x + dx, y, z) for dx in (-1.7, 1.7) for y, z in [(1.0, -8.8), (11.6, -8.6), (10.2, -13.2), (2.4, -13.2)]],
               'paint2', bevel=0.14)
        c.hull([C(x + dx, y + dy, z) for dx in (-1.25, 1.25) for dy in (0.08, 0.22) for y, z in [(11.56, -9.2), (10.36, -12.9)]],
               'team', bevel=0.03)
    for x in (-2.7, 2.7):
        c.cyl(C(x, 11.0, -11.4), C(x, 18.4, -12.2), 1.0, 8, 'dark', bevel=0.04)         # exhaust stacks
        c.cyl(C(x, 18.3, -12.18), C(x, 18.5, -12.22), 0.68, 8, 'black')

    # ------------------------------------------------------------------ head (0, 45.46, 1.77)
    h = k.piece('head'); H = h.at
    h.hull([H(x * sx, y, z) for sx in (-1, 1) for x, y, z in
            [(3.6, 0.4, -4.0), (3.6, 0.4, 3.0), (3.2, 5.0, -3.6), (3.0, 5.6, 2.0), (2.2, 6.8, -1.6), (2.6, 2.6, 3.8)]],
           'paint2', bevel=0.2)
    h.hull([H(x * sx, y, z) for sx in (-1, 1) for x, y, z in
            [(2.8, 2.2, 3.5), (2.6, 3.8, 3.2), (2.8, 2.2, 3.8), (2.6, 3.8, 3.5)]], 'lightr', bevel=0.0)
    h.hull([H(x, y, z) for x in (-0.6, 0.6) for y, z in [(6.6, 1.6), (7.8, -0.6), (7.4, -3.8), (6.0, -4.2)]], 'team', bevel=0.06)

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
    n.hull([N(x, y + dy, z) for x in (-3.2, 3.2) for dy in (0.08, 0.22) for y, z in [(5.15, 5.2), (4.22, 11.8)]],
           'hazard', bevel=0.03)                                                         # nano side: the gauntlet's visible front half
    n.cyl(N(0, 0, 12.6), N(0, 0, 15.6), 2.0, 10, 'steel', r2=1.2)
    n.cyl(N(0, 0, 15.5), N(0, 0, 16.4), 1.0, 10, 'lightc')

    # ------------------------------------------------------------------ D-gun (r_dgun, -14.4, 34.42, 0.15)
    g = k.piece('r_dgun'); G = g.at                    # muzzle bigflsh at (0, 4.24, 23.39)
    g.cyl(G(-2.4, 0, 0), G(2.4, 0, 0), 2.4, 10, 'dark', bevel=0.06)
    g.hull([G(x * sx, y, z) for sx in (-1, 1) for x, y, z in
            [(3.4, -2.2, -0.8), (3.4, 6.4, -0.8), (3.4, -2.0, 9.0), (3.4, 6.4, 9.0), (2.4, -1.0, 12.0), (2.4, 6.0, 12.0)]],
           'paint2', bevel=0.24)
    g.hull([G(x, y, z) for x in (-2.5, 2.5) for y in (6.5, 6.66) for z in (3.8, 9.0)], 'team', bevel=0.03)   # team plate on the D-gun housing
    g.cyl(G(0, 4.24, 8.0), G(0, 4.24, 22.4), 2.0, 12, 'steel')
    for z in (13.0, 17.0):
        g.cyl(G(0, 4.24, z), G(0, 4.24, z + 1.0), 2.45, 12, 'dark')
    g.cyl(G(0, 4.24, 22.2), G(0, 4.24, 23.4), 2.6, 12, 'dark', bevel=0.06)
    g.cyl(G(0, 4.24, 23.35), G(0, 4.24, 23.5), 1.6, 12, 'black')
