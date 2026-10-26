"""Radar Tower (ARM_T1_DEF_RadarTower) - Arm radar. A tall slim lattice mast on a square pad; on top a spinning hub
(drops 7 elmo into the mast collar when switched off) carrying two wide radar paddles that tumble on their X axles.
Identity from above: a long light bar (the two paddles, dark frames, cyan tips) crossing a small team-capped hub, over
a dark square pad with team corners - nothing else on the Arm side is a 'T' of paddles.
Pieces (Lua script): base, dish (move y, spin y), ear1/ear2 (spin x; ear2 is ear1 mirrored).
Coordinates are ENGINE/global: X right, Y up, Z forward."""
import math

UNIT = dict(
    res=1024,
    wreck=dict(seed=13, drop=['ear2'], pose={'ear1': (40, 0, 0)}),
    preview_pose={'dish': (0, 20, 0), 'ear1': (35, 0, 0), 'ear2': (-35, 0, 0)},
)


def build(k):
    # ------------------------------------------------------------------ base: pad + lattice mast
    b = k.piece('base')
    pad = [(-14, -10), (-10, -14), (10, -14), (14, -10), (14, 10), (10, 14), (-10, 14), (-14, 10)]
    b.plan(0.0, 2.2, pad, 'paint2', bevel=0.2, top_inset=0.8)
    for sz in (-1, 1):   # team corner chevrons
        b.hull([(x, y, z * sz) for x, y, z in
                [(6.0, 2.2, 12.6), (12.6, 2.2, 6.0), (9.4, 2.2, 12.6), (12.6, 2.2, 9.4),
                 (6.0, 2.38, 12.6), (12.6, 2.38, 6.0), (9.4, 2.38, 12.6), (12.6, 2.38, 9.4)]], 'team', bevel=0.0, mirror=True)
    # footing pyramid
    b.plan(2.0, 9.0, [(-9.5, -9.5), (9.5, -9.5), (9.5, 9.5), (-9.5, 9.5)], 'paint', bevel=0.2, top_inset=3.0)
    # four corner legs of the mast (slightly tapering), dark
    for sz in (-1, 1):
        b.hull([(x, y, z * sz) for x, y, z in
                [(4.2, 8.0, 4.2), (6.6, 8.0, 4.2), (4.2, 8.0, 6.6), (6.6, 8.0, 6.6),
                 (3.0, 47.0, 3.0), (4.8, 47.0, 3.0), (3.0, 47.0, 4.8), (4.8, 47.0, 4.8)]], 'dark', bevel=0.12, mirror=True)
    # light core panels between the legs (the mast reads as a light column with dark corner edges)
    b.cyl((0, 8.0, 0), (0, 47.0, 0), 5.6, 4, 'paint', r2=4.4, rot=math.pi / 4, bevel=0.15)
    # bracing bands
    for y in (19.0, 33.0):
        b.cyl((0, y, 0), (0, y + 2.2, 0), 7.6, 4, 'paint2', rot=math.pi / 4, bevel=0.12)
    # top collar the hub sinks into
    b.cyl((0, 46.0, 0), (0, 52.8, 0), 8.6, 8, 'paint2', r2=8.0, rot=math.pi / 8, bevel=0.15)
    b.cyl((0, 52.8, 0), (0, 52.95, 0), 6.4, 12, 'black')
    b.box((-1.0, 49.0, 7.4), (1.0, 50.4, 8.3), 'lightr', bevel=0.0)

    # ---------------------------------------------------------------- dish: spinning hub (origin -0.99, 53.26, 0.16)
    d = k.piece('dish'); D = d.at
    d.cyl(D(0, -1.0, 0), D(0, 9.0, 0), 5.4, 12, 'paint', bevel=0.12)
    d.cyl(D(0, 9.0, 0), D(0, 11.0, 0), 4.0, 12, 'dark', bevel=0.08)
    # axle housing across X
    d.cyl(D(-10.6, 13.39, 2.61), D(11.3, 13.39, 2.61), 2.6, 10, 'dark', bevel=0.08)
    d.hull([D(x, y, z) for x in (-5.6, 6.2) for y, z in
            [(9.0, -3.4), (9.0, 6.0), (17.2, -2.8), (17.2, 5.6)]], 'paint', bevel=0.2)
    d.hull([D(x, y, z) for x in (-4.4, 5.0) for y, z in
            [(17.2, -2.0), (17.2, 4.8), (17.38, -2.0), (17.38, 4.8)]], 'team', bevel=0.0)
    d.box(D(-1.0, 13.0, 5.95), D(1.6, 14.4, 6.1), 'lightc', bevel=0.0)

    # --------------------------------------------------------------- ears: radar paddles (ear1 origin +9.71, 66.65, 2.77)
    e = k.piece('ear1'); E = e.at
    e.cyl(E(-0.4, 0, 0), E(5.0, 0, 0), 1.6, 8, 'steel')
    e.box(E(3.4, -7.4, -1.6), E(19.8, 7.4, 1.6), 'dark', bevel=0.15)            # frame
    e.box(E(4.4, -6.6, -2.0), E(18.8, 6.6, 2.0), 'paint', bevel=0.15)           # array faces (both sides)
    e.box(E(4.6, -0.3, -2.1), E(18.6, 0.3, 2.1), 'paint2', bevel=0.0)              # centre element rib
    e.box(E(19.6, -2.2, -0.8), E(20.6, 2.2, 0.8), 'lightc', bevel=0.0)
    k.clone('ear2', 'ear1', mirror_x=True)
