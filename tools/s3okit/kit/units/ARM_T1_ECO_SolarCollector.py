"""Solar Collector (ARM_T1_ECO_SolarCollector) - Arm solar. A square plinth with a glowing collector core, enclosed
when closed by four armoured petals standing almost upright (a light truncated pyramid); switched on, the petals
fold out 97 deg on their hinges and lie nearly flat, showing their dark-blue solar-cell inner faces.
Identity from above (open): a big plus/star of four dark cell petals with team spines and team tips round a light
square hub - by far the widest flat Arm eco plan. Closed: a light square box with a team-cross roof gap.
Pieces (Lua script, third-party S3O layout kept): arm_solar.3ds (empty root), base, dish1..4 (turn x / z by -+1.7
rad = 97.4 deg to open; dish1 at -z, dish2 +z, dish3 -x, dish4 +x).
Preview: OPEN (the script opens on Activate; the model rest pose is closed).
Coordinates are ENGINE/global: X right, Y up, Z forward."""
import math

OPEN = math.degrees(1.7)
UNIT = dict(
    wreck=dict(seed=13, pose={'dish1': (-40, 0, 0), 'dish4': (0, 0, -60)}, drop=['dish2']),
    preview_pose={'dish1': (-OPEN, 0, 0), 'dish2': (OPEN, 0, 0), 'dish3': (0, 0, OPEN), 'dish4': (0, 0, -OPEN)},
)

TH_C = math.radians(10.0 + OPEN)     # closed petal elevation, measured from the OUTWARD horizontal (open = 10 deg)
L = 24.0                             # petal length from the hinge
W0, W1 = 15.2, 8.4                   # petal half-width at hinge / tip


def petal(k, name, o, lat, half=True):
    """o = outward unit (x, z); lat = lateral unit (x, z). Solar cells on the INNER face (it faces the sky when open)."""
    p = k.piece(name); O = k.P[name]
    d = (o[0] * math.cos(TH_C), math.sin(TH_C), o[1] * math.cos(TH_C))           # along the petal, hinge -> tip
    n = (-o[0] * math.sin(TH_C), math.cos(TH_C), -o[1] * math.sin(TH_C))          # inner face normal

    def P(s, t, h):
        return (O[0] + d[0] * s + lat[0] * t + n[0] * h, O[1] + d[1] * s + n[1] * h, O[2] + d[2] * s + lat[1] * t + n[2] * h)

    def w(s):
        return W0 - (W0 - W1) * s / L

    def quad(s0, s1, t0f, t1f, h0, h1, mat, bevel, inset=0.0):
        pts = []
        for s in (s0, s1):
            for tf in (t0f, t1f):
                t = tf(s) if callable(tf) else tf
                for h in (h0, h1):
                    pts.append(P(s, t, h))
        p.hull(pts, mat, bevel=bevel, mirror=half)

    t_lo = 0.0 if half else (lambda s: -w(s))
    # armoured back shell (light paint, the closed outside)
    quad(0.0, L, t_lo, w, -1.1, 0.0, 'paint', 0.2)
    # dark hinge knuckle along the bottom edge
    quad(-0.6, 2.4, t_lo, lambda s: w(s) - 0.6, -1.6, 0.5, 'paint2', 0.15)
    # solar cells (glass) in a frame, split by a team spine; team tip band
    quad(3.0, L - 3.2, 2.7 if half else (lambda s: -w(s) + 1.4), lambda s: w(s) - 1.4, 0.0, 0.22, 'glass', 0.0)
    quad(2.6, L - 3.0, 0.0, 2.7, 0.0, 0.42, 'team', 0.0)
    quad(L - 3.0, L - 0.4, 0.0, lambda s: w(s) - 0.5, 0.0, 0.42, 'team', 0.05)
    # cell grid: dark cross bars
    for s0 in (8.4, 14.0):
        quad(s0, s0 + 0.7, 2.7, lambda s: w(s) - 1.4, 0.2, 0.36, 'dark', 0.0)
    return p


