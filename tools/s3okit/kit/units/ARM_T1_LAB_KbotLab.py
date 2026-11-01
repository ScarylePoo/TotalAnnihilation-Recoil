"""Kbot Lab (ARM_T1_LAB_KbotLab) - Arm T1 kbot factory. TA's cross plan kept: a dark build lane (x +-16, the yardmap's
`c` columns) runs front to back between two low light side decks; four light door blocks with team roofs close over
the lane (door1..4 + their roof slabs door1a..4a) and, on activation, the slabs slide outward into the blocks and the
blocks slide sideways off the lane; two big hazard-striped hatch lids (nano1/nano2) lying over pits beside the lane
flip up ~66 deg on hinged lift rails (stand1/stand2) and point their emitter spikes (beam1/beam2) at the pad.
Arm lab family: light chamfered blocks with team roof panels, dark lane floor with hazard edge strips, light round
build pad, cyan lights. Identity from above (open): a dark lane with a light disc, four team-roofed blocks at the
corners, two yellow-black lids standing up at the sides (the vehicle plant is a long single hall, the aircraft plant
a broad open deck).
Pieces (COB): base, stand1/2 (turn z), nano1/2 (turn z), beam1/2 (empty nano emit points), door1..4 (move x),
door1a..4a (move z), pad (spin y; QueryBuildInfo). Preview: OPEN (activatescr end state; COB z turns and x moves
negated for the engine frame). Lane cells must stay clear above the floor in the open state.
Coordinates are ENGINE/global: X right, Y up, Z forward."""
import math

UNIT = dict(
    res=2048,
    hazard_period=5.0,
    always_visible=['nano1', 'nano2', 'stand1', 'stand2'],
    wreck=dict(seed=61, drop=['nano2']),
    preview_pose={
        'door1a': {'move': (0, 0, 24.75)}, 'door2a': {'move': (0, 0, 25.0)},
        'door3a': {'move': (0, 0, -23.75)}, 'door4a': {'move': (0, 0, -24.0)},
        'door1': {'move': (-23.75, 0, 0)}, 'door2': {'move': (26.25, 0, 0)},
        'door3': {'move': (-23.75, 0, 0)}, 'door4': {'move': (26.25, 0, 0)},
        'stand1': (0, 0, -35.1), 'stand2': (0, 0, 35.54),
        'nano1': (0, 0, 100.8), 'nano2': (0, 0, -102.15),
    },
)

LANE = 16.0          # lane half-width (yardmap c columns)
ZE = 47.5            # deck half-length


