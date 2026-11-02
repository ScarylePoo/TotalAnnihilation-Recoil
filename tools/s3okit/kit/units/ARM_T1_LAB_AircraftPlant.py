"""Aircraft Plant (ARM_T1_LAB_AircraftPlant) - Arm T1 air factory. A broad light airfield deck (the yardmap lane, x +-40,
plus team-striped shoulders) carrying a big round pad, with TA's back row kept: a tall light control tower with a cyan
cab (left), a hangar block whose roof hatch (door1) swings up and drops behind it (centre) and a round silo whose cap
(door2) flips up on its edge (right). Opening, the elevator plates (plate1/plate2) rise to the roofline and the nano
arms (post/nano 1-2) unfold above them toward the pad.
Arm lab family: light chamfered blocks, team panels, dark/hazard lane markings, light round pad, cyan lights.
Identity from above: a huge light deck with a round pad and two team side stripes, a dark back row with a tower
(the kbot lab is a cross of four blocks, the vehicle plant a hall split in two).
Pieces (COB): base, plate1/2 (move y; the hangar and silo lifts), post1/2 (turn y), nano1/2 (turn z / x), beam1/2
(empty nano emit points), door1 (turn x, move y), door2 (turn z, move y), cylinder (the silo, static), radar (hidden
at Create: left empty), light (deck beacon), pad (spin y; QueryBuildInfo).
Preview: OPEN (activatescr end state; COB z turns and x moves negated for the engine frame).
Coordinates are ENGINE/global: X right, Y up, Z forward."""
import math

UNIT = dict(
    res=2048,
    hazard_period=5.0,
    always_visible=['plate1', 'plate2', 'post1', 'post2', 'nano1', 'nano2'],
    wreck=dict(seed=65, drop=['door2']),
    preview_pose={
        'door1': {'move': (0, -20.875, 0), 'rot': (-88.65, 0, 0)},
        'door2': {'move': (0, -13.25, 0), 'rot': (0, 0, -90.0)},
        'plate1': {'move': (0, 19.375, 0)}, 'plate2': {'move': (0, 24.0, 0)},
        'post1': (0, 76.95, 0), 'post2': (0, -48.15, 0),
        'nano1': (0, 0, 128.7), 'nano2': (132.3, 0, 0),
        'radar': 'hide',
    },
)

DY = 1.0             # deck top


def nano_arm(n, tip, mat_top='hazard'):
    """folded nano arm from the piece origin up to the emit point `tip` (piece-relative)"""
    N = n.at
    tx, ty, tz = tip
    n.box(N(-2.2, -2.0, -2.2), N(2.2, 2.0, 2.2), 'steel', bevel=0.3)
    n.hull([N(x, y, z) for x, y, z in [(-1.6, 0.0, -1.6), (1.6, 0.0, -1.6), (-1.6, 0.0, 1.6), (1.6, 0.0, 1.6)]]
           + [N(tx * 0.85 + dx, ty * 0.85, tz * 0.85 + dz) for dx in (-1.3, 1.3) for dz in (-1.3, 1.3)], 'dark',
           bevel=0.2)
    n.hull([N(tx * 0.8 + dx, ty * 0.8 + dy, tz * 0.8 + dz) for dx in (-2.0, 2.0) for dy in (-1.6, 1.6) for dz in (-2.0, 2.0)]
           + [N(tx + dx, ty, tz + dz) for dx in (-1.0, 1.0) for dz in (-1.0, 1.0)], mat_top, bevel=0.15)
    n.cyl(N(tx * 0.97, ty * 0.97, tz * 0.97), N(tx * 1.03, ty * 1.03, tz * 1.03), 1.2, 10, 'lightc')


