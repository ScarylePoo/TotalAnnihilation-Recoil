"""Floating Metal Maker (ARM_T1_SEAECO_FloatingMetalMaker) - Arm sea metal maker. Waterline 4 (the water surface is
model y = 4). A light hexagonal converter hub on three long outrigger spokes (team tops) ending in light float drums,
three short dark capacitor blocks between them - the land maker's six-spoke star, floating. On top the hub has a round
well holding the converter (dome): switched on, the script flips it 180 deg about x and its glowing cyan dome faces
up; switched off its flat light lid closes the well.
Identity from above: a light three-armed star with float drums at the tips, team spokes, a bright cyan dome in the
centre (the land maker has tall arching pylons; the Core sea maker is a dark drum with an iris on top).
Pieces (Lua script): base, dome (turn x: 180 deg on; origin 6.65, 19.52, -0.12, converter centred at local x -7).
flipped=['dome']: its rest-pose underside (the glowing dome) faces the camera when on.
Preview: ON (dome flipped).
Coordinates are ENGINE/global: X right, Y up, Z forward."""
import math

WL = 4.0
UNIT = dict(
    res=1024,
    ground=False, water=WL,
    flipped=['dome'],
    wreck=dict(seed=61, drop=['dome']),
    preview_pose={'dome': (180, 0, 0)},
)

DX = -0.35        # converter centre x (dome origin 6.65 + local -7)


def build(k):
    b = k.piece('base')
    hexa = [(11.5 * math.cos(math.pi / 6 + i * math.pi / 3), 11.5 * math.sin(math.pi / 6 + i * math.pi / 3))
            for i in range(6)]
    b.plan(0.0, 15.0, hexa, 'paint', bevel=0.35, top_inset=1.6)
    b.cyl((0, 14.8, 0), (0, 19.4, 0), 9.6, 12, 'paint2', r2=9.0, bevel=0.2)       # well rim
    b.cyl((0, 19.3, 0), (0, 19.7, 0), 9.0, 12, 'dark')
    b.cyl((DX, 15.0, -0.12), (DX, 19.75, -0.12), 7.3, 16, 'black', cap=True)      # well (dark inside)
    b.cyl((0, 2.6, 0), (0, 5.2, 0), 11.2, 6, 'dark', rot=math.pi / 6)              # waterline band
    b.box((-1.0, 11.0, 10.3), (1.0, 12.2, 10.6), 'lightc', bevel=0.0)

    def spoke(ang, mirror):
        c, s = math.cos(math.radians(ang)), math.sin(math.radians(ang))
        R = lambda u, y, w: (c * u - s * w, y, s * u + c * w)
        b.hull([R(u, y, w) for u, y0, y1 in ((8.0, 8.0, 14.0), (17.0, 7.0, 10.6)) for y in (y0, y1)
                for w in (-2.8, 2.8)], 'paint', bevel=0.25, mirror=mirror)
        b.hull([R(u, y, w) for u, yt in ((9.4, 14.0), (16.6, 10.6)) for y in (yt - 0.05, yt + 0.2)
                for w in (-2.1, 2.1)], 'team', bevel=0.0, mirror=mirror)
        cx, cz = c * 19.0, s * 19.0
        b.cyl((cx, -1.0, cz), (cx, 8.0, cz), 5.4, 12, 'paint', bevel=0.3, mirror=mirror)
        b.cyl((cx, 7.9, cz), (cx, 8.3, cz), 3.6, 12, 'team', mirror=mirror)
        b.cyl((cx, 3.2, cz), (cx, 4.6, cz), 5.65, 12, 'dark', mirror=mirror)

    def block(ang, mirror):
        c, s = math.cos(math.radians(ang)), math.sin(math.radians(ang))
        R = lambda u, y, w: (c * u - s * w, y, s * u + c * w)
        b.hull([R(u, y, w) for u in (9.0, 14.0) for y in (2.0, 9.0) for w in (-3.4, 3.4)], 'paint2', bevel=0.2,
               mirror=mirror)
        for y in (6.0, 7.6):
            b.hull([R(u, yy, w) for u in (13.9, 14.25) for yy in (y, y + 0.7) for w in (-2.6, 2.6)], 'black',
                   bevel=0.0, mirror=mirror)

    spoke(90, False); spoke(330, True)
    block(270, False); block(30, True)

    # ---------------------------------------------------------------- dome: converter (origin 6.65, 19.52, -0.12)
    d = k.piece('dome'); Dm = d.at
    ring = [(6.4 * math.cos(i * math.pi / 8), 6.4 * math.sin(i * math.pi / 8)) for i in range(16)]
    pts = []
    for t, f in ((0.0, 1.0), (1.6, 0.93), (3.2, 0.74), (4.4, 0.45), (5.0, 0.0)):
        pts += [Dm(-7.0 + x * f, -0.3 - t, z * f) for x, z in ring] if f else [Dm(-7.0, -5.3, 0.0)]
    d.hull(pts, 'lightc', bevel=0.0)
    d.hull([Dm(-7.0 + x * 1.06, y, z * 1.06) for x, z in ring for y in (-0.35, 0.3)], 'paint', bevel=0.12)
    d.hull([Dm(-7.0 + x * 0.55, y, z * 0.55) for x, z in ring for y in (0.25, 0.5)], 'paint2', bevel=0.0)
