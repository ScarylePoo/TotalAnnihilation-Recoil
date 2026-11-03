"""Hurricane (CORE_T2_AIR_Hurricane) - Core T2 heavy bomber. A flying slab: a 31-elmo wide, flat armoured centre
wing with three engine housings across its trailing edge, a blocky raised fuselage with a long beak, a retractable
ventral twin-gun turret (turret turns y and moves y, barrels turn x) and a dorsal V-tail. The huge Core tip panels
(wing1/wing2, 16 x 31 elmo) stand up when landed and fold out 90 deg in flight, making a broad 62 x 55 elmo rectangle
from above - squarer and heavier than the T1 Shadow's trapezoid. Two tail plates (tail1/tail2) rise 30 deg in flight.
Deliberate departure from the 3DO (user report: gun on top and tail below looked upside down; the 3DO had turret y +5.59,
tail y +0.11, tails dropping): skeleton_opts moves the origins. The turret's rest position is RETRACTED, wholly inside
the fuselage, because aircraft sit with y = 0 on the ground; the script lowers it GUN_DROP elmos once airborne.
Pieces: base (bombs empty), wing1/wing2 (tip panels; wing1 = mirrored clone of wing2), tail1/tail2 (dorsal plates; tail1
= mirrored clone), turret > barrels > flare1/flare2 (empty gun points, emit dir +z along the barrels), thrusta1/thrusta2
(empty lift-jet emits).
Value groups from above: dark warm armour, darker paint2 engine housings and fuselage spine, light steel tail plates and
slab leading-edge intakes (light bars on dark), team on the outer half of the tip panels' inner face (= top in flight)
+ the dorsal spine fairing + the tail plates.
Coordinates are ENGINE/global: X right, Y up, Z forward. mirror=True builds the -X twin sharing UVs."""
import math

GUN_DROP = 6.0      # scripts/CORE_T2_AIR_Hurricane.lua lowers the turret by this much in flight
TAIL_RISE = 30.23

UNIT = dict(
    res=1024,
    skeleton_opts=dict(
        move={'turret': (0.0, 5.4, -19.0), 'barrels': (0.0, 2.0, -18.4),
              'tail1': (-3.2, 7.9, -19.85), 'tail2': (3.2, 7.9, -19.85)},
        emit={'flare1': [(0, 0, 0), (0, 0, 1)], 'flare2': [(0, 0, 0), (0, 0, 1)]}),
    # crash: one tip panel and the belly turret torn off (`drop` lays them on the ground by the hull), the other panel bent, tail crumpled
    wreck=dict(seed=37, drop=['wing1', 'turret'], pose={'wing2': (0, 0, -50), 'tail2': (0, 0, 18), 'tail1': (0, 0, -55)}),
    # flight state, lifted off the preview ground so the belly gun shows
    preview_pose={'base': {'move': (0, 16.0, 0)}, 'wing1': (0, 0, 90.0), 'wing2': (0, 0, -90.0),
                  'tail1': (0, 0, -TAIL_RISE), 'tail2': (0, 0, TAIL_RISE),
                  'turret': {'move': (0, -GUN_DROP, 0), 'rot': (0, -25, 0)}, 'barrels': (25, 0, 0)},
)


