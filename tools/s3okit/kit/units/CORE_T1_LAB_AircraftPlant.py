"""Aircraft Plant (CORE_T1_LAB_AircraftPlant) - Core T1 air factory, built to the third-party remodel's piece layout
(Lua unit script scripts/CORE_T1_LAB_AircraftPlant.lua drives it; Lua angles/moves are engine-frame, no sign flips).
A broad dark chamfered deck (the lane, x +-40) with team shoulders and an octagonal pad (padbase) ringed by chasing
lights (pad1..3: one third of the ring each, cycled by hide/show), and a back row: a heavy dark tower block on the right
topped by a control tower with a team cap, and the `bay` - a long armoured drawer that slides 18 left out of the
tower on Open, exposing its cradle: the nano boom (narm1/nano1) swings up and aims over the pad, the gripper arm
(arm1b/arm1/arm1top/arm1bot) and conduit (pow1/pow2) unfold, the front door (door2) swings in and the platform
(plate) carrying the second nano head (nano2) slides out of the bay. The radar on the bay roof spins.
Core lab family: dark warm armour, pylons/towers with team caps, near-black lane with ochre hazard edges, light
steel pad, warm lights. Identity from above: a huge dark deck with a light octagon and two team shoulder stripes, a
tall tower at the back right (the Arm air plant is a light deck with a tower on the left).
Preview: OPEN (end state of Open()); pad2/pad3 hidden (one light frame shows at a time after the first cycle).
Coordinates are ENGINE/global: X right, Y up, Z forward."""
import math

UNIT = dict(
    res=2048,
    hazard_period=5.0,
    always_visible=['narm1', 'nano1', 'arm1b', 'arm1', 'arm1top', 'arm1bot', 'pow1', 'pow2', 'plate', 'nano2'],
    wreck=dict(seed=66, drop=['radar']),
    preview_pose={
        'bay': {'move': (-18.0, 0, 0)},
        'narm1': (84.0, 0, 0), 'nano1': (-75.0, 0, 0),
        'arm1b': {'move': (-11.0, 0, 0)}, 'pow1': (0, 0, -90.0), 'door2': (0, 90.0, 0),
        'arm1': (30.0, 0, 0), 'arm1top': (-50.0, 0, 0), 'arm1bot': (75.06, 0, 0), 'pow2': (90.0, 0, 0),
        'plate': {'move': (0, 0, 8.47)}, 'nano2': (0, 40.0, 0),
        'pad2': 'hide', 'pad3': 'hide',
    },
)

DY = 2.5             # deck top
PZ = 20.5            # pad centre z


def octagon(r, cz, cx=0.0):
    return [(cx + r * math.cos(math.pi / 8 + i * math.pi / 4), cz + r * math.sin(math.pi / 8 + i * math.pi / 4))
            for i in range(8)]


