"""Titan (CORE_T2_AIR_Titan) - Core T2 torpedo bomber. A long narrow fuselage (58 elmo, the longest Core plane) with a
raised dark spine, light steel intake cowls along its flanks and a tall canted twin tail, sitting on a low, sharply
swept delta that carries two light-ringed lift fans (thrusta1/thrusta2). The Core tip panels (wing1/wing2) stand up
when landed and fold out 90 deg in flight (COB turn z); each carries a big torpedo on its outer face (= underside in
flight; flare1/flare2 are the launch points), whose steel body and ochre warhead poke out ahead of the panel's
leading edge - the torpedo bomber's mark from above. Where the Arm Lancet is a broad diamond, the Titan is a long
dark dart on a cranked delta.
Pieces (TA layout): base, wing1/wing2 (tip panels with torpedoes; wing1 = mirrored clone of wing2), flare1/flare2
(empty launch points), thrusta1/thrusta2 (lift fans), thrustb (tail nozzle) - empty emit points.
Value groups from above: dark warm fuselage and delta, darker paint2 spine/fins, light steel intake cowls, lift-fan
rings and torpedo noses, team on the panels' inner face (= top in flight).
Coordinates are ENGINE/global: X right, Y up, Z forward. mirror=True builds the -X twin sharing UVs."""
import math

UNIT = dict(
    res=1024,
    wreck=dict(seed=45, drop=['wing1'], pose={'wing2': (0, 0, -40)}),
    preview_pose={'wing1': (0, 0, 90.0), 'wing2': (0, 0, -90.0)},     # flight: panels folded out
)


