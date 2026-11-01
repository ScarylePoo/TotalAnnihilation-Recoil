"""Solar Collector (CORE_T1_ECO_SolarCollector) - Core solar. A low dark truncated pyramid (the shell) on a square pad,
its roof covered by four stacked armoured wing plates. Switched on, four corner buttresses slide out along the
diagonals, the shell rises 10.25 elmo on them and the wings flip over 229 deg to lie on the four sloped sides,
showing their warm-glass solar cells.
Identity from above (open): a square ring of four dark cell trapezoids round a team-coloured roof square, light
steel buttress tips poking out of the corners (the Arm solar is a far-reaching star of four flat petals).
Pieces (COB): base (pad), shell (move y 10.25), wing1..4 (wing1/2 turn z, wing3/4 turn x + move y 0.75),
leg1..4 (move x/z ~11 outward). The kit's walker heuristic flags leg1..4 - they are buttresses, no skeleton.
Preview: OPEN (activatescr end state; COB z turns and x moves negated for the engine frame).
Coordinates are ENGINE/global: X right, Y up, Z forward."""
import math

OPEN = 229.25
UNIT = dict(
    wreck=dict(seed=14, pose={'wing1': (0, 0, 120), 'wing3': (-60, 0, 0)}, drop=['wing2']),
    preview_pose={
        'shell': {'move': (0, 10.25, 0)},
        'wing1': (0, 0, OPEN), 'wing2': (0, 0, -OPEN),
        'wing3': {'move': (0, 0.75, 0), 'rot': (-OPEN, 0, 0)}, 'wing4': {'move': (0, 0.75, 0), 'rot': (OPEN, 0, 0)},
        'leg1': {'move': (-11.125, 0, 11.25)}, 'leg2': {'move': (11.375, 0, 11.25)},
        'leg3': {'move': (10.875, 0, -11.125)}, 'leg4': {'move': (-11.0, 0, -11.0)},
    },
)

R2 = math.sqrt(0.5)
HB, HT, HS = 24.8, 14.32, 12.3      # shell frustum: bottom half-size, top half-size, height (shell-relative)


