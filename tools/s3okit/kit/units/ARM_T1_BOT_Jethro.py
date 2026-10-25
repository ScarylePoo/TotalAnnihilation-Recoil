"""Jethro (ARM_T1_BOT_Jethro) - Arm anti-air kbot. A slim upright torso carried between two tall armoured missile
pods. Each pod is two shells hinged on the torso side (luparm = upper shell, lloarm = lower shell + the launcher
`lgun`); the script swings them apart about Z when the unit aims, exposing the launcher racks, and closes them after
the restore delay. Standard biped skeleton; script ported to scripts/ARM_T1_BOT_Jethro.lua.
Coordinates are ENGINE/global: X right, Y up, Z forward.
Top view (what makes it a Jethro): two tall light pods standing ABOVE the torso level with team-coloured roofs, a dark
gap between them where the narrow torso sits with a dark sensor dish; the legs below are mostly hidden by the pods."""
import math

UNIT = dict(
    skeleton='biped',
    skeleton_opts=dict(hipx=3.3),      # TA's 2.52 makes the two legs touch
    res=1024,
    wreck=dict(seed=6, drop=['ruparm'], remove=[]),
    preview_pose={},
)


def build(k):
    k.standard_legs()

    # ------------------------------------------------------------------ torso (0, 16.11, 1.01)
    t = k.piece('torso'); A = t.at
    t.cyl(A(0, -3.6, 0), A(0, -0.6, 0), 2.3, 10, 'dark', bevel=0.08)                     # waist
    # slim chest: deep front-to-back, narrow, sloping forward like the TA original
    t.hull([A(x * sx, y, z) for sx in (-1, 1) for x, y, z in
            [(3.2, -1.0, -4.6), (3.2, -1.0, 5.0), (4.0, 4.0, -6.2), (4.0, 4.0, 7.6),
             (3.4, 8.6, -5.6), (3.4, 8.6, 4.2), (3.0, 6.6, 8.0)]], 'paint', bevel=0.2)
    # shoulder yoke the pods hang from (dark: separates pods from chest in the top view)
    t.box(A(-5.3, 3.2, -3.2), A(5.3, 7.2, 3.2), 'dark', bevel=0.14)
    # front sensor face: dark slab with a cyan eye strip
    t.hull([A(x * sx, y, z) for sx in (-1, 1) for x, y, z in
            [(2.4, 4.3, 7.75), (2.1, 6.4, 7.95), (2.4, 4.3, 7.95), (2.1, 6.4, 8.15)]], 'dark', bevel=0.04)
    t.box(A(-1.6, 5.2, 8.05), A(1.6, 5.6, 8.25), 'lightc', bevel=0.0)
    # AA tracking dish on the roof (dark bowl, steel feed): the AA tell from above
    t.cyl(A(0, 8.6, -1.0), A(0, 9.4, -1.0), 0.7, 8, 'dark')
    t.cyl(A(0, 9.3, -1.0), A(0, 10.4, -1.0), 2.6, 12, 'dark', r2=3.3, bevel=0.05)
    t.cyl(A(0, 10.3, -1.0), A(0, 11.6, -1.0), 0.18, 6, 'steel', r2=0.1)
    t.cyl(A(0, 11.6, -1.0), A(0, 11.8, -1.0), 0.28, 6, 'lightc')
    # team band across the chest roof in front of the dish
    t.hull([A(x * sx, y, z) for sx in (-1, 1) for x, y, z in
            [(3.0, 8.58, 1.6), (3.0, 8.58, 4.0), (2.95, 8.74, 1.65), (2.95, 8.74, 3.95)]], 'team', bevel=0.03)
    # back pack (paint2) with exhaust slots
    t.hull([A(x * sx, y, z) for sx in (-1, 1) for x, y, z in
            [(2.8, 0.0, -5.0), (2.8, 7.4, -5.6), (2.4, 0.8, -8.0), (2.2, 6.6, -8.2)]], 'paint2', bevel=0.14)
    for y in (2.0, 3.2, 4.4):
        t.box(A(-1.6, y, -8.3), A(1.6, y + 0.5, -8.0), 'black', bevel=0.0)

    # ------------------------------------------------------------------ left pod (cloned mirrored to the right)
    # lower shell lloarm (5.04, 19.89, 1.01): hinge at its inner bottom edge; shell spans x 0.3..6.9, y 0..5.8
    lo = k.piece('lloarm'); L = lo.at
    lo.cyl(L(0, 0, -2.5), L(0, 0, 2.5), 0.9, 8, 'dark')                                     # hinge pin
    lo.hull([L(x, y, z) for x, y, z in
             [(0.4, 0.0, -5.0), (6.6, 0.0, -4.6), (0.4, 0.0, 5.6), (6.6, 0.0, 5.0),
              (0.4, 5.7, -5.3), (7.0, 5.7, -5.0), (0.4, 5.7, 5.8), (7.0, 5.7, 5.3)]], 'paint2', bevel=0.18)
    # upper shell luparm (5.04, 25.68, 1.01): hinge at its inner bottom edge; shell spans x 0.3..6.9, y 0..5.9
    up = k.piece('luparm'); U = up.at
    up.hull([U(x, y, z) for x, y, z in
             [(0.4, 0.0, -5.3), (7.0, 0.0, -5.0), (0.4, 0.0, 5.8), (7.0, 0.0, 5.3),
              (0.8, 5.0, -4.6), (6.0, 5.9, -4.3), (0.8, 5.0, 4.8), (6.0, 5.9, 4.4)]], 'paint', bevel=0.2)
    # team roof plate on the pod top (sloping up outwards: catches light, big team read from above)
    up.hull([U(x, y, z) for x, y, z in
             [(1.6, 5.2, -3.4), (5.4, 5.72, -3.2), (1.6, 5.2, 3.6), (5.4, 5.72, 3.3),
              (1.6, 5.36, -3.35), (5.4, 5.88, -3.15), (1.6, 5.36, 3.55), (5.4, 5.88, 3.25)]], 'team', bevel=0.03)
    # dark seam band where the shells part, and a dark front grille on the upper shell
    up.box(U(0.6, 0.0, 5.3), U(6.8, 1.0, 5.75), 'dark', bevel=0.04)
    # launcher lgun (8.56, 25.43, 1.01) on the lower shell: twin-tube rack, light warheads
    g = k.piece('lgun'); G = g.at
    g.box(G(-2.2, 0.3, -4.4), G(2.0, 3.6, 4.0), 'dark', bevel=0.12)
    for dx in (-1.05, 1.0):
        g.cyl(G(dx, 1.95, 3.8), G(dx, 1.95, 5.0), 0.95, 10, 'dark', bevel=0.04)
        g.cyl(G(dx, 1.95, 4.9), G(dx, 1.95, 5.7), 0.62, 10, 'steel', r2=0.15)          # missile nose
    k.clone('rloarm', 'lloarm', mirror_x=True)
    k.clone('ruparm', 'luparm', mirror_x=True)
    k.clone('rgun', 'lgun', mirror_x=True)
