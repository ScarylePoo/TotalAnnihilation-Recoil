"""Atlas (ARM_T1_AIR_Atlas) - Arm VTOL transport. Bulky, round-shouldered cargo body with a long cockpit nose and a
dorsal intake hump, carried by THREE big ducted lift fans: two side pods and a larger tail fan. From above the three
team-rimmed fan discs around a light hull are the unit (no wings at all). The fan pods are on telescoping struts:
the COB slides the side pods out 8.5 elmo and swings them 21 deg, and pushes the tail fan 12 elmo aft on take-off.
Pieces (TA layout): base, link (empty: cargo attach point under the belly clamp), arm1/arm2 (side fan pods on struts;
arm1's geometry is on +x; arm2 = mirrored clone), arm3 (tail fan), jet1..3 (empty emit points under the fans).
Value groups from above: light Arm hull + duct cowls, dark paint2 struts/hump/belly clamp, black fan wells with dark
blades, team rims on the fans + a roof band.
Coordinates are ENGINE/global: X right, Y up, Z forward. mirror=True builds the -X twin sharing UVs."""
import math

UNIT = dict(
    res=1024,
    wreck=dict(seed=8, drop=['arm2']),
    preview_pose={'arm1': {'move': (8.5, 0, 0), 'rot': (0, -21.2, 0)}, 'arm2': {'move': (-8.5, 0, 0), 'rot': (0, 21.2, 0)},
                  'arm3': {'move': (0, 0, -12.0)}},   # flight pose (COB activatescr)
)


def fan(p, c, r, h0, h1):
    """ducted fan around c (global x, z), cowl from y h0 to h1, team rim on top, black well with dark blades."""
    x, z = c
    p.cyl((x, h0, z), (x, h1, z), r, 20, 'paint', r2=r * 1.04, bevel=0.12)
    p.cyl((x, h1, z), (x, h1 + 0.35, z), r * 1.04, 20, 'team', r2=r * 0.98, bevel=0.04)
    p.cyl((x, h1 + 0.35, z), (x, h1 + 0.42, z), r * 0.74, 20, 'black')
    for a in (0, 60, 120):
        t = math.radians(a)
        dx, dz = math.cos(t) * r * 0.72, math.sin(t) * r * 0.72
        p.hull([(x + dx * s + ox, h1 + 0.42 + dy, z + dz * s + oz) for s in (-1, 1) for dy in (0.0, 0.16)
                for ox, oz in ((-math.sin(t) * 0.45, math.cos(t) * 0.45), (math.sin(t) * 0.45, -math.cos(t) * 0.45))],
               'dark', bevel=0.0)
    p.cyl((x, h1 + 0.4, z), (x, h1 + 0.9, z), r * 0.2, 10, 'dark', r2=r * 0.12)
    p.cyl((x, h0 - 0.1, z), (x, h0, z), r * 0.8, 16, 'lightc')       # downwash glow under the fan


