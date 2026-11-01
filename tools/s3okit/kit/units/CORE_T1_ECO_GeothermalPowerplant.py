"""Geothermal Powerplant (CORE_T1_ECO_GeothermalPowerplant) - Core geothermal. Three dark hexagonal turbine towers
set in a triskelion round a squat hex core, a tall dark vent chimney rising from the core (lit mouth), two sloped
bridge roofs (the 'arms') between the towers, and on the fourth side a low annex (the 'foot') carrying three thick
light steel steam pipes down to the well.
Identity from above: a dark three-lobed cluster with team hex caps on the lobes, a black chimney mouth in the middle
and a light pipe bundle off one corner (the Arm geothermal is a long light hall with a side stack and pipe ring).
Pieces (COB): base, foot, pipes, arm1, arm2, tower - all at the origin, static. The kit's walker heuristic flags
'foot' as a leg - it is the annex, no skeleton.
Coordinates are ENGINE/global: X right, Y up, Z forward."""
import math

UNIT = dict(
    wreck=dict(seed=24, drop=['tower']),
    preview_pose={},
)

CX, CZ = 3.0, -2.0
TOWERS = ((80, 34.0), (200, 30.0), (320, 34.0))      # (angle, height)
RT, DT = 11.0, 21.0                                  # tower hex radius, distance from the core


def hexa(cx, cz, r, rot=0.0):
    return [(cx + r * math.cos(rot + i * math.pi / 3), cz + r * math.sin(rot + i * math.pi / 3)) for i in range(6)]


def tpos(ang):
    a = math.radians(ang)
    return CX + DT * math.cos(a), CZ + DT * math.sin(a)


def build(k):
    b = k.piece('base')
    b.plan(0.0, 28.0, hexa(CX, CZ, 10.0, math.pi / 6), 'paint2', bevel=0.3, top_inset=0.8)
    for ang, h in TOWERS:
        tx, tz = tpos(ang)
        rot = math.radians(ang)
        b.plan(0.0, 3.0, hexa(tx, tz, RT + 1.2, rot), 'paint2', bevel=0.25, top_inset=0.8)
        b.plan(2.9, h, hexa(tx, tz, RT, rot), 'paint', bevel=0.35, top_inset=1.2)
        b.plan(h - 0.1, h + 0.35, hexa(tx, tz, RT - 3.6, rot), 'team', bevel=0.0)
        b.plan(h * 0.55, h * 0.55 + 2.0, hexa(tx, tz, RT + 0.3 - 0.6, rot), 'dark', bevel=0.08, top_inset=0.1)
        # outward-facing black intake slot and a warm light
        a = rot; ox, oz = math.cos(a), math.sin(a); px, pz = -oz, ox
        ap = RT * math.cos(math.pi / 6)
        r_at = lambda y: ap - (y - 2.9) / (h - 2.9) * 1.2 * math.cos(math.pi / 6)
        b.hull([(tx + ox * (r_at(y) + d) + px * v, y, tz + oz * (r_at(y) + d) + pz * v) for y in (5.0, 14.0)
                for v in (-4.0, 4.0) for d in (0.05, 0.35)], 'black', bevel=0.0)
        b.hull([(tx + ox * (r_at(y) + d) + px * v, y, tz + oz * (r_at(y) + d) + pz * v) for y in (h - 5.0, h - 3.8)
                for v in (-1.4, 1.4) for d in (0.05, 0.3)], 'lightc', bevel=0.0)

    # ------------------------------------------------------------------ tower: the vent chimney on the core
    t = k.piece('tower')
    t.plan(27.9, 31.0, hexa(CX, CZ, 8.6, math.pi / 6), 'dark', bevel=0.2, top_inset=0.6)
    t.plan(30.9, 56.0, hexa(CX, CZ, 6.6, math.pi / 6), 'dark', bevel=0.2, top_inset=1.8)
    t.plan(42.0, 43.6, hexa(CX, CZ, 6.1, math.pi / 6), 'steel', bevel=0.05, top_inset=0.2)
    t.cyl((CX, 55.9, CZ), (CX, 56.6, CZ), 4.4, 6, 'lightr', rot=math.pi / 6)
    t.cyl((CX, 56.2, CZ), (CX, 56.9, CZ), 3.2, 6, 'black', rot=math.pi / 6)

    # ------------------------------------------------------------------ arms: sloped bridge roofs between towers
    def bridge(name, a0, a1):
        g = k.piece(name)
        (x0, z0), (x1, z1) = tpos(a0), tpos(a1)
        mx, mz = (x0 + x1) / 2, (z0 + z1) / 2
        dx, dz = x1 - x0, z1 - z0; L = math.hypot(dx, dz); ux, uz = dx / L, dz / L
        ox, oz = mx - CX, mz - CZ; Lo = math.hypot(ox, oz); ox, oz = ox / Lo, oz / Lo
        pts = []
        for s in (-8.0, 8.0):
            for (o, y) in ((-Lo + 7.0, 31.0), (6.0, 24.0), (6.0, 20.0), (-Lo + 7.0, 20.0)):
                pts.append((mx + ux * s + ox * o, y, mz + uz * s + oz * o))
        g.hull(pts, 'paint2', bevel=0.3)
        o0, o1 = -Lo + 7.0, 6.0
        ytop = lambda o: 31.0 + (o - o0) * (24.0 - 31.0) / (o1 - o0)
        for s0, mat in ((-6.6, 'dark'), (-1.2, 'hazard'), (4.2, 'dark')):
            g.hull([(mx + ux * s + ox * o, ytop(o) + dy, mz + uz * s + oz * o) for s in (s0, s0 + 2.4)
                    for o in (o0 + 2.0, o1 - 2.0) for dy in (0.1, 0.35)], mat, bevel=0.0)
    bridge('arm1', 200, 320)
    bridge('arm2', 320, 80 + 360)

    # ------------------------------------------------------------------ foot: low annex toward the free corner
    f = k.piece('foot')
    fa = math.radians(140); fx, fz = math.cos(fa), math.sin(fa); px, pz = -fz, fx
    F = lambda u, v, y: (CX + fx * u + px * v, y, CZ + fz * u + pz * v)
    f.hull([F(u, v, y) for (u, y) in ((6.0, 0.0), (36.0, 0.0), (36.0, 5.0), (30.0, 12.0), (6.0, 18.0))
            for v in (-11.0, 11.0)], 'paint2', bevel=0.35)
    f.hull([F(u, v, y) for (u, y) in ((33.0, 0.0), (38.0, 0.0), (33.0, 3.4), (38.0, 3.4)) for v in (-11.8, 11.8)],
           'dark', bevel=0.15)

    # ------------------------------------------------------------------ pipes: three thick steam pipes on the foot
    p = k.piece('pipes')
    for v in (-6.4, 0.0, 6.4):
        y0 = 18.0 + 2.6
        p.cyl(F(6.0, v, y0), F(30.0, v, 12.0 + 2.6), 2.6, 10, 'steel', rot=math.pi / 10)
        p.cyl(F(30.0, v, 12.0 + 2.6), F(35.0, v, 2.6), 2.6, 10, 'steel', rot=math.pi / 10)
        for u in (14.0, 24.0):
            y = y0 - (u - 6.0) * (y0 - 14.6) / 24.0
            p.cyl(F(u, v, y + 0.4), F(u + 1.6, v, y - 0.0), 3.1, 10, 'dark', rot=math.pi / 10)
