"""Ambusher (ARM_T2_DEF_Ambusher) - Arm pop-up heavy cannon. A low octagonal armoured ring round a deep well; closed, four
hazard-striped quarter lids (pinwheel) cover the well. On activation the lids swing down into the ground, the rotating
stand and the turret rise out of the well and the long gun comes level.
Identity from above (open): a light octagon ring with four team facets, a dark spiked stand, a light twin-cheek turret
with a team roof over its breech and a long dark barrel reaching well past the ring; closed = the ring round a yellow-
black pinwheel of lids (the hatch is the meaningful hazard).
Pieces (COB): base, door1..4 (turn x/z, move y), stand (move y, turn y), turret (move y), gun (turn x), barrel (move z),
flare (emit, empty). The model's default pose is OPEN (the COB closes it at Create: lids flat, turret 36 down); the
preview shows it open with the lids moved down out of sight, as the COB leaves them.
Two wrecks: ARM_T2_DEF_Ambusher_dead1 (level 1) and ARM_T2_DEF_Ambusher_dead2 (level 2, more broken).
Coordinates are ENGINE/global: X right, Y up, Z forward."""
import math

UNIT = dict(
    res=1024,
    wreck=dict(seed=17, drop=['barrel'], pose={'gun': (12, 0, 0), 'door1': (90, 0, 0), 'door3': (-90, 0, 0)}),
    preview_pose={'door1': {'move': (0, -8.5, 0)}, 'door2': {'move': (0, -8.5, 0)}, 'door3': {'move': (0, -8.5, 0)},
                  'door4': {'move': (0, -8.5, 0)}, 'stand': (0, 20, 0), 'turret': (0, 0, 0)},
)

RO0, RO1, RI, H = 24.4, 20.6, 15.6, 8.6     # ring: outer radius at ground / top, inner radius, height


def octagon(r, rot=math.pi / 8):
    return [(r * math.cos(rot + i * math.pi / 4), r * math.sin(rot + i * math.pi / 4)) for i in range(8)]


