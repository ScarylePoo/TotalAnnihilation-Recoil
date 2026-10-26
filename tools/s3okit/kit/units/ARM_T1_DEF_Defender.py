"""Defender (ARM_T1_DEF_Defender) - Arm missile tower. A tall four-legged pylon on a square pad, a yoke turret on top
and a long missile box with a fat revolving three-tube cluster at the nose (the barrel piece turns on z between shots).
Identity from above: a long light launcher box with a team-coloured roof stripe on a dark pad with team corners, the
dark revolver drum out front.
Pieces (Lua script): base, turret (turn y), launcher (turn x), barrel (turn z: revolver), flare (emit, empty).
Coordinates are ENGINE/global: X right, Y up, Z forward."""
import math

UNIT = dict(
    res=1024,
    wreck=dict(seed=5, drop=['barrel'], pose={'turret': (0, 40, 0), 'launcher': (12, 0, 0)}),
    preview_pose={'turret': (0, -25, 0), 'launcher': (-12, 0, 0)},
)


def build(k):
    # ------------------------------------------------------------------ base: pad + four splayed legs + column
    b = k.piece('base')
    # square pad with chamfered corners (footprint 3x3 = 48 elmo; pad 44)
    pad = [(-22, -15), (-15, -22), (15, -22), (22, -15), (22, 15), (15, 22), (-15, 22), (-22, 15)]
    b.plan(0.0, 2.6, pad, 'paint2', bevel=0.2, top_inset=1.0)
    # team bands along the four pad edges, between the leg feet (wide, top-facing)
    b.box((17.0, 2.6, -8.5), (20.4, 2.78, 8.5), 'team', bevel=0.04, mirror=True)
    for sz in (-1, 1):
        b.box((-8.5, 2.6, min(17.0 * sz, 20.4 * sz)), (8.5, 2.78, max(17.0 * sz, 20.4 * sz)), 'team', bevel=0.04)
    # inner raised plinth
    b.plan(2.5, 4.6, [(-11, -8), (-8, -11), (8, -11), (11, -8), (11, 8), (8, 11), (-8, 11), (-11, 8)], 'paint', bevel=0.18, top_inset=0.8)
    # four splayed legs: foot blocks on the pad corners, leaning in to the column
    for sz in (-1, 1):
        b.hull([(x, y, z * sz) for x, y, z in
                [(10.5, 2.5, 10.5), (16.5, 2.5, 10.5), (10.5, 2.5, 16.5), (16.5, 2.5, 16.5),
                 (11.0, 6.5, 11.0), (16.0, 6.5, 11.0), (11.0, 6.5, 16.0), (16.0, 6.5, 16.0)]], 'dark', bevel=0.2, mirror=True)
        b.hull([(x, y, z * sz) for x, y, z in
                [(11.8, 6.0, 11.8), (15.2, 6.0, 11.8), (11.8, 6.0, 15.2), (15.2, 6.0, 15.2),
                 (3.0, 27.0, 3.0), (6.0, 27.0, 3.0), (3.0, 27.0, 6.0), (6.0, 27.0, 6.0)]], 'paint', bevel=0.2, mirror=True)
    # central column (crosses x=0)
    b.cyl((0, 4.5, 0), (0, 41.0, 0), 4.4, 8, 'paint2', r2=3.6, rot=math.pi / 8, bevel=0.15)
    b.cyl((0, 24.5, 0), (0, 30.0, 0), 7.2, 8, 'paint', r2=6.0, rot=math.pi / 8, bevel=0.2)   # leg collar
    for y in (33.0, 37.0):
        b.cyl((0, y, 0), (0, y + 1.0, 0), 4.6, 8, 'dark', rot=math.pi / 8, bevel=0.05)
    b.box((-1.2, 28.0, 6.5), (1.2, 29.3, 6.75), 'lightc', bevel=0.0)

    # ---------------------------------------------------------------- turret: yoke (origin 0, 40.7, -0.3)
    t = k.piece('turret'); A = t.at
    t.cyl(A(0, 0, 0), A(0, 1.6, 0), 6.4, 12, 'dark', bevel=0.1)
    t.hull([A(x * sx, y, z) for sx in (-1, 1) for x, y, z in
            [(5.6, 1.6, -5.0), (5.6, 1.6, 5.0), (4.6, 4.5, -4.4), (4.6, 4.5, 4.4)]], 'paint', bevel=0.15)
    # yoke arms either side of the launcher
    t.hull([A(x, y, z) for x, y, z in
            [(5.6, 4.0, -3.4), (8.6, 4.0, -3.4), (5.6, 4.0, 3.4), (8.6, 4.0, 3.4),
             (5.6, 12.4, -2.6), (8.2, 12.4, -2.6), (5.6, 12.4, 2.6), (8.2, 12.4, 2.6)]], 'paint2', bevel=0.15, mirror=True)
    t.cyl(A(8.2, 9.9, 1.1), A(9.4, 9.9, 1.1), 2.2, 10, 'dark', bevel=0.06, mirror=True)

    # --------------------------------------------------------------- launcher: long missile box (origin 0, 50.6, 0.8)
    l = k.piece('launcher'); L = l.at
    l.hull([L(x * sx, y, z) for sx in (-1, 1) for x, y, z in
            [(5.4, -3.6, -22.0), (5.4, -3.6, 15.0), (5.4, 4.2, -21.0), (5.4, 4.2, 14.4),
             (4.2, 5.6, -20.0), (4.2, 5.6, 13.6), (4.0, -4.6, -20.4), (4.0, -4.6, 14.8)]], 'paint', bevel=0.2)
    # team roof stripe running the length of the box
    l.hull([L(x * sx, y, z) for sx in (-1, 1) for x, y, z in
            [(2.6, 5.62, -18.0), (2.6, 5.62, 11.0), (2.4, 5.78, -17.8), (2.4, 5.78, 10.8)]], 'team', bevel=0.0)
    # dark rear exhaust block and side ribs
    l.box(L(-4.6, -3.0, -24.6), L(4.6, 3.8, -21.6), 'dark', bevel=0.15)
    for z in (-23.8, -22.8):
        l.box(L(-3.8, -2.2, z - 0.25), L(3.8, 3.0, z), 'black', bevel=0.0)
    l.box(L(5.3, -2.2, -16.0), L(6.0, 3.0, 8.0), 'paint2', bevel=0.1, mirror=True)
    # front collar holding the revolver
    l.cyl(L(0, 3.3, 14.4), L(0, 3.3, 18.0), 6.2, 12, 'dark', bevel=0.1)
    l.box(L(-1.0, 5.6, 11.8), L(1.0, 5.75, 13.2), 'lightr', bevel=0.0)

    # --------------------------------------------------------------- barrel: revolving 3-tube cluster (origin 0, 53.9, 19.5)
    br = k.piece('barrel'); B = br.at
    br.cyl(B(0, 0, -0.6), B(0, 0, 10.0), 2.4, 10, 'dark', bevel=0.05)
    for i in range(3):
        a = math.radians(90 + 120 * i)
        cx, cy = 4.3 * math.cos(a), 4.3 * math.sin(a)
        br.cyl(B(cx, cy, -0.4), B(cx, cy, 10.4), 2.75, 10, 'paint2', bevel=0.08)
        br.cyl(B(cx, cy, 10.4), B(cx, cy, 10.95), 2.0, 10, 'steel')
        br.cyl(B(cx, cy, 10.9), B(cx, cy, 11.05), 1.5, 10, 'black')
    br.cyl(B(0, 0, 3.6), B(0, 0, 5.2), 7.4, 12, 'dark', bevel=0.08)        # band round the cluster
    br.cyl(B(0, 0, 10.0), B(0, 0, 10.8), 1.4, 8, 'hazard')
