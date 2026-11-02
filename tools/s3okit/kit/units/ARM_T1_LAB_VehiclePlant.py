"""Vehicle Plant (ARM_T1_LAB_VehiclePlant) - Arm T1 vehicle factory. Closed it is one tall light hall (two halves,
side1/side2, meeting at the centre seam) with cyan-lit walls, between a low back block and two front pylons. On
activation the halves fall outward ~89 deg on their outer floor hinges (turn z) and lie on their sides beside the
lane, so their seam faces become the tops: big team panels framed by hazard stripes; the work plates (plate1/2) slide
out of the seams and the nano heads (nano1/2) on their posts tip over to point at the pad.
Arm lab family: light chamfered blocks with team roof panels, dark lane floor with hazard edge strips, light round
build pad, cyan lights. Identity from above (open): a wide lane with a big light disc between two long hazard-framed
team slabs, a light back block and two front pylons (the kbot lab is a cross of four small blocks with tilted lids).
Pieces (COB): base, side1/side2 (turn z), plate1/2 (move x), post1/2, nano1/2 (turn z), beam1/2 (empty nano emit
points), door1/doo2 (seam plates, hidden between/inside the halves in both states: left empty), pad (spin y;
QueryBuildInfo). Side 2 is a mirror clone of side 1.
The halves hinge at x +-27.25 (script), so their hinge edges stand in the outer 4.75 elmo of the yardmap lane
(x +-32) when open, as in TA; nothing else is in the lane.
Preview: OPEN (activatescr end state; COB z turns and x moves negated for the engine frame).
Coordinates are ENGINE/global: X right, Y up, Z forward."""
import math

UNIT = dict(
    res=2048,
    hazard_period=5.0,
    always_visible=['side1', 'side2', 'plate1', 'plate2', 'post1', 'post2', 'nano1', 'nano2'],
    wreck=dict(seed=63, drop=['side2']),
    preview_pose={
        'side1': (0, 0, 88.99), 'side2': (0, 0, -88.99),
        'plate1': {'move': (16.25, 0, 0)}, 'plate2': {'move': (-14.625, 0, 0)},
        'nano1': (0, 0, -41.0), 'nano2': (0, 0, 37.0),
        'door1': {'move': (-17.75, 0, 0), 'rot': (0, 0, 90)}, 'doo2': {'move': (17.5, 0, 0), 'rot': (0, 0, -90)},
    },
)

LX = 27.2            # clear lane half-width (hinge line)


