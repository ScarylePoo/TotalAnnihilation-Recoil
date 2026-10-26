"""Crusader (ARM_T1_SEA_Crusader) - Arm destroyer. Long pointed light hull with a raised centre deck; the gun tower
stands on a tall pylon at the STERN and fires forward over the whole ship: a wide turret with two long gun housings,
a wedge cab and two tall swept fins that make an H seen from above. Forward bridge with a team roof, twin dark
funnels amidships, depth-charge rack on the foredeck (flare3 = depth charge emit point).
Pieces (TA layout): base, turret (turn y AND x: the whole tower head pitches), barrel1/2 (recoil 6 along z),
flare1/2 (empty muzzle points), flare3 (empty), wake1/2 (empty wake emitters).
Value groups from above: light Arm hull + raised deck top, dark paint2 lower hull / deck-edge slopes / pylon / fins,
near-black funnels and machinery, team on the bridge roof and the turret roof.
Floater, waterline 4: the water surface is at model y = 4.
Coordinates are ENGINE/global: X right, Y up, Z forward. mirror=True builds the -X twin sharing UVs."""
import math

UNIT = dict(
    res=1024,
    wreck=dict(seed=3, pose={'turret': (10, 40, 0)}),
    preview_pose={'turret': (0, -20, 0)},
)

DECK = 7.6
WL = 4.0
# half outline of the main deck (x >= 0), bow to stern
OUT = [(0.0, 41.4), (3.4, 35.0), (9.4, 23.0), (14.2, 10.0), (15.6, 2.0), (15.6, -14.0), (14.0, -29.5), (7.6, -40.8)]


def ring(pts, y, sx=1.0, sz=1.0, dz=0.0, sheer=0.0):
    out = []
    for x, z in pts:
        yy = y + sheer * max(0.0, (z - 12.0) / 29.4) ** 1.5
        for s in ((-1, 1) if x > 0 else (1,)):
            out.append((x * sx * s, yy, z * sz + dz))
    return out