def build(k):
    # ------------------------------------------------------------------ base: dark pad with buttress slots
    b = k.piece('base')
    b.plan(0.0, 0.7, [(-34.0, -34.0), (34.0, -34.0), (34.0, 34.0), (-34.0, 34.0)], 'paint2', bevel=0.2, top_inset=0.5)
    for sz in (-1, 1):       # slots along the -x diagonals (mirrored to +x)
        pts = []
        for u in (22.0, 45.0):
            for v in (-3.4, 3.4):
                x, z = -u * R2 + v * R2, sz * (u * R2 + v * R2)
                for y in (0.6, 0.78):
                    pts.append((x, y, z))
        b.hull(pts, 'dark', bevel=0.0, mirror=True)
    b.box((-8.0, 0.6, 33.0), (8.0, 0.9, 33.9), 'hazard', bevel=0.0)
    b.box((-1.2, 0.6, -33.9), (1.2, 1.4, -33.6), 'lightr', bevel=0.0)

    # ------------------------------------------------------------------ shell: truncated pyramid (origin y 0.22)
    s = k.piece('shell'); S = s.at
    s.plan(S(0, 0, 0)[1], S(0, HS, 0)[1], [(-HB, -HB), (HB, -HB), (HB, HB), (-HB, HB)], 'paint', bevel=0.3,
           top_inset=(HB - HT) * math.sqrt(2))   # plan insets the corners
    # team roof deck with a dark centre vent and four dark hinge rails under the wing hinges
    s.box(S(-12.6, HS - 0.2, -12.6), S(12.6, HS + 0.06, 12.6), 'team', bevel=0.0)
    s.cyl(S(0, HS - 0.1, 0), S(0, HS + 0.1, 0), 4.4, 8, 'dark', rot=math.pi / 8)
    s.cyl(S(0, HS + 0.08, 0), S(0, HS + 0.13, 0), 2.4, 8, 'lightc', rot=math.pi / 8)
    s.box(S(-14.3, HS - 0.3, -14.3), S(-12.6, HS + 0.08, 14.3), 'dark', bevel=0.05, mirror=True)
    s.box(S(-12.6, HS - 0.3, -14.3), S(12.6, HS + 0.08, -12.6), 'dark', bevel=0.05)
    s.box(S(-12.6, HS - 0.3, 12.6), S(12.6, HS + 0.08, 14.3), 'dark', bevel=0.05)
    # side vents low on each face (visible in both states below the wings)
    for sx in (-1, 1):
        s.hull([S(sx * (HB - 0.6 * 0.852 - d), 0.6 + d * 0, z) for z in (-7.0, 7.0) for d in (0.05, 0.3)] +
               [S(sx * (HB - 1.6 * 0.852 - d), 1.6, z) for z in (-7.0, 7.0) for d in (0.05, 0.3)], 'black', bevel=0.0)
    for sz in (-1, 1):
        s.hull([S(x, 0.6, sz * (HB - 0.6 * 0.852 - d)) for x in (-7.0, 7.0) for d in (0.05, 0.3)] +
               [S(x, 1.6, sz * (HB - 1.6 * 0.852 - d)) for x in (-7.0, 7.0) for d in (0.05, 0.3)], 'black', bevel=0.0)

    # ------------------------------------------------------------------ wings: geometry ABOVE the hinge axis; the
    # bottom face carries the cells (it faces outward-up once flipped 229 deg onto the sloped sides)
    def wing(name, axis, ribs=False):
        w = k.piece(name); W = w.at
        o = k.P[name]
        inward = 1.0 if (o[0] if axis == 'x' else o[2]) < 0 else -1.0

        def pt(a, l, y):           # a = along the hinge, l = inward from the hinge
            return W(inward * l, y, a) if axis == 'x' else W(a, y, inward * l)
        w.hull([pt(a, l, y) for a in (-14.4, 14.4) for l in (0.2, 14.4) for y in (0.22, 0.62)], 'paint', bevel=0.12)
        w.hull([pt(a, l, y) for a in (-13.0, 13.0) for l in (1.4, 12.2) for y in (0.06, 0.24)], 'glass', bevel=0.0)
        for a0 in (-4.6, 4.2):     # dark cell dividers
            w.hull([pt(a, l, y) for a in (a0, a0 + 0.5) for l in (1.4, 12.0) for y in (0.0, 0.1)], 'dark', bevel=0.0)
        w.hull([pt(a, l, y) for a in (-14.4, 14.4) for l in (12.0, 14.4) for y in (0.0, 0.24)], 'team', bevel=0.0)
        # armoured back: dark ribs (the closed roof)
        for l0 in ((4.0, 9.0) if ribs else ()):
            w.hull([pt(a, l, y) for a in (-12.0, 12.0) for l in (l0, l0 + 1.2) for y in (0.6, 0.86)], 'paint2', bevel=0.05)
        return w
    wing('wing1', 'x', ribs=True)
    k.clone('wing2', 'wing1', mirror_x=True)
    wing('wing3', 'z')
    wing('wing4', 'z')

    # ------------------------------------------------------------------ legs: corner buttresses (diagonal beams)
    def leg(name, sx, sz):
        g = k.piece(name)
        dx, dz = sx * R2, sz * R2
        px, pz = -dz, dx

        def P(u, v, y):
            return (dx * u + px * v, y, dz * u + pz * v)
        prof = [(2.0, 0.0), (2.0, 10.0), (19.0, 10.0), (30.6, 0.0)]
        g.hull([P(u, v, y) for u, y in prof for v in (-2.6, 2.6)], 'dark', bevel=0.2)
        g.hull([P(u, v, y) for u, y in ((14.0, 10.0), (19.2, 10.0), (14.0, 10.5), (18.6, 10.5)) for v in (-2.0, 2.0)],
               'steel', bevel=0.08)
        g.cyl(P(19.0, 0, 9.2), P(29.0, 0, 1.0), 1.3, 8, 'steel')
        g.hull([P(u, v, y) for u, y in ((26.0, 0.0), (32.4, 0.0), (26.0, 1.4), (31.0, 1.4)) for v in (-3.6, 3.6)],
               'steel', bevel=0.15)
    leg('leg1', -1, 1)
    k.clone('leg2', 'leg1', mirror_x=True)
    leg('leg4', -1, -1)
    k.clone('leg3', 'leg4', mirror_x=True)