def build(k):
    b = k.piece('base')
    # ------------------------------------------------------------------ cargo body (crosses x = 0)
    b.hull([(x * sx, y, z) for sx in (-1, 1) for x, y, z in
            [(1.6, 6.0, 25.0), (3.6, 4.0, 21.0), (3.8, 9.0, 21.6),
             (7.6, 3.9, 12.0), (8.4, 9.8, 11.0), (6.8, 14.6, 9.0),
             (8.2, 3.9, -12.0), (8.6, 10.6, -10.0), (6.8, 15.2, -9.0),
             (5.0, 4.4, -16.4), (5.2, 11.6, -17.2), (3.6, 13.8, -16.6)]], 'paint', bevel=0.22, seg=2)
    # cockpit glazing on the nose
    b.hull([(x * sx, y, z) for sx in (-1, 1) for x, y, z in
            [(2.6, 8.6, 22.6), (4.6, 11.2, 17.0), (2.2, 13.4, 14.6), (2.4, 9.0, 22.2)]] +
           [(x * sx, y + 0.12, z + 0.1) for sx in (-1, 1) for x, y, z in
            [(2.6, 8.6, 22.6), (4.6, 11.2, 17.0), (2.2, 13.4, 14.6)]], 'glass', bevel=0.06)
    # team roof band across the middle of the hull
    b.hull([(x * sx, y, z) for sx in (-1, 1) for x, y, z in
            [(6.4, 15.0, 2.0), (6.4, 15.25, -4.0), (6.5, 15.24, 2.0), (6.5, 15.49, -4.0)]], 'team', bevel=0.03)
    # dorsal intake hump with a dark grille (rear)
    b.hull([(x * sx, y, z) for sx in (-1, 1) for x, y, z in
            [(3.2, 15.0, -5.0), (3.2, 14.4, -15.6), (2.6, 18.6, -7.0), (2.4, 17.6, -13.6)]], 'paint2', bevel=0.12)
    b.box((-2.2, 16.6, -5.9), (2.2, 18.2, -5.4), 'black', bevel=0.0)
    b.cyl((0, 17.5, -14.2), (0, 17.5, -16.8), 1.3, 10, 'dark', r2=1.1, bevel=0.04)
    b.cyl((0, 17.5, -16.75), (0, 17.5, -16.9), 0.8, 10, 'lightc')
    # side strut sockets (the side pods' struts slide in here)
    b.box((7.4, 6.2, 2.4), (8.9, 10.4, 8.4), 'paint2', bevel=0.12, mirror=True)
    # tail strut socket
    b.box((-2.6, 7.0, -18.0), (2.6, 11.0, -15.0), 'paint2', bevel=0.12)
    # belly cargo clamp around the link point
    b.box((-5.2, 2.6, -6.0), (5.2, 4.1, 8.0), 'paint2', bevel=0.14)
    for z in (-5.6, 7.6):
        b.box((-4.6, 1.2, z - 0.6), (4.6, 2.7, z + 0.6), 'dark', bevel=0.08)
    b.cyl((0, 2.6, 1.2), (0, 2.0, 1.2), 1.4, 12, 'dark', bevel=0.04)
    # lights: landing lights under the nose, red beacon on the hump
    b.box((-1.4, 3.6, 22.4), (1.4, 4.4, 22.9), 'lightw', bevel=0.0)
    b.cyl((0, 18.5, -9.6), (0, 19.2, -9.6), 0.5, 8, 'lightr')
    # antenna on the roof, offset left
    b.cyl((-4.0, 14.4, 6.0), (-4.0, 20.0, 6.0), 0.1, 6, 'steel', r2=0.05)

    # ------------------------------------------------------------------ side fan pod (arm1 origin -0.38, 5, 5; geometry +x)
    a = k.piece('arm1'); A = a.at
    a.box(A(-0.3, 1.6, 0.6), A(10.4, 4.6, 5.6), 'paint2', bevel=0.14)            # telescoping strut (slides out 8.5)
    a.box(A(4.0, 4.55, 1.4), A(9.6, 4.7, 4.8), 'dark', bevel=0.0)
    fan(a, (A(14.36, 0, -0.16)[0], A(14.36, 0, -0.16)[2]), 4.6, A(0, -3.6, 0)[1], A(0, 4.4, 0)[1])
    # guide vane behind the fan
    a.hull([A(x, y, z) for x in (13.9, 14.8) for y, z in ((-2.6, -4.6), (3.8, -4.6), (-2.0, -8.6), (2.6, -8.0))], 'paint2', bevel=0.08)
    a.box(A(14.0, 3.6, -8.4), A(14.7, 3.9, -7.8), 'lightw', bevel=0.0)
    k.clone('arm2', 'arm1', mirror_x=True)

    # ------------------------------------------------------------------ tail fan (arm3 origin 0, 5, -6.12)
    t = k.piece('arm3'); T = t.at
    t.hull([T(x * sx, y, z) for sx in (-1, 1) for x, y, z in
            [(2.2, 2.6, 2.0), (2.2, 5.6, 2.0), (1.8, 2.8, -10.6), (1.8, 5.4, -10.6)]], 'paint2', bevel=0.12)   # telescopes out 12
    t.box(T(-1.6, 5.55, -10.2), T(1.6, 5.7, -1.0), 'dark', bevel=0.0)
    fan(t, (T(0.22, 0, -15.2)[0], T(0.22, 0, -15.2)[2]), 5.4, T(0, -3.2, 0)[1], T(0, 5.0, 0)[1])
    # twin tail fins either side of the big fan
    for s in (-1, 1):
        t.hull([T(x, y, z) for x in (s * 6.0 + 0.22, s * 6.8 + 0.22) for y, z in
                ((2.0, -12.0), (2.0, -19.0), (9.4, -16.6), (9.4, -19.6))], 'paint', bevel=0.08)
        t.box(T(s * 6.4 + 0.22 - 0.45, 9.4, -19.4), T(s * 6.4 + 0.22 + 0.45, 9.8, -18.6), 'lightr', bevel=0.0)
