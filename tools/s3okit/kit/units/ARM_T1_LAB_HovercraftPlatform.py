"""Hovercraft Platform (ARM_T1_LAB_HovercraftPlatform) - Arm T1 hover factory. Two long light side halls with rounded
ends and team roofs flank a wide dark deck (the yardmap lane, x +-32) carrying a big light pad; in the middle of each
hall a bay hatch (door1/door2) flips up on its outer hinge and slides down into the wall, the lift (plate1/plate2)
rises flush with the roof and the nano head (post/nano) swings 90 deg to aim across the pad.
Arm lab family: light chamfered blocks with team roof panels, dark lane with hazard edges, light round pad, cyan
lights. Identity from above: two long team-roofed capsules either side of the widest disc of the Arm labs, a hazard
square in the middle of each hall (the vehicle plant's halves lie as two hazard-framed slabs, the kbot lab is a cross).
Pieces (COB): base, plate1/2 (move y), post1/2, nano1/2 (turn y), beam1/2 (empty nano emit points), door1/2 (turn z,
move y), pad (spin y; QueryBuildInfo).
Preview: OPEN (activatescr end state; COB z turns and x moves negated for the engine frame).
Coordinates are ENGINE/global: X right, Y up, Z forward."""
import math

UNIT = dict(
    res=2048,
    hazard_period=5.0,
    always_visible=['plate1', 'plate2', 'post1', 'post2', 'nano1', 'nano2'],
    wreck=dict(seed=69, drop=['door2']),
    preview_pose={
        'door1': {'move': (0, -13.125, 0), 'rot': (0, 0, 89.99)},
        'door2': {'move': (0, -14.625, 0), 'rot': (0, 0, -89.99)},
        'plate1': {'move': (0, 10.125, 0)}, 'plate2': {'move': (0, 10.375, 0)},
        'nano1': (0, 89.99, 0), 'nano2': (0, -89.99, 0),
    },
)

H = 14.4             # hall roof
BZ0, BZ1 = -12.6, 16.2   # bay z range
XO, XI = -51.4, -38.2    # bay x range (outer, inner), -x side