def build(k):
    b = k.piece('base')
    # ------------------------------------------------------------------ hull (crosses x = 0)
    b.hull(ring(OUT, 0.3, 0.55, 0.88, -1.5) + ring(OUT, WL + 0.3, 0.93, 0.975), 'paint2', bevel=0.2)
    b.hull(ring(OUT, WL, 0.93, 0.975) + ring(OUT, DECK, sheer=2.0), 'paint', bevel=0.2)
    # raised centre deck: dark sloped edges, light top plate -> crisp outline from above
    sup = [(4.6, 28.0), (10.6, 4.0), (10.0, -24.0), (5.0, -35.8)]
    sup_full = [(0.0, 31.0)] + sup
    b.plan(DECK - 0.2, 11.0, sup_full + [(-x, z) for x, z in reversed(sup)], 'paint2', bevel=0.15, top_inset=1.6)
    inner = [(0.0, 26.0), (3.4, 24.0), (8.3, 3.6), (7.8, -23.0), (3.6, -33.6)]
    b.plan(10.95, 11.2, [(x, z) for x, z in inner] + [(-x, z) for x, z in reversed(inner[1:])], 'paint', bevel=0.06)
    # deck-edge walkway stripes along the main deck (dark), break up the light rim with a line
    b.hull([(13.6, DECK - 0.05, -26.0), (14.8, DECK - 0.05, -12.0), (14.8, DECK - 0.05, 2.0), (13.4, DECK - 0.05, 9.5),
            (13.6, DECK + 0.2, -26.0), (14.8, DECK + 0.2, -12.0), (14.8, DECK + 0.2, 2.0), (13.4, DECK + 0.2, 9.5)],
           'dark', bevel=0.03, mirror=True)
    # ------------------------------------------------------------------ bridge (forward deckhouse)
    b.hull([(x * s, y, z) for s in (-1, 1) for x, y, z in
            [(6.6, 11.0, -1.0), (6.6, 11.0, 12.0), (4.0, 11.0, 15.0),
             (5.4, 15.2, -0.4), (5.4, 15.2, 10.4), (3.2, 15.2, 12.6)]], 'paint', bevel=0.18)
    b.hull([(x * s, y, z) for s in (-1, 1) for x, y, z in
            [(4.6, 15.15, 0.2), (4.6, 15.15, 9.8), (2.6, 15.15, 11.8),
             (4.5, 15.4, 0.3), (4.5, 15.4, 9.7), (2.5, 15.4, 11.7)]], 'team', bevel=0.04)
    # bridge window band (wraps the front)
    b.hull([(x * s, y, z) for s in (-1, 1) for x, y, z in
            [(5.75, 13.4, 9.6), (3.55, 13.4, 12.15), (5.65, 14.4, 9.5), (3.4, 14.4, 11.95),
             (5.9, 13.4, 9.0), (5.85, 14.4, 9.0)]], 'glass', bevel=0.0)
    # mast on the bridge with a radar bar and a red top light
    b.cyl((0, 15.4, 3.0), (0, 22.0, 3.0), 0.45, 8, 'dark', r2=0.3)
    b.box((-3.2, 19.6, 2.6), (3.2, 20.2, 3.4), 'dark', bevel=0.05)
    b.cyl((0, 22.0, 3.0), (0, 22.4, 3.0), 0.3, 8, 'lightr')
    # side running lights on the bridge wings
    b.box((6.5, 12.2, 9.0), (6.75, 12.8, 10.2), 'lightw', bevel=0.0, mirror=True)
    # foredeck depth-charge rack (dark block, black launch tubes)
    b.hull([(x * s, y, z) for s in (-1, 1) for x, y, z in
            [(3.8, 11.0, 15.4), (3.8, 11.0, 21.0), (3.0, 12.9, 16.0), (3.0, 12.9, 20.2)]], 'dark', bevel=0.12)
    for x in (-1.5, 1.5):
        b.cyl((x, 12.6, 16.6), (x, 13.8, 19.6), 0.85, 10, 'black')
    # ------------------------------------------------------------------ twin funnels amidships
    for z0 in (-6.0,):
        b.hull([(x, y, z) for x, y, z in
                [(1.4, 11.0, z0 + 3.0), (5.2, 11.0, z0 + 3.0), (1.4, 11.0, z0 - 4.0), (5.2, 11.0, z0 - 4.0),
                 (1.8, 15.6, z0 + 2.2), (4.8, 15.6, z0 + 2.2), (1.8, 15.6, z0 - 4.6), (4.8, 15.6, z0 - 4.6)]],
               'dark', bevel=0.14, mirror=True)
        b.box((2.2, 15.55, z0 - 4.0), (4.4, 15.75, z0 + 1.6), 'black', bevel=0.0, mirror=True)
    # vents / ammo hatches on the raised deck
    for z in (-14.0, -17.0):
        b.box((-6.8, 11.15, z), (-3.6, 11.5, z + 1.8), 'dark', bevel=0.06)
    b.cyl((5.2, 11.15, -15.6), (5.2, 11.6, -15.6), 1.3, 12, 'dark', bevel=0.05)
    # ------------------------------------------------------------------ gun-tower pylon (stern)
    b.hull([(x * s, y, z) for s in (-1, 1) for x, y, z in
            [(7.0, 10.8, -18.6), (7.0, 10.8, -31.4), (3.8, 21.1, -22.0), (3.8, 21.1, -28.4)]], 'paint2', bevel=0.2)
    b.box((7.0, 13.0, -27.6), (7.25, 13.6, -22.4), 'lightc', bevel=0.0, mirror=True)
    # quarterdeck: stern bollards + red stern light
    for z in (-36.0,):
        b.cyl((4.2, DECK, z), (4.2, DECK + 1.2, z), 0.7, 8, 'dark', mirror=True)
    b.box((-1.6, 6.0, -40.75), (1.6, 6.8, -40.5), 'lightr', bevel=0.0)

    # ------------------------------------------------------------------ turret (gun tower head; origin 0.16, 20.93, -25.17)
    t = k.piece('turret'); A = t.at
    # wide body: the two gun housings joined by a deck, light, team roof between them
    t.hull([A(x * s, y, z) for s in (-1, 1) for x, y, z in
            [(7.2, 0.0, 7.6), (7.2, 0.0, -7.4), (7.0, 3.0, 7.4), (7.0, 3.0, -7.6),
             (5.4, 4.8, 6.6), (5.4, 4.8, -7.0), (6.2, 1.0, 9.0)]], 'paint', bevel=0.2)
    t.hull([A(x * s, y, z) for s in (-1, 1) for x, y, z in
            [(4.9, 4.77, 5.8), (4.9, 4.77, -6.2), (4.8, 4.97, 5.7), (4.8, 4.97, -6.1)]], 'team', bevel=0.04)
    # dark gun cradles at the front corners (the barrels come out of these)
    t.hull([A(x, y, z) for x, y, z in
            [(-6.8, 0.2, 7.2), (-3.0, 0.2, 7.2), (-6.8, 0.2, 12.6), (-3.0, 0.2, 12.6),
             (-6.4, 3.0, 7.2), (-3.4, 3.0, 7.2), (-6.4, 2.6, 12.0), (-3.4, 2.6, 12.0)]], 'dark', bevel=0.12)
    t.hull([A(x, y, z) for x, y, z in
            [(3.2, 0.2, 7.2), (7.0, 0.2, 7.2), (3.2, 0.2, 12.6), (7.0, 0.2, 12.6),
             (3.6, 3.0, 7.2), (6.6, 3.0, 7.2), (3.6, 2.6, 12.0), (6.6, 2.6, 12.0)]], 'dark', bevel=0.12)
    # wedge cab on top, dark, with a cyan visor
    t.hull([A(x * s, y, z) for s in (-1, 1) for x, y, z in
            [(3.1, 4.8, 3.6), (3.1, 4.8, -3.6), (2.6, 10.4, 0.2), (2.6, 10.4, -2.4), (2.8, 7.8, 3.0)]], 'paint2', bevel=0.16)
    t.hull([A(x * s, y, z) for s in (-1, 1) for x, y, z in
            [(2.4, 7.6, 3.15), (2.4, 9.4, 1.6), (2.4, 7.7, 3.3), (2.4, 9.5, 1.75)]], 'lightc', bevel=0.0)
    # two tall swept fins either side (TA's tell): thick, dark, raked back, light tips
    for s in (-1, 1):
        x0, x1 = 7.4 * s, 8.9 * s
        t.hull([A(x, y, z) for x in (x0, x1) for y, z in ((1.0, 6.6), (1.0, -2.6), (18.4, -2.2), (18.4, -6.0))],
               'paint2', bevel=0.16)
        t.box(A(min(x0, x1) + 0.2, 18.3, -5.6), A(max(x0, x1) - 0.2, 18.7, -4.6), 'lightr', bevel=0.0)
        # cross brace from the cab to the fin
        t.box(A(min(2.8 * s, 7.6 * s), 7.0, -1.8), A(max(2.8 * s, 7.6 * s), 8.3, -0.6), 'dark', bevel=0.08)
    # rear vent block
    t.box(A(-3.4, 1.0, -8.6), A(3.4, 3.8, -7.2), 'dark', bevel=0.1)

    # ------------------------------------------------------------------ barrels (recoil 6 back into the cradles)
    br = k.piece('barrel1'); B = br.at
    br.cyl(B(0, 0, -1.2), B(0, 0, 9.9), 0.82, 10, 'steel')
    br.cyl(B(0, 0, 1.0), B(0, 0, 2.2), 1.05, 10, 'dark', bevel=0.05)
    br.cyl(B(0, 0, 8.4), B(0, 0, 10.4), 1.1, 8, 'dark', r2=0.95, rot=math.pi / 8, bevel=0.05)
    br.cyl(B(0, 0, 10.38), B(0, 0, 10.46), 0.5, 8, 'black')
    k.clone('barrel2', 'barrel1')
