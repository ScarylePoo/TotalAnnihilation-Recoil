"""Advanced Radar Tower (ARM_T2_DEF_AdvancedRadar) - Arm long-range radar. Closed it is a squat tapered tower with two
fan-shaped radar vanes hanging down its flanks; switched on, the mast rises 25 elmo out of the tower, the vanes swing
up ~84 deg into a pair of wide horizontal wings and the whole head spins while the wings roll on their axles.
Identity from above (open): a long light 'bow tie' of two trapezoid wings, widening outward, each with a broad team band
along its span and dark frames, over a small light tower - far wider than the T1 radar's paddles.
Pieces (Lua script): base, post (move y 25), turret (spin y), arm1/arm2 (spin x), dish1/dish2 (turn z +-1.46 rad).
The preview shows the OPEN state.
Coordinates are ENGINE/global: X right, Y up, Z forward."""
import math

UNIT = dict(
    res=1024,
    wreck=dict(seed=21, drop=['dish2'], pose={'turret': (0, 30, 0)}),
    preview_pose={'post': {'move': (0, 25.0, 0)}, 'turret': (0, 20, 0), 'dish1': (0, 0, -84), 'dish2': (0, 0, 84)},
)


def vane(d):
    """a radar vane hanging from its hinge (local y 0 at the hinge, down to -27): narrow at the hinge, wide at the tip.
    Faces are +-X (the outer face is the top when the vane is open); both faces carry a team band (the arm rolls)."""
    D = d.at
    ys = [(-1.2, 6.6), (-27.0, 14.6)]          # (y, half-width in z)
    d.hull([D(x, y, z * s) for y, w in ys for s in (-1, 1) for x, z in ((-1.5, w), (1.5, w))], 'dark', bevel=0.12)
    d.hull([D(x, y, z * s) for y, w in [(-2.4, 5.8), (-25.8, 13.4)] for s in (-1, 1) for x, z in ((-1.8, w), (1.8, w))],
           'paint', bevel=0.12)
    d.hull([D(x, y, z * s) for y, w in [(-3.2, 1.8), (-25.0, 3.8)] for s in (-1, 1) for x, z in ((-1.95, w), (1.95, w))],
           'team', bevel=0.0)
    # hinge knuckle and a cyan tip light
    d.cyl(D(0, 0.4, -4.6), D(0, 0.4, 4.6), 1.9, 8, 'dark', bevel=0.06)
    d.box(D(-0.6, -27.6, -2.0), D(0.6, -26.9, 2.0), 'lightc', bevel=0.0)


def build(k):
    # ------------------------------------------------------------------ base: tapered tower between the vanes
    b = k.piece('base')
    b.plan(0.0, 2.0, [(-15.4, -15.4), (15.4, -15.4), (15.4, 15.4), (-15.4, 15.4)], 'paint2', bevel=0.2, top_inset=0.8)
    # core column: narrow in x (the vanes hang either side), tapered in z
    b.hull([(x * s, y, z * t) for s in (-1, 1) for t in (-1, 1) for x, y, z in
            [(7.0, 1.9, 14.0), (5.6, 24.6, 6.4)]], 'paint', bevel=0.25)
    # dark grooves on the flanks where the vanes nest, and a dark collar the mast rises from
    b.hull([(x * s, y, z * t) for s in (-1, 1) for t in (-1, 1) for x, y, z in
            [(7.2, 2.0, 9.0), (5.8, 22.0, 4.0)]], 'dark', bevel=0.08)
    b.cyl((0, 24.0, 0), (0, 25.6, 0), 5.2, 8, 'dark', rot=math.pi / 8, bevel=0.08)
    # team: the front/back sloped faces of the column and the plinth corners
    for t in (-1, 1):
        pts = []
        for y, hz, hx in ((4.0, 12.95, 5.2), (21.0, 7.85, 4.2)):
            for s in (-1, 1):
                for dd in (0.08, 0.26):
                    pts.append((hx * s, y + dd * 0.2, (hz + dd) * t))
        b.hull(pts, 'team', bevel=0.0)
    for s in (-1, 1):
        for t in (-1, 1):
            b.box((min(9.6 * s, 14.6 * s), 1.9, min(9.6 * t, 14.6 * t)), (max(9.6 * s, 14.6 * s), 2.6, max(9.6 * t, 14.6 * t)),
                  'team', bevel=0.06)
    b.box((-1.0, 12.0, 11.3), (1.0, 13.4, 11.6), 'lightc', bevel=0.0)

    # ------------------------------------------------------------------ post: the mast that rises 25 elmo
    p = k.piece('post'); A = p.at
    p.cyl(A(0, 0.2, 0), A(0, 25.2, 0), 3.4, 8, 'steel', rot=math.pi / 8, bevel=0.05)
    for y in (8.0, 16.0):
        p.cyl(A(0, y, 0), A(0, y + 1.2, 0), 3.8, 8, 'dark', rot=math.pi / 8, bevel=0.04)

    # ------------------------------------------------------------------ turret: spinning head (origin 0, 25.05, 0)
    t = k.piece('turret'); T = t.at
    t.cyl(T(0, 0, 0), T(0, 1.2, 0), 4.4, 10, 'dark', bevel=0.06)
    t.hull([T(x * s, y, z * u) for s in (-1, 1) for u in (-1, 1) for x, y, z in
            [(3.0, 1.0, 6.0), (2.0, 6.8, 4.0), (0.6, 2.6, 12.4), (0.6, 4.0, 12.0)]], 'paint', bevel=0.15)
    t.box(T(-1.6, 6.8, -3.0), T(1.6, 7.6, 3.0), 'team', bevel=0.04)
    t.box(T(-0.5, 3.0, 12.2), T(0.5, 4.0, 12.8), 'lightr', bevel=0.0)

    # ------------------------------------------------------------------ arms: axles (arm1 origin -2.5, 27.8, 0)
    a = k.piece('arm1'); R = a.at
    a.cyl(R(0.2, 0, 0), R(-8.2, 0, 0), 1.7, 8, 'steel', bevel=0.04)
    a.cyl(R(-6.2, 0, 0), R(-8.4, 0, 0), 2.6, 8, 'dark', bevel=0.06)
    k.clone('arm2', 'arm1', mirror_x=True)

    # ------------------------------------------------------------------ vanes (dish1 origin -10.5, 27.42, 0)
    vane(k.piece('dish1'))
    k.clone('dish2', 'dish1', mirror_x=True)
