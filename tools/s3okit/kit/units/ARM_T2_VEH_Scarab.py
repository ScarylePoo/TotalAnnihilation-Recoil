"""Scarab (ARM_T2_VEH_Scarab) - Arm T2 mobile anti-nuke (MOBILE_ANTI_NUCLEAR_MISSILE). TA's model is a beetle: a dome
in two halves (lbody/rbody) that slide apart sideways while the launcher inside swings up 98 deg to vertical and the
interceptor leaves from `emit`. Six legs from under the dome. Remodelled on the shared six-leg skeleton (skeleton='hexa',
walk.Hexa); script ported to scripts/ARM_T2_VEH_Scarab.lua. TA's side/front plates (LFfoot, LRfoot, RFfoot, RRfoot)
were only ever exploded by the script; their shapes are part of the shell and head now.
Coordinates are ENGINE/global: X right, Y up, Z forward.
Top view (what makes the Scarab): a big round light shell split down the spine, a team band along each wing case and
a dark rim, a dark head with white eyes in front, short stubby dark legs peeking out all round. Nothing like the
Spider's long-legged two-segment body. Opened, the dark launcher with a hazard-banded white interceptor stands up out
of the split."""

SPLAY = 30

# wing-case cross-section (x >= 0, y) at full size; scaled per station along z
PROFILE = [(0.0, 21.2), (6.0, 20.4), (10.8, 18.0), (14.0, 14.4), (15.2, 11.6), (15.0, 10.4), (0.0, 10.4)]
STATIONS = [(11.0, 0.72), (7.0, 0.94), (0.0, 1.0), (-8.0, 0.97), (-14.0, 0.8), (-18.0, 0.52), (-19.6, 0.24)]

UNIT = dict(
    skeleton='hexa',
    skeleton_opts=dict(height=6.0, hipx=11.4, hipz=8.6),
    res=1024,
    wreck=dict(seed=43, drop=['rbody'], remove=[]),
    preview_pose={'rfthigh': (0, SPLAY, 0), 'lfthigh': (0, -SPLAY, 0), 'rbthigh': (0, -SPLAY, 0), 'lbthigh': (0, SPLAY, 0)},
)


def section(z, s, prof=PROFILE, x0=0.0, y0=10.4):
    return [(x0 + x * s, y0 + (y - y0) * s, z) for x, y in prof]


def surf(x, s, lift):
    """point on the scaled wing-case top at x (interpolated along the profile), lifted by `lift`"""
    pr = [(px * s, 10.4 + (py - 10.4) * s) for px, py in PROFILE[:5]]
    for (xa, ya), (xb, yb) in zip(pr, pr[1:]):
        if xa <= x <= xb:
            t = (x - xa) / (xb - xa)
            return (x, ya + (yb - ya) * t + lift)
    return pr[-1]


