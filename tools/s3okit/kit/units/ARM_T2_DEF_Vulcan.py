"""Vulcan (ARM_T2_DEF_Vulcan) - Arm rapid-fire plasma cannon (TA:CC). A splay-legged pedestal, a tall tapering column
and on top a pitching neck carrying a huge four-barrel rotary gun: four long barrels in a '+' round the spindle,
each in a boxy housing, that spin a quarter turn per shot (spindle turn z) and recoil 25 elmo.
Identity from above: a very long, thick dark gun bundle (four barrels, light housings with team tops) reaching far
forward over a light column and a light four-legged pedestal with team leg tops - the longest gun on the Arm side.
Pieces (COB): GP, Base, Turret (turn y), Neck (turn x), Spindle (turn z), Housing01..04, Barrel01..04 (move z),
Flare (emit, empty), Shell (hidden; exploded as the ejected casing).
Housing/barrel origins are not at their geometry (TA offsets): geometry is placed globally around the spindle axis
(y 64.51), barrels 11.6 elmo from it: 01 top, 02 left (-x), 03 bottom, 04 right.
Coordinates are ENGINE/global: X right, Y up, Z forward."""
import math

UNIT = dict(
    res=2048,
    wreck=dict(seed=49, drop=['Barrel02', 'Barrel04'], pose={'Turret': (0, 30, 0), 'Neck': (14, 0, 0)}),
    preview_pose={'Turret': (0, -25, 0), 'Neck': (-4, 0, 0)},
)

AX = (0.0, 64.51)          # spindle axis (x, y)
RB = 11.6                  # barrel distance from the axis
POS = {1: (0.0, 1.0), 2: (-1.0, 0.0), 3: (0.0, -1.0), 4: (1.0, 0.0)}


def octagon(r, rot=math.pi / 8):
    return [(r * math.cos(rot + i * math.pi / 4), r * math.sin(rot + i * math.pi / 4)) for i in range(8)]


