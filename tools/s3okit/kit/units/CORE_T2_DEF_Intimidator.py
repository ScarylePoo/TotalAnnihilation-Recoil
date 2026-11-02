"""Intimidator (CORE_T2_DEF_Intimidator) - Core long-range plasma cannon. A broad hexagonal plinth carrying a huge split
dome turret; the gun slab rides in the slot between the two dome halves and a fat light steel barrel with a heavy
muzzle brake projects far forward. Gun and barrel recoil (move z).
Identity from above: two big dark half-domes with team crests either side of a light steel gun line that runs from
the dome's slot well past the plinth - one massive gun, where the Arm Big Bertha is a tall pylon with a long thin one.
Pieces (COB): base, turret (turn y), gun (turn x, move z), barrel (move z), flare (emit, empty).
The barrel ends at the original flare (projectiles spawn there), so its length is TA's; it reads big by thickness
and the long steel sleeve on the gun slab.
Coordinates are ENGINE/global: X right, Y up, Z forward."""
import math

UNIT = dict(
    res=1024,
    wreck=dict(seed=45, drop=['barrel'], pose={'turret': (0, 30, 0), 'gun': (10, 0, 0)}),
    preview_pose={'turret': (0, -25, 0), 'gun': (-8, 0, 0)},
)


def hexa(rx, rz):
    return [(rx, 0.0), (rx * 0.5, rz), (-rx * 0.5, rz), (-rx, 0.0), (-rx * 0.5, -rz), (rx * 0.5, -rz)]


def build(k):
    # ------------------------------------------------------------------ base: hexagonal plinth
    b = k.piece('base')
    b.plan(0.0, 3.0, hexa(26.0, 23.4), 'paint2', bevel=0.3, top_inset=1.0)
    b.plan(2.8, 21.2, hexa(22.6, 20.4), 'paint', bevel=0.35, top_inset=3.4)
    b.cyl((0, 20.6, 0), (0, 21.6, 0), 15.6, 16, 'dark', bevel=0.1)
    # team pads on the plinth ledge at the four diagonal corners
    for sx in (-1, 1):
        for sz in (-1, 1):
            cx, cz = sx * 12.4, sz * 19.6
            b.hull([(cx + x, y, cz + z) for x, z in ((-3.6, -1.2), (3.6, -1.2), (3.0, 1.6), (-3.0, 1.6)) for y in (2.8, 3.4)],
                   'team', bevel=0.05)
    b.box((-4.0, 3.0, 19.6), (4.0, 12.0, 20.6), 'dark', bevel=0.1)
    b.box((-1.0, 13.0, 18.9), (1.0, 14.4, 19.6), 'lightr', bevel=0.0)

    # ------------------------------------------------------------------ turret: split dome (origin 0, 21.17, 0)
    t = k.piece('turret'); T = t.at
    t.cyl(T(0, 0.0, 0), T(0, 1.6, 0), 15.0, 16, 'dark', bevel=0.1)
    arc = [(15.6 * math.cos(math.radians(a)), 14.0 + 14.6 * math.sin(math.radians(a))) for a in range(0, 181, 20)]
    for sx in (-1, 1):
        pts = [T(sx * x, 1.4, z) for x in (3.6, 15.2) for z in (-16.2, 16.2)]
        pts += [T(sx * 3.6, y, z) for z, y in arc] + [T(sx * 13.6, y - 1.6, z * 0.9) for z, y in arc]
        t.hull(pts, 'paint', bevel=0.35)
        # team crest along the dome top
        cap = [(15.6 * 1.012 * math.cos(math.radians(a)), 14.0 + 14.6 * 1.012 * math.sin(math.radians(a))) for a in range(40, 141, 20)]
        t.hull([T(sx * x, y, z) for z, y in cap for x in (5.2, 11.6)], 'team', bevel=0.0)
        # dark ribs on the dome's outer flank
        t.hull([T(sx * x, y, z) for x in (14.4, 15.4) for y, z in ((3.0, -4.0), (3.0, 4.0), (16.0, -3.2), (16.0, 3.2))], 'dark', bevel=0.1)
    t.box(T(-3.6, 1.6, -15.0), T(3.6, 6.0, 15.0), 'dark', bevel=0.1)              # slot floor

    # ------------------------------------------------------------------ gun: slab in the slot (origin 0, 35.13, 0)
    g = k.piece('gun'); G = g.at
    g.cyl(G(-4.6, 0, 0), G(4.6, 0, 0), 4.2, 12, 'dark', bevel=0.06)
    g.hull([G(x * sx, y, z) for sx in (-1, 1) for x, y, z in
            [(3.3, -11.6, -13.6), (3.3, 13.6, -6.0), (3.3, 13.6, 6.0), (3.3, -6.0, 14.0), (3.3, 8.0, 14.0)]], 'paint2', bevel=0.3)
    # long steel sleeve from the slab front to the barrel
    g.cyl(G(0, 0, 10.0), G(0, 0, 29.6), 4.6, 12, 'steel', rot=math.pi / 12, bevel=0.08)
    g.cyl(G(0, 0, 21.0), G(0, 0, 23.0), 5.0, 12, 'dark', rot=math.pi / 12, bevel=0.06)

    # ------------------------------------------------------------------ barrel (origin 0, 35.13, 29.35)
    br = k.piece('barrel'); B = br.at
    br.cyl(B(0, 0, -0.4), B(0, 0, 11.6), 3.6, 12, 'steel', rot=math.pi / 12)
    br.cyl(B(0, 0, 11.0), B(0, 0, 16.3), 4.8, 8, 'steel', r2=4.4, rot=math.pi / 8, bevel=0.1)   # muzzle brake
    br.cyl(B(0, 0, 12.6), B(0, 0, 14.0), 4.95, 8, 'dark', rot=math.pi / 8)
    br.cyl(B(0, 0, 16.28), B(0, 0, 16.4), 2.4, 12, 'black')
