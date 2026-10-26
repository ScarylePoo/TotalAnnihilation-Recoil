"""Nixer (CORE_T1_HOV_Nixer) - Core hover rocket launcher. Broad faceted hull (TA's stepped multi-lobed plan) on a
black skirt; a sunken launcher well in the middle of the deck holds a twin-pod rocket launcher on a scissor lift:
on activation `arm1` (pivot at deck centre) and `arm2` (pivot at its rear end) unfold and the `launcher` rides up and
forward; lmispoint/rmispoint (empty) are the rocket exits at the two pod mouths. Two big lift fans flank the bow.
Value groups from above: black skirt, dark warm faceted hull, darker paint2 launcher well, the two rocket pods as
light steel blocks with team lids (the Nixer's top read: two bright parallel slabs), ochre hazard pod mouths,
dark fan discs with light blades at the bow corners.
Coordinates are ENGINE/global: X right, Y up, Z forward. mirror=True builds the -X twin sharing UVs."""
import math

UNIT = dict(
    res=1024,
    wreck=dict(seed=10, drop=['launcher']),
    preview_pose={},
)

PLAN = [(1.0, 23.4), (8.3, 24.2), (16.4, 15.8), (20.6, 5.1), (20.6, -6.7), (16.8, -16.5), (8.5, -24.8), (1.0, -23.6)]


def ring(y, d=0.0):
    out = []
    for x, z in PLAN:
        L = math.hypot(x - 4, z) or 1
        p = (x + (x - 4) / L * d, y, z + z / L * d)
        out += [p, (-p[0], y, p[2])]
    return out