def build(k):
    # ------------------------------------------------------------------ base: deck, rail bed, tower block
    b = k.piece('base')
    deck = [(-56.0, -12.0), (-52.0, -16.0), (52.0, -16.0), (56.0, -12.0), (56.0, 43.0), (51.0, 48.0), (-51.0, 48.0),
            (-56.0, 43.0)]
    b.plan(0.0, DY, deck, 'paint', bevel=0.25, top_inset=2.0)
    b.box((-38.0, DY - 0.05, -13.0), (38.0, DY + 0.07, 45.0), 'paint2', bevel=0.04)                  # lane panel
    b.box((-40.0, DY - 0.05, -13.0), (-36.4, DY + 0.1, 45.0), 'hazard', bevel=0.04, mirror=True)   # lane edges
    b.box((-52.0, DY - 0.05, -10.0), (-42.0, DY + 0.12, 42.0), 'team', bevel=0.05, mirror=True)   # team shoulders
    for x in (-24.0, -8.0, 8.0, 24.0):
        b.box((x - 2.0, 0.6, 47.2), (x + 2.0, 1.6, 47.6), 'lightw', bevel=0.0)
    # rail bed the bay slides on (z -46..-18)
    b.box((-56.0, 0.0, -48.0), (47.0, 4.5, -16.0), 'paint2', bevel=0.3)
    for z in (-40.0, -24.0):
        b.box((-55.0, 4.4, z - 1.0), (46.0, 5.0, z + 1.0), 'steel', bevel=0.1)
    # tower block (right): hollow on its left (x=18) side, the bay cradle parks inside
    for lo, hi in (((47.0, 0.0, -48.5), (56.0, 31.0, -15.5)), ((18.0, 4.4, -48.5), (47.0, 31.0, -46.8)),
                   ((18.0, 4.4, -17.2), (47.0, 31.0, -15.5)), ((18.0, 29.4, -46.8), (47.0, 31.0, -17.2))):
        b.box(lo, hi, 'paint', bevel=0.35)
    b.box((19.0, 4.5, -46.7), (46.9, 4.8, -17.3), 'black', bevel=0.0)
    b.hull([(x, 30.9, z) for x, z in ((18.0, -48.5), (56.0, -48.5), (56.0, -15.5), (18.0, -15.5))]
           + [(x, 34.0, z) for x, z in ((21.0, -45.5), (53.0, -45.5), (53.0, -18.5), (21.0, -18.5))], 'paint',
           bevel=0.3)
    b.box((22.0, 33.9, -44.5), (52.0, 34.5, -19.5), 'team', bevel=0.12)
    b.box((24.0, 18.0, -15.6), (44.0, 19.4, -15.3), 'lightw', bevel=0.0)
    # control tower on the block
    b.hull([(x, 34.0, z) for x, z in ((30.0, -42.0), (48.0, -42.0), (48.0, -24.0), (30.0, -24.0))]
           + [(x, 58.0, z) for x, z in ((35.0, -37.0), (43.0, -37.0), (43.0, -29.0), (35.0, -29.0))], 'paint',
           bevel=0.35)
    b.hull([(x, 57.0, z) for x, z in ((33.0, -39.0), (45.0, -39.0), (45.0, -27.0), (33.0, -27.0))]
           + [(x, 66.0, z) for x, z in ((31.0, -41.0), (47.0, -41.0), (47.0, -25.0), (31.0, -25.0))], 'paint2',
           bevel=0.3)
    b.box((30.7, 61.0, -41.3), (47.3, 63.2, -24.7), 'lightw', bevel=0.1)
    b.hull([(x, 65.9, z) for x, z in ((31.0, -41.0), (47.0, -41.0), (47.0, -25.0), (31.0, -25.0))]
           + [(x, 70.0, z) for x, z in ((34.0, -38.0), (44.0, -38.0), (44.0, -28.0), (34.0, -28.0))], 'team',
           bevel=0.25)

    # ------------------------------------------------------------------ bay (origin 0, 0, -29): sliding drawer
    y = k.piece('bay')
    y.box((-33.0, 4.5, -46.0), (18.0, 22.0, -27.6), 'paint', bevel=0.4)                     # back housing
    y.box((-2.2, 4.5, -27.6), (18.0, 22.0, -6.4), 'paint', bevel=0.4)                       # right front block
    y.box((-22.4, 19.2, -27.6), (-2.2, 22.0, -6.4), 'paint', bevel=0.3)                     # roof over the slot
    y.box((-22.4, 4.5, -27.6), (-2.2, 5.8, -6.4), 'black', bevel=0.0)                       # slot floor
    y.box((-31.0, 21.9, -44.0), (16.0, 22.5, -29.6), 'hazard', bevel=0.1)                   # roof stripes
    y.box((0.0, 21.9, -25.6), (16.0, 22.5, -8.4), 'team', bevel=0.1)
    y.box((2.0, 13.0, -6.5), (16.0, 14.4, -6.2), 'lightw', bevel=0.0)
    # cradle: the right end that parks inside the tower block
    y.box((18.0, 4.5, -45.0), (45.4, 8.0, -18.0), 'dark', bevel=0.3)
    y.box((19.0, 7.9, -44.0), (44.4, 8.4, -40.0), 'hazard', bevel=0.05)
    y.box((19.0, 7.9, -22.0), (44.4, 8.4, -19.0), 'hazard', bevel=0.05)

    d1 = k.piece('door1')                                                                     # left front block
    d1.box((-32.6, 5.9, -27.4), (-22.5, 19.1, -6.4), 'paint', bevel=0.35)
    d1.box((-31.0, 18.9, -25.0), (-24.0, 19.4, -9.0), 'team', bevel=0.08)
    d2 = k.piece('door2')                                                                     # front door
    d2.box((-22.3, 5.9, -7.2), (-2.4, 19.1, -6.2), 'paint2', bevel=0.15)
    d2.box((-20.0, 7.0, -6.25), (-4.6, 8.0, -6.0), 'hazard', bevel=0.0)

    # radar mast + dish (spins)
    r = k.piece('radar'); R = r.at
    r.cyl(R(0, 12.0, 4.0), R(0, 24.0, 4.0), 1.1, 8, 'steel')
    r.hull([R(x, yy, z) for x, yy, z in [(-9.0, 22.0, 1.0), (9.0, 22.0, 1.0), (-9.0, 30.0, 0.0), (9.0, 30.0, 0.0),
                                         (-6.0, 22.5, 3.5), (6.0, 22.5, 3.5), (-6.0, 29.5, 2.6), (6.0, 29.5, 2.6)]],
           'dark', bevel=0.15)
    r.box(R(-1.0, 25.0, 3.0), R(1.0, 27.0, 5.0), 'lightr', bevel=0.0)

    # nano boom: narm1 (19.25, 12, -18.97) lies back along -z at rest, swings up 84 deg
    a = k.piece('narm1'); A = a.at
    a.cyl(A(-3.8, 0, 0), A(3.8, 0, 0), 2.2, 10, 'steel', rot=math.pi / 10)
    a.box(A(-2.0, -1.8, -15.0), A(2.0, 1.8, -0.5), 'dark', bevel=0.25)
    a.box(A(-1.8, 1.7, -14.0), A(1.8, 2.1, -1.5), 'hazard', bevel=0.05)
    n = k.piece('nano1'); N = n.at                                                           # head, emit1 at z +13.9
    n.box(N(-3.0, -2.4, -3.6), N(3.0, 2.4, 2.4), 'steel', bevel=0.35)
    n.cyl(N(0, 0, 2.2), N(0, 0, 12.6), 1.5, 10, 'dark', r2=1.1)
    n.cyl(N(0, 0, 12.5), N(0, 0, 13.9), 1.2, 10, 'lightc')
    # gripper arm: arm1b post (moves x), arm1 boom, claw jaws
    ab = k.piece('arm1b'); AB = ab.at
    ab.box(AB(-5.6, -11.4, -12.0), AB(-0.4, 1.6, 1.4), 'dark', bevel=0.3)
    ab.box(AB(-5.2, 1.5, -11.6), AB(-0.8, 1.9, 1.0), 'hazard', bevel=0.05)
    a1 = k.piece('arm1'); A1 = a1.at
    a1.box(A1(-9.8, -2.2, -10.4), A1(-0.4, 2.0, 1.0), 'paint2', bevel=0.25)
    for nm, y0, y1 in (('arm1top', -2.2, 0.0), ('arm1bot', 0.0, 2.2)):
        c = k.piece(nm); C = c.at
        c.box(C(-0.9, y0, 0.2), C(0.9, y1, 7.0), 'steel', bevel=0.12)
    # conduit
    p1 = k.piece('pow1'); P1 = p1.at
    p1.cyl(P1(-0.5, 0.0, 0), P1(-0.5, 8.4, 0), 1.3, 8, 'dark')
    p2 = k.piece('pow2'); P2 = p2.at
    p2.cyl(P2(-1.5, 0.0, 0.0), P2(-1.5, -6.6, -9.6), 1.1, 8, 'steel')
    p2.box(P2(-3.2, -1.2, -1.2), P2(0.2, 1.2, 1.2), 'dark', bevel=0.15)
    # platform + second nano head (slides out of the slot)
    pl = k.piece('plate'); PL = pl.at
    pl.box(PL(-19.6, -1.0, -1.8), PL(-0.4, 0.0, 20.8), 'paint2', bevel=0.15)
    pl.box(PL(-19.2, -0.05, 18.2), PL(-0.8, 0.2, 20.4), 'hazard', bevel=0.03)
    n2 = k.piece('nano2'); N2 = n2.at                                                        # emit2 at (0, 5.11, 13.9)
    n2.cyl(N2(0, 0.0, 0), N2(0, 3.4, 0), 3.6, 12, 'dark', rot=math.pi / 12)
    n2.box(N2(-2.8, 3.0, -3.0), N2(2.8, 7.4, 3.6), 'steel', bevel=0.35)
    n2.cyl(N2(0, 5.11, 3.4), N2(0, 5.11, 12.6), 1.4, 10, 'dark', r2=1.0)
    n2.cyl(N2(0, 5.11, 12.5), N2(0, 5.11, 13.9), 1.1, 10, 'lightc')

    # ------------------------------------------------------------------ pad: octagon base + chasing light frames
    pb = k.piece('padbase')
    pb.plan(DY - 0.1, 3.9, octagon(21.8, PZ), 'dark', bevel=0.15, top_inset=0.6)
    pb.plan(3.85, 4.0, octagon(18.4, PZ), 'steel', bevel=0.0)
    for j, nm in enumerate(('pad1', 'pad2', 'pad3')):
        pd = k.piece(nm)
        for i in range(j, 12, 3):
            t = 2 * math.pi * i / 12 + math.pi / 12
            cx, cz = 19.9 * math.cos(t), PZ + 19.9 * math.sin(t)
            pd.box((cx - 0.8, 3.7, cz - 0.8), (cx + 0.8, 4.05, cz + 0.8), 'lightw', bevel=0.0)
