"""Roach (CORE_T2_BOT_Roach) - Core T2 crawling bomb (kamikaze, no weapon, no corpse). TA's model: a flat armoured
box with twelve stub legs (lega1-6 right, legb1-6 left) that shuffle. Remodelled on the shared six-leg skeleton
(skeleton='hexa', walk.Hexa) with the body raised onto real legs; script ported to scripts/CORE_T2_BOT_Roach.lua.
Coordinates are ENGINE/global: X right, Y up, Z forward.
Top view (what makes the Roach): a small dark-warm oval bug - team-colour back plateau with the warhead in its middle
(ochre hazard ring, red glowing cap: it is a bomb), ochre hazard shoulder chevrons, a darker head with red eyes and two
light steel antennae swept forward, six short legs. Smaller than every other walker; no gun anywhere."""

SPLAY = 30

UNIT = dict(
    skeleton='hexa',
    skeleton_opts=dict(height=3.6, hipx=4.4, hipz=3.2),
    res=512,
    preview_pose={'rfthigh': (0, SPLAY, 0), 'lfthigh': (0, -SPLAY, 0), 'rbthigh': (0, -SPLAY, 0), 'lbthigh': (0, SPLAY, 0)},
)


def ring(y, pts):
    return [(x * s, y, z) for s in (-1, 1) for x, z in pts]


def lerp(a, b, t):
    return tuple(a[i] + (b[i] - a[i]) * t for i in range(3))


def build(k):
    k.hexa_legs(thigh='paint2', shin='dark', foot='dark', joint='dark', armour='paint', width=2.1, thick=1.7,
                knee_spike=True)

    b = k.piece('base'); A = b.at                      # origin (0, 0, 0)
    b.hull([A(*p) for p in ring(1.4, [(3.6, -6.4), (4.2, -2.0), (4.2, 3.0), (3.0, 5.8)]) +
            ring(3.6, [(4.0, -7.0), (4.6, -2.0), (4.6, 3.0), (3.4, 6.2)])], 'paint2', bevel=0.12)       # belly
    top = [(2.8, -5.4), (3.1, -2.6), (3.1, 1.8), (2.0, 4.0)]
    b.hull([A(*p) for p in ring(3.0, [(4.9, -7.8), (5.5, -3.0), (5.5, 2.6), (4.2, 6.4)]) +
            ring(5.1, [(4.4, -7.0), (4.9, -3.0), (4.9, 2.3), (3.7, 5.6)]) + ring(6.1, top)], 'paint', bevel=0.2)  # carapace
    # team plateau on the back (the warhead sits in its middle)
    b.hull([A(*p) for p in ring(6.17, [(x - 0.2, z * 0.95) for x, z in top]) + ring(6.33, [(x - 0.3, z * 0.93) for x, z in top])],
           'team', bevel=0.03)
    # hazard chevrons on the front shoulders (bomb warning), on the carapace slope 0.08 proud
    lo = [(4.9, 5.1, 2.3), (3.7, 5.1, 5.6)]           # carapace ring y 5.1, front-side segment
    hi = [(3.1, 6.1, 1.8), (2.0, 6.1, 4.0)]           # plateau ring y 6.1
    n = (0.49, 0.87, 0.0)                             # slope normal (up and out)
    pts = [lerp(lerp(lo[0], lo[1], u), lerp(hi[0], hi[1], u), t) for u in (0.1, 0.9) for t in (0.12, 0.85)]
    b.hull([A(*(p[i] + n[i] * d for i in range(3))) for p in pts for d in (0.07, 0.17)], 'hazard', bevel=0.02, mirror=True)
    # warhead: ochre hazard ring, red glowing cap
    b.cyl(A(0, 5.9, -1.4), A(0, 6.9, -1.4), 2.2, 12, 'hazard', bevel=0.06)
    b.cyl(A(0, 6.85, -1.4), A(0, 7.15, -1.4), 1.55, 12, 'dark')
    b.sphere(A(0, 7.15, -1.4), 1.25, 'lightr', segs=10, rings=5, scale=(1, 0.55, 1))
    # head, eyes, mandibles, antennae
    b.hull([A(*p) for p in ring(1.6, [(2.6, 5.0), (2.0, 8.0)]) + ring(4.4, [(2.8, 5.2), (1.8, 7.4)]) + ring(3.0, [(1.2, 8.8)])],
           'paint2', bevel=0.15)
    b.sphere(A(1.45, 3.75, 7.7), 0.55, 'lightr', segs=8, rings=4, mirror=True)
    b.hull([A(x, y, z) for x, y, z in [(0.6, 1.8, 8.4), (1.6, 1.8, 8.0), (1.0, 2.6, 8.2), (0.5, 1.9, 10.2), (0.8, 2.3, 10.0)]],
           'dark', bevel=0.05, mirror=True)
    b.cyl(A(1.1, 4.2, 7.6), A(3.6, 5.6, 11.6), 0.32, 6, 'steel', r2=0.16, mirror=True)
    # rear vent
    b.box(A(-1.6, 2.6, -8.15), A(1.6, 3.4, -7.75), 'lightr', bevel=0.0)
