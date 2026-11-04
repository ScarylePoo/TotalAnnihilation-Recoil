"""Seaplane Platform (ARM_T1_LAB_SeaplanePlatform) - Arm T1 seaplane factory. Waterline 53: the water surface is model
y = 53, so at rest the whole factory lies submerged - an octagonal light tower (`platform`) standing in a sunk
octagonal well, braced to four corner pontoon pods in the yardmap's `w` ring. On activation the tower surfaces
(+29.1) until its flight deck is 9.5 above the water: a dark octagonal deck with team corner panels round a light
pad, and in its two side bays the hatches (door1/door2) flip up and drop into the bay walls while the lift columns
(plate1/plate2) climb 25 above the deck as two nano towers whose heads (nano1/nano2) rise again and bend over the pad.
Arm lab family: light chamfered blocks, team panels, dark deck/lane, light round pad, hazard on the builder parts,
cyan lights. Identity from above (open): a light octagon in open water with a big disc and two hazard-capped towers
on its flanks (the Core seaplane platform is a dark cross-shaped block).
Pieces (COB): base (submerged frame), platform (move y), plate1/2 (move y), nano1/2 (move y, turn z), beam1/2 (empty
nano emit points), door1/2 (turn z, move y), pad (spin y; QueryBuildInfo).
Preview: OPEN (activatescr end state; COB z turns negated for the engine frame).
Coordinates are ENGINE/global: X right, Y up, Z forward."""
import math

UNIT = dict(
    res=2048,
    hazard_period=5.0,
    ground=False, water=53.0,
    water_lift={'platform': 29.125},
    always_visible=['plate1', 'plate2', 'nano1', 'nano2'],
    wreck=dict(seed=71, drop=['plate2']),
    preview_pose={
        'platform': {'move': (0, 29.125, 0)},
        'door1': {'move': (0, -18.5, 0), 'rot': (0, 0, 90.0)},
        'door2': {'move': (0, -18.25, 0), 'rot': (0, 0, -90.0)},
        'plate1': {'move': (0, 25.0, 0)}, 'plate2': {'move': (0, 25.0, 0)},
        'nano1': {'move': (0, 14.0, 0), 'rot': (0, 0, 115.34)},
        'nano2': {'move': (0, 14.0, 0), 'rot': (0, 0, -115.34)},
    },
)

PX, PZ = 1.25, -2.5  # platform origin x/z
TOP = 33.12          # deck height (platform-local)
R = 31.0             # tower octagon radius (to the corners)


def octagon(r, cx=0.0, cz=0.0):
    return [(cx + r * math.cos(math.pi / 8 + i * math.pi / 4), cz + r * math.sin(math.pi / 8 + i * math.pi / 4))
            for i in range(8)]


