"""Skeeter (ARM_T1_SEA_Skeeter) - Arm scout boat. A long narrow dart: needle bow, low raked cockpit amidships, a
raised dark aft deckhouse carrying a small twin-gun turret at the very stern, and two fat outboard engine pods on
the transom (fast). From above: a slim light arrow with a dark spine, a team chevron on the foredeck pointing
forward and a team roof on the turret.
Pieces (TA layout): base, turret (turn y and x), barrel1/2 (recoil 6 along z), flare1/2 (empty muzzles),
flare3/4 (empty, secondary weapon points on the turret top: small missile rails there), wake1/2 (empty).
Value groups from above: light Arm hull, dark paint2 spine/deckhouse, near-black engine pods and gun cradles,
team chevron + turret roof. Floater, waterline 2 (water surface at model y = 2).
Coordinates are ENGINE/global: X right, Y up, Z forward. mirror=True builds the -X twin sharing UVs."""
import math

UNIT = dict(
    res=1024,
    wreck=dict(seed=5, pose={'turret': (0, 60, 0)}),
    preview_pose={'turret': (0, -25, 0)},
)

WL = 2.0
DECK = 4.6
OUT = [(0.0, 33.6), (2.2, 28.0), (5.6, 17.0), (8.4, 6.0), (9.6, -2.0), (9.4, -14.0), (7.6, -27.0), (5.2, -31.6)]


def ring(pts, y, sx=1.0, sz=1.0, dz=0.0, sheer=0.0):
    out = []
    for x, z in pts:
        yy = y + sheer * max(0.0, (z - 10.0) / 23.6) ** 1.5
        for s in ((-1, 1) if x > 0 else (1,)):
            out.append((x * sx * s, yy, z * sz + dz))
    return out


