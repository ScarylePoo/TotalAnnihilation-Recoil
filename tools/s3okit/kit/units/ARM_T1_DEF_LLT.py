"""L.L.T. (ARM_T1_DEF_LLT) - Arm light laser tower. A slim tapering spire on four cross-shaped buttresses, a fork
turret on a thin neck and a long pointed laser pod (arrowhead nose) with a short emitter barrel.
Identity from above: a cross (four buttress arms, team-capped) round a light spire, the long arrow-shaped laser pod
with a dark centre spine and cyan lens on top.
Pieces (Lua script): base, turret (turn y), sleeve (turn x), barrel (static), flare (emit, empty).
Coordinates are ENGINE/global: X right, Y up, Z forward."""
import math

UNIT = dict(
    res=1024,
    wreck=dict(seed=11, drop=['sleeve'], pose={'turret': (0, 50, 0)}),
    preview_pose={'turret': (0, -25, 0), 'sleeve': (-8, 0, 0)},
)


def build(k):
    # ------------------------------------------------------------------ base: buttressed spire
    b = k.piece('base')
    # low square foot slab
    b.plan(0.0, 1.8, [(-14, -10), (-10, -14), (10, -14), (14, -10), (14, 10), (10, 14), (-10, 14), (-14, 10)],
           'paint2', bevel=0.2, top_inset=0.6)
    # four buttress arms (cross plan): sloped wedges from the spire to the edge, team caps at the outer ends
    for ax in ('x', 'z'):
        for s in (-1, 1):
            def P(u, y, w):            # u along the arm, w across
                return (u * s, y, w) if ax == 'x' else (w, y, u * s)
            pts = [P(u, y, w) for (u, y) in ((5.0, 1.6), (16.0, 1.6), (15.4, 6.2), (5.0, 17.0)) for w in (-3.4, 3.4)]
            b.hull(pts, 'paint', bevel=0.2)
            ys = lambda u: 6.2 + (15.4 - u) / 10.4 * 10.8          # top slope of the buttress
            cap = [P(u, ys(u) + d, w) for u in (8.0, 15.0) for w in (-2.9, 2.9) for d in (0.06, 0.22)]
            b.hull(cap, 'team', bevel=0.0)
    # spire (tapered octagon)
    b.cyl((0, 1.6, 0), (0, 24.0, 0), 8.4, 8, 'paint2', r2=4.0, rot=math.pi / 8, bevel=0.2)
    b.cyl((0, 23.6, 0), (0, 25.2, 0), 4.6, 8, 'dark', rot=math.pi / 8, bevel=0.08)
    b.box((-0.8, 14.0, 5.75), (0.8, 15.0, 6.05), 'lightc', bevel=0.0)   # status light on the spire front

    # ---------------------------------------------------------------- turret: neck + fork (origin 0, 25.12, 0)
    t = k.piece('turret'); A = t.at
    t.cyl(A(0, 0, 0), A(0, 9.0, 0), 2.6, 8, 'dark', rot=math.pi / 8, bevel=0.08)
    t.cyl(A(0, 3.0, 0), A(0, 5.0, 0), 3.6, 8, 'paint', rot=math.pi / 8, bevel=0.1)
    t.hull([A(x * sx, y, z) for sx in (-1, 1) for x, y, z in
            [(5.6, 8.6, -2.4), (5.6, 8.6, 2.4), (5.0, 10.6, -2.6), (5.0, 10.6, 2.6)]], 'paint', bevel=0.15)
    t.hull([A(x, y, z) for x, y, z in
            [(3.4, 10.0, -2.0), (5.4, 10.0, -2.0), (3.4, 10.0, 2.0), (5.4, 10.0, 2.0),
             (3.6, 17.2, -1.6), (5.2, 17.2, -1.6), (3.6, 17.2, 1.6), (5.2, 17.2, 1.6)]], 'paint2', bevel=0.12, mirror=True)

    # --------------------------------------------------------------- sleeve: long arrow-shaped laser pod (origin 0, 40.88, 0)
    sv = k.piece('sleeve'); S = sv.at
    sv.cyl(S(-5.4, 0, 0), S(5.4, 0, 0), 1.3, 8, 'steel')
    pod = [(3.4, -2.6, -11.6), (3.8, -2.6, -2.0), (3.6, -2.0, 6.0), (1.6, -1.4, 13.6),
           (3.0, 3.0, -11.0), (3.4, 3.4, -2.0), (3.0, 3.0, 5.0), (1.3, 1.4, 13.0)]
    sv.hull([S(x * sx, y, z) for sx in (-1, 1) for x, y, z in pod], 'paint', bevel=0.2)
    # dark spine on top of the pod, lens near the nose
    sv.hull([S(x * sx, y, z) for sx in (-1, 1) for x, y, z in
             [(1.6, 3.32, -10.4), (1.6, 3.32, 3.6), (1.4, 3.62, -10.2), (1.4, 3.62, 3.4)]], 'team', bevel=0.03)
    sv.cyl(S(0, 3.0, 5.4), S(0, 3.75, 5.0), 1.0, 10, 'lightc')
    # dark side cooling fins
    sv.hull([S(x, y, z) for x, y, z in
             [(3.3, -1.0, -9.6), (5.6, -0.6, -9.0), (3.3, -1.0, -2.0), (5.6, -0.6, -3.0),
              (3.3, 1.6, -9.6), (5.2, 1.2, -9.0), (3.3, 1.6, -2.0), (5.2, 1.2, -3.0)]], 'dark', bevel=0.1, mirror=True)
    sv.box(S(-2.6, -1.8, -12.8), S(2.6, 2.2, -11.2), 'dark', bevel=0.1)

    # --------------------------------------------------------------- barrel: emitter (origin 0, 40.75, 14.5)
    br = k.piece('barrel'); B = br.at
    br.cyl(B(0, 0, -1.0), B(0, 0, 6.6), 0.75, 8, 'steel')
    br.cyl(B(0, 0, 1.2), B(0, 0, 2.2), 1.05, 8, 'dark')
    br.cyl(B(0, 0, 6.4), B(0, 0, 7.0), 0.85, 8, 'lightc')
