"""Shooter (ARM_T2_BOT_Shooter) - Arm T2 sniper kbot. A tall lanky walker with TA's big V-shaped chest, slab
shoulder guards, a hooded head with one large cyan scope eye, and a long scoped sniper rifle carried at the waist in the right hand.
To fire it shoulders the rifle, level all the way (the gun piece counter-turns the arm), and the barrel telescopes out 9 elmo; idle it reverses. Standard biped skeleton; script ported
to scripts/ARM_T2_BOT_Shooter.lua. Coordinates are ENGINE/global: X right, Y up, Z forward.
Top view (what makes it a Shooter): a wide light V/arrowhead chest with two team plates on its shoulders and team
tops on the slab shoulder guards, a dark
hood in front, and the thin dark rifle - the tallest, narrowest-legged Arm kbot."""
import math

UNIT = dict(
    skeleton='biped',
    # the rifle layout is the kit's, not the 3DO's: gun at the hand, barrel on the receiver's axis, muzzle at the longer barrel's tip
    skeleton_opts=dict(hipx=3.6,
                       move={'gun': (-9.8, 14.6, -3.95), 'sleave': (-9.8, 16.74, 0.55), 'flash': (-9.8, 16.1, 13.19)},
                       emit={'flash': [(0, 0, 0), (0, 0, 1)]}),
    res=1024,
    wreck=dict(seed=14, drop=['gun'], remove=[]),
    preview_pose={'ruparm': (-15, 0, 0), 'rarm': (-60, 0, 0), 'gun': (75, 0, 0)},      # idle carry, the pose it spends most time in
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
    gy = lambda x: 6.4 - (x - 0.6) * 0.4                                               # guard top slope, normal (0.371, 0.928)
    lu.hull([V(x + 0.371 * d, gy(x) + 0.928 * d, z) for x in (1.0, 4.2) for z in (-2.4, 2.4) for d in (0.06, 0.2)],
            'team', bevel=0.03)                                                        # team plate on the guard top
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

    # ------------------------------------------------------------------ the rifle (ball grip in the right hand, barrel in line with the receiver)
    g = k.piece('gun'); G = g.at                       # at the hand: pivots freely, the script keeps it level as the arm moves
    g.sphere(G(0, 0, 0), 2.0, 'dark')                  # the grip, so forearm and rifle join at any angle
    g.hull([G(x, y, z) for x in (-1.5, 1.5) for y, z in                                  # receiver
            [(0.2, -3.2), (3.0, -3.2), (3.0, 4.8), (0.2, 4.8)]], 'dark', bevel=0.12)
    g.hull([G(x, y, z) for x in (-1.0, 1.0) for y, z in                                  # stock, reaches back to the shoulder
            [(0.6, -3.0), (2.6, -3.0), (2.2, -8.6), (-0.8, -9.4), (0.8, -9.4)]], 'paint2', bevel=0.1)
    g.box(G(-1.2, -1.8, -9.5), G(1.2, 2.4, -8.9), 'dark', bevel=0.05)                    # butt plate
    g.box(G(-0.8, -2.8, 1.2), G(0.8, 0.4, 3.0), 'dark', bevel=0.06)                      # magazine
    g.box(G(-1.2, 3.02, -2.8), G(1.2, 3.2, 1.0), 'team', bevel=0.02)
    sc = k.piece('scope'); SC = sc.at                  # gun + (0, 0.4, 0): long scope on top, what makes it read as a sniper rifle
    sc.cyl(SC(0, 3.9, -3.0), SC(0, 3.9, 5.2), 0.85, 10, 'dark', bevel=0.04)
    sc.cyl(SC(0, 3.9, 5.15), SC(0, 3.9, 5.35), 0.5, 10, 'lightc')
    sc.box(SC(-0.5, 2.5, -1.4), SC(0.5, 3.6, 2.6), 'dark', bevel=0.04)
    sl = k.piece('sleave'); SL = sl.at                 # barrel housing along +z, on the receiver's axis
    sl.cyl(SL(0, -0.64, -0.3), SL(0, -0.64, 14.6), 1.25, 10, 'paint2', bevel=0.06)
    for z in (1.6, 8.2):
        sl.cyl(SL(0, -0.64, z), SL(0, -0.64, z + 1.2), 1.55, 10, 'dark')
    sl.cyl(SL(0, -0.64, 14.4), SL(0, -0.64, 14.9), 0.95, 10, 'dark')
    sl.box(SL(-1.0, 0.56, 3.0), SL(1.0, 0.76, 8.0), 'team', bevel=0.02)                  # team along the housing's top: the rifle reads from above
    sl.box(SL(-1.0, 0.56, 9.6), SL(1.0, 0.76, 14.0), 'team', bevel=0.02)
    b = k.piece('barrel'); B = b.at                    # telescopes out 9 along z when the rifle comes up
    b.cyl(B(0, 0, 0.2), B(0, 0, 12.0), 0.7, 8, 'steel')
    b.cyl(B(0, 0, 11.0), B(0, 0, 12.2), 1.05, 8, 'dark', bevel=0.03)
