"""Spectre (CORE_T2_BOT_Spectre) - Core T2 radar jammer kbot. A small armoured core block over a wide skirt
(legcover) that roofs both hips, with a jammer hub at the front of the core; when active the two jammer tongs lying
along the flanks flip forward (180 deg) and the hub spins them. Standard biped skeleton; script ported to
scripts/CORE_T2_BOT_Spectre.lua. Coordinates are ENGINE/global: X right, Y up, Z forward.
Top view (what makes it a Spectre): a wide flat dark-warm skirt with two team panels, a small ochre-topped core in the
middle and two light tongs either side - a low table, unlike the Arm Eraser's high beam."""
import math

UNIT = dict(
    skeleton='biped',
    skeleton_opts=dict(hipx=5.0),
    res=1024,
    wreck=dict(seed=30, drop=['ltong'], remove=[]),
    preview_pose={'ltong': (180, 0, 0), 'rtong': (180, 0, 0), 'tongspivot': (0, 0, 25)},     # jammer active
)


def build(k):
    k.standard_legs(width=1.55)

    # ------------------------------------------------------------------ pelvis (0, 13.75, 0)
    p = k.piece('pelvis'); Q = p.at
    p.hull([Q(x * sx, y, z) for sx in (-1, 1) for x, y, z in
            [(4.2, -2.0, -3.0), (4.2, -2.0, 2.4), (4.4, 1.6, -4.4), (4.4, 1.6, 2.6), (2.4, -3.0, -2.0), (2.4, -3.0, 1.8)]],
           'dark', bevel=0.16)

    # ------------------------------------------------------------------ torso (0, 19.5, -5): core block
    t = k.piece('torso'); A = t.at
    t.hull([A(x * sx, y, z) for sx in (-1, 1) for x, y, z in
            [(3.2, -3.0, -8.4), (3.2, -3.0, 2.2), (3.3, 2.8, -8.8), (3.3, 2.8, 1.6), (2.4, 4.0, -7.6), (2.4, 4.0, 0.6)]],
           'paint2', bevel=0.18)
    t.box(A(-2.0, 3.95, -6.8), A(2.0, 4.15, -0.4), 'hazard', bevel=0.03)
    t.cyl(A(-1.2, 4.0, -7.4), A(-1.2, 9.0, -7.4), 0.14, 6, 'steel', r2=0.07)            # antenna
    t.cyl(A(-1.2, 9.0, -7.4), A(-1.2, 9.25, -7.4), 0.2, 6, 'lightr')

    # ------------------------------------------------------------------ legcover (0, 15, -5): the wide skirt
    c = k.piece('legcover'); C = c.at
    for sx in (-1, 1):
        c.hull([C(sx * x, y, z) for x, y, z in                                           # roof panel, sloping out
                [(3.0, 3.4, -7.8), (3.0, 3.4, 2.8), (11.0, 2.0, -7.8), (11.0, 2.0, 2.8),
                 (3.0, 2.4, -7.8), (3.0, 2.4, 2.8), (11.0, 1.0, -7.8), (11.0, 1.0, 2.8)]], 'paint', bevel=0.16)
        c.hull([C(sx * x, y, z) for x, y, z in                                           # side skirt
                [(10.2, 1.2, -7.6), (10.2, 1.2, 2.6), (11.6, 1.6, -7.6), (11.6, 1.6, 2.6),
                 (10.6, -3.6, -7.0), (10.6, -3.6, 2.0), (11.4, -3.6, -7.0), (11.4, -3.6, 2.0)]], 'paint2', bevel=0.12)
        c.hull([C(sx * x, y, z) for x, y, z in                                           # team panel on the roof
                [(4.2, 3.32, -6.6), (4.2, 3.32, 1.6), (10.0, 2.16, -6.6), (10.0, 2.16, 1.6),
                 (4.2, 3.48, -6.55), (4.2, 3.48, 1.55), (10.0, 2.32, -6.55), (10.0, 2.32, 1.55)]], 'team', bevel=0.03)
        c.box(C(sx * 11.7 - 0.2, -1.8, -6.0), C(sx * 11.7 + 0.2, -0.8, 1.0), 'lightr', bevel=0.0)

    # ------------------------------------------------------------------ hub (tongspivot, 0, 19.5, -2.5), spins about Z
    h = k.piece('tongspivot'); H = h.at
    h.cyl(H(0, 0, -0.4), H(0, 0, 3.4), 2.4, 8, 'dark', bevel=0.1)
    h.cyl(H(0, 0, 3.3), H(0, 0, 4.9), 1.7, 8, 'paint', r2=1.0, bevel=0.05)
    h.cyl(H(0, 0, 4.85), H(0, 0, 5.05), 0.8, 8, 'lightw')

    # ------------------------------------------------------------------ tongs: lying back along the flanks at rest
    g = k.piece('ltong'); G = g.at                     # (2.39, 19.5, -2.56)
    g.hull([G(x, y, z) for x in (0.2, 3.6) for y in (-1.4, 1.4) for z in (-1.4, 0.4)], 'dark', bevel=0.1)
    g.hull([G(x, y, z) for y in (-1.5, 1.5) for x, z in [(0.4, -1.2), (3.8, -1.2), (2.8, -11.0), (1.2, -12.4)]], 'paint',
           bevel=0.14)
    g.cyl(G(1.9, 0, -12.2), G(1.9, 0, -12.8), 0.9, 8, 'lightw')
    k.clone('rtong', 'ltong', mirror_x=True)
