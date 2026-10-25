"""Warrior (ARM_T1_BOT_Warrior) - Arm medium infantry kbot: the heavyweight of the T1 Arm kbots. Barrel chest with a
domed sensor head, tall slab shoulder guards, and two thick forearm guns held forward at hip height: a laser cannon
on the right (rarm + rgun, primary: ruparm pitches, rarm yaws) and an EMG on the left (larm + lemg, secondary: luparm
pitches). Standard biped skeleton (TA's centred `hips` block becomes the pelvis); script ported to
scripts/ARM_T1_BOT_Warrior.lua.
Coordinates are ENGINE/global: X right, Y up, Z forward.
Top view (what makes it a Warrior): the widest Arm T1 kbot - a broad light chest, team dome head in the middle, dark
(paint2) slab guards on both shoulders, and two long dark gun arms sticking far forward with team stripes on top.
The two guns differ (fat round laser right, boxy twin-barrel EMG left)."""
import math

UNIT = dict(
    skeleton='biped',
    skeleton_opts=dict(height=13.2, hipx=4.5),
    res=1024,
    wreck=dict(seed=8, drop=['luparm'], remove=[]),
    preview_pose={},
)


def build(k):
    k.standard_legs(width=1.6)                   # heavier legs than the Peewee's

    # ------------------------------------------------------------------ torso (0, 15.88, 0)
    t = k.piece('torso'); A = t.at
    t.cyl(A(0, -2.8, -0.4), A(0, 0.8, -0.4), 3.0, 12, 'dark', bevel=0.1)                    # waist
    # barrel chest: wide at the shoulders, faceted front, narrower at the waist
    t.hull([A(x * sx, y, z) for sx in (-1, 1) for x, y, z in
            [(4.2, 0.4, -4.2), (4.4, 0.4, 3.8), (6.8, 5.0, -5.2), (6.8, 5.0, 5.4),
             (6.2, 10.2, -4.6), (6.2, 10.2, 3.2), (4.8, 8.4, 6.0), (3.4, 2.4, 5.6)]], 'paint', bevel=0.24)
    # paint2 belly plate (front lower chest): dark band between light chest and legs, seen from the front
    t.hull([A(x * sx, y, z) for sx in (-1, 1) for x, y, z in
            [(3.6, 0.8, 4.2), (4.6, 4.2, 5.75), (3.4, 1.0, 4.5), (4.4, 4.2, 6.0)]], 'paint2', bevel=0.08)
    # collar ring the head sits in
    t.cyl(A(0, 10.1, 1.0), A(0, 10.7, 1.0), 3.4, 12, 'dark', bevel=0.06)
    # heavy back pack (paint2) with cooling fins and two exhaust stacks
    t.hull([A(x * sx, y, z) for sx in (-1, 1) for x, y, z in
            [(4.6, 2.0, -4.6), (4.6, 9.4, -4.4), (4.0, 2.8, -9.8), (3.8, 8.6, -9.4)]], 'paint2', bevel=0.18)
    for y in (3.6, 5.0, 6.4, 7.8):
        t.box(A(-3.4, y, -10.0), A(3.4, y + 0.5, -9.6), 'dark', bevel=0.04)
    for sx in (-1, 1):
        t.cyl(A(2.6 * sx, 8.4, -8.2), A(2.6 * sx, 12.0, -8.6), 0.8, 10, 'dark', bevel=0.04)
        t.cyl(A(2.6 * sx, 12.0, -8.6), A(2.6 * sx, 12.15, -8.62), 0.5, 10, 'black')

    # ------------------------------------------------------------------ head (0, 24.27, 1.02): dome, team top
    h = k.piece('head'); H = h.at
    h.cyl(H(0, 1.8, 0), H(0, 4.4, 0), 3.0, 12, 'paint', r2=2.8, bevel=0.15)
    h.cyl(H(0, 4.4, 0), H(0, 5.6, 0), 2.8, 12, 'team', r2=1.6, bevel=0.1)                  # team dome
    h.hull([H(x * sx, y, z) for sx in (-1, 1) for x, y, z in                                   # visor brow
            [(2.2, 2.6, 2.2), (2.0, 3.8, 2.3), (2.2, 2.6, 2.9), (2.0, 3.8, 2.9)]], 'dark', bevel=0.05)
    h.box(H(-1.7, 3.0, 2.85), H(1.7, 3.45, 3.05), 'lightc', bevel=0.0)

    # ------------------------------------------------------------------ shoulders: slab guards (luparm built, cloned)
    u = k.piece('luparm'); U = u.at                    # (9.07, 21.77, -0.45); elbow (larm) at local (1.47, -8.28, -1.02)
    u.cyl(U(-2.4, 0, 0), U(0.4, 0, 0), 2.0, 12, 'dark', bevel=0.08)                           # shoulder joint
    u.hull([U(x, y, z) for x, y, z in                                                          # tall slab guard
            [(0.4, -4.6, -5.6), (0.4, -4.6, 5.4), (0.4, 4.4, -5.0), (0.4, 4.4, 4.4),
             (2.4, -4.0, -5.2), (2.4, -4.0, 5.0), (2.6, 4.0, -4.6), (2.6, 4.0, 4.0),
             (1.4, 5.2, -4.4), (1.4, 5.2, 3.8)]], 'paint2', bevel=0.2)
    u.box(U(2.45, -2.6, -3.4), U(2.75, 2.2, 2.8), 'dark', bevel=0.06)                          # bolted outer plate
    u.hull([U(x, y, z) for x, y, z in                                                          # upper arm to the elbow
            [(0.2, -2.0, -1.4), (0.2, -2.0, 1.2), (2.2, -2.0, -1.4), (2.2, -2.0, 1.2),
             (0.6, -8.4, -2.2), (0.6, -8.4, 0.2), (2.6, -8.4, -2.2), (2.6, -8.4, 0.2)]], 'dark', bevel=0.12)
    k.clone('ruparm', 'luparm', mirror_x=True)

    # ------------------------------------------------------------------ left forearm + EMG (larm (10.55, 13.5, -1.47))
    la = k.piece('larm'); L = la.at
    la.cyl(L(-1.9, 0, 0), L(1.9, 0, 0), 1.9, 10, 'dark', bevel=0.06)                          # elbow
    la.hull([L(x, y, z) for x, y, z in                                                         # boxy forearm housing
             [(-2.3, -2.2, -2.4), (2.3, -2.2, -2.4), (-2.3, 2.3, -2.4), (2.3, 2.3, -2.4),
              (-2.0, -1.8, 9.6), (2.0, -1.8, 9.6), (-2.0, 2.0, 9.6), (2.0, 2.0, 9.6)]], 'paint2', bevel=0.2)
    la.box(L(-1.3, 2.0, -0.6), L(1.3, 2.18, 8.4), 'team', bevel=0.04)                          # team stripe on top
    la.box(L(2.1, -1.0, 1.0), L(2.45, 0.9, 7.2), 'dark', bevel=0.05)                           # ammo feed on the side
    em = k.piece('lemg'); E = em.at                    # (10.55, 13.61, 8.89): twin EMG barrels
    em.box(E(-1.9, -1.6, 0.0), E(1.9, 1.6, 1.6), 'dark', bevel=0.1)
    for dx in (-0.85, 0.85):
        em.cyl(E(dx, 0, 1.4), E(dx, 0, 4.8), 0.62, 8, 'steel')
        em.cyl(E(dx, 0, 4.0), E(dx, 0, 4.85), 0.78, 8, 'dark', bevel=0.03)
        em.cyl(E(dx, 0, 4.8), E(dx, 0, 4.9), 0.36, 8, 'black')

    # ------------------------------------------------------------------ right forearm + laser (rarm (-10.32, 12.93, -1.47))
    ra = k.piece('rarm'); R = ra.at
    ra.cyl(R(-1.9, 0, 0), R(1.9, 0, 0), 1.9, 10, 'dark', bevel=0.06)
    ra.cyl(R(0, 0, -2.4), R(0, 0, 8.0), 2.7, 8, 'paint2', rot=math.pi / 8, bevel=0.2)       # fat round housing
    ra.hull([R(x, y, z) for x, y, z in                                                         # team saddle on top
             [(-1.3, 2.45, -0.8), (1.3, 2.45, -0.8), (-1.3, 2.45, 6.6), (1.3, 2.45, 6.6),
              (-1.25, 2.62, -0.75), (1.25, 2.62, -0.75), (-1.25, 2.62, 6.55), (1.25, 2.62, 6.55)]], 'team', bevel=0.03)
    for z in (1.4, 4.4):
        ra.cyl(R(0, 0, z), R(0, 0, z + 0.6), 2.82, 8, 'dark', rot=math.pi / 8, bevel=0.04)  # cooling rings
    # rgun: the laser emitter (piece origin is far off in the TA model; geometry is placed in global coords)
    g = k.piece('rgun')
    tip = (-10.21, 12.93, 12.59)                                                              # gunflare
    g.cyl((tip[0], tip[1], 6.4), (tip[0], tip[1], 11.6), 1.35, 10, 'steel', r2=1.0)
    g.cyl((tip[0], tip[1], 8.4), (tip[0], tip[1], 9.0), 1.6, 10, 'dark', bevel=0.04)
    g.cyl((tip[0], tip[1], 11.4), (tip[0], tip[1], 12.5), 1.55, 8, 'dark', rot=math.pi / 8, bevel=0.05)
    g.cyl((tip[0], tip[1], 12.45), (tip[0], tip[1], 12.6), 0.75, 10, 'lightr')               # emitter lens