def build(k):
    b = k.piece('base')
    # ------------------------------------------------------------------ deck + lane
    b.box((-34.0, 0.0, -55.0), (34.0, 0.4, 55.0), 'paint2', bevel=0.08)
    b.box((-34.0, 0.0, -55.0), (-30.4, 0.55, 55.0), 'hazard', bevel=0.04, mirror=True)
    for z in (-50.0, 50.0):                                                   # front/back sills with lights
        b.box((-30.0, 0.3, z - 1.0), (30.0, 0.55, z + 1.0), 'paint', bevel=0.1)
    for x in (-22.0, -11.0, 0.0, 11.0, 22.0):
        b.box((x - 1.2, 0.6, 50.8), (x + 1.2, 1.0, 51.1), 'lightc', bevel=0.0)
    # ------------------------------------------------------------------ side halls (built on -x, mirrored)
    for z0, z1 in ((-44.0, BZ0), (BZ1, 44.0)):
        b.plan(0.0, H, [(-60.0, z0), (-36.0, z0), (-36.0, z1), (-60.0, z1)], 'paint', bevel=0.4, top_inset=1.2,
               mirror=True)
        za, zb = (z0 + 10.0, z1 - 2.4) if z0 < 0 else (z0 + 2.4, z1 - 10.0)
        b.box((-57.6, H - 0.05, za), (-38.4, H + 0.35, zb), 'team', bevel=0.12, mirror=True)
    for zc in (-44.0, 44.0):                                                  # rounded hall ends
        b.cyl((-48.0, 0.0, zc), (-48.0, H - 0.3, zc), 11.6, 20, 'paint', rot=math.pi / 20, bevel=0.35, mirror=True)
        b.cyl((-48.0, H - 0.35, zc), (-48.0, H + 0.08, zc), 9.2, 20, 'team', rot=math.pi / 20, mirror=True)
        b.cyl((-48.0, H - 0.05, zc), (-48.0, H + 1.3, zc), 3.0, 12, 'dark', rot=math.pi / 12, mirror=True)
    for zc in (-55.5, 55.5):                                                  # end lights
        b.box((-50.0, 6.0, zc - 0.2), (-46.0, 7.2, zc + 0.2), 'lightc', bevel=0.0, mirror=True)
    # bay walls round the lift well, dark skirt along the lane side
    b.box((-60.0, 0.0, BZ0), (XO, H, BZ1), 'paint', bevel=0.35, mirror=True)
    b.box((XI, 0.0, BZ0), (-36.0, H, BZ1), 'paint', bevel=0.3, mirror=True)
    b.box((-59.2, H - 0.05, BZ0 + 0.6), (XO - 0.6, H + 0.35, BZ1 - 0.6), 'hazard', bevel=0.08, mirror=True)
    b.box((XO, 0.0, BZ0), (XI, 3.9, BZ1), 'black', bevel=0.0, mirror=True)                       # well floor
    b.box((-36.4, 2.0, -44.0), (-35.6, 9.0, 44.0), 'paint2', bevel=0.1, mirror=True)              # lane-side skirt
    b.box((-35.75, 10.0, -30.0), (-35.5, 11.0, 30.0), 'lightc', bevel=0.0, mirror=True)

    # ------------------------------------------------------------------ hatch (door1 origin -51.31, 14.37, -0.04)
    d = k.piece('door1'); D = d.at
    d.box(D(0.1, -0.45, -12.3), D(12.9, 0.35, 15.9), 'paint', bevel=0.2)
    d.box(D(1.6, 0.3, -10.6), D(11.4, 0.55, 14.2), 'paint2', bevel=0.06)
    k.clone('door2', 'door1', mirror_x=True)
    # lift + nano head (plate1 origin -45.3, 4.35, -0.04)
    p = k.piece('plate1'); P = p.at
    p.box(P(-5.8, -0.6, -12.2), P(6.8, 0.0, 15.8), 'paint2', bevel=0.15)
    for lo, hi in (((-5.6, -0.05, -12.0), (6.6, 0.2, -9.6)), ((-5.6, -0.05, 13.4), (6.6, 0.2, 15.6))):
        p.box(P(*lo), P(*hi), 'hazard', bevel=0.03)
    k.clone('plate2', 'plate1', mirror_x=True)
    q = k.piece('post1'); Q = q.at
    q.cyl(Q(0, 0.0, -3.0), Q(0, 3.2, -3.0), 2.6, 12, 'dark', rot=math.pi / 12)
    q.box(Q(-1.5, 0.0, -8.0), Q(1.5, 3.4, -0.4), 'steel', bevel=0.2)
    k.clone('post2', 'post1', mirror_x=True)
    n = k.piece('nano1'); N = n.at                                            # arm along +z to beam1 (0, 4.27, 10.59)
    n.box(N(-2.6, -1.8, -2.6), N(2.6, 3.6, 2.6), 'steel', bevel=0.3)
    n.hull([N(x, y, z) for x, y, z in [(-1.8, 0.0, 1.0), (1.8, 0.0, 1.0), (-1.8, 3.4, 1.0), (1.8, 3.4, 1.0),
                                       (-1.2, 3.2, 9.0), (1.2, 3.2, 9.0), (-1.2, 5.2, 9.0), (1.2, 5.2, 9.0)]], 'dark',
           bevel=0.2)
    n.box(N(-1.4, 3.4, 1.2), N(1.4, 3.9, 7.6), 'hazard', bevel=0.05)
    n.cyl(N(0, 4.27, 8.8), N(0, 4.27, 10.6), 1.2, 10, 'lightc')
    k.clone('nano2', 'nano1', mirror_x=True)

    # ------------------------------------------------------------------ pad (origin -1.12, 0.64, -1.92): spinning disc
    pd = k.piece('pad'); Pd = pd.at
    pd.cyl(Pd(0, -0.3, 0), Pd(0, 0.25, 0), 30.4, 44, 'dark', bevel=0.12)
    pd.cyl(Pd(0, 0.25, 0), Pd(0, 0.37, 0), 28.2, 44, 'paint')
    for a in range(6):                                          # fan-blade marks: the hover lab's pad
        t = a * math.pi / 3
        pd.hull([Pd(r * math.cos(t + dt), yy, r * math.sin(t + dt)) for r, dt in ((6.0, -0.25), (6.0, 0.25),
                 (22.0, 0.05), (22.0, 0.32)) for yy in (0.3, 0.45)], 'paint2', bevel=0.0)
    pd.cyl(Pd(0, 0.35, 0), Pd(0, 0.5, 0), 5.0, 16, 'paint2')
