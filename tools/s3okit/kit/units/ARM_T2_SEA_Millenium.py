"""Millenium (ARM_T2_SEA_Millenium) - Arm T2 battleship. A very tall, pointed clipper hull (the widest part low, bow
raked far forward) with a dark stepped citadel and two huge triple turrets in line: turret2 forward on a short barbette,
turret1 superfiring from the top of a tall waisted tower aft, with two big swept vanes behind it. Everything is built for
the gun line down the centre: three thick dark sleeves and steel barrels on each turret.
From above: a long light spearhead hull, dark citadel down the middle, two big team-roofed turret blocks in line with their
dark triple guns, vanes aft. The Colossus is its opposite: blunt, flat, dark decks, no guns.
Pieces (TA layout): base (origin y 6.41), turret1 / turret2 (turn y + x: the whole turret elevates; origins x -0.21 / -1.36,
so no mirror on them), barrel1A-C / barrel2A-C (recoil 6; B and C are clones of A), flare* (empty), wake1/2 (empty).
Value groups from above: light hull + turret bodies, dark citadel and towers, near-black sleeves, team on the turret roofs,
bow and stern.
Floater, no waterline (water surface at model y = 0). Decks are flat (no sheer): real tops are DECK and CIT.
Coordinates are ENGINE/global: X right, Y up, Z forward. mirror=True builds the -X twin sharing UVs."""
import math

UNIT = dict(
    wreck=dict(seed=62, remove=['barrel1C', 'barrel2A'], pose={'turret1': (10, 35, 0), 'turret2': (16, -40, 0)}),
    preview_pose={},
)

DECK = 19.1     # main deck (ring walk)
CIT = 23.8      # citadel roof
BOT = [(17.0, 41.9), (24.5, 28.7), (27.4, 18.5), (27.4, -21.4), (24.5, -50.5), (11.2, -70.8)]
MID = [(4.0, 58.2), (15.7, 38.9), (22.6, 26.7), (25.4, 17.3), (25.4, -19.6), (22.6, -46.6), (10.3, -65.4)]
SEGS = ((26.7, 60.0), (-19.6, 26.7), (-46.6, -19.6), (-72.0, -46.6))
BOW_Z = 58.2


def cut(pts, z0, z1):
    """outline pts between stations z0 and z1, with the end stations interpolated"""
    P = sorted({z: x for x, z in pts}.items())
    zs = [z for z, _ in P]; xs = [x for _, x in P]

    def xat(z):
        for i in range(len(zs) - 1):
            if zs[i] <= z <= zs[i + 1]:
                t = (z - zs[i]) / (zs[i + 1] - zs[i]); return xs[i] + t * (xs[i + 1] - xs[i])
        return xs[0] if z < zs[0] else xs[-1]
    lo, hi = max(z0, zs[0]), min(z1, zs[-1])
    return [(xat(z), z) for z in sorted({lo, hi} | {z for z in zs if lo < z < hi})]


def ring(o, y):
    return [(x * s, y, z) for x, z in o for s in (-1, 1)]


