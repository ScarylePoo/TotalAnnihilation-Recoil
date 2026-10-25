"""Thud (CORE_T1_BOT_Thud) - Core artillery kbot. A forward-leaning wedge torso hunched over the legs, carrying a
wide gun cradle (gun) on its back with a squat armoured box at each end and a long plasma cannon running forward
out of each box (rgun / lgun recoil). Standard biped skeleton; script ported to scripts/CORE_T1_BOT_Thud.lua.
Coordinates are ENGINE/global: X right, Y up, Z forward.
Top view (what makes it a Thud): a dark warm H - two angular dark boxes far out left and right with team plates,
joined by the cradle beam across the back, two long LIGHT steel barrels reaching far forward past the dark wedge
torso, whose ochre hazard spine points the way. Exaggerated barrel length and thickness vs the TA model."""
import math

UNIT = dict(
    skeleton='biped',
    skeleton_opts=dict(height=14.0, hipx=4.4),
    res=1024,
    wreck=dict(seed=12, drop=['lgun'], remove=[]),
    preview_pose={},
)


def build(k):
    k.standard_legs(width=1.5)

    # ------------------------------------------------------------------ torso (0, 14.94, -1.12): forward wedge
    t = k.piece('torso'); A = t.at
    t.cyl(A(0, -2.6, 1.0), A(0, 0.4, 1.0), 2.8, 10, 'dark', bevel=0.08)                     # waist
    t.hull([A(x * sx, y, z) for sx in (-1, 1) for x, y, z in
            [(3.4, -1.0, -6.0), (3.6, -1.0, 4.4), (4.6, 3.4, -8.4), (4.4, 3.4, 5.4),
             (3.4, 6.8, -9.4), (2.6, 5.6, 2.4), (1.4, 2.2, 7.6), (1.6, -0.6, 6.4)]], 'paint', bevel=0.22)
    # ochre hazard spine along the top of the wedge (Core accent; points the facing)
    t.hull([A(x * sx, y, z) for sx in (-1, 1) for x, y, z in
            [(0.9, 6.68, -8.2), (0.9, 5.52, 1.8), (0.6, 2.4, 6.9),
             (0.85, 6.84, -8.1), (0.85, 5.68, 1.75), (0.55, 2.56, 6.85)]], 'hazard', bevel=0.02)
    # dark sensor slits on the nose, warm eye
    for sx in (-1, 1):
        t.hull([A(x, y, z) for x, y, z in
                [(1.6 * sx, 1.6, 6.6), (3.0 * sx, 2.6, 4.9), (1.6 * sx, 2.4, 6.4), (3.0 * sx, 3.4, 4.7),
                 (1.7 * sx, 1.7, 6.8), (3.1 * sx, 2.7, 5.1)]], 'dark', bevel=0.03)
    t.box(A(-0.6, 0.9, 7.35), A(0.6, 1.5, 7.6), 'lightr', bevel=0.0)
    # paint2 side armour flanks (darker band low on the wedge)
    t.hull([A(x, y, z) for x, y, z in
            [(4.3, 0.0, -6.0), (4.3, 0.0, 3.8), (4.75, 3.2, -7.8), (4.6, 3.2, 4.8),
             (3.7, 0.0, -6.0), (3.7, 0.0, 3.8), (4.1, 3.2, -7.8), (4.0, 3.2, 4.8)]], 'paint2', bevel=0.08, mirror=True)

    # ------------------------------------------------------------------ gun cradle (0, 19.4, -6.79)
    g = k.piece('gun'); G = g.at
    g.cyl(G(-6.0, 0, 0), G(6.0, 0, 0), 1.6, 10, 'dark', bevel=0.06)                          # cradle beam
    # gun boxes at the ends: angular, dark warm (paint2) with team top plates
    g.hull([G(x, y, z) for x, y, z in
            [(5.8, -3.8, -6.0), (10.6, -3.8, -6.0), (5.8, -3.8, 6.2), (10.6, -3.8, 6.2),
             (6.2, 3.4, -5.4), (10.2, 3.4, -5.4), (6.2, 2.8, 4.6), (10.2, 2.8, 4.6),
             (6.0, 0.0, 7.4), (10.4, 0.0, 7.4)]], 'paint2', bevel=0.2, mirror=True)
    g.hull([G(x, y, z) for x, y, z in
            [(6.6, 3.42, -5.0), (9.8, 3.42, -5.0), (6.6, 2.88, 4.0), (9.8, 2.88, 4.0),
             (6.6, 3.6, -4.95), (9.8, 3.6, -4.95), (6.6, 3.06, 3.95), (9.8, 3.06, 3.95)]], 'team', bevel=0.03, mirror=True)
    # ammo drums at the back of each box
    g.cyl(G(8.2, -0.4, -6.0), G(8.2, -0.4, -7.6), 2.4, 10, 'dark', bevel=0.06, mirror=True)
    g.cyl(G(8.2, -0.4, -7.55), G(8.2, -0.4, -7.75), 1.2, 10, 'black', mirror=True)

    # ------------------------------------------------------------------ barrels (lgun built, rgun cloned mirrored)
    b = k.piece('lgun'); B = b.at                       # (7.88, 19.4, -0.24); firept at z +16.98
    b.cyl(B(0, 0, 4.0), B(0, 0, 17.0), 1.15, 10, 'steel', r2=0.95)                           # long LIGHT barrel
    b.cyl(B(0, 0, 3.6), B(0, 0, 8.2), 1.55, 10, 'steel', rot=math.pi / 10, bevel=0.06)       # thick root sleeve
    b.cyl(B(0, 0, 8.1), B(0, 0, 8.7), 1.65, 10, 'dark', bevel=0.04)
    b.cyl(B(0, 0, 13.0), B(0, 0, 13.5), 1.3, 10, 'dark', bevel=0.03)
    b.cyl(B(0, 0, 16.4), B(0, 0, 17.6), 1.5, 8, 'dark', rot=math.pi / 8, bevel=0.05)         # muzzle
    b.cyl(B(0, 0, 17.55), B(0, 0, 17.7), 0.7, 8, 'black')
    k.clone('rgun', 'lgun', mirror_x=True)
