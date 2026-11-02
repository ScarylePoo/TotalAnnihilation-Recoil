"""Big Bertha (ARM_T2_DEF_BigBertha) - Arm long-range plasma cannon. A tall tapering light tower on a buttressed
footing, a big boxy turret on top and an enormous gun: a jacketed cradle (sleeve) and a very long dark barrel with a
heavy muzzle brake reaching 120 elmo forward; it recoils 50 elmo.
Identity from above: by far the longest gun in the game - a thick dark line with light steel bands running from a light
turret with a team roof far past the footprint, over a light tower with team buttress tops.
Built on the third-party S3O's piece layout (its Lua script drives it): armbigbertha.3ds (root), base, ground (empty),
turret (turn y), sleeve (turn x), barrel (move z), flare / muzzle / barrel_back (empty emit points), cooling1, cooling2,
coolng3, cooling4 (fins on the sleeve). Geometry is placed globally (the pieces' origins are off-centre).
Coordinates are ENGINE/global: X right, Y up, Z forward."""
import math

UNIT = dict(
    res=2048, bake_res=2048,          # no 2x supersampling: machine time (see the batch report)
    wreck=dict(seed=65, drop=['barrel'], pose={'turret': (0, 25, 0), 'sleeve': (12, 0, 0)}),
    preview_pose={'turret': (0, -20, 0), 'sleeve': (-6, 0, 0)},
)

GY = 112.86                # barrel axis height (flare)
GX = 0.0


def octagon(r, rot=math.pi / 8):
    return [(r * math.cos(rot + i * math.pi / 4), r * math.sin(rot + i * math.pi / 4)) for i in range(8)]


def build(k):
    # ------------------------------------------------------------------ base: footing + tapering tower
    b = k.piece('base')
    b.plan(0.0, 4.0, octagon(31.0), 'paint2', bevel=0.3, top_inset=1.2)
    b.hull([(x, y, z) for y, r in ((3.8, 22.0), (80.0, 11.6)) for x, z in octagon(r)], 'paint', bevel=0.4)
    for sx in (-1, 1):
        for sz in (-1, 1):   # four buttress legs on the diagonals, team on their backs
            c = lambda u, w: ((u - w) * 0.7071 * sx, (u + w) * 0.7071 * sz)
            pts = []
            for u, y, hw in ((14.0, 3.8, 5.0), (31.0, 3.8, 4.0), (30.0, 9.0, 3.0), (14.0, 46.0, 3.6)):
                for w in (-hw, hw):
                    x, z = c(u, w); pts.append((x, y, z))
            b.hull(pts, 'paint2', bevel=0.35)
            tp = []
            for u in (17.0, 27.6):
                y = 46.0 - (u - 14.0) * 37.0 / 16.0
                for w in (-2.6, 2.6):
                    for d in (0.12, 0.32):
                        x, z = c(u, w); tp.append((x + d * 0.5 * sx, y + d, z + d * 0.5 * sz))
            b.hull(tp, 'team', bevel=0.0)
    for y in (30.0, 56.0):
        r = 22.0 - (y - 3.8) / 76.2 * 10.4 + 0.4
        b.hull([(x, yy, z) for yy in (y, y + 2.6) for x, z in octagon(r)], 'dark', bevel=0.08)
    b.hull([(x, y, z) for y, r in ((79.0, 13.6), (83.6, 13.0)) for x, z in octagon(r)], 'dark', bevel=0.15)
    b.box((-1.2, 40.0, 17.0), (1.2, 42.0, 17.6), 'lightc', bevel=0.0)

    # ------------------------------------------------------------------ turret: big housing (origin -0.06, 83.68, -0.18)
    t = k.piece('turret')
    t.hull([(x * sx, y, z) for sx in (-1, 1) for x, y, z in
            [(19.0, 83.8, -24.0), (19.0, 83.8, 8.0), (14.0, 83.8, 16.0), (17.0, 106.0, -22.0), (17.0, 106.0, 4.0),
             (11.0, 106.0, 12.0), (12.0, 119.0, -16.0), (12.0, 119.0, 0.0)]], 'paint', bevel=0.45)
    t.box((-9.0, 118.9, -14.0), (9.0, 119.25, -1.0), 'team', bevel=0.04)
    for sx in (-1, 1):        # team slabs on the upper side slopes
        t.hull([(sx * x, y, z) for x, y, z in
                [(16.8, 106.4, -20.0), (12.4, 118.4, -14.6), (16.8, 106.4, 2.0), (12.4, 118.4, -1.0)]] +
               [(sx * (x + 0.25), y + 0.1, z) for x, y, z in
                [(16.8, 106.4, -20.0), (12.4, 118.4, -14.6), (16.8, 106.4, 2.0), (12.4, 118.4, -1.0)]], 'team', bevel=0.0)
    t.box((-12.0, 92.0, -24.6), (12.0, 102.0, -23.9), 'black', bevel=0.0)        # rear vents
    t.cyl((0, 82.0, -2.0), (0, 84.6, -2.0), 14.4, 16, 'dark', bevel=0.1)

    # ------------------------------------------------------------------ sleeve: gun jacket (pivot 3.93, 110.08, -12.49)
    s = k.piece('sleeve')
    s.cyl((-13.0, 110.08, -12.49), (13.0, 110.08, -12.49), 4.6, 12, 'steel', bevel=0.08)     # trunnion
    s.hull([(GX + x * sx, GY + y, z) for sx in (-1, 1) for x, y, z in
            [(7.4, -7.4, -30.0), (7.4, 7.0, -30.0), (7.0, -6.6, 40.0), (7.0, 6.6, 40.0), (5.6, -5.4, 60.0), (5.6, 5.4, 60.0)]],
           'paint2', bevel=0.4)
    s.box((GX - 4.0, GY + 6.9, -24.0), (GX + 4.0, GY + 7.25, 30.0), 'team', bevel=0.05)      # team spine on the gun jacket
    # cooling fins (separate pieces in the S3O)
    for name, sx, z in (('cooling1', -1, 45.0), ('cooling2', -1, 53.0), ('coolng3', 1, 53.0), ('cooling4', 1, 45.0)):
        c = k.piece(name)
        x0, x1 = (GX + 5.4, GX + 7.2) if sx > 0 else (GX - 7.2, GX - 5.4)
        c.box((x0, GY - 3.4, z), (x1, GY + 3.4, z + 6.0), 'dark', bevel=0.08)

    # ------------------------------------------------------------------ barrel (origin = sleeve origin)
    br = k.piece('barrel')
    br.cyl((GX, GY, -39.0), (GX, GY, 112.0), 4.0, 12, 'dark', rot=math.pi / 12)
    for z in (66.0, 84.0, 100.0):
        br.cyl((GX, GY, z), (GX, GY, z + 2.4), 4.7, 12, 'steel', rot=math.pi / 12)
    br.cyl((GX, GY, 110.0), (GX, GY, 120.4), 5.8, 8, 'steel', r2=5.2, rot=math.pi / 8, bevel=0.1)     # muzzle brake
    br.cyl((GX, GY, 113.6), (GX, GY, 115.6), 6.0, 8, 'dark', rot=math.pi / 8)
    br.cyl((GX, GY, 120.38), (GX, GY, 120.5), 2.6, 12, 'black')
    br.cyl((GX, GY, -40.0), (GX, GY, -36.0), 5.4, 12, 'steel', bevel=0.1)                      # breech
