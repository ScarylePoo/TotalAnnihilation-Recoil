"""Fusion Reactor (ARM_T2_ECO_FusionPowerplant) - Arm fusion. A broad dark platform carrying two big light reactor
domes side by side, each on a stepped square plinth and girdled by a wide team-coloured containment ring with a
glowing cyan crown; a dark conduit bridge joins them and a low annex with a team roof feeds them steel pipes.
Identity from above: two big light circles with team rings and cyan centres (twin eyes) - the Arm cloakable fusion
is two dark stepped pyramids with emitter masts; the Core fusion is one huge steel globe with three leaning towers.
Pieces (Lua script, third-party S3O layout kept): fusion.3ds (empty root), base, pieces (annex + pipes).
Coordinates are ENGINE/global: X right, Y up, Z forward."""
import math

UNIT = dict(
    wreck=dict(seed=25, drop=['pieces']),
    preview_pose={},
)

DX, DZ = 20.0, -8.0         # dome centres (+-DX, DZ)
RD = 12.6                   # dome radius


def build(k):
    b = k.piece('base')
    plat = [(-39.0, -27.0), (-35.0, -31.0), (35.0, -31.0), (39.0, -27.0), (39.0, 27.0), (35.0, 31.0), (-35.0, 31.0),
            (-39.0, 27.0)]
    b.plan(0.0, 4.0, plat, 'paint2', bevel=0.3, top_inset=1.2)
    sq = lambda cx, cz, h: [(cx - h, cz - h), (cx + h, cz - h), (cx + h, cz + h), (cx - h, cz + h)]
    # reactors (built on -x, mirrored to +x)
    b.plan(3.9, 10.0, sq(-DX, DZ, 17.0), 'paint', bevel=0.35, top_inset=1.6, mirror=True)
    b.plan(9.9, 15.0, sq(-DX, DZ, 15.0), 'paint2', bevel=0.3, top_inset=0.8, mirror=True)
    # containment ring (team) and dome
    b.cyl((-DX, 14.8, DZ), (-DX, 18.4, DZ), RD + 3.4, 20, 'team', rot=math.pi / 20, bevel=0.2, mirror=True)
    b.cyl((-DX, 14.4, DZ), (-DX, 15.4, DZ), RD + 3.8, 20, 'dark', rot=math.pi / 20, bevel=0.1, mirror=True)
    b.sphere((-DX, 16.4, DZ), RD, 'paint', segs=20, rings=10, scale=(1, 0.9, 1), mirror=True)
    b.cyl((-DX, 26.6, DZ), (-DX, 28.4, DZ), 5.2, 12, 'dark', rot=math.pi / 12, bevel=0.1, mirror=True)
    b.cyl((-DX, 28.3, DZ), (-DX, 29.6, DZ), 3.8, 12, 'lightc', r2=3.0, rot=math.pi / 12, mirror=True)
    # four dark coil clamps on the dome (on the diagonals)
    for a in (45, 135, 225, 315):
        ar = math.radians(a)
        cx, cz = -DX + math.cos(ar) * (RD - 1.0), DZ + math.sin(ar) * (RD - 1.0)
        b.cyl((cx, 17.0, cz), (-DX + math.cos(ar) * 6.0, 25.2, DZ + math.sin(ar) * 6.0), 1.5, 8, 'dark', mirror=True)
    # conduit bridge between the reactors
    b.box((-4.0, 3.9, DZ - 7.0), (4.0, 14.0, DZ + 7.0), 'dark', bevel=0.3)
    b.cyl((-6.0, 11.0, DZ), (6.0, 11.0, DZ), 3.0, 10, 'steel', rot=math.pi / 10)
    b.box((-3.0, 13.9, DZ - 5.0), (3.0, 14.3, DZ + 5.0), 'hazard', bevel=0.0)
    # rear lights
    b.box((-1.2, 1.0, -30.9), (1.2, 2.4, -30.6), 'lightr', bevel=0.0)

    # ------------------------------------------------------------------ pieces: front annex + feed pipes
    p = k.piece('pieces')
    p.plan(3.9, 12.0, [(-15.0, 12.0), (15.0, 12.0), (15.0, 29.0), (-15.0, 29.0)], 'paint', bevel=0.35, top_inset=1.2)
    p.box((-12.0, 11.9, 14.6), (12.0, 12.3, 26.4), 'team', bevel=0.0)
    p.box((-4.0, 12.2, 17.0), (4.0, 15.0, 24.0), 'dark', bevel=0.2)
    for x0 in (-13.0, -6.0, 1.0, 8.0):
        p.box((x0, 5.0, 28.75), (x0 + 4.0, 10.0, 29.1), 'black', bevel=0.0)
    for sx in (-1, 1):
        p.cyl((sx * 13.0, 8.0, 18.0), (sx * 24.0, 8.0, 18.0), 2.2, 10, 'steel', rot=math.pi / 10)
        p.cyl((sx * 24.0, 8.0, 18.0), (sx * 24.0, 8.0, 8.0), 2.2, 10, 'steel', rot=math.pi / 10)
        p.cyl((sx * 24.0, 8.0, 8.0), (sx * 24.0, 12.0, 6.0), 2.2, 10, 'steel', rot=math.pi / 10)
        p.cyl((sx * 24.0, 8.0, 13.6), (sx * 24.0, 8.0, 15.0), 2.8, 10, 'dark', rot=math.pi / 10)
        p.box((sx * 30.0 - 4.0, 3.9, 14.0), (sx * 30.0 + 4.0, 9.0, 26.0), 'paint2', bevel=0.3)
        p.box((sx * 30.0 - 3.0, 8.9, 16.0), (sx * 30.0 + 3.0, 9.3, 24.0), 'dark', bevel=0.0)