def build(k):
    b = k.piece('base')
    # ------------------------------------------------------------------ skirt
    b.hull(ring(0.0, 0.0) + ring(2.6, 1.6) + ring(4.8, 1.2) + ring(6.2, 0.2), 'tread', bevel=0.3)
    # ------------------------------------------------------------------ hull (two tiers, faceted)
    b.hull(ring(5.8, -0.6) + ring(9.5, -1.6), 'paint', bevel=0.2)
    b.hull(ring(5.6, 0.0) + ring(6.8, -0.1), 'steel', bevel=0.08)
    # upper tier: side decks either side of the well (+X, mirrored)
    b.hull([(11.6, 9.4, -21.0), (17.0, 9.4, -15.6), (19.0, 9.4, -5.4), (19.0, 9.4, 4.0), (14.6, 9.4, 14.6), (11.6, 9.4, 15.6),
            (11.8, 13.2, -16.6), (15.2, 13.2, -12.8), (16.2, 13.2, -4.6), (16.2, 13.2, 3.0), (12.2, 13.2, 9.0), (11.8, 13.2, 10.0)],
           'paint', bevel=0.2, mirror=True)
    # ochre hazard chevron on the outer edge of each side deck
    b.hull([(15.6, 13.24, -1.6), (15.6, 13.24, 2.8), (14.2, 13.24, -1.6), (14.2, 13.24, 3.4),
            (15.6, 13.38, -1.6), (15.6, 13.38, 2.8), (14.2, 13.38, -1.6), (14.2, 13.38, 3.4)], 'hazard', bevel=0.02, mirror=True)
    # launcher well walls + floor (darker)
    b.box((-11.0, 9.4, -20.4), (11.0, 10.4, 12.0), 'paint2', bevel=0.12)
    b.box((-11.6, 9.4, 11.0), (11.6, 12.2, 13.6), 'paint', bevel=0.16)             # well front wall
    # bow: armoured prow block with a sensor dome and lights
    b.hull([(x * sx, y, z) for sx in (-1, 1) for x, y, z in
            [(8.2, 9.4, 13.4), (8.2, 9.4, 21.6), (3.2, 9.4, 23.6), (6.0, 15.0, 13.6), (2.6, 16.2, 13.6), (2.4, 13.0, 20.6)]],
           'paint', bevel=0.2)
    b.sphere((0, 15.6, 15.2), 2.0, 'glass', segs=12, rings=6, scale=(1, 0.7, 1))
    b.box((3.6, 7.0, 22.6), (6.4, 8.6, 23.6), 'dark', bevel=0.05, mirror=True)
    b.hull([(3.8, 7.2, 23.5), (6.2, 7.2, 23.2), (3.8, 8.4, 23.5), (6.2, 8.4, 23.2),
            (3.8, 7.2, 23.62), (6.2, 7.2, 23.32), (3.8, 8.4, 23.62), (6.2, 8.4, 23.32)], 'lightw', bevel=0.0, mirror=True)
    # lift fans flanking the bow
    x, z = 13.4, -6.8
    b.cyl((x, 12.6, z), (x, 14.0, z), 3.3, 16, 'dark', bevel=0.12, mirror=True)
    b.cyl((x, 14.0, z), (x, 14.05, z), 2.5, 16, 'black', mirror=True)
    for i in range(4):
        a = i * math.pi / 2 + 0.3
        ca, sa = math.cos(a), math.sin(a)
        pts = []
        for d in (0.7, 2.3):
            for s in (-0.55, 0.55):
                px, pz = x + ca * d - sa * s, z + sa * d + ca * s
                pts += [(px, 13.75, pz), (px, 14.05, pz)]
        b.hull(pts, 'steel', bevel=0.0, mirror=True)
    b.cyl((x, 13.7, z), (x, 14.4, z), 0.9, 10, 'steel', bevel=0.05, mirror=True)
    # stern exhaust grille + lights
    b.box((-6.4, 6.6, -24.6), (6.4, 9.2, -23.4), 'dark', bevel=0.08)
    b.box((-6.0, 7.0, -24.75), (6.0, 8.8, -24.5), 'black', bevel=0.0)
    b.box((12.0, 7.6, -20.6), (14.0, 8.6, -20.0), 'lightr', bevel=0.0, mirror=True)
    # antenna
    b.cyl((-17.2, 13.2, -6.0), (-17.2, 14.0, -6.0), 0.35, 8, 'dark')
    b.cyl((-17.2, 14.0, -6.0), (-17.2, 21.0, -6.0), 0.09, 6, 'steel', r2=0.04)
    b.cyl((-17.2, 21.0, -6.0), (-17.2, 21.2, -6.0), 0.14, 6, 'lightr')

    # ------------------------------------------------------------------ scissor lift
    a1 = k.piece('arm1'); A = a1.at
    a1.cyl(A(-2.6, 0.6, 0), A(2.6, 0.6, 0), 1.0, 10, 'dark', bevel=0.04)
    a1.box(A(-1.6, 0.0, -11.8), A(1.6, 2.6, 0.4), 'steel', bevel=0.12)
    a2 = k.piece('arm2'); C = a2.at
    a2.cyl(C(-2.6, 0.6, 0), C(2.6, 0.6, 0), 1.0, 10, 'dark', bevel=0.04)
    a2.box(C(-1.4, 0.2, -0.4), C(1.4, 2.6, 10.8), 'dark', bevel=0.12)

    # ------------------------------------------------------------------ launcher (two rocket pods on a cradle)
    l = k.piece('launcher'); L = l.at
    l.box(L(-2.6, -2.4, -6.4), L(2.6, -0.6, 12.8), 'dark', bevel=0.12)           # cradle spine
    for sx in (-1, 1):   # (launcher origin x = 0, but pods built explicitly so each keeps its own team lid UV)
        x0, x1 = sorted((2.4 * sx, 9.2 * sx))
        l.box(L(x0, -2.6, -1.6), L(x1, 3.0, 19.0), 'steel', bevel=0.22)
        l.box(L(x0 + 0.6, 2.95, -0.2), L(x1 - 0.6, 3.2, 16.8), 'team', bevel=0.05)
        # side fin
        xf0, xf1 = sorted((9.1 * sx, 11.0 * sx))
        l.box(L(xf0, -1.4, 2.0), L(xf1, 1.6, 14.8), 'dark', bevel=0.1)
        # front face: 2x2 rocket tubes around the mispoint (x +-5.5, y 0, z 18.98 global offset -> launcher z ~19?)
        l.box(L(x0 + 0.3, -2.2, 18.9), L(x1 - 0.3, 2.6, 19.2), 'hazard', bevel=0.04)
        for dx in (-1.6, 1.6):
            for dy in (-1.0, 1.4):
                cx = 5.8 * sx + dx
                l.cyl(L(cx, dy, 19.1), L(cx, dy, 19.6), 1.05, 10, 'dark', bevel=0.03)
                l.cyl(L(cx, dy, 19.6), L(cx, dy, 19.65), 0.7, 10, 'black')
        # rear exhaust
        l.box(L(x0 + 0.5, -2.0, -1.9), L(x1 - 0.5, 2.4, -1.5), 'black', bevel=0.0)
