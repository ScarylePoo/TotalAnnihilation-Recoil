"""Annihilator (ARM_T2_DEF_Annihilator) - Arm long-range energy weapon. A massive stepped bunker with a slot in its
roof; switched on, the slot doors stand up and a tall pylon (arm) lifts the gun head 62.5 elmo out of the bunker. The
head carries one long heavy beam barrel, a short secondary barrel (ledgun) on the left, a spinning radar on the right
and an antenna mast.
Identity from above: a broad light square bunker with team decks either side of the slot and team-topped side pods,
the gun head on its pylon with a team roof and a long dark barrel pointing out over the bunker edge.
Built on the third-party S3O's piece layout (the COB drives it; preserved in tools/s3okit/ref/): annihilator.3ds
(root), base, arm (move y), turret (turn y), gun (turn x), ledgun (move z), radar (spin y), barrel (move z), fire
(emit, empty), antenna, door1/door2 (turn z). Default pose = open (deactivate sinks the arm and closes the doors).
Coordinates are ENGINE/global: X right, Y up, Z forward."""
import math

UNIT = dict(
    res=2048, bake_res=2048,          # no 2x supersampling: machine time (see the batch report)
    wreck=dict(seed=63, drop=['barrel', 'antenna'], pose={'turret': (0, 30, 0), 'gun': (14, 0, 0)}),
    preview_pose={'turret': (0, -25, 0), 'gun': (-6, 0, 0)},
)

TOP = 29.9
SX, SZ = 8.4, 16.0          # slot half-size