def build(k):
    b = k.piece('base')
    # ------------------------------------------------------------------ hull: deep-V, crosses x = 0
    b.hull(ring(OUT, 0.2, 0.25, 0.9, -1.0) + ring(OUT, WL + 0.4, 0.92, 0.97), 'paint2', bevel=0.16)
    b.hull(ring(OUT, WL + 0.4, 0.92, 0.97) + ring(OUT, DECK, sheer=1.6), 'paint', bevel=0.18)
    # chine strakes: dark lines along the hull sides (speed lines seen from the 3/4 view)
    b.hull([(9.25, 3.0, -22.0), (9.5, 3.0, -2.0), (8.3, 3.0, 6.0), (5.4, 3.0, 16.4),
            (9.4, 3.5, -22.0), (9.65, 3.5, -2.0), (8.45, 3.5, 6.0), (5.55, 3.5, 16.4)], 'dark', bevel=0.03, mirror=True)
    # dark spine: raised centre deck from the cockpit back to the deckhouse
    b.plan(DECK - 0.2, 6.6, [(0.0, 13.0), (4.6, 4.0), (6.6, -4.0), (6.6, -27.4), (3.2, -30.6),
                              (-3.2, -30.6), (-6.6, -27.4), (-6.6, -4.0), (-4.6, 4.0)], 'paint2', bevel=0.14, top_inset=1.0)
    # team chevron on the foredeck, pointing forward (the scout's tell): two wide solid arms on the sheered deck
    dy = lambda z: DECK + 1.6 * max(0.0, (z - 10.0) / 23.6) ** 1.5
    for s in (-1, 1):
        q = [(0.0, 25.0), (2.6, 25.0), (7.0, 8.6), (3.4, 8.6)]
        b.hull([(x * s, dy(z) + h + 0.75 * (z - 8.6) / 16.4, z) for x, z in q for h in (0.1, 0.28)], 'team', bevel=0.04)
    # cockpit: raked light canopy block with a wraparound dark glass band
    b.hull([(x * s, y, z) for s in (-1, 1) for x, y, z in
            [(3.4, 6.5, -3.0), (3.0, 6.5, 6.6), (1.2, 6.5, 10.0),
             (2.7, 10.8, -2.0), (2.2, 10.4, 2.6), (0.8, 8.4, 7.4)]], 'paint', bevel=0.18)
    b.hull([(x * s, y, z) for s in (-1, 1) for x, y, z in
            [(2.95, 7.6, 6.2), (1.15, 7.6, 9.2), (2.5, 9.9, 2.8), (0.85, 8.5, 7.25),
             (3.05, 7.6, 5.4), (2.6, 9.9, 2.0)]], 'glass', bevel=0.0)
    # aft deckhouse under the turret (dark block, team-free; vents)
    b.hull([(x * s, y, z) for s in (-1, 1) for x, y, z in
            [(4.6, 6.5, -9.0), (4.6, 6.5, -27.0), (3.6, 6.5, -29.4),
             (3.4, 12.7, -12.2), (3.6, 12.7, -26.6), (2.6, 12.7, -28.0)]], 'paint2', bevel=0.16)
    for z in (-13.4, -14.6, -15.8):
        b.box((-2.6, 12.65, z), (2.6, 12.85, z + 0.6), 'black', bevel=0.0)
    b.box((4.0, 9.6, -24.0), (4.35, 10.2, -16.0), 'lightc', bevel=0.0, mirror=True)
    # radar mast between cockpit and deckhouse
    b.cyl((0, 6.5, -6.0), (0, 14.6, -6.6), 0.35, 8, 'dark', r2=0.22)
    b.box((-2.4, 13.2, -6.9), (2.4, 13.7, -6.2), 'dark', bevel=0.04)
    b.cyl((0, 14.6, -6.6), (0, 14.9, -6.6), 0.26, 6, 'lightr')
    # twin outboard engine pods on the transom (fat, black/dark, cyan exhaust glow)
    for s in (1,):
        b.hull([(x, y, z) for x, y, z in
                [(3.2, 1.4, -27.0), (7.6, 1.4, -27.0), (3.2, 1.4, -35.0), (7.6, 1.4, -35.0),
                 (3.6, 6.2, -27.6), (7.2, 6.2, -27.6), (3.8, 5.6, -34.0), (7.0, 5.6, -34.0)]],
               'dark', bevel=0.2, mirror=True)
        b.box((4.3, 5.9, -33.2), (6.5, 6.35, -28.6), 'paint', bevel=0.05, mirror=True)
        b.cyl((5.4, 3.2, -35.0), (5.4, 3.2, -35.2), 1.3, 10, 'lightc', mirror=True)
    # nav lights
    b.box((8.9, 4.3, 4.0), (9.2, 4.8, 5.4), 'lightw', bevel=0.0, mirror=True)
    b.cyl((0, DECK + 0.4, 31.0), (0, DECK + 0.9, 31.0), 0.3, 6, 'lightr')

    # ------------------------------------------------------------------ turret (origin 0.25, 12.75, -24.25)
    t = k.piece('turret'); A = t.at
    t.cyl(A(0, 0, -1.0), A(0, 0.4, -1.0), 3.4, 14, 'dark', bevel=0.04)
    t.hull([A(x * s, y, z) for s in (-1, 1) for x, y, z in
            [(4.0, 0.3, 4.6), (4.2, 0.3, -4.8), (3.4, 2.6, 3.6), (3.6, 2.6, -4.2), (2.4, 0.8, 6.2)]], 'paint', bevel=0.14)
    t.hull([A(x * s, y, z) for s in (-1, 1) for x, y, z in
            [(2.8, 2.57, 3.0), (3.0, 2.57, -3.6), (2.75, 2.75, 2.9), (2.95, 2.75, -3.5)]], 'team', bevel=0.03)
    # small missile rails on the roof, either side of the flare3/flare4 points (secondary weapon)
    for x in (-1.6, 1.6):
        t.cyl(A(x, 3.0, -2.6), A(x, 3.0, 2.6), 0.42, 8, 'dark', bevel=0.02)
        t.cyl(A(x, 3.0, 2.6), A(x, 3.0, 3.1), 0.42, 8, 'hazard', r2=0.12)
    # gun cradles
    for x in (-2.4, 2.4):
        t.box(A(x - 0.9, 0.5, 4.0), A(x + 0.9, 2.1, 6.6), 'dark', bevel=0.08)

    # ------------------------------------------------------------------ barrels (light guns, recoil 6)
    br = k.piece('barrel1'); B = br.at
    br.cyl(B(0, 0, -0.6), B(0, 0, 5.9), 0.42, 8, 'steel')
    br.cyl(B(0, 0, 4.9), B(0, 0, 6.1), 0.6, 8, 'dark', rot=math.pi / 8, bevel=0.03)
    br.cyl(B(0, 0, 6.08), B(0, 0, 6.14), 0.25, 8, 'black')
    k.clone('barrel2', 'barrel1')
