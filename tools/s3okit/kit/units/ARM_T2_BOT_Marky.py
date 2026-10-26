"""Marky (ARM_T2_BOT_Marky) - Arm T2 radar kbot. A small walking sensor cabin with two big hexagonal radar vanes on
its flanks that spin about their span when the radar is on. Standard biped skeleton; script ported to
scripts/ARM_T2_BOT_Marky.lua. Coordinates are ENGINE/global: X right, Y up, Z forward.
Top view (what makes it a Marky): a light cabin with a team roof and a dark sensor nose between two long vanes that
flicker light/dark as they turn - a wide cross shape no combat kbot has."""
import math

UNIT = dict(
    skeleton='biped',
    skeleton_opts=dict(hipx=3.3),
    res=1024,
    wreck=dict(seed=13, drop=['Ldish'], remove=[]),
    preview_pose={'ldish': (35, 0, 0), 'rdish': (-35, 0, 0)},
)


def build(k):
    k.standard_legs(width=1.5)

    # ------------------------------------------------------------------ pelvis (0, 11, 0)
    p = k.piece('pelvis'); Q = p.at
    p.hull([Q(x * sx, y, z) for sx in (-1, 1) for x, y, z in
            [(2.6, -1.8, -2.2), (2.6, -1.8, 2.4), (3.0, 1.4, -2.6), (3.0, 1.4, 2.8), (1.6, -2.6, -1.4), (1.6, -2.6, 1.6)]],
           'paint2', bevel=0.14)

    # ------------------------------------------------------------------ head (0, 12, 1): the sensor cabin
    h = k.piece('head'); H = h.at
    h.hull([H(x * sx, y, z) for sx in (-1, 1) for x, y, z in
            [(3.6, -0.6, -6.2), (3.6, -0.6, 4.6), (4.4, 4.0, -6.8), (4.4, 4.0, 5.8), (3.8, 8.2, -6.0), (3.4, 8.8, 2.0),
             (2.6, 5.4, 8.6), (2.4, 1.2, 7.4)]], 'paint', bevel=0.22)
    # team roof
    h.hull([H(x * sx, y, z) for sx in (-1, 1) for x, y, z in
            [(2.9, 8.33, -5.2), (2.7, 8.8, 1.4), (2.9, 8.49, -5.15), (2.7, 8.96, 1.35)]], 'team', bevel=0.04)
    # dark sensor nose with a cyan eye strip
    h.hull([H(x * sx, y, z) for sx in (-1, 1) for x, y, z in
            [(2.0, 2.0, 7.6), (2.2, 5.0, 8.4), (1.6, 2.4, 9.2), (1.8, 4.8, 9.4)]], 'dark', bevel=0.06)
    h.box(H(-1.4, 3.4, 9.3), H(1.4, 4.0, 9.55), 'lightc', bevel=0.0)
    # vane hubs on the flanks
    for sx in (-1, 1):
        h.cyl(H(sx * 4.0, 3.6, -0.75), H(sx * 4.6, 3.6, -0.75), 2.2, 10, 'dark', bevel=0.06)
    # rear equipment box with an antenna mast
    h.box(H(-2.8, 0.6, -8.0), H(2.8, 6.4, -6.0), 'paint2', bevel=0.14)
    h.cyl(H(1.8, 8.4, -5.0), H(1.8, 13.0, -5.0), 0.12, 6, 'steel', r2=0.06)
    h.cyl(H(1.8, 13.0, -5.0), H(1.8, 13.25, -5.0), 0.18, 6, 'lightr')

    # ------------------------------------------------------------------ radar vanes (left built, right mirrored)
    d = k.piece('Ldish'); D = d.at                     # (4.25, 15.6, 0.25), spins about X
    d.cyl(D(0.0, 0, 0.6), D(10.4, 0, 0.6), 0.55, 8, 'steel')                         # spar
    hexa = [(1.0, -2.6), (1.0, 2.6), (3.2, 6.8), (8.0, 6.8), (10.2, 2.6), (10.2, -2.6), (8.0, -6.8), (3.2, -6.8)]
    d.hull([D(x, y, z) for x, y in hexa for z in (0.0, 1.2)], 'paint', bevel=0.12)
    d.hull([D(x * 0.92 + 0.45, y * 0.86, z) for x, y in hexa for z in (1.15, 1.45)], 'dark', bevel=0.05)  # emitter face
    for y in (-4.0, -1.4, 1.2, 3.8):                                                    # emitter rows
        d.box(D(2.6, y, 1.42), D(8.6, y + 0.6, 1.6), 'lightc', bevel=0.0)
    d.hull([D(x * 0.9 + 0.5, y * 0.8, z) for x, y in hexa for z in (-0.2, 0.05)], 'paint2', bevel=0.04)  # back plate
    k.clone('Rdish', 'Ldish', mirror_x=True)
