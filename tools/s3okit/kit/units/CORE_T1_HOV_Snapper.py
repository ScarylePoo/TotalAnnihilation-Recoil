"""Snapper (CORE_T1_HOV_Snapper) - Core hovertank. TA's X-shaped hull: a central armoured body with four angled
float pods splayed out at the corners (each on its own black skirt), and a low split turret set back: the left half
is the fixed `turret` block, the right half is the elevating `sleeve` carrying one heavy cannon (`barrel` recoils z)
offset to the right. Distinct from the Anaconda: four splayed pods instead of one round skirt, off-centre gun on
the right, dark warm Core armour.
Pieces: base (rocks x/z), turret (turn y), sleeve (turn x), barrel (move z), flare (empty), wake1..8 (empty).
Value groups from above: four black skirt pods in an X, dark warm pods/body (paint), darker paint2 central deck,
light steel cannon + mantlet (Core = light guns), team: turret roof + a band across the pod tops at the rear.
Coordinates are ENGINE/global: X right, Y up, Z forward. mirror=True builds the -X twin sharing UVs."""
import math

UNIT = dict(
    res=1024,
    wreck=dict(seed=14, drop=['barrel'], pose={'turret': (0, -35, 0)}),
    preview_pose={'turret': (0, -20, 0), 'sleeve': (-4, 0, 0)},
)


def pod(b, c0, c1, w, top):
    """skirted float pod from point c0 to c1 (x, z) in plan, width w; +X side (mirrored)"""
    (x0, z0), (x1, z1) = c0, c1
    dx, dz = x1 - x0, z1 - z0
    L = math.hypot(dx, dz); ux, uz = dx / L, dz / L
    nx, nz = -uz, ux

    def ring(y, g, taper=0.0):
        hw = w / 2 + g
        pts = []
        for (px, pz), e in (((x0, z0), -1), ((x1, z1), 1)):
            ex, ez = px + ux * e * (g + 0.0), pz + uz * e * (g + 0.0)
            for s in (-1, 1):
                pts.append((ex + nx * s * (hw - taper) - ux * e * 1.6, y, ez + nz * s * (hw - taper) - uz * e * 1.6))
                pts.append((ex + nx * s * (hw - 1.6 - taper), y, ez + nz * s * (hw - 1.6 - taper)))
        return pts
    b.hull(ring(0.0, 0.6) + ring(2.4, 1.9) + ring(4.4, 1.6) + ring(5.6, 0.8), 'tread', bevel=0.25, mirror=True)
    b.hull(ring(5.2, 0.0) + ring(top, -0.8, 0.6), 'paint', bevel=0.2, mirror=True)
    b.hull(ring(5.4, 0.5) + ring(6.4, 0.4), 'steel', bevel=0.07, mirror=True)


