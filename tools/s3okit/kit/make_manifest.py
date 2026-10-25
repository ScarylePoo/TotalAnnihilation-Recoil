"""Build manifest.json/manifest.md: user's unit list -> XTA unit defs, scripts, models, corpse chain.
usage: python3 make_manifest.py <xta repo> <unit_list.txt> <out_dir>"""
import re, glob, os, sys, json, struct
repo, listf, out = sys.argv[1:4]

def kv(t, k):
    m = re.search(r'(?im)^\s*%s\s*=\s*([^;\r\n]*);' % k, t)
    return m.group(1).strip() if m else None

units = []
SUBFACTION_DIRS = {'Talon', 'Guardians of Kadesh', 'TheLostLegacy', 'critters', 'fleabowl', 'spidertortoise', 'xtaids', 'cheatonly', 'MinesUtillity', 'rockettoggle'}
# request name -> unitnames, where the in-game name differs from the TA name on the list
ALIASES = {
    'advanced construction sub': ['arm_adv_construction_sub', 'core_adv_construction_sub'],
    'cloakable fusion reactor': ['arm_cloakable_fusion_reactor', 'core_cloakable_fusion_power_plant'],
    'fusion power plant': ['core_fusion_power_plant', 'core_light_fusion_power_plant'],
    'fusion reactor': ['arm_fusion_reactor'],
    'missile frigate': ['core_missile_frigate'],
    'l.l.t': ['arm_light_laser_tower'],
    'light laser tower': ['core_light_laser_tower'],
    'defender - ns': ['arm_floating_defender', 'arm_defender_ns', 'armdl'],
}
def slug(s): return re.sub(r'[^a-z0-9]+', '_', s.lower()).strip('_')
for f in glob.glob(os.path.join(repo, 'units/**/*.fbi'), recursive=True):
    t = open(f, errors='replace').read()
    side = (kv(t, 'side') or '').upper()
    if side not in ('ARM', 'CORE', 'COR'):
        continue
    subdir = os.path.dirname(os.path.relpath(f, os.path.join(repo, 'units')))
    if subdir in SUBFACTION_DIRS:      # Talon / Guardians / Lost Legacy etc. reuse side=Arm/Core
        continue
    units.append(dict(fbi=os.path.relpath(f, repo), unitname=kv(t, 'unitname'), name=kv(t, 'name'),
                      side='ARM' if side == 'ARM' else 'CORE', description=kv(t, 'description'),
                      objectname=kv(t, 'objectname'), corpse=kv(t, 'corpse'),
                      footprint=[kv(t, 'footprintx'), kv(t, 'footprintz')],
                      sub=os.path.dirname(os.path.relpath(f, os.path.join(repo, 'units'))) or None))

# features: name -> dict
feats = {}
for f in glob.glob(os.path.join(repo, 'features/**/*.tdf'), recursive=True):
    t = open(f, errors='replace').read()
    for m in re.finditer(r'\[([^\]]+)\]\s*\{(.*?)\n\}', t, re.S):
        body = m.group(2)
        feats[m.group(1).strip().lower()] = dict(tdf=os.path.relpath(f, repo), object=kv(body, 'object'),
                                                  featuredead=kv(body, 'featuredead'),
                                                  footprint=[kv(body, 'footprintx'), kv(body, 'footprintz')])

objs = {os.path.basename(p).lower(): os.path.relpath(p, repo) for p in glob.glob(os.path.join(repo, 'objects3d/**/*'), recursive=True)}
def objpath(n):
    if not n: return None
    n = n.lower()
    for c in (n, n + '.3do', n + '.s3o'):
        if c in objs: return objs[c]
    return None

def pieces_3do(path):
    try:
        d = open(os.path.join(repo, path), 'rb').read()
        names = []
        def walk(off, root=False):
            while off or root:
                root = False
                v = struct.unpack_from('<13i', d, off)
                names.append(d[v[7]:d.index(b'\0', v[7])].decode('latin1'))
                walk(v[12]); off = v[11]
        walk(0, True)
        return names
    except Exception as e:
        return ['?' + str(e)]

wanted = [l.strip() for l in open(listf) if l.strip() and len(l.strip()) > 1 and not l.startswith(('Now', '(', '#')) and
          not l.startswith('It is') and not l.startswith('The list') and not l.startswith('Please')]
