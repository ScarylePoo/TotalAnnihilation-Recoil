"""Seaplane Platform (CORE_T1_LAB_SeaplanePlatform) - Core T1 seaplane factory. Waterline 43: the water surface is
model y = 43, so at rest the factory lies submerged - a dark cross-shaped block (`platform`: two crossing arms and an
octagonal hub) set flush into four corner caissons (`base`). On activation the cross surfaces (+19) until its deck
stands 7.7 above the water: a dark deck with team arm ends round a light steel pad with ochre wedges; at the ends of
the x arm the hatches (door1/door2) flip up and drop into the bay walls and the lift posts (post1/post2) climb 31 as two
nano masts whose heads (nano1/nano2) bend over the pad.
Core lab family: dark warm armour, team caps, ochre hazard on the builder parts, light steel pad, warm lights.
Identity from above (open): a dark cross in open water with a light disc at its heart and two masts at its east/west
ends (the Arm seaplane platform is a light octagon with two towers).
Pieces (COB): base (submerged caissons), platform (move y), post1/2 (move y), nano1/2 (turn z), beam1/2 (empty nano
emit points), door1/2 (turn z, move y), pad (spin y; QueryBuildInfo).
Preview: OPEN (activatescr end state; COB z turns negated for the engine frame).
Coordinates are ENGINE/global: X right, Y up, Z forward."""
import math

UNIT = dict(
    res=2048,
    hazard_period=5.0,
    ground=False, water=43.0,
    water_lift={'platform': 19.0},
    always_visible=['post1', 'post2', 'nano1', 'nano2'],
    wreck=dict(seed=72, drop=['post2']),
    preview_pose={
        'platform': {'move': (0, 19.0, 0)},
        'door1': {'move': (0, -11.25, 0), 'rot': (0, 0, 90.0)},
        'door2': {'move': (0, -11.125, 0), 'rot': (0, 0, -90.0)},
        'post1': {'move': (0, 31.0, 0)}, 'post2': {'move': (0, 31.0, 0)},
        'nano1': (0, 0, 99.88), 'nano2': (0, 0, -99.33),
    },
)

TOP = 31.2           # deck height (platform-local; platform origin y 0.5)
AW = 20.0            # arm half-width


