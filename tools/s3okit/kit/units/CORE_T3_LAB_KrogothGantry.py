"""Krogoth Gantry (CORE_T3_LAB_KrogothGantry) - Core's experimental factory, 9x9. Closed: the long crane lies flat along
the lane on its hinge, four clamps meet over the pad, and the arms are folded under the crane. On activation (12 s) the
clamps slide out to the sides (move x; jaws and lights retract), the crane stands up 90 deg (turn x) into a ~105 elmo
tower at the back of the lane, its four nano arms unfold to both sides at two heights (y 50 and 87) with the lathes
facing the pad, and the gangplank (QueryBuildInfo: the Krogoth spawns on its origin at z=+1) slides forward.
Core lab family: dark warm armoured blocks, four corner pylons with team caps, near-black lane with ochre hazard
edges, light steel pad, warm lights. Identity from above (open): the biggest footprint in the game, a long light pad
between four clamp blocks, a team-roofed citadel at the back, and an ochre-striped candelabra of nano arms on a tower.
It must visibly fit a Krogoth (x +-28, z -26..+15 at the build point, 70-75 tall): TA's walls at x 12..28, z -30..-1
would cut through its shoulders and silos, so the walls moved behind the crane and out to the sides, and the crane
got thinner (world z -38.5..-30 standing, TA's slab reached z -10). Nothing but the plate stands on the lane.
Pieces (COB): base, glowybits (static lights), gangplank (move z), crane + cranetop (turn x), arm1..4a (turn z, 1 and 4
also move z), arm1..4b (turn z), lathe1..4, nano1..4 (empty emit points), clamp1..4 (move x), clamp1..4b (move x, y,
turn z), clamplight1..4 (move x). The script stays the COB. Preview: OPEN (activatescr end state; COB x moves and z
turns negated for the engine frame). Coordinates are ENGINE/global: X right, Y up, Z forward."""
import math

UNIT = dict(
    res=2048,
    hazard_period=5.0,
    preview_zoom=1.6,
    preview_thumb_half=110,
    flipped=['crane', 'cranetop', 'arm1a', 'arm2a', 'arm3a', 'arm4a', 'arm1b', 'arm2b', 'arm3b', 'arm4b',
             'lathe1', 'lathe2', 'lathe3', 'lathe4'],
    always_visible=['crane', 'cranetop', 'arm1a', 'arm1b', 'lathe1', 'clamp1', 'clamp1b', 'clamplight1'],
    wreck=dict(seed=93, drop=['arm2a', 'clamp4'], pose={'crane': (-28, 0, 0), 'arm1a': (0, 0, -35), 'arm3a': (0, 0, 60)}),
    preview_pose={
        'crane': (-90, 0, 0),
        'arm1a': {'move': (0, 0, -12.25), 'rot': (0, 0, -86.83)}, 'arm1b': (0, 0, -77.69),
        'arm2a': (0, 0, -86.48), 'arm2b': (0, 0, -78.39),
        'arm3a': (0, 0, 83.67), 'arm3b': (0, 0, 74.88),
        'arm4a': {'move': (0, 0, -12.25), 'rot': (0, 0, 86.83)}, 'arm4b': (0, 0, 78.05),
        'clamp1': {'move': (-37.5, 0, 0)}, 'clamp2': {'move': (-37.75, 0, 0)},
        'clamp3': {'move': (37.375, 0, 0)}, 'clamp4': {'move': (37.875, 0, 0)},
        'clamp1b': {'move': (-11.5, -13.0, 0)}, 'clamp2b': {'move': (-11.625, -12.625, 0)},
        'clamp3b': {'move': (11.5, -12.625, 0)}, 'clamp4b': {'move': (11.5, -13.125, 0)},
        'clamplight1': {'move': (8.75, 0, 0)}, 'clamplight2': {'move': (8.875, 0, 0)},
        'clamplight3': {'move': (-9.125, 0, 0)}, 'clamplight4': {'move': (-9.25, 0, 0)},
        'gangplank': {'move': (0, 0, 24.75)},
    },
)

LANE = 38.0


def rect(x0, x1, z0, z1):
    return [(x0, z0), (x1, z0), (x1, z1), (x0, z1)]


