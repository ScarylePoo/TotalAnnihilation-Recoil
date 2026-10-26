"""Guardian (ARM_T1_DEF_Guardian) - Arm plasma battery. A broad hexagonal bunker plinth, a tall hooded artillery
turret and two very long heavy plasma barrels running through it (they recoil 6 elmo).
Identity from above: big light hexagon with a dark ring, a light hooded turret with a team roof and team cheek plates,
two long fat steel barrels well past the plinth edge.
Pieces (Lua script): base, turret (turn y), sleeves (turn x), barrel1/2 (move z recoil), flare1/2 (emit, empty).
Coordinates are ENGINE/global: X right, Y up, Z forward."""
import math

UNIT = dict(
    res=1024,
    wreck=dict(seed=7, drop=['barrel2'], pose={'turret': (0, -30, 0), 'sleeves': (8, 0, 0)}),
    preview_pose={'turret': (0, -25, 0), 'sleeves': (-8, 0, 0)},
)


def hexagon(r, rot=0.0):
    return [(r * math.cos(rot + i * math.pi / 3), r * math.sin(rot + i * math.pi / 3)) for i in range(6)]


def build(k):
    # ------------------------------------------------------------------ base: hex plinth (origin 0, 2.67, 0)
    b = k.piece('base')
    # bottom skirt (wide, dark) and sloped plinth
    b.plan(0.0, 2.2, [(x, z) for x, z in hexagon(23.0)], 'paint2', bevel=0.2, top_inset=0.8)
    b.plan(2.1, 15.6, [(x, z) for x, z in hexagon(20.6)], 'paint', bevel=0.25, top_inset=4.6)
    # dark ring round the turret seat
    b.cyl((0, 15.4, 0), (0, 17.6, 0), 12.6, 12, 'dark', rot=math.pi / 12, bevel=0.12)
    # plates on the sloped faces (hex vertices at 0/60/..., faces at 30/90/...): team on the four diagonal faces,
    # dark hatches front and back. Apothem shrinks from 17.84 at y 2.1 to 13.86 at y 15.6.
    def face_plate(ang, t0, mat, y0=4.0, y1=13.0, w=6.0):
        a = math.radians(ang); cx, cz = math.cos(a), math.sin(a); px, pz = -cz, cx
        pts = []
        for y in (y0, y1):
            r = 17.84 - (y - 2.1) / 13.5 * 3.98
            for t in (-w, w):
                for d in (0.08, 0.26):
                    pts.append((cx * (r + d) + px * t, y + d * 0.3, cz * (r + d) + pz * t))
        b.hull(pts, mat, bevel=0.0)
    for ang in (30, 150, 210, 330):
        face_plate(ang, 0, 'team')
    for ang in (90, 270):
        face_plate(ang, 0, 'dark', y0=3.5, y1=9.5, w=3.6)

    # ---------------------------------------------------------------- turret: hooded artillery housing (origin 0, 17.61, 0)
    t = k.piece('turret'); A = t.at
    t.cyl(A(0, 0, 0), A(0, 1.4, 0), 11.6, 12, 'dark', rot=math.pi / 12, bevel=0.1)
    # main housing: tapers up into a hood, open-fronted between the cheeks
    t.hull([A(x * sx, y, z) for sx in (-1, 1) for x, y, z in
            [(12.4, 1.4, -13.6), (12.4, 1.4, 4.0), (10.6, 1.4, 7.6),
             (9.6, 17.0, -11.6), (9.6, 17.0, 0.0), (8.2, 13.0, 5.6),
             (4.2, 25.6, -9.4), (4.2, 25.6, -3.0)]], 'paint', bevel=0.25)
    # team roof plate on the hood ridge + the two upper cheek slopes
    t.hull([A(x * sx, y, z) for sx in (-1, 1) for x, y, z in
            [(3.2, 25.62, -8.6), (3.2, 25.62, -3.6), (3.0, 25.8, -8.4), (3.0, 25.8, -3.8)]], 'team', bevel=0.0)
    # dark slot where the barrels pass through the housing (front opening), and the rear vent
    t.box(A(-10.6, 4.6, 6.4), A(10.6, 12.6, 7.8), 'black', bevel=0.0)
    t.hull([A(x * sx, y, z) for sx in (-1, 1) for x, y, z in
            [(9.0, 4.0, -14.2), (9.0, 13.0, -12.6), (9.0, 4.0, -13.0), (9.0, 13.0, -11.6)]], 'dark', bevel=0.08)
    # side armour cheeks (paint2), team top strips
    t.hull([A(x, y, z) for x, y, z in
            [(11.6, 2.0, -9.0), (14.0, 2.0, -8.0), (11.6, 2.0, 4.0), (14.0, 2.0, 3.0),
             (10.6, 13.0, -8.0), (12.6, 12.0, -7.2), (10.6, 13.0, 2.0), (12.6, 12.0, 1.4)]], 'paint2', bevel=0.15, mirror=True)
    t.hull([A(x, y, z) for x, y, z in
            [(11.0, 12.75, -7.0), (12.4, 12.1, -6.4), (11.0, 12.75, 1.2), (12.4, 12.1, 0.8),
             (11.0, 12.9, -7.0), (12.4, 12.25, -6.4), (11.0, 12.9, 1.2), (12.4, 12.25, 0.8)]], 'team', bevel=0.0, mirror=True)
    t.box(A(-1.0, 19.0, -1.6), A(1.0, 20.6, -0.2), 'dark', bevel=0.05)
    t.box(A(-0.7, 19.3, -0.22), A(0.7, 20.2, -0.1), 'lightc', bevel=0.0)

    # --------------------------------------------------------------- sleeves: trunnion (origin 0, 26.23, 0)
    sv = k.piece('sleeves'); S = sv.at
    sv.cyl(S(-11.6, 0, 0), S(11.6, 0, 0), 2.6, 10, 'steel', bevel=0.05)
    sv.hull([S(x, y, z) for x, y, z in
             [(3.8, -3.6, -6.0), (9.6, -3.6, -6.0), (3.8, 3.4, -6.0), (9.6, 3.4, -6.0),
              (3.8, -3.6, 12.0), (9.6, -3.6, 12.0), (3.8, 3.0, 12.0), (9.6, 3.0, 12.0)]], 'dark', bevel=0.2, mirror=True)

    # --------------------------------------------------------------- barrels (origin x=-6.75, 25.48, -13.38)
    br = k.piece('barrel1'); B = br.at
    br.cyl(B(0, 0, -1.2), B(0, 0, 3.0), 3.4, 10, 'dark', rot=math.pi / 10, bevel=0.1)       # breech
    br.cyl(B(0, 0, 3.0), B(0, 0, 37.0), 2.4, 10, 'steel', rot=math.pi / 10)
    for z in (15.0, 26.0):
        br.cyl(B(0, 0, z), B(0, 0, z + 1.2), 2.6, 10, 'dark', rot=math.pi / 10, bevel=0.05)
    br.cyl(B(0, 0, 36.8), B(0, 0, 41.0), 3.0, 8, 'paint2', r2=2.7, rot=math.pi / 8, bevel=0.1)  # muzzle brake
    br.cyl(B(0, 0, 37.6), B(0, 0, 38.8), 3.08, 8, 'hazard', rot=math.pi / 8)
    br.cyl(B(0, 0, 40.98), B(0, 0, 41.08), 1.5, 10, 'black')
    k.clone('barrel2', 'barrel1')
