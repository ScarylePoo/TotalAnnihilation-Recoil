"""Punisher (CORE_T1_DEF_Punisher) - Core heavy plasma battery. A wide low octagonal bunker with four diagonal
buttress pods at the corners (TA's 'X' plan), a broad armoured turret with a domed cap, and two thick plasma barrels
side by side (alternate recoil). Not a pop-up: the COB only turns turret (y) / sleeves (x) and recoils the barrels.
Identity from above: a big dark X of corner pods with team tops, the turret dome with an ochre hazard ring, two fat
light steel barrels - heavier and lower than the Arm Guardian's tall hooded housing.
Pieces (COB): base, turret (turn y), sleeves (turn x), barrel1/2 (move z), flare1/2 (emit, empty).
TA's dome cap sat on the base above the turret; here it is part of the turret so it turns with it.
Coordinates are ENGINE/global: X right, Y up, Z forward."""
import math

UNIT = dict(
    res=1024,
    wreck=dict(seed=37, drop=['barrel2'], pose={'turret': (0, -35, 0), 'sleeves': (10, 0, 0)}),
    preview_pose={'turret': (0, -25, 0), 'sleeves': (-6, 0, 0)},
)


def build(k):
    # ------------------------------------------------------------------ base: octagonal bunker + corner pods
    b = k.piece('base')
    oct8 = lambda r: [(r * math.cos(math.pi / 8 + i * math.pi / 4), r * math.sin(math.pi / 8 + i * math.pi / 4)) for i in range(8)]
    b.plan(0.0, 2.2, oct8(21.0), 'paint2', bevel=0.25, top_inset=0.6)
    b.plan(2.0, 15.6, oct8(18.0), 'paint', bevel=0.3, top_inset=4.0)
    b.cyl((0, 15.0, 0), (0, 16.0, 0), 11.4, 16, 'dark', bevel=0.1)
    # four corner pods (diagonals), dark, with team tops
    for sx in (-1, 1):
        for sz in (-1, 1):
            c = lambda u, w: ((u - w) * 0.7071 * sx, (u + w) * 0.7071 * sz)
            pts = []
            for (u, y, hw) in ((10.0, 0.0, 6.4), (27.0, 0.0, 6.0), (27.0, 7.6, 5.0), (12.0, 12.0, 5.2)):
                for w in (-hw, hw):
                    x, z = c(u, w); pts.append((x, y, z))
            b.hull(pts, 'paint2', bevel=0.3)
            tp = []
            for u in (14.0, 25.4):
                y = 12.0 - (u - 12.0) * 4.4 / 15.0          # on the sloped pod top
                for w in (-3.9, 3.9):
                    for d in (0.1, 0.28):
                        x, z = c(u, w); tp.append((x, y + d, z))
            b.hull(tp, 'team', bevel=0.0)
            x, z = c(27.25, 0)
            b.box((x - 1.0, 2.6, z - 1.0), (x + 1.0, 4.0, z + 1.0), 'lightr', bevel=0.0)
    b.box((-3.6, 2.2, 17.2), (3.6, 8.6, 17.7), 'black', bevel=0.0)
    b.box((-4.2, 8.6, 16.6), (4.2, 9.4, 17.8), 'hazard', bevel=0.04)

    # ---------------------------------------------------------------- turret (origin 0, 15.43, 0)
    t = k.piece('turret'); A = t.at
    t.cyl(A(0, 0, 0), A(0, 1.0, 0), 11.0, 16, 'dark', bevel=0.08)
    t.hull([A(x * sx, y, z) for sx in (-1, 1) for x, y, z in
            [(10.4, 1.0, -9.6), (10.4, 1.0, 6.0), (8.6, 1.0, 11.6),
             (9.0, 9.4, -8.6), (9.0, 9.4, 4.0), (7.0, 8.0, 8.6)]], 'paint', bevel=0.3)
    # domed cap (from TA's base-top dome)
    t.cyl(A(0, 9.2, -2.0), A(0, 11.6, -2.0), 8.4, 8, 'paint2', r2=7.4, rot=math.pi / 8, bevel=0.2)
    t.cyl(A(0, 11.6, -2.0), A(0, 13.6, -2.0), 7.4, 8, 'paint', r2=4.6, rot=math.pi / 8, bevel=0.2)
    t.cyl(A(0, 13.55, -2.0), A(0, 13.8, -2.0), 4.4, 8, 'team', rot=math.pi / 8)
    t.cyl(A(0, 11.0, -2.0), A(0, 11.7, -2.0), 8.0, 8, 'hazard', r2=7.3, rot=math.pi / 8)
    # side team slabs
    t.hull([A(x, y, z) for x, y, z in
            [(10.6, 2.0, -8.0), (12.0, 2.0, -7.4), (10.6, 2.0, 4.0), (12.0, 2.0, 3.4),
             (9.6, 8.6, -7.4), (11.0, 8.0, -6.8), (9.6, 8.6, 3.4), (11.0, 8.0, 2.8)]], 'paint2', bevel=0.15, mirror=True)
    t.hull([A(x, y, z) for x, y, z in
            [(9.8, 8.62, -6.6), (10.9, 8.1, -6.0), (9.8, 8.62, 2.6), (10.9, 8.1, 2.0),
             (9.8, 8.78, -6.6), (10.9, 8.26, -6.0), (9.8, 8.78, 2.6), (10.9, 8.26, 2.0)]], 'team', bevel=0.0, mirror=True)
    t.box(A(-8.0, 2.0, -10.4), A(8.0, 7.4, -9.9), 'black', bevel=0.0)

    # ---------------------------------------------------------------- sleeves (origin 0, 19.75, 7.5)
    sv = k.piece('sleeves'); S = sv.at
    sv.cyl(S(-7.6, 0, 0), S(7.6, 0, 0), 2.4, 10, 'steel', bevel=0.04)
    sv.hull([S(x * sx, y, z) for sx in (-1, 1) for x, y, z in
             [(7.6, -3.4, -2.0), (7.6, 3.2, -2.0), (7.2, -3.0, 9.6), (7.2, 2.8, 9.6)]], 'paint2', bevel=0.2)

    # ---------------------------------------------------------------- barrels (barrel1 origin -4.75, 19.75, 16.5)
    br = k.piece('barrel1'); B = br.at
    br.cyl(B(0, 0, -1.0), B(0, 0, 13.0), 2.0, 10, 'steel', rot=math.pi / 10)
    br.cyl(B(0, 0, 4.0), B(0, 0, 5.2), 2.4, 10, 'dark', rot=math.pi / 10)
    br.cyl(B(0, 0, 11.6), B(0, 0, 14.4), 2.6, 8, 'dark', rot=math.pi / 8, bevel=0.06)
    br.cyl(B(0, 0, 14.38), B(0, 0, 14.5), 1.3, 10, 'black')
    k.clone('barrel2', 'barrel1')
