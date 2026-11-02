"""Advanced Aircraft Plant (CORE_T2_LAB_AdvancedAircraftPlant) - Core T2 air factory. A broad dark chamfered deck
(lane x +-40, team shoulders, ochre lane edges) with a light steel octagon pad in front of a heavy dark hall: its back
half carries a tall control tower (team cap, warm cab), red beacons (blinks) and a spinning dish; its front half is
a lift well under a roof of two armoured blocks (block1/block2). On activation the roof blocks flip 180 deg outward
over their outer edges to lie on the deck either side of the hall (their undersides, team-plated and carrying the
heads/bumps/conduits machinery, become their tops), the lift (pedistal) rises 12.5, the gun sleeves slide out and the
two nano guns (gun1/gun2) turn 180 to aim at the pad.
Core lab family (T2 = taller, more parts): dark warm armour, team caps, near-black lane with ochre hazard edges, light
steel pad, warm lights. Identity from above (open): a dark hall with a tower at the back, two team-topped blocks
flipped out beside it, a hazard-framed lift between them, a light octagon on a huge dark deck (the T1 Core air plant
has its tower on the right and a sliding drawer).
Pieces (COB): base, block1/2 (turn z), head1/2 (move), bump1/2 (move), conduit1/2 (move), pedistal (move y),
sleeve1/2 (move x), gun1/2 (turn x), beam1/2 (empty nano emit points), dish (spin y), blinks (beacons), pad
(spin y; QueryBuildInfo).
Preview: OPEN (activatescr end state; COB z turns and x moves negated for the engine frame).
Coordinates are ENGINE/global: X right, Y up, Z forward."""
import math

UNIT = dict(
    res=2048,
    hazard_period=5.0,
    flipped=['block1', 'block2', 'head1', 'head2', 'bump1', 'bump2', 'conduit1', 'conduit2'],
    always_visible=['pedistal', 'sleeve1', 'sleeve2', 'gun1', 'gun2', 'head1', 'head2', 'bump1', 'bump2',
                    'conduit1', 'conduit2'],
    wreck=dict(seed=78, drop=['dish']),
    preview_pose={
        'block1': (0, 0, 180.23), 'block2': (0, 0, -180.23),
        'pedistal': {'move': (0, 12.5, 0)},
        'sleeve1': {'move': (-9.25, 0, 0)}, 'sleeve2': {'move': (9.125, 0, 0)},
        'head1': {'move': (-2.0, -7.125, 0)}, 'head2': {'move': (2.0, -7.125, 0)},
        'bump1': {'move': (6.0, 1.0, 0)}, 'bump2': {'move': (-6.0, 1.0, 0)},
        'conduit1': {'move': (-9.25, 0, -0.75)}, 'conduit2': {'move': (9.375, 0, 0)},
        'gun1': (179.77, 0, 0), 'gun2': (179.77, 0, 0),
    },
)

DY = 1.2             # deck top
HY = 16.88           # lower hall height / roof block pivot


def octagon(r, cz, cx=0.0):
    return [(cx + r * math.cos(math.pi / 8 + i * math.pi / 4), cz + r * math.sin(math.pi / 8 + i * math.pi / 4))
            for i in range(8)]


