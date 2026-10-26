"""Voyeur (CORE_T2_BOT_Voyeur) - Core T2 mobile radar kbot. A low flat body on two legs, two boxy sensor pods
(arm1/arm2) jutting forward at its front corners, and one tall octagonal radar plate (dish1) standing upright on its
back that spins about the vertical when the radar is on. Standard biped skeleton; script ported to
scripts/CORE_T2_BOT_Voyeur.lua. Coordinates are ENGINE/global: X right, Y up, Z forward.
Top view (what makes it a Voyeur): a dark-warm slab with team deck plates, team equipment boxes, two sensor pods forward (team tops) and a thin light radar
steel blade across the middle that sweeps round - unlike Arm's Marky with its two side vanes."""
import math

UNIT = dict(
    skeleton='biped',
    skeleton_opts=dict(hipx=7.0),
    res=1024,
    wreck=dict(seed=31, drop=['dish1'], remove=[]),
    preview_pose={'dish1': (0, 35, 0)},
)


def build(k):
    k.standard_legs(width=1.6)

    # ------------------------------------------------------------------ pelvis (0, 10.5, 0)
    p = k.piece('pelvis'); Q = p.at
    p.hull([Q(x * sx, y, z) for sx in (-1, 1) for x, y, z in
            [(6.2, -1.4, -2.0), (6.2, -1.4, 1.8), (6.2, 1.2, -2.0), (6.2, 1.2, 1.8), (3.0, -2.4, -2.4), (3.0, -2.4, 2.0)]],
           'dark', bevel=0.14)

    # ------------------------------------------------------------------ body (0, 10.75, -2.79): flat slab
    b = k.piece('body'); B = b.at
    b.hull([B(x * sx, y, z) for sx in (-1, 1) for x, y, z in
            [(5.4, -1.2, -6.6), (5.4, -1.2, 8.6), (5.6, 2.6, -7.0), (5.6, 2.6, 9.0), (4.2, 3.6, -6.0), (4.2, 3.6, 7.6),
             (2.6, 1.0, 10.6), (3.4, -1.0, -7.2)]], 'paint', bevel=0.22)
    b.hull([B(x * sx, y, z) for sx in (-1, 1) for x, y, z in                            # front sensor window
            [(2.4, 0.2, 10.2), (2.4, 1.6, 10.0), (2.4, 0.2, 10.45), (2.4, 1.6, 10.25)]], 'dark', bevel=0.04)
    b.box(B(-1.8, 0.6, 10.4), B(1.8, 1.2, 10.55), 'lightr', bevel=0.0)
    b.cyl(B(0, 3.4, 0), B(0, 4.4, 0), 2.6, 10, 'dark', bevel=0.06)                     # dish turntable
    b.box(B(-3.6, 3.5, -6.0), B(3.6, 4.2, -3.6), 'hazard', bevel=0.04)
    for sx in (-1, 1):                                                                  # rear equipment boxes (team)
        b.box(B(sx * 3.6 - 1.4, 0.0, -9.4), B(sx * 3.6 + 1.4, 3.0, -6.8), 'team', bevel=0.1)
        b.box(B(sx * 2.2 - 1.6, 3.62, 3.0), B(sx * 2.2 + 1.6, 3.78, 7.0), 'team', bevel=0.03)   # team deck plates

    # ------------------------------------------------------------------ sensor pods (arm2 built, arm1 = mirror)
    a = k.piece('arm2'); A = a.at                      # (5, 11.5, 1.46)
    a.hull([A(x, y, z) for x, y, z in
            [(-1.6, -3.8, 0.2), (4.2, -3.8, 0.2), (-1.6, 1.6, 0.2), (4.2, 1.6, 0.2),
             (-1.2, -3.4, 8.4), (3.8, -3.4, 8.4), (-1.2, 1.4, 7.6), (3.8, 1.4, 7.6)]], 'paint2', bevel=0.18)
    a.box(A(-0.6, 1.4, 1.4), A(3.2, 1.6, 6.4), 'team', bevel=0.03)
    a.cyl(A(1.3, -1.2, 8.2), A(1.3, -1.2, 8.8), 1.3, 10, 'dark')
    a.cyl(A(1.3, -1.2, 8.75), A(1.3, -1.2, 8.9), 0.85, 10, 'lightr')
    k.clone('arm1', 'arm2', mirror_x=True)

    # ------------------------------------------------------------------ radar plate (dish1, 0, 12.25, -2.79)
    d = k.piece('dish1'); D = d.at
    d.cyl(D(0, 0, 0), D(0, 2.2, 0), 1.0, 8, 'steel')
    octa = [(5.0 * math.cos(a), 5.4 + 5.0 * math.sin(a)) for a in [i * math.pi / 4 + math.pi / 8 for i in range(8)]]
    d.hull([D(x, y, z) for z, y in [(o[0] * 1.3, o[1]) for o in octa] for x in (-0.5, 0.7)], 'steel', bevel=0.12)
    d.hull([D(x, y, z) for z, y in [(o[0] * 1.08, 5.4 + (o[1] - 5.4) * 0.84) for o in octa] for x in (0.68, 1.1)],
           'dark', bevel=0.05)                                                           # emitter face (+x)
    for y in (3.0, 5.4, 7.8):
        d.box(D(1.05, y - 0.25, -4.6), D(1.2, y + 0.25, 4.6), 'lightr', bevel=0.0)
    d.hull([D(x, y, z) for z, y in [(o[0] * 1.1, 5.4 + (o[1] - 5.4) * 0.85) for o in octa] for x in (-0.7, -0.48)],
           'paint2', bevel=0.04)                                                         # back plate (-x)
