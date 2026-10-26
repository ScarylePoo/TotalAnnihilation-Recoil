"""Viper (CORE_T1_DEF_Viper) - Core pop-up gun. Closed it is a flat armoured pad with a four-leaf hatch (hazard-striped
doors); on activation the doors flip open outward (turn ~179 deg on their hinges) and the stand rises 58.5 elmo out
of the ground with a boxy gun head whose barrel swings down from vertical (turret2 x 90 deg when stowed).
Identity from above: closed = dark square pad, team corner blocks, a yellow-black hatch cross in the middle (the only
striped hatch on the Core side); open = the flipped dark door undersides round a tall pillar with a team-topped gun
head and a long light barrel on its left side.
Pieces (COB): base, door1..4 (turn z / x), stand (move y), turret1 (turn y), turret2 (turn x), barrel, flare (empty).
The preview shows the OPEN state (doors flipped, stand up): the default model pose is open, the COB closes it at
Create (stand -58.5, doors ~-3 deg, turret2 90 deg).
Coordinates are ENGINE/global: X right, Y up, Z forward."""
import math

UNIT = dict(
    res=1024,
    wreck=dict(seed=41, drop=['barrel'], pose={'turret1': (0, 40, 0)}),
    preview_pose={'door1': (0, 0, -179), 'door2': (0, 0, 179), 'door3': (-179, 0, 0), 'door4': (179, 0, 0),
                  'turret1': (0, -25, 0)},
)

HX, HZ = 13.72, 7.24        # hatch half-size (door hinges)


def door_plate(d, pts_xz, y0=-0.35, y1=0.35):
    """a door: hazard top, dark-warm underside (seen when flipped open)"""
    D = d.at
    d.hull([D(x, y, z) for x, z in pts_xz for y in (0.0, y1)], 'hazard', bevel=0.06)
    d.hull([D(x, y, z) for x, z in pts_xz for y in (y0, 0.0)], 'paint2', bevel=0.06)


