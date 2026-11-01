"""Fusion Power Plant (CORE_T2_ECO_FusionPowerplant) - Core fusion. A massive dark hexagonal stepped platform carrying a
huge light steel containment globe (upper and lower halves, a glowing warm seam at the equator, a team polar cap)
flanked by three tall dark pentagonal field towers leaning outward, each with a team cap and a lit tip.
Identity from above: one huge light circle with a team centre on a dark hexagon, three team-capped tower tips round
it (the Arm fusion is two light domes side by side; the Core cloakable fusion is a smaller dark globe in a tripod
cage).
Pieces (COB): base, globebottom, globetop, tower1..3 - all at the origin, static.
Coordinates are ENGINE/global: X right, Y up, Z forward."""
import math

UNIT = dict(
    wreck=dict(seed=27, drop=['globetop', 'tower3']),
    preview_pose={},
)

GX, GY, GZ, GR = 0.0, 40.2, -6.7, 20.6


def hemi(piece, c, r, up, mat, segs=20, rings=6, scale=(1, 1, 1), r_extra=0.0, lat0=0.0):
    pts = []
    for j in range(rings + 1):
        lat = lat0 + (math.pi / 2 - lat0) * j / rings
        for i in range(segs if j < rings else 1):
            lon = 2 * math.pi * i / segs + math.pi / segs
            rr = (r + r_extra) * math.cos(lat)
            y = (r + r_extra) * math.sin(lat) * (1 if up else -1)
            pts.append((c[0] + rr * math.cos(lon) * scale[0], c[1] + y * scale[1], c[2] + rr * math.sin(lon) * scale[2]))
    if lat0 > 0:   # close the cap at its base ring
        pts += [(c[0], c[1] + (r + r_extra) * math.sin(lat0) * (1 if up else -1) * scale[1] * 0.98, c[2])]
    piece.hull(pts, mat, bevel=0.0)


def build(k):
    b = k.piece('base')
    hexa = lambda r, cz=0.0: [(r * math.cos(i * math.pi / 3), cz + r * math.sin(i * math.pi / 3)) for i in range(6)]
    b.plan(0.0, 4.0, hexa(42.0), 'paint2', bevel=0.35, top_inset=1.2)
    b.plan(3.9, 19.0, hexa(39.0), 'paint', bevel=0.4, top_inset=6.0)
    b.plan(18.9, 22.2, hexa(32.0), 'paint2', bevel=0.3, top_inset=1.0)
    # team plates on the three deck corners between the towers (hex vertices at 0/60/.../300 deg)
    for ang in (30, 150, 270):
        a = math.radians(ang); ox, oz = math.cos(a), math.sin(a); px, pz = -oz, ox
        pts = [(ox * u + px * v, y, oz * u + pz * v) for u in (22.6, 26.6) for v in (-9.0, 9.0) for y in (22.1, 22.45)]
        b.hull(pts, 'team', bevel=0.0)
    # dark radiator grilles on the slopes (all six faces)
    for i in range(6):
        a = math.pi / 6 + i * math.pi / 3; ox, oz = math.cos(a), math.sin(a); px, pz = -oz, ox
        ap = lambda y: (39.0 - (y - 3.9) / 15.1 * 6.0) * math.cos(math.pi / 6)
        for y0 in (7.0, 11.0, 15.0):
            b.hull([(ox * (ap(y) + d) + px * v, y, oz * (ap(y) + d) + pz * v) for y in (y0, y0 + 1.6)
                    for v in (-12.0, 12.0) for d in (0.05, 0.3)], 'black', bevel=0.0)
    b.box((-1.4, 1.0, 36.2), (1.4, 2.6, 36.5), 'lightr', bevel=0.0)

    # ------------------------------------------------------------------ the globe
    gb = k.piece('globebottom')
    hemi(gb, (GX, GY, GZ), GR, False, 'paint2', scale=(1, 0.88, 1))
    gb.cyl((GX, GY - 0.9, GZ), (GX, GY + 0.1, GZ), GR + 0.35, 20, 'lightc', rot=math.pi / 20)
    gb.cyl((GX, 21.8, GZ), (GX, 26.0, GZ), 12.0, 12, 'dark', rot=math.pi / 12, bevel=0.15)
    gt = k.piece('globetop')
    hemi(gt, (GX, GY, GZ), GR, True, 'steel')
    hemi(gt, (GX, GY, GZ), GR, True, 'team', r_extra=0.15, lat0=math.radians(46), rings=4, segs=20)
    for latd in (14, 32):     # dark hoops
        lat = math.radians(latd)
        y = GY + GR * math.sin(lat); rr = GR * math.cos(lat)
        gt.cyl((GX, y - 0.7, GZ), (GX, y + 0.7, GZ), rr + 0.3, 20, 'dark', rot=math.pi / 20)

    # ------------------------------------------------------------------ towers: pentagonal, leaning outward
    def tower(name, B, T):
        t = k.piece(name)
        t.cyl(B, T, 5.6, 5, 'paint', r2=4.6, bevel=0.2)
        L = [T[i] - B[i] for i in range(3)]
        at = lambda f: tuple(B[i] + L[i] * f for i in range(3))
        for f in (0.3, 0.6):
            t.cyl(at(f), at(f + 0.04), 6.0 - f * 1.0, 5, 'dark')
        t.cyl(at(0.97), at(1.0), 4.9, 5, 'team')
        t.cyl(at(1.0), at(1.025), 2.4, 5, 'lightr')
        t.cyl(at(-0.02), at(0.06), 7.4, 5, 'paint2', bevel=0.15)
    tower('tower1', (-17.0, 21.5, -14.0), (-30.0, 59.0, -21.0))
    k.clone('tower2', 'tower1', mirror_x=True)
    tower('tower3', (0.0, 21.5, 14.0), (0.0, 59.0, 28.0))
