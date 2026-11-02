"""Protector (ARM_T2_DEF_Protector) - Arm anti-nuke silo. A tapered plinth carrying a tall four-sided silo; each wall
is a door hinged at its foot with a triangular roof leaf, so the closed silo is a light box with a pyramid roof. To
fire, the four doors fold outward ~130 deg like petals and lie down around the plinth, exposing a launcher drum with
three interceptor missiles standing upright (it turns 120 deg per shot).
Identity from above: closed = light box with a team diamond roof (four team triangles) on a dark plinth; open = a
four-petal cross of yellow-black silo-door faces (the only meaningful hazard: missile silo doors) with team roof
leaves at the tips, round a dark drum with three white missile noses.
Pieces (Lua script, ported from the COB): base, turret (turn y), rocket1..3 (hide/show, query), door1/2 (turn z),
door3/4 (turn x). The preview shows the OPEN state (doors at +-130 deg).
Coordinates are ENGINE/global: X right, Y up, Z forward."""
import math

UNIT = dict(
    res=2048,
    wreck=dict(seed=31, drop=['door2'], pose={'door1': (0, 0, 40), 'door3': (-25, 0, 0)}),
    preview_pose={'door1': (0, 0, 130), 'door2': (0, 0, -130), 'door3': (-130, 0, 0), 'door4': (130, 0, 0),
                  'turret': (0, 15, 0)},
)

HY = 17.62          # hinge height
WALL = 25.6         # wall height above the hinge
TH = 1.5            # wall thickness


def door(k, name, axis, sgn, half_w, inward):
    """one door, built in its own frame: the wall rises from the hinge (local y 0..WALL), its outer face toward
    -inward, roof leaf from the wall top to the silo axis. axis 'x': wall normal along x; 'z': along z.
    half_w: (lo, hi) extent along the hinge; inward: distance from the hinge to the silo axis."""
    d = k.piece(name); D = d.at

    def P(n, y, t):           # n = along the wall normal (+ = inward), t = along the hinge
        return D(n * sgn, y, t) if axis == 'x' else D(t, y, n * sgn)
    lo, hi = half_w
    # wall: outer paint skin, inner hazard face (silo door), dark edges
    d.hull([P(n, y, t) for n in (-TH, -0.35) for y in (0.4, WALL) for t in (lo, hi)], 'paint', bevel=0.2)
    d.hull([P(n, y, t) for n in (-0.4, 0.0) for y in (1.6, WALL - 1.6) for t in (lo + 1.6, hi - 1.6)], 'hazard', bevel=0.05)
    d.hull([P(n, y, t) for n in (-0.4, -0.1) for y in (0.4, WALL) for t in (lo, hi)], 'dark', bevel=0.05)
    # hinge barrel along the foot
    d.cyl(P(-0.75, 0.2, lo + 1.0), P(-0.75, 0.2, hi - 1.0), 1.2, 8, 'dark', bevel=0.05)
    # side pod on the outer face (TA's ear hatch), paint2
    m = 0.5 * (lo + hi)
    d.hull([P(n, y, m + t) for n, ts in ((-TH, (-5.2, 5.2)), (-TH - 2.6, (-3.6, 3.6))) for y in (9.0, 19.0) for t in ts],
           'paint2', bevel=0.2)
    # roof leaf: a low triangle from the wall top to the axis (outer team skin, paint2 underside)
    apex_t = 0.0
    yt, ya = WALL, WALL + 4.6
    tri_top = [P(-TH, yt + 0.05, lo), P(-TH, yt + 0.05, hi), P(inward - 0.3, ya + 0.05, apex_t)]
    tri_bot = [P(-TH, yt - 1.0, lo + 0.6), P(-TH, yt - 1.0, hi - 0.6), P(inward - 0.6, ya - 1.0, apex_t)]
    d.hull(tri_top + tri_bot, 'paint2', bevel=0.12)
    # outer skin: team diamond (the closed roof); inner skin: team (faces up when the door lies open)
    tri_team = [P(-TH + 1.6, yt + 0.12, lo + 3.4), P(-TH + 1.6, yt + 0.12, hi - 3.4), P(inward - 2.8, ya - 0.3, apex_t)]
    d.hull(tri_team + [(v[0], v[1] + 0.22, v[2]) for v in tri_team], 'team', bevel=0.0)
    tri_in = [P(-TH + 0.4, yt - 1.08, lo + 1.4), P(-TH + 0.4, yt - 1.08, hi - 1.4), P(inward - 1.4, ya - 1.08, apex_t)]
    d.hull(tri_in + [(v[0], v[1] - 0.22, v[2]) for v in tri_in], 'team', bevel=0.0)
    return d


