"""Torpedo Launcher (CORE_T1_SEADEF_TorpedoLauncher) - Core T1 torpedo launcher. Waterline 23 (the water surface is
model y = 23): the launcher lies submerged, as in TA. A dark X frame of four arms to heavy corner pods (team tops) on
short legs, a hub from which a broad flat twin-tube torpedo box (gun) hangs and swivels; the static 'pointer' is a
marker mast from the hub up through the surface, ending in a squat dark float with a team top and a warm beacon.
Identity from above: a dark X with four team corner squares and a broad dark box with two light steel muzzles under
the water, a small team float at the centre (the Arm T1 launcher is a light ring with one long light tube).
Pieces (COB): base, gun (turn y; origin 0, 12.25, 0; hangs below), pointer (static; same origin; the marker mast),
flare (emit, empty).
Coordinates are ENGINE/global: X right, Y up, Z forward."""
import math

WL = 23.0
UNIT = dict(
    res=1024,
    ground=False, water=WL,
    wreck=dict(seed=161, drop=['pointer']),
    preview_pose={'gun': (0, 30, 0)},
)

R = 25.0        # corner pod distance along the diagonals (x = z = R / sqrt2)


def build(k):
    b = k.piece('base')
    c = R / math.sqrt(2)
    for sz in (-1, 1):
        # arm from hub to pod (diagonal), pod, leg + foot
        b.hull([(x, y, x * sz + w * sz) for x in (4.0, c - 2.0) for y in (12.8, 16.0) for w in (-1.8, 1.8)],
               'paint', bevel=0.2, mirror=True)
        b.hull([(x, y, z * sz) for x in (c - 4.6, c + 4.6) for z in (c - 4.6, c + 4.6) for y in (10.0, 16.8)],
               'paint', bevel=0.4, mirror=True)
        b.hull([(x, y, z * sz) for x in (c - 3.4, c + 3.4) for z in (c - 3.4, c + 3.4) for y in (16.75, 17.0)],
               'team', bevel=0.0, mirror=True)
        b.hull([(x, y, z * sz) for x in (c - 2.2, c + 2.2) for z in (c - 2.2, c + 2.2) for y in (0.0, 10.2)]
               + [(x, 0.0, z * sz) for x in (c - 3.6, c + 3.6) for z in (c - 3.6, c + 3.6)], 'paint2', bevel=0.2,
               mirror=True)
        b.box((c + 4.55, 12.0, c * sz - 0.8), (c + 4.85, 12.8, c * sz + 0.8), 'lightr', bevel=0.0, mirror=True)
    b.cyl((0, 12.6, 0), (0, 16.6, 0), 6.0, 8, 'paint2', rot=math.pi / 8, bevel=0.2)

    # ---------------------------------------------------------------- pointer: marker mast + float (static)
    p = k.piece('pointer')
    p.cyl((0, 16.4, 0), (0, 21.2, 0), 1.8, 8, 'steel')
    p.cyl((0, 20.6, 0), (0, 25.4, 0), 5.0, 8, 'paint', r2=4.4, rot=math.pi / 8, bevel=0.3)
    p.cyl((0, 22.4, 0), (0, 23.4, 0), 5.2, 8, 'dark', rot=math.pi / 8)
    p.cyl((0, 25.3, 0), (0, 25.6, 0), 3.6, 8, 'team', rot=math.pi / 8)
    p.cyl((0, 25.5, 0), (0, 27.0, 0), 1.0, 8, 'lightr')

    # ---------------------------------------------------------------- gun: torpedo box (origin 0, 12.25, 0)
    g = k.piece('gun'); G = g.at
    g.cyl(G(0, -3.0, 0), G(0, 0.3, 0), 4.0, 10, 'dark', bevel=0.08)
    g.hull([G(x, y, z) for x in (-9.6, 9.6) for y in (-11.6, -3.4) for z in (-12.6, 11.0)]
           + [G(x, y, 14.6) for x in (-8.6, 8.6) for y in (-11.0, -5.0)]
           + [G(x, -2.4, z) for x in (-7.0, 7.0) for z in (-10.0, 8.0)], 'paint', bevel=0.4)
    g.hull([G(x, y, z) for x in (-5.4, 5.4) for y in (-2.45, -2.2) for z in (-8.0, 5.0)], 'paint2', bevel=0.0)
    for sx in (-1, 1):
        g.cyl(G(4.6 * sx, -11.0, 13.0), G(4.6 * sx, -11.0, 16.0), 2.6, 10, 'steel', bevel=0.05)
        g.cyl(G(4.6 * sx, -11.0, 15.9), G(4.6 * sx, -11.0, 16.2), 1.9, 10, 'black')
    g.box(G(-9.8, -9.0, -13.0), G(9.8, -6.0, -12.4), 'black', bevel=0.0)
