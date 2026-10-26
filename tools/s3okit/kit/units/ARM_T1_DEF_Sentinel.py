"""Sentinel (ARM_T1_DEF_Sentinel) - Arm heavy laser tower. A stout armoured blockhouse with three raked buttress fins,
a tall column and a wide Y-yoke carrying two big laser pods far out to the sides (the TA silhouette: a 'tuning fork'
on a pole).
Identity from above: two long light laser pods with team backs and cyan lenses, joined by a dark yoke, high over an
octagonal light blockhouse with dark fins - wider and heavier than the LLT's single arrow pod.
Pieces (Lua script): base, turret (turn y), guns (turn x), flash1/flash2 (emit, empty).
turret/guns origins sit at x = 0.25 (not 0), so nothing above the base can use mirror=True: built whole.
Coordinates are ENGINE/global: X right, Y up, Z forward."""
import math

UNIT = dict(
    res=1024,
    wreck=dict(seed=17, drop=[], pose={'turret': (0, 35, 0), 'guns': (15, 0, 0)}),
    preview_pose={'turret': (0, -25, 0), 'guns': (-6, 0, 0)},
)

POD_X = (-8.5, 8.42)          # global x of the two flash pieces = the pod axes


def build(k):
    # ------------------------------------------------------------------ base: octagonal blockhouse + fins
    b = k.piece('base')
    oct8 = lambda r: [(r * math.cos(math.pi / 8 + i * math.pi / 4), r * math.sin(math.pi / 8 + i * math.pi / 4)) for i in range(8)]
    b.plan(0.0, 2.0, oct8(17.0), 'paint2', bevel=0.2, top_inset=0.6)
    b.plan(1.9, 20.0, oct8(11.4), 'paint', bevel=0.22, top_inset=1.6)
    b.plan(19.8, 28.2, oct8(9.6), 'paint', bevel=0.2, top_inset=3.0)
    # team band round the shoulder: four top-facing trapezoids on the sloped roof (diagonal faces)
    for i in range(8):
        a0 = math.pi / 8 + i * math.pi / 4; a1 = a0 + math.pi / 4
        if i % 2:
            continue
        pts = []
        for (r, y) in ((9.95, 20.6), (8.2, 24.6)):
            for a in (a0 + 0.05, a1 - 0.05):
                for d in (0.08, 0.24):
                    pts.append(((r + d) * math.cos(a), y + d * 0.4, (r + d) * math.sin(a)))
        b.hull(pts, 'team', bevel=0.0)
    b.cyl((0, 27.6, 1.0), (0, 28.3, 1.0), 5.2, 12, 'dark', bevel=0.08)
    # three raked buttress fins (rear, front-left, front-right), dark
    for ang in (-90, 30, 150):
        a = math.radians(ang); cx, cz = math.cos(a), math.sin(a); px, pz = -cz, cx
        pts = [((cx * u + px * w), y, (cz * u + pz * w)) for (u, y) in ((9.0, 1.8), (17.4, 1.8), (9.0, 15.0)) for w in (-1.6, 1.6)]
        b.hull(pts, 'dark', bevel=0.15)
    # door + lights
    b.box((-2.6, 2.0, 10.6), (2.6, 9.0, 11.6), 'black', bevel=0.05)
    b.box((-3.2, 9.0, 10.4), (3.2, 9.8, 11.7), 'hazard', bevel=0.04)
    b.box((-0.7, 16.0, 10.9), (0.7, 17.0, 11.2), 'lightc', bevel=0.0)

    # ---------------------------------------------------------------- turret: column (origin 0.25, 28.11, 1.0)
    t = k.piece('turret'); A = t.at
    t.cyl(A(0, 0, 0), A(0, 2.0, 0), 4.6, 8, 'paint2', rot=math.pi / 8, bevel=0.1)
    t.cyl(A(0, 2.0, 0), A(0, 21.0, 0), 3.2, 8, 'paint', r2=2.6, rot=math.pi / 8, bevel=0.12)
    for y in (8.0, 14.0):
        t.cyl(A(0, y, 0), A(0, y + 1.2, 0), 3.7, 8, 'dark', rot=math.pi / 8, bevel=0.05)
    t.cyl(A(0, 20.4, 0), A(0, 23.4, 0), 3.8, 8, 'dark', rot=math.pi / 8, bevel=0.08)

    # --------------------------------------------------------------- guns: Y-yoke + two laser pods (origin 0.25, 51.61, 1.25)
    g = k.piece('guns'); G = g.at
    gx = k.P['guns'].x
    # hub
    g.box(G(-3.0, -2.6, -3.0), G(3.0, 2.4, 3.6), 'dark', bevel=0.2)
    for px in POD_X:
        lx = px - gx; s = 1 if lx > 0 else -1
        # yoke arm: from the hub up and out to the pod
        g.hull([G(x, y, z) for x, y, z in
                [(2.4 * s, -2.0, -2.0), (2.4 * s, -2.0, 2.6), (2.4 * s, 1.8, -2.0), (2.4 * s, 1.8, 2.6),
                 (lx - 2.6 * s, 2.6, -2.2), (lx - 2.6 * s, 2.6, 2.8), (lx - 2.6 * s, 6.4, -2.2), (lx - 2.6 * s, 6.4, 2.8)]],
               'paint2', bevel=0.15)
        # pod body: long hexagonal prism, pointed rear
        cy = 4.88
        pod = []
        for (z, r) in ((-13.0, 1.4), (-10.0, 3.4), (8.0, 3.4), (13.0, 2.6)):
            for i in range(6):
                a = math.pi / 6 + i * math.pi / 3
                pod.append(G(lx + r * math.cos(a) * 1.05, cy + r * math.sin(a), z))
        g.hull(pod, 'paint', bevel=0.2)
        # team top plate
        g.hull([G(lx + x, cy + y, z) for x in (-1.5, 1.5) for y in (3.0, 3.18) for z in (-9.0, 6.6)], 'team', bevel=0.0)
        # dark side fins (outward) and cyan lens
        g.hull([G(lx + x * s, cy + y, z) for x, y, z in
                [(3.0, -1.0, -10.0), (7.0, -0.6, -12.6), (3.0, -1.0, 0.0), (6.4, -0.6, -6.0),
                 (3.0, 0.6, -10.0), (6.6, 0.4, -12.4), (3.0, 0.6, 0.0), (6.0, 0.4, -6.0)]], 'dark', bevel=0.1)
        g.cyl(G(lx, cy + 2.6, 4.0), G(lx, cy + 3.5, 3.6), 1.15, 10, 'lightc')
        # emitter barrel to the flash point
        g.cyl(G(lx, cy, 12.6), G(lx, cy, 22.0), 1.0, 8, 'steel')
        g.cyl(G(lx, cy, 15.0), G(lx, cy, 16.2), 1.5, 8, 'dark')
        g.cyl(G(lx, cy, 21.4), G(lx, cy, 23.0), 1.6, 8, 'dark', bevel=0.05)
        g.cyl(G(lx, cy, 22.98), G(lx, cy, 23.08), 0.9, 8, 'lightc')
