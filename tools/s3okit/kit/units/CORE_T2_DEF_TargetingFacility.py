"""Targeting Facility (CORE_T2_DEF_TargetingFacility) - Core automatic radar targeting. A squat square hub crowned by a
stepped pyramid with a red beacon; four heavy hexagonal sensor blocks sit against its sides on ground rails. Switched
on, the four blocks roll outward 13.5 elmo along their rails and red sensor lamps rise out of their roofs.
Identity from above: a dark '+' of four hexagonal blocks with team roofs round a light steel pyramid with a red tip,
dark rails reaching to the footprint edge - blocks where the Arm facility has pylons.
Pieces (COB): base, centerlight, arm1..4 (move z/x along the rails), light1..4 (move y). The preview shows the OPEN
state (blocks out, lamps up).
Coordinates are ENGINE/global: X right, Y up, Z forward."""
import math

UNIT = dict(
    res=2048, bake_res=2048,          # no 2x supersampling: machine time (see the batch report)
    wreck=dict(seed=57, drop=['arm3']),
    preview_pose={'arm1': {'move': (0, 0, -13.375)}, 'arm2': {'move': (0, 0, 13.25)}, 'arm3': {'move': (13.75, 0, 0)},
                  'arm4': {'move': (-13.625, 0, 0)}, 'light1': {'move': (0, 2.875, 0)}, 'light2': {'move': (0, 3.0, 0)},
                  'light3': {'move': (0, 3.0, 0)}, 'light4': {'move': (0, 3.0, 0)}},
)


def arm(k, name, light, u, sgn):
    """hexagonal sensor block: outer face at the piece origin, extending inward (sgn = toward the hub) along u; closed,
    its inner half hides in the hub. The lamp rises out of a hatch in the roof."""
    a = k.piece(name); A = a.at

    def Q(s, y, w):        # s = inward distance from the outer face, w = across
        return A(sgn * s, y, w) if u == 'x' else A(w, y, sgn * s)
    prof = [(0.0, -5.0), (0.0, 5.0), (7.0, 8.8), (21.0, 8.8), (21.0, -8.8), (7.0, -8.8)]
    a.hull([Q(s, y, w) for s, w in prof for y in (-3.6, 4.4)], 'paint', bevel=0.35)
    # team roof plate (around the lamp hatch) and a dark hatch rim
    a.hull([Q(s, y, w) for s, w in ((2.0, -3.6), (2.0, 3.6), (6.0, 5.4), (11.4, 5.4), (11.4, -5.4), (6.0, -5.4))
            for y in (4.35, 4.6)], 'team', bevel=0.0)
    a.hull([Q(s, y, w) for s, w in ((13.6, -3.2), (13.6, 3.2), (19.9, 3.2), (19.9, -3.2)) for y in (4.5, 4.62)], 'black', bevel=0.0)
    # rail wheels
    for s in (4.0, 17.0):
        a.cyl(Q(s, -2.6, -6.6), Q(s, -2.6, 6.6), 1.3, 8, 'dark', bevel=0.03)
    l = k.piece(light); L = l.at

    def R(s, y, w):
        return L(sgn * s, y, w) if u == 'x' else L(w, y, sgn * s)
    l.hull([R(s, y, w) for s in (-2.4, 2.4) for y in (-0.6, 4.6) for w in (-2.4, 2.4)], 'dark', bevel=0.1)
    l.hull([R(s, y, w) for s in (-1.6, 1.6) for y in (4.5, 5.5) for w in (-1.6, 1.6)], 'lightr', bevel=0.0)


def build(k):
    # ------------------------------------------------------------------ base: hub + rails
    b = k.piece('base')
    b.plan(0.0, 3.0, [(-10.0, -10.0), (10.0, -10.0), (10.0, 10.0), (-10.0, 10.0)], 'paint2', bevel=0.25, top_inset=0.4)
    b.plan(2.8, 11.3, [(-9.6, -9.6), (9.6, -9.6), (9.6, 9.6), (-9.6, 9.6)], 'paint', bevel=0.3, top_inset=1.6)
    for u in ('x', 'z'):           # twin rails along both axes out to the footprint edge
        for w in (-4.2, 4.2):
            for sg in (-1, 1):
                if u == 'x':
                    b.box((min(sg * 9.0, sg * 31.6), 0.0, w - 0.7), (max(sg * 9.0, sg * 31.6), 0.7, w + 0.7), 'dark', bevel=0.05)
                else:
                    b.box((w - 0.7, 0.0, min(sg * 9.0, sg * 31.6)), (w + 0.7, 0.7, max(sg * 9.0, sg * 31.6)), 'dark', bevel=0.05)
    # rail end stops (team)
    for x, z in ((31.0, 0.0), (-31.0, 0.0), (0.0, 31.0), (0.0, -31.0)):
        b.box((x - (1.0 if x else 6.0), 0.0, z - (1.0 if z else 6.0)), (x + (1.0 if x else 6.0), 1.6, z + (1.0 if z else 6.0)),
              'team', bevel=0.08)

    # ------------------------------------------------------------------ centerlight: stepped pyramid with a red tip
    c = k.piece('centerlight')
    c.plan(11.2, 15.6, [(-6.4, -6.4), (6.4, -6.4), (6.4, 6.4), (-6.4, 6.4)], 'steel', bevel=0.2, top_inset=2.0)
    c.plan(15.4, 19.0, [(-3.4, -3.4), (3.4, -3.4), (3.4, 3.4), (-3.4, 3.4)], 'dark', bevel=0.15, top_inset=0.8)
    c.hull([(x, 19.0, z) for x in (-1.6, 1.6) for z in (-1.6, 1.6)] + [(0.0, 21.6, 0.0)], 'lightr', bevel=0.0)

    # ------------------------------------------------------------------ arms: the sensor blocks (origins 18.5 out, y 3.75)
    arm(k, 'arm1', 'light1', 'z', 1)      # origin (0, 3.75, -18.5), inward +z
    arm(k, 'arm2', 'light2', 'z', -1)     # origin (0, 3.75, 18.5)
    arm(k, 'arm3', 'light3', 'x', -1)     # origin (18.5, 3.75, 0)
    arm(k, 'arm4', 'light4', 'x', 1)      # origin (-18.5, 3.75, 0)
