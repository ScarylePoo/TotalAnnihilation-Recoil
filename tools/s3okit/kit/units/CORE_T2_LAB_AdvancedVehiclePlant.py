"""Advanced Vehicle Plant (CORE_T2_LAB_AdvancedVehiclePlant) - Core T2 vehicle factory. Closed: three massive dark
wedge blocks (wing1 left, wing2 back, wing3 right) meet over the pad like a three-pointed star, each with a team top
plate and an ochre-striped nose, between two tall back corner towers (team caps, red beacons: blink) and two front
pylons; two octagonal drawer pillars stand in the inside corners. On activation each wedge flips 180 deg end over end
on its mid-height pivot (wing1/3 turn z, wing2 turn x) so its nose points outward and its underside (another team
plate) becomes the top; the drawers rise 20.5 and their nano guns (gun1/gun2) slide in toward the pad, which moves
23 forward.
Core lab family (T2 = taller, more parts): dark warm armour, towers/pylons with team caps, near-black lane with ochre
hazard edges, light steel pad, warm lights. Identity from above (open): a dark three-pointed star of wedges pointing
outward round a light disc, two tall towers at the back corners (the T1 vehicle plant is a split rotunda).
Pieces (COB): base, wing1..3 (turn), drawer1/2 (move y), gun1/2 (move x, z), beam1/2 (empty nano emit points), blink
(beacons), pad (move z; QueryBuildInfo).
Preview: OPEN (activatescr end state; COB z turns and x moves negated for the engine frame).
Coordinates are ENGINE/global: X right, Y up, Z forward."""
import math

UNIT = dict(
    res=2048,
    hazard_period=5.0,
    flipped=['wing1', 'wing2', 'wing3'],
    always_visible=['gun1', 'gun2'],
    wreck=dict(seed=76, drop=['wing2']),
    preview_pose={
        'wing1': (0, 0, 179.99), 'wing2': (-179.46, 0, 0), 'wing3': (0, 0, -179.46),
        'drawer1': {'move': (0, 20.625, 0)}, 'drawer2': {'move': (0, 20.5, 0)},
        'gun1': {'move': (7.75, 0, 7.875)}, 'gun2': {'move': (-7.75, 0, 7.75)},
        'pad': {'move': (0, 0, 23.0)},
    },
)


def wedge(w, X):
    """a wing block in its own frame via X(lx, ly, lz) -> global; long axis +lx (nose), height +-12.3, width +-lz"""
    # the block keeps 0.9 off the ground at rest: its underside is the TOP once flipped, and faces below y 0.35
    # are culled as ground contact
    H = 11.4
    body = [(-6.2, -H, -17.8), (-6.2, -H, 17.8), (6.1, -H, -17.8), (6.1, -H, 17.8), (27.4, -H, -6.3), (27.4, -H, 6.3)]
    top = [(x, -y, z) for x, y, z in body]
    w.hull([X(*p) for p in body + top], 'paint', bevel=0.5)
    for s in (1, -1):                                                         # team plates top and underside
        w.hull([X(x, s * H + s * dy, z) for dy in (-0.05, 0.4) for x, z in
                ((-5.6, -17.0), (-5.6, 17.0), (6.4, -17.0), (6.4, 17.0), (25.2, -6.4), (25.2, 6.4))], 'team',
               bevel=0.1)
    for s in (1, -1):                                                         # ochre nose stripes, dark side bands
        w.hull([X(x, y, z) for x in (26.0, 27.6) for y in (-9.6, 9.6) for z in (-5.6, 5.6)], 'hazard',
               bevel=0.08)
        w.hull([X(x, y, s * zz) for x, zz in ((6.4, 17.85), (25.0, 7.2)) for y in (-6.0, 6.0)]
               + [X(x, y, s * (zz - 0.6)) for x, zz in ((6.4, 17.85), (25.0, 7.2)) for y in (-6.0, 6.0)], 'paint2',
               bevel=0.1)
        w.box(X(-6.6, -2.0, s * 9.0 - 3.0), X(-6.1, 2.0, s * 9.0 + 3.0), 'lightw', bevel=0.0)


