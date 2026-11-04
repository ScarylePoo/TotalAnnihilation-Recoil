"""Flakker (ARM_T2_DEF_Flakker) - Arm flak gun. A squat octagonal bunker with four side blocks; on top a turret with
two tall rounded ear shields either side of a short cradle that carries two long flak barrels close together.
Identity from above: a light octagon with team side blocks, two light ear shields with team tops framing a dark
cradle, two long thin dark barrels side by side - the Arm Defender is a missile rack instead.
Pieces (Lua script): Base, XTurret (turn y), YTurret (turn x), Barrel1/2 (move z recoil), Flare1/2 (emit, empty).
Coordinates are ENGINE/global: X right, Y up, Z forward."""
import math

UNIT = dict(
    res=1024,
    wreck=dict(seed=19, drop=['Barrel2'], pose={'XTurret': (0, 35, 0), 'YTurret': (15, 0, 0)}),
    preview_pose={'XTurret': (0, -25, 0), 'YTurret': (-25, 0, 0)},
)


def octagon(r, rot=math.pi / 8):
    return [(r * math.cos(rot + i * math.pi / 4), r * math.sin(rot + i * math.pi / 4)) for i in range(8)]


def build(k):
    # ------------------------------------------------------------------ Base: octagonal bunker + side blocks
    b = k.piece('Base')
    b.plan(0.0, 2.0, octagon(15.6), 'paint2', bevel=0.2, top_inset=0.6)
    b.plan(1.8, 10.1, octagon(13.6), 'paint', bevel=0.3, top_inset=2.6)
    for ux, uz in ((1, 0), (-1, 0), (0, 1), (0, -1)):
        px, pz = -uz, ux
        b.hull([(ux * u + px * w, y, uz * u + pz * w) for u, y in ((9.0, 0.0), (15.8, 0.0), (15.8, 5.6), (11.0, 8.4), (9.0, 8.4))
                for w in (-3.8, 3.8)], 'paint2', bevel=0.2)
        tp = []
        for u in (11.8, 15.0):
            y = 8.4 - (u - 11.0) * 2.8 / 4.8
            for w in (-3.0, 3.0):
                for d in (0.08, 0.26):
                    tp.append((ux * u + px * w, y + d, uz * u + pz * w))
        b.hull(tp, 'team', bevel=0.0)
    b.cyl((0, 9.6, 0), (0, 10.3, 0), 9.6, 12, 'dark', bevel=0.06)

    # ------------------------------------------------------------------ XTurret: ring + two ear shields (origin 0.08, 10.05, -0.33)
    t = k.piece('XTurret'); T = t.at
    t.cyl(T(0, 0.0, 0), T(0, 2.4, 0), 9.2, 12, 'dark', bevel=0.08)
    for sx in (-1, 1):
        t.hull([T(sx * x, y, z) for x, y, z in
                [(5.6, 2.2, -7.6), (10.4, 2.2, -7.6), (5.6, 2.2, 7.6), (10.4, 2.2, 7.6),
                 (5.6, 9.6, -6.0), (9.2, 8.6, -6.0), (5.6, 9.6, 6.0), (9.2, 8.6, 6.0),
                 (6.0, 11.4, -2.6), (8.4, 11.0, -2.6), (6.0, 11.4, 2.6), (8.4, 11.0, 2.6)]], 'paint', bevel=0.3)
        # team cap over the whole ear top (shell 0.15 above the ear's top faces)
        t.hull([T(sx * x, y + 0.15, z) for x, y, z in
                [(5.9, 9.55, -5.6), (8.9, 8.7, -5.6), (5.9, 9.55, 5.6), (8.9, 8.7, 5.6),
                 (6.2, 11.3, -2.4), (8.2, 10.9, -2.4), (6.2, 11.3, 2.4), (8.2, 10.9, 2.4)]], 'team', bevel=0.0)
    t.box(T(-0.8, 2.2, -8.2), T(0.8, 3.4, -7.6), 'lightc', bevel=0.0)

    # ------------------------------------------------------------------ YTurret: gun cradle (origin 0.08, 14.40, -0.67)
    y = k.piece('YTurret'); Y = y.at
    y.cyl(Y(-6.2, 0, 0), Y(6.2, 0, 0), 2.0, 10, 'steel', bevel=0.04)
    y.hull([Y(x * sx, yy, z) for sx in (-1, 1) for x, yy, z in
            [(5.0, -3.0, -4.0), (5.0, 3.2, -4.0), (5.0, -3.0, 10.0), (5.0, 2.4, 10.0), (3.6, -2.2, 13.2), (3.6, 1.8, 13.2)]],
           'paint2', bevel=0.25)
    y.box(Y(-4.2, 3.15, -3.6), Y(4.2, 3.4, 8.4), 'team', bevel=0.04)          # team cradle roof

    # ------------------------------------------------------------------ barrels (Barrel1 origin -1.93, 14.57, 12.23)
    br = k.piece('Barrel1'); B = br.at
    br.cyl(B(0, 0, -0.6), B(0, 0, 19.6), 1.1, 8, 'dark', rot=math.pi / 8)
    br.cyl(B(0, 0, 16.6), B(0, 0, 19.8), 1.45, 8, 'steel', rot=math.pi / 8, bevel=0.04)
    br.cyl(B(0, 0, 19.78), B(0, 0, 19.9), 0.7, 8, 'black')
    k.clone('Barrel2', 'Barrel1', mirror_x=True)
