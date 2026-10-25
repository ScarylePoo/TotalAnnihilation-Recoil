"""Valkyrie (CORE_T1_AIR_Valkyrie) - Core air transport. A long tubby cargo fuselage with a wasp waist, a tail boom
with a tall T-tail, and FOUR lift-jet pods slung under the corners of the hull like a quadcopter. The pods hang from
the struts arm1..arm4 that pivot at the hull sides (x +-9.5) and swing out 54 deg when picking up cargo (COB turn y),
so the four pods stick out past the waist from above - a cigar with four dark lugs and a T, unlike the Arm Atlas'
three fan discs. Cargo hangs from `link` under the belly clamp.
Pieces (TA layout): base, arm1/arm3 (left rear/front pods), arm2/arm4 (right rear/front; mirrored clones of
arm1/arm3), thrust1..4 (empty jet emit points under the pods), link (empty).
Value groups from above: dark warm hull, darker paint2 pods/struts/boom, light steel pod cowl rims and cargo clamp,
team roof stripe + T-tail plane, ochre hazard nose band.
Coordinates are ENGINE/global: X right, Y up, Z forward. mirror=True builds the -X twin sharing UVs."""
import math

UNIT = dict(
    res=1024,
    wreck=dict(seed=27, drop=['arm4'], pose={'arm1': (0, 30, 0)}),
    preview_pose={},
)

PX = 10.0      # pod centre |x|: sticks out past the hull from above; the TA thrust emit (x 6.9) stays under the pod rim
PZ = 10.0      # pod centre |z|


def pod(k, name, zs):
    """lift pod + strut on piece `name` (left side, origin x -9.54); zs = +1 front pod, -1 rear pod."""
    a = k.piece(name)
    zc = PZ * zs
    x = -PX
    # strut from the hull-side pivot down to the pod
    a.hull([(-6.4, y, z) for y in (6.6, 7.8) for z in (zc * 0.4 - 1.2, zc * 0.4 + 1.2)] +
           [(x + 1.0, y, z) for y in (4.2, 5.4) for z in (zc - 1.4, zc + 1.4)], 'paint2', bevel=0.1)
    a.cyl((-6.9, 7.2, zc * 0.4), (-5.9, 7.2, zc * 0.4), 1.2, 10, 'dark', bevel=0.04)
    # pod body: short fat vertical nacelle, outer half bulged out past the waist
    a.cyl((x, 0.3, zc), (x, 4.6, zc), 3.4, 14, 'paint2', r2=3.6, bevel=0.12)
    a.cyl((x, 4.6, zc), (x, 5.3, zc), 3.6, 14, 'steel', r2=3.0, bevel=0.06)
    a.cyl((x, 5.3, zc), (x, 5.45, zc), 2.2, 14, 'black')                 # intake
    a.cyl((x, 5.45, zc), (x, 6.1, zc), 0.8, 8, 'dark')
    a.cyl((x, 0.3, zc), (x, -0.2, zc), 3.0, 14, 'dark', r2=2.2)          # nozzle
    a.cyl((x, -0.2, zc), (x, -0.3, zc), 1.8, 14, 'lightr')
    a.box((x - 3.9, 2.0, zc - 0.7), (x - 3.4, 3.4, zc + 0.7), 'lightw' if zs > 0 else 'lightr', bevel=0.0)


