"""Necro (CORE_T2_BOT_Necro) - Core T2 resurrection kbot. A gaunt walker with TA's V-shaped chest and a long hooded
skull of a head jutting forward and up (red eyes), angular shoulder blades, a three-clawed left hand (finger1/2,
thumb) and a long conical resurrection lathe as the right forearm. To work it raises both arms and bows its head
(COB keyframes). Standard biped skeleton; script ported to scripts/CORE_T2_BOT_Necro.lua.
Coordinates are ENGINE/global: X right, Y up, Z forward.
Top view (what makes it a Necro): a long pale steel skull pointing forward over a dark warm V chest, two team-topped
shoulder blades, the light steel lathe cone on the right and the claw on the left - spiky, unlike any Core combat kbot."""
import math

UNIT = dict(
    skeleton='biped',
    skeleton_opts=dict(hipx=4.6),
    res=1024,
    wreck=dict(seed=24, drop=['lathe'], remove=[]),
    preview_pose={},
)


def build(k):
    k.standard_legs(width=1.45)

    # ------------------------------------------------------------------ pelvis (0, 17.5, 0)
    p = k.piece('pelvis'); Q = p.at
    p.hull([Q(x * sx, y, z) for sx in (-1, 1) for x, y, z in
            [(3.6, -2.4, -2.8), (3.6, -2.4, 2.6), (4.0, 1.0, -3.2), (4.0, 1.0, 3.0), (2.0, -3.4, -2.0), (2.0, -3.4, 1.8)]],
           'paint2', bevel=0.16)

    # ------------------------------------------------------------------ torso (0, 14, -0.5): V chest + spine
    t = k.piece('torso'); A = t.at
    t.cyl(A(0, 3.0, 0), A(0, 6.6, 0), 2.4, 10, 'dark', bevel=0.06)                    # waist / spine
    t.hull([A(x * sx, y, z) for sx in (-1, 1) for x, y, z in                           # V chest
            [(1.6, 5.4, -3.0), (1.6, 5.4, 3.4), (7.0, 12.0, -4.6), (7.0, 12.0, 4.0), (6.4, 14.4, -4.2), (6.4, 14.4, 3.2),
             (2.4, 14.4, -4.6), (2.4, 14.4, 4.6), (2.6, 9.6, 5.6)]], 'paint', bevel=0.22)
    for y in (8.4, 10.0, 11.6):                                                         # ochre ribs across the chest
        t.hull([A(x * sx, yy, z) for sx in (-1, 1) for x, yy, z in
                [(0.6 + (y - 5.4) * 0.6, y, 4.5 + (y - 8.4) * 0.12), (0.6 + (y - 5.4) * 0.6, y + 0.6, 4.6 + (y - 8.4) * 0.12),
                 (0.6 + (y - 5.4) * 0.6, y, 4.8 + (y - 8.4) * 0.12), (0.6 + (y - 5.4) * 0.6, y + 0.6, 4.9 + (y - 8.4) * 0.12)]],
               'hazard', bevel=0.02)
    t.hull([A(x * sx, y, z) for sx in (-1, 1) for x, y, z in                           # back plate / power pack
            [(3.6, 7.4, -3.6), (5.0, 13.6, -4.4), (3.0, 8.0, -6.6), (4.2, 13.0, -6.8)]], 'paint2', bevel=0.16)
    for x in (-2.4, 2.4):
        t.cyl(A(x, 13.4, -5.6), A(x, 16.0, -6.4), 0.6, 8, 'dark')                        # vent horns

    # ------------------------------------------------------------------ head (0, 23.5, 3.5): long hooded skull
    h = k.piece('head'); H = h.at
    h.hull([H(x * sx, y, z) for sx in (-1, 1) for x, y, z in
            [(3.2, -3.4, -4.6), (3.4, -1.0, 2.6), (2.6, 2.8, -5.4), (2.4, 5.4, 4.6), (1.4, 10.6, 11.0), (1.2, 7.4, 12.4),
             (2.6, -2.6, 5.4)]], 'steel', bevel=0.2)
    h.hull([H(x * sx, y, z) for sx in (-1, 1) for x, y, z in                           # dark hood rim
            [(3.3, -3.5, -4.0), (3.5, -1.1, 2.4), (3.6, -3.0, 1.0), (2.8, 2.6, -4.8), (2.9, 2.8, -3.6)]], 'dark', bevel=0.1)
    h.hull([H(x * sx, y, z) for sx in (-1, 1) for x, y, z in                           # face (dark) with red eyes
            [(2.4, -2.2, 5.6), (2.0, 1.0, 6.8), (1.0, -2.6, 6.4), (1.0, 1.4, 7.6)]], 'dark', bevel=0.06)
    for sx in (-1.2, 1.2):
        h.cyl(H(sx, -0.4, 6.9), H(sx, -0.4, 7.5), 0.55, 8, 'lightr')
    h.hull([H(x, y, z) for x in (-0.55, 0.55) for y, z in [(5.6, 4.0), (6.4, 2.0), (11.0, 10.4), (10.6, 11.4)]], 'team', bevel=0.05)

    # ------------------------------------------------------------------ shoulder blades: left built, right = clone
    lu = k.piece('luparm'); V = lu.at                  # (5, 25.5, -3.5); larm at (7.5, -4, -2)
    lu.cyl(V(-0.6, 0, 0), V(2.0, 0, 0), 2.0, 10, 'dark', bevel=0.06)
    lu.hull([V(x, y, z) for x, y, z in
             [(0.8, 3.6, -3.2), (0.8, 3.6, 3.0), (8.4, 2.0, -2.8), (8.4, 2.0, 2.6), (2.0, -2.6, -3.0), (2.0, -2.6, 2.8),
              (8.2, -4.8, -2.2), (8.2, -4.8, 1.8)]], 'paint', bevel=0.18)
    lu.hull([V(x, y, z) for x, y, z in
             [(1.2, 3.58, -2.9), (1.2, 3.58, 2.7), (8.0, 2.15, -2.5), (8.0, 2.15, 2.3),
              (1.2, 3.74, -2.85), (1.2, 3.74, 2.65), (8.0, 2.31, -2.45), (8.0, 2.31, 2.25)]], 'team', bevel=0.03)
    k.clone('ruparm', 'luparm', mirror_x=True)
    la = k.piece('larm'); W = la.at                    # (12.5, 21.5, -5.5): forearm toward the claw
    la.cyl(W(-1.5, 0, 0), W(1.5, 0, 0), 1.5, 10, 'dark', bevel=0.05)
    la.hull([W(x, y, z) for x, y, z in
             [(-1.3, -0.6, -1.2), (1.6, -0.6, -1.2), (-1.3, 0.6, 1.4), (1.6, 0.6, 1.4),
              (-1.4, -8.6, 4.0), (4.4, -8.6, 4.0), (-1.4, -9.2, 6.6), (4.4, -9.2, 6.6), (1.4, -9.4, 1.0)]], 'paint2', bevel=0.16)
    for name, dx in (('finger1', 0.0), ('finger2', 0.0)):
        f = k.piece(name); F = f.at
        f.hull([F(x, y, z) for x, y, z in
                [(-1.0, 0.0, 0.2), (1.0, 0.0, 0.2), (-1.0, 0.0, 2.4), (1.0, 0.0, 2.4), (-0.6, -3.2, 3.6), (0.6, -3.2, 3.6),
                 (0.0, -6.2, 4.4), (0.0, -5.6, 2.6)]], 'dark', bevel=0.08)
    th = k.piece('thumb'); TH = th.at
    th.hull([TH(x, y, z) for x, y, z in
             [(-0.4, 0.2, -1.0), (0.6, 0.2, -1.0), (-0.4, 0.2, 1.2), (0.6, 0.2, 1.2), (-3.4, -3.0, 0.0), (-2.6, -4.8, 0.4)]],
            'dark', bevel=0.08)

    # ------------------------------------------------------------------ right forearm + lathe cone
    ra = k.piece('rarm'); R = ra.at                    # (-12.5, 21.5, -5.5)
    ra.cyl(R(-1.5, 0, 0), R(1.5, 0, 0), 1.5, 10, 'dark', bevel=0.05)
    ra.hull([R(x, y, z) for x, y, z in
             [(-1.6, -0.6, -1.2), (1.3, -0.6, -1.2), (-1.6, 0.6, 1.4), (1.3, 0.6, 1.4),
              (-4.4, -7.4, 1.0), (0.4, -7.4, 1.0), (-4.4, -7.4, 4.6), (0.4, -7.4, 4.6)]], 'paint2', bevel=0.16)
    lt = k.piece('lathe'); L = lt.at                   # (-15, 14, -2.5): cone down to the nano point
    lt.cyl(L(0, 0.4, 0), L(0, -2.6, 0), 4.2, 12, 'dark', bevel=0.12)
    lt.cyl(L(0, -2.4, 0), L(0, -11.6, 0), 3.4, 12, 'steel', r2=1.0)
    for y in (-4.6, -7.4):
        lt.cyl(L(0, y, 0), L(0, y - 0.7, 0), 3.4 - (abs(y) - 2.4) * 0.26 + 0.35, 12, 'dark')
    lt.cyl(L(0, -11.5, 0), L(0, -12.6, 0), 1.0, 10, 'lightc', r2=0.5)
