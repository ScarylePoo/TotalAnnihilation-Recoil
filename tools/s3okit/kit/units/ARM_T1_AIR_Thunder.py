"""Thunder (ARM_T1_AIR_Thunder) - Arm T1 bomber. The broadest Arm T1 plan: a long fuselage with twin canted tail fins
and a huge cranked straight wing (78 elmo span). Four VTOL lift engines on a transverse spar (`jets`) stand vertical
when landed and tilt 90 deg to horizontal thrust in flight (COB turn x). The outer wing panels (`wing1`/`wing2`) are
swing panels: they lie flush on the outer wing when landed and swing 90 deg aft in flight (COB turn y), giving the
flying bomber a broad W outline.
Pieces (TA layout): base (fuselage + fixed wing; bombs drop from base), jets (spar + 4 engines; origin x 0.28, so built
whole), vertjet1/vertjet2 (empty), wing1/wing2 (swing panels; wing1 = mirrored clone of wing2), nose (empty).
Value groups from above: light Arm wing and fuselage, dark paint2 engine nacelles + bomb-bay spine + panel rims,
near-black nozzles, team on the swing panels (the bomber's big colour blocks), cyan engine glows.
Coordinates are ENGINE/global: X right, Y up, Z forward. mirror=True builds the -X twin sharing UVs."""
import math

UNIT = dict(
    res=1024,
    wreck=dict(seed=12, drop=['wing1'], pose={'jets': (40, 0, 0)}),
    # flight pose: engines horizontal, swing panels aft
    preview_pose={'jets': (89.6, 0, 0), 'wing1': (0, -90.9, 0), 'wing2': (0, 90.2, 0)},
)

WY = 3.65      # wing mid-plane


