"""Infiltrator (ARM_T2_BOT_Infiltrator) - Arm T2 spy kbot (cloaks). A low, wide-stance stalker: a faceted body slung
between widely spaced legs, a long tapering tail (butt) behind and a sensor head hanging forward and down, all under a
peaked roof of three stealth plates. Cloaking (Activate) slides the front plate (hood) forward and tips it over the
head, and the rear plate (buttguard) back over the tail. Standard biped skeleton; script ported to
scripts/ARM_T2_BOT_Infiltrator.lua. Coordinates are ENGINE/global: X right, Y up, Z forward.
Top view (what makes it an Infiltrator): a long dark arrowhead (head - roof - tail) on two splayed legs, the roof a
light chevron with a team ridge - darker overall than any other Arm kbot (stealth), lit by a cyan eye."""
import math

UNIT = dict(
    skeleton='biped',
    skeleton_opts=dict(hipx=8.2),
    res=1024,
    wreck=dict(seed=16, drop=['hood'], remove=[]),
    preview_pose={},
)


def roof(b, y0, y1, w, z0, z1, mat='paint', team=False):
    """inverted-V stealth plate (two slopes) in piece-local coords: eaves at +-w / y0, ridge at y1, from z0 to z1."""
    A = b.at
    for sx in (-1, 1):
        b.hull([A(sx * x, y + dy, z) for x, y in [(0.0, y1), (w, y0)] for dy in (0.0, -0.5) for z in (z0, z1)], mat, bevel=0.1)
    if team:
        for sx in (-1, 1):
            b.hull([A(sx * (w * f), y1 + (y0 - y1) * f + 0.07 + dy, z) for f in (0.08, 0.55) for dy in (0.0, 0.14)
                    for z in (z0 + 0.8, z1 - 0.8)], 'team', bevel=0.03)


def build(k):
    k.standard_legs(thigh='paint2', shin='dark', foot='dark', width=1.35)

    # ------------------------------------------------------------------ pelvis (0, 13.55, 0): wide leg yoke
    p = k.piece('pelvis'); Q = p.at
    p.hull([Q(x * sx, y, z) for sx in (-1, 1) for x, y, z in
            [(7.6, -1.4, -1.8), (7.6, -1.4, 1.8), (7.6, 1.4, -1.8), (7.6, 1.4, 1.8), (3.0, -2.6, -2.6), (3.0, -2.6, 2.4),
             (3.0, 2.2, -2.6), (3.0, 2.2, 2.4)]], 'dark', bevel=0.14)

    # ------------------------------------------------------------------ torso (0, 13, 1.5): faceted body
    t = k.piece('torso'); A = t.at
    t.hull([A(x * sx, y, z) for sx in (-1, 1) for x, y, z in
            [(3.8, -2.0, -5.6), (3.8, -2.0, 3.4), (5.4, 2.6, -6.4), (5.4, 2.6, 3.8), (2.0, 6.2, -5.0), (2.0, 6.2, 2.6),
             (1.2, 0.0, 5.0)]], 'paint2', bevel=0.18)
    t.box(A(-2.2, 1.2, 3.6), A(2.2, 3.4, 4.4), 'dark', bevel=0.06)

    # ------------------------------------------------------------------ butt (0, 11.5, -4): long tapering tail
    b = k.piece('butt'); B = b.at
    b.hull([B(x * sx, y, z) for sx in (-1, 1) for x, y, z in
            [(4.0, -3.4, -0.6), (4.2, 4.0, -0.6), (3.4, -2.6, -8.0), (3.6, 3.4, -8.0), (1.4, -0.6, -17.0), (1.4, 1.2, -17.0)]],
           'paint2', bevel=0.2)
    b.hull([B(x * sx, y, z) for sx in (-1, 1) for x, y, z in                              # light dorsal plate
            [(2.6, 4.1, -1.4), (2.4, 3.5, -8.4), (0.9, 1.4, -15.6), (2.6, 4.26, -1.4), (2.4, 3.66, -8.4), (0.9, 1.56, -15.6)]],
           'paint', bevel=0.06)
    for z in (-4.0, -7.0, -10.0):                                                         # vent slots
        b.box(B(-3.7, -1.6, z), B(-3.5, 1.6, z - 1.2), 'black', bevel=0.0)
        b.box(B(3.5, -1.6, z), B(3.7, 1.6, z - 1.2), 'black', bevel=0.0)
    b.cyl(B(0, 0.3, -17.0), B(0, 0.3, -17.6), 0.7, 8, 'lightr')

    # ------------------------------------------------------------------ head (0, 16, 6): forward-hanging sensor head
    h = k.piece('head'); H = h.at
    h.hull([H(x * sx, y, z) for sx in (-1, 1) for x, y, z in
            [(3.6, -1.0, -1.6), (3.0, -0.4, 4.0), (4.4, -6.0, 1.0), (3.6, -7.0, 8.0), (1.6, -10.6, 9.4), (1.2, -6.4, 11.0),
             (1.6, -10.8, 4.0)]], 'paint2', bevel=0.2)
    h.hull([H(x * sx, y, z) for sx in (-1, 1) for x, y, z in                              # dark face
            [(2.6, -6.6, 9.2), (1.4, -9.8, 9.9), (2.6, -6.4, 9.45), (1.4, -9.6, 10.15), (1.0, -6.0, 10.9), (1.0, -5.8, 11.1)]],
           'dark', bevel=0.04)
    h.cyl(H(0, -7.6, 10.2), H(0, -7.6, 11.0), 1.2, 10, 'lightc')                         # single cyan eye
    for sx in (-2.4, 2.4):                                                                # mandible antennae
        h.cyl(H(sx, -10.0, 8.6), H(sx * 1.2, -11.6, 12.2), 0.3, 6, 'steel', r2=0.15)

    # ------------------------------------------------------------------ the three stealth roof plates
    roof(k.piece('backshield'), 0.4, 8.4, 7.6, -4.8, 5.3, 'paint', team=True)            # (0, 15, 0.5)
    roof(k.piece('buttguard'), 0.6, 8.2, 7.4, -6.4, 1.8, 'paint')                        # (0, 14, -0.5)
    roof(k.piece('hood'), 0.4, 8.2, 7.4, -2.0, 6.0, 'paint')                             # (0, 13.12, 1.25)
