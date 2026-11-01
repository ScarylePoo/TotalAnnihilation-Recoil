"""FARK (ARM_T2_BOT_FARK) - Arm T2 Fast Assist-Repair Kbot. A squat engineer: a wide low body with hazard-striped
tool pods, a small visored head, a fan of four armour plates spread behind it like a shell, and two arms ending in
nano lathes. To build it leans forward, raises and spreads the arms and turns the torso to the job. Short standard
biped legs (TA's FARK is the squattest walker); script ported to scripts/ARM_T2_BOT_FARK.lua.
Coordinates are ENGINE/global: X right, Y up, Z forward.
Top view (what makes it a FARK): a light half-disc fan with a team band across it, the yellow-striped pods either
side and two cyan nano tips in front - a small round shell, unlike any other Arm kbot."""
import math

UNIT = dict(
    skeleton='biped',
    skeleton_opts=dict(hipx=3.4),
    res=1024,
    wreck=dict(seed=17, drop=['Larm'], remove=[]),
    preview_pose={},
)


def fan(b, a_deg, team=False):
    """one radial shell plate around the piece origin, pointing back (a=0), up (a=90) or down-back (a<0)."""
    from mathutils import Vector
    a = math.radians(a_deg)
    d = Vector((0, math.sin(a), -math.cos(a)))
    n = Vector((0, math.cos(a), math.sin(a)))
    o = Vector(b.at(0, 0, 0))
    pts = [o + d * r + n * t + Vector((x, 0, 0)) for r, w in ((1.8, 4.6), (9.8, 8.0)) for x in (-w, w) for t in (-0.45, 0.45)]
    b.hull(pts, 'paint', bevel=0.12)
    if team:
        b.hull([o + d * r + n * t + Vector((x, 0, 0)) for r in (3.4, 9.0) for x in (-2.8, 2.8) for t in (0.47, 0.6)],
               'team', bevel=0.03)


def build(k):
    k.standard_legs(width=2.1)

    # ------------------------------------------------------------------ pelvis (0, 7, 0)
    p = k.piece('pelvis'); Q = p.at
    p.hull([Q(x * sx, y, z) for sx in (-1, 1) for x, y, z in
            [(3.0, -1.2, -2.2), (3.0, -1.2, 2.2), (3.4, 1.0, -2.6), (3.4, 1.0, 2.6)]], 'dark', bevel=0.14)

    # ------------------------------------------------------------------ torso (0, 7.5, 0): wide low body
    t = k.piece('torso'); A = t.at
    t.hull([A(x * sx, y, z) for sx in (-1, 1) for x, y, z in
            [(4.4, 0.4, -3.4), (4.4, 0.4, 3.6), (6.0, 4.0, -3.8), (6.0, 4.0, 4.2), (5.0, 8.0, -3.4), (4.6, 8.0, 3.0),
             (2.6, 2.0, 5.0)]], 'paint2', bevel=0.2)
    for sx in (-1, 1):                                                                  # tool pods
        t.hull([A(sx * x, y, z) for x, y, z in
                [(5.6, 2.6, -2.8), (5.6, 2.6, 2.8), (10.0, 3.2, -2.4), (10.0, 3.2, 2.4), (5.6, 7.0, -2.8), (5.6, 7.0, 2.8),
                 (9.6, 6.6, -2.2), (9.6, 6.6, 2.2)]], 'hazard', bevel=0.16)
        t.cyl(A(sx * 10.0, 4.9, 0), A(sx * 10.5, 4.9, 0), 1.3, 10, 'dark')
    t.box(A(-3.0, 1.6, 4.0), A(3.0, 4.6, 4.6), 'dark', bevel=0.06)                      # chest grille
    for y in (2.2, 3.4):
        t.box(A(-2.6, y, 4.55), A(2.6, y + 0.5, 4.75), 'black', bevel=0.0)

    # ------------------------------------------------------------------ head (0, 15, 0)
    h = k.piece('head'); H = h.at
    h.hull([H(x * sx, y, z) for sx in (-1, 1) for x, y, z in
            [(2.2, 0.0, -1.6), (2.2, 0.0, 3.6), (2.0, 3.6, -1.2), (1.8, 3.8, 3.0), (1.4, 1.6, 5.4)]], 'paint', bevel=0.16)
    h.hull([H(x * sx, y, z) for sx in (-1, 1) for x, y, z in
            [(1.6, 1.4, 4.5), (1.6, 2.6, 4.1), (1.2, 1.4, 5.25), (1.2, 2.6, 4.9)]], 'dark', bevel=0.04)
    h.box(H(-1.0, 1.8, 5.0), H(1.0, 2.25, 5.2), 'lightc', bevel=0.0)

    # ------------------------------------------------------------------ the fan shell (4 plates, origin 0, 15, 0)
    fan(k.piece('shield1'), 90)
    fan(k.piece('shield2'), 42, team=True)
    fan(k.piece('shield3'), 0, team=True)
    fan(k.piece('shield4'), -42)

    # ------------------------------------------------------------------ arms: left built, right = mirrored clones
    s = k.piece('Lshoulder'); S = s.at                 # (4.5, 15.5, 2)
    s.hull([S(x, y, z) for x in (-1.6, 1.8) for y, z in [(0.0, -2.0), (0.0, 2.4), (3.4, 4.4), (4.4, 2.6), (2.6, -1.6)]],
           'paint', bevel=0.14)
    a = k.piece('Larm'); R = a.at                      # (4.25, 17.75, 5.75)
    a.cyl(R(-1.6, 0, 0), R(1.6, 0, 0), 1.4, 10, 'dark', bevel=0.05)
    a.hull([R(x, y, z) for x in (-1.3, 1.3) for y in (-0.6, -5.6) for z in (-1.3, 1.4)], 'paint2', bevel=0.12)
    l = k.piece('Llathe'); L = l.at                    # (4.25, 12.25, 5.75): emitter toward -y
    l.cyl(L(0, 0.2, 0), L(0, -5.4, 0), 1.25, 10, 'dark', bevel=0.05)
    for y in (-1.4, -3.0, -4.6):
        l.cyl(L(0, y, 0), L(0, y - 0.6, 0), 1.55, 10, 'steel')
    l.cyl(L(0, -5.3, 0), L(0, -7.2, 0), 0.9, 10, 'steel', r2=0.6)
    l.cyl(L(0, -7.1, 0), L(0, -7.5, 0), 0.65, 10, 'lightc')
    k.clone('Rshoulder', 'Lshoulder', mirror_x=True)
    k.clone('Rarm', 'Larm', mirror_x=True)
    k.clone('Rlathe', 'Llathe', mirror_x=True)