def build(k):
    # ------------------------------------------------------------------ base: stepped bunker round the slot
    b = k.piece('base')
    b.plan(0.0, 4.0, [(-32.0, -29.0), (-29.0, -32.0), (29.0, -32.0), (32.0, -29.0), (32.0, 29.0), (29.0, 32.0),
                      (-29.0, 32.0), (-32.0, 29.0)], 'paint2', bevel=0.3, top_inset=1.0)
    for s in (-1, 1):       # two halves of the main block either side of the slot (sloped outer, vertical inner)
        b.hull([(s * x, y, z) for x, y, zs in ((28.0, 3.8, 28.0), (SX, 3.8, 28.0), (20.0, TOP, 21.0), (SX, TOP, 21.0))
                for z in (-zs, zs)], 'paint', bevel=0.4)
        b.hull([(x, y, s * z) for x in (-SX - 0.5, SX + 0.5) for y, z in ((3.8, 28.0), (TOP, 21.0), (3.8, SZ), (TOP, SZ))],
               'paint', bevel=0.35)
    b.box((-SX, 4.0, -SZ), (SX, 5.0, SZ), 'black', bevel=0.0)
    # team decks either side of the slot
    for s in (-1, 1):
        b.box((min(s * 11.0, s * 17.6), TOP - 0.1, -16.0), (max(s * 11.0, s * 17.6), TOP + 0.22, 16.0), 'team', bevel=0.04)
    # four side pods (TA's flank blocks) with team tops
    for sx in (-1, 1):
        for sz in (-1, 1):
            cx, cz = sx * 27.0, sz * 12.0
            b.hull([(cx + x, y, cz + z) for x, y, z in
                    ((-5.0, 3.8, -6.0), (5.4, 3.8, -6.0), (-5.0, 3.8, 6.0), (5.4, 3.8, 6.0),
                     (-4.0, 15.0, -5.0), (3.6, 13.0, -5.0), (-4.0, 15.0, 5.0), (3.6, 13.0, 5.0))], 'paint2', bevel=0.3)
            b.hull([(cx + x, y, cz + z) for x, y, z in
                    ((-3.4, 14.95, -4.0), (2.8, 13.3, -4.0), (-3.4, 14.95, 4.0), (2.8, 13.3, 4.0),
                     (-3.4, 15.2, -4.0), (2.8, 13.55, -4.0), (-3.4, 15.2, 4.0), (2.8, 13.55, 4.0))], 'team', bevel=0.0)
    b.box((-6.0, 4.0, 27.4), (6.0, 14.0, 28.6), 'dark', bevel=0.1)
    b.box((-1.0, 16.0, 26.2), (1.0, 17.4, 26.8), 'lightc', bevel=0.0)

    # ------------------------------------------------------------------ doors: slot doors, standing when open (door1 x -8.56)
    d = k.piece('door1'); D = d.at
    d.box(D(-1.2, 0.0, -15.8), D(0.0, 8.4, 15.8), 'dark', bevel=0.1)
    d.box(D(-1.4, 0.6, -15.0), D(-1.15, 7.8, 15.0), 'hazard', bevel=0.03)
    k.clone('door2', 'door1', mirror_x=True)

    # ------------------------------------------------------------------ arm: the lifting pylon (origin 0, 0, 0)
    a = k.piece('arm')
    a.hull([(x * sx, y, z * sz) for sx in (-1, 1) for sz in (-1, 1) for x, y, z in
            [(7.2, 8.4, 14.2), (4.6, 49.2, 6.0)]], 'paint2', bevel=0.3)
    for y in (20.0, 34.0):
        f = (y - 8.4) / 40.8
        a.hull([(x * sx, yy, z * sz) for sx in (-1, 1) for sz in (-1, 1) for x, yy, z in
                [(7.4 - 2.6 * f, y, 14.4 - 8.2 * f), (7.4 - 2.6 * (f + 0.05), y + 2.0, 14.4 - 8.2 * (f + 0.05))]], 'dark', bevel=0.06)

    # ------------------------------------------------------------------ turret: swivel ring (origin 0, 0, 0)
    t = k.piece('turret')
    t.cyl((0, 49.0, 0), (0, 53.4, 0), 5.6, 12, 'dark', bevel=0.1)

    # ------------------------------------------------------------------ gun: head (origin 0, 53.63, 0)
    g = k.piece('gun'); G = g.at
    g.hull([G(x * sx, y, z) for sx in (-1, 1) for x, y, z in
            [(9.0, -2.6, -14.0), (9.0, -2.6, 9.0), (6.0, -2.6, 13.4), (8.2, 7.6, -12.6), (8.2, 7.6, 6.0), (4.8, 7.0, 12.4)]],
           'paint', bevel=0.35)
    g.box(G(-6.0, 7.55, -11.0), G(6.0, 7.85, 4.4), 'team', bevel=0.03)
    g.cyl(G(0, 6.24, 9.0), G(0, 6.24, 13.6), 3.8, 10, 'dark', bevel=0.06)      # barrel mantlet
    g.box(G(-8.0, 0.6, -14.3), G(8.0, 5.6, -13.8), 'black', bevel=0.0)

    # ------------------------------------------------------------------ ledgun (origin -6, 59.86, 10.19)
    l = k.piece('ledgun'); L = l.at
    l.cyl(L(0, 0, -2.0), L(0, 0, 10.6), 1.0, 8, 'dark', rot=math.pi / 8)
    l.cyl(L(0, 0, 9.4), L(0, 0, 10.8), 1.3, 8, 'steel', rot=math.pi / 8)

    # ------------------------------------------------------------------ radar (origin 5.26, 62.64, -6.3)
    r = k.piece('radar'); R = r.at
    r.cyl(R(0, -0.2, 0), R(0, 0.8, 0), 0.8, 8, 'dark')
    r.hull([R(x, y, z) for x in (-1.6, -0.6) for y in (0.4, 2.4) for z in (-4.2, 4.2)], 'steel', bevel=0.08)

    # ------------------------------------------------------------------ barrel (origin 0, 59.87, 12.97)
    br = k.piece('barrel'); B = br.at
    br.cyl(B(0, 0, -0.5), B(0, 0, 17.0), 2.7, 10, 'dark', rot=math.pi / 10)
    for z in (5.0, 10.0):
        br.cyl(B(0, 0, z), B(0, 0, z + 1.2), 3.1, 10, 'steel', rot=math.pi / 10)
    br.cyl(B(0, 0, 16.4), B(0, 0, 19.6), 3.5, 8, 'steel', r2=3.1, rot=math.pi / 8, bevel=0.05)
    br.cyl(B(0, 0, 19.58), B(0, 0, 19.7), 1.2, 8, 'lightc')

    # ------------------------------------------------------------------ antenna (origin 0, 62.57, -7.26)
    an = k.piece('antenna'); N = an.at
    an.cyl(N(-5.4, -0.4, -1.0), N(-5.4, 20.0, -1.0), 0.55, 6, 'dark')
    an.box(N(-6.0, 19.6, -1.6), N(-4.8, 20.8, -0.4), 'lightr', bevel=0.0)
