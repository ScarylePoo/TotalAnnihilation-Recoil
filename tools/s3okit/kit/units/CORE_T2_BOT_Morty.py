"""Morty (CORE_T2_BOT_Morty) - Core T2 mobile mortar kbot. The unit used a third-party S3O (preserved in
tools/s3okit/ref/); remodelled to its piece layout: a chunky torso with a small domed head and one red eye, an armoured
box pauldron on the right shoulder, and on the left a cradle (support) carrying a long heavy mortar tube (barrel) that
kicks back 12.5 elmo when it fires. A hip skirt (cod) over standard biped legs (skeleton); script ported to
scripts/CORE_T2_BOT_Morty.lua. Coordinates are ENGINE/global: X right, Y up, Z forward.
Top view (what makes it a Morty): a dark-warm block body with a team plate, a team-topped pauldron on one side and
a team-lidded cradle with a long fat LIGHT steel tube on the other reaching far forward - lopsided, one big gun."""
import math

UNIT = dict(
    skeleton='biped',
    skeleton_opts=dict(hipx=3.7),
    res=1024,
    wreck=dict(seed=28, drop=['barrel'], remove=[]),
    preview_pose={},
)


def build(k):
    k.standard_legs(width=1.6)

    # ------------------------------------------------------------------ pelvis (0, 16.4, 0) + hip skirt (cod)
    p = k.piece('pelvis'); Q = p.at
    p.hull([Q(x * sx, y, z) for sx in (-1, 1) for x, y, z in
            [(3.0, -2.0, -2.6), (3.0, -2.0, 2.4), (3.4, 1.6, -3.0), (3.4, 1.6, 2.8)]], 'dark', bevel=0.14)
    c = k.piece('cod'); C = c.at                       # (0, 19.45, -0.59)
    c.hull([C(x * sx, y, z) for sx in (-1, 1) for x, y, z in
            [(4.6, -0.2, -4.4), (4.6, -0.2, 4.4), (4.2, -3.0, -4.0), (4.2, -3.0, 4.2), (2.6, -5.4, 3.6), (2.6, -5.4, -2.6)]],
           'paint2', bevel=0.16)

    # ------------------------------------------------------------------ torso (0, 19.44, -0.6)
    t = k.piece('torso'); A = t.at
    t.hull([A(x * sx, y, z) for sx in (-1, 1) for x, y, z in
            [(4.8, 0.0, -6.6), (4.8, 0.0, 5.6), (6.1, 4.4, -7.4), (6.1, 4.4, 7.4), (5.4, 8.6, -6.6), (5.0, 8.6, 5.4),
             (3.4, 10.0, -4.6), (3.4, 10.0, 3.0)]], 'paint', bevel=0.24)
    t.hull([A(x * sx, y, z) for sx in (-1, 1) for x, y, z in                           # team plate on the chest top
            [(2.2, 10.02, -3.6), (2.2, 10.02, 2.2), (2.2, 10.18, -3.55), (2.2, 10.18, 2.15)]], 'team', bevel=0.03)
    t.hull([A(x * sx, y, z) for sx in (-1, 1) for x, y, z in                           # dark front grille
            [(3.6, 2.0, 7.4), (3.6, 5.6, 7.6), (3.6, 2.0, 7.65), (3.6, 5.6, 7.85)]], 'dark', bevel=0.05)
    for y in (2.8, 4.2):
        t.box(A(-3.0, y, 7.75), A(3.0, y + 0.5, 7.95), 'black', bevel=0.0)
    t.cyl(A(-3.6, 5.0, -7.2), A(3.6, 5.0, -7.2), 2.8, 10, 'paint2', bevel=0.12)         # ammo drum on the back
    for x in (-2.0, 2.0):
        t.cyl(A(x - 0.4, 5.0, -7.2), A(x + 0.4, 5.0, -7.2), 2.95, 10, 'hazard')

    # ------------------------------------------------------------------ head + eye
    h = k.piece('head'); H = h.at                      # (0, 27.5, -0.65)
    h.cyl(H(0, -0.2, 0), H(0, 1.6, 0), 2.2, 10, 'dark', bevel=0.06)
    h.sphere(H(0, 1.8, 0), 2.1, 'paint2', segs=10, rings=6, scale=(1, 0.85, 1))
    e = k.piece('eye'); E = e.at                       # (0, 29.13, -0.65)
    e.cyl(E(0, 0, 1.0), E(0, 0, 2.2), 0.9, 10, 'dark')
    e.cyl(E(0, 0, 2.15), E(0, 0, 2.3), 0.65, 10, 'lightr')

    # ------------------------------------------------------------------ right pauldron (shoulder, -5.95, 24.93, -0.65)
    s = k.piece('shoulder'); S = s.at
    s.hull([S(x, y, z) for x, y, z in
            [(-0.2, -3.4, -7.6), (-0.2, -3.4, 6.6), (-7.0, -3.4, -7.0), (-7.0, -3.4, 6.0),
             (-0.6, 3.6, -7.2), (-0.6, 3.6, 6.2), (-6.4, 3.0, -6.4), (-6.4, 3.0, 5.4)]], 'paint', bevel=0.22)
    s.hull([S(x, y, z) for x, y, z in
            [(-1.4, 3.56, -5.8), (-1.4, 3.56, 4.8), (-5.6, 3.08, -5.2), (-5.6, 3.08, 4.2),
             (-1.4, 3.72, -5.75), (-1.4, 3.72, 4.75), (-5.6, 3.24, -5.15), (-5.6, 3.24, 4.15)]], 'team', bevel=0.03)
    s.box(S(-7.15, -1.6, -5.0), S(-6.9, 1.4, 4.0), 'dark', bevel=0.04)

    # ------------------------------------------------------------------ mortar cradle (support, 6.06, 25.1, 0.24)
    u = k.piece('support'); U = u.at
    u.hull([U(x, y, z) for x, y, z in
            [(0.0, -3.4, -5.6), (0.0, -3.4, 10.0), (6.6, -3.4, -5.6), (6.6, -3.4, 10.0),
             (0.0, 3.2, -5.2), (0.0, 3.2, 8.6), (6.6, 3.2, -5.2), (6.6, 3.2, 8.6)]], 'paint2', bevel=0.2)
    u.box(U(0.6, 3.15, -4.4), U(6.0, 3.35, 5.6), 'team', bevel=0.03)                 # team cradle lid
    u.box(U(0.6, 3.1, 6.0), U(6.0, 3.3, 7.8), 'hazard', bevel=0.03)
    u.cyl(U(-0.6, 0, 0), U(1.2, 0, 0), 2.4, 10, 'dark', bevel=0.06)                   # trunnion

    # ------------------------------------------------------------------ the mortar tube (barrel, 9.32, 25.15, 0.24)
    b = k.piece('barrel'); B = b.at                    # muzzle (flare) at (-0.07, 0.04, 25.87)
    b.cyl(B(0, 0, -8.6), B(0, 0, -4.0), 2.8, 12, 'dark', bevel=0.12)                  # breech
    b.cyl(B(0, 0, -4.2), B(0, 0, 24.4), 2.3, 12, 'steel')
    for z in (6.0, 14.0):
        b.cyl(B(0, 0, z), B(0, 0, z + 1.0), 2.65, 12, 'dark')
    b.cyl(B(0, 0, 24.2), B(0, 0, 26.0), 2.75, 12, 'dark', bevel=0.06)                 # muzzle ring
    b.cyl(B(0, 0, 25.95), B(0, 0, 26.1), 1.8, 12, 'black')
