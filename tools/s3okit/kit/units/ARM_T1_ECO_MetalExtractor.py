"""Metal Extractor (ARM_T1_ECO_MetalExtractor) - Arm mex. A stepped light octagonal pad over the metal spot with a
tapering central drill column; on top a long crossbar rotor (spins on y while extracting) carrying two raked drill
legs that reach down to the pad.
Identity from above: light octagon with a dark collar ring and a long bar with team top plate and two dark drill
heads at its ends (the Core mex is a dark round pad with a three-armed claw instead).
Pieces (Lua script): base, arms (spin y), pieces (static braces, explode only in the old model).
Coordinates are ENGINE/global: X right, Y up, Z forward."""
import math

UNIT = dict(
    res=1024,
    wreck=dict(seed=11, drop=['arms']),
    preview_pose={'arms': (0, 30, 0)},
)


def octagon(r, rot=math.pi / 8):
    return [(r * math.cos(rot + i * math.pi / 4), r * math.sin(rot + i * math.pi / 4)) for i in range(8)]


def build(k):
    # ------------------------------------------------------------------ base: stepped octagon pad + column
    b = k.piece('base')
    b.plan(0.0, 2.4, octagon(25.0), 'paint2', bevel=0.2, top_inset=0.8)
    b.plan(2.3, 9.0, octagon(22.4), 'paint', bevel=0.25, top_inset=6.0)
    # team plates on the four diagonal slopes (octagon faces at 22.5+45*i deg -> faces centred on 0/45/90...)
    def face_plate(ang, mat, w=5.2):
        a = math.radians(ang); cx, cz = math.cos(a), math.sin(a); px, pz = -cz, cx
        ap0, ap1 = 22.4 * math.cos(math.pi / 8), (22.4 - 6.0) * math.cos(math.pi / 8)
        pts = []
        for y, r in ((3.2, ap0 - (3.2 - 2.3) / 6.7 * (ap0 - ap1)), (8.4, ap0 - (8.4 - 2.3) / 6.7 * (ap0 - ap1))):
            for t in (-w, w):
                for d in (0.08, 0.3):
                    pts.append((cx * (r + d) + px * t, y + d * 0.6, cz * (r + d) + pz * t))
        b.hull(pts, mat, bevel=0.0)
    for ang in (0, 45, 135, 180, 225, 315):
        face_plate(ang, 'team')
    # dark collar ring and the tapered column
    b.cyl((0, 8.8, 0), (0, 10.6, 0), 11.0, 16, 'dark', rot=math.pi / 16, bevel=0.12)
    b.cyl((0, 10.4, 0), (0, 13.0, 0), 8.6, 16, 'black', rot=math.pi / 16)
    b.cyl((0, 10.6, 0), (0, 21.0, 0), 6.4, 8, 'paint', r2=4.4, rot=math.pi / 8, bevel=0.15)
    for y in (14.0, 17.6):
        b.cyl((0, y, 0), (0, y + 1.0, 0), 6.4 - (y - 10.6) * 0.2 + 0.3, 8, 'dark', rot=math.pi / 8, bevel=0.05)
    # small red status light on the front skirt
    b.box((-1.0, 0.8, 24.1), (1.0, 1.8, 24.4), 'lightr', bevel=0.0)

    # ------------------------------------------------------------------ pieces: front/back ramps (static braces)
    p = k.piece('pieces')
    for sz in (-1, 1):
        p.hull([(x, y, z * sz) for x in (-4.4, 4.4) for (y, z) in
                ((2.0, 25.4), (2.0, 13.0), (10.4, 13.0), (9.6, 14.6))], 'paint2', bevel=0.15)
        for z0 in (17.0, 20.2, 23.2):     # dark tread ribs on the ramp
            zz = z0 * sz
            yy = 2.0 + (25.4 - z0) / 12.4 * 7.8
            p.hull([(x, y, zz + dz) for x in (-3.8, 3.8) for (y, dz) in
                    ((yy + 0.1, -0.6), (yy + 0.1, 0.6), (yy + 0.55, -0.6), (yy + 0.55, 0.6))], 'dark', bevel=0.0)

    # ------------------------------------------------------------------ arms: crossbar rotor (origin 0, 22, 0.06)
    a = k.piece('arms'); A = a.at
    a.cyl(A(0, -2.0, 0), A(0, 4.6, 0), 4.6, 8, 'dark', rot=math.pi / 8, bevel=0.12)
    a.cyl(A(0, 4.5, 0), A(0, 5.4, 0), 2.6, 8, 'lightc', rot=math.pi / 8)
    # the bar: one hull each side (mirrored), thick so it reads from above
    a.hull([A(x, y, z) for x in (4.0, 21.0) for y in (-0.4, 3.0) for z in (-3.2, 3.2)], 'paint', bevel=0.25, mirror=True)
    a.box(A(5.0, 3.0, -2.4), A(19.0, 3.25, 2.4), 'team', bevel=0.0, mirror=True)
    # drill heads at the ends (dark boxes) and raked drill legs down to the pad
    a.hull([A(x, y, z) for x in (19.6, 26.0) for y in (-2.4, 4.4) for z in (-4.4, 4.4)], 'dark', bevel=0.3, mirror=True)
    a.box(A(21.0, 4.3, -2.6), A(24.6, 4.6, 2.6), 'hazard', bevel=0.0, mirror=True)
    a.cyl(A(21.6, -2.0, 0), A(10.6, -11.0, 0), 1.6, 8, 'steel', rot=math.pi / 8, mirror=True)
    a.cyl(A(10.6, -11.0, 0), A(8.6, -12.6, 0), 2.2, 8, 'dark', r2=0.8, rot=math.pi / 8, mirror=True)
    # lighter brace from the hub to the leg
    a.cyl(A(4.2, -1.0, 0), A(15.0, -6.4, 0), 0.9, 6, 'dark', mirror=True)