def build(k):
    # ------------------------------------------------------------------ base: four corner caissons (submerged)
    b = k.piece('base')
    for sx in (-1, 1):
        for sz in (-1, 1):
            pts = [(sx * 22.0, sz * 33.0), (sx * 22.0, sz * 55.0), (sx * 40.0, sz * 55.0), (sx * 55.0, sz * 40.0),
                   (sx * 55.0, sz * 22.0), (sx * 33.0, sz * 22.0)]
            b.plan(0.0, 31.0, pts, 'paint2', bevel=0.3, top_inset=0.8)
            inner = [(x * 0.92 + sx * 2.0, z * 0.92 + sz * 2.0) for x, z in pts]
            b.plan(30.9, 31.4, inner, 'paint' if sx * sz > 0 else 'hazard', bevel=0.05)

    # ------------------------------------------------------------------ platform (origin 0, 0.5, 0): the cross
    p = k.piece('platform'); P = p.at
    oc = [(30.0 * math.cos(math.pi / 8 + i * math.pi / 4), 30.0 * math.sin(math.pi / 8 + i * math.pi / 4)) for i in range(8)]
    p.plan(P(0, 0, 0)[1], P(0, TOP, 0)[1], oc, 'paint', bevel=0.35)                         # hub
    p.box(P(-AW, 0.0, -56.0), P(AW, TOP, 56.0), 'paint', bevel=0.4)                         # z arm
    for sx in (-1, 1):                                                                      # x arm (bays at the ends)
        x0, x1 = sorted((sx * 20.0, sx * 44.8))
        p.box(P(x0, 0.0, -AW), P(x1, TOP, AW), 'paint', bevel=0.4)
        xa, xb = sorted((sx * 44.8, sx * 56.0))
        p.box(P(xa, 0.0, -AW), P(xb, TOP, -15.6), 'paint', bevel=0.3)
        p.box(P(xa, 0.0, 13.1), P(xb, TOP, AW), 'paint', bevel=0.3)
        xo0, xo1 = sorted((sx * 55.4, sx * 56.0))
        p.box(P(xo0, 0.0, -15.6), P(xo1, TOP, 13.1), 'paint', bevel=0.15)
        p.box(P(xa, 0.0, -15.6), P(xb, 2.0, 13.1), 'black', bevel=0.0)                      # well floor
        for z0, z1 in ((-19.4, -16.0), (13.5, 19.4)):
            p.box(P(xa + 0.3, TOP - 0.05, z0), P(xb - 0.3, TOP + 0.4, z1), 'hazard', bevel=0.05)
        za, zb = (-AW + 1.0, AW - 1.0)
        p.box(P(min(sx * 24.0, sx * 42.0), TOP - 0.05, za), P(max(sx * 24.0, sx * 42.0), TOP + 0.35, zb), 'team',
              bevel=0.1)
        p.box(P(min(sx * 56.05, sx * 56.3), 22.0, -10.0), P(max(sx * 56.05, sx * 56.3), 23.4, 10.0), 'lightw',
              bevel=0.0)
    for sz in (-1, 1):                                                                      # z arm ends: team decks
        z0, z1 = sorted((sz * 36.0, sz * 52.0))
        p.box(P(-12.0, TOP - 0.05, z0), P(12.0, TOP + 0.35, z1), 'team', bevel=0.1)
        p.box(P(-10.0, 22.0, sz * 56.05), P(10.0, 23.4, sz * 56.3), 'lightw', bevel=0.0)
    # hatches (door1 origin 45.62, 31.75, -1.25; hinged on the inner edge)
    d = k.piece('door1'); D = d.at
    d.box(D(0.2, -0.5, -13.6), D(10.4, 0.35, 13.6), 'paint2', bevel=0.2)
    d.box(D(1.4, 0.3, -12.0), D(9.2, 0.55, 12.0), 'hazard', bevel=0.05)
    k.clone('door2', 'door1', mirror_x=True)
    # lift posts (post1 origin 51.25, 0.5, 0)
    q = k.piece('post1'); Q = q.at
    q.box(Q(-5.4, 0.0, -14.6), Q(3.9, 3.0, 12.4), 'paint2', bevel=0.2)
    q.box(Q(-3.6, 0.0, -4.0), Q(3.6, 18.5, 4.0), 'dark', bevel=0.3)
    q.box(Q(-3.2, 18.4, -3.6), Q(3.2, 18.9, 3.6), 'hazard', bevel=0.05)
    k.clone('post2', 'post1', mirror_x=True)
    # nano heads (nano1 origin 49.25, 17.5, -1.5): arm up to beam1 (0.75, 13.5, 0)
    n = k.piece('nano1'); N = n.at
    n.box(N(-2.6, -5.6, -3.6), N(4.2, 1.0, 3.6), 'steel', bevel=0.35)
    n.hull([N(x, y, z) for x, y, z in [(-1.8, 0.8, -2.6), (3.2, 0.8, -2.6), (-1.8, 0.8, 2.6), (3.2, 0.8, 2.6),
                                       (-0.6, 11.8, -1.4), (2.1, 11.8, -1.4), (-0.6, 11.8, 1.4), (2.1, 11.8, 1.4)]], 'dark',
           bevel=0.2)
    n.cyl(N(0.75, 11.6, 0), N(0.75, 13.5, 0), 1.25, 10, 'lightc')
    k.clone('nano2', 'nano1', mirror_x=True)

    # ------------------------------------------------------------------ pad (origin 0, 32.35, -1.25)
    pd = k.piece('pad'); Pd = pd.at
    pd.cyl(Pd(0, -0.7, 0), Pd(0, 0.5, 0), 25.8, 40, 'dark', bevel=0.12)
    pd.cyl(Pd(0, 0.5, 0), Pd(0, 0.62, 0), 23.6, 40, 'steel')
    for a in range(4):
        t = math.radians(a * 90 + 45)
        pd.hull([Pd(r * math.cos(t + dt), yy, r * math.sin(t + dt)) for r in (23.7, 25.6) for dt in (-0.18, 0.18)
                 for yy in (0.45, 0.6)], 'hazard', bevel=0.0)