def build(k):
    b = k.piece('base')
    # ------------------------------------------------------------------ low cranked delta (mirrored halves)
    b.hull([(4.6, 0.4, 14.0), (4.6, 2.4, 13.0), (14.7, 0.2, -7.1), (14.7, 1.5, -7.6),
            (14.7, 0.2, -28.9), (14.7, 1.5, -28.6), (4.6, 0.4, -26.0), (4.6, 2.4, -26.0)], 'paint', bevel=0.12, mirror=True)
    # lift fans in the delta (thrusta1/2 at x +-10.2, z -12)
    b.cyl((10.2, 1.2, -13.0), (10.2, 1.9, -13.0), 3.0, 18, 'steel', r2=2.8, bevel=0.06, mirror=True)
    b.cyl((10.2, 1.9, -13.0), (10.2, 1.98, -13.0), 2.1, 18, 'black', mirror=True)
    for a in (0, 60, 120):
        t = math.radians(a)
        dx, dz = math.cos(t) * 1.9, math.sin(t) * 1.9
        b.hull([(10.2 + dx * s + ox, y, -13.0 + dz * s + oz) for s in (-1, 1) for y in (1.96, 2.1)
                for ox, oz in ((-math.sin(t) * 0.3, math.cos(t) * 0.3), (math.sin(t) * 0.3, -math.cos(t) * 0.3))],
               'dark', bevel=0.0, mirror=True)
    b.cyl((10.2, 0.2, -13.0), (10.2, 0.0, -13.0), 2.2, 14, 'lightr', mirror=True)
    # panel hinge rails (wing1/2 pivot at x +-14.74, y 1.36)
    b.box((13.9, 0.2, -29.0), (14.75, 2.3, -7.0), 'paint2', bevel=0.08, mirror=True)

    # ------------------------------------------------------------------ long fuselage (crosses x = 0)
    b.hull([(x * sx, y, z) for sx in (-1, 1) for x, y, z in
            [(0.5, 6.0, 30.6), (0.5, 7.8, 29.6), (3.6, 4.6, 20.0), (3.4, 9.4, 17.0),
             (5.3, 3.0, 12.5), (5.3, 8.6, 13.4), (5.3, 1.0, -6.0), (5.3, 8.4, -18.9),
             (4.0, 1.0, -26.0), (4.0, 7.6, -26.6), (2.7, 5.4, -27.6), (1.4, 8.6, -27.6)]], 'paint', bevel=0.18)
    # raised dark spine
    b.hull([(x * sx, y, z) for sx in (-1, 1) for x, y, z in
            [(2.6, 8.9, 12.0), (2.0, 9.9, 8.0), (1.6, 12.1, -18.0), (1.6, 12.1, -27.6), (3.0, 8.6, -27.0), (3.4, 8.6, -14.0)]],
           'paint2', bevel=0.14)
    b.cyl((0, 12.2, -8.0), (0, 12.7, -8.0), 0.6, 8, 'lightr')
    # cockpit
    b.hull([(x * sx, y, z) for sx in (-1, 1) for x, y, z in
            [(1.8, 8.2, 25.0), (3.2, 9.4, 18.0), (2.4, 10.6, 12.4), (1.0, 11.1, 15.4), (1.0, 10.6, 12.0), (1.4, 8.8, 23.8)]],
           'glass', bevel=0.07)
    b.cyl((0, 6.8, 30.4), (0, 6.8, 33.0), 0.45, 8, 'dark', r2=0.15)
    # light steel intake cowls along the flanks
    b.hull([(4.6, 4.2, 12.0), (7.4, 3.8, 10.6), (4.6, 8.4, 11.0), (7.0, 7.4, 9.6),
            (4.6, 3.0, -16.0), (7.4, 2.6, -16.0), (4.6, 8.4, -17.0), (7.0, 7.2, -17.0)], 'steel', bevel=0.18, mirror=True)
    b.hull([(4.9, 4.4, 12.1), (7.2, 4.0, 10.7), (4.9, 8.0, 11.1), (6.8, 7.2, 9.7),
            (4.9, 4.4, 11.8), (7.2, 4.0, 10.4), (4.9, 8.0, 10.8), (6.8, 7.2, 9.4)], 'black', bevel=0.0, mirror=True)
    # tail nozzle (thrustb 0, 7.4, -26.8 .. -33)
    b.cyl((0, 7.4, -26.4), (0, 7.4, -29.6), 2.6, 12, 'dark', r2=2.2, bevel=0.05)
    b.cyl((0, 7.4, -29.55), (0, 7.4, -29.7), 1.6, 12, 'lightr')
    # tall canted twin tail
    b.hull([(0.8, 11.6, -18.0), (0.8, 11.4, -28.2), (3.8, 17.9, -28.0), (3.8, 17.9, -32.6),
            (1.6, 11.6, -18.0), (1.6, 11.4, -28.2), (4.6, 17.9, -28.0), (4.6, 17.9, -32.6)], 'paint2', bevel=0.07, mirror=True)
    b.box((3.7, 17.8, -32.4), (4.7, 18.2, -31.4), 'lightr', bevel=0.0, mirror=True)
    b.box((14.2, 0.4, -7.6), (14.8, 1.4, -7.0), 'lightw', bevel=0.0, mirror=True)

    # ------------------------------------------------------------------ tip panel (wing2 at +x; wing1 = mirror)
    w = k.piece('wing2'); W = w.at
    # landed: vertical; local y = span (0 at hinge, 14.7 at tip), local x 0 = inner face (top in flight)
    out = [(0.0, 11.3), (0.0, -10.5), (14.7, -9.3), (14.7, 2.0), (12.4, 3.0)]
    w.hull([W(x, y, z) for y, z in out for x in (0.05, 1.1)], 'paint', bevel=0.08)
    w.hull([W(x, y, z) for y, z in [(2.6, 8.6), (2.6, -9.8), (14.0, -8.6), (14.0, 1.4), (12.0, 2.4)]
            for x in (-0.08, 0.1)], 'team', bevel=0.03)
    w.hull([W(x, y, z) for y, z in [(0.6, -10.4), (0.6, -9.5), (14.6, -8.4), (14.6, -9.2)] for x in (-0.04, 0.1)],
           'dark', bevel=0.0)
    w.cyl(W(0.6, 14.9, 2.4), W(0.6, 14.9, -9.6), 0.55, 8, 'dark', r2=0.4)
    w.cyl(W(0.6, 14.9, 2.9), W(0.6, 14.9, 2.38), 0.35, 8, 'lightw', r2=0.55)
    w.cyl(W(0.6, -0.3, -10.4), W(0.6, -0.3, 11.0), 0.7, 8, 'dark')                 # hinge barrel
    # torpedo on the outer face (flare2 launch point at local 1.36, 5.88, 8.97)
    tx, ty = 2.4, 5.9
    w.box(W(1.0, ty - 0.4, -3.0), W(1.6, ty + 0.4, 6.0), 'dark', bevel=0.0)           # pylon
    w.cyl(W(tx, ty, -5.6), W(tx, ty, 9.6), 1.3, 12, 'steel', bevel=0.04)
    w.cyl(W(tx, ty, 9.6), W(tx, ty, 13.0), 1.3, 12, 'hazard', r2=0.45, bevel=0.03)
    w.cyl(W(tx, ty, -5.6), W(tx, ty, -7.4), 1.3, 12, 'dark', r2=0.6)
    w.box(W(tx - 1.9, ty - 0.08, -7.6), W(tx + 1.9, ty + 0.08, -6.0), 'dark', bevel=0.0)
    w.box(W(tx - 0.08, ty - 1.9, -7.6), W(tx + 0.08, ty + 1.9, -6.0), 'dark', bevel=0.0)
    k.clone('wing1', 'wing2', mirror_x=True)
