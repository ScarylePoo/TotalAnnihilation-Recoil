"""Light Laser Tower (CORE_T1_DEF_LightLaserTower) - Core LLT. A stepped square pagoda: a broad buttressed plinth, two
narrower tiers with dark collars between, a thin swivel stem and a wide flat wedge-shaped laser head with a long thin
emitter lance.
Identity from above: concentric squares stepping in (dark plinth, team-cornered middle tier, ochre top tier) under a
light steel wedge head with a red lens - the Arm LLT is a cross of buttresses with an arrow pod instead.
Pieces (Lua script): base, stand (turn y), gun (turn x), flare (emit, empty).
Coordinates are ENGINE/global: X right, Y up, Z forward."""
import math

UNIT = dict(
    res=1024,
    wreck=dict(seed=29, drop=['gun'], pose={'stand': (0, 30, 0)}),
    preview_pose={'stand': (0, -25, 0), 'gun': (-6, 0, 0)},
)


def sq(r):
    return [(-r, -r), (r, -r), (r, r), (-r, r)]


def build(k):
    # ------------------------------------------------------------------ base: stepped pagoda
    b = k.piece('base')
    b.plan(0.0, 2.0, [(-15, -11), (-11, -15), (11, -15), (15, -11), (15, 11), (11, 15), (-11, 15), (-15, 11)],
           'paint2', bevel=0.2, top_inset=0.5)
    # cross buttresses (TA's lower block), squat and dark-warm
    b.box((-13.0, 1.8, -5.2), (13.0, 12.4, 5.2), 'paint', bevel=0.3)
    b.box((-5.2, 1.8, -13.0), (5.2, 12.4, 13.0), 'paint', bevel=0.3)
    b.plan(1.8, 17.0, sq(9.6), 'paint', bevel=0.3, top_inset=1.6)
    # team plates on the buttress tops (four arm ends)
    for ax in ('x', 'z'):
        for s in (-1, 1):
            lo, hi = (9.0 * s, 12.4, -4.2), (12.4 * s, 12.58, 4.2)
            if ax == 'z':
                lo, hi = (lo[2], lo[1], lo[0]), (hi[2], hi[1], hi[0])
            b.box(tuple(min(a, c) for a, c in zip(lo, hi)), tuple(max(a, c) for a, c in zip(lo, hi)), 'team', bevel=0.03)
    b.cyl((0, 16.6, 0), (0, 19.4, 0), 8.2, 4, 'dark', rot=math.pi / 4, bevel=0.1)          # collar
    b.plan(19.2, 27.4, sq(6.6), 'paint2', bevel=0.25, top_inset=1.0)                      # middle tier
    b.cyl((0, 27.2, 0), (0, 29.2, 0), 7.6, 4, 'dark', rot=math.pi / 4, bevel=0.1)
    b.plan(29.0, 36.9, sq(5.0), 'paint', bevel=0.22, top_inset=1.6)                       # top tier
    b.hull([(x, y, z) for x, z in sq(3.6) for y in (36.85, 37.05)], 'hazard', bevel=0.0)
    for s in (-1, 1):
        b.box((-1.2, 22.0, 6.62 * s - 0.15), (1.2, 23.6, 6.62 * s + 0.15), 'lightr', bevel=0.0)
    b.box((-2.4, 2.0, 12.9), (2.4, 8.4, 13.2), 'black', bevel=0.0)

    # ---------------------------------------------------------------- stand: swivel stem (origin 0, 36.85, 0)
    s_ = k.piece('stand'); S = s_.at
    s_.cyl(S(0, 0, 0), S(0, 1.2, 0), 3.2, 10, 'dark', bevel=0.06)
    s_.cyl(S(0, 1.2, 0), S(0, 8.4, 0), 1.6, 8, 'steel')

    # ---------------------------------------------------------------- gun: wide flat wedge head (origin 0, 45.53, 0)
    g = k.piece('gun'); G = g.at
    head = [(5.6, -3.0, -12.0), (6.0, -3.0, -4.0), (3.4, -2.6, 9.0), (1.4, -1.6, 16.0),
            (4.8, 3.2, -11.0), (5.2, 4.4, -4.0), (2.8, 2.8, 8.0), (1.2, 1.4, 15.0)]
    g.hull([G(x * sx, y, z) for sx in (-1, 1) for x, y, z in head], 'steel', bevel=0.22)
    # flared dark rear (TA's wide tail) and dark side cheeks
    g.hull([G(x * sx, y, z) for sx in (-1, 1) for x, y, z in
            [(7.4, -2.6, -14.6), (7.4, 3.2, -13.6), (5.4, -2.8, -10.4), (5.0, 3.6, -10.0)]], 'paint2', bevel=0.15)
    g.hull([G(x * sx, y, z) for sx in (-1, 1) for x, y, z in
            [(2.6, 4.25, -9.0), (2.6, 4.25, 3.0), (2.4, 4.5, -8.8), (2.4, 4.5, 2.8)]], 'team', bevel=0.02)
    g.cyl(G(0, 3.0, 6.6), G(0, 3.9, 6.0), 1.25, 10, 'lightr')
    g.box(G(-6.4, -1.2, -9.0), G(6.4, 0.8, -3.0), 'dark', bevel=0.12)
    # emitter lance to the flare
    g.cyl(G(0, 0.5, 14.6), G(0, 0.5, 23.6), 0.75, 8, 'steel')
    g.cyl(G(0, 0.5, 18.0), G(0, 0.5, 19.0), 1.1, 8, 'dark')
    g.cyl(G(0, 0.5, 23.2), G(0, 0.5, 24.0), 1.0, 8, 'lightr')
