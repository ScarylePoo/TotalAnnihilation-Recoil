"""Samson (ARM_T1_VEH_Samson) - Arm mobile missile launcher. Half-track truck: low cab with two front wheels,
tall tracked cargo bed at the rear carrying a twin-tube missile box on a post (turret turns y, launcher turns x),
offset to the right as in TA.
Value groups from above: light Arm cab + bed sides, darker paint2 cargo deck, dark tracks/wheels, a big
team-coloured lid on the launcher box (the unit's signature read from above) + team bands on the bed rails.
Coordinates are ENGINE/global: X right, Y up, Z forward. mirror=True builds the -X twin sharing UVs."""
import math

UNIT = dict(
    res=1024,
    wreck=dict(seed=2, drop=['launcher'], pose={'turret': (0, 50, 0)}),
    preview_pose={'turret': (0, -15, 0), 'launcher': (-12, 0, 0)},
)


def build(k):
    b = k.piece('base')
    # ------------------------------------------------------------------ running gear
    # rear tracks (z -23 .. 2)
    xi, xo = 10.4, 16.4
    belt = [(-20.6, 0.0), (-1.0, 0.0), (1.8, 2.2), (1.2, 4.6), (-21.0, 4.6), (-23.2, 2.4)]
    b.prism(xi, xo, belt, 'tread', bevel=0.15, mirror=True)
    for z in (-18.0, -12.6, -7.2, -1.8):
        b.cyl((xi, 1.8, z), (xi - 0.45, 1.8, z), 1.5, 12, 'dark', mirror=True)
        b.cyl((xi - 0.45, 1.8, z), (xi - 0.7, 1.8, z), 0.6, 8, 'steel', mirror=True)
    # front wheels (static, part of base)
    for z in (16.0,):
        b.cyl((11.0, 4.6, z), (16.0, 4.6, z), 4.6, 16, 'tread', rot=math.pi / 16, bevel=0.15, mirror=True)
        b.cyl((16.0, 4.6, z), (16.3, 4.6, z), 2.5, 12, 'dark', bevel=0.05, mirror=True)
        b.cyl((16.3, 4.6, z), (16.5, 4.6, z), 1.0, 8, 'steel', mirror=True)
        # mudguard with team top
        b.hull([(10.6, 9.6, z - 5.4), (16.8, 9.6, z - 5.4), (10.6, 9.6, z + 4.6), (16.8, 9.6, z + 4.6),
                (10.6, 10.6, z - 4.0), (16.8, 10.6, z - 4.0), (10.6, 10.6, z + 3.2), (16.8, 10.6, z + 3.2),
                (10.6, 7.8, z + 6.0), (16.8, 7.8, z + 6.0)], 'paint', bevel=0.12, mirror=True)
        b.box((11.4, 10.6, z - 3.4), (16.0, 10.76, z + 2.6), 'team', bevel=0.04, mirror=True)

    # ------------------------------------------------------------------ chassis + cab (crosses x = 0)
    b.prism(-10.6, 10.6, [(-22.6, 3.0), (20.6, 3.0), (22.4, 5.0), (21.6, 7.4), (-22.8, 7.4), (-23.6, 5.0)], 'paint2', bevel=0.15)
    # cab: low, sloped windscreen, bonnet to the nose
    b.hull([(x * sx, y, z) for sx in (-1, 1) for x, y, z in
            [(10.0, 7.2, 1.0), (10.0, 7.2, 21.8), (9.0, 7.0, 23.2),
             (9.4, 11.4, 21.0), (9.6, 12.6, 12.0), (9.0, 16.6, 8.4), (9.4, 16.6, 1.0)]], 'paint', bevel=0.16)
    b.hull([(x * sx, y, z) for sx in (-1, 1) for x, y, z in
            [(8.0, 12.9, 11.5), (7.6, 16.1, 8.9), (8.0, 13.02, 11.62), (7.6, 16.22, 9.02)]], 'glass', bevel=0.03)
    # team plate on the cab roof, hazard bonnet band
    b.box((-7.0, 16.6, 2.0), (7.0, 16.78, 7.6), 'team', bevel=0.04)
    b.hull([(x * sx, y, z) for sx in (-1, 1) for x, y, z in
            [(8.0, 11.42, 20.6), (8.0, 12.4, 15.0), (8.0, 11.56, 20.64), (8.0, 12.54, 15.04)]], 'hazard', bevel=0.03)
    # grille + headlights
    b.box((-6.0, 8.0, 22.3), (6.0, 10.6, 22.9), 'dark', bevel=0.06)
    for y in (8.4, 9.2, 10.0):
        b.box((-5.6, y, 22.85), (5.6, y + 0.35, 23.0), 'black', bevel=0.0)
    b.box((6.6, 8.6, 22.2), (8.6, 10.0, 22.9), 'dark', bevel=0.06, mirror=True)
    b.box((6.8, 8.8, 22.88), (8.4, 9.8, 22.98), 'lightw', bevel=0.0, mirror=True)

    # ------------------------------------------------------------------ cargo bed (rear, tall)
    # bed sides: light armoured walls
    b.hull([(9.0, 7.2, -22.6), (11.4, 7.2, -22.6), (9.0, 7.2, 0.6), (11.4, 7.2, 0.6),
            (9.0, 15.2, -22.0), (10.8, 15.2, -22.0), (9.0, 15.2, 0.4), (10.8, 15.2, 0.4)], 'paint', bevel=0.14, mirror=True)
    b.box((9.3, 15.2, -21.0), (10.6, 15.36, -0.6), 'team', bevel=0.03, mirror=True)
    # bed deck between the walls, darker (launcher sits on it)
    b.box((-9.1, 7.2, -22.4), (9.1, 14.2, 0.6), 'paint2', bevel=0.12)
    # left side of the deck: reload rack of spare missiles (lies flat, reads as dark/light stripes)
    for x in (-7.4, -4.6):
        b.cyl((x, 15.3, -20.6), (x, 15.3, -4.0), 1.15, 10, 'dark', rot=math.pi / 10)
        b.cyl((x, 15.3, -4.0), (x, 15.3, -2.2), 1.15, 10, 'hazard', r2=0.3, rot=math.pi / 10)
    b.box((-8.8, 14.2, -18.0), (-3.2, 14.6, -16.6), 'dark', bevel=0.05)
    b.box((-8.8, 14.2, -8.0), (-3.2, 14.6, -6.6), 'dark', bevel=0.05)
    # tail: dark plate + lights
    b.box((-8.0, 8.0, -23.2), (8.0, 13.0, -22.6), 'dark', bevel=0.06)
    b.box((6.2, 11.4, -23.3), (7.6, 12.2, -23.15), 'lightr', bevel=0.0, mirror=True)
    # antenna on the cab, left
    b.cyl((-8.2, 16.6, 2.6), (-8.2, 17.3, 2.6), 0.34, 8, 'dark')
    b.cyl((-8.2, 17.3, 2.6), (-8.2, 22.5, 2.6), 0.09, 6, 'steel', r2=0.045)
    b.cyl((-8.2, 22.5, 2.6), (-8.2, 22.7, 2.6), 0.14, 6, 'lightc')

    # ---------------------------------------------------------------- turret (post, origin 3.62, 16.62, -12.88)
    t = k.piece('turret'); A = t.at
    t.cyl(A(0, -2.4, 0), A(0, -1.6, 0), 3.0, 14, 'dark', bevel=0.06)
    t.cyl(A(0, -1.6, 0), A(0, 2.6, 0), 1.35, 10, 'steel', rot=math.pi / 10)
    t.box(A(-2.0, 2.0, -1.2), A(2.0, 3.1, 1.2), 'dark', bevel=0.08)

    # ---------------------------------------------------------------- launcher (origin y 19.75; elevates)
    l = k.piece('launcher'); L = l.at
    # box: two tube rows side by side, light shell with a team lid
    l.hull([L(x * sx, y, z) for sx in (-1, 1) for x, y, z in
            [(4.6, 0.1, -8.0), (4.6, 0.1, 7.4), (4.6, 4.2, -8.0), (4.4, 4.2, 7.0)]], 'paint', bevel=0.16)
    l.box(L(-3.8, 4.15, -7.0), L(3.8, 4.35, 6.0), 'team', bevel=0.04)
    # front face: dark with two big tube mouths (bore axis at x +-1.75, y 2.13)
    l.box(L(-4.2, 0.5, 7.3), L(4.2, 3.8, 7.6), 'dark', bevel=0.05)
    for sx in (-1, 1):
        l.cyl(L(1.75 * sx, 2.13, 7.3), L(1.75 * sx, 2.13, 7.9), 1.3, 12, 'steel', bevel=0.04)
        l.cyl(L(1.75 * sx, 2.13, 7.9), L(1.75 * sx, 2.13, 7.98), 0.9, 12, 'black')
    # rear blast vents
    l.box(L(-3.8, 0.8, -8.3), L(3.8, 3.5, -7.9), 'black', bevel=0.0)
    # side rails (dark bands break the box from above at the edges)
    for sx in (-1, 1):   # launcher origin is off-centre: no mirror=True here
        l.box(L(min(4.5 * sx, 5.0 * sx), 1.0, -7.4), L(max(4.5 * sx, 5.0 * sx), 3.4, 6.8), 'dark', bevel=0.06)
    # sight on the left of the box
    l.box(L(-5.6, 2.4, 3.4), L(-4.9, 3.6, 5.6), 'dark', bevel=0.06)
    l.box(L(-5.5, 2.6, 5.58), L(-5.0, 3.3, 5.68), 'lightc', bevel=0.0)
