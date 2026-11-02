"""Hovercraft Platform (CORE_T1_LAB_HovercraftPlatform) - Core T1 hover factory. Two long dark sloped side plinths
with team decks and buttressed corner blocks flank a wide near-black lane (x +-32) carrying a light steel pad with
ochre fan vanes; mid-plinth stands a tall armoured lift tower on each side: its roof hatch (door1/door2) flips up on
the outer hinge and drops into the wall, the lift (platform1/platform2) rises 18.75 to the roof and the nano head
on it swings 90 deg to aim across the pad.
Core lab family: dark warm armour, corner blocks/pylons with team caps, near-black lane with ochre hazard edges,
light steel pad, warm lights. Identity from above: two long dark plinths with team decks and a tower in the middle of
each, a wide light disc with fan vanes between (the Arm hover platform is two light capsules with team roofs).
Pieces (COB): base, platform1/2 (move y), nano1/2 (turn y), beam1/2 (empty nano emit points), door1/2 (turn z,
move y), pad (spin y; QueryBuildInfo).
Preview: OPEN (activatescr end state; COB z turns negated for the engine frame).
Coordinates are ENGINE/global: X right, Y up, Z forward."""
import math

UNIT = dict(
    res=2048,
    hazard_period=5.0,
    always_visible=['platform1', 'platform2', 'nano1', 'nano2'],
    wreck=dict(seed=70, drop=['door1']),
    preview_pose={
        'door1': {'move': (0, -11.25, 0), 'rot': (0, 0, 89.99)},
        'door2': {'move': (0, -11.25, 0), 'rot': (0, 0, -89.99)},
        'platform1': {'move': (0, 18.75, 0)}, 'platform2': {'move': (0, 18.75, 0)},
        'nano1': (0, -89.99, 0), 'nano2': (0, -89.99, 0),
    },
)

TY = 22.2            # tower roof
TX0, TX1 = -59.0, -42.0   # tower x (outer, inner), -x side
TZ = 13.0            # tower half length