def build(k):
    b = k.piece('base')
    # ------------------------------------------------------------------ four splayed pods
    pod(b, (7.0, 6.0), (10.2, 21.6), 7.2, 8.6)         # front, splayed out
    pod(b, (7.4, -6.6), (11.0, -22.4), 7.8, 8.6)       # rear, splayed out
    # team plate on each rear pod top
    b.hull([(x, y, z) for y in (8.62, 8.78) for x, z in [(7.2, -10.4), (10.0, -10.4), (11.4, -17.6), (8.6, -17.6)]],
           'team', bevel=0.03, mirror=True)
    # outrigger arms joining the pods to the body (+X, mirrored)
    b.hull([(4.0, 5.0, -10.0), (4.0, 5.0, 8.0), (13.2, 5.0, -8.6), (13.2, 5.0, 6.7), (21.2, 6.4, -5.0), (21.2, 6.4, 3.0),
            (4.0, 9.2, -9.0), (4.0, 9.2, 7.0), (11.6, 9.6, -8.0), (11.6, 9.6, 6.0), (21.6, 8.6, -5.6), (21.6, 8.6, 3.6)],
           'paint', bevel=0.2, mirror=True)
    # lift fans on the outriggers
    x, z = 16.6, -1.0
    b.cyl((x, 8.4, z), (x, 9.8, z), 4.2, 16, 'dark', bevel=0.12, mirror=True)
    b.cyl((x, 9.8, z), (x, 9.85, z), 3.4, 16, 'black', mirror=True)
    for i in range(4):
        a = i * math.pi / 2 + 0.7
        ca, sa = math.cos(a), math.sin(a)
        pts = []
        for d in (0.7, 3.2):
            for s in (-0.6, 0.6):
                px, pz = x + ca * d - sa * s, z + sa * d + ca * s
                pts += [(px, 9.55, pz), (px, 9.85, pz)]
        b.hull(pts, 'steel', bevel=0.0, mirror=True)
    b.cyl((x, 9.5, z), (x, 10.2, z), 1.0, 10, 'steel', bevel=0.05, mirror=True)
    # ------------------------------------------------------------------ central body (crosses x = 0)
    b.hull([(x * sx, y, z) for sx in (-1, 1) for x, y, z in
            [(5.0, 4.0, -21.0), (5.0, 4.0, 20.0), (2.4, 4.6, 23.0), (6.6, 12.7, -13.3), (6.6, 12.7, 6.0),
             (3.0, 10.2, 20.0), (4.4, 8.6, -20.4)]], 'paint', bevel=0.22)
    # darker deck under the turret
    b.hull([(x * sx, y, z) for sx in (-1, 1) for x, y, z in
            [(6.0, 12.68, -12.8), (6.0, 12.68, 5.4), (6.0, 12.86, -12.8), (6.0, 12.86, 5.4)]], 'paint2', bevel=0.04)
    # glacis: ochre hazard band + lights
    b.hull([(x * sx, y, z) for sx in (-1, 1) for x, y, z in
            [(4.2, 11.8, 9.6), (3.4, 10.7, 16.0), (4.2, 11.94, 9.64), (3.4, 10.84, 16.04)]], 'hazard', bevel=0.02)
    b.box((1.0, 6.4, 22.4), (3.4, 8.0, 23.2), 'dark', bevel=0.05, mirror=True)
    b.hull([(1.2, 6.6, 23.1), (3.2, 6.6, 22.6), (1.2, 7.8, 23.1), (3.2, 7.8, 22.6),
            (1.2, 6.6, 23.22), (3.2, 6.6, 22.72), (1.2, 7.8, 23.22), (3.2, 7.8, 22.72)], 'lightw', bevel=0.0, mirror=True)
    # stern: exhaust grille, tail lights, team band across the rear pods' inner ends
    b.box((-4.0, 5.6, -21.6), (4.0, 8.6, -20.8), 'dark', bevel=0.06)
    b.box((-3.6, 6.0, -21.75), (3.6, 8.2, -21.5), 'black', bevel=0.0)
    b.box((5.4, 6.2, -24.4), (7.4, 7.2, -23.8), 'lightr', bevel=0.0, mirror=True)
    b.hull([(x * sx, y, z) for sx in (-1, 1) for x, y, z in
            [(5.6, 10.0, -17.4), (5.6, 10.0, -14.0), (5.6, 10.2, -17.4), (5.6, 10.2, -14.0)]], 'team', bevel=0.03)
    # antenna
    b.cyl((-5.0, 9.4, -18.0), (-5.0, 10.2, -18.0), 0.35, 8, 'dark')
    b.cyl((-5.0, 10.2, -18.0), (-5.0, 17.0, -18.0), 0.09, 6, 'steel', r2=0.04)
    b.cyl((-5.0, 17.0, -18.0), (-5.0, 17.2, -18.0), 0.14, 6, 'lightr')

    # ---------------------------------------------------------------- turret (origin 0, 13.1, -9.3): left block
    t = k.piece('turret'); A = t.at
    t.cyl(A(-1.4, -0.2, -0.6), A(-1.4, 0.3, -0.6), 6.6, 18, 'dark', bevel=0.06)
    t.hull([A(x, y, z) for x, y, z in
            [(-8.0, 0.2, -9.8), (0.5, 0.2, -10.4), (0.5, 0.2, 6.8), (-6.6, 0.2, 5.4),
             (-6.8, 4.0, -8.2), (0.5, 4.0, -8.8), (0.5, 3.0, 5.4), (-5.6, 3.0, 4.2)]], 'paint', bevel=0.18)
    t.hull([A(x, y, z) for x, y, z in
            [(-5.8, 4.02, -7.0), (-0.3, 4.02, -7.4), (-0.3, 3.2, 3.6), (-4.8, 3.2, 2.8),
             (-5.8, 4.16, -7.0), (-0.3, 4.16, -7.4), (-0.3, 3.34, 3.6), (-4.8, 3.34, 2.8)]], 'team', bevel=0.03)
    t.cyl(A(-4.4, 4.0, -5.4), A(-4.4, 5.0, -5.4), 1.3, 12, 'paint2', bevel=0.06)
    t.box(A(-5.0, 4.4, -4.15), A(-3.8, 4.8, -3.95), 'lightc', bevel=0.0)

    # ---------------------------------------------------------------- sleeve (origin 2.42, 15, -9.3): right gun block
    s = k.piece('sleeve'); S = s.at
    s.hull([S(x, y, z) for x, y, z in
            [(-1.8, -2.2, -8.6), (3.6, -2.2, -8.6), (-1.8, -2.2, 9.2), (2.6, -2.2, 9.2),
             (-1.8, 1.8, -7.0), (2.4, 1.8, -7.0), (-1.8, 1.6, 7.6), (2.0, 1.6, 7.6)]], 'paint', bevel=0.18)
    s.box(S(-1.2, 1.75, -6.0), S(1.8, 1.95, 5.6), 'team', bevel=0.03)
    s.box(S(-1.2, -1.8, 8.8), S(2.8, 1.2, 10.4), 'steel', bevel=0.14)       # mantlet

    # ---------------------------------------------------------------- barrel (origin 2.86, 14.47, 0.16)
    br = k.piece('barrel'); B = br.at
    br.cyl(B(0, 0, 0.0), B(0, 0, 16.4), 1.0, 12, 'steel')
    br.cyl(B(0, 0, 0.2), B(0, 0, 4.0), 1.45, 12, 'steel', bevel=0.05)
    br.cyl(B(0, 0, 9.0), B(0, 0, 11.4), 1.3, 12, 'dark', bevel=0.05)
    br.cyl(B(0, 0, 16.2), B(0, 0, 17.8), 1.55, 8, 'steel', rot=math.pi / 8, bevel=0.06)
    br.cyl(B(0, 0, 17.78), B(0, 0, 17.86), 0.7, 10, 'black')
