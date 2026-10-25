"""Standard walker skeletons (user requirement, 2026-10-24): every legged unit except the Spider gets the same
piece hierarchy and BACKWARDS (digitigrade) legs like Splinter Faction's Federation walkers, so one walk script
drives all bipeds and one drives all quadrupeds. The Can and the Sumo get tracks instead of legs.

  biped:  pelvis > legs > rthigh > rleg > rfoot          (r = -X side, as in SF)
                        > lthigh > lleg > lfoot
  quad:   pelvis > legs > {rf,lf,rb,lb}thigh > ..leg > ..foot     (names confirmed by the user)
Not converted: Spider, Roach, Scarab (keep their legs and scripts). The Can and Sumo get tracks instead.

Proportions are the SF Federation rig (fedbear/fedgoliath/fedstriker) scaled by pelvis height H, because SF's
shared walk (common.WalkScript, generated from one Blender rig) only looks right on those ratios:
  legs  = pelvis + (0, -0.013H, 0)
  thigh = legs   + (+-hipx, 0, 0)            hipx ~ 0.66H on Fed walkers; default here from the TA model
  leg   = thigh  + (0, -0.32H, -0.325H)      knee BEHIND the hip
  foot  = leg    + (0, -0.49H, +0.49H)       ankle in front of the knee, ~0.17H above ground
Non-leg pieces of the original model (torso, arms, guns, flares...) are kept at their global positions and
re-parented: to the matching new leg piece if they hung off an old leg, otherwise to pelvis.
"""
import re

LEGS = {'biped': ['r', 'l'], 'quad': ['rf', 'lf', 'rb', 'lb']}
RATIO = dict(legs_y=-0.013, knee_y=-0.32, knee_z=-0.325, ankle_y=-0.49, ankle_z=0.49)
LEGWORD = re.compile(r'(thigh|leg|shin|calf|knee|foot|feet|boot|ankle|toe|hip)', re.I)
NOT_LEG = re.compile(r'(flare|fire|emit|sfx|gun|barrel|nano|muzzle|cover)', re.I)


def is_leg_piece(name):
    return bool(LEGWORD.search(name)) and not NOT_LEG.search(name)


def _kind_of(name):
    n = name.lower()
    if re.search(r'(foot|feet|boot|toe|ankle)', n): return 'foot'
    if re.search(r'(thigh|upleg|uleg|hip)', n): return 'thigh'
    return 'leg'


def _side_hint(name):
    n = name.lower()
    return bool(re.match(r'^(r|right|l|left)', n) or re.search(r'(^|_)[rl](_|$)', n))


def _side_of(name, gpos):
    n = name.lower()
    if re.match(r'^(r|right)', n) or re.search(r'(^|_)r(_|$)', n): s = 'r'
    elif re.match(r'^(l|left)', n) or re.search(r'(^|_)l(_|$)', n): s = 'l'
    else: s = 'r' if gpos[0] < 0 else 'l'
    return s


def remap(T, kind='biped', height=None, hipx=None, hipz=None, drop=(), keep=()):
    """T: original piece table (threedo.load_any). Returns (newT, report)."""
    ids = LEGS[kind]
    old_legs = [n for n in T if (is_leg_piece(n) or n in drop) and n not in keep and n.lower() != 'pelvis']
    # pelvis height
    if height is None:
        if 'pelvis' in T and T['pelvis']['gpos'][1] > 1:
            height = T['pelvis']['gpos'][1]
        else:
            ys = [T[n]['gpos'][1] for n in old_legs if _kind_of(n) == 'thigh'] or \
                 [max(v[1] + T[n]['gpos'][1] for n in T for v in T[n]['verts']) * 0.45]
            height = max(ys)
    H = float(height)
    if hipx is None:
        xs = [abs(T[n]['gpos'][0]) for n in old_legs if _kind_of(n) == 'thigh']
        hipx = max(xs) if xs else 0.45 * H
    if hipz is None:
        zs = [abs(T[n]['gpos'][2]) for n in old_legs]
        hipz = max(zs) if (zs and kind == 'quad') else 0.6 * H
    new = {}
    def add(name, parent, g, verts=(), prims=()):
        pg = new[parent]['gpos'] if parent else (0.0, 0.0, 0.0)
        new[name] = dict(parent=parent, off=(g[0] - pg[0], g[1] - pg[1], g[2] - pg[2]), gpos=tuple(g),
                         verts=list(verts), prims=list(prims), children=[], src=T.get(name, {}).get('src'))
        if parent:
            new[parent]['children'].append(name)
    pel = T.get('pelvis')
    add('pelvis', None, (0.0, H, 0.0), pel['verts'] if pel else (), pel['prims'] if pel else ())
    lg = (0.0, H + RATIO['legs_y'] * H, 0.0)
    add('legs', 'pelvis', lg)
    for i in ids:
        sx = -1 if i.startswith('r') else 1
        sz = 0.0 if kind == 'biped' else (hipz if i.endswith('f') else -hipz)
        th = (sx * hipx, lg[1], sz)
        kn = (th[0], th[1] + RATIO['knee_y'] * H, th[2] + RATIO['knee_z'] * H)
        an = (kn[0], kn[1] + RATIO['ankle_y'] * H, kn[2] + RATIO['ankle_z'] * H)
        add(i + 'thigh', 'legs', th); add(i + 'leg', i + 'thigh', kn); add(i + 'foot', i + 'leg', an)
    # keep everything else, re-parented
    report = dict(kind=kind, pelvis_height=round(H, 2), hipx=round(hipx, 2), dropped=old_legs, reparented={})
    root = next(n for n, t in T.items() if t['parent'] is None)
    def new_parent(old):
        p = T[old]['parent']
        while p is not None:
            if p in new and p not in old_legs:
                return p
            if p in old_legs:
                g = T[p]['gpos']
                if abs(g[0]) < 0.5 and not _side_hint(p):   # centred hip block (e.g. Warrior's `hips`) = pelvis
                    return 'pelvis'
                s = _side_of(p, g)
                cands = [i for i in ids if i.startswith(s)] or ids
                if kind == 'quad':
                    cands = sorted(cands, key=lambda i: abs((hipz if i.endswith('f') else -hipz) - g[2]))
                return cands[0] + _kind_of(p)
            p = T[p]['parent']
        return 'pelvis'
    for n, t in T.items():
        if n == 'pelvis' or n in old_legs:
            continue
        par = 'pelvis' if n == root else new_parent(n)
        add(n, par, t['gpos'], t['verts'], t['prims'])
        if par != t['parent']:
            report['reparented'][n] = f"{t['parent']} -> {par}"
    return new, report


def leg_points(T, i):
    """global hip/knee/ankle positions of leg i ('r', 'l', 'rf', ...) in a remapped table"""
    from mathutils import Vector
    return dict(hip=Vector(T[i + 'thigh']['gpos']), knee=Vector(T[i + 'leg']['gpos']), ankle=Vector(T[i + 'foot']['gpos']))