def build(k):
    # ------------------------------------------------------------------ base: octagonal ring round the well
    b = k.piece('base')
    o0, o1, ii = octagon(RO0), octagon(RO1), octagon(RI)
    for i in range(8):
        j = (i + 1) % 8
        b.hull([(x, 0.0, z) for x, z in (o0[i], o0[j])] + [(x, H, z) for x, z in (o1[i], o1[j])] +
               [(x, y, z) for x, z in (ii[i], ii[j]) for y in (0.0, H)], 'paint', bevel=0.25)
        if i % 2 == 0:      # team on four of the sloped facets
            pts = []
            for f in (0.22, 0.78):
                for t in (0.18, 0.82):
                    for d in (0.08, 0.26):
                        a0 = (o0[i][0] * (1 - t) + o0[j][0] * t, o0[i][1] * (1 - t) + o0[j][1] * t)
                        a1 = (o1[i][0] * (1 - t) + o1[j][0] * t, o1[i][1] * (1 - t) + o1[j][1] * t)
                        x = a0[0] * (1 - f) + a1[0] * f; z = a0[1] * (1 - f) + a1[1] * f; y = H * f
                        n = math.hypot(x, z)
                        pts.append((x + x / n * d * 0.9, y + d * 0.45, z + z / n * d * 0.9))
            b.hull(pts, 'team', bevel=0.0)
        else:               # dark armour plates on the other four
            pts = []
            for f in (0.3, 0.7):
                for t in (0.3, 0.7):
                    for d in (0.08, 0.2):
                        a0 = (o0[i][0] * (1 - t) + o0[j][0] * t, o0[i][1] * (1 - t) + o0[j][1] * t)
                        a1 = (o1[i][0] * (1 - t) + o1[j][0] * t, o1[i][1] * (1 - t) + o1[j][1] * t)
                        x = a0[0] * (1 - f) + a1[0] * f; z = a0[1] * (1 - f) + a1[1] * f; y = H * f
                        n = math.hypot(x, z)
                        pts.append((x + x / n * d * 0.9, y + d * 0.45, z + z / n * d * 0.9))
            b.hull(pts, 'dark', bevel=0.0)
    # dark rim round the well mouth and the well floor
    for i in range(8):
        j = (i + 1) % 8
        r0, r1 = octagon(RI + 1.6), octagon(RI)
        b.hull([(x, y, z) for x, z in (r0[i], r0[j], r1[i], r1[j]) for y in (H - 0.2, H + 0.35)], 'dark', bevel=0.05)
    b.plan(0.0, 0.4, octagon(RI), 'black', bevel=0.0)
    # team bands on the ring's flat top over the four team facets
    t0, t1 = octagon(RI + 2.0), octagon(RO1 - 0.5)
    for i in range(0, 8, 2):
        j = (i + 1) % 8
        b.hull([(x * 0.97 + x2 * 0.03, y, z * 0.97 + z2 * 0.03) for (x, z), (x2, z2) in
                ((t0[i], t0[j]), (t0[j], t0[i]), (t1[i], t1[j]), (t1[j], t1[i])) for y in (H, H + 0.2)], 'team', bevel=0.0)
    b.box((-1.0, 3.0, RO0 - 1.6), (1.0, 4.2, RO0 - 0.9), 'lightc', bevel=0.0)

    # ------------------------------------------------------------------ doors: quarter lids, hanging when open
    # door1 origin (-0.54, 8.58, 15.57): panel x -15.1..0, hanging y -16.1..0 at the rim; inner face (-z) is the lid top
    d1 = k.piece('door1'); D = d1.at
    d1.box(D(-15.0, -15.8, -0.9), D(-0.2, 0.0, 0.0), 'dark', bevel=0.1)
    d1.box(D(-14.2, -15.0, -1.1), D(-1.0, -0.8, -0.85), 'hazard', bevel=0.03)
    d2 = k.piece('door2'); D = d2.at          # origin (-15.37, 8.67, -0.5): panel z -15.5..0, inner face +x
    d2.box(D(0.0, -14.8, -15.4), D(0.9, 0.0, -0.2), 'dark', bevel=0.1)
    d2.box(D(0.85, -14.0, -14.6), D(1.1, -0.8, -1.0), 'hazard', bevel=0.03)
    d3 = k.piece('door3'); D = d3.at          # origin (-0.54, 8.52, -16): panel x 0..16.2, inner face +z
    d3.box(D(0.2, -15.4, 0.0), D(16.0, 0.0, 0.9), 'dark', bevel=0.1)
    d3.box(D(1.0, -14.6, 0.85), D(15.2, -0.8, 1.1), 'hazard', bevel=0.03)
    d4 = k.piece('door4'); D = d4.at          # origin (15.37, 8.61, -0.5): panel z 0..16.1, inner face -x
    d4.box(D(-0.9, -15.8, 0.2), D(0.0, 0.0, 16.0), 'dark', bevel=0.1)
    d4.box(D(-1.1, -15.0, 1.0), D(-0.85, -0.8, 15.2), 'hazard', bevel=0.03)

    # ------------------------------------------------------------------ stand: rotating spiked platform (origin 0, 2.48, -0.19)
    s = k.piece('stand'); S = s.at
    s.plan(S(0, -0.2, 0)[1], S(0, 3.2, 0)[1], [(x, z - 0.19) for x, z in octagon(14.4, 0.0)], 'paint2', bevel=0.2, top_inset=1.0)
    for i in range(8):
        a = i * math.pi / 4 + math.pi / 8
        c, sn = math.cos(a), math.sin(a)
        s.hull([S(c * r + (-sn) * w, 3.0, sn * r + c * w) for r in (9.6, 13.2) for w in (-1.6, 1.6)] +
               [S(c * 11.6, 8.6, sn * 11.6)], 'dark', bevel=0.1)

    # ------------------------------------------------------------------ turret: yoke (origin -0.1, 2.95, 0.17)
    t = k.piece('turret'); T = t.at
    t.cyl(T(0, 0.0, 0), T(0, 3.4, 0), 8.0, 12, 'dark', bevel=0.1)
    for sx in (-1, 1):
        t.hull([T(sx * x, y, z) for x, y, z in
                [(4.4, 3.2, -7.6), (8.4, 3.2, -7.6), (4.4, 3.2, 7.6), (8.4, 3.2, 7.6),
                 (4.4, 18.8, -5.6), (7.6, 18.0, -5.6), (4.4, 18.8, 4.4), (7.6, 18.0, 4.4)]], 'paint', bevel=0.25)
        t.hull([T(sx * x, y, z) for x, y, z in
                [(4.9, 18.85, -4.8), (7.2, 18.1, -4.8), (4.9, 18.85, 3.6), (7.2, 18.1, 3.6),
                 (4.9, 19.05, -4.8), (7.2, 18.3, -4.8), (4.9, 19.05, 3.6), (7.2, 18.3, 3.6)]], 'team', bevel=0.0)

    # ------------------------------------------------------------------ gun: breech housing (origin -0.28, 18.52, -0.19)
    g = k.piece('gun'); G = g.at
    g.cyl(G(-8.8, 0, 0), G(8.8, 0, 0), 2.4, 10, 'steel', bevel=0.05)
    g.hull([G(x * sx, y, z) for sx in (-1, 1) for x, y, z in
            [(4.2, -3.6, -10.2), (4.2, 4.6, -10.2), (4.2, -3.6, 12.0), (4.2, 4.6, 10.0), (3.0, -2.6, 17.4), (3.0, 3.2, 17.4)]],
           'paint', bevel=0.3)
    g.hull([G(x * sx, y, z) for sx in (-1, 1) for x, y, z in
            [(3.0, 4.62, -8.8), (3.0, 4.62, 8.6), (3.0, 4.85, -8.8), (3.0, 4.85, 8.6)]], 'team', bevel=0.0)
    g.box(G(-4.4, -2.0, -10.6), G(4.4, 3.0, -10.1), 'black', bevel=0.0)

    # ------------------------------------------------------------------ barrel (origin -0.1, 18.52, 16.61)
    br = k.piece('barrel'); B = br.at
    br.cyl(B(0, 0, -1.0), B(0, 0, 19.6), 2.2, 10, 'dark', rot=math.pi / 10)
    br.cyl(B(0, 0, 8.0), B(0, 0, 9.2), 2.5, 10, 'steel', rot=math.pi / 10)
    br.cyl(B(0, 0, 17.4), B(0, 0, 20.6), 2.8, 8, 'steel', rot=math.pi / 8, bevel=0.06)
    br.cyl(B(0, 0, 20.58), B(0, 0, 20.7), 1.4, 10, 'black')
