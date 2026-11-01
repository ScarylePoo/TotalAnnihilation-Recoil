"""Shooter (ARM_T2_BOT_Shooter) - Arm T2 sniper kbot. A tall lanky walker with TA's big V-shaped chest, slab
shoulder guards, a hooded head with one large cyan scope eye, and a long sniper rifle carried low in the right hand.
To fire it shoulders the rifle: the arm comes up, the rifle turns level, the barrel housing (sleave) flips round, the
barrel telescopes out 9 elmo and the scope drops into place; idle it reverses. Standard biped skeleton; script ported
to scripts/ARM_T2_BOT_Shooter.lua. Coordinates are ENGINE/global: X right, Y up, Z forward.
Top view (what makes it a Shooter): a wide light V/arrowhead chest with two team plates on its shoulders, a dark
hood in front, and the thin dark rifle - the tallest, narrowest-legged Arm kbot."""
import math

UNIT = dict(
    skeleton='biped',
    skeleton_opts=dict(hipx=3.6),
    res=1024,
    wreck=dict(seed=14, drop=['gun'], remove=[]),
    preview_pose={},
)


def build(k):
    k.standard_legs(width=1.3)

    # ------------------------------------------------------------------ pelvis (0, 18.95, 0)
    p = k.piece('pelvis'); Q = p.at
    p.hull([Q(x * sx, y, z) for sx in (-1, 1) for x, y, z in
            [(3.0, -2.6, -2.6), (3.0, -2.6, 2.4), (3.4, 1.4, -3.0), (3.4, 1.4, 2.8), (1.8, -3.4, -1.8), (1.8, -3.4, 1.6)]],
           'paint2', bevel=0.16)
    p.cyl(Q(0, 1.0, -0.6), Q(0, 3.4, -0.6), 2.2, 10, 'dark', bevel=0.06)               # waist joint

    # ------------------------------------------------------------------ torso (0, 27.95, -0.85): V chest
    t = k.piece('torso'); A = t.at
    t.hull([A(x * sx, y, z) for sx in (-1, 1) for x, y, z in
            [(8.6, 6.0, -4.6), (8.6, 6.0, 3.2), (7.4, 7.8, -4.0), (7.4, 7.8, 2.4), (2.4, 7.4, -4.8), (2.4, 7.4, 4.6),
             (1.8, -6.8, -2.6), (1.8, -6.8, 2.4), (4.2, 0.6, 4.8), (4.2, 0.6, -5.4)]], 'paint', bevel=0.24)
    t.hull([A(x * sx, y, z) for sx in (-1, 1) for x, y, z in                          # dark keel down the front
            [(1.4, -6.4, 2.6), (2.2, 2.0, 4.8), (1.4, -6.4, 2.8), (2.2, 2.0, 5.0), (0.6, 3.4, 5.2), (0.6, 3.4, 5.0)]],
           'paint2', bevel=0.06)
    t.hull([A(x, y, z) for x, y, z in                                                  # team plates on the shoulder tops
            [(4.4, 7.66, -3.6), (7.2, 7.84, -3.4), (4.4, 7.66, 2.2), (7.2, 7.84, 1.9),
             (4.4, 7.82, -3.55), (7.15, 8.0, -3.35), (4.4, 7.82, 2.15), (7.15, 8.0, 1.85)]], 'team', bevel=0.03, mirror=True)
    t.box(A(-2.6, 0.4, -6.2), A(2.6, 6.4, -4.6), 'dark', bevel=0.1)                   # back power pack
    for y in (1.4, 2.8, 4.2):
        t.box(A(-2.2, y, -6.45), A(2.2, y + 0.5, -6.1), 'black', bevel=0.0)

    # ------------------------------------------------------------------ head (0, 31.32, 3.52): hood + scope eye
    h = k.piece('head'); H = h.at
    h.hull([H(x * sx, y, z) for sx in (-1, 1) for x, y, z in
            [(3.4, 0.4, -4.4), (3.4, 0.4, 3.8), (3.8, 4.0, -4.8), (3.4, 4.6, 3.0), (2.4, 6.4, -3.6), (2.0, 6.2, 1.4),
             (2.6, 2.0, 5.2)]], 'paint2', bevel=0.2)
    h.cyl(H(1.2, 2.8, 3.6), H(1.2, 2.8, 6.0), 1.5, 10, 'dark', bevel=0.06)            # scope eye, offset right of centre
    h.cyl(H(1.2, 2.8, 5.95), H(1.2, 2.8, 6.15), 1.05, 10, 'lightc')
    h.box(H(-2.6, 2.2, 4.5), H(-0.6, 2.8, 4.75), 'lightc', bevel=0.0)
    h.hull([H(x, y, z) for x in (-0.5, 0.5) for y, z in [(6.3, 1.0), (6.9, -0.4), (6.7, -3.6), (6.2, -3.8)]], 'dark', bevel=0.06)

    # ------------------------------------------------------------------ arms: left built, right = mirrored clones
    lu = k.piece('luparm'); V = lu.at                  # (7.16, 33.08, -3.85); elbow at (2.89, -8.55, 0)
    lu.hull([V(x, y, z) for x, y, z in                                                 # tall slab shoulder guard
             [(0.6, 6.4, -2.8), (0.6, 6.4, 2.8), (4.6, 4.8, -2.8), (4.6, 4.8, 2.8), (0.8, -2.4, -2.6), (0.8, -2.4, 2.6),
              (4.8, -4.0, -2.6), (4.8, -4.0, 2.6)]], 'paint', bevel=0.2)
    lu.hull([V(x, y, z) for x, y, z in
             [(2.0, -3.0, -1.4), (2.0, -3.0, 1.4), (3.8, -3.0, -1.4), (3.8, -3.0, 1.4),
              (2.1, -8.6, -1.2), (2.1, -8.6, 1.2), (3.6, -8.6, -1.2), (3.6, -8.6, 1.2)]], 'dark', bevel=0.1)
    la = k.piece('larm'); W = la.at                    # (10.05, 24.53, -3.85): forearm
    la.cyl(W(-1.5, 0, 0), W(1.5, 0, 0), 1.5, 10, 'dark', bevel=0.05)
    la.hull([W(x, y, z) for x, y, z in
             [(-1.6, -0.8, -1.7), (1.6, -0.8, -1.7), (-1.6, -0.8, 1.8), (1.6, -0.8, 1.8),
              (-1.9, -5.0, -2.0), (1.9, -5.0, -2.0), (-1.9, -5.0, 2.1), (1.9, -5.0, 2.1),
              (-1.4, -9.0, -1.5), (1.4, -9.0, -1.5), (-1.4, -9.0, 1.6), (1.4, -9.0, 1.6)]], 'paint2', bevel=0.12)
    k.clone('ruparm', 'luparm', mirror_x=True)
    k.clone('rarm', 'larm', mirror_x=True)
    hd = k.piece('lhand'); HD = hd.at                  # (10.05, 14.59, -3.85)
    hd.hull([HD(x, y, z) for x in (-1.3, 1.4) for y in (0.6, -3.0) for z in (-1.3, 1.6)], 'dark', bevel=0.12)

    # ------------------------------------------------------------------ the rifle (in the right hand)
    g = k.piece('gun'); G = g.at                       # (-10.37, 11.91, -3.95): receiver + stock along z
    g.hull([G(x, y, z) for x in (-1.5, 1.5) for y, z in
            [(-1.6, -5.2), (1.4, -5.2), (2.0, -1.0), (2.0, 4.0), (-1.4, 4.4), (-2.2, 0.4)]], 'dark', bevel=0.14)
    g.hull([G(x, y, z) for x in (-1.2, 1.2) for y, z in [(-1.0, -5.0), (0.8, -5.0), (0.4, -7.0), (-1.4, -7.0)]], 'paint2', bevel=0.1)
    g.box(G(-1.0, 2.0, -0.4), G(1.0, 2.2, 3.4), 'team', bevel=0.02)
    sc = k.piece('scope'); SC = sc.at                  # (-10.37, 12.34, -3.95)
    sc.cyl(SC(0, -2.6, -3.8), SC(0, -2.6, 3.8), 0.9, 10, 'dark', bevel=0.04)
    sc.cyl(SC(0, -2.6, 3.75), SC(0, -2.6, 3.95), 0.6, 10, 'lightc')
    sc.box(SC(-0.5, -1.8, -1.0), SC(0.5, -0.1, 1.0), 'dark', bevel=0.04)
    sl = k.piece('sleave'); SL = sl.at                 # (-10.37, 6.46, -9.51): barrel housing along +z
    sl.cyl(SL(0, -0.64, -0.3), SL(0, -0.64, 11.6), 1.35, 10, 'paint2', bevel=0.06)
    sl.cyl(SL(0, -0.64, 2.0), SL(0, -0.64, 3.2), 1.6, 10, 'dark')
    sl.cyl(SL(0, -0.64, 11.4), SL(0, -0.64, 11.8), 0.95, 10, 'dark')
    b = k.piece('barrel'); B = b.at                    # (-10.37, 5.82, -8.87): telescopes out 9 along z
    b.cyl(B(0, 0, 0.2), B(0, 0, 8.6), 0.7, 8, 'steel')
    b.cyl(B(0, 0, 7.8), B(0, 0, 8.8), 0.95, 8, 'dark', bevel=0.03)
