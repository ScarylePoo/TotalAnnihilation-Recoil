"""Kbot Lab (CORE_T1_LAB_KbotLab) - Core T1 kbot factory. Closed it is two tall dark armoured halves (lower1/upper1,
lower2/upper2) standing over the pad with a slot between them, bridged by team door plates, their roofs hazard-capped.
On activation each upper half flips 180 deg forward off its lower (turn x), both halves slide sideways off the lane
(lower move x), the door plates slide out over them, the nano boxes (lbox/ubox) rise out of the blocks as a tower on
each side and the nano heads (gun1/gun2) swing to face the pad; the pad slides forward 15.6.
Core lab family: dark warm armoured blocks, four corner pylons with sloped buttresses and team caps, near-black lane
with ochre hazard edges, light steel pad disc, warm lights. Identity from above (open): a wide dark lane with a light
disc between two long low side blocks carrying team plates and steel nano booms, four pylons at the corners.
Pieces (COB): base, pad (move z, spin y; QueryBuildInfo), lower1/2 (move x), ldoor1/2, udoor1/2 (move x, y), upper1/2
(turn x 180), lbox1/2, ubox1/2 (move y), gun1/2 (move z, turn y), beam1/2 (empty nano emit points), blink (beacon).
All side-2 pieces are mirror clones of side 1 (the 3DO offsets are exact mirrors).
The open halves sit at x +-(32..47), i.e. outside the yardmap's `c` columns (x +-32); only the nano booms/heads
reach over the lane edge, ~19 elmo up, as the script places them.
Preview: OPEN (activatescr end state; COB x moves negated for the engine frame).
Coordinates are ENGINE/global: X right, Y up, Z forward."""
import math

UNIT = dict(
    res=2048,
    hazard_period=5.0,
    flipped=['upper1', 'upper2', 'udoor1', 'udoor2', 'ubox1', 'ubox2', 'gun1', 'gun2'],
    always_visible=['lbox1', 'lbox2', 'ubox1', 'ubox2', 'udoor1', 'udoor2'],
    wreck=dict(seed=62, drop=['upper2']),
    preview_pose={
        'lower1': {'move': (-22.25, 0, 0)}, 'lower2': {'move': (22.375, 0, 0)},
        'upper1': (180, 0, 0), 'upper2': (180, 0, 0),
        'ldoor1': {'move': (-9.125, -0.375, 0)}, 'ldoor2': {'move': (9.125, -0.375, 0)},
        'udoor1': {'move': (-9.25, 0.375, 0)}, 'udoor2': {'move': (9.125, 0.375, 0)},
        'lbox1': {'move': (0, 11.125, 0)}, 'lbox2': {'move': (0, 11.125, 0)},
        'ubox1': {'move': (0, -11.125, 0)}, 'ubox2': {'move': (0, -11.125, 0)},
        'gun1': {'move': (0, 0, 2.75), 'rot': (0, -90, 0)}, 'gun2': {'move': (0, 0, 2.75), 'rot': (0, 90, 0)},
        'pad': {'move': (0, 0, 15.625)},
    },
)

LANE = 32.0


def pylon(b, zs):
    """corner pylon on the -x side; zs = +1 front, -1 back (mirrored to +x by the caller's mirror flag)"""
    z0, z1 = sorted((31.6 * zs, 46.4 * zs))
    b.plan(0.0, 13.0, [(-47.6, z0), (-32.4, z0), (-32.4, z1), (-47.6, z1)], 'paint', bevel=0.3, top_inset=1.6,
           mirror=True)
    zc = 39.0 * zs
    b.hull([(x, y, z) for x, z in ((-46.0, zc - 6.0), (-35.6, zc - 6.0), (-35.6, zc + 6.0), (-46.0, zc + 6.0))
            for y in (12.0,)] + [(x, 27.0, z) for x, z in ((-46.0, zc - 5.4), (-35.6, zc - 5.4), (-35.6, zc + 5.4),
                                                           (-46.0, zc + 5.4))], 'paint', bevel=0.3, mirror=True)
    b.box((-45.6, 26.9, zc - 5.0), (-36.0, 27.6, zc + 5.0), 'team', bevel=0.1, mirror=True)
    # buttress fin toward the lane end
    zf = 31.8 * zs
    b.hull([(-41.0, 0.0, zf), (-38.0, 0.0, zf), (-41.0, 0.0, zf - 12.0 * zs), (-38.0, 0.0, zf - 12.0 * zs),
            (-41.0, 12.0, zf), (-38.0, 12.0, zf)], 'paint2', bevel=0.2, mirror=True)
    # ochre slab on the pylon's lane-facing slope and a warm light
    b.box((-33.0, 9.0, zc - 5.0), (-32.6, 10.6, zc + 5.0), 'lightw', bevel=0.0, mirror=True)


