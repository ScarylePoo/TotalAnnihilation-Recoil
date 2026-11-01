"""Energy Storage (CORE_T1_ECO_EnergyStorage) - Core energy storage. A squat dark round accumulator drum ringed by ten
tall radial cooling fins (a cog from above), warm glowing cell windows between the fins and a light steel dome on top.
Identity from above: a dark ten-toothed cog with team-capped teeth round a light dome (the Arm storage is a light
octagonal tank with a cyan core; the Core metal storage is a tall ribbed spine block).
Pieces (COB): base (drum + fins), windows (glow panels), dome - all at the origin, explode only.
Coordinates are ENGINE/global: X right, Y up, Z forward."""
import math

UNIT = dict(
    wreck=dict(seed=18, drop=['dome']),
    preview_pose={},
)

RD = 19.0          # drum radius
NF = 10


def build(k):
    b = k.piece('base')
    b.cyl((0, 0, 0), (0, 2.6, 0), 24.0, 20, 'paint2', rot=math.pi / 20, bevel=0.2)
    b.cyl((0, 2.4, 0), (0, 29.0, 0), RD, 20, 'paint2', rot=math.pi / 20, bevel=0.2)
    b.cyl((0, 28.8, 0), (0, 30.4, 0), RD - 0.4, 20, 'paint', r2=RD - 2.0, rot=math.pi / 20, bevel=0.15)
    b.cyl((0, 30.2, 0), (0, 31.0, 0), 11.6, 20, 'dark', rot=math.pi / 20, bevel=0.08)

    def fin(ang, mirror):
        a = math.radians(ang); d = (math.cos(a), math.sin(a)); p = (-d[1], d[0])
        P = lambda u, v, y: (d[0] * u + p[0] * v, y, d[1] * u + p[1] * v)
        prof = [(RD - 2.0, 0.0), (31.0, 0.0), (31.0, 3.0), (30.0, 28.0), (28.0, 31.2), (RD - 2.0, 31.2)]
        b.hull([P(u, v, y) for u, y in prof for v in (-2.7, 2.7)], 'paint', bevel=0.25, mirror=mirror)
        b.hull([P(u, v, y) for u, y in ((RD - 1.5, 31.2), (27.6, 31.2), (RD - 1.5, 31.45), (27.4, 31.45))
                for v in (-2.55, 2.55)], 'team', bevel=0.0, mirror=mirror)
        b.hull([P(u, v, y) for u, y in ((29.6, 14.0), (29.9, 14.0), (29.6, 22.0), (29.9, 22.0)) for v in (-1.2, 1.2)],
               'dark', bevel=0.0, mirror=mirror)
        # small ochre warning tab on the fin foot
        b.hull([P(u, v, y) for u, y in ((30.9, 1.0), (31.2, 1.0), (30.9, 2.6), (31.2, 2.6)) for v in (-2.0, 2.0)],
               'hazard', bevel=0.0, mirror=mirror)
    for i in range(NF):
        ang = 90 + 36 * i
        a = ang % 360
        if a in (90, 270):
            fin(a, False)
        elif 270 < a or a < 90:          # +x side: build with its -x mirror twin
            fin(a, True)

    # ------------------------------------------------------------------ windows: glowing cells between the fins
    w = k.piece('windows')
    for i in range(NF):
        ang = 90 + 36 * i + 18
        a = ang % 360
        if not (270 < a or a < 90):
            continue
        aa = math.radians(a); d = (math.cos(aa), math.sin(aa)); p = (-d[1], d[0])
        P = lambda u, v, y: (d[0] * u + p[0] * v, y, d[1] * u + p[1] * v)
        hw = RD * math.tan(math.radians(9)) - 0.3
        w.hull([P(u, v, y) for u in (RD * math.cos(math.radians(9)) - 0.1, RD * math.cos(math.radians(9)) + 0.35)
                for v in (-hw, hw) for y in (5.0, 25.0)], 'lightc', bevel=0.0, mirror=True)
        w.hull([P(u, v, y) for u in (RD * math.cos(math.radians(9)) + 0.3, RD * math.cos(math.radians(9)) + 0.7)
                for v in (-hw, hw) for y in (14.2, 15.4)], 'dark', bevel=0.0, mirror=True)

    # ------------------------------------------------------------------ dome
    dm = k.piece('dome')
    dm.sphere((0, 30.6, 0), 9.6, 'steel', segs=14, rings=7, scale=(1, 0.72, 1))
    dm.cyl((0, 36.8, 0), (0, 37.9, 0), 2.6, 10, 'lightc')
    for a in (0, 90):
        aa = math.radians(a)
        dm.hull([(math.cos(aa) * u + -math.sin(aa) * v, 30.4 + 7.0 * math.sqrt(max(0, 1 - (u / 9.8) ** 2)), math.sin(aa) * u + math.cos(aa) * v)
                 for u in (-9.8, -4.0, 0.0, 4.0, 9.8) for v in (-0.6, 0.6)], 'dark', bevel=0.0)