def build(k):
    # ------------------------------------------------------------------ base: plinth + collector core
    b = k.piece('base')
    b.plan(-0.9, 0.6, [(-17.2, -17.2), (17.2, -17.2), (17.2, 17.2), (-17.2, 17.2)], 'paint2', bevel=0.2, top_inset=0.5)
    # hinge rails just inside the four hinge lines
    for z0, z1 in ((-15.6, -14.0), (14.0, 15.6)):
        b.box((-14.0, 0.5, z0), (14.0, 2.4, z1), 'dark', bevel=0.12)
    b.box((-15.6, 0.5, -14.0), (-14.0, 2.4, 14.0), 'dark', bevel=0.12, mirror=True)
    # inner deck (light) and the collector core: stepped square column, glowing cap
    b.box((-14.0, 0.5, -14.0), (14.0, 2.2, 14.0), 'paint', bevel=0.2)
    b.plan(2.1, 9.0, [(-8.0, -8.0), (8.0, -8.0), (8.0, 8.0), (-8.0, 8.0)], 'paint', bevel=0.25, top_inset=1.6)
    b.box((-5.6, 8.8, -5.6), (5.6, 16.0, 5.6), 'paint2', bevel=0.2)
    b.cyl((0, 15.8, 0), (0, 17.4, 0), 4.6, 8, 'dark', rot=math.pi / 8, bevel=0.08)
    b.cyl((0, 17.3, 0), (0, 18.4, 0), 3.4, 8, 'lightc', rot=math.pi / 8)
    # team corner blocks on the inner deck (visible open and closed through the gap)
    for sx in (-1, 1):
        for sz in (-1, 1):
            b.box((min(9.6 * sx, 13.8 * sx), 2.1, min(9.6 * sz, 13.8 * sz)),
                  (max(9.6 * sx, 13.8 * sx), 3.0, max(9.6 * sz, 13.8 * sz)), 'team', bevel=0.08)
    b.box((-1.0, -0.2, 17.0), (1.0, 0.5, 17.3), 'lightc', bevel=0.0)

    # ------------------------------------------------------------------ petals
    petal(k, 'dish1', (0.0, -1.0), (1.0, 0.0), half=True)
    petal(k, 'dish2', (0.0, 1.0), (1.0, 0.0), half=True)
    build_side(k)


def build_side(k):
    """dish3 (-x hinge) built whole from two halves (it is not on x = 0), dish4 its mirror clone."""
    p = k.piece('dish3'); O = k.P['dish3']
    o = (-1.0, 0.0)
    d = (o[0] * math.cos(TH_C), math.sin(TH_C), o[1] * math.cos(TH_C))
    n = (-o[0] * math.sin(TH_C), math.cos(TH_C), -o[1] * math.sin(TH_C))

    def P(s, t, h):
        return (O[0] + d[0] * s + n[0] * h, O[1] + d[1] * s + n[1] * h, O[2] + t + d[2] * s + n[2] * h)

    def w(s):
        return W0 - (W0 - W1) * s / L

    def quad(s0, s1, t0f, t1f, h0, h1, mat, bevel):
        pts = []
        for s in (s0, s1):
            for tf in (t0f, t1f):
                t = tf(s) if callable(tf) else tf
                for h in (h0, h1):
                    pts.append(P(s, t, h))
        p.hull(pts, mat, bevel=bevel)

    for sg in (-1, 1):
        f = (lambda g: (lambda s: g * w(s)))(sg)
        fi = (lambda g: (lambda s: g * (w(s) - 1.4)))(sg)
        fk = (lambda g: (lambda s: g * (w(s) - 0.6)))(sg)
        fb = (lambda g: (lambda s: g * (w(s) - 0.5)))(sg)
        quad(0.0, L, 0.0, f, -1.1, 0.0, 'paint', 0.2)
        quad(-0.6, 2.4, 0.0, fk, -1.6, 0.5, 'paint2', 0.15)
        quad(3.0, L - 3.2, 2.7 * sg, fi, 0.0, 0.22, 'glass', 0.0)
        quad(2.6, L - 3.0, 0.0, 2.7 * sg, 0.0, 0.42, 'team', 0.0)
        quad(L - 3.0, L - 0.4, 0.0, fb, 0.0, 0.42, 'team', 0.05)
        for s0 in (8.4, 14.0):
            quad(s0, s0 + 0.7, 2.7 * sg, fi, 0.2, 0.36, 'dark', 0.0)
    k.clone('dish4', 'dish3', mirror_x=True)