def build(k):
    b = k.piece('base')
    # ------------------------------------------------------------------ fuselage (crosses x = 0)
    b.hull([(x * sx, y, z) for sx in (-1, 1) for x, y, z in
            [(0.6, 3.2, 35.4), (2.4, 2.0, 31.0), (2.4, 5.0, 31.0),
             (4.2, 1.2, 22.0), (4.2, 6.0, 22.0), (4.4, 1.2, -6.0), (4.4, 6.0, -6.0),
             (3.4, 1.8, -30.0), (3.4, 5.6, -30.0), (2.0, 2.6, -35.4), (2.0, 5.0, -35.4)]], 'paint', bevel=0.18)
    # bomb-bay spine: dark band along the top, readable stripe between the light wings
    b.hull([(x * sx, y, z) for sx in (-1, 1) for x, y, z in
            [(2.4, 6.0, 18.0), (2.4, 6.0, -26.0), (2.4, 6.2, 18.0), (2.4, 6.2, -26.0)]], 'paint2', bevel=0.04)
    for z in (12.0, 4.0, -4.0, -12.0, -20.0):
        b.box((-2.0, 6.2, z - 1.2), (2.0, 6.32, z + 1.2), 'dark', bevel=0.02)
    # canopy
    b.hull([(x * sx, y, z) for sx in (-1, 1) for x, y, z in
            [(1.8, 4.6, 31.0), (3.0, 6.0, 26.0), (3.0, 6.0, 20.6), (1.4, 7.6, 25.2), (1.4, 7.6, 21.6)]], 'glass', bevel=0.08)
    b.cyl((0, 3.2, 35.2), (0, 3.2, 37.6), 0.5, 10, 'dark', r2=0.2)
    # rear engine block (houses the jets spar)
    b.hull([(x * sx, y, z) for sx in (-1, 1) for x, y, z in
            [(7.0, 1.4, -8.6), (7.0, 1.4, -18.6), (7.0, 5.0, -8.6), (7.0, 5.0, -18.6),
             (4.4, 1.2, -6.0), (4.0, 1.4, -21.0), (4.4, 6.0, -6.0), (4.0, 5.6, -21.0)]], 'paint2', bevel=0.14)
    # tail nozzle
    b.cyl((0, 3.8, -33.0), (0, 3.8, -36.8), 1.9, 12, 'dark', r2=1.6, bevel=0.05)
    b.cyl((0, 3.8, -36.75), (0, 3.8, -36.9), 1.2, 12, 'lightc')
    # twin canted fins
    b.hull([(2.6, 5.2, -24.0), (3.2, 5.0, -35.0), (6.4, 12.2, -31.6), (6.8, 12.4, -36.0),
            (2.2, 5.4, -24.0), (2.8, 5.2, -35.0), (6.0, 12.3, -31.6), (6.4, 12.5, -36.0)], 'paint', bevel=0.06, mirror=True)
    b.box((6.0, 12.3, -35.6), (6.9, 12.7, -34.4), 'lightr', bevel=0.0, mirror=True)
    # tail stabilisers
    b.hull([(3.2, WY + 0.4, -26.0), (3.0, WY + 0.4, -34.0), (12.6, WY + 0.6, -32.0), (12.6, WY + 0.6, -35.4),
            (3.2, WY - 0.3, -26.0), (3.0, WY - 0.3, -34.0), (12.6, WY + 0.25, -32.0), (12.6, WY + 0.25, -35.4)],
           'paint', bevel=0.06, mirror=True)

    # ------------------------------------------------------------------ main wing (mirrored halves)
    def slab(pl, t0, t1, mat, x0, x1, dy=0.0, bevel=0.08):
        pts = []
        for x, z in pl:
            t = t0 + (t1 - t0) * (x - x0) / (x1 - x0)
            pts += [(x, WY + dy + t, z), (x, WY + dy - t, z)]
        b.hull(pts, mat, bevel=bevel, mirror=True)
    slab([(4.0, 24.0), (20.8, 21.9), (20.8, -9.4), (4.0, -9.4), (4.0, 26.0)], 1.0, 0.85, 'paint', 4.0, 20.8)
    slab([(20.7, 21.9), (35.1, 7.6), (39.3, -9.4), (20.7, -9.4)], 0.85, 0.35, 'paint', 20.7, 39.3)
    # team chevron bands along the outer leading edges (the bomber's main colour read from above)
    b.hull([(x, WY + t + d, z) for x, t, zs in ((24.0, 0.76, (17.2, 12.4)), (33.0, 0.52, (8.3, 3.5))) for z in zs
            for d in (0.04, 0.14)], 'team', bevel=0.03, mirror=True)
    # dark flap strip along the inner trailing edge (separates the wing from the engines at distance)
    b.hull([(x, WY + d, z) for x in (7.2, 20.6) for z in (-6.6, -9.2) for d in (0.88, 0.98)], 'paint2', bevel=0.0, mirror=True)
    # wing-tip nav pods
    b.cyl((39.0, WY, -0.6), (39.0, WY, -10.4), 0.65, 8, 'dark', r2=0.5, mirror=True)
    b.cyl((39.0, WY, -0.1), (39.0, WY, -0.62), 0.4, 8, 'lightw', r2=0.65, mirror=True)
    # wing-root intake fairings
    b.hull([(4.2, 4.4, 20.0), (7.2, 4.4, 18.4), (4.2, 6.2, 18.6), (6.8, 5.2, 17.6),
            (4.2, 4.4, 2.0), (7.2, 4.4, 2.0), (4.2, 6.2, 2.0), (6.8, 5.2, 2.0)], 'paint', bevel=0.12, mirror=True)
    b.box((4.4, 4.6, 19.4), (6.6, 5.7, 19.7), 'black', bevel=0.0, mirror=True)

    # ------------------------------------------------------------------ swing panel (wing2 at +x; wing1 = mirror)
    w = k.piece('wing2'); W = w.at
    out = [(0.0, 0.2), (12.3, 4.8), (5.0, 16.6), (0.0, 18.0)]
    pts = []
    for x, z in out:
        pts += [W(x, 0.95, z), W(x, 1.35, z)]
    w.hull(pts, 'paint2', bevel=0.06)
    inn = [(0.9, 1.1), (10.6, 5.0), (4.6, 15.3), (0.9, 16.6)]
    w.hull([W(x, y, z) for x, z in inn for y in (1.3, 1.44)], 'team', bevel=0.03)
    w.cyl(W(0, 0.75, 0.6), W(0, 1.6, 0.6), 0.9, 10, 'dark', bevel=0.04)     # swing pivot
    k.clone('wing1', 'wing2', mirror_x=True)

    # ------------------------------------------------------------------ jets: spar + 4 lift engines (origin 0.28, 4.08, -12.58)
    j = k.piece('jets'); J = j.at
    j.cyl(J(-19.8, 0, 0), J(19.8, 0, 0), 0.9, 10, 'dark', rot=math.pi / 10)
    for x in (-17.6, -10.0, 10.0, 17.6):
        j.cyl(J(x, -6.4, 0), J(x, 5.6, 0), 2.3, 12, 'paint2', r2=2.1, bevel=0.08)
        j.cyl(J(x, 5.6, 0), J(x, 6.4, 0), 1.9, 12, 'dark', r2=1.4, bevel=0.04)          # intake cap
        j.cyl(J(x, 6.38, 0), J(x, 6.5, 0), 1.25, 12, 'black')
        j.cyl(J(x, -6.4, 0), J(x, -7.6, 0), 2.1, 12, 'dark', r2=1.8, bevel=0.04)         # nozzle
        j.cyl(J(x, -7.55, 0), J(x, -7.7, 0), 1.3, 12, 'lightc')
        j.box(J(x - 0.5, -3.0, 2.0), J(x + 0.5, 3.4, 2.5), 'team', bevel=0.0)              # stripe (front face)
