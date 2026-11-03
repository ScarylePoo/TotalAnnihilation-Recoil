"""Shark (CORE_T2_SEA_Shark) - Core sub killer. Literally the fish, as the TA model has it: a blunt pointed snout, big
pectoral fins swept back from the shoulders, a tall dorsal hump, a pinched tail stock and a wide forked tail.
From above: dark body, light steel snout and dorsal, team pectorals and tail flukes, so the top view is a cross on a stick
with a fork at the end. Narrow-waisted where the T1 Snake is wide at the back; the Leviathan is the wide trident.
Pieces (TA layout): base, torp1/2 (empty torpedo points in the shoulders), wake (empty emit point at the stern).
Submarine: def has waterline 40 and SHIP_SUBMARINE, no floater; run.py resolves water=40 from the movement class.
Coordinates are ENGINE/global: X right, Y up, Z forward. mirror=True builds the -X twin sharing UVs."""

UNIT = dict(
    res=1024,
    wreck=dict(seed=31),
    preview_pose={},
)


def sym(pts):
    return [(x * s, y, z) for s in (-1, 1) for x, y, z in pts]


def build(k):
    b = k.piece('base')
    # ------------------------------------------------------------------ fore body and snout
    b.hull(sym([(6.2, 2.6, 2.0), (7.8, 6.4, 3.0), (5.6, 11.2, 2.0), (6.0, 2.6, 14.0), (7.2, 6.4, 14.0), (5.0, 10.6, 14.0),
                (2.6, 4.2, 26.0), (2.6, 8.0, 25.0), (1.0, 5.2, 28.0), (1.0, 7.0, 28.0)]), 'paint', bevel=0.22)
    # light steel head cap: the one big light block on the dark fish
    b.hull(sym([(5.3, 11.0, 12.8), (5.3, 6.4, 12.8), (2.9, 8.5, 25.3), (2.9, 5.2, 25.3), (1.25, 7.5, 28.4), (1.25, 5.2, 28.4), (0.0, 11.4, 12.8)]), 'steel', bevel=0.1)
    # torpedo cheeks
    b.hull([(x, y, z) for x, y, z in [(4.0, 4.6, 12.0), (7.0, 5.0, 12.0), (7.0, 9.4, 12.0), (4.0, 9.8, 12.0),
                                      (3.8, 5.6, 21.8), (6.4, 6.2, 20.4), (6.2, 8.6, 20.4), (3.8, 9.0, 21.8)]], 'paint2', bevel=0.14, mirror=True)
    b.cyl((5.0, 7.5, 20.6), (5.0, 7.5, 21.6), 1.1, 10, 'black', mirror=True)
    # ------------------------------------------------------------------ waist and tail stock (dark, thin: makes the fish)
    b.hull(sym([(6.2, 2.6, 2.0), (7.8, 6.4, 3.0), (5.6, 11.2, 2.0), (3.6, 3.8, -20.0), (4.2, 7.2, -20.0), (3.2, 10.0, -20.0)]), 'paint', bevel=0.2)
    # ------------------------------------------------------------------ dorsal hump: tall, swept, light top
    b.hull(sym([(4.0, 10.8, 10.0), (4.4, 10.6, -2.0), (2.6, 9.6, -13.0), (2.6, 14.6, 5.0), (2.8, 14.6, -2.2), (0.6, 11.0, -13.0)]), 'paint2', bevel=0.18)
    b.hull(sym([(2.0, 14.55, 4.2), (2.2, 14.55, -1.6), (2.0, 14.75, 4.2), (2.2, 14.75, -1.6)]), 'steel', bevel=0.03)
    b.cyl((0, 14.7, 1.0), (0, 16.8, 0.8), 0.36, 8, 'dark', r2=0.28)
    b.cyl((0, 16.8, 0.8), (0, 17.1, 0.8), 0.28, 6, 'lightr')
    # ------------------------------------------------------------------ pectorals: broad, swept back, team
    b.hull([(x, y, z) for y in (5.6, 7.2) for x, z in [(6.8, 14.4), (14.6, 5.8), (14.6, 2.6), (7.2, 0.6)]], 'paint2', bevel=0.14, mirror=True)
    b.hull([(x, y, z) for y in (7.15, 7.4) for x, z in [(7.9, 12.6), (13.9, 5.8), (13.9, 3.2), (7.9, 2.0)]], 'team', bevel=0.04, mirror=True)
    # ------------------------------------------------------------------ forked tail: the widest part, team flukes
    b.hull([(x, y, z) for y in (5.2, 7.6) for x, z in [(3.2, -13.0), (5.0, -14.0), (14.0, -27.8), (9.6, -28.4), (3.2, -24.0)]], 'paint2', bevel=0.16, mirror=True)
    b.hull([(x, y, z) for y in (7.55, 7.8) for x, z in [(4.4, -16.4), (5.0, -15.6), (13.0, -27.2), (10.0, -27.6), (4.4, -23.4)]], 'team', bevel=0.04, mirror=True)
    # stern plug between the flukes, around the wake point
    b.hull(sym([(3.6, 3.8, -20.0), (4.2, 7.2, -20.0), (3.2, 10.0, -20.0), (2.0, 5.2, -25.6), (2.0, 9.0, -25.6)]), 'dark', bevel=0.14)
    b.cyl((0, 7.3, -25.5), (0, 7.3, -25.9), 1.5, 10, 'lightr')
    # upper tail fin
    b.hull(sym([(0.5, 10.0, -12.0), (0.5, 9.8, -21.0), (0.4, 13.0, -24.8), (0.4, 13.0, -21.0)]), 'dark', bevel=0.08)
