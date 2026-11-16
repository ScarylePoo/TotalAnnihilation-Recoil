"""Galactic Gate (ARM_GalacticGate) - Arm campaign objective, a static "space teleporter". TA's layout kept: a big
light dome over an octagonal teleport chamber at the rear, a glowing cyan portal in its front face, three steel
conduits running forward to a stepped control block with a team roof hatch. A wide dark skirt under the chamber
carries team wing plates and four cyan beacons.
Identity from above: one big light dome with a team cap and a cyan ring on a wide dark octagon, a smaller light
block in front joined by three bright conduits (the Core gate is a four-legged pylon with a horizontal drum).
Pieces (TA armgate): base, turret (portal), dish (dome), door (roof hatch). plate/arm/gun/flap1-3 were a pop-up gun
buried under the control block that no script ever raised: kept as empty pieces. No baseplate.
Coordinates are ENGINE/global: X right, Y up, Z forward."""
import math

UNIT = dict(
    wreck=dict(seed=34, drop=['turret']),
    preview_pose={},
    hazard_period=5,
)

CZ = -20.0          # chamber centre z (the turret piece's origin)
RC = 13.0           # chamber drum radius
DY = 18.8           # dome springline


def oct_(r, cx, cz, sx=1.0, sz=1.0):
    return [(cx + sx * r * math.cos(math.pi / 8 + i * math.pi / 4), cz + sz * r * math.sin(math.pi / 8 + i * math.pi / 4))
            for i in range(8)]


def cap(piece, c, r, lat0, mat, segs=16, rings=3, scale=1.0):
    """spherical cap above latitude lat0 of a sphere (centre c, radius r)"""
    pts = []
    for j in range(rings + 1):
        lat = lat0 + (math.pi / 2 - lat0) * j / rings
        for i in range(segs if j < rings else 1):
            lon = 2 * math.pi * i / segs + math.pi / segs
            rr = r * math.cos(lat)
            pts.append((c[0] + rr * math.cos(lon), c[1] + r * math.sin(lat) * scale, c[2] + rr * math.sin(lon)))
    piece.hull(pts, mat, bevel=0.0)


