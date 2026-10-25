"""Rocko (ARM_T1_BOT_Rocko) - Arm rocket kbot. Deliberately asymmetric, like the TA original: a squat octagonal body,
a tall hexagonal rocket pod on the left arm (lmisspod; hangs muzzle-down at rest, the script swings it 90 deg forward
to fire; lbarrel is the launch tube that kicks back into the pod) and a tall slab shield on the right arm (rshield,
static). Standard biped skeleton (backwards legs, hips widened from TA's 1.95 so the legs read as two);
script ported to scripts/ARM_T1_BOT_Rocko.lua.
Coordinates are ENGINE/global: X right, Y up, Z forward.
Top view: light octagon body with a team band, light hex pod with a team cap on the left, a dark (paint2) shield
slab with a hazard edge on the right - a lopsided outline no other Arm kbot has."""
import math

UNIT = dict(
    skeleton='biped',
    skeleton_opts=dict(hipx=3.4),
    res=1024,
    wreck=dict(seed=7, drop=['rshield'], remove=[]),
    preview_pose={'lmisspod': (-90, 0, 0)},       # firing pose: pod swung forward
)


def build(k):
    k.standard_legs()

    # ------------------------------------------------------------------ torso (0, 13.67, 1.71)
    t = k.piece('torso'); A = t.at
    t.cyl(A(0, -0.8, -0.7), A(0, 1.4, -0.7), 2.6, 10, 'dark', bevel=0.08)                   # waist
    # squat octagonal body (TA's look): octagon in the front view, extruded front-to-back
    oct_ = [(2.2, 1.0), (4.6, 3.2), (4.6, 7.8), (2.4, 10.4)]
    t.hull([A(x * sx, y, z) for sx in (-1, 1) for (x, y) in oct_ for z in (-4.8, 4.6)], 'paint', bevel=0.22)
    # front chest plate (paint2) with a cyan eye strip: the "face"
    t.hull([A(x * sx, y, z) for sx in (-1, 1) for x, y, z in
            [(2.8, 3.4, 4.6), (2.8, 7.4, 4.6), (2.4, 3.8, 5.6), (2.4, 7.0, 5.6)]], 'paint2', bevel=0.1)
    t.box(A(-1.8, 6.0, 5.55), A(1.8, 6.5, 5.75), 'lightc', bevel=0.0)
    # team band across the roof, front to back
    t.hull([A(x * sx, y, z) for sx in (-1, 1) for x, y, z in
            [(1.4, 10.38, -4.2), (1.4, 10.38, 4.0), (1.35, 10.54, -4.15), (1.35, 10.54, 3.95)]], 'team', bevel=0.03)
    # dark back pack with vents
    t.box(A(-3.0, 2.6, -7.0), A(3.0, 8.4, -4.6), 'dark', bevel=0.14)
    for y in (3.6, 4.8, 6.0, 7.2):
        t.box(A(-2.4, y, -7.15), A(2.4, y + 0.45, -6.95), 'black', bevel=0.0)
    # shoulder stubs: left one carries the pod hinge, right one the shield
    t.cyl(A(4.3, 6.47, -0.85), A(7.6, 6.47, -0.85), 1.5, 8, 'dark', bevel=0.06)
    t.cyl(A(-4.3, 6.47, 0.0), A(-6.0, 6.47, 0.0), 1.5, 8, 'dark', bevel=0.06)

    # ------------------------------------------------------------------ rocket pod (7.45, 20.15, 0.85), hinge on x
    m = k.piece('lmisspod'); M = m.at
    hexr = 3.4
    m.cyl(M(3.3, 5.6, 0), M(3.3, -3.4, 0), hexr, 6, 'paint', rot=0.0, bevel=0.2)           # hex body, muzzle down
    m.cyl(M(3.3, 5.6, 0), M(3.3, 6.1, 0), 2.6, 6, 'team', bevel=0.06)                       # team cap (top at rest)
    m.cyl(M(3.3, -3.4, 0), M(3.3, -4.0, 0), 3.0, 6, 'dark', bevel=0.06)                     # muzzle collar
    m.cyl(M(0.0, 0.0, 0), M(0.6, 0.0, 0), 1.8, 10, 'dark', bevel=0.05)                      # hinge boss
    # dark armour bands around the hex (read as rings when the pod points forward)
    m.cyl(M(3.3, 2.2, 0), M(3.3, 1.2, 0), hexr + 0.12, 6, 'paint2', bevel=0.04)
    # rocket noses showing in the muzzle face, around the launch tube
    for a in range(6):
        ang = a * math.pi / 3 + math.pi / 6
        m.cyl(M(3.3 + 1.95 * math.cos(ang), -3.9, 1.95 * math.sin(ang)),
              M(3.3 + 1.95 * math.cos(ang), -4.35, 1.95 * math.sin(ang)), 0.55, 8, 'steel', r2=0.2)

    # launch tube (10.87, 16.73, 0.85): recoils +y into the pod
    b = k.piece('lbarrel'); B = b.at
    b.cyl(B(0, 2.6, 0), B(0, -4.6, 0), 1.25, 10, 'dark', bevel=0.05)
    b.cyl(B(0, -4.4, 0), B(0, -5.2, 0), 1.55, 8, 'dark', rot=math.pi / 8, bevel=0.05)
    b.cyl(B(0, -5.15, 0), B(0, -5.3, 0), 0.8, 10, 'black')

    # ------------------------------------------------------------------ shield (-6.84, 20.15, 1.71)
    s = k.piece('rshield'); S = s.at
    # tall slab, slightly curved (two hulls), outer face angled outwards; dark contrasting mass on the right
    s.hull([S(x, y, z) for x, y, z in
            [(-0.6, -6.4, -4.4), (-0.6, -6.4, 4.4), (-0.6, 8.0, -4.0), (-0.6, 8.0, 4.0),
             (-2.6, -6.0, -3.8), (-2.6, -6.0, 3.8), (-2.2, 8.0, -3.4), (-2.2, 8.0, 3.4)]], 'paint2', bevel=0.18)
    s.hull([S(x, y, z) for x, y, z in
            [(-0.6, 4.0, -4.0), (-0.6, 4.0, 4.0), (-0.6, 8.0, -4.0), (-0.6, 8.0, 4.0),
             (-2.2, 4.0, -3.6), (-2.2, 4.0, 3.6), (-2.2, 8.0, -3.4), (-2.2, 8.0, 3.4),
             (-1.4, 8.6, -3.6), (-1.4, 8.6, 3.6)]], 'paint2', bevel=0.12)
    # hazard chevron strip along the top edge (a real warning: the shield edge sweeps when the torso turns)
    s.hull([S(x, y, z) for x, y, z in
            [(-0.7, 8.62, -3.3), (-0.7, 8.62, 3.3), (-2.0, 8.62, -3.0), (-2.0, 8.62, 3.0),
             (-0.75, 8.78, -3.25), (-0.75, 8.78, 3.25), (-1.95, 8.78, -2.95), (-1.95, 8.78, 2.95)]], 'hazard', bevel=0.02)
    # bolted grip plates on the outer face
    for y in (-3.2, 1.8):
        s.box(S(-2.75, y, -2.4), S(-2.45, y + 1.6, 2.4), 'dark', bevel=0.05)
    s.cyl(S(0.4, 0, 0), S(-0.7, 0, 0), 1.6, 8, 'dark', bevel=0.05)                         # mount