def build(k):
    # ------------------------------------------------------------------ base: lane, slide beds, pylons
    b = k.piece('base')
    b.box((-LANE, 0.0, -46.4), (LANE, 0.3, 46.4), 'paint2', bevel=0.05)
    b.box((-LANE, 0.0, -46.4), (-27.6, 0.45, 46.4), 'hazard', bevel=0.04, mirror=True)        # lane edges
    b.box((-27.4, 0.0, 40.4), (27.4, 0.42, 46.2), 'team', bevel=0.04)                        # exit threshold
    b.box((-47.6, 0.0, -31.2), (-LANE, 0.4, 31.2), 'dark', bevel=0.05, mirror=True)           # slide beds
    for z in (-24.0, -6.0, 6.0, 24.0):                                                         # slide rails
        b.box((-47.0, 0.3, z - 0.8), (-10.0, 0.7, z + 0.8), 'steel', bevel=0.08, mirror=True)
    for zs in (1, -1):
        pylon(b, zs)

    # ------------------------------------------------------------------ lower1 (origin -4.92, 0.15, 0): lower block
    lo = k.piece('lower1'); L = lo.at
    lo.box(L(-20.1, 0.0, -30.0), L(-5.0, 12.5, 0.0), 'paint', bevel=0.4)
    lo.box(L(-5.3, 2.0, -27.0), L(-4.9, 10.0, -3.0), 'paint2', bevel=0.08)                      # inner panel
    lo.box(L(-5.1, 7.6, -20.0), L(-4.8, 8.6, -10.0), 'lightw', bevel=0.0)
    lo.prism(L(-20.6, 0, 0)[0], L(-19.8, 0, 0)[0],                                             # outer armour skirt
             [(-29.0, 0.15), (-29.0, 8.0), (-1.0, 8.0), (-1.0, 0.15)], 'paint2', bevel=0.15)
    # ldoor1 (origin -8.75, 12.65, -6.63): team plate; closed it bridges the slot, open it lies on the lower block
    d = k.piece('ldoor1'); D = d.at
    d.box(D(-1.2, 0.4, -23.4), D(9.0, 0.9, 6.6), 'team', bevel=0.12)
    # lbox1 (origin -3.75, 1.0, -0.25): nano tower base, hidden in the block when closed
    x = k.piece('lbox1'); X = x.at
    x.box(X(-11.8, -0.5, -12.2), X(-6.4, 6.6, 0.0), 'dark', bevel=0.2)
    x.box(X(-11.4, 6.5, -11.8), X(-6.8, 6.9, -0.4), 'hazard', bevel=0.06)

    # ------------------------------------------------------------------ upper1 (origin -12.29, 12.65, 0)
    # at rest it sits on lower1 (roof up); open it is flipped 180 on x in front of lower1 (local y=0 face on top)
    u = k.piece('upper1'); U_ = u.at
    u.box(U_(-12.7, 0.0, -30.0), U_(2.3, 9.5, 0.0), 'paint', bevel=0.4)
    u.hull([U_(xx, yy, zz) for xx, yy, zz in
            [(-12.7, 9.4, -30.0), (2.3, 9.4, -30.0), (-12.7, 9.4, 0.0), (2.3, 9.4, 0.0),
             (-12.7, 12.5, -27.0), (-2.0, 12.5, -27.0), (-12.7, 12.5, -3.0), (-2.0, 12.5, -3.0)]], 'paint2', bevel=0.3)
    u.box(U_(-11.6, 12.4, -25.6), U_(-3.0, 12.9, -4.4), 'hazard', bevel=0.1)                   # roof cap (closed)
    u.box(U_(2.2, 2.0, -27.0), U_(2.6, 8.0, -3.0), 'paint2', bevel=0.08)                       # inner panel
    u.box(U_(-12.9, 1.5, -20.0), U_(-12.6, 2.5, -10.0), 'lightw', bevel=0.0)
    # udoor1 (origin -8.75, 12.65, -6.63): team plate under the upper; open it lies on the flipped upper
    e = k.piece('udoor1'); E = e.at
    e.box(E(-1.2, -0.9, -23.4), E(9.0, -0.4, 6.6), 'team', bevel=0.12)
    # ubox1 (origin -3.75, 24.3, -0.25): nano tower top + boom out to the head
    w = k.piece('ubox1'); W = w.at
    w.box(W(-11.8, -6.6, -12.2), W(-6.4, 0.5, 0.0), 'dark', bevel=0.2)
    w.box(W(-11.4, -7.0, -11.8), W(-6.8, -6.5, -0.4), 'hazard', bevel=0.06)
    w.box(W(-7.0, -7.8, -4.6), W(0.6, -5.4, -0.6), 'steel', bevel=0.2)                          # boom
    # gun1 (origin -3.25, 17.55, -3.0): nano head, emitter beam1 at (0, 0.63, -6.53)
    g = k.piece('gun1'); G = g.at
    g.box(G(-2.4, -2.4, -2.0), G(2.4, 1.6, 2.2), 'steel', bevel=0.3)
    g.cyl(G(0, 0.63, -1.8), G(0, 0.63, -5.6), 1.5, 10, 'dark', r2=1.1, rot=math.pi / 10)
    g.cyl(G(0, 0.63, -5.5), G(0, 0.63, -6.5), 1.2, 10, 'lightc', rot=math.pi / 10)

    for a, bb in (('lower', 'lower'), ('ldoor', 'ldoor'), ('lbox', 'lbox'), ('upper', 'upper'), ('udoor', 'udoor'),
                  ('ubox', 'ubox'), ('gun', 'gun')):
        k.clone(a + '2', bb + '1', mirror_x=True)

    # ------------------------------------------------------------------ pad (origin 0, 0.05, -14.38): spinning disc
    p = k.piece('pad'); Pp = p.at
    p.cyl(Pp(0, 0.0, 0), Pp(0, 0.5, 0), 15.0, 32, 'dark', bevel=0.1)
    p.cyl(Pp(0, 0.5, 0), Pp(0, 0.62, 0), 13.2, 32, 'steel')
    for a in range(4):                                           # four ochre wedges on the rim
        t = math.radians(a * 90 + 45)
        c, s = math.cos(t), math.sin(t)
        p.hull([Pp(r * math.cos(t + dt), yy, r * math.sin(t + dt)) for r in (13.3, 14.8) for dt in (-0.22, 0.22)
                for yy in (0.45, 0.6)], 'hazard', bevel=0.0)

    # ------------------------------------------------------------------ blink: beacon on the front-left pylon
    k.piece('blink').box((-41.8, 27.5, 37.0), (-39.8, 29.5, 39.0), 'lightr', bevel=0.1)