rows = []
for w in wanted:
    m = re.match(r'(.*?)\s*\((ARM|CORE)\)\s*$', w, re.I)
    nm, side = (m.group(1), m.group(2).upper()) if m else (w, None)
    if nm.lower() in ALIASES:
        cands = [u for u in units if (u['unitname'] or '').lower() in ALIASES[nm.lower()]]
    else:
        cands = [u for u in units if (u['name'] or '').lower() == nm.lower() and (side is None or u['side'] == side)]
    if not cands:
        cands = [u for u in units if re.sub(r'^(arm|core)_', '', (u['unitname'] or '').lower()) == slug(nm) and (side is None or u['side'] == side)]
    if not cands:  # loose match: ignore punctuation
        k = re.sub(r'[^a-z0-9]', '', nm.lower())
        cands = [u for u in units if re.sub(r'[^a-z0-9]', '', (u['name'] or '').lower()) == k and (side is None or u['side'] == side)]
    base = [u for u in cands if not re.search(r'_(rt|xtra)$', (u['unitname'] or ''), re.I)]
    rows.append(dict(request=w, matches=base or cands,
                     variants=[u['unitname'] for u in cands if base and u not in base]))

def chain(u):
    c = []
    f = (u['corpse'] or '').lower()
    seen = set()
    while f and f in feats and f not in seen:
        seen.add(f); fd = feats[f]
        c.append(dict(feature=f, object=fd['object'], model=objpath(fd['object']), tdf=fd['tdf']))
        f = (fd['featuredead'] or '').lower()
    return c

for r in rows:
    for u in r['matches']:
        u['model'] = objpath(u['objectname'])
        u['pieces'] = pieces_3do(u['model']) if u['model'] and u['model'].lower().endswith('.3do') else None
        u['script'] = next((p for p in (f"scripts/{u['unitname']}.cob", f"scripts/bos/{u['unitname']}.bos",
                                         f"scripts/{u['unitname']}.lua") if os.path.exists(os.path.join(repo, p))), None)
        u['corpse_chain'] = chain(u)

os.makedirs(out, exist_ok=True)
json.dump(rows, open(os.path.join(out, 'manifest.json'), 'w'), indent=1)
LEGWORDS = re.compile(r'(thigh|leg|shin|calf|knee|foot|feet|boot|ankle|toe|hip)', re.I)
def model_pieces(u):
    if not u.get('model'):
        return []
    if u['model'].lower().endswith('.3do'):
        return u['pieces'] or []
    try:
        sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
        from s3okit import s3o as S3O
        return [p['name'] for p in S3O.read(os.path.join(repo, u['model']))['pieces']]
    except Exception:
        return []
legged = []
for r in rows:
    for u in r['matches']:
        names = model_pieces(u)
        legs = [n for n in names if LEGWORDS.search(n) and not re.search(r'(flare|fire|emit|leg_?sfx)', n, re.I)]
        feet = [n for n in names if re.search(r'(foot|feet|boot|toe)', n, re.I)]
        if legs:
            nleg = len(feet) or len([n for n in legs if re.search('thigh', n, re.I)]) or len(legs)
            legged.append(dict(request=r['request'], unitname=u['unitname'], model=u['model'], leg_pieces=legs, feet=len(feet),
                               guess=('quad' if nleg >= 4 else 'biped')))
json.dump(legged, open(os.path.join(out, 'legged.json'), 'w'), indent=1)
heaps = sorted({c['object'] for r in rows for u in r['matches'] for c in u['corpse_chain'][1:] if c['object']})
with open(os.path.join(out, 'manifest.md'), 'w') as o:
    o.write('# Unit manifest (generated by make_manifest.py)\n\n')
    o.write('| Request | unitname | side | model | pieces | script | corpse model | heap model |\n|---|---|---|---|---|---|---|---|\n')
    miss = []
    for r in rows:
        if not r['matches']:
            miss.append(r['request']); continue
        for u in r['matches']:
            ch = u['corpse_chain']
            o.write(f"| {r['request']} | {u['unitname']} | {u['side']} | {u['model'] or 'MISSING ' + str(u['objectname'])} | "
                    f"{len(u['pieces']) if u['pieces'] else '-'} | {'yes' if u['script'] else 'NO'} | "
                    f"{ch[0]['model'] if ch else '-'} | {ch[1]['object'] if len(ch) > 1 else '-'} |\n")
    o.write('\n## Requests with no Arm/Core unit def matching by name\n\n' + ''.join(f'- {m}\n' for m in miss))
    o.write('\n## Generic heap models referenced by these corpses\n\n' + ', '.join(heaps) + '\n')
    o.write('\n## Legged units (by leg-like piece names in the current model; verify each with `run.py inspect`)\n\n'
            '| Request | unitname | guess | feet | leg pieces in current model |\n|---|---|---|---|---|\n')
    for L in legged:
        o.write(f"| {L['request']} | {L['unitname']} | {L['guess']} | {L['feet']} | {', '.join(L['leg_pieces'])} |\n")
print('requests', len(rows), 'matched', sum(1 for r in rows if r['matches']), 'unit defs', sum(len(r['matches']) for r in rows))
print('unmatched:', [r['request'] for r in rows if not r['matches']])
print('multi:', [(r['request'], [u['unitname'] for u in r['matches']]) for r in rows if len(r['matches']) > 1])
print('heaps:', heaps)
