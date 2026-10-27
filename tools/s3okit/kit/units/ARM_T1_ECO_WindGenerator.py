"""Wind Generator (ARM_T1_ECO_WindGenerator) - Arm wind. A light four-buttress foot, a tall slim tapered tower, a
nacelle that yaws into the wind with a tall tail fin, and a big three-blade rotor on its nose (spins on z).
Identity from above: small light cross-shaped foot with team buttress tops, a long dark-edged blade line with team
tips sweeping a wide disc across the tower, team nacelle roof (the Core wind is a tall vertical-axis drum rotor).
Pieces (Lua script, third-party S3O layout kept): windgenerator.3ds (empty root), base, post (turn y = heading),
blades (spin z, hub at the post's nose).
Coordinates are ENGINE/global: X right, Y up, Z forward."""
import math

UNIT = dict(
    wreck=dict(seed=15, drop=['blades'], pose={'post': (0, 40, 0)}),
    preview_pose={'post': (0, 35, 0), 'blades': (0, 0, 20)},
)

BLADE_R = 34.0


def build(k):
    # ------------------------------------------------------------------ base: foot with four buttresses + tower
    b = k.piece('base')
    oct8 = [(13.0 * math.cos(math.pi / 8 + i * math.pi / 4), 13.0 * math.sin(math.pi / 8 + i * math.pi / 4)) for i in range(8)]
    b.plan(0.0, 5.0, oct8, 'paint2', bevel=0.25, top_inset=1.6)
    for sz in (-1, 1):            # buttresses on the -x diagonals, mirrored to +x
        d = (-math.sqrt(0.5), sz * math.sqrt(0.5)); p = (-d[1], d[0])
        P = lambda u, v, y: (d[0] * u + p[0] * v, y, d[1] * u + p[1] * v)
        prof = [(4.0, 0.0), (24.0, 0.0), (24.0, 2.0), (8.0, 12.0), (4.0, 12.0)]
        b.hull([P(u, v, y) for u, y in prof for v in (-2.6, 2.6)], 'paint', bevel=0.2, mirror=True)
        # team cap on the buttress slope (slope rises 10 over 16)
        b.hull([P(u, v, 2.0 + (24.0 - u) * 10.0 / 16.0 + dy) for u in (13.0, 21.0) for v in (-2.0, 2.0)
                for dy in (0.12, 0.36)], 'team', bevel=0.0, mirror=True)
        b.hull([P(u, v, y) for u, y in ((20.0, 0.0), (25.0, 0.0), (20.0, 1.2), (25.0, 1.2)) for v in (-3.4, 3.4)],
               'dark', bevel=0.12, mirror=True)
    # tower
    b.cyl((0, 4.8, 0), (0, 44.8, 0), 6.2, 10, 'paint', r2=3.2, rot=math.pi / 10, bevel=0.15)
    for y, r in ((12.0, 5.75), (24.0, 4.85), (36.0, 3.95)):
        b.cyl((0, y, 0), (0, y + 1.2, 0), r + 0.35, 10, 'dark', rot=math.pi / 10, bevel=0.05)
    b.box((-1.0, 4.4, 10.9), (1.0, 6.4, 11.4), 'lightc', bevel=0.0)

    # ------------------------------------------------------------------ post: nacelle (origin 0, 45, 0), nose to -z
    n = k.piece('post'); N = n.at
    n.cyl(N(0, -1.0, 0), N(0, 1.0, 0), 3.8, 10, 'dark', rot=math.pi / 10, bevel=0.08)
    n.hull([N(x, y, z) for x in (-3.8, 3.8) for (y, z) in
            ((1.0, -6.6), (8.6, -6.6), (1.0, 9.0), (7.4, 9.0))] +
           [N(x, y, z) for x in (-2.6, 2.6) for (y, z) in ((0.4, 12.0), (6.0, 12.0))], 'paint', bevel=0.4)
    n.hull([N(x, y, z) for x in (-2.6, 2.6) for (y, z) in ((8.6, -5.4), (8.9, -5.4), (8.6, 6.4), (8.9, 6.4))], 'team',
           bevel=0.0)
    # tail fin (tall, swept)
    n.hull([N(x, y, z) for x in (-0.7, 0.7) for (y, z) in ((6.0, 6.0), (6.0, 13.6), (24.0, 16.6), (24.0, 13.0))],
           'paint2', bevel=0.12)
    n.hull([N(x, y, z) for x in (-0.85, 0.85) for (y, z) in ((19.0, 12.2), (19.0, 15.9), (24.2, 16.7), (24.2, 13.1))],
           'team', bevel=0.0)
    n.box(N(-0.9, 23.0, 14.0), N(0.9, 24.6, 15.4), 'lightr', bevel=0.0)
    # radiator grilles on the flanks
    n.box(N(3.75, 3.0, 0.0), N(3.95, 6.6, 6.0), 'black', bevel=0.0, mirror=True)

    # ------------------------------------------------------------------ blades: hub + three blades (origin 0, 49.98, -9.81)
    r = k.piece('blades'); R = r.at
    r.cyl(R(0, 0, 3.6), R(0, 0, -1.0), 4.4, 10, 'paint', r2=3.6, rot=math.pi / 10, bevel=0.12)
    r.cyl(R(0, 0, -1.0), R(0, 0, -4.6), 3.6, 10, 'dark', r2=1.2, rot=math.pi / 10, bevel=0.06)

    def blade(ang, mirror=False):
        a = math.radians(ang)
        d = (math.sin(a), math.cos(a)); p = (d[1], -d[0])          # radial dir, chord dir (both in the xy plane)
        tw = math.radians(28)                                     # pitch: chord tilted out of the rotor plane

        def P(rad, c, t):          # rad along blade, c along chord, t thickness
            cx, cz = math.cos(tw) * c - math.sin(tw) * t, math.sin(tw) * c + math.cos(tw) * t
            return R(d[0] * rad + p[0] * cx, d[1] * rad + p[1] * cx, cz)
        sec = [(3.6, 3.0, 1.0), (8.0, 4.4, 0.9), (BLADE_R - 4.5, 2.9, 0.55), (BLADE_R, 2.4, 0.45)]
        r.hull([P(rd, c * s, t * s2) for rd, c, t in sec[:3] for s in (-1, 1) for s2 in (-1, 1)], 'paint', bevel=0.12,
               mirror=mirror)
        r.hull([P(rd, c * s, t * s2) for rd, c, t in ((BLADE_R - 4.5, 2.95, 0.6), (BLADE_R, 2.45, 0.5))
                for s in (-1, 1) for s2 in (-1, 1)], 'team', bevel=0.08, mirror=mirror)
        r.hull([P(rd, c, t * s2) for rd, c, t in ((8.0, 4.4, 0.95), (BLADE_R - 7.2, 3.2, 0.65))
                for c in (-4.6 if rd < 9 else -3.4, -3.0 if rd < 9 else -2.2) for s2 in (-1, 1)], 'dark', bevel=0.0,
               mirror=mirror)
    blade(0)
    blade(120, mirror=True)
