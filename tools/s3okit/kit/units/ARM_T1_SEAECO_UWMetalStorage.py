"""Underwater Metal Storage (ARM_T1_SEAECO_UWMetalStorage) - Arm seabed metal storage (no waterline: sits on the sea
bed under at least 31 elmo of water). The land storage's long light vault laid down as two long light ingot cylinders
side by side on a dark cradle, strapped by two team bands; on top (topdoodads) a dark catwalk between them and two pairs
of dark hexagonal loading hatches with light caps.
Identity from above (through the water): a long light double bar (twin cylinders) crossed by two team straps, dark
seam between (the Arm UW energy storage is a wide octagonal dome with a cyan core).
Pieces (Lua script): gp (empty root), base (cradle), canisters (the cylinders), topdoodads (hatches, catwalk) - all at
the origin, explode only.
res 1024: seen only through 30+ elmo of water.
Coordinates are ENGINE/global: X right, Y up, Z forward."""
import math

UNIT = dict(
    res=1024,
    preview_water=31.0,
    wreck=dict(seed=101),
)

CX, CY, CR, CL = 11.5, 13.0, 9.6, 31.0      # cylinder axis x (+-), height, radius, half length


def hexagon(r, rot=0.0):
    return [(r * math.cos(rot + i * math.pi / 3), r * math.sin(rot + i * math.pi / 3)) for i in range(6)]


def build(k):
    b = k.piece('Base')
    b.plan(0.0, 3.4, [(-26.0, -33.0), (26.0, -33.0), (28.0, -30.0), (28.0, 30.0), (26.0, 33.0), (-26.0, 33.0),
                      (-28.0, 30.0), (-28.0, -30.0)], 'paint2', bevel=0.35, top_inset=1.2)
    for z in (-24.0, 0.0, 24.0):                                  # saddles
        b.hull([(x, y, zz) for x in (2.0, 24.0) for y in (3.0, 7.0) for zz in (z - 2.6, z + 2.6)]
               + [(x, 9.0, zz) for x in (4.0, 22.0) for zz in (z - 2.2, z + 2.2)], 'dark', bevel=0.2, mirror=True)
    for sz in (-1, 1):
        b.box((-2.0, 1.6, 33.0 * sz - 0.3), (2.0, 2.6, 33.0 * sz + 0.3), 'lightc', bevel=0.0)

    # ---------------------------------------------------------------- canisters: twin ingot cylinders along z
    c = k.piece('Canisters')
    c.cyl((CX, CY, -CL), (CX, CY, CL), CR, 12, 'paint', rot=math.pi / 12, bevel=0.35, mirror=True)
    for sz in (-1, 1):
        c.cyl((CX, CY, CL * sz), (CX, CY, (CL + 4.0) * sz), CR - 0.4, 12, 'paint2', r2=4.0, rot=math.pi / 12,
              bevel=0.2, mirror=True)
        c.cyl((CX, CY, (CL + 3.8) * sz), (CX, CY, (CL + 4.6) * sz), 3.0, 8, 'dark', mirror=True)
        # team straps (top-facing bands)
        c.cyl((CX, CY, 9.0 * sz - 4.7), (CX, CY, 9.0 * sz + 4.7), CR + 0.15, 12, 'team', rot=math.pi / 12,
              mirror=True)
    for z in (-21.0, 21.0):
        c.cyl((CX, CY, z - 0.8), (CX, CY, z + 0.8), CR + 0.2, 12, 'dark', rot=math.pi / 12, mirror=True)

    # ---------------------------------------------------------------- topdoodads: catwalk + hatches
    t = k.piece('TopDooDads')
    t.box((-2.4, 3.0, -30.0), (2.4, 21.0, 30.0), 'paint2', bevel=0.3)
    t.box((-1.6, 20.9, -28.0), (1.6, 21.3, 28.0), 'dark', bevel=0.0)
    for z in (-2.0, 3.0):
        t.box((-1.4, 21.2, z), (1.4, 21.4, z + 1.2), 'lightc', bevel=0.0)
    for z in (-19.0, 19.0):
        t.plan(21.5, 23.6, [(CX + x, z + y) for x, y in hexagon(4.2)], 'dark', bevel=0.2, top_inset=0.5, mirror=True)
        t.plan(23.5, 24.0, [(CX + x, z + y) for x, y in hexagon(2.6)], 'steel', bevel=0.0, mirror=True)
