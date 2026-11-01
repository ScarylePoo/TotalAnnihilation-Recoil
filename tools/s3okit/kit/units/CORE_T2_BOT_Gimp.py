"""Gimp (CORE_T2_BOT_Gimp) - Core T2 amphibious kbot (AMPHTANK: walks along the sea floor). A rounded submersible
hull with ballast tanks and a dorsal fin, legs set wide at its flanks, and a flat wide gun bar (head) on top carrying a
long laser on the left and a heavier cannon on the right. Standard biped skeleton; script ported to
scripts/CORE_T2_BOT_Gimp.lua (bubble/wake emission by terrain kept). Coordinates are ENGINE/global: X right, Y up,
Z forward. Seen from above through water, so the value blocks are big: dark warm hull, team plates on the gun bar,
ochre ballast bands, team ballast tanks and hull-top plates, two light steel barrels.
Top view (what makes it a Gimp): a squat egg with two long parallel barrels reaching far forward from a wide bar -
the twin-barrel "tuning fork" read no other Core kbot has."""
import math

UNIT = dict(
    skeleton='biped',
    skeleton_opts=dict(hipx=9.4, height=13.5),
    res=1024,
    wreck=dict(seed=25, drop=['laser'], remove=[]),
    preview_pose={'head': (0, -15, 0)},
)


def build(k):
    k.standard_legs(width=1.6)

    # ------------------------------------------------------------------ pelvis (0, 13.5, 0): hip bar to the flanks
    p = k.piece('pelvis'); Q = p.at
    p.hull([Q(x * sx, y, z) for sx in (-1, 1) for x, y, z in
            [(8.8, -1.6, -2.0), (8.8, -1.6, 1.8), (8.8, 1.6, -2.0), (8.8, 1.6, 1.8), (5.0, -2.4, -2.4), (5.0, 2.4, -2.4)]],
           'dark', bevel=0.16)

    # ------------------------------------------------------------------ body (0, 10.5, -4): submersible hull
    b = k.piece('body'); B = b.at
    ring = lambda y, rx, rz, zc: [B(rx * math.cos(a), y, zc + rz * math.sin(a)) for a in [i * math.pi / 6 for i in range(12)]]
    b.hull(ring(-1.0, 5.4, 5.6, 2.0) + ring(3.0, 7.6, 7.4, 2.0) + ring(9.0, 7.6, 7.2, 2.0) + ring(12.8, 5.2, 5.4, 2.4),
           'paint', bevel=0.2)
    for y in (2.0, 7.0):                                                                # ochre ballast bands
        b.hull(ring(y, 7.75, 7.55, 2.0) + ring(y + 1.0, 7.8, 7.6, 2.0), 'hazard', bevel=0.03)
    b.hull([B(x, y, z) for x in (-0.6, 0.6) for y, z in [(12.6, -3.6), (16.6, -4.8), (16.2, -2.4), (13.0, 2.4)]],
           'dark', bevel=0.08)                                                          # dorsal fin
    b.hull([B(x * sx, y, z) for sx in (-1, 1) for x, y, z in                            # front sensor dome (dark)
            [(3.2, 4.0, 8.6), (3.0, 9.0, 8.4), (2.0, 5.0, 9.8), (2.0, 8.0, 9.6)]], 'dark', bevel=0.12)
    for sx in (-1.2, 1.2):
        b.cyl(B(sx, 6.6, 9.6), B(sx, 6.6, 10.1), 0.6, 8, 'lightw')
    for sx in (-1, 1):                                                                  # rear ballast tanks
        b.cyl(B(sx * 4.2, 6.0, -5.0), B(sx * 4.2, 6.0, -8.6), 2.0, 10, 'team', bevel=0.1)
        b.hull([B(sx * x, y, z) for x in (1.0, 3.6) for y in (12.84, 13.0) for z in (-1.0, 2.8)], 'team', bevel=0.03)
        b.cyl(B(sx * 4.2, 6.0, -8.5), B(sx * 4.2, 6.0, -8.8), 1.2, 10, 'black')

    # ------------------------------------------------------------------ head (0, 19.5, 3): flat gun bar
    h = k.piece('head'); H = h.at
    h.hull([H(x * sx, y, z) for sx in (-1, 1) for x, y, z in
            [(3.6, 3.6, -3.8), (3.6, 3.6, 6.0), (9.0, 4.4, -2.6), (9.0, 4.4, 4.6), (8.4, 8.0, -2.2), (8.4, 8.0, 4.0),
             (3.2, 9.0, -3.2), (3.2, 9.0, 5.0), (2.4, 6.0, 8.6)]], 'paint2', bevel=0.22)
    for sx in (-1, 1):                                                                  # team plates on the bar top
        h.hull([H(sx * x, y, z) for x, y, z in
                [(3.6, 9.02, -2.4), (3.6, 9.02, 3.6), (7.8, 8.12, -1.6), (7.8, 8.12, 2.8),
                 (3.6, 9.18, -2.35), (3.6, 9.18, 3.55), (7.8, 8.28, -1.55), (7.8, 8.28, 2.75)]], 'team', bevel=0.03)
    h.box(H(-1.2, 5.6, 8.0), H(1.2, 6.6, 8.5), 'lightr', bevel=0.0)

    # ------------------------------------------------------------------ laser (-6.5, 25.5, 4.5): long thin barrel
    l = k.piece('laser'); L = l.at
    l.box(L(-2.0, -1.7, -0.8), L(2.0, 1.7, 5.0), 'dark', bevel=0.12)
    l.cyl(L(-0.15, 0.1, 4.8), L(-0.15, 0.1, 21.0), 0.75, 10, 'steel')
    for z in (8.0, 12.0, 16.0):
        l.cyl(L(-0.15, 0.1, z), L(-0.15, 0.1, z + 0.6), 1.05, 10, 'dark')
    l.cyl(L(-0.15, 0.1, 20.8), L(-0.15, 0.1, 21.6), 1.0, 10, 'dark', bevel=0.03)
    l.cyl(L(-0.15, 0.1, 21.55), L(-0.15, 0.1, 21.7), 0.5, 10, 'lightr')

    # ------------------------------------------------------------------ gun (6.5, 25.5, 4.5): heavier cannon
    g = k.piece('gun'); G = g.at
    g.hull([G(x, y, z) for x in (-1.4, 2.0) for y in (-2.2, 2.4) for z in (-5.2, 4.0)], 'dark', bevel=0.16)
    g.cyl(G(0.25, 0, 3.8), G(0.25, 0, 14.6), 1.15, 10, 'steel')
    g.cyl(G(0.25, 0, 13.8), G(0.25, 0, 15.5), 1.5, 8, 'dark', rot=math.pi / 8, bevel=0.05)
    g.cyl(G(0.25, 0, 15.45), G(0.25, 0, 15.6), 0.75, 8, 'black')