def build(k):
    b = k.piece('base')
    # ------------------------------------------------------------------ chamber skirt and drum
    skirt = [(-27.0, -24.0), (-20.0, -31.0), (20.0, -31.0), (27.0, -24.0), (27.0, -12.0), (18.0, -5.0),
             (-18.0, -5.0), (-27.0, -12.0)]
    b.plan(0.0, 5.0, skirt, 'paint2', bevel=0.35, top_inset=1.5)
    for sx in (-1,):   # team wing plates on the skirt top (mirrored to +x)
        b.hull([(sx * x, y, z) for x in (15.5, 24.0) for z in (-25.0, -11.0) for y in (4.95, 5.35)], 'team',
               bevel=0.0, mirror=True)
        # cyan beacons on the skirt corners, front and back
        for z in (-27.5, -8.0):
            b.cyl((sx * 21.5, 4.9, z), (sx * 21.5, 7.4, z), 1.6, 8, 'dark', rot=math.pi / 8, mirror=True)
            b.cyl((sx * 21.5, 7.3, z), (sx * 21.5, 8.6, z), 1.1, 8, 'lightc', rot=math.pi / 8, mirror=True)
    b.plan(4.9, DY, oct_(RC, 0.0, CZ), 'paint', bevel=0.35, top_inset=0.6)
    # dark buttresses on the drum diagonals
    for a in (135, 225):
        ar = math.radians(a)
        ox, oz = math.cos(ar), math.sin(ar)
        px, pz = -oz, ox
        pts = []
        for (d, y) in ((RC - 1.0, 5.0), (RC - 1.0, 16.0), (RC + 3.5, 5.0), (RC + 0.8, 13.0)):
            for v in (-1.6, 1.6):
                pts.append((ox * d + px * v, y, CZ + oz * d + pz * v))
        b.hull(pts, 'dark', bevel=0.2, mirror=True)
    for a in (270,):   # rear buttress (on x = 0, whole)
        pts = []
        for (d, y) in ((RC - 1.0, 5.0), (RC - 1.0, 16.0), (RC + 3.5, 5.0), (RC + 0.8, 13.0)):
            for v in (-1.6, 1.6):
                pts.append((v, y, CZ - d))
        b.hull(pts, 'dark', bevel=0.2)
    b.box((-1.4, 1.2, -31.0), (1.4, 2.8, -30.7), 'lightr', bevel=0.0)

    # ------------------------------------------------------------------ conduits to the control block
    for x in (-4.5, 0.0, 4.5):
        b.cyl((x, 6.5, -8.5), (x, 6.5, 12.0), 1.5, 10, 'steel', rot=math.pi / 10)
    for z in (-2.0, 5.0):
        b.box((-7.0, 0.0, z - 1.4), (7.0, 5.6, z + 1.4), 'dark', bevel=0.2)
        b.box((-6.0, 7.9, z - 0.5), (6.0, 8.4, z + 0.5), 'lightc', bevel=0.0)

    # ------------------------------------------------------------------ control block (stepped)
    b.plan(0.0, 7.0, [(-12.5, 8.0), (12.5, 8.0), (12.5, 31.0), (-12.5, 31.0)], 'paint2', bevel=0.35, top_inset=2.0)
    b.plan(6.9, 17.5, [(-7.5, 12.0), (7.5, 12.0), (7.5, 27.5), (-7.5, 27.5)], 'paint', bevel=0.3, top_inset=2.6)
    # sloped front windows and side vents
    b.hull([(x, y, z) for x in (-5.0, 5.0) for (y, z) in ((9.0, 26.0), (9.0, 26.4), (15.0, 24.2), (15.0, 24.6))],
           'glass', bevel=0.0)
    for sx in (-1,):
        b.hull([(sx * x, y, z) for x in (9.6, 10.0) for y in (2.0, 5.0) for z in (12.0, 27.0)], 'black', bevel=0.0,
               mirror=True)
    b.box((-12.6, 1.2, 30.9), (-10.0, 2.6, 31.2), 'lightw', bevel=0.0)
    b.box((10.0, 1.2, 30.9), (12.6, 2.6, 31.2), 'lightw', bevel=0.0)

    d = k.piece('door')
    d.box((-4.4, 17.4, 15.4), (4.4, 18.0, 23.8), 'team', bevel=0.1)
    d.box((-1.0, 17.9, 16.6), (1.0, 18.5, 22.6), 'lightc', bevel=0.0)

    # ------------------------------------------------------------------ dome (dish) + cyan springline ring
    s = k.piece('dish')
    c = (0.0, DY, CZ)
    s.sphere(c, RC, 'paint', segs=16, rings=8, scale=(1, 0.98, 1))
    s.cyl((0.0, DY - 0.2, CZ), (0.0, DY + 0.9, CZ), RC + 0.45, 16, 'lightc', rot=math.pi / 16)
    yr = DY + 6.5
    s.cyl((0.0, yr - 0.6, CZ), (0.0, yr + 0.6, CZ), math.sqrt(RC ** 2 - (6.5 / 0.98) ** 2) + 0.55, 16, 'dark',
          rot=math.pi / 16)
    cap(s, c, RC + 0.12, math.radians(52), 'team', segs=16, rings=3, scale=0.98)
    s.cyl((0.0, DY + RC * 0.98 - 0.4, CZ), (0.0, DY + RC * 0.98 + 1.4, CZ), 2.2, 8, 'lightc', rot=math.pi / 8)

    # ------------------------------------------------------------------ portal (turret) in the chamber's front face
    t = k.piece('turret')
    zf = CZ + RC * math.cos(math.pi / 8)        # drum's front face
    t.box((-8.0, 4.9, zf - 2.0), (8.0, 21.0, zf + 1.8), 'dark', bevel=0.3)
    t.box((-5.5, 6.5, zf + 1.7), (5.5, 18.5, zf + 2.1), 'lightc', bevel=0.0)
    t.box((-9.0, 20.8, zf - 3.0), (9.0, 23.0, zf + 2.6), 'paint2', bevel=0.3)
    for sx in (-1, 1):
        t.box((sx * 7.0 - 1.0, 4.9, zf + 1.7), (sx * 7.0 + 1.0, 20.8, zf + 3.0), 'steel', bevel=0.15)
