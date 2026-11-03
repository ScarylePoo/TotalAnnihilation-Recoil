"""Advanced Construction Sub (CORE_T2_SEA_AdvancedConstructor) - Core T2 underwater builder. Flat and long: a needle ram
nose longer than the hull behind it, a low wide bay amidships whose two flat doors (door1/door2) swing right over onto the
sloped shoulders, a pair of swept delta fins and two big stern nacelles with a slot between them. The boom (boom > neck
> gun) lies folded in the bay and swings up when building.
From above: dark hull, striped bay doors (the builder read; the striped undersides show once open), light steel ram,
team deltas and nacelle tops. Longest silhouette of all the subs; the Leviathan is the wide one.
Pieces (TA layout): base, door1/door2 (turn z 228 deg, door2 = mirrored clone; flipped: undersides face up when open),
boom (turn x 39 deg), neck (turn x -39, turn y), gun, flare (empty nano point), exhaust (empty emit point).
Submarine: def has waterline 40 and SHIP_SUBMARINE, no floater; run.py resolves water=40 from the movement class.
Coordinates are ENGINE/global: X right, Y up, Z forward. mirror=True builds the -X twin sharing UVs."""

UNIT = dict(
    res=1024,
    always_visible=['boom', 'neck', 'gun'],       # inside the closed bay at rest, raised by the build script
    flipped=['door1', 'door2'],
    wreck=dict(seed=27, drop=['door2'], pose={'door1': (0, 0, 60)}),
    preview_pose={},
)

BZ0, BZ1 = -13.1, 11.7         # bay ends = the doors' z extent in the 3DO
HY = 9.04                      # door hinge height


def sym(pts):
    return [(x * s, y, z) for s in (-1, 1) for x, y, z in pts]


def build(k):
    b = k.piece('base')
    # ------------------------------------------------------------------ keel and shoulders. The straight shoulder runs just
    # under the line of the open door (228 deg about the eave, 48 deg down from level), so the open doors lie on it
    b.hull(sym([(9.0, 0.4, BZ0 - 4.0), (9.0, 0.4, BZ1 + 4.0), (9.0, 2.0, BZ0 - 4.0), (9.0, 2.0, BZ1 + 4.0)]), 'paint2', bevel=0.18)
    b.hull([(x, y, z) for z in (BZ0, BZ1) for x, y in
            ((6.0, 1.6), (12.6, 1.6), (6.0, 8.3))], 'paint', bevel=0.16, mirror=True)
    # ------------------------------------------------------------------ fore body and ram: light steel plate on a dark wedge
    b.hull(sym([(13.0, 1.8, BZ1), (13.4, 3.6, BZ1), (6.9, 9.4, BZ1), (0.0, 10.0, BZ1), (5.0, 1.0, 21.0), (5.0, 7.0, 21.0), (0.0, 8.6, 21.0)]), 'paint', bevel=0.2)
    b.hull(sym([(5.0, 1.0, 21.0), (5.0, 7.0, 21.0), (0.0, 8.6, 21.0), (0.5, 3.8, 41.0), (0.5, 5.6, 41.0)]), 'paint', bevel=0.16)
    b.hull(sym([(4.0, 7.45, 21.0), (0.0, 8.68, 21.0), (0.3, 5.8, 39.6), (4.0, 7.65, 21.0), (0.0, 8.88, 21.0), (0.3, 6.0, 39.6)]), 'steel', bevel=0.04)
    # ------------------------------------------------------------------ aft body: dark, drops to the nacelles
    b.hull(sym([(13.0, 1.8, BZ0), (13.4, 3.6, BZ0), (6.9, 9.4, BZ0), (0.0, 10.0, BZ0), (6.0, 1.2, -22.0), (6.0, 8.0, -22.0), (0.0, 8.4, -22.0)]), 'paint2', bevel=0.2)
    # ------------------------------------------------------------------ stern nacelles (the wide, chunky end), team tops
    nac = [(x, y, z) for z in (-20.0, -36.0) for x, y in ((3.0, 2.4), (11.0, 2.4), (13.4, 5.0), (11.0, 9.2), (3.0, 9.2), (2.4, 5.0))]
    nac += [(5.6, 5.0, -40.4), (9.0, 5.0, -40.4), (5.6, 7.2, -40.2), (9.0, 7.2, -40.2)]
    b.hull(nac, 'paint', bevel=0.2, mirror=True)
    b.hull([(x, y, z) for y in (9.15, 9.4) for x, z in [(3.8, -21.0), (10.6, -21.0), (10.6, -35.0), (3.8, -35.0)]], 'team', bevel=0.04, mirror=True)
    b.cyl((7.4, 6.0, -40.0), (7.4, 6.0, -40.6), 1.5, 10, 'lightr', mirror=True)
    # ------------------------------------------------------------------ delta fins (team) + small aft fins (dark)
    b.hull([(x, y, z) for y in (2.4, 3.8) for x, z in [(9.0, 11.0), (24.2, -0.6), (24.2, -4.4), (9.0, -8.0)]], 'paint', bevel=0.14, mirror=True)
    b.hull([(x, y, z) for y in (3.85, 4.05) for x, z in [(11.4, 8.4), (23.6, -1.0), (23.6, -3.8), (11.4, -6.6)]], 'team', bevel=0.04, mirror=True)
    b.hull([(x, y, z) for y in (2.6, 3.6) for x, z in [(9.6, -9.6), (18.0, -16.6), (18.0, -18.0), (9.6, -17.0)]], 'dark', bevel=0.1, mirror=True)
    # ------------------------------------------------------------------ bay floor
    b.box((-6.2, 1.6, BZ0), (6.2, 2.1, BZ1), 'black', bevel=0.0)
    # coaming: closes the slit between the shoulder top and the closed door (it clears the door, which swings outward)
    b.box((5.3, 7.4, BZ0), (6.0, 8.92, BZ1), 'dark', bevel=0.04, mirror=True)
    # ------------------------------------------------------------------ doors: flat, striped both sides
    d = k.piece('door1')
    d.box((-6.27, HY - 0.05, BZ0 + 0.05), (-0.03, HY + 0.3, BZ1 - 0.05), 'hazard', bevel=0.06)
    k.clone('door2', 'door1', mirror_x=True)
    # ------------------------------------------------------------------ boom > neck > gun (origins on x = 0)
    p = k.piece('boom'); P = p.at
    p.box(P(-1.7, -1.1, -14.4), P(1.7, 0.9, 1.0), 'hazard', bevel=0.1)
    n = k.piece('neck'); N = n.at
    n.box(N(-1.5, -1.9, -1.8), N(1.5, 1.6, 1.8), 'dark', bevel=0.1)
    g = k.piece('gun'); G = g.at
    g.hull([G(x, y, z) for x, y, z in [(-3.6, -0.9, -5.6), (3.6, -0.9, -5.6), (-3.6, -0.9, 5.0), (3.6, -0.9, 5.0),
                                       (-2.6, 2.7, -4.6), (2.6, 2.7, -4.6), (-2.0, 2.2, 3.6), (2.0, 2.2, 3.6)]], 'hazard', bevel=0.12)
    g.cyl(G(0, 0.2, 4.8), G(0, -0.8, 13.2), 1.2, 10, 'steel', r2=0.8, bevel=0.05)
    g.cyl(G(0, -0.8, 13.2), G(0, -0.9, 14.0), 0.8, 8, 'lightc')