def build(k):
    # ------------------------------------------------------------------ base: pad around the hatch well
    b = k.piece('base')
    y = 1.69
    b.box((-16.0, 0.0, -16.0), (16.0, y - 0.4, -HZ), 'paint', bevel=0.25)
    b.box((-16.0, 0.0, HZ), (16.0, y - 0.4, 16.0), 'paint', bevel=0.25)
    b.box((-16.0, 0.0, -HZ), (-HX, y - 0.4, HZ), 'paint', bevel=0.25)
    b.box((HX, 0.0, -HZ), (16.0, y - 0.4, HZ), 'paint', bevel=0.25)
    # raised hatch coaming (dark ring) and well
    b.box((-HX - 1.2, y - 0.5, -HZ - 1.2), (HX + 1.2, y + 0.3, -HZ), 'dark', bevel=0.1)
    b.box((-HX - 1.2, y - 0.5, HZ), (HX + 1.2, y + 0.3, HZ + 1.2), 'dark', bevel=0.1)
    b.box((-HX - 1.2, y - 0.5, -HZ), (-HX, y + 0.3, HZ), 'dark', bevel=0.1)
    b.box((HX, y - 0.5, -HZ), (HX + 1.2, y + 0.3, HZ), 'dark', bevel=0.1)
    b.box((-HX, -0.4, -HZ), (HX, 0.2, HZ), 'black', bevel=0.0)                 # well floor
    # team corner blocks
    for sx in (-1, 1):
        for sz in (-1, 1):
            lo = (min(10.0 * sx, 15.4 * sx), y - 0.4, min(10.4 * sz, 15.4 * sz))
            hi = (max(10.0 * sx, 15.4 * sx), y + 1.2, max(10.4 * sz, 15.4 * sz))
            b.box(lo, hi, 'team', bevel=0.12)
    b.box((15.95, 0.4, -1.0), (16.1, 1.0, 1.0), 'lightr', bevel=0.0)

    # ------------------------------------------------------------------ doors (hinged at the coaming, closing inward)
    d1 = k.piece('door1')
    door_plate(d1, [(0.0, -7.1), (6.95, -7.1), (6.95, 7.1), (0.0, 7.1)])
    k.clone('door2', 'door1', mirror_x=True)
    d3 = k.piece('door3')
    door_plate(d3, [(-6.65, 0.0), (6.65, 0.0), (6.65, 7.15), (-6.65, 7.15)])
    d4 = k.piece('door4')
    door_plate(d4, [(-6.65, -7.15), (6.65, -7.15), (6.65, 0.0), (-6.65, 0.0)])

    # ------------------------------------------------------------------ stand: the pillar that rises (origin 0, 1.8, 0)
    s = k.piece('stand'); S = s.at
    s.box(S(-5.6, -0.2, -6.4), S(5.6, 33.6, 6.2), 'paint', bevel=0.3)
    for yy in (8.0, 18.0, 28.0):
        s.box(S(-5.9, yy, -6.7), S(5.9, yy + 1.4, 6.5), 'dark', bevel=0.08)
    s.box(S(-3.6, 2.0, 6.2), S(3.6, 26.0, 6.6), 'paint2', bevel=0.06)

    # ------------------------------------------------------------------ turret1: gun head (origin 0, 35.49, 0)
    t = k.piece('turret1'); A = t.at
    t.cyl(A(0, -1.4, 0), A(0, 0.2, 0), 5.6, 12, 'dark', bevel=0.08)
    t.hull([A(x, y, z) for x, y, z in
            [(-3.6, 0.0, -7.2), (9.6, 0.0, -7.2), (-3.6, 0.0, 6.6), (9.6, 0.0, 6.0),
             (-3.6, 11.6, -6.6), (8.0, 11.6, -6.6), (-3.6, 11.6, 4.6), (8.0, 10.4, 5.4)]], 'paint', bevel=0.3)
    t.hull([A(x, y, z) for x, y, z in
            [(-2.6, 11.6, -5.6), (7.0, 11.6, -5.6), (-2.6, 11.6, 3.6), (7.0, 11.6, 3.6),
             (-2.6, 11.8, -5.6), (7.0, 11.8, -5.6), (-2.6, 11.8, 3.6), (7.0, 11.8, 3.6)]], 'team', bevel=0.0)
    t.box(A(9.4, 2.0, -5.0), A(10.0, 9.0, 3.0), 'paint2', bevel=0.08)
    t.box(A(3.0, 6.0, 5.6), A(6.0, 7.4, 6.2), 'lightr', bevel=0.0)

    # ------------------------------------------------------------------ turret2: gun cradle (origin -3.75, 42.49, -0.52)
    c = k.piece('turret2'); C = c.at
    c.cyl(C(-0.4, 0, 0), C(1.0, 0, 0), 3.4, 10, 'dark', bevel=0.06)
    c.hull([C(x, y, z) for x, y, z in
            [(-9.8, -5.6, -9.6), (-0.2, -5.6, -9.6), (-9.8, 5.6, -9.6), (-0.2, 5.6, -9.6),
             (-9.8, -5.0, 13.4), (-0.2, -5.0, 13.4), (-9.8, 6.4, 13.4), (-0.2, 6.4, 13.4)]], 'paint2', bevel=0.3)
    c.box(C(-9.0, 6.3, -7.0), C(-1.0, 6.5, 11.0), 'hazard', bevel=0.03)
    c.cyl(C(-4.0, 2.5, 13.2), C(-4.0, 2.5, 16.4), 3.0, 8, 'dark', rot=math.pi / 8, bevel=0.08)

    # ------------------------------------------------------------------ barrel (origin -7.75, 44.99, 15.23)
    br = k.piece('barrel'); B = br.at
    br.cyl(B(0, 0, 0.0), B(0, 0, 15.2), 1.35, 8, 'steel', rot=math.pi / 8)
    br.cyl(B(0, 0, 6.0), B(0, 0, 7.0), 1.7, 8, 'dark', rot=math.pi / 8)
    br.cyl(B(0, 0, 14.0), B(0, 0, 16.0), 1.9, 8, 'dark', rot=math.pi / 8, bevel=0.05)
    br.cyl(B(0, 0, 15.98), B(0, 0, 16.08), 0.9, 8, 'black')
