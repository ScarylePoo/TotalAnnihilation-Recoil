"""Peewee (ARM_T1_BOT_Peewee) - Arm light assault kbot: blocky chest, small visored head, hex backpack, cube shoulder
pads, both forearms are guns. Standard biped skeleton (backwards Federation legs, shared walk in
scripts/headers/walk.lua); script ported to scripts/ARM_T1_BOT_Peewee.lua.
Coordinates are ENGINE/global: X right, Y up, Z forward.
Value groups from above: light armour (chest, head, pads), team plates on the chest top and pad tops, dark guns and
backpack, legs paint/paint2/dark from standard_legs."""
import math

UNIT = dict(
    skeleton='biped',
    res=1024,
    wreck=dict(seed=2, drop=['lloarm'], remove=[]),
    preview_pose={'lloarm': (0, 0, 0), 'rloarm': (0, 0, 0)},     # aiming pose (idle has the guns pointing down)
)


def build(k):
    k.standard_legs()                      # thighs paint, shins paint2, feet dark; all legs share one UV set

    # ------------------------------------------------------------------ torso (origin 0, 13.76, 0.19)
    t = k.piece('torso'); A = t.at
    # waist joint above the pelvis
    t.cyl(A(0, -2.6, -0.6), A(0, 0.6, -0.6), 2.6, 12, 'dark', bevel=0.1)
    # chest: wide at the shoulders, sloped front, narrower waist
    t.hull([A(x * sx, y, z) for sx in (-1, 1) for x, y, z in
            [(3.2, 0.4, -3.2), (3.4, 0.4, 3.4), (4.7, 6.0, -3.8), (4.7, 6.0, 4.2),
             (4.2, 9.2, -3.6), (4.2, 9.2, 2.6), (3.4, 4.0, 4.9)]], 'paint', bevel=0.18)
    # chest front armour plate (darker band across the front: reads as the "face" of the unit from the front)
    t.hull([A(x * sx, y, z) for sx in (-1, 1) for x, y, z in
            [(2.6, 1.4, 4.0), (3.0, 4.6, 4.9), (2.6, 1.4, 4.2), (3.0, 4.6, 5.1)]], 'paint2', bevel=0.06)
    # team plate on the chest top
    t.hull([A(x * sx, y, z) for sx in (-1, 1) for x, y, z in
            [(3.5, 9.18, -3.0), (3.5, 9.18, 2.0), (3.45, 9.34, -2.95), (3.45, 9.34, 1.95)]], 'team', bevel=0.04)
    # head: small block on top of the chest, cyan visor slit
    t.hull([A(x * sx, y, z) for sx in (-1, 1) for x, y, z in
            [(1.9, 9.3, -1.2), (1.9, 9.3, 2.4), (1.6, 12.4, -1.0), (1.6, 12.4, 1.9), (1.4, 10.4, 3.0)]], 'paint', bevel=0.12)
    t.box(A(-1.25, 10.9, 2.55), A(1.25, 11.45, 2.75), 'lightc', bevel=0.0)
    t.box(A(-1.0, 12.35, -0.6), A(1.0, 12.55, 1.2), 'dark', bevel=0.03)
    # hexagonal backpack (power pack), dark, with vents and a stubby antenna
    t.cyl(A(0, 5.4, -3.4), A(0, 5.4, -8.4), 3.4, 6, 'paint2', rot=math.pi / 6, bevel=0.14)
    for y in (4.2, 5.2, 6.2):
        t.box(A(-2.0, y, -8.6), A(2.0, y + 0.45, -8.3), 'black', bevel=0.0)
    t.cyl(A(-2.2, 8.4, -6.8), A(-2.2, 13.6, -6.8), 0.12, 6, 'steel', r2=0.06)
    t.cyl(A(-2.2, 13.6, -6.8), A(-2.2, 13.85, -6.8), 0.16, 6, 'lightc')
    # hip skirt plates either side of the waist (break up the silhouette between chest and legs)
    t.hull([A(x, y, z) for x, y, z in
            [(2.6, -0.2, -2.4), (2.6, -0.2, 2.6), (4.0, 0.6, -2.0), (4.0, 0.6, 2.2),
             (3.3, -2.3, -1.6), (3.3, -2.3, 1.8)]], 'paint', bevel=0.1, mirror=True)

    # ------------------------------------------------------------------ left arm (built once, cloned to the right)
    u = k.piece('luparm'); U = u.at                     # shoulder at (4, 19.76, -0.61); elbow at local (4.38, -4.38, 0)
    u.cyl(U(0, 0, 0), U(1.2, 0, 0), 1.6, 12, 'dark', bevel=0.08)              # shoulder joint
    u.hull([U(x, y, z) for x, y, z in                                          # shoulder pad
            [(0.9, -1.6, -3.0), (0.9, -1.6, 3.0), (4.6, -1.8, -2.8), (4.6, -1.8, 2.8),
             (1.2, 2.4, -2.6), (1.2, 2.4, 2.6), (4.1, 2.0, -2.4), (4.1, 2.0, 2.4)]], 'paint', bevel=0.16)
    u.hull([U(x, y, z) for x, y, z in                                          # team plate on the pad top
            [(1.6, 2.32, -2.0), (1.6, 2.32, 2.0), (3.7, 2.0, -1.9), (3.7, 2.0, 1.9),
             (1.6, 2.46, -1.95), (1.6, 2.46, 1.95), (3.7, 2.14, -1.85), (3.7, 2.14, 1.85)]], 'team', bevel=0.03)
    u.hull([U(x, y, z) for x, y, z in                                          # upper arm down to the elbow
            [(2.6, -1.4, -1.0), (2.6, -1.4, 1.0), (3.6, -1.4, -1.0), (3.6, -1.4, 1.0),
             (3.7, -4.6, -0.9), (3.7, -4.6, 0.9), (5.0, -4.4, -0.9), (5.0, -4.4, 0.9)]], 'dark', bevel=0.1)

    g = k.piece('lloarm'); G = g.at                     # elbow; muzzle (lfire) at local (0, 3.62, 13.75)
    d = (0.0, 3.62 / 14.22, 13.75 / 14.22)              # gun axis (unit vector)
    P = lambda t_, dx=0.0, dy=0.0: G(dx, d[1] * t_ + dy, d[2] * t_)
    g.cyl(G(-1.15, 0, 0), G(1.15, 0, 0), 1.2, 10, 'dark', bevel=0.06)          # elbow joint
    g.hull([P(t_, dx, dy) for t_ in (-1.4, 8.6) for dx in (-1.35, 1.35) for dy in (-1.3, 1.3)], 'paint2', bevel=0.14)
    g.hull([P(t_, dx, dy) for t_ in (1.0, 6.5) for dx in (-0.9, 0.9) for dy in (1.28, 1.95)], 'dark', bevel=0.08)  # top rail
    g.cyl(P(8.4), P(13.4), 0.62, 10, 'steel')                                  # barrel
    g.cyl(P(10.6), P(11.0), 0.8, 10, 'dark')
    g.cyl(P(13.2), P(14.15), 0.82, 8, 'dark', rot=math.pi / 8, bevel=0.04)     # muzzle brake
    g.cyl(P(14.1), P(14.2), 0.4, 8, 'black')

    k.clone('ruparm', 'luparm', mirror_x=True)
    k.clone('rloarm', 'lloarm', mirror_x=True)