def build(k):
    # ------------------------------------------------------------------ base: lane floor, back block, front pylons
    b = k.piece('base')
    b.box((-LX, 0.0, -36.0), (LX, 0.3, 48.0), 'paint2', bevel=0.05)
    b.box((-LX, 0.0, -36.0), (-23.4, 0.42, 48.0), 'hazard', bevel=0.04, mirror=True)
    # back block (behind the hall)
    b.plan(0.0, 19.0, [(-47.0, -49.0), (47.0, -49.0), (47.0, -38.6), (-47.0, -38.6)], 'paint', bevel=0.4,
           top_inset=1.4)
    b.box((-40.0, 18.9, -47.4), (40.0, 19.5, -40.2), 'team', bevel=0.12)
    b.box((-30.0, 6.0, -38.75), (-10.0, 7.4, -38.45), 'lightc', bevel=0.0, mirror=True)
    b.box((-47.0, 0.0, -38.6), (-28.0, 3.0, -36.0), 'paint2', bevel=0.2, mirror=True)
    # front pylons: leaning light towers with team caps
    b.hull([(-49.0, 0.0, 34.0), (-37.0, 0.0, 34.0), (-49.0, 0.0, 47.0), (-37.0, 0.0, 47.0),
            (-46.5, 30.0, 39.0), (-40.5, 30.0, 39.0), (-46.5, 30.0, 44.0), (-40.5, 30.0, 44.0)], 'paint', bevel=0.35,
           mirror=True)
    b.box((-46.2, 29.9, 39.3), (-40.8, 30.5, 43.7), 'team', bevel=0.08, mirror=True)
    b.box((-44.5, 0.0, 33.0), (-41.5, 14.0, 34.6), 'paint2', bevel=0.15, mirror=True)
    b.box((-44.0, 22.0, 39.0 - 0.6), (-42.0, 25.0, 39.0 - 0.2), 'lightc', bevel=0.0, mirror=True)

    # ------------------------------------------------------------------ side1 (origin -27.25, 0.12, -6.25): hall half
    s = k.piece('side1'); S = s.at
    s.hull([S(x, y, z) for x, y, z in
            [(0.0, 0.3, -31.2), (0.0, 0.3, 31.2), (0.0, 25.0, -31.2), (0.0, 25.0, 31.2),
             (10.0, 37.2, -29.0), (10.0, 37.2, 29.0), (26.2, 37.2, -29.0), (26.2, 37.2, 29.0),
             (26.2, 0.3, -31.2), (26.2, 0.3, 31.2)]], 'paint', bevel=0.45)
    # (the floor edge starts 0.3 up: a face at y < 0.35 counts as a ground-contact underside and is culled, but it
    # is the lane-facing side of the half when it lies open)
    # outer wall: paint2 armour band with cyan slit lights
    s.box(S(-0.4, 4.0, -27.0), S(0.1, 14.0, 27.0), 'paint2', bevel=0.1)
    s.box(S(-0.55, 10.0, -20.0), S(-0.35, 11.2, 20.0), 'lightc', bevel=0.0)
    # roof ribs (closed: light ribs across the roof)
    for z in (-22.0, -8.0, 8.0, 22.0):
        s.hull([S(x, y, zz) for x, y in ((3.0, 30.0), (10.4, 37.3), (24.0, 37.3), (24.0, 37.6), (10.4, 37.6), (3.0, 30.3))
                for zz in (z - 1.2, z + 1.2)], 'paint2', bevel=0.1)
    # seam face (the TOP when open): light frame, hazard band, big team panel
    X0, X1 = 26.1, 27.35
    s.box(S(X0, 0.3, -29.0), S(X1, 3.0, 29.0), 'paint', bevel=0.1)
    s.box(S(X0, 3.0, -29.0), S(X1, 9.0, 29.0), 'hazard', bevel=0.1)
    s.box(S(X0, 31.0, -29.0), S(X1, 37.2, 29.0), 'hazard', bevel=0.1)
    s.box(S(X0, 9.0, -29.0), S(X1, 31.0, -21.0), 'hazard', bevel=0.1)
    s.box(S(X0, 9.0, 21.0), S(X1, 31.0, 29.0), 'hazard', bevel=0.1)
    s.box(S(X0, 9.0, -21.0), S(X1, 31.0, 21.0), 'team', bevel=0.1)
    k.clone('side2', 'side1', mirror_x=True)

    # ------------------------------------------------------------------ plate1 (origin -16, 9, -6.5): work plate
    p = k.piece('plate1'); P = p.at
    p.box(P(0.0, -8.3, -10.8), P(2.4, 8.3, 11.2), 'paint', bevel=0.25)
    p.box(P(2.2, -6.4, -8.8), P(2.75, 6.4, 9.2), 'paint2', bevel=0.08)
    k.clone('plate2', 'plate1', mirror_x=True)
    # post1 (origin -13.43, 9.45, -6.94)
    q = k.piece('post1'); Q = q.at
    q.box(Q(0.0, -1.9, -1.8), Q(5.6, 1.5, 1.8), 'dark', bevel=0.2)
    q.cyl(Q(0.4, -0.2, -2.6), Q(0.4, -0.2, 2.6), 1.6, 10, 'steel', rot=math.pi / 10)
    k.clone('post2', 'post1', mirror_x=True)
    # nano1 (origin -8.15, 8.92, -7.0): emitter head, beam1 at (3.53, -8.34, 0)
    n = k.piece('nano1'); N = n.at
    n.box(N(-0.7, -2.8, -3.0), N(4.6, 3.2, 3.0), 'steel', bevel=0.35)
    n.box(N(0.0, 3.0, -2.2), N(3.8, 3.6, 2.2), 'hazard', bevel=0.08)
    n.cyl(N(2.2, -2.0, 0.0), N(3.4, -7.0, 0.0), 1.6, 10, 'dark', r2=1.1)
    n.cyl(N(3.4, -6.9, 0.0), N(3.55, -8.2, 0.0), 1.15, 10, 'lightc')
    k.clone('nano2', 'nano1', mirror_x=True)

    # ------------------------------------------------------------------ pad (origin 0, 0.5, -10): spinning disc
    d = k.piece('pad'); D = d.at
    d.cyl(D(0, -0.2, 0), D(0, 0.35, 0), 24.4, 40, 'dark', bevel=0.12)
    d.cyl(D(0, 0.35, 0), D(0, 0.47, 0), 22.4, 40, 'paint')
    d.cyl(D(0, 0.45, 0), D(0, 0.55, 0), 4.0, 16, 'paint2')
