"""Fibber (ARM_T2_SEA_Fibber) - Arm sonar jamming sub. A split almond: two light leaf-shaped cheeks either side of an open
black slot in the bow, the jammer fork spinning in the slot, a narrow dark spine running aft from it to a tall stern bar.
From above: a short, fat leaf with a black slit down its front half (an eye), team leaves on the front cheeks and stern bar, cyan fork tips.
Short and wide next to the needle Piranha and the arrowhead builder, which keep a solid centre line.
Pieces (TA layout): GP (empty root), base, fork (spin z; origin -0.09, 5.66, 1.47, radius 3: the slot clears it, no
mirror because of the origin), bubbles (empty emit point at the stern).
Submarine: def has waterline 40 and SHIP_SUBMARINE, no floater; run.py resolves water=40 from the movement class.
Coordinates are ENGINE/global: X right, Y up, Z forward. mirror=True builds the -X twin sharing UVs."""

UNIT = dict(
    res=1024,
    wreck=dict(seed=23, pose={'fork': (12, 8, 40)}),
    preview_pose={'fork': (0, 0, 20)},
)

SLOT = 3.7         # half width of the slot; the fork sweeps radius 3.05 about x = -0.09
TOP = 8.6          # flat top of the cheeks


def sym(pts):
    return [(x * s, y, z) for s in (-1, 1) for x, y, z in pts]


def build(k):
    b = k.piece('base')
    # ------------------------------------------------------------------ cheeks: the light leaves (forward half)
    C = [(SLOT, 25.0), (6.4, 21.0), (11.7, 6.0), (11.7, 0.6), (SLOT, 0.6)]
    b.hull([(x, TOP, z) for x, z in [(SLOT, 24.0), (6.0, 20.4), (9.8, 6.2), (9.8, 0.6), (SLOT, 0.6)]]
           + [(x, 5.6, z) for x, z in C] + [(x * 0.84 + 0.6, 2.2, z) for x, z in [(SLOT, 24.0), (6.4, 20.0), (11.7, 6.0), (11.7, 0.6), (SLOT, 0.6)]],
           'paint', bevel=0.2, mirror=True)
    b.hull([(x, y, z) for y in (TOP - 0.05, TOP + 0.2) for x, z in [(4.5, 21.0), (5.9, 18.6), (9.2, 6.4), (9.2, 1.4), (4.5, 1.4)]],
           'team', bevel=0.04, mirror=True)
    # ------------------------------------------------------------------ aft leaves: bare light paint, tapering to the neck
    b.hull([(x, y, z) for x, y, z in
            [(3.0, TOP, 0.6), (9.8, TOP, 0.6), (11.7, 5.6, 0.6), (10.0, 2.2, 0.6), (3.0, 1.0, 0.6),
             (3.0, 7.8, -18.0), (5.0, 7.6, -18.0), (6.0, 5.2, -17.0), (3.0, 1.6, -18.0)]], 'paint', bevel=0.2, mirror=True)
    # ------------------------------------------------------------------ slot floor (black) and the socket the fork turns in
    b.box((-SLOT - 0.2, 1.4, 1.0), (SLOT + 0.2, 2.3, 24.4), 'black', bevel=0.0)
    b.hull(sym([(4.0, 1.4, 1.2), (4.0, 2.4, 1.2), (0.0, 1.0, 26.6), (0.0, 1.8, 26.6), (2.6, 1.2, 24.6), (2.6, 2.3, 24.6)]), 'paint2', bevel=0.1)
    # ------------------------------------------------------------------ spine: dark, narrow, climbs aft to the stern bar
    b.hull(sym([(3.6, 1.0, 1.4), (3.6, 9.9, 1.4), (1.8, 11.2, -3.0), (3.0, 1.2, -20.0), (3.0, 11.6, -20.0), (1.6, 12.2, -14.0)]), 'paint2', bevel=0.2)
    b.cyl((-0.09, 5.66, 1.5), (-0.09, 5.66, 1.0), 3.0, 12, 'black')
    # ------------------------------------------------------------------ stern bar: wide, tall, the second dark block
    b.hull(sym([(4.6, 0.6, -20.0), (4.6, 10.4, -20.0), (7.6, 0.6, -25.6), (7.6, 12.2, -25.6), (7.2, 0.6, -26.0), (7.2, 12.2, -26.0)]), 'dark', bevel=0.18)
    b.hull(sym([(4.4, 10.5, -20.6), (7.0, 12.26, -25.2), (4.4, 10.7, -20.6), (7.0, 12.46, -25.2)]), 'team', bevel=0.04)
    b.cyl((0, 6.0, -25.9), (0, 6.0, -26.3), 3.4, 12, 'black')
    b.cyl((-8.0, 9.0, -24.0), (8.0, 9.0, -24.0), 0.32, 6, 'lightc')
    # ------------------------------------------------------------------ the jammer fork (spins in the slot)
    f = k.piece('fork'); F = f.at
    f.cyl(F(0, 0, 0), F(0, 0, 6.0), 1.7, 8, 'dark', r2=1.4, bevel=0.06)
    f.box(F(-2.9, -0.9, 5.0), F(2.9, 0.9, 7.6), 'dark', bevel=0.08)
    for x0, x1 in ((-2.9, -1.1), (1.1, 2.9)):
        f.box(F(x0, -0.8, 7.0), F(x1, 0.8, 24.0), 'steel', bevel=0.08)
        f.box(F(x0, -0.8, 24.0), F(x1, 0.8, 24.6), 'lightc', bevel=0.0)
