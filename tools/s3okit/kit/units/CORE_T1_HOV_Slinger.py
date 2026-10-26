"""Slinger (CORE_T1_HOV_Slinger) - Core anti-air hovercraft. TA's layout: four separate skirted float pods (small
pair forward, big pair aft) joined by a cross-shaped frame, a tall forward bridge tower, and an open well at the
stern holding the missile rack. Stowed, the triple-tube `launcher` lies flat on the folded `arms`; when activated
the `pole` and `turret` rise out of the well, the arms swing up and the scripts swap the visible rack for
`launcher2` (same rack, parented to the turret, aims y/x). emit1..3 (empty) are the three tube mouths.
launcher2 is a clone of launcher (identical shape and UVs).
Value groups from above: four black skirt rings (the Slinger's pattern from above), dark warm pod decks, darker
paint2 frame/well, light steel missile rack with a team lid, team plates on the bridge roof, ochre tube rims.
Coordinates are ENGINE/global: X right, Y up, Z forward. mirror=True builds the -X twin sharing UVs."""
import math

UNIT = dict(
    res=1024,
    wreck=dict(seed=13, remove=['launcher2'], pose={'turret': (0, 40, 0)}),
    preview_pose={'launcher2': 'hide'},
)


def pod(b, x0, x1, z0, z1, top, c):
    def ring(y, d):
        return [(x0 - d + c, y, z0 - d), (x1 + d - c, y, z0 - d), (x1 + d, y, z0 - d + c), (x1 + d, y, z1 + d - c),
                (x1 + d - c, y, z1 + d), (x0 - d + c, y, z1 + d), (x0 - d, y, z1 + d - c), (x0 - d, y, z0 - d + c)]
    b.hull(ring(0.0, 0.6) + ring(2.6, 1.9) + ring(4.8, 1.6) + ring(5.8, 0.8), 'tread', bevel=0.26, mirror=True)
    b.hull(ring(5.4, 0.0) + ring(top, -1.4), 'paint', bevel=0.2, mirror=True)
    b.hull(ring(5.6, 0.5) + ring(6.6, 0.4), 'steel', bevel=0.07, mirror=True)