def build(k):
    b = k.piece('base')
    # ------------------------------------------------------------------ cargo fuselage (crosses x = 0)
    b.hull([(x * sx, y, z) for sx in (-1, 1) for x, y, z in
            [(1.2, 7.4, 27.2), (1.6, 9.8, 26.6), (3.8, 6.4, 20.0), (4.0, 12.6, 19.0),
             (6.4, 6.2, 13.0), (6.6, 15.6, 12.0), (5.4, 17.2, 10.0)]], 'paint', bevel=0.2, seg=2)
    b.hull([(x * sx, y, z) for sx in (-1, 1) for x, y, z in
            [(6.4, 6.2, 13.0), (6.6, 15.6, 12.0), (5.4, 17.2, 10.0),
             (5.2, 6.4, 0.0), (5.2, 16.0, 0.0), (4.2, 17.4, 0.0),          # wasp waist
             (6.4, 6.2, -12.0), (6.6, 15.6, -11.0), (5.4, 17.2, -9.0)]], 'paint', bevel=0.2, seg=2)
    b.hull([(x * sx, y, z) for sx in (-1, 1) for x, y, z in
            [(6.4, 6.2, -12.0), (6.6, 15.6, -11.0), (5.4, 17.2, -9.0),
             (3.0, 14.8, -19.0), (3.0, 17.6, -19.0), (2.4, 9.8, -16.0)]], 'paint', bevel=0.18)
    # tail boom
    b.hull([(x * sx, y, z) for sx in (-1, 1) for x, y, z in
            [(2.6, 15.4, -18.0), (2.6, 18.0, -18.0), (1.5, 15.9, -30.0), (1.5, 17.8, -30.0)]], 'paint2', bevel=0.12)
    # T-tail: tall fin + stabiliser
    b.hull([(x, y, z) for x in (-0.7, 0.7) for y, z in ((17.6, -21.0), (17.6, -29.6), (27.1, -26.4), (27.1, -30.6))],
           'paint2', bevel=0.08)
    b.hull([(x * sx, y, z) for sx in (-1, 1) for x, y, z in
            [(9.6, 26.9, -29.2), (9.6, 26.9, -31.4), (1.0, 26.6, -25.6), (1.0, 26.6, -30.8),
             (9.6, 27.4, -29.2), (9.6, 27.4, -31.4), (1.0, 27.6, -25.6), (1.0, 27.6, -30.8)]], 'paint', bevel=0.06)
    b.hull([(x * sx, y, z) for sx in (-1, 1) for x, y, z in
            [(8.8, 27.44, -29.4), (8.8, 27.44, -31.0), (1.6, 27.62, -26.4), (1.6, 27.62, -30.6),
             (8.8, 27.56, -29.4), (8.8, 27.56, -31.0), (1.6, 27.74, -26.4), (1.6, 27.74, -30.6)]], 'team', bevel=0.02)
    b.box((9.0, 26.9, -31.2), (9.9, 27.5, -30.0), 'lightr', bevel=0.0, mirror=True)
    # cockpit glazing
    b.hull([(x * sx, y, z) for sx in (-1, 1) for x, y, z in
            [(1.4, 10.0, 26.4), (3.6, 12.6, 20.6), (2.8, 15.0, 17.0), (1.2, 10.3, 26.3)]] +
           [(x * sx, y + 0.12, z + 0.1) for sx in (-1, 1) for x, y, z in [(3.6, 12.6, 20.6), (2.8, 15.0, 17.0)]],
           'glass', bevel=0.05)
    # ochre hazard band around the nose
    b.hull([(x * sx, y, z) for sx in (-1, 1) for x, y, z in
            [(4.1, 12.7, 19.4), (3.6, 14.4, 17.6), (5.6, 14.0, 16.0), (4.6, 15.8, 14.6)]] +
           [(x * sx, y + 0.14, z) for sx in (-1, 1) for x, y, z in
            [(4.1, 12.7, 19.4), (3.6, 14.4, 17.6), (5.6, 14.0, 16.0), (4.6, 15.8, 14.6)]], 'hazard', bevel=0.02)
    # team roof stripe along the hull
    b.hull([(x * sx, y, z) for sx in (-1, 1) for x, y, z in
            [(2.6, 17.2, 11.0), (2.6, 17.42, 0.0), (2.6, 17.2, -10.0),
             (2.6, 17.38, 11.0), (2.6, 17.58, 0.0), (2.6, 17.38, -10.0)]], 'team', bevel=0.03)
    # dorsal exhausts / vents beside the stripe
    for z in (6.0, -5.0):
        b.box((3.0, 16.6, z - 2.0), (4.4, 17.5, z + 2.0), 'dark', bevel=0.08, mirror=True)
        b.box((3.2, 17.5, z - 1.6), (4.2, 17.6, z + 1.6), 'black', bevel=0.0, mirror=True)
    # belly cargo clamp (link at 0,0,0)
    b.box((-4.4, 4.6, -7.0), (4.4, 6.4, 7.0), 'paint2', bevel=0.12)
    for z in (-6.2, 6.2):
        b.box((-3.8, 2.4, z - 0.7), (3.8, 4.7, z + 0.7), 'steel', bevel=0.08)
    b.cyl((0, 4.6, 0), (0, 3.6, 0), 1.5, 12, 'dark', bevel=0.04)
    b.box((-1.4, 6.6, 26.9), (1.4, 7.4, 27.3), 'lightw', bevel=0.0)

    # ------------------------------------------------------------------ four lift pods
    pod(k, 'arm1', -1)
    pod(k, 'arm3', +1)
    k.clone('arm2', 'arm1', mirror_x=True)
    k.clone('arm4', 'arm3', mirror_x=True)