def build(k):
    b = k.piece('base')
    # ------------------------------------------------------------------ tall hull in segments (crosses x = 0)
    for z0, z1 in SEGS:
        m = cut(MID, z0, z1)
        lo = cut(BOT, max(z0, -70.8), min(z1, 41.9)) if z0 < 41.9 else cut(BOT, 30.0, 41.9)
        b.hull(ring(lo, -0.5) + ring(lo, 3.6), 'paint2', bevel=0.25)
        b.hull(ring(lo, 3.6) + ring(m, 16.3), 'paint', bevel=0.25)
        b.hull(ring(m, 16.3) + ring(m, DECK), 'paint', bevel=0.2)
    # raked bow stem down to the water
    b.hull([(x * s, y, z) for s in (-1, 1) for x, y, z in
            [(4.0, 16.3, 58.2), (4.0, DECK, 58.2), (15.7, 16.3, 38.9), (17.0, 3.6, 41.9)]], 'paint', bevel=0.2)
    # dark gunwale line
    b.hull([(x, y, z) for y in (DECK - 0.05, DECK + 0.22) for x, z in ((21.6, -42.0), (24.2, -19.6), (24.2, 17.3), (21.6, 26.0))],
           'dark', bevel=0.03, mirror=True)
    # ------------------------------------------------------------------ dark citadel down the middle
    b.hull([(x * s, y, z) for s in (-1, 1) for x, y, z in
            [(3.8, DECK - 0.1, 47.7), (20.2, DECK - 0.1, 17.3), (20.2, DECK - 0.1, -28.7), (1.0, CIT, 47.7), (17.4, CIT, 17.3),
             (17.1, CIT, -31.7)]], 'paint2', bevel=0.25)
    # aft citadel taper to the stern block
    b.hull([(x * s, y, z) for s in (-1, 1) for x, y, z in
            [(20.1, DECK - 0.1, -28.7), (4.6, DECK - 0.1, -60.8), (17.1, CIT, -31.7), (3.0, CIT, -60.8)]], 'paint2', bevel=0.25)
    # four side casemates (secondary battery blocks on the main deck)
    for z0, z1 in ((0.4, 15.7), (-18.0, -2.7)):
        b.hull([(x, y, z) for z in (z0, z1) for x, y in ((18.0, DECK - 0.1), (24.6, DECK - 0.1), (22.3, 21.5), (18.0, 21.5))],
               'dark', bevel=0.15, mirror=True)
        # team roof plate: the casemate top is flat at 21.5
        b.hull([(x, y, z) for y in (21.58, 21.76) for x, z in ((18.4, min(z0, z1) + 0.6), (21.9, min(z0, z1) + 0.6), (21.9, max(z0, z1) - 0.6), (18.4, max(z0, z1) - 0.6))],
               'team', bevel=0.03, mirror=True)
    # ------------------------------------------------------------------ bow and stern team plates (deck is flat at DECK)
    b.hull([(x, y, z) for y in (DECK + 0.08, DECK + 0.28) for x, z in ((0.0, 49.2), (0.0, 56.0), (3.8, 56.6), (15.0, 38.0), (10.6, 33.6))],
           'team', bevel=0.03, mirror=True)
    b.cyl((0, DECK, 57.0), (0, DECK + 0.9, 57.0), 0.6, 6, 'lightr')
    # team band across the citadel roof amidships, between the turrets
    b.hull([(x, y, z) for y in (CIT + 0.08, CIT + 0.28) for x, z in ((6.0, -9.6), (16.4, -9.6), (16.8, 1.0), (6.0, 1.0))],
           'team', bevel=0.03, mirror=True)
    # stern deck: bollards, stern light
    b.cyl((7.0, DECK, -56.0), (7.0, DECK + 1.4, -56.0), 0.9, 8, 'dark', mirror=True)
    b.box((-3.8, 10.0, -68.4), (3.8, 11.6, -67.3), 'lightr', bevel=0.0)
    # ------------------------------------------------------------------ forward barbette under turret2
    b.hull([(x * s, y, z) for s in (-1, 1) for x, y, z in
            [(11.0, CIT - 0.1, 28.8), (17.3, CIT - 0.1, 17.5), (17.3, CIT - 0.1, 1.3), (8.1, 34.2, 22.5), (10.9, 34.2, 17.5), (10.9, 34.2, 6.3)]],
           'paint2', bevel=0.25)
    # ------------------------------------------------------------------ aft structure: stack block + waisted tower
    b.hull([(x * s, y, z) for s in (-1, 1) for x, y, z in
            [(17.2, CIT - 0.1, -11.8), (17.2, CIT - 0.1, -31.8), (12.7, 29.9, -11.8), (12.9, 29.9, -33.0), (5.1, 29.9, -11.8)]],
           'paint2', bevel=0.25)
    # twin funnels on the stack block
    for z in (-16.0, -24.0):
        b.cyl((7.0, 29.8, z), (7.0, 34.6, z), 3.0, 10, 'dark', r2=2.6, bevel=0.05, mirror=True)
        b.cyl((7.0, 34.55, z), (7.0, 34.75, z), 1.9, 10, 'black', mirror=True)
    # tower lower part
    b.hull([(x * s, y, z) for s in (-1, 1) for x, y, z in
            [(13.8, CIT - 0.1, -33.0), (11.0, CIT - 0.1, -56.0), (4.4, CIT - 0.1, -62.4), (11.8, 33.2, -36.6), (3.9, 33.2, -60.9), (8.0, 36.6, -40.6), (2.6, 36.6, -57.0)]],
           'paint2', bevel=0.25)
    # waist and top flare
    b.hull([(x * s, y, z) for s in (-1, 1) for x, y, z in
            [(8.0, 36.5, -40.6), (2.6, 36.5, -57.0), (8.0, 41.5, -40.6), (2.6, 41.5, -57.0)]], 'dark', bevel=0.12)
    b.hull([(x * s, y, z) for s in (-1, 1) for x, y, z in
            [(8.0, 41.4, -40.6), (2.6, 41.4, -57.0), (10.4, 45.2, -38.1), (3.4, 45.2, -59.4)]], 'paint2', bevel=0.15)

    # ------------------------------------------------------------------ turret2 (forward): origin x -1.36, centred at +0.6
    t = k.piece('turret2'); A = t.at
    C = 0.66

    def T2(x, y, z):
        return A(C + x, y, z)
    t.hull([T2(x * s, y, z) for s in (-1, 1) for x, y, z in
            [(12.0, -0.6, 11.7), (14.0, 0.0, 9.5), (14.0, 0.0, -6.3), (11.4, -0.6, -8.5), (12.0, 6.5, 11.7),
             (14.0, 4.0, 9.5), (14.0, 4.0, -6.3), (11.4, 6.5, -8.5), (11.4, 11.1, -8.5), (11.4, 11.1, 4.2)]], 'paint', bevel=0.3)
    # rear bustle blocks
    for x in (-7.0, 0.0, 7.0):
        t.box(T2(x - 3.2, -0.8, -12.6), T2(x + 3.2, 9.6, -7.9), 'paint2', bevel=0.15)
    # team roof: the top is flat at 11.1, the sloped front follows it
    t.hull([T2(x * s, y, z) for s in (-1, 1) for x, y, z in
            [(10.4, 11.18, 3.4), (10.4, 11.18, -7.7), (10.4, 11.38, 3.4), (10.4, 11.38, -7.7)]], 'team', bevel=0.03)
    t.hull([T2(x * s, y, z) for s in (-1, 1) for x, y, z in
            [(10.4, 6.9, 10.6), (10.4, 10.95, 4.4), (10.4, 7.1, 10.7), (10.4, 11.15, 4.5)]], 'team', bevel=0.03)
    # three thick sleeves from the turret face out to the barrels
    for bn in ('barrel2A', 'barrel2B', 'barrel2C'):
        bo = k.P[bn]; x = bo.x - k.P['turret2'].x
        t.hull([A(x + sx * sg, y, z) for sg in (-1, 1) for sx, y, z in
                [(3.6, 0.8, 11.0), (3.6, 5.7, 11.0), (3.0, 1.2, 22.5), (3.0, 5.5, 22.5)]], 'dark', bevel=0.12)
    # roof sensors and the tall mast (right rear of the roof, as the 3DO)
    t.box(A(-8.6, 11.3, -5.5), A(-1.5, 13.5, 1.5), 'dark', bevel=0.12)
    t.cyl(A(-5.05, 13.5, -2.0), A(-5.05, 13.7, -2.0), 2.0, 10, 'lightc')
    t.box(A(3.3, 11.3, -7.8), A(9.6, 12.6, -1.5), 'dark', bevel=0.12)
    t.cyl(A(6.45, 12.6, -4.65), A(6.45, 28.5, -4.65), 0.8, 8, 'dark', r2=0.34)
    t.cyl(A(6.45, 28.5, -4.65), A(6.45, 29.0, -4.65), 0.34, 6, 'lightr')

    # ------------------------------------------------------------------ turret1 (aft, on the tower): origin x -0.21
    u = k.piece('turret1'); B = u.at
    C1 = 0.21

    def T1(x, y, z):
        return B(C1 + x, y, z)
    u.hull([T1(x * s, y, z) for s in (-1, 1) for x, y, z in
            [(12.4, -0.1, 9.6), (14.4, -0.1, 8.3), (14.4, -0.1, -4.2), (12.4, -0.1, -5.5), (14.4, 6.3, 8.3), (14.4, 6.3, -4.2),
             (12.4, 7.3, 9.6), (12.4, 7.3, -5.5), (10.2, 12.6, -1.2), (10.2, 12.6, -7.7), (5.7, -0.1, -16.3), (5.7, 7.3, -16.3)]],
           'paint', bevel=0.3)
    # side armour cheeks (wide and low, the 3DO's outer blocks)
    for s in (-1, 1):
        u.hull([T1(x * s, y, z) for x, y, z in
                [(14.0, 1.2, 6.5), (14.0, 5.0, 6.5), (14.0, 1.2, -4.6), (14.0, 5.0, -4.6), (17.3, 1.9, 6.1), (17.3, 4.3, 6.1),
                 (17.3, 1.9, -4.2), (17.3, 4.3, -4.2)]], 'paint2', bevel=0.12)
    # rear blocks
    for x in (-5.0, 5.0):
        u.box(T1(x - 3.4, -1.7, -18.4), T1(x + 3.4, 5.5, -8.0), 'paint2', bevel=0.15)
    u.box(T1(-3.9, 7.2, -14.1), T1(3.9, 10.5, -5.1), 'dark', bevel=0.12)
    # team roof
    u.hull([T1(x * s, y, z) for s in (-1, 1) for x, y, z in
            [(9.2, 12.68, -1.9), (9.2, 12.68, -7.0), (9.2, 12.88, -1.9), (9.2, 12.88, -7.0)]], 'team', bevel=0.03)
    u.hull([T1(x * s, y, z) for s in (-1, 1) for x, y, z in
            [(11.2, 7.72, 9.0), (9.2, 12.48, -1.0), (11.2, 7.92, 9.1), (9.2, 12.68, -0.9)]], 'team', bevel=0.03)
    # three thick sleeves, longer than turret2's
    for bn in ('barrel1A', 'barrel1B', 'barrel1C'):
        bo = k.P[bn]; x = bo.x - k.P['turret1'].x
        u.hull([B(x + sx * sg, y, z) for sg in (-1, 1) for sx, y, z in
                [(3.9, -0.8, 9.0), (3.9, 7.0, 9.0), (3.1, 0.3, 26.0), (3.1, 5.6, 26.0)]], 'dark', bevel=0.12)
    # the two swept vanes behind the turret (the ship's silhouette from astern)
    for s in (-1, 1):
        u.hull([T1(x * s, y, z) for x, y, z in
                [(5.4, 0.8, -12.0), (5.4, 0.8, -17.6), (5.4, 6.6, -9.4), (5.4, 6.6, -15.6), (21.6, 15.7, -23.6), (21.6, 15.7, -25.1),
                 (19.4, 15.7, -23.6), (19.4, 15.7, -25.1)]], 'dark', bevel=0.12)
    u.cyl(T1(20.5, 15.7, -24.3), T1(20.5, 16.3, -24.3), 0.5, 6, 'lightr')
    u.cyl(T1(-20.5, 15.7, -24.3), T1(-20.5, 16.3, -24.3), 0.5, 6, 'lightr')

    # ------------------------------------------------------------------ barrels: fat, steel, dark muzzle (recoil 6)
    for a, l, r, rm in (('barrel1A', 14.5, 2.2, 2.6), ('barrel2A', 12.1, 1.9, 2.2)):
        br = k.piece(a); P = br.at
        br.cyl(P(0, 0, -6.4), P(0, 0, l - 2.6), r, 10, 'steel', r2=r * 0.86)
        br.cyl(P(0, 0, l - 2.6), P(0, 0, l), rm, 8, 'dark', r2=rm * 0.9, rot=math.pi / 8, bevel=0.06)
        br.cyl(P(0, 0, l - 0.02), P(0, 0, l + 0.06), r * 0.55, 8, 'black')
    for a in ('barrel1B', 'barrel1C'):
        k.clone(a, 'barrel1A')
    for a in ('barrel2B', 'barrel2C'):
        k.clone(a, 'barrel2A')