def build(k):
    b = k.piece('base')
    # ------------------------------------------------------------------ four float pods (+X, mirrored)
    pod(b, 6.7, 17.2, -21.6, 2.5, 9.8, 3.2)    # rear, big
    pod(b, 3.4, 13.3, 6.0, 20.6, 9.6, 2.8)     # front, smaller
    # small lift fan on each rear pod
    x, z = 12.0, -9.6
    b.cyl((x, 9.2, z), (x, 10.4, z), 3.6, 14, 'dark', bevel=0.1, mirror=True)
    b.cyl((x, 10.4, z), (x, 10.45, z), 2.8, 14, 'black', mirror=True)
    for i in range(3):
        a = i * 2 * math.pi / 3 + 0.5
        ca, sa = math.cos(a), math.sin(a)
        pts = []
        for d in (0.6, 2.6):
            for s in (-0.5, 0.5):
                px, pz = x + ca * d - sa * s, z + sa * d + ca * s
                pts += [(px, 10.15, pz), (px, 10.45, pz)]
        b.hull(pts, 'steel', bevel=0.0, mirror=True)
    # team plate on each front pod (forward-pointing)
    b.hull([(5.6, y, 9.6) for y in (9.62, 9.76)] + [(11.2, y, 9.6) for y in (9.62, 9.76)] +
           [(11.2, y, 15.0) for y in (9.62, 9.76)] + [(7.6, y, 18.2) for y in (9.62, 9.76)], 'team', bevel=0.03, mirror=True)
    # ------------------------------------------------------------------ cross frame (crosses x = 0), darker
    b.box((-7.2, 5.8, -21.0), (7.2, 9.0, 2.8), 'paint2', bevel=0.14)          # well floor between rear pods
    b.box((-12.0, 6.4, 2.0), (12.0, 9.4, 6.6), 'paint2', bevel=0.14)          # cross beam
    b.box((-3.6, 5.8, 2.0), (3.6, 9.4, 22.0), 'paint2', bevel=0.14)           # keel to the bow
    # well rim (hazard: launch area)
    b.box((6.2, 9.0, -20.6), (7.0, 9.6, 1.6), 'hazard', bevel=0.03, mirror=True)
    # ------------------------------------------------------------------ forward bridge tower (crosses x = 0)
    b.hull([(x * sx, y, z) for sx in (-1, 1) for x, y, z in
            [(5.4, 9.2, 3.4), (5.4, 9.2, 16.4), (2.0, 9.2, 21.0), (4.6, 16.6, 4.2), (4.2, 16.0, 11.8),
             (2.4, 15.6, 15.0), (3.0, 19.3, 6.0), (2.6, 18.8, 10.4)]], 'paint', bevel=0.2)
    b.hull([(x * sx, y, z) for sx in (-1, 1) for x, y, z in
            [(2.2, 19.32, 6.4), (2.0, 18.84, 9.8), (2.2, 19.46, 6.4), (2.0, 18.98, 9.8)]], 'team', bevel=0.02)
    b.hull([(x * sx, y, z) for sx in (-1, 1) for x, y, z in
            [(3.6, 16.2, 12.4), (2.2, 15.3, 15.0), (3.6, 16.32, 12.52), (2.2, 15.42, 15.12)]], 'glass', bevel=0.02)
    # radar on the bridge
    b.cyl((0, 19.1, 7.0), (0, 21.0, 7.0), 0.5, 8, 'dark')
    b.box((-3.2, 21.0, 6.4), (3.2, 22.0, 7.6), 'steel', bevel=0.08)
    # lights
    b.box((-1.4, 9.4, 21.2), (1.4, 10.6, 21.8), 'lightw', bevel=0.0)
    b.box((14.6, 7.6, -22.6), (16.2, 8.6, -22.0), 'lightr', bevel=0.0, mirror=True)

    # ------------------------------------------------------------------ pole / turret / arms
    p = k.piece('pole'); P = p.at
    p.cyl(P(0, 0.0, 0), P(0, 5.6, 0), 1.9, 12, 'steel', bevel=0.05)
    t = k.piece('turret'); T = t.at
    t.cyl(T(0, 0.0, 0), T(0, 1.0, 0), 3.6, 14, 'dark', bevel=0.06)
    t.box(T(-3.4, 0.9, -3.2), T(3.4, 3.8, 2.8), 'paint', bevel=0.16)
    t.box(T(-2.6, 3.75, -2.4), T(2.6, 3.95, 2.0), 'team', bevel=0.03)
    a = k.piece('arms'); A = a.at          # two parallel arms from the turret back to the rack
    for sx in (-1, 1):
        x0, x1 = sorted((3.8 * sx, 6.8 * sx))
        a.box(A(x0, -1.1, -0.8), A(x1, 1.1, 13.4), 'steel', bevel=0.12)
    a.cyl(A(-7.0, 0, 0), A(7.0, 0, 0), 0.9, 10, 'dark')

    # ------------------------------------------------------------------ missile rack (launcher; launcher2 = clone)
    l = k.piece('launcher'); L = l.at
    l.box(L(-6.6, -1.0, -7.8), L(6.6, 3.9, 5.0), 'steel', bevel=0.22)
    l.box(L(-5.6, 3.85, -6.6), L(5.6, 4.1, 3.8), 'team', bevel=0.05)
    l.box(L(-6.4, -0.8, 4.9), L(6.4, 3.6, 5.2), 'dark', bevel=0.04)
    for x in (-4.65, 0.0, 4.65):
        l.cyl(L(x, 0.81, 5.1), L(x, 0.81, 5.8), 1.6, 12, 'hazard', bevel=0.04)
        l.cyl(L(x, 0.81, 5.8), L(x, 0.81, 5.86), 1.1, 12, 'black')
    l.box(L(-6.2, -0.6, -8.1), L(6.2, 3.2, -7.7), 'black', bevel=0.0)
    for sx in (-1, 1):
        x0, x1 = sorted((6.5 * sx, 7.1 * sx))
        l.box(L(x0, 0.2, -6.8), L(x1, 2.8, 4.0), 'dark', bevel=0.06)
    k.clone('launcher2', 'launcher')