def build(k):
    # ------------------------------------------------------------------ base: submerged well, pods, braces
    b = k.piece('base')
    ring_o, ring_i = octagon(40.0), octagon(35.0)
    ring_t = octagon(R - 1.0, PX, PZ)
    for i in range(8):                                                     # well wall: eight segments
        pts = [ring_o[i], ring_o[(i + 1) % 8], ring_i[i], ring_i[(i + 1) % 8]]
        b.hull([(x, y, z) for x, z in pts for y in (0.0, 30.0)], 'paint2', bevel=0.25)
        b.hull([(x, y, z) for x, z in pts for y in (29.9, 30.4)], 'team' if i % 2 == 0 else 'hazard', bevel=0.05)
        # lip closing the well round the tower, so the raised tower still bears on it
        lip = [ring_i[i], ring_i[(i + 1) % 8], ring_t[i], ring_t[(i + 1) % 8]]
        b.hull([(x, y, z) for x, z in lip for y in (29.5, 30.3)], 'paint2', bevel=0.05)
    for sx in (-1, 1):
        for sz in (-1, 1):
            cx, cz = sx * 47.0, sz * 47.0
            b.cyl((cx, 0.0, cz), (cx, 43.0, cz), 8.4, 8, 'paint', rot=math.pi / 8, bevel=0.3)
            b.cyl((cx, 42.9, cz), (cx, 43.4, cz), 6.8, 8, 'team', rot=math.pi / 8)
            ex, ez = -sz * 1.6, sx * 1.6                                   # brace arm from the pod to the well
            b.hull([(px + s * ex, y, pz + s * ez) for px, pz in ((cx - 5.0 * sx, cz - 5.0 * sz), (sx * 25.0, sz * 25.0))
                    for s in (-1, 1) for y in (24.0, 28.0)], 'paint2', bevel=0.2)

    # ------------------------------------------------------------------ platform (origin 1.25, 0.25, -2.5)
    p = k.piece('platform'); P = p.at
    oc = octagon(R, PX, PZ)
    p.hull([(x, P(0, 0, 0)[1], z) for x, z in oc] + [(x, P(0, 22.0, 0)[1], z) for x, z in oc], 'paint2', bevel=0.3)
    p.hull([(x, P(0, 21.8, 0)[1], z) for x, z in oc] + [(x, P(0, TOP - 0.6, 0)[1], z) for x, z in octagon(R - 1.0, PX, PZ)],
           'paint', bevel=0.35)
    p.plan(P(0, TOP - 0.7, 0)[1], P(0, TOP, 0)[1], octagon(R - 1.4, PX, PZ), 'paint2', bevel=0.1)        # flight deck
    for i in range(0, 8):                                                   # team corner panels outside the pad
        t = math.pi / 8 + i * math.pi / 4
        if abs(math.cos(t)) > 0.9:                                         # skip the bay sides (+-x)
            continue
        cx, cz = PX + (R - 4.0) * math.cos(t), PZ + (R - 4.0) * math.sin(t)
        p.cyl((cx, P(0, TOP - 0.1, 0)[1], cz), (cx, P(0, TOP + 0.3, 0)[1], cz), 3.6, 8, 'team', rot=math.pi / 8)
    p.box(P(-30.6, 26.0, -6.0), P(-30.2, 27.4, 6.0), 'lightc', bevel=0.0)
    # side bays (x +-(29.8..48)), hollow; the lift columns fill them at rest
    for sx in (-1, 1):
        x0, x1 = sorted((sx * 28.5, sx * 49.0))
        xo0, xo1 = sorted((sx * 47.8, sx * 49.0))
        p.box(P(xo0, 6.0, -9.2), P(xo1, TOP, 13.0), 'paint', bevel=0.3)                     # outer wall
        p.box(P(x0, 6.0, -9.2), P(x1, TOP, -7.4), 'paint', bevel=0.3)
        p.box(P(x0, 6.0, 11.2), P(x1, TOP, 13.0), 'paint', bevel=0.3)
        p.box(P(x0, 6.0, -7.4), P(x1, 8.0, 11.2), 'black', bevel=0.0)                        # well floor
        p.box(P(x0 + 0.4, TOP - 0.05, -8.9), P(x1 - 0.4, TOP + 0.35, -7.6), 'hazard', bevel=0.04)
        p.box(P(x0 + 0.4, TOP - 0.05, 11.4), P(x1 - 0.4, TOP + 0.35, 12.7), 'hazard', bevel=0.04)

    # hatches (door1 origin 31, 33.37, -0.25; hinged on the inner edge)
    d = k.piece('door1'); D = d.at
    d.box(D(0.2, -0.45, -9.6), D(17.6, 0.3, 8.8), 'paint', bevel=0.2)
    d.box(D(1.8, 0.25, -8.0), D(16.0, 0.5, 7.2), 'team', bevel=0.06)
    k.clone('door2', 'door1', mirror_x=True)
    # lift columns (plate1 origin 39.25, 8.5, -0.5)
    c = k.piece('plate1'); C = c.at
    c.box(C(-7.8, 0.0, -8.8), C(9.0, 23.6, 8.6), 'paint', bevel=0.4)
    c.box(C(-7.0, 23.5, -8.0), C(8.2, 24.0, 7.8), 'hazard', bevel=0.06)
    c.box(C(-8.0, 14.0, -6.0), C(-7.7, 15.4, 6.0), 'lightc', bevel=0.0)
    c.box(C(-8.0, 2.0, -7.0), C(9.2, 6.0, 7.0), 'paint2', bevel=0.15)
    k.clone('plate2', 'plate1', mirror_x=True)
    # nano heads (nano1 origin 43.87, 16.5, -0.5): arm up to beam1 (0, 11.12, 0); bends over the pad when open
    n = k.piece('nano1'); N = n.at
    n.box(N(-2.8, -4.6, -3.0), N(3.0, 1.6, 3.0), 'steel', bevel=0.3)
    n.hull([N(x, y, z) for x, y, z in [(-2.2, 1.4, -2.4), (2.4, 1.4, -2.4), (-2.2, 1.4, 2.4), (2.4, 1.4, 2.4),
                                       (-1.3, 9.6, -1.3), (1.3, 9.6, -1.3), (-1.3, 9.6, 1.3), (1.3, 9.6, 1.3)]], 'dark',
           bevel=0.2)
    n.box(N(2.3, 2.0, -1.8), N(2.7, 8.6, 1.8), 'hazard', bevel=0.03)
    n.cyl(N(0, 9.5, 0), N(0, 11.12, 0), 1.2, 10, 'lightc')
    k.clone('nano2', 'nano1', mirror_x=True)

    # ------------------------------------------------------------------ pad (origin 1.29, 34.98, -2.09)
    pd = k.piece('pad'); Pd = pd.at
    pd.cyl(Pd(0, -1.95, 0), Pd(0, -0.3, 0), 26.6, 40, 'dark', bevel=0.12)
    pd.cyl(Pd(0, -0.3, 0), Pd(0, -0.18, 0), 24.4, 40, 'paint')
    pd.cyl(Pd(0, -0.2, 0), Pd(0, -0.1, 0), 4.2, 16, 'paint2')