def build(k):
    k.hexa_legs(thigh='paint2', shin='paint2', foot='dark', joint='dark', armour='dark', width=1.9, thick=1.5,
                knee_spike=False)

    # ------------------------------------------------------------------ wing case (lbody, origin 0, 9.56, 5.62)
    c = k.piece('lbody'); C = c.at
    G = lambda p: C(p[0], p[1] - 9.56, p[2] - 5.62)          # global -> piece-relative
    c.hull([G(p) for z, s in STATIONS for p in section(z, s)], 'paint', bevel=0.3)
    # team band along the wing case (x 2.6..6.8 at full width), 0.08 above the shell
    band = []
    for z, s in STATIONS[:-1]:
        for x in (2.6 * s, 6.8 * s):
            for lift in (0.08, 0.3):
                x_, y_ = surf(x, s, lift)
                band.append(G((x_, y_, z)))
    c.hull(band, 'team', bevel=0.04)
    # dark rim along the lower outer edge (value break between the light shell and the legs)
    rim = []
    for z, s in STATIONS:
        for x, y in ((15.2 * s + 0.1, 11.6), (15.1 * s + 0.12, 10.3), (13.6 * s, 10.3), (14.0 * s + 0.1, 13.4)):
            rim.append(G((x, y, z)))
    c.hull(rim, 'paint2', bevel=0.08)
    c.hull([G((x, 10.4 + (21.2 - 10.4) * s + dy, z)) for z, s in STATIONS[1:-2] for x in (0.0, 0.5) for dy in (-0.1, 0.22)],
           'dark', bevel=0.05)                                                  # spine seam, following the shell
    k.clone('rbody', 'lbody', mirror_x=True)

    # ------------------------------------------------------------------ base (0, 9.56, 0): belly and head
    b = k.piece('base'); B = lambda x, y, z: b.at(x, y - 9.56, z)
    b.hull([B(x * s, y, z) for s in (-1, 1) for x, y, z in
            [(11.0, 4.2, -14.0), (12.6, 5.0, -6.0), (12.6, 5.0, 8.0), (10.0, 4.4, 11.0),
             (11.4, 10.4, -15.0), (13.2, 10.4, -6.0), (13.2, 10.4, 8.0), (10.4, 10.4, 11.4)]], 'dark', bevel=0.25)
    b.hull([B(x * s, y, z) for s in (-1, 1) for x, y, z in                     # head (pronotum)
            [(9.6, 4.6, 9.0), (10.2, 13.6, 9.6), (6.6, 15.2, 13.0), (7.6, 5.0, 19.0), (5.4, 11.2, 20.6), (3.6, 7.0, 23.2)]],
           'paint2', bevel=0.3)
    b.hull([B(x * s, y, z) for s in (-1, 1) for x, y, z in                     # team plate on the head
            [(5.6, 15.12, 12.6), (3.4, 12.9, 18.4), (5.5, 15.32, 12.5), (3.3, 13.1, 18.3)]], 'team', bevel=0.03)
    for x in (3.0, 5.4):                                                       # eyes
        b.sphere(B(x, 10.6 - (x - 3.0) * 0.5, 20.6 - (x - 3.0) * 0.6), 0.85, 'lightw', segs=8, rings=4, mirror=True)
    b.hull([B(x, y, z) for x, y, z in                                          # horns (mandibles), dark
            [(2.0, 5.4, 21.6), (3.6, 6.8, 20.8), (2.4, 8.0, 21.4), (1.2, 6.4, 27.2), (1.6, 7.4, 26.6)]], 'dark',
           bevel=0.1, mirror=True)

    # ------------------------------------------------------------------ launcher (0, 16.31, 7.88), hinged at its front top
    l = k.piece('launcher'); L = l.at
    l.box(L(-3.2, -8.8, -21.8), L(3.2, -7.4, -0.4), 'dark', bevel=0.12)       # cradle floor
    for sx in (-1, 1):
        l.box(L(sx * 3.2 - 0.55, -8.8, -21.8), L(sx * 3.2 + 0.55, -2.8, -0.4), 'dark', bevel=0.12, mirror=False)
    l.cyl(L(0, -0.6, -0.6), L(0, -0.6, -2.2), 1.1, 10, 'steel')               # hinge
    l.cyl(L(0, -4.6, -1.2), L(0, -4.6, -17.2), 2.3, 12, 'paint')              # interceptor body (white)
    l.cyl(L(0, -4.6, -5.0), L(0, -4.6, -8.4), 2.36, 12, 'hazard')             # warning band
    l.cyl(L(0, -4.6, -17.2), L(0, -4.6, -21.4), 2.3, 12, 'steel', r2=0.35)     # nose
    for a in (0, 1):                                                          # tail fins
        if a == 0:
            l.box(L(-3.0, -4.85, -1.2), L(3.0, -4.35, -3.8), 'paint2', bevel=0.04)
        else:
            l.box(L(-0.25, -7.2, -1.2), L(0.25, -2.0, -3.8), 'paint2', bevel=0.04)