def build(k):
    # ------------------------------------------------------------------ base: lane, towers, pylons
    b = k.piece('base')
    b.box((-32.0, 0.0, -16.0), (32.0, 0.3, 48.0), 'paint2', bevel=0.05)
    b.box((-32.0, 0.0, -16.0), (-28.4, 0.45, 48.0), 'hazard', bevel=0.04, mirror=True)
    b.box((-62.0, 0.0, -58.0), (62.0, 0.25, 32.0), 'dark', bevel=0.05)                         # apron
    for sx in (-1, 1):
        x0, x1 = sorted((sx * 42.0, sx * 62.0))
        b.plan(0.0, 14.0, [(x0, -56.0), (x1, -56.0), (x1, -32.0), (x0, -32.0)], 'paint', bevel=0.35, top_inset=1.8)
        xc = sx * 54.0
        b.hull([(x, 13.5, z) for x in (xc - 7.0, xc + 7.0) for z in (-51.0, -36.0)]
               + [(x, 27.7, z) for x in (xc - 4.0, xc + 4.0) for z in (-47.0, -40.0)], 'paint', bevel=0.3)
        b.box((xc - 3.8, 27.6, -46.8), (xc + 3.8, 28.1, -40.2), 'team', bevel=0.06)
        b.box((xc - 7.4, 8.0, -31.9), (xc + 7.4, 9.4, -31.6), 'lightw', bevel=0.0)
        x0, x1 = sorted((sx * 36.0, sx * 58.0))
        b.plan(0.0, 9.0, [(x0, 32.0), (x1, 32.0), (x1, 47.0), (x0, 47.0)], 'paint', bevel=0.3, top_inset=1.5)
        xc = sx * 47.0
        b.hull([(x, 8.5, z) for x in (xc - 7.0, xc + 7.0) for z in (34.0, 45.0)]
               + [(x, 19.0, z) for x in (xc - 5.5, xc + 5.5) for z in (35.5, 43.5)], 'paint', bevel=0.3)
        b.box((xc - 5.2, 18.9, 35.8), (xc + 5.2, 19.5, 43.2), 'team', bevel=0.06)
    k.piece('blink').box((-55.4, 27.9, -44.8), (-52.6, 30.8, -42.0), 'lightr', bevel=0.15)
    k.piece('blink').box((52.6, 27.9, -44.8), (55.4, 30.8, -42.0), 'lightr', bevel=0.15)

    # ------------------------------------------------------------------ wings
    w1 = k.piece('wing1'); o = w1.org
    wedge(w1, lambda x, y, z: (o.x + x, o.y + y, o.z + z))
    k.clone('wing3', 'wing1', mirror_x=True)
    w2 = k.piece('wing2'); o2 = w2.org                       # same block turned 90 deg: nose toward +z
    wedge(w2, lambda x, y, z: (o2.x - z, o2.y + y, o2.z + x))

    # ------------------------------------------------------------------ drawers + guns (drawer1 origin -27.7, 0.66, -17.7)
    d = k.piece('drawer1'); D = d.at
    oc = [(8.6 * math.cos(math.pi / 8 + i * math.pi / 4), 8.6 * math.sin(math.pi / 8 + i * math.pi / 4)) for i in range(8)]
    d.hull([D(x, y, z) for x, z in oc for y in (0.0, 20.6)], 'paint2', bevel=0.3)
    d.hull([D(x * 0.8, y, z * 0.8) for x, z in oc for y in (20.5, 21.1)], 'hazard', bevel=0.06)
    d.box(D(-8.9, 6.0, -1.5), D(-8.5, 16.0, 1.5), 'lightw', bevel=0.0)
    k.clone('drawer2', 'drawer1', mirror_x=True)
    g = k.piece('gun1'); G = g.at                                      # beam1 at (5.95, -3.83, 8.7)
    g.box(G(-3.6, -2.8, -3.0), G(3.4, 4.6, 3.6), 'steel', bevel=0.35)
    g.cyl(G(1.2, -1.2, 2.0), G(5.4, -3.5, 8.0), 1.5, 10, 'dark', r2=1.1)
    g.cyl(G(5.2, -3.4, 7.7), G(5.95, -3.83, 8.7), 1.15, 10, 'lightc')
    g.box(G(-3.2, 4.5, -2.6), G(3.0, 4.9, 3.2), 'hazard', bevel=0.04)
    k.clone('gun2', 'gun1', mirror_x=True)

    # ------------------------------------------------------------------ pad (origin 0, 0.34, 2.62), slides +23 forward
    p = k.piece('pad'); Pp = p.at
    p.cyl(Pp(0, 0.0, 0), Pp(0, 0.5, 0), 18.4, 36, 'dark', bevel=0.1)
    p.cyl(Pp(0, 0.5, 0), Pp(0, 0.62, 0), 16.6, 36, 'steel')
    for a in range(3):
        t = math.radians(a * 120 + 90)
        p.hull([Pp(r * math.cos(t + dt), yy, r * math.sin(t + dt)) for r in (16.7, 18.2) for dt in (-0.25, 0.25)
                for yy in (0.45, 0.6)], 'hazard', bevel=0.0)
