"""Advanced Construction Aircraft (ARM_T2_AIR_AdvancedConstructor) - Arm T2 air builder. The T1 flying van grown into
a heavy flying workshop: a bigger boxy hull with a hazard-banded glazed nose, a dorsal equipment deck, twin tail fins,
and FOUR ducted lift fans in corner pods (dark discs round the light hull from above - the T1 has none). The stub
wings live inside a glove slab under the hull and slide out 14 elmo on take-off (COB move x; wing1 sits at +x when
stowed and slides to the LEFT), so the flying plan is a fat cross with four fans. A hazard-striped nano turret sits
on the right rear pod, aimed at the build-beam origin (base's first vertex, the rear-right corner, as in TA).
Pieces (TA layout): base, wing1/wing2 (sliding wings; wing1 = mirrored clone of wing2).
Value groups from above: light Arm hull and wings, dark paint2 fan pods + deck, black fan wells, team on the wing tips,
the deck centre and the fin tops; yellow hazard on the nose band and the nano turret.
Coordinates are ENGINE/global: X right, Y up, Z forward. mirror=True builds the -X twin sharing UVs."""
import math

UNIT = dict(
    res=1024,
    wreck=dict(seed=55, remove=['wing1']),
    always_visible=['wing1', 'wing2'],
    # flight pose: wings slid out (engine x = -COB x)
    preview_pose={'wing1': {'move': (-14.0, 0, 0)}, 'wing2': {'move': (14.125, 0, 0)}},
)


def fan(b, x, z, r, y0, y1, team=False):
    """ducted lift fan pod (mirrored), team-free: dark cowl, black well, three dark blades, cyan downwash."""
    b.cyl((x, y0, z), (x, y1, z), r, 18, 'paint2', r2=r * 1.05, bevel=0.14, mirror=True)
    b.cyl((x, y1, z), (x, y1 + 0.1, z), r * 0.76, 18, 'black', mirror=True)
    if team:
        b.cyl((x, y1 - 0.05, z), (x, y1 + 0.12, z), r * 1.02, 18, 'team', r2=r * 0.9, mirror=True)   # team rim
    for a in (15, 75, 135):
        t = math.radians(a)
        dx, dz = math.cos(t) * r * 0.72, math.sin(t) * r * 0.72
        b.hull([(x + dx * s + ox, y1 + dy, z + dz * s + oz) for s in (-1, 1) for dy in (0.0, 0.16)
                for ox, oz in ((-math.sin(t) * 0.42, math.cos(t) * 0.42), (math.sin(t) * 0.42, -math.cos(t) * 0.42))],
               'dark', bevel=0.0, mirror=True)
    b.cyl((x, y1 - 0.2, z), (x, y1 + 0.6, z), r * 0.2, 10, 'dark', r2=r * 0.12, mirror=True)
    b.cyl((x, y0 - 0.1, z), (x, y0, z), r * 0.8, 16, 'lightc', mirror=True)