def build(k):
    b = k.piece('base')
    # ------------------------------------------------------------------ flat centre slab (mirrored halves)
    b.hull([(4.0, 3.2, 14.2), (11.4, 3.2, 13.5), (15.5, 3.3, 5.6), (15.5, 3.3, -26.2), (4.0, 3.2, -26.4),
            (4.0, 5.6, 14.0), (11.4, 4.9, 13.3), (15.5, 5.55, 5.3), (15.5, 5.55, -26.2), (4.0, 5.9, -26.4)],
           'paint', bevel=0.14, mirror=True)
    # light steel intake lip along the slab's swept leading edge
    b.hull([(5.0, 4.4, 14.6), (11.6, 4.0, 13.9), (14.4, 4.2, 8.4), (5.0, 5.7, 14.0), (11.4, 5.1, 13.2), (14.2, 5.6, 7.8),
            (5.0, 4.0, 12.0), (11.0, 4.0, 11.4)], 'steel', bevel=0.12, mirror=True)
    b.hull([(5.4, 4.5, 14.75), (11.4, 4.1, 14.05), (5.4, 5.3, 14.45), (11.3, 4.8, 13.75),
            (5.4, 4.5, 14.45), (11.4, 4.1, 13.75), (5.4, 5.3, 14.15), (11.3, 4.8, 13.45)], 'black', bevel=0.0, mirror=True)
    # engine housing on each slab half + exhaust (dark paint2 blocks across the trailing edge)
    b.hull([(x, y, z) for x in (7.4, 13.6) for y, z in ((5.4, -6.0), (7.4, -9.0), (5.4, -27.4), (7.4, -26.6))],
           'paint2', bevel=0.2, mirror=True)
    b.box((8.4, 7.38, -22.0), (12.6, 7.5, -12.0), 'dark', bevel=0.0, mirror=True)
    b.cyl((10.5, 6.2, -26.8), (10.5, 6.2, -28.6), 1.9, 12, 'dark', r2=1.6, bevel=0.04, mirror=True)
    b.cyl((10.5, 6.2, -28.55), (10.5, 6.2, -28.7), 1.2, 12, 'lightr', mirror=True)
    # tip hinge blocks (wing pivots at x +-15.48, y 5.53)
    b.box((14.6, 3.2, -26.4), (15.5, 5.9, 5.6), 'paint2', bevel=0.1, mirror=True)
    # lift-jet grilles under the slab (thrusta at x +-4.3, z -6.4)
    b.cyl((5.6, 3.3, -6.4), (5.6, 3.0, -6.4), 1.6, 12, 'dark', mirror=True)
    b.cyl((5.6, 3.02, -6.4), (5.6, 2.92, -6.4), 1.1, 12, 'lightr', mirror=True)

    # ------------------------------------------------------------------ blocky fuselage + beak (crosses x = 0)
    b.hull([(x * sx, y, z) for sx in (-1, 1) for x, y, z in
            [(0.6, 0.9, 28.6), (1.0, 2.8, 27.4), (4.2, 0.2, 16.1), (4.2, 5.6, 16.1),
             (4.4, 0.2, -26.9), (4.4, 6.2, -26.9), (5.0, 0.6, 8.0), (5.0, 6.0, -20.0)]], 'paint', bevel=0.18)
    b.hull([(x * sx, y, z) for sx in (-1, 1) for x, y, z in
            [(3.4, 5.5, 14.4), (5.4, 5.6, 8.6), (5.4, 7.8, 7.6), (3.2, 8.2, 0.0), (5.0, 7.4, -1.0),
             (2.6, 7.6, -8.0), (4.4, 6.2, -9.0), (4.4, 5.8, -26.0), (2.8, 6.4, -26.0)]], 'paint2', bevel=0.16)
    # cockpit
    b.hull([(x * sx, y, z) for sx in (-1, 1) for x, y, z in
            [(1.6, 4.0, 22.6), (3.2, 5.7, 16.6), (2.6, 7.4, 12.2), (1.2, 7.9, 13.4), (2.0, 5.2, 20.6)]], 'glass', bevel=0.07)
    b.cyl((0, 1.9, 28.4), (0, 1.9, 31.0), 0.5, 8, 'dark', r2=0.18)
    # centre exhaust
    b.cyl((0, 3.4, -26.6), (0, 3.4, -28.8), 2.4, 12, 'dark', r2=2.0, bevel=0.05)
    b.cyl((0, 3.4, -28.75), (0, 3.4, -28.9), 1.5, 12, 'lightr')
    # bomb bay (bombs at 0, 0, 0)
    b.box((-3.2, -0.05, -14.0), (3.2, 0.3, 8.0), 'black', bevel=0.05)
    # lights
    b.box((-1.0, 8.15, 1.8), (1.0, 8.5, 3.2), 'lightr', bevel=0.0)
    b.box((15.0, 4.0, 5.4), (15.6, 4.9, 6.0), 'lightw', bevel=0.0, mirror=True)

    # ------------------------------------------------------------------ dorsal spine fairing carrying the V-tail hinges
    b.hull([(x * sx, y, z) for sx in (-1, 1) for x, y, z in
            [(2.2, 6.4, -8.0), (3.6, 6.2, -12.0), (2.6, 8.2, -12.0), (3.6, 6.2, -27.0), (2.8, 8.4, -26.0), (1.8, 7.0, -28.2)]],
           'paint', bevel=0.14)
    b.hull([(x * sx, y, z) for sx in (-1, 1) for x, y, z in
            [(1.9, 8.3, -13.0), (1.9, 8.5, -25.4), (1.9, 8.42, -13.0), (1.9, 8.62, -25.4)]], 'team', bevel=0.02)
    b.box((-0.5, 8.35, -11.8), (0.5, 8.8, -10.8), 'lightr', bevel=0.0)
    # gun bay under the fuselage: the turret and barrels retract through this into the fuselage
    b.cyl((0, 0.3, -19.0), (0, 0.1, -19.0), 4.3, 16, 'black')

    # ------------------------------------------------------------------ ventral turret, retracted at rest
    # origin (0, 5.4, -19): everything fits in the fuselage (|x| < 4.4, y > 0.2); -GUN_DROP in flight
    t = k.piece('turret'); T = t.at
    t.cyl(T(0, 1.3, 0), T(0, -0.3, 0), 2.6, 12, 'dark', bevel=0.05)                # neck through the belly
    t.cyl(T(0, -0.2, 0), T(0, -1.5, 0), 4.0, 16, 'paint2', r2=3.8, bevel=0.1)      # bearing ring
    for sx in (-1, 1):                                                              # cheeks either side of the barrels
        t.hull([T(x * sx, y, z) for x in (2.75, 3.75) for y, z in
                [(-1.4, 3.0), (-1.4, -3.2), (-4.6, 1.8), (-4.6, -1.8), (-5.1, 0.6), (-5.1, -0.8)]], 'steel', bevel=0.12)
    t.box(T(-3.0, -1.5, -3.2), T(3.0, -2.2, -1.9), 'dark', bevel=0.05)              # rear bridge, clear of the swinging breech
    # barrels (origin = turret + (0, -3.4, 0.6)); flare1/2 at x +-1.74, z 9.24; swing freely down between the cheeks
    g = k.piece('barrels'); G = g.at
    g.cyl(G(-2.7, 0, 0.1), G(2.7, 0, 0.1), 1.45, 12, 'dark', bevel=0.08)            # trunnion drum
    for dx in (-1.74, 1.74):
        g.cyl(G(dx, 0, 1.2), G(dx, 0, 9.2), 0.52, 8, 'steel', rot=math.pi / 8)
        g.cyl(G(dx, 0, 8.2), G(dx, 0, 9.4), 0.7, 8, 'dark', rot=math.pi / 8)

    # ------------------------------------------------------------------ tip panel (wing2 at +x; wing1 = mirror)
    w = k.piece('wing2'); W = w.at
    # landed: vertical; local y = span (0 at hinge, 15.7 at tip), local z = chord; local x 0 = inner face (top in flight)
    out = [(0.0, 15.6), (0.0, -15.9), (15.7, -14.9), (15.7, 0.6), (12.5, 3.7)]
    w.hull([W(x, y, z) for y, z in out for x in (0.05, 1.6)], 'paint', bevel=0.08)
    w.hull([W(x, y, z) for y, z in [(4.2, 9.4), (4.2, -14.2), (15.0, -13.6), (15.0, 0.2), (12.4, 2.7)]
            for x in (-0.08, 0.1)], 'team', bevel=0.03)
    # dark spar strips on the inner face (break the panel into a heavy ribbed plate)
    for y in (2.6,):
        w.box(W(-0.04, y - 0.5, -15.0), W(0.1, y + 0.5, 13.0 - y * 0.2), 'paint2', bevel=0.0)
    w.hull([W(x, y, z) for y, z in [(0.6, -14.9), (0.6, -15.8), (15.6, -14.8), (15.6, -14.0)] for x in (-0.04, 0.1)],
           'dark', bevel=0.0)                                  # trailing-edge strip
    w.cyl(W(0.8, 15.9, 0.8), W(0.8, 15.9, -15.0), 0.6, 8, 'dark', r2=0.45)
    w.cyl(W(0.8, 15.9, 1.3), W(0.8, 15.9, 0.78), 0.38, 8, 'lightw', r2=0.6)
    w.cyl(W(0.8, -0.3, -15.6), W(0.8, -0.3, 15.0), 0.8, 8, 'dark')              # hinge barrel
    k.clone('wing1', 'wing2', mirror_x=True)

    # ------------------------------------------------------------------ dorsal V-tail plates (tail2 at +x)
    # flat at rest, clear above the engine housings (top y 7.5); rise TAIL_RISE deg from the hinge in flight
    v = k.piece('tail2'); V = v.at
    out = ((0.0, 9.1), (7.5, -3.8), (7.5, -10.2), (0.0, -7.0))
    v.hull([V(x, y, z) for x, z in out for y in (-0.35, 0.35)], 'steel', bevel=0.06)
    v.hull([V(x, y, z) for x, z in ((1.0, 5.0), (6.9, -4.6), (6.9, -9.2), (1.0, -5.6)) for y in (0.3, 0.45)], 'team', bevel=0.02)
    v.box(V(6.9, -0.4, -10.0), V(7.6, 0.4, -9.0), 'lightr', bevel=0.0)
    v.cyl(V(0.0, 0, 8.0), V(0.0, 0, -6.0), 0.6, 8, 'dark')                          # hinge barrel
    k.clone('tail1', 'tail2', mirror_x=True)