def build(k):
    # ------------------------------------------------------------------ Base: pedestal with four splayed legs
    b = k.piece('Base')
    b.plan(0.0, 3.0, octagon(20.0), 'paint2', bevel=0.3, top_inset=1.0)
    b.plan(2.8, 16.4, octagon(16.6), 'paint', bevel=0.35, top_inset=3.0)
    for sx in (-1, 1):
        for sz in (-1, 1):
            c = lambda u, w: ((u - w) * 0.7071 * sx, (u + w) * 0.7071 * sz)
            pts = []
            for u, y, hw in ((10.0, 0.0, 4.6), (29.0, 0.0, 3.4), (28.0, 4.0, 2.6), (12.0, 15.0, 3.6)):
                for w in (-hw, hw):
                    x, z = c(u, w); pts.append((x, y, z))
            b.hull(pts, 'paint', bevel=0.3)
            tp = []
            for u in (14.0, 26.0):
                y = 15.0 - (u - 12.0) * 11.0 / 16.0
                for w in (-2.4, 2.4):
                    for d in (0.1, 0.28):
                        x, z = c(u, w); tp.append((x, y + d, z))
            b.hull(tp, 'team', bevel=0.0)
            x, z = c(28.6, 0)
            b.box((x - 0.8, 1.0, z - 0.8), (x + 0.8, 2.4, z + 0.8), 'dark', bevel=0.05)
    b.cyl((0, 16.0, -2.0), (0, 16.6, -2.0), 13.0, 16, 'dark', bevel=0.06)

    # ------------------------------------------------------------------ Turret: tall tapering column (origin 0, 16.17, -2.02)
    t = k.piece('Turret'); T = t.at
    t.cyl(T(0, 0, 0), T(0, 2.0, 0), 12.6, 16, 'dark', bevel=0.1)
    t.hull([T(x * sx, y, z) for sx in (-1, 1) for x, y, z in
            [(12.0, 1.8, -12.0), (12.0, 1.8, 10.0), (8.0, 1.8, 14.0), (8.0, 1.8, -15.0),
             (6.0, 40.0, -9.0), (6.0, 40.0, 1.0), (4.6, 44.6, -6.0), (4.6, 44.6, -1.0)]], 'paint', bevel=0.35)
    for sx in (-1, 1):     # team bands on the column's sloped flanks
        pts = []
        for y in (6.0, 30.0):
            f = (y - 1.8) / 38.2
            xx = 12.0 - 6.0 * f
            for z in (-10.0 + 1.0 * f, 6.0 - 5.0 * f):
                for d in (0.08, 0.26):
                    pts.append(T(sx * (xx + d), y + d * 0.15, z))
        t.hull(pts, 'team', bevel=0.0)
    for y in (16.0, 28.0):
        t.hull([T(x * sx, yy, z) for sx in (-1, 1) for x, yy, z in
                [(11.0 - (y - 1.8) * 0.157 + 0.4, y, -12.0 + (y - 1.8) * 0.08), (11.0 - (y - 1.8) * 0.157 + 0.4, y + 2.0, -12.0 + (y - 1.8) * 0.08),
                 (11.0 - (y - 1.8) * 0.157 + 0.4, y, 10.0 - (y - 1.8) * 0.2), (11.0 - (y - 1.8) * 0.157 + 0.4, y + 2.0, 10.0 - (y - 1.8) * 0.2)]],
               'dark', bevel=0.06)

    # ------------------------------------------------------------------ Neck: pitching beam (origin 0, 64.26, -15.36)
    n = k.piece('Neck'); N = n.at
    n.cyl(N(-7.0, 0, 0), N(7.0, 0, 0), 5.4, 12, 'dark', bevel=0.08)
    n.hull([N(x * sx, y, z) for sx in (-1, 1) for x, y, z in
            [(5.6, -5.6, -6.0), (5.6, 5.6, -6.0), (5.6, -5.0, 22.0), (5.6, 5.0, 22.0), (4.2, -3.6, 28.4), (4.2, 3.6, 28.4)]],
           'paint2', bevel=0.3)
    n.box(N(-2.4, 5.55, -4.0), N(2.4, 5.8, 18.0), 'team', bevel=0.03)
    # shell: ejected casing (hidden, exploded on fire) (origin 0, 76.28, 19.7)
    sh = k.piece('Shell'); H = sh.at
    sh.cyl(H(0, 0, -2.6), H(0, 0, 2.6), 1.0, 8, 'steel', bevel=0.03)

    # ------------------------------------------------------------------ Spindle: drum hub (origin 0, 64.51, 13.42)
    sp = k.piece('Spindle'); P = sp.at
    sp.cyl(P(0, 0, 0.2), P(0, 0, 27.0), 7.4, 12, 'dark', rot=math.pi / 12, bevel=0.12)
    for z in (2.0, 24.6):
        sp.cyl(P(0, 0, z), P(0, 0, z + 2.4), 15.4, 4, 'steel', rot=math.pi / 4, bevel=0.15)    # barrel clamp plates

    # ------------------------------------------------------------------ housings and barrels (global around the axis)
    for i in range(1, 5):
        ux, uy = POS[i]
        cx, cy = AX[0] + ux * RB, AX[1] + uy * RB
        h = k.piece(f'Housing0{i}')
        px, py = -uy, ux                     # tangent
        pts = []
        for z in (12.6, 30.0):
            for r in (-4.6, 4.6):
                for tt in (-4.6, 4.6):
                    pts.append((cx + ux * r + px * tt, cy + uy * r + py * tt, z))
        h.hull(pts, 'paint', bevel=0.3)
        # team on the housing's outward face and both tangential faces (one of them faces up on the side housings)
        tp = []
        for z in (14.6, 28.0):
            for tt in (-3.2, 3.2):
                for d in (4.65, 4.85):
                    tp.append((cx + ux * d + px * tt, cy + uy * d + py * tt, z))
        h.hull(tp, 'team', bevel=0.0)
        for sg in (-1, 1):
            tp = []
            for z in (14.6, 28.0):
                for r in (-3.2, 3.2):
                    for d in (4.65, 4.85):
                        tp.append((cx + ux * r + px * d * sg, cy + uy * r + py * d * sg, z))
            h.hull(tp, 'team', bevel=0.0)
        br = k.piece(f'Barrel0{i}')
        br.cyl((cx, cy, -4.6), (cx, cy, 64.0), 3.0, 10, 'dark', rot=math.pi / 10)
        for z in (36.0, 50.0):
            br.cyl((cx, cy, z), (cx, cy, z + 1.6), 3.5, 10, 'steel', rot=math.pi / 10)
        br.cyl((cx, cy, 63.4), (cx, cy, 72.6), 3.9, 8, 'steel', r2=3.5, rot=math.pi / 8, bevel=0.06)
        br.cyl((cx, cy, 72.58), (cx, cy, 72.7), 1.8, 10, 'black')