def build(k):
    b = k.piece('base')
    # ------------------------------------------------------------------ glove slab (the wings stow inside it)
    b.hull([(x * sx, y, z) for sx in (-1, 1) for x, y, z in
            [(9.4, 0.4, 9.0), (9.4, 2.2, 8.5), (9.4, 0.4, -7.0), (9.4, 2.2, -6.6)]], 'paint2', bevel=0.12)
    # ------------------------------------------------------------------ big box hull (crosses x = 0)
    b.hull([(x * sx, y, z) for sx in (-1, 1) for x, y, z in
            [(6.4, 1.6, 17.0), (7.4, 1.6, 10.0), (7.6, 1.6, -14.0), (5.4, 3.0, -24.0),
             (6.0, 9.6, 16.4), (7.0, 10.6, 10.0), (7.0, 10.8, -14.0), (5.0, 10.0, -24.0),
             (4.4, 3.4, 23.6), (4.2, 7.8, 23.0)]], 'paint', bevel=0.22, seg=2)
    # blunt glazed nose + hazard band (construction tell)
    b.hull([(x * sx, y, z) for sx in (-1, 1) for x, y, z in
            [(2.8, 7.8, 22.7), (3.8, 9.6, 18.6), (2.8, 10.6, 16.2)]] +
           [(x * sx, y + 0.14, z + 0.12) for sx in (-1, 1) for x, y, z in
            [(2.8, 7.8, 22.7), (3.8, 9.6, 18.6), (2.8, 10.6, 16.2)]], 'glass', bevel=0.05)
    b.hull([(x * sx, y, z) for sx in (-1, 1) for x, y, z in
            [(4.4, 7.0, 23.2), (5.2, 8.8, 21.0)]] +
           [(x * sx, y + 0.14, z + 0.12) for sx in (-1, 1) for x, y, z in
            [(4.4, 7.0, 23.2), (5.2, 8.8, 21.0)]], 'hazard', bevel=0.02)
    b.box((-2.4, 2.8, 23.6), (2.4, 3.6, 23.9), 'lightw', bevel=0.0)
    # dorsal equipment deck: dark raised block, team centre panel, vents, a little crane boom
    b.hull([(x * sx, y, z) for sx in (-1, 1) for x, y, z in
            [(5.8, 10.6, 12.0), (5.8, 10.8, -16.0), (5.0, 13.0, 10.6), (5.0, 13.0, -15.0)]], 'paint2', bevel=0.14)
    b.hull([(x * sx, y, z) for sx in (-1, 1) for x, y, z in
            [(4.2, 12.98, 9.6), (4.2, 12.98, -4.4), (4.2, 13.14, 9.6), (4.2, 13.14, -4.4)]], 'team', bevel=0.03)
    for z in (-6.4, -8.6, -10.8):
        b.box((-4.0, 13.0, z - 0.5), (4.0, 13.15, z + 0.5), 'black', bevel=0.0)
    b.cyl((3.4, 13.0, -13.4), (3.4, 14.6, -13.4), 0.9, 10, 'dark', bevel=0.03)
    b.cyl((3.4, 14.4, -13.4), (-3.0, 15.6, -6.0), 0.4, 6, 'steel')                       # crane boom
    b.cyl((-3.0, 15.6, -6.0), (-3.0, 14.2, -6.0), 0.12, 4, 'dark')
    b.cyl((-3.6, 13.0, -14.4), (-3.6, 13.6, -14.4), 0.5, 8, 'lightr')
    # twin tail fins with team tops
    b.hull([(2.6, 10.0, -14.0), (2.8, 9.6, -24.0), (4.2, 15.4, -21.0), (3.8, 15.4, -26.0),
            (3.6, 10.0, -14.0), (3.8, 9.6, -24.0), (5.0, 15.4, -21.0), (4.6, 15.4, -26.0)], 'paint', bevel=0.07, mirror=True)
    b.hull([(x, y, z) for x, y, z in [(3.9, 13.6, -19.4), (4.2, 15.4, -21.0), (3.8, 15.4, -26.0), (3.6, 13.6, -25.4)]] +
           [(x + 1.15, y, z) for x, y, z in [(3.9, 13.6, -19.4), (4.2, 15.4, -21.0), (3.8, 15.4, -26.0), (3.6, 13.6, -25.4)]],
           'team', bevel=0.0, mirror=True)
    b.box((3.7, 15.3, -25.8), (4.7, 15.7, -24.8), 'lightr', bevel=0.0, mirror=True)
    # four ducted lift fans in corner pods, on short spars
    for z in (14.0, -15.0):
        b.box((6.6, 4.0, z - 1.2), (9.0, 6.0, z + 1.2), 'dark', bevel=0.1, mirror=True)
        fan(b, 12.0, z, 4.0, 2.6, 7.4, team=z > 0)
    # rear engines
    for x in (-2.8, 2.8):
        b.cyl((x, 6.4, -23.4), (x, 6.4, -25.4), 1.8, 12, 'dark', r2=1.5, bevel=0.04)
        b.cyl((x, 6.4, -25.35), (x, 6.4, -25.5), 1.1, 12, 'lightc')
    b.box((7.4, 4.0, 2.0), (7.9, 8.4, 7.0), 'black', bevel=0.0, mirror=True)               # side intakes
    # nano turret on the right rear pod spar, aimed back-right at the build-beam origin (23, 0, -24)
    b.cyl((12.0, 7.4, -15.0), (12.0, 8.6, -15.0), 1.9, 12, 'dark', bevel=0.06)
    b.cyl((12.0, 8.4, -15.0), (14.4, 7.4, -18.0), 1.25, 10, 'hazard', r2=1.05, bevel=0.04)
    b.cyl((14.4, 7.4, -18.0), (15.6, 6.9, -19.6), 1.0, 10, 'dark', r2=0.65)
    b.cyl((15.6, 6.9, -19.6), (15.8, 6.8, -19.9), 0.6, 10, 'lightc')

    # ------------------------------------------------------------------ wing2 (origin -5.12, 1.25, 1.25; slides +14.1)
    w = k.piece('wing2'); W = w.at
    pts = []
    for x, zl, zt, t in ((0.4, 7.1, -7.5, 0.5), (14.6, 1.8, -3.6, 0.3)):
        for z, tt in ((zl, 0.12), (zl - 1.4, t), (zt + 0.9, t * 0.8), (zt, 0.08)):
            pts += [W(x, tt, z), W(x, -tt, z)]
    w.hull(pts, 'paint', bevel=0.05)
    w.hull([W(x, dy + d, z) for x, dy, zs in ((8.0, 0.44, (3.8, -5.4)), (14.0, 0.34, (1.3, -3.1)))
            for z in zs for d in (0.0, 0.1)], 'team', bevel=0.02)
    w.cyl(W(14.6, 0, 1.6), W(14.6, 0, -4.0), 0.5, 8, 'dark', r2=0.4)
    w.cyl(W(14.6, 0, 2.0), W(14.6, 0, 1.58), 0.3, 8, 'lightw', r2=0.5)
    k.clone('wing1', 'wing2', mirror_x=True)
