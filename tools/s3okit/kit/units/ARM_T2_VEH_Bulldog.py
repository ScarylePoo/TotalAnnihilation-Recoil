"""Bulldog (ARM_T2_VEH_Bulldog) - Arm heavy assault tank. Very wide, tall slab hull on broad tracks with flared,
faceted sponsons; a low wide turret set far back carrying two heavy cannon in pods on a cross sleeve (TA layout).
Value groups from above: light Arm hull/sponsons/turret, darker paint2 lower hull and gun pods, black/dark glacis
grille and engine louvres, team colour on the turret roof + pod tops + a cross band on the front deck (no fender
bands: that is the T1 tanks' read), dark heavy barrels with fat muzzle brakes reaching past the nose.
Coordinates are ENGINE/global: X right, Y up, Z forward. mirror=True builds the -X twin sharing UVs."""
import math

UNIT = dict(
    wreck=dict(seed=7, drop=['barrel2'], pose={'turret': (0, -32, 0), 'sleeve': (6, 0, 0)}),
    preview_pose={'turret': (0, -18, 0), 'sleeve': (-4, 0, 0)},
)


def build(k):
    # ------------------------------------------------------------------ base
    b = k.piece('base')
    xi, xo = 13.4, 21.4
    belt = [(-19.6, 0.0), (19.0, 0.0), (22.2, 2.4), (21.8, 5.0), (19.6, 6.8), (-19.8, 6.8), (-22.4, 4.6), (-22.2, 2.0)]
    b.prism(xi, xo, belt, 'tread', bevel=0.18, mirror=True)
    for z in (-15.6, -9.4, -3.2, 3.0, 9.2, 15.4):
        b.cyl((xi, 2.3, z), (xi - 0.5, 2.3, z), 2.0, 14, 'dark', mirror=True)
        b.cyl((xi - 0.5, 2.3, z), (xi - 0.8, 2.3, z), 0.8, 8, 'steel', mirror=True)
    # sponsons: heavy faceted armour over the tracks, flaring at the front corners (TA's wedge "wings")
    top = 8.6
    b.hull([(12.8, top, -19.6), (22.0, top, -19.0), (22.6, top, 12.0), (12.8, top, 15.6),
            (12.8, 6.6, 22.6), (21.4, 6.2, 20.4), (12.8, 6.8, -22.6), (21.4, 6.8, -21.6),
            (12.8, 6.4, -19.6), (22.8, 6.4, -19.0), (23.4, 6.4, 12.4), (12.8, 6.0, 15.6)], 'paint', bevel=0.18, mirror=True)
    # dark armour skirt under the sponson edge (separates the hull from the ground)
    b.hull([(22.4, 6.6, -19.4), (23.4, 6.6, -18.8), (23.8, 6.6, 12.0), (22.8, 6.6, 12.6),
            (21.8, 3.0, -17.8), (22.8, 3.0, -17.4), (23.2, 3.0, 10.4), (22.2, 3.0, 11.0)], 'paint2', bevel=0.12, mirror=True)
    # paint2 inset panels on the sponson tops (break the long light slab into two plates)
    b.box((15.0, top, -17.6), (20.4, top + 0.22, 9.6), 'paint2', bevel=0.06, mirror=True)
    # stowage bins + exhausts on the rear sponsons
    b.box((14.0, top, -21.0), (20.6, top + 1.4, -18.6), 'dark', bevel=0.1, mirror=True)
    b.cyl((17.2, top + 1.0, -19.8), (17.2, top + 3.6, -20.6), 0.85, 10, 'dark', bevel=0.05, mirror=True)
    b.cyl((17.2, top + 3.6, -20.6), (17.2, top + 3.75, -20.65), 0.6, 10, 'black', mirror=True)
    # headlight clusters on the sponson noses
    b.box((15.6, 5.8, 20.6), (19.0, 7.2, 21.6), 'dark', bevel=0.08, mirror=True)
    b.box((15.9, 6.0, 21.58), (18.7, 6.95, 21.7), 'lightw', bevel=0.0, mirror=True)

    # ------------------------------------------------------------------ hull (crosses x = 0)
    b.prism(-13.4, 13.4, [(-21.6, 2.6), (20.6, 2.6), (23.4, 5.6), (22.0, 8.6), (-21.6, 8.6), (-22.4, 5.2)], 'paint2', bevel=0.18)
    # upper hull: tall slab, sloped glacis, flat deck at the rear under the turret
    b.hull([(x * sx, y, z) for sx in (-1, 1) for x, y, z in
            [(13.0, 8.6, -21.8), (13.0, 8.6, 18.0), (11.6, 7.4, 22.6),
             (11.4, 14.6, -20.4), (11.4, 14.6, 8.2), (9.6, 11.6, 18.6)]], 'paint', bevel=0.2)
    # glacis grille: dark block with black slats (TA's slatted front plates)
    b.hull([(x * sx, y, z) for sx in (-1, 1) for x, y, z in
            [(8.0, 11.9, 17.6), (8.0, 13.8, 11.2), (8.0, 12.08, 17.7), (8.0, 13.98, 11.3)]], 'dark', bevel=0.05)
    for i in range(4):
        z = 12.4 + i * 1.4
        y = 13.98 - (z + 0.55 - 11.3) * 0.297
        b.box((-7.4, y - 0.1, z), (7.4, y + 0.2, z + 0.55), 'black', bevel=0.0)
    # team cross band over the front deck (the Bulldog's own read: transverse, not fender stripes)
    b.box((-11.0, 14.6, 1.0), (11.0, 14.82, 5.4), 'team', bevel=0.05)
    # hatches either side of the band
    for x in (-5.6, 5.6):
        b.cyl((x, 14.6, 7.0), (x, 15.0, 7.0), 1.3, 14, 'paint2', bevel=0.05)
        b.box((x - 0.5, 15.0, 6.85), (x + 0.5, 15.15, 7.15), 'dark', bevel=0.0)
    # rear plate, louvres, tail lights
    b.box((-10.6, 9.2, -22.4), (10.6, 13.6, -21.7), 'dark', bevel=0.08)
    for y in (9.8, 10.8, 11.8, 12.8):
        b.box((-9.8, y, -22.6), (9.8, y + 0.4, -22.3), 'black', bevel=0.0)
    b.box((11.0, 11.0, -22.3), (12.6, 12.0, -21.9), 'lightr', bevel=0.0, mirror=True)
    # whip antenna, left rear sponson
    b.cyl((-14.6, top, -15.0), (-14.6, top + 0.8, -15.0), 0.4, 8, 'dark')
    b.cyl((-14.6, top + 0.8, -15.0), (-14.6, top + 7.5, -15.0), 0.1, 6, 'steel', r2=0.05)
    b.cyl((-14.6, top + 7.5, -15.0), (-14.6, top + 7.7, -15.0), 0.16, 6, 'lightc')

    # ---------------------------------------------------------------- turret (origin 0, 14.7, -9.45; turns y)
    t = k.piece('turret'); A = t.at
    t.cyl(A(0, -0.1, -2.0), A(0, 0.5, -2.0), 7.4, 20, 'dark', bevel=0.08)
    t.hull([A(x * sx, y, z) for sx in (-1, 1) for x, y, z in
            [(6.6, 0.4, -11.0), (7.0, 0.4, -3.0), (5.8, 0.4, 4.4), (3.0, 0.4, 7.0),
             (5.6, 4.6, -10.2), (6.0, 4.6, -3.0), (4.8, 4.6, 3.4), (2.4, 4.6, 5.6)]], 'paint', bevel=0.18)
    # big team roof plate
    t.hull([A(x * sx, y, z) for sx in (-1, 1) for x, y, z in
            [(4.4, 4.58, -9.0), (4.8, 4.58, -3.0), (3.8, 4.58, 2.6), (1.8, 4.58, 4.4),
             (4.35, 4.74, -8.95), (4.75, 4.74, -3.0), (3.75, 4.74, 2.55), (1.75, 4.74, 4.35)]], 'team', bevel=0.04)
    # commander cupola (left) and sensor box (right)
    t.cyl(A(-2.4, 4.7, -6.0), A(-2.4, 5.8, -6.0), 1.5, 14, 'paint2', bevel=0.08)
    t.box(A(-3.1, 5.8, -5.0), A(-1.7, 6.1, -4.7), 'lightc', bevel=0.0)
    t.box(A(1.4, 4.7, -7.6), A(3.4, 5.9, -5.4), 'dark', bevel=0.08)
    t.box(A(1.7, 5.0, -5.42), A(3.1, 5.6, -5.3), 'lightc', bevel=0.0)
    # bustle rack at the back
    t.hull([A(x * sx, y, z) for sx in (-1, 1) for x, y, z in
            [(5.4, 0.8, -10.8), (5.2, 3.8, -10.4), (4.8, 1.0, -12.4), (4.6, 3.4, -12.2)]], 'paint2', bevel=0.1)

    # ---------------------------------------------------------------- sleeve (cross sleeve with two gun pods)
    s = k.piece('sleeve'); S = s.at
    s.cyl(S(-9.0, 0, 0), S(9.0, 0, 0), 1.0, 12, 'steel')
    px = 7.13
    s.hull([S(x, y, z) for x in (px - 2.0, px + 2.0) for y, z in
            [(-2.4, -5.8), (2.0, -5.8), (2.2, 1.6), (-2.6, 2.4), (0.6, 3.6), (-1.6, 3.6)]], 'paint2', bevel=0.14, mirror=True)
    s.box(S(px - 1.5, 2.1, -5.0), S(px + 1.5, 2.36, 1.0), 'team', bevel=0.04, mirror=True)
    s.cyl(S(px, 0, 3.1), S(px, 0, 4.4), 1.75, 12, 'dark', bevel=0.06, mirror=True)
    s.box(S(px + 2.0, -1.2, -4.0), S(px + 2.4, 0.8, 0.6), 'dark', bevel=0.05, mirror=True)

    # ---------------------------------------------------------------- barrels (recoil along z)
    br = k.piece('barrel1'); B = br.at
    br.cyl(B(0, 0, 0.0), B(0, 0, 4.4), 1.4, 12, 'dark', r2=1.2, bevel=0.06)
    br.cyl(B(0, 0, 4.0), B(0, 0, 16.0), 1.02, 12, 'steel')
    br.cyl(B(0, 0, 9.4), B(0, 0, 10.6), 1.3, 12, 'dark', bevel=0.05)          # fume extractor
    br.cyl(B(0, 0, 15.6), B(0, 0, 18.4), 1.5, 8, 'dark', rot=math.pi / 8, bevel=0.07)   # muzzle brake
    br.cyl(B(0, 0, 18.38), B(0, 0, 18.46), 0.7, 8, 'black')
    for sx in (-1, 1):
        br.box(B(1.25 * sx, -0.4, 16.2), B(1.55 * sx, 0.4, 16.9), 'black', bevel=0.0)
        br.box(B(1.25 * sx, -0.4, 17.3), B(1.55 * sx, 0.4, 18.0), 'black', bevel=0.0)
    k.clone('barrel2', 'barrel1')