def build(k):
    # ------------------------------------------------------------------ base: deck, back row
    b = k.piece('base')
    b.plan(0.0, DY, [(-56.0, -15.0), (56.0, -15.0), (56.0, 47.0), (-56.0, 47.0)], 'paint', bevel=0.2, top_inset=0.5)
    b.box((-36.3, DY - 0.05, -14.5), (36.3, DY + 0.07, 44.0), 'paint2', bevel=0.04)               # dark lane
    b.box((-54.8, DY - 0.05, -12.0), (-41.6, DY + 0.12, 45.0), 'team', bevel=0.05, mirror=True)  # team shoulders
    b.box((-40.0, DY - 0.05, -13.0), (-36.4, DY + 0.1, 46.0), 'hazard', bevel=0.04, mirror=True)  # lane edges
    b.box((-36.0, DY - 0.05, 44.0), (36.0, DY + 0.08, 46.0), 'paint2', bevel=0.03)                 # front sill
    for x in (-30.0, -18.0, -6.0, 6.0, 18.0, 30.0):
        b.box((x - 1.0, DY, 46.6), (x + 1.0, DY + 0.5, 47.1), 'lightc', bevel=0.0)
    # back strip (z -48..-15): dark service apron under the row
    b.box((-56.0, 0.0, -48.5), (56.0, 0.8, -15.0), 'paint2', bevel=0.1)
    # control tower (left): tapered light shaft, dark cab with cyan glazing
    b.hull([(x, 0.6, z) for x, z in ((-23.0, -47.0), (-1.5, -47.0), (-1.5, -26.0), (-23.0, -26.0))]
           + [(x, 14.0, z) for x, z in ((-21.5, -45.5), (-3.0, -45.5), (-3.0, -27.5), (-21.5, -27.5))], 'paint',
           bevel=0.4)
    b.hull([(x, 13.5, z) for x, z in ((-18.0, -42.0), (-6.0, -42.0), (-6.0, -31.0), (-18.0, -31.0))]
           + [(x, 50.0, z) for x, z in ((-14.6, -39.0), (-9.0, -39.0), (-9.0, -33.8), (-14.6, -33.8))], 'paint',
           bevel=0.35)
    b.hull([(x, 49.0, z) for x, z in ((-16.0, -40.6), (-7.6, -40.6), (-7.6, -32.2), (-16.0, -32.2))]
           + [(x, 58.0, z) for x, z in ((-17.6, -42.2), (-6.0, -42.2), (-6.0, -30.6), (-17.6, -30.6))], 'paint2',
           bevel=0.3)
    b.box((-17.9, 53.0, -42.5), (-5.7, 55.6, -30.3), 'lightc', bevel=0.1)
    b.hull([(x, 57.9, z) for x, z in ((-17.6, -42.2), (-6.0, -42.2), (-6.0, -30.6), (-17.6, -30.6))]
           + [(x, 62.0, z) for x, z in ((-15.0, -39.6), (-8.6, -39.6), (-8.6, -33.2), (-15.0, -33.2))], 'team',
           bevel=0.25)
    b.cyl((-11.8, 61.9, -36.4), (-11.8, 66.0, -36.4), 0.7, 8, 'steel')
    b.box((-12.4, 65.8, -37.0), (-11.2, 67.0, -35.8), 'lightr', bevel=0.0)
    # left annex: low block with a team roof
    b.plan(0.6, 10.0, [(-55.0, -47.0), (-25.0, -47.0), (-25.0, -26.0), (-55.0, -26.0)], 'paint', bevel=0.35,
           top_inset=1.0)
    b.box((-52.0, 9.9, -44.0), (-28.0, 10.4, -29.0), 'team', bevel=0.1)
    b.box((-50.0, 4.0, -25.75), (-30.0, 5.2, -25.45), 'lightc', bevel=0.0)
    # hangar shell (interior x -0.3..25.3, z -46.8..-25.8 is the lift well)
    for lo, hi in (((-2.0, 0.6, -48.4), (-0.4, 19.6, -24.2)), ((25.4, 0.6, -48.4), (27.0, 19.6, -24.2)),
                   ((-0.4, 0.6, -25.7), (25.4, 19.6, -24.2)), ((-0.4, 0.6, -48.4), (25.4, 18.0, -47.0))):
        b.box(lo, hi, 'paint', bevel=0.25)
    for lo, hi in (((-2.0, 19.5, -48.4), (-0.4, 20.0, -24.2)), ((25.4, 19.5, -48.4), (27.0, 20.0, -24.2)),
                   ((-0.4, 19.5, -25.7), (25.4, 20.0, -24.2))):
        b.box(lo, hi, 'hazard', bevel=0.06)
    b.box((2.0, 3.0, -24.3), (23.0, 12.0, -23.9), 'paint2', bevel=0.08)                         # hangar front panel
    b.box((4.0, 13.4, -23.95), (21.0, 14.4, -23.75), 'lightc', bevel=0.0)
    b.box((0.0, 0.6, -46.6), (25.0, 0.9, -26.0), 'black', bevel=0.0)                            # well floor

    # ------------------------------------------------------------------ cylinder: the silo (interior x 32..46, z -36.5..-15.2)
    c = k.piece('cylinder')
    for lo, hi in (((29.4, 0.6, -38.2), (31.9, 28.6, -13.2)), ((46.1, 0.6, -38.2), (48.6, 28.6, -13.2)),
                   ((31.9, 0.6, -15.1), (46.1, 28.6, -13.2)), ((31.9, 0.6, -38.2), (46.1, 28.6, -36.5))):
        c.box(lo, hi, 'paint', bevel=0.3)
    for x, z in ((29.4, -38.2), (48.6, -38.2), (29.4, -13.2), (48.6, -13.2)):                    # round corner posts
        c.cyl((x, 0.6, z), (x, 29.4, z), 2.6, 12, 'paint2', rot=math.pi / 12)
    for lo, hi in (((29.6, 28.5, -38.0), (31.9, 29.1, -13.4)), ((46.1, 28.5, -38.0), (48.4, 29.1, -13.4)),
                   ((31.9, 28.5, -15.1), (46.1, 29.1, -13.4)), ((31.9, 28.5, -38.0), (46.1, 29.1, -36.5))):
        c.box(lo, hi, 'team', bevel=0.08)
    c.box((33.0, 8.0, -13.3), (45.0, 9.2, -13.0), 'lightc', bevel=0.0)
    c.box((32.0, 0.6, -36.4), (46.0, 0.9, -15.2), 'black', bevel=0.0)

    # ------------------------------------------------------------------ hatches
    d1 = k.piece('door1'); D = d1.at
    d1.box(D(-13.6, -0.35, 0.2), D(11.6, 0.35, 20.8), 'paint', bevel=0.2)
    d1.box(D(-11.6, 0.3, 2.0), D(9.6, 0.55, 19.0), 'team', bevel=0.06)
    d2 = k.piece('door2'); E = d2.at
    e_pts = [(-13.5, -10.4), (-0.2, -10.4), (-0.2, 10.4), (-13.5, 10.4)]
    d2.box(E(-13.6, -0.35, -10.5), E(-0.1, 0.35, 10.5), 'paint', bevel=0.2)
    d2.box(E(-12.0, 0.3, -8.8), E(-1.7, 0.55, 8.8), 'team', bevel=0.06)

    # ------------------------------------------------------------------ lifts + nano arms
    p1 = k.piece('plate1'); P = p1.at
    p1.box(P(-12.8, -0.6, -9.7), P(12.3, 0.0, 10.9), 'paint2', bevel=0.15)
    for lo, hi in (((-12.6, -0.05, -9.5), (12.1, 0.2, -7.5)), ((-12.6, -0.05, 8.7), (12.1, 0.2, 10.7)),
                   ((-12.6, -0.05, -7.5), (-10.6, 0.2, 8.7)), ((10.1, -0.05, -7.5), (12.1, 0.2, 8.7))):
        p1.box(P(*lo), P(*hi), 'hazard', bevel=0.03)
    p2 = k.piece('plate2'); Q = p2.at
    p2.box(Q(-6.8, -0.6, -10.4), Q(6.6, 0.0, 10.3), 'paint2', bevel=0.15)
    for lo, hi in (((-6.6, -0.05, -10.2), (6.4, 0.2, -8.4)), ((-6.6, -0.05, 8.3), (6.4, 0.2, 10.1))):
        p2.box(Q(*lo), Q(*hi), 'hazard', bevel=0.03)
    for nm in ('post1', 'post2'):
        q = k.piece(nm); R = q.at
        q.cyl(R(0, 0.0, 0), R(0, 9.4, 0), 2.0, 10, 'dark', rot=math.pi / 10)
        q.cyl(R(0, 0.0, 0), R(0, 1.2, 0), 3.0, 10, 'steel', rot=math.pi / 10)
    nano_arm(k.piece('nano1'), (6.99, 10.66, -0.07))
    nano_arm(k.piece('nano2'), (-0.07, 10.93, -8.05))

    # ------------------------------------------------------------------ deck beacon and pad
    k.piece('light').box((-55.4, DY, 37.0), (-50.8, 4.6, 41.6), 'lightr', bevel=0.3)
    pd = k.piece('pad'); Pd = pd.at
    pd.cyl(Pd(0, DY - 0.33, 0), Pd(0, DY + 0.1, 0), 26.0, 40, 'dark', bevel=0.12)
    pd.cyl(Pd(0, DY + 0.1, 0), Pd(0, DY + 0.22, 0), 23.8, 40, 'paint')
    pd.cyl(Pd(0, DY + 0.2, 0), Pd(0, DY + 0.3, 0), 4.2, 16, 'paint2')
