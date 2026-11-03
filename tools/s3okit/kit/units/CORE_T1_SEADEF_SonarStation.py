"""Sonar Station (CORE_T1_SEADEF_SonarStation) - Core sonar buoy. Waterline 37 (the water surface is model y = 37;
the TA model lay entirely under it). A dark three-legged anchor on the sea bed, a tall dark column up through the
surface ending in a squat dark float (3 elmo freeboard) with a team top and a warm beacon; round the column, 10 elmo
under the water, the dish: a spinning bar carrying two big light steel hydrophone pods with team stripes (the TA
'twin pod' array).
Identity from above: a small dark float with a team cap over a long bar with two light pods under the water (the Arm
sonar is a light float disc with a paddle rotor above the water).
Pieces (COB): base, dish (spin y; origin 0, 18.5, 0).
Coordinates are ENGINE/global: X right, Y up, Z forward."""
import math

WL = 37.0
UNIT = dict(
    res=1024,
    ground=False, water=WL,
    wreck=dict(seed=171, drop=['dish']),
    preview_pose={'dish': (0, 35, 0)},
)


def build(k):
    b = k.piece('base')
    for a in (90, 210, 330):
        c, s = math.cos(math.radians(a)), math.sin(math.radians(a))
        R = lambda r, w, y: (c * r - s * w, y, s * r + c * w)
        b.hull([R(r, w, y) for r, y in ((3.0, 14.0), (5.0, 14.0)) for w in (-1.8, 1.8)]
               + [R(r, w, y) for r, y in ((11.0, 1.5), (14.0, 1.5)) for w in (-2.4, 2.4)], 'paint', bevel=0.15)
        b.hull([R(r, w, y) for r in (9.5, 15.5) for w in (-3.4, 3.4) for y in (0.0, 1.8)], 'paint2', bevel=0.1)
    b.cyl((0, 0.0, 0), (0, 36.0, 0), 3.6, 8, 'paint2', r2=3.0, rot=math.pi / 8, bevel=0.1)
    b.cyl((0, 10.0, 0), (0, 16.0, 0), 5.6, 8, 'paint', rot=math.pi / 8, bevel=0.15)
    # float
    b.cyl((0, 33.0, 0), (0, 40.0, 0), 6.4, 8, 'paint', r2=5.8, rot=math.pi / 8, bevel=0.3)
    b.cyl((0, 36.4, 0), (0, 37.6, 0), 6.65, 8, 'dark', rot=math.pi / 8)
    b.cyl((0, 39.9, 0), (0, 40.2, 0), 4.6, 8, 'team', rot=math.pi / 8)
    b.cyl((0, 40.1, 0), (0, 41.8, 0), 1.2, 8, 'steel')
    b.cyl((0, 41.7, 0), (0, 42.8, 0), 1.5, 8, 'lightr')
    b.cyl((0, 28.0, 0), (0, 33.2, 0), 2.6, 8, 'paint2', r2=5.0, rot=math.pi / 8)

    # ---------------------------------------------------------------- dish: spinning twin-pod array
    d = k.piece('dish'); D = d.at
    d.cyl(D(0, 6.0, 0), D(0, 10.6, 0), 5.4, 8, 'paint', rot=math.pi / 8, bevel=0.2)
    d.hull([D(x, y, z) for x in (4.0, 11.0) for y in (7.2, 9.6) for z in (-2.0, 2.0)], 'paint2', bevel=0.15,
           mirror=True)
    d.cyl(D(12.6, 8.4, -8.0), D(12.6, 8.4, 7.0), 3.6, 10, 'steel', bevel=0.1, mirror=True)
    d.cyl(D(12.6, 8.4, 7.0), D(12.6, 8.4, 10.0), 3.6, 10, 'steel', r2=1.2, mirror=True)
    d.cyl(D(12.6, 8.4, -11.0), D(12.6, 8.4, -8.0), 1.6, 10, 'dark', r2=3.6, mirror=True)
    d.hull([D(x, y, z) for x in (11.4, 13.8) for y in (11.78, 12.02) for z in (-6.0, 5.0)], 'team', bevel=0.0,
           mirror=True)
    d.cyl(D(12.6, 8.4, -2.0), D(12.6, 8.4, -0.6), 3.85, 10, 'dark', mirror=True)