def build(k):
    b = k.piece('base')
    # ------------------------------------------------------------------ lane
    b.box((-34.0, 0.0, -55.0), (34.0, 0.4, 55.0), 'paint2', bevel=0.08)
    b.box((-34.0, 0.0, -55.0), (-30.0, 0.55, 55.0), 'hazard', bevel=0.04, mirror=True)
    for x in (-20.0, -7.0, 7.0, 20.0):
        b.box((x - 1.6, 0.3, 54.6), (x + 1.6, 0.9, 55.0), 'lightw', bevel=0.0)
    # ------------------------------------------------------------------ side plinths (-x, mirrored)
    b.plan(0.0, 8.0, [(-61.0, -52.0), (-36.0, -52.0), (-36.0, 52.0), (-61.0, 52.0)], 'paint', bevel=0.35,
           top_inset=2.4, mirror=True)
    for z0, z1 in ((-44.0, -TZ - 1.0), (TZ + 1.0, 44.0)):
        b.box((-57.0, 7.95, z0), (-40.0, 8.4, z1), 'team', bevel=0.1, mirror=True)
    # corner blocks with buttresses
    for zs in (1, -1):
        zc = 49.0 * zs
        z0, z1 = sorted((zc - 6.0, zc + 6.0))
        b.plan(0.0, 14.0, [(-61.0, z0), (-47.0, z0), (-47.0, z1), (-61.0, z1)], 'paint', bevel=0.35, top_inset=1.8,
               mirror=True)
        b.box((-58.8, 13.9, z0 + 2.0), (-49.2, 14.4, z1 - 2.0), 'team', bevel=0.08, mirror=True)
        b.hull([(-47.0, 0.0, z0), (-47.0, 0.0, z1), (-47.0, 10.0, z0), (-47.0, 10.0, z1), (-38.0, 0.0, z0 + 2.0),
                (-38.0, 0.0, z1 - 2.0)], 'paint2', bevel=0.2, mirror=True)
    # lift towers (hollow well x -56.5..-45, z -9.8..8.8)
    for lo, hi in (((TX0, 0.0, -TZ), (-56.6, TY, TZ)), ((-44.9, 0.0, -TZ), (TX1, TY, TZ)),
                   ((-56.6, 0.0, -TZ), (-44.9, TY, -9.9)), ((-56.6, 0.0, 8.9), (-44.9, TY, TZ))):
        b.box(lo, hi, 'paint', bevel=0.35, mirror=True)
    b.box((-56.6, 0.0, -9.9), (-44.9, 3.3, 8.9), 'black', bevel=0.0, mirror=True)
    b.hull([(x, 0.0, z) for x in (TX1, -38.0) for z in (-TZ, TZ)] + [(TX1, 16.0, -TZ + 2.0), (TX1, 16.0, TZ - 2.0)],
           'paint2', bevel=0.3, mirror=True)                                               # lane-side buttress
    for lo, hi in (((TX0 + 0.4, TY - 0.05, -TZ + 0.4), (-56.6, TY + 0.4, TZ - 0.4)),
                   ((-44.9, TY - 0.05, -TZ + 0.4), (TX1 - 0.4, TY + 0.4, TZ - 0.4))):
        b.box(lo, hi, 'hazard', bevel=0.05, mirror=True)
    b.box((-42.1, 18.0, -8.0), (-41.8, 19.4, 8.0), 'lightw', bevel=0.0, mirror=True)

    # ------------------------------------------------------------------ hatch (door1 origin -56.54, 22.17, 0)
    d = k.piece('door1'); D = d.at
    d.box(D(0.1, -0.5, -9.7), D(11.4, 0.4, 8.8), 'paint2', bevel=0.2)
    d.box(D(1.4, 0.35, -8.2), D(10.2, 0.6, 7.3), 'team', bevel=0.06)
    k.clone('door2', 'door1', mirror_x=True)
    # lift (platform1 origin -50.5, 3.5, 0): column + deck, the nano head on top
    p = k.piece('platform1'); P = p.at
    p.box(P(-5.8, 0.0, -9.6), P(5.4, 0.6, 8.6), 'paint2', bevel=0.15)
    p.box(P(-4.0, 0.0, -6.0), P(4.0, 10.2, 6.0), 'dark', bevel=0.3)
    p.box(P(-5.6, 0.55, -9.4), P(5.2, 0.8, -7.4), 'hazard', bevel=0.03)
    p.box(P(-5.6, 0.55, 6.4), P(5.2, 0.8, 8.4), 'hazard', bevel=0.03)
    p.box(P(-3.6, 10.1, -5.6), P(3.6, 10.6, 5.6), 'hazard', bevel=0.05)
    k.clone('platform2', 'platform1', mirror_x=True)
    n = k.piece('nano1'); N = n.at                                       # head; beam1 at (0, -0.25, -12.75)
    n.box(N(-3.2, -1.0, -3.0), N(3.2, 2.6, 5.2), 'steel', bevel=0.3)
    n.cyl(N(0, -0.25, -2.8), N(0, -0.25, -11.4), 1.5, 10, 'dark', r2=1.1)
    n.cyl(N(0, -0.25, -11.3), N(0, -0.25, -12.75), 1.15, 10, 'lightc')
    m = k.piece('nano2'); M = m.at                                       # beam2 at (0, -0.25, +12.75)
    m.box(M(-3.2, -1.0, -5.2), M(3.2, 2.6, 3.0), 'steel', bevel=0.3)
    m.cyl(M(0, -0.25, 2.8), M(0, -0.25, 11.4), 1.5, 10, 'dark', r2=1.1)
    m.cyl(M(0, -0.25, 11.3), M(0, -0.25, 12.75), 1.15, 10, 'lightc')

    # ------------------------------------------------------------------ pad (origin 0, 2.5, 0): steel disc, fan vanes
    pd = k.piece('pad'); Pd = pd.at
    pd.cyl(Pd(0, -2.2, 0), Pd(0, -1.6, 0), 30.4, 40, 'dark', bevel=0.12)
    pd.cyl(Pd(0, -1.6, 0), Pd(0, -1.48, 0), 28.0, 40, 'steel')
    for a in range(6):
        t = a * math.pi / 3
        pd.hull([Pd(r * math.cos(t + dt), yy, r * math.sin(t + dt)) for r, dt in ((6.0, -0.22), (6.0, 0.22),
                 (24.0, 0.04), (24.0, 0.30)) for yy in (-1.55, -1.4)], 'hazard', bevel=0.0)
    pd.cyl(Pd(0, -1.5, 0), Pd(0, -1.35, 0), 5.0, 16, 'dark')