def build(k):
    # ------------------------------------------------------------------ base: lane, clamp rails
    b = k.piece('base')
    b.box((-LANE, 0.0, -39.5), (LANE, 0.3, 64.0), 'paint2', bevel=0.05)
    b.box((-LANE, 0.0, -30.0), (-LANE + 4.0, 0.5, 64.0), 'hazard', bevel=0.04, mirror=True)
    for z0, z1 in ((0.0, 13.0), (25.0, 38.0)):                                  # clamp beds outside the lane
        b.box((-66.0, 0.0, z0), (-LANE, 0.45, z1), 'dark', bevel=0.05, mirror=True)
        b.box((-65.0, 0.4, z0 + 2.0), (-LANE, 0.8, z0 + 4.0), 'steel', bevel=0.08, mirror=True)
        b.box((-65.0, 0.4, z1 - 4.0), (-LANE, 0.8, z1 - 2.0), 'steel', bevel=0.08, mirror=True)
    # ------------------------------------------------------------------ citadel behind the crane (solid yardmap rows)
    b.plan(0.0, 32.0, rect(-32.0, 32.0, -64.0, -39.5), 'paint', bevel=0.5, top_inset=3.0)
    b.box((-28.0, 31.95, -61.0), (28.0, 32.5, -42.3), 'team', bevel=0.1)
    b.box((-30.0, 6.0, -39.6), (-17.0, 7.5, -39.3), 'lightw', bevel=0.0, mirror=True)
    # wings either side of the crane slot; the Krogoth's silos end at z -26, the wings at -30
    b.plan(0.0, 20.0, rect(-37.0, -16.0, -40.0, -30.0), 'paint2', bevel=0.35, top_inset=1.6, mirror=True)
    b.box((-34.0, 19.95, -38.0), (-19.0, 20.45, -32.0), 'hazard', bevel=0.06, mirror=True)
    # crane slot: near-black floor, hinge block
    b.box((-16.0, 0.0, -39.5), (16.0, 0.45, -29.0), 'black', bevel=0.0)
    b.box((-3.9, 0.0, -28.5), (3.9, 18.0, -18.5), 'dark', bevel=0.35)
    b.cyl((-3.9, 21.25, -22.5), (3.9, 21.25, -22.5), 4.6, 12, 'steel')
    b.hull([(x, y, z) for x in (-3.9, 3.9) for y, z in ((17.0, -28.0), (17.0, -19.0), (21.0, -26.0), (21.0, -19.5))],
           'dark', bevel=0.15)
    # ------------------------------------------------------------------ rear corner towers (TA: x +-39, z -50)
    for sx in (-1, 1):
        x0, x1 = sorted((sx * 31.0, sx * 56.0))
        xa, xb = sorted((sx * 34.0, sx * 52.0))
        b.plan(0.0, 7.0, rect(x0, x1, -66.0, -40.0), 'paint2', bevel=0.35, top_inset=1.0)
        b.plan(6.5, 18.0, rect(xa, xb, -62.0, -42.0), 'paint', bevel=0.4, top_inset=2.2)
        b.box((xa + 2.0, 17.95, -60.0), (xb - 2.0, 18.5, -44.0), 'team', bevel=0.08)
        b.cyl((sx * 39.0, 18.0, -50.0), (sx * 39.0, 38.0, -50.0), 3.0, 8, 'dark', r2=1.9, rot=math.pi / 8)
    # ------------------------------------------------------------------ front corner pylons (TA: x +-50, z 50..62)
    for sx in (-1, 1):
        x0, x1 = sorted((sx * 40.0, sx * 64.0))
        xa, xb = sorted((sx * 43.0, sx * 61.0))
        b.plan(0.0, 10.0, rect(x0, x1, 46.0, 66.0), 'paint', bevel=0.35, top_inset=1.8)
        b.hull([(x, 9.5, z) for x in (xa, xb) for z in (49.0, 63.0)]
               + [(x, 22.0, z) for x in (xa + 1.5, xb - 1.5) for z in (50.0, 62.0)], 'paint', bevel=0.35)
        b.box((xa + 1.9, 21.95, 50.4), (xb - 1.9, 22.5, 61.6), 'team', bevel=0.08)
        b.hull([(sx * 40.1, 0.0, 49.0), (sx * 40.1, 0.0, 63.0), (sx * 40.1, 8.0, 50.0), (sx * 40.1, 8.0, 62.0),
                (sx * 37.5, 0.0, 51.0), (sx * 37.5, 0.0, 61.0)], 'paint2', bevel=0.2)

    # ------------------------------------------------------------------ glowybits: beacons and pylon lights
    g = k.piece('glowybits')
    for sx in (-1, 1):
        g.box((sx * 39.0 - 2.6, 38.0, -52.6), (sx * 39.0 + 2.6, 44.0, -47.4), 'lightr', bevel=0.3)
        x0, x1 = sorted((sx * 37.4, sx * 38.0))
        g.box((x0, 2.0, 51.5), (x1, 6.5, 60.5), 'lightw', bevel=0.0)

    # ------------------------------------------------------------------ gangplank: the pad (clear; the Krogoth stands on it)
    p = k.piece('gangplank'); G = p.at                                          # origin 0, 0, -23.75; open z = +1
    p.box(G(-27.0, 0.3, -28.0), G(27.0, 0.6, 63.0), 'steel', bevel=0.08)
    p.box(G(-30.0, 0.25, -28.0), G(-27.0, 0.75, 63.0), 'dark', bevel=0.06, mirror=True)
    p.cyl(G(0, 0.55, 0), G(0, 0.68, 0), 20.0, 40, 'dark')
    p.cyl(G(0, 0.6, 0), G(0, 0.74, 0), 17.6, 40, 'steel')

    # ------------------------------------------------------------------ crane, standing when open. Built at rest:
    # crane-local (x, y, z) = global (x, y + 21.25, z - 22.5); local y+ = world -z when standing.
    c = k.piece('crane')
    Y0, Y1, Z0, Z1 = 28.75, 37.25, -36.3, 50.0
    c.box((-11.0, Y0, Z0), (11.0, Y1, Z1), 'paint', bevel=0.5)
    c.box((-3.9, 21.25, -28.0), (3.9, Y0 + 0.1, -17.0), 'dark', bevel=0.3)                     # hinge lug
    c.box((-3.6, Y0 - 0.15, -14.0), (3.6, Y0 + 0.1, 49.0), 'hazard', bevel=0.03)               # faces the pad, standing
    c.box((-11.5, Y0 + 2.0, -30.0), (-10.8, Y1 - 2.0, 48.0), 'paint2', bevel=0.1, mirror=True)
    c.box((-6.5, Y1 - 0.1, -20.0), (6.5, Y1 + 0.25, 46.0), 'team', bevel=0.05)                  # closed: roof stripe
    for z in (-1.0, 25.0):                                                                      # arm saddles
        c.box((-11.3, Y0 - 1.2, z - 5.0), (11.3, Y0 + 0.2, z + 5.0), 'dark', bevel=0.1)
    t = k.piece('cranetop')
    t.hull([(x, y, z) for x in (-15.0, 15.0) for y, z in ((27.0, 50.0), (39.0, 50.0), (27.0, 61.2), (39.0, 61.2))]
           + [(x, y, 45.0) for x in (-11.0, 11.0) for y in (28.75, 37.25)], 'paint2', bevel=0.4)
    t.box((-14.0, 27.6, 61.15), (14.0, 38.4, 61.5), 'team', bevel=0.05)                        # top of the tower, open
    t.box((-6.0, 26.8, 53.0), (6.0, 27.1, 59.0), 'lightw', bevel=0.0)

    # ------------------------------------------------------------------ nano arm 1, cloned to the other three
    a = k.piece('arm1a'); A = a.at                                                  # origin (0, 27.5, 18.75)
    W = 3.6                                                                         # half thickness (height, standing)
    a.hull([A(x, y, z) for z in (-W, W) for x, y in ((3.0, 3.0), (-3.0, 3.0), (3.0, -3.0), (-20.0, -25.5), (-26.0, -25.5),
                                                     (-26.0, -19.5))], 'paint2', bevel=0.3)
    a.hull([A(x, y, z) for z in (W + 0.02, W + 0.25) for x, y in ((3.0, 2.0), (-1.5, 2.0), (2.0, -2.5), (-20.5, -25.0),
                                                                  (-25.5, -25.0), (-25.5, -20.0))],
           'hazard', bevel=0.03)
    b1 = k.piece('arm1b'); B = b1.at                                                # origin (-23, 5, 18.75)
    b1.cyl(B(0, 0, -W), B(0, 0, W + 1.0), 4.2, 12, 'dark')
    b1.hull([B(x, y, z) for z in (-2.6, 2.6) for x, y in ((-2.5, -3.2), (-2.5, 3.2), (23.5, -3.6), (23.5, 3.6))],
            'paint', bevel=0.3)
    b1.hull([B(x, y, z) for z in (2.62, 2.85) for x, y in ((3.8, -2.9), (3.8, 2.9), (21.5, -3.2), (21.5, 3.2))],
            'hazard', bevel=0.03)
    l = k.piece('lathe1'); L = l.at                                                 # origin (-5, 6.25, 18.75)
    l.hull([L(x, y, z) for x in (-4.6, 4.6) for z in (-4.6, 4.6) for y in (-2.0,)]
           + [L(x, 9.0, z) for x in (-4.0, 4.0) for z in (-4.0, 4.0)], 'hazard', bevel=0.3)
    l.cyl(L(0, 9.0, 0), L(0, 14.0, 0), 3.0, 10, 'dark', r2=2.0)
    l.cyl(L(0, 14.0, 0), L(0, 15.5, 0), 2.0, 10, 'lightc')
    for s, m in (('2', False), ('3', True), ('4', True)):
        k.clone('arm%sa' % s, 'arm1a', mirror_x=m)
        k.clone('arm%sb' % s, 'arm1b', mirror_x=m)
        k.clone('lathe%s' % s, 'lathe1', mirror_x=m)

    # ------------------------------------------------------------------ clamp 1, cloned to the other three
    q = k.piece('clamp1'); Q = q.at                                                 # origin (-7.5, 0, 31.5); closed
    q.plan(0.0, 13.0, [(Q(x, 0, z)[0], Q(x, 0, z)[2]) for x, z in ((-17.5, -6.5), (7.5, -6.5), (7.5, 6.0), (-17.5, 6.0))],
           'paint', bevel=0.4, top_inset=1.0)
    q.hull([Q(x, y, z) for x, y, z in
            [(-17.0, 12.5, -5.8), (-17.0, 12.5, 5.3), (2.0, 12.5, -5.8), (2.0, 12.5, 5.3), (-16.4, 18.8, -5.2),
             (-16.4, 18.8, 4.7), (0.8, 18.8, -5.2), (0.8, 18.8, 4.7)]], 'paint2', bevel=0.3)
    q.hull([Q(x, y, z) for x, y, z in
            [(-15.6, 18.75, -4.5), (-15.6, 18.75, 4.0), (0.0, 18.75, -4.5), (0.0, 18.75, 4.0),
             (-15.6, 19.1, -4.5), (-15.6, 19.1, 4.0), (0.0, 19.1, -4.5), (0.0, 19.1, 4.0)]], 'team', bevel=0.04)
    j = k.piece('clamp1b'); J = j.at                                                # origin (-10.37, 15.87, 31.25)
    j.hull([J(x, y, z) for z in (-3.6, 3.6) for x, y in ((-1.7, 0.0), (-1.7, 8.0), (4.0, 11.3), (9.4, 6.0), (9.4, 2.0),
                                                         (3.0, 0.0))], 'dark', bevel=0.3)
    h = k.piece('clamplight1'); H = h.at                                            # origin (-8.75, 5, 31.25)
    h.box(H(-0.5, -3.5, -4.0), H(5.4, 3.5, 4.0), 'dark', bevel=0.2)
    h.box(H(5.3, -2.6, -3.1), H(5.7, 2.6, 3.1), 'lightw', bevel=0.0)
    for s, m in (('2', False), ('3', True), ('4', True)):
        k.clone('clamp%s' % s, 'clamp1', mirror_x=m)
        k.clone('clamp%sb' % s, 'clamp1b', mirror_x=m)
        k.clone('clamplight%s' % s, 'clamplight1', mirror_x=m)