def build(k):
    # ------------------------------------------------------------------ deck
    b = k.piece('base')
    deck = [(-56.0, -12.0), (-52.0, -16.0), (52.0, -16.0), (56.0, -12.0), (56.0, 43.0), (51.0, 48.0), (-51.0, 48.0),
            (-56.0, 43.0)]
    b.plan(0.0, DY, deck, 'paint', bevel=0.2, top_inset=1.0)
    b.box((-38.0, DY - 0.05, -13.0), (38.0, DY + 0.07, 45.0), 'paint2', bevel=0.04)
    b.box((-40.0, DY - 0.05, -13.0), (-36.4, DY + 0.1, 45.0), 'hazard', bevel=0.04, mirror=True)
    b.box((-53.0, DY - 0.05, -2.0), (-42.0, DY + 0.12, 42.0), 'team', bevel=0.05, mirror=True)
    for x in (-24.0, -8.0, 8.0, 24.0):
        b.box((x - 2.0, 0.4, 47.2), (x + 2.0, 1.2, 47.6), 'lightw', bevel=0.0)
    b.box((-56.0, 0.0, -48.0), (56.0, 0.8, -16.0), 'paint2', bevel=0.1)                        # back apron
    # ------------------------------------------------------------------ hall: back half (tower), front lower walls
    b.box((-25.0, 0.0, -48.0), (25.0, 32.5, -23.8), 'paint', bevel=0.45)
    b.box((-24.0, 32.4, -47.0), (24.0, 32.9, -36.0), 'hazard', bevel=0.06)
    b.box((1.0, 32.4, -35.4), (24.0, 32.9, -24.8), 'team', bevel=0.06)
    b.box((-26.0, 0.0, -44.0), (-25.0, 28.0, -28.0), 'paint2', bevel=0.15, mirror=True)        # flank ribs
    for lo, hi in (((-25.0, 0.0, -23.8), (-15.2, HY, -0.2)), ((15.2, 0.0, -23.8), (25.0, HY, -0.2)),
                   ((-15.2, 0.0, -6.0), (15.2, HY, -0.2))):
        b.box(lo, hi, 'paint', bevel=0.35)
    b.box((-15.2, 0.0, -23.8), (15.2, 2.4, -6.0), 'black', bevel=0.0)                           # lift well floor
    b.box((-12.0, 8.0, -0.3), (12.0, 9.4, 0.0), 'lightw', bevel=0.0)
    # control tower (back left of the roof)
    b.hull([(x, 32.4, z) for x in (-22.0, -4.0) for z in (-46.0, -31.0)]
           + [(x, 48.0, z) for x in (-17.0, -9.0) for z in (-42.0, -35.0)], 'paint', bevel=0.35)
    b.hull([(x, 47.0, z) for x in (-18.0, -8.0) for z in (-43.0, -34.0)]
           + [(x, 54.0, z) for x in (-19.5, -6.5) for z in (-44.5, -32.5)], 'paint2', bevel=0.3)
    b.box((-19.8, 50.0, -44.8), (-6.2, 52.0, -32.2), 'lightw', bevel=0.1)
    b.hull([(x, 53.9, z) for x in (-19.5, -6.5) for z in (-44.5, -32.5)]
           + [(x, 56.6, z) for x in (-16.5, -9.5) for z in (-41.5, -35.5)], 'team', bevel=0.2)
    bl = k.piece('blinks')
    for x in (-19.0, -12.0):
        bl.box((x, 32.5, -28.4), (x + 2.6, 35.6, -25.4), 'lightr', bevel=0.15)
    d = k.piece('dish'); D = d.at                                                             # spinning dish
    d.cyl(D(0, -0.5, 0), D(0, 4.0, 0), 1.0, 8, 'steel')
    d.hull([D(x, y, z) for x, y, z in [(-5.0, 3.0, 0.6), (5.0, 3.0, 0.6), (-5.0, 10.3, -0.4), (5.0, 10.3, -0.4),
                                       (-3.4, 3.4, 1.5), (3.4, 3.4, 1.5), (-3.4, 9.8, 0.8), (3.4, 9.8, 0.8)]], 'dark',
           bevel=0.12)
    d.box(D(-0.8, 6.0, 1.2), D(0.8, 7.4, 1.8), 'lightr', bevel=0.0)

    # ------------------------------------------------------------------ roof blocks (block1 origin -25, 16.88, -12.52)
    r = k.piece('block1'); R = r.at
    r.box(R(0.2, 0.0, -11.1), R(24.8, 15.0, 12.3), 'paint', bevel=0.5)
    r.box(R(1.6, 14.95, -9.6), R(23.4, 15.4, 10.8), 'team', bevel=0.1)                        # roof (closed)
    r.box(R(1.6, -0.4, -9.6), R(23.4, 0.05, 10.8), 'team', bevel=0.1)                          # underside (open top)
    r.box(R(-0.2, 3.0, -8.0), R(0.3, 12.0, 8.0), 'paint2', bevel=0.08)                          # outer face panel
    k.clone('block2', 'block1', mirror_x=True)
    for nm, sx in (('head1', 1), ('head2', -1)):                                               # heads (under the roof)
        h = k.piece(nm); H = h.at
        x0, x1 = sorted((sx * -7.0, sx * 9.5))
        h.box(H(x0, -5.4, -2.2), H(x1, 0.3, 4.6), 'steel', bevel=0.3)
        h.box(H(x0 + 0.6, -5.8, -1.6), H(x1 - 0.6, -5.3, 4.0), 'hazard', bevel=0.04)
    for nm, sx in (('bump1', 1), ('bump2', -1)):
        u = k.piece(nm); U_ = u.at
        x0, x1 = sorted((0.0, sx * 5.0))
        u.box(U_(x0, -4.2, -5.0), U_(x1, 4.2, 5.2), 'dark', bevel=0.4)
    for nm, sx in (('conduit1', 1), ('conduit2', -1)):
        c = k.piece(nm); C = c.at
        c.cyl(C(0.0, 0.2, 0), C(-sx * 9.4, 0.2, 0), 1.2, 8, 'steel')
    # ------------------------------------------------------------------ lift + guns (pedistal origin 0, 2.5, -16.25)
    p = k.piece('pedistal'); P = p.at
    p.box(P(-14.8, 0.0, -7.3), P(14.8, 14.3, 9.8), 'dark', bevel=0.35)
    for lo, hi in (((-14.4, 14.2, -6.9), (14.4, 14.6, -5.0)), ((-14.4, 14.2, 7.6), (14.4, 14.6, 9.4))):
        p.box(P(*lo), P(*hi), 'hazard', bevel=0.04)
    s = k.piece('sleeve1'); S = s.at
    s.box(S(-8.6, -2.4, 0.4), S(-0.2, 7.8, 13.4), 'paint2', bevel=0.3)
    k.clone('sleeve2', 'sleeve1', mirror_x=True)
    g = k.piece('gun1'); G = g.at                                       # points back at rest, beam1 (6.19, 2.84, -7.23)
    g.box(G(0.4, -4.6, -3.0), G(8.4, 4.6, 0.0), 'steel', bevel=0.35)
    g.cyl(G(6.19, 2.84, -2.8), G(6.19, 2.84, -6.2), 1.4, 10, 'dark', r2=1.0)
    g.cyl(G(6.19, 2.84, -6.1), G(6.19, 2.84, -7.23), 1.05, 10, 'lightc')
    k.clone('gun2', 'gun1', mirror_x=True)

    # ------------------------------------------------------------------ pad (origin 0, 1.18, 25): octagon
    pd = k.piece('pad'); Pd = pd.at
    pd.plan(Pd(0, -0.1, 0)[1], Pd(0, 0.45, 0)[1], octagon(21.5, 25.0), 'dark', bevel=0.12, top_inset=0.4)
    pd.plan(Pd(0, 0.4, 0)[1], Pd(0, 0.55, 0)[1], octagon(19.0, 25.0), 'steel', bevel=0.0)
    for a in range(4):
        t = math.radians(a * 90 + 22.5)
        pd.hull([Pd(rr * math.cos(t + dt), yy, rr * math.sin(t + dt)) for rr in (19.1, 20.8) for dt in (-0.18, 0.18)
                 for yy in (0.4, 0.55)], 'hazard', bevel=0.0)
