"""Geothermal Powerplant (ARM_T1_ECO_GeothermalPowerplant) - Arm geothermal. A long light turbine hall at the back
of the footprint, a dark raised turbine house in the middle of its roof, a tall fat dark vent stack on the left and
a loop of thick steel steam pipes running forward round the vent to a wellhead at the front.
Identity from above: a wide light block with a big black stack mouth (lit rim) on the left, a team roof plate on
the right and a steel pipe ring in front (the Core geothermal is a dark hall with a tilted tower and sweeping arms).
Pieces (Lua script): base, pieces (pipes + wellhead), smoke / explode1 / explode2 (empty emit points; the stack
mouth sits at the smoke point).
Coordinates are ENGINE/global: X right, Y up, Z forward."""
import math

UNIT = dict(
    wreck=dict(seed=23, drop=['pieces']),
    preview_pose={},
)

SX, SZ = -18.46, -4.73        # stack axis (the 'smoke' emit point is at y 57.18)


def build(k):
    b = k.piece('base')
    hall = [(-32.0, -26.0), (-28.0, -30.0), (28.0, -30.0), (32.0, -26.0), (32.0, -2.0), (28.0, 2.0), (-28.0, 2.0),
            (-32.0, -2.0)]
    b.plan(0.0, 3.0, [(x * 1.06, z * 1.04 - 0.6) for x, z in hall], 'paint2', bevel=0.3, top_inset=1.0)
    b.plan(2.9, 36.0, hall, 'paint', bevel=0.4, top_inset=1.6)
    # dark girders round the hall
    b.plan(18.0, 20.4, [(x * 1.0 + (0.4 if x > 0 else -0.4), z + (0.4 if z > -14 else -0.4)) for x, z in hall], 'dark',
           bevel=0.1, top_inset=0.2)
    # turbine house on the roof (dark) with black louvre slats
    b.box((-10.0, 35.8, -27.0), (10.0, 46.0, -7.0), 'paint2', bevel=0.35)
    for z0 in (-24.0, -20.0, -16.0, -12.0):
        b.box((-8.6, 45.9, z0), (8.6, 46.4, z0 + 2.0), 'black', bevel=0.0)
    # team roof plate on the right wing
    b.box((12.6, 35.9, -26.4), (28.6, 36.3, -4.0), 'team', bevel=0.0)
    b.box((-30.4, 35.9, -26.4), (-26.2, 36.3, -1.4), 'team', bevel=0.0)
    # vent stack on the left wing: fat dark tapered chimney, lit rim, black mouth
    b.cyl((SX, 35.8, SZ), (SX, 39.0, SZ), 9.0, 12, 'paint2', r2=8.2, rot=math.pi / 12, bevel=0.2)
    b.cyl((SX, 38.9, SZ), (SX, 56.4, SZ), 7.2, 12, 'dark', r2=5.8, rot=math.pi / 12, bevel=0.15)
    for y in (44.0, 50.0):
        b.cyl((SX, y, SZ), (SX, y + 1.4, SZ), 7.2 - (y - 38.9) * 0.08 + 0.35, 12, 'steel', rot=math.pi / 12)
    b.cyl((SX, 56.3, SZ), (SX, 57.3, SZ), 6.4, 12, 'lightr', rot=math.pi / 12)
    b.cyl((SX, 56.6, SZ), (SX, 57.5, SZ), 4.6, 12, 'black', rot=math.pi / 12)
    # front: big dark doors with hazard lintels on both wings
    for x0 in (-26.0, 12.0):
        b.box((x0, 3.0, 1.6), (x0 + 14.0, 16.0, 2.3), 'dark', bevel=0.05)
        b.box((x0, 16.2, 1.6), (x0 + 14.0, 17.6, 2.4), 'hazard', bevel=0.0)
    b.box((-2.0, 30.0, 1.5), (2.0, 31.6, 2.1), 'lightc', bevel=0.0)

    # ------------------------------------------------------------------ pieces: steam pipe loop + wellhead
    p = k.piece('pieces')
    R = 3.0
    for sx in (-1, 1):
        x = sx * 15.0
        p.cyl((x, 20.0, 1.0), (x, 20.0, 18.0), R, 10, 'steel', rot=math.pi / 10)
        p.cyl((x, 20.0, 18.0), (sx * 8.0, 20.0, 26.0), R, 10, 'steel', rot=math.pi / 10)
        p.cyl((sx * 8.0, 20.0, 26.0), (sx * 4.2, 20.0, 26.0), R, 10, 'steel', rot=math.pi / 10)
        for z in (6.0, 13.0):
            p.cyl((x, 20.0, z), (x, 20.0, z + 1.6), R + 0.5, 10, 'dark', rot=math.pi / 10)
        p.box((x - 2.0, 0.0, 10.0), (x + 2.0, 17.6, 12.0), 'dark', bevel=0.15)             # pipe trestle
        p.box((x - 3.6, 0.0, 9.0), (x + 3.6, 1.2, 13.0), 'paint2', bevel=0.1)
    # wellhead
    p.box((-5.0, 0.0, 22.0), (5.0, 24.0, 30.0), 'paint', bevel=0.35)
    p.box((-5.3, 21.0, 21.7), (5.3, 22.4, 30.3), 'dark', bevel=0.05)
    p.box((-3.6, 23.9, 23.4), (3.6, 24.3, 28.6), 'team', bevel=0.0)
    p.cyl((0, 24.0, 26.0), (0, 30.0, 26.0), 1.4, 8, 'steel')
    p.cyl((-3.6, 29.0, 26.0), (3.6, 29.0, 26.0), 0.8, 8, 'hazard')