def build(k):
    # ------------------------------------------------------------------ base: wide plinth + tapered silo socket
    b = k.piece('base')
    b.plan(0.0, 2.6, [(-23.0, -19.0), (-19.0, -23.0), (19.0, -23.0), (23.0, -19.0), (23.0, 19.0), (19.0, 23.0),
                      (-19.0, 23.0), (-23.0, 19.0)], 'paint2', bevel=0.25, top_inset=1.0)
    b.plan(2.4, HY, [(-16.0, -16.0), (16.0, -16.0), (16.0, 16.0), (-16.0, 16.0)], 'paint', bevel=0.3, top_inset=3.6)
    b.box((-12.4, HY - 0.6, -12.4), (12.4, HY + 0.2, 12.4), 'dark', bevel=0.1)          # silo floor
    # team corner blocks on the plinth (wide: they show in both states)
    for s_ in (-1, 1):
        for t in (-1, 1):
            b.hull([(x * s_, y, z * t) for y in (2.5, 4.2) for x, z in
                    ((12.0, 21.6), (21.6, 12.0), (19.0, 21.6), (21.6, 19.0), (12.0, 18.2), (18.2, 12.0))], 'team', bevel=0.08)
    b.box((-1.2, 7.0, 15.0), (1.2, 8.6, 15.4), 'lightc', bevel=0.0)

    # ------------------------------------------------------------------ doors (hinges on the silo rim)
    door(k, 'door1', 'x', 1, (-11.2, 10.8), 10.5)     # origin (-10.5, 17.63, -0.75): wall at -x, inward +x
    door(k, 'door2', 'x', -1, (-12.0, 10.0), 10.75)   # origin (10.75, 17.62, 0): wall at +x, inward -x
    door(k, 'door3', 'z', 1, (-10.5, 10.8), 12.0)     # origin (0, 17.62, -12): wall at -z, inward +z
    door(k, 'door4', 'z', -1, (-10.5, 10.8), 10.0)    # origin (0, 17.62, 10): wall at +z, inward -z

    # ------------------------------------------------------------------ turret: launcher drum (origin 0, 17.62, 1)
    t = k.piece('turret'); T = t.at
    t.cyl(T(0, 0.2, 0), T(0, 3.0, 0), 9.8, 12, 'dark', bevel=0.1)
    t.cyl(T(0, 3.0, 0), T(0, 20.0, 0), 4.6, 12, 'paint2', bevel=0.15)
    t.cyl(T(0, 20.0, 0), T(0, 22.4, 0), 3.2, 12, 'dark', bevel=0.08)
    # three cradle rails out to the missiles
    for rx, rz in ((-8.06, 3.93), (0.38, -7.39), (8.06, 3.93)):
        L = math.hypot(rx, rz); ux, uz = rx / L, rz / L; px, pz = -uz, ux
        t.hull([T(ux * f * L + px * w, y, uz * f * L + pz * w) for f in (0.4, 0.78) for y in (4.0, 18.0) for w in (-1.0, 1.0)],
               'dark', bevel=0.05)
    t.cyl(T(0, 22.35, 0), T(0, 22.6, 0), 2.6, 10, 'team')
    t.box(T(-0.6, 21.0, 2.0), T(0.6, 22.0, 2.4), 'lightr', bevel=0.0)

    # ------------------------------------------------------------------ missiles (rocket1 origin -8.06, 28.76, 4.93)
    r = k.piece('rocket1'); R = r.at
    r.cyl(R(0, -10.4, 0), R(0, 7.0, 0), 1.7, 10, 'paint')
    r.cyl(R(0, 7.0, 0), R(0, 10.8, 0), 1.7, 10, 'steel', r2=0.4)          # nose cone
    r.cyl(R(0, 5.6, 0), R(0, 7.0, 0), 1.78, 10, 'hazard')
    for ang in (45, 135, 225, 315):
        a = math.radians(ang)
        r.hull([R(math.cos(a) * rr, y, math.sin(a) * rr) for rr in (1.2, 3.2) for y in (-10.4, -6.0)] +
               [R(math.cos(a) * 1.2, -3.0, math.sin(a) * 1.2)], 'dark', bevel=0.0)
    k.clone('rocket2', 'rocket1')
    k.clone('rocket3', 'rocket1')