def build(k):
    # ------------------------------------------------------------------ base: lane floor, side decks, pits, buttresses
    b = k.piece('base')
    b.box((-LANE, 0.0, -ZE), (LANE, 0.3, ZE), 'paint2', bevel=0.05)                      # lane floor (flat)
    b.box((-LANE, 0.0, -ZE), (-12.6, 0.42, ZE), 'hazard', bevel=0.04, mirror=True)       # lane edge strips
    for z0, z1 in ((15.6, ZE), (-ZE, -16.6)):                                            # side decks front / back
        b.plan(0.0, 1.8, [(-47.0, z0), (-16.4, z0), (-16.4, z1), (-47.0, z1)], 'paint', bevel=0.2, top_inset=0.6,
               mirror=True)
    # nano pits (under the lids) with a dark coaming and a team outer lip
    b.box((-46.6, 0.0, -16.6), (-16.4, 0.25, 15.6), 'black', bevel=0.0, mirror=True)
    b.box((-47.4, 0.0, -16.6), (-44.6, 2.4, 15.6), 'team', bevel=0.15, mirror=True)
    b.box((-18.2, 0.0, -16.6), (-16.4, 1.2, 15.6), 'dark', bevel=0.1, mirror=True)
    # corner buttresses (TA wedges), sloping away from the pits, flat team crest
    for zs in (1, -1):
        prof = [(15.8 * zs, 0.0), (15.8 * zs, 11.3), (19.6 * zs, 11.3), (25.4 * zs, 1.6), (25.4 * zs, 0.0)]
        b.prism(-34.0, -17.0, prof, 'paint', bevel=0.25, mirror=True)
        zlo, zhi = sorted((15.6 * zs, 19.8 * zs))
        b.box((-33.4, 11.0, zlo), (-17.6, 11.6, zhi), 'team', bevel=0.08, mirror=True)
        zlo, zhi = sorted((15.5 * zs, 15.8 * zs))
        b.box((-31.0, 4.0, zlo), (-20.0, 5.0, zhi), 'lightc', bevel=0.0, mirror=True)
    # hinge blocks the stands pivot on
    for z0, z1 in ((-16.0, -7.0), (6.0, 15.0)):
        b.box((-31.0, 0.0, z0), (-24.0, 2.6, z1), 'dark', bevel=0.15, mirror=True)

    # ------------------------------------------------------------------ stands: lift rails (origin -27.5, 0, 0)
    s = k.piece('stand1'); S = s.at
    for z0, z1 in ((-15.6, -7.2), (6.2, 14.6)):
        s.hull([S(x, y, z) for x, y in ((-18.4, 0.6), (-15.7, 4.0), (4.4, 3.4), (2.0, 0.6)) for z in (z0, z1)],
               'paint2', bevel=0.2)
        s.box(S(-17.0, 3.5, z0 + 1.6), S(2.0, 3.9, z1 - 1.6), 'hazard', bevel=0.05)
    s.cyl(S(0.0, 1.4, -16.0), S(0.0, 1.4, 15.0), 1.3, 10, 'steel', rot=math.pi / 10)
    k.clone('stand2', 'stand1', mirror_x=True)

    # ------------------------------------------------------------------ nano lids (origin -43.24, 4.0, 0)
    n = k.piece('nano1'); N = n.at
    n.box(N(-3.0, -0.2, -15.8), N(28.0, 2.4, 14.6), 'paint2', bevel=0.3)                 # lid body
    n.box(N(-2.2, 2.3, -15.0), N(27.2, 3.4, 13.8), 'hazard', bevel=0.25)                # striped top
    # emitter housing on the lid (dark ridge with a team cap) - stands up toward the pad when open
    n.hull([N(x, y, z) for x, y, z in
            [(-2.0, 3.3, -6.0), (20.0, 3.3, -4.0), (-2.0, 3.3, 5.0), (20.0, 3.3, 3.0),
             (-2.0, 8.6, -3.6), (16.0, 8.6, -2.6), (-2.0, 8.6, 2.6), (16.0, 8.6, 1.6)]], 'dark', bevel=0.3)
    n.box(N(0.0, 8.5, -2.6), N(14.0, 9.1, 1.6), 'paint', bevel=0.12)
    # emitter spike under the lid down to beam1 (10.04, -13.21, -1.0)
    n.hull([N(x, y, z) for x, y, z in
            [(6.0, -0.2, -4.0), (16.0, -0.2, -4.0), (6.0, -0.2, 2.0), (16.0, -0.2, 2.0),
             (8.6, -11.0, -2.6), (12.0, -11.0, -2.6), (8.6, -11.0, 0.6), (12.0, -11.0, 0.6)]], 'dark', bevel=0.2)
    n.cyl(N(10.3, -10.8, -1.0), N(10.1, -13.3, -1.0), 1.5, 10, 'lightc', r2=0.9)
    for z in (-11.0, 9.8):
        n.cyl(N(4.0, -0.2, z), N(9.4, -8.0, -1.0), 0.7, 8, 'steel')
    k.clone('nano2', 'nano1', mirror_x=True)

    # ------------------------------------------------------------------ door blocks (door1 origin -15, 0, 37.5)
    d = k.piece('door1'); D = d.at
    d.box(D(0.0, 0.0, -12.5), D(15.6, 10.8, 12.5), 'paint', bevel=0.35)
    d.box(D(1.2, 10.6, -11.2), D(14.4, 11.3, 11.2), 'team', bevel=0.15)
    d.box(D(-0.2, 2.0, -8.0), D(0.1, 7.0, 8.0), 'paint2', bevel=0.05)                   # outer vent panel
    d.box(D(4.0, 6.5, 12.45), D(11.6, 7.6, 12.7), 'lightc', bevel=0.0)
    k.clone('door2', 'door1', mirror_x=True)
    k.clone('door3', 'door1')
    k.clone('door4', 'door1', mirror_x=True)

    # roof slabs (closed: the lane roof; open: hidden inside the blocks)
    a = k.piece('door1A'); A = a.at
    a.box(A(-7.3, 8.8, -23.5), A(7.3, 10.2, 0.0), 'paint', bevel=0.2)
    a.box(A(-5.6, 10.1, -22.0), A(5.6, 10.4, -1.5), 'paint2', bevel=0.05)
    k.clone('door2A', 'door1A', mirror_x=True)
    c = k.piece('door3A'); C = c.at
    c.box(C(-7.3, 8.8, 0.0), C(7.3, 10.2, 23.0), 'paint', bevel=0.2)
    c.box(C(-5.6, 10.1, 1.5), C(5.6, 10.4, 21.5), 'paint2', bevel=0.05)
    k.clone('door4A', 'door3A', mirror_x=True)

    # ------------------------------------------------------------------ pad: spinning build disc (origin 0.5, 0.4, -3.5)
    p = k.piece('pad'); Pp = p.at
    p.cyl(Pp(0, 0.0, 0), Pp(0, 0.5, 0), 15.4, 32, 'dark', bevel=0.12)
    p.cyl(Pp(0, 0.5, 0), Pp(0, 0.62, 0), 13.6, 32, 'paint')
    p.cyl(Pp(0, 0.6, 0), Pp(0, 0.7, 0), 3.0, 16, 'paint2')
