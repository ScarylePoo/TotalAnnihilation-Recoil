"""Metal Maker (CORE_T1_ECO_MetalMaker) - Core metal maker. A squat dark trapezoidal block with a sunken well; in the
well sits the 'plug', a stepped octagonal converter crowned by a glowing orange crystal under a light steel arch.
Switched off, the plug flips 180 deg about z and buries itself in the block (the default pose is the working one).
Identity from above: dark rectangle with two team side rails, a light steel arch over a bright warm crystal, a
paint2 machinery block at the front (the Arm maker is a six-spoke star round a cyan sphere).
Pieces (COB): base, plug (turn z: 0 on, 180 off; origin 0, 11.92, 4.9), glow (child of plug, the crystal).
Coordinates are ENGINE/global: X right, Y up, Z forward."""
import math

UNIT = dict(
    wreck=dict(seed=22, pose={'plug': (0, 0, 35)}),
    preview_pose={},
)

RX, RZ = -2.5, -3.4          # converter centre (global x, z)


def build(k):
    b = k.piece('base')
    b.plan(0.0, 11.2, [(-23.0, -17.6), (23.0, -17.6), (23.0, 17.6), (-23.0, 17.6)], 'paint', bevel=0.35, top_inset=3.0)
    # rim walls round the well (sides mirrored), back wall, front machinery block
    b.hull([(x, y, z) for x in (-20.0, -13.8) for y in (11.1, 14.4) for z in (-14.6, 14.6)], 'paint', bevel=0.3,
           mirror=True)
    b.box((-19.4, 14.35, -13.4), (-14.4, 14.7, 13.4), 'team', bevel=0.0, mirror=True)
    b.box((-13.8, 11.1, -14.6), (13.8, 13.0, -12.8), 'paint', bevel=0.2)
    b.hull([(x, y, z) for x in (-13.8, 13.8) for (y, z) in ((11.1, 6.6), (11.1, 14.6), (17.6, 14.6), (17.6, 8.6))],
           'paint2', bevel=0.3)
    for x0 in (-10.0, -4.0, 2.0, 8.0):
        b.box((x0, 12.0, 14.55), (x0 + 3.4, 16.4, 14.9), 'black', bevel=0.0)
    b.box((-12.0, 17.55, 9.4), (12.0, 17.9, 11.0), 'hazard', bevel=0.0)
    b.box((-13.8, 11.0, -12.8), (13.8, 11.4, 6.6), 'black', bevel=0.0)                  # well floor
    for sx in (-1, 1):                                                                  # side vents low down
        b.hull([(sx * (23.0 - (y - 0.0) / 11.2 * 3.0 * 23.0 / math.hypot(23.0, 17.6) + d), y, z) for y in (3.0, 8.0) for z in (-8.0, 8.0)
                for d in (0.05, 0.35)], 'dark', bevel=0.0)
    b.box((-1.2, 1.0, 17.55), (1.2, 2.4, 17.85), 'lightr', bevel=0.0)

    # ------------------------------------------------------------------ plug: stepped octagonal converter + arch
    p = k.piece('plug')
    y0 = k.P['plug'][1]
    p.box((-12.8, y0 - 0.2, -12.4), (12.8, y0 + 1.4, 4.6), 'dark', bevel=0.15)
    oc = lambda r: [(RX + r * math.cos(math.pi / 8 + i * math.pi / 4), RZ + r * math.sin(math.pi / 8 + i * math.pi / 4))
                    for i in range(8)]
    p.plan(y0 + 1.3, y0 + 4.0, oc(8.6), 'paint', bevel=0.25, top_inset=1.0)
    p.plan(y0 + 3.9, y0 + 6.0, oc(6.6), 'paint2', bevel=0.2, top_inset=0.6)
    p.cyl((RX, y0 + 5.9, RZ), (RX, y0 + 6.5, RZ), 4.2, 8, 'team', rot=math.pi / 8)
    # steel arch over the crystal
    for x in (RX - 7.6, RX + 6.0):
        p.box((x, y0 + 1.3, RZ - 1.6), (x + 1.6, y0 + 11.6, RZ + 1.6), 'steel', bevel=0.2)
    p.box((RX - 7.6, y0 + 10.4, RZ - 1.8), (RX + 7.6, y0 + 12.6, RZ + 1.8), 'steel', bevel=0.25)
    p.box((RX - 1.0, y0 + 9.4, RZ - 1.0), (RX + 1.0, y0 + 10.5, RZ + 1.0), 'dark', bevel=0.05)
    # cable boxes on the deck
    p.box((5.6, y0 + 1.3, -11.6), (11.8, y0 + 4.2, -6.0), 'paint2', bevel=0.2)
    p.box((5.6, y0 + 1.3, -1.4), (11.8, y0 + 3.4, 3.8), 'paint2', bevel=0.2)

    # ------------------------------------------------------------------ glow: the crystal
    g = k.piece('glow')
    yc = y0 + 7.6
    ring = [(RX + 2.6 * math.cos(i * math.pi / 3), yc, RZ + 2.6 * math.sin(i * math.pi / 3)) for i in range(6)]
    g.hull(ring + [(RX, y0 + 6.2, RZ), (RX, y0 + 9.2, RZ)], 'lightc', bevel=0.0)
