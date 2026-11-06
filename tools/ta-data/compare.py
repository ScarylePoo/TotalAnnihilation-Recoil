#!/usr/bin/env python3
"""Compare TA 3.1c unit/weapon values with the TA:Recoil Lua defs.

Usage: compare.py REPO TA_OUT TA_XDIR OUTDIR
"""
import csv, glob, json, os, re, sys
import lupa

REPO, TAOUT, TAX, OUT = sys.argv[1:5]

MANUAL = {
    'ARM_T1_DEF_Mine3': 'armmine3', 'ARM_T1_DEF_Mine5': 'armmine5', 'ARM_T1_DEF_Mine6': 'armmine6',
    'ARM_T2_BOT_DecoyCommander': 'armdecom', 'CORE_T2_BOT_DecoyCommander': 'cordecom',
    'ARM_T2_ECO_FusionPowerplant': 'armfus', 'CORE_T2_ECO_FusionPowerplant': 'corfus',
    'ARM_T2_ECO_CloakableFusion': 'armckfus', 'CORE_T2_ECO_CloakableFusion': 'corckfus',
    'ARM_T2_SEAECO_UWFusionPowerplant': 'armuwfus', 'CORE_T2_SEAECO_UWFusionPowerplant': 'coruwfus',
    'CORE_T2_BOT_Necro': 'cornecro', 'CORE_T2_VEH_Pillager': 'cormart',
    'ARM_T1_SEADEF_Defender': 'armfrt',
}
for _n in range(1, 7):
    MANUAL['ARM_T1_DEF_Mine%d' % _n] = 'armmine%d' % _n
    MANUAL['CORE_T1_DEF_Mine%d' % _n] = 'cormine%d' % _n

# Tags compared for units. Everything gameplay-relevant that TA FBIs carry.
UNIT_KEYS = [
    ('Economy', ['buildcostmetal', 'buildcostenergy', 'buildtime', 'workertime', 'builddistance',
                 'energymake', 'metalmake', 'energyuse', 'makesmetal', 'extractsmetal',
                 'windgenerator', 'tidalgenerator', 'energystorage', 'metalstorage',
                 'cloakcost', 'cloakcostmoving', 'mincloakdistance']),
    ('Durability', ['maxdamage', 'damagemodifier', 'healtime', 'autoheal', 'idleautoheal', 'idletime']),
    ('Movement', ['maxvelocity', 'acceleration', 'brakerate', 'turnrate', 'movementclass',
                  'maxwaterdepth', 'minwaterdepth', 'maxslope', 'waterline', 'cruisealt',
                  'canfly', 'canhover', 'floater', 'upright', 'footprintx', 'footprintz']),
    ('Sensors', ['sightdistance', 'radardistance', 'sonardistance', 'radardistancejam',
                 'sonardistancejam', 'seismicdistance', 'stealth', 'istargetingupgrade']),
    ('Abilities', ['cancloak', 'canresurrect', 'cancapture', 'canload', 'transportcapacity',
                   'transportsize', 'onoffable', 'activatewhenbuilt', 'kamikaze',
                   'kamikazedistance', 'antiweapons', 'commander', 'canstockpile',
                   'canmanualfire', 'canattack', 'canreclamate', 'canrepair']),
    ('Weapons', ['weapon1', 'weapon2', 'weapon3', 'explodeas', 'selfdestructas', 'corpse']),
]

WEAP_KEYS = [
    'range', 'reloadtime', 'damage', 'areaofeffect', 'edgeeffectiveness', 'weaponvelocity',
    'startvelocity', 'weaponacceleration', 'turnrate', 'flighttime', 'weapontimer',
    'energypershot', 'metalpershot', 'accuracy', 'sprayangle', 'tolerance', 'pitchtolerance',
    'burst', 'burstrate', 'projectiles', 'minbarrelangle', 'lineofsight', 'ballistic',
    'dropped', 'vlaunch', 'selfprop', 'tracks', 'guidance', 'turret', 'beamweapon',
    'commandfire', 'stockpile', 'paralyzer', 'paralyzetime', 'noautorange', 'toairweapon',
    'waterweapon', 'firestarter', 'coverage', 'targetable', 'interceptor', 'twophase',
    'cruise', 'duration', 'noexplode', 'groundbounce', 'impulsefactor',
]

lua = lupa.LuaRuntime(unpack_returned_tuples=True)


def tolua(path):
    src = open(path, encoding='latin-1').read()
    fn = lua.eval('function(src, name) Shared = setmetatable({}, {__index=function() return {} end})'
                  ' local f, e = load(src, name) if not f then error(e) end return f() end')
    return conv(fn(src, path))


def conv(v):
    if lupa.lua_type(v) == 'table':
        keys = list(v.keys())
        if keys and all(isinstance(k, (int, float)) for k in keys):
            return [conv(v[k]) for k in sorted(keys)]
        return {str(k).lower(): conv(v[k]) for k in keys}
    return v


def norm(v):
    if v is None or v == '':
        return None
    if isinstance(v, bool):
        return 1 if v else 0
    if isinstance(v, (int, float)):
        return round(float(v), 4)
    s = str(v).strip()
    try:
        return round(float(s), 4)
    except ValueError:
        return s.lower()


def fmt(v):
    if v is None:
        return ''
    if isinstance(v, float) and v == int(v):
        return int(v)
    return v


# ---- load TA data
ta_units = json.load(open(os.path.join(TAOUT, 'units.json')))
ta_weaps = json.load(open(os.path.join(TAOUT, 'weapons.json')))
ta_units = {k: {kk.lower(): vv for kk, vv in v['stats'].items()} for k, v in ta_units.items()}
ta_weaps = {k: v['stats'] for k, v in ta_weaps.items()}
by_name = {}
for k, s in ta_units.items():
    by_name.setdefault((str(s.get('side', '')).upper()[:3], str(s.get('name', '')).lower()), []).append(k)

# ---- load repo
repo_units = {}
for p in sorted(glob.glob(os.path.join(REPO, 'units', '*.lua'))):
    for k, d in tolua(p).items():
        repo_units[os.path.basename(p)[:-4]] = (k, d)
repo_weaps = {}
weap_file = {}
for p in sorted(glob.glob(os.path.join(REPO, 'Weapons', '*.lua'))):
    t = tolua(p)
    for k, d in t.items():
        repo_weaps[k.lower()] = d
        weap_file[k.lower()] = os.path.basename(p)


def find_3do(root, name):
    for p in glob.glob(os.path.join(root, 'objects3d', '*.3do')) + glob.glob(os.path.join(root, '*', 'objects3d', '*.3do')):
        if os.path.basename(p).lower() == name.lower() + '.3do':
            return p


ta3do = {}
for layer in ['totala1.hpi', 'ccdata.ccx', 'btdata.ccx', 'cavedog.ufo', 'rev31.gp3']:
    for p in glob.glob(os.path.join(TAX, layer, 'objects3d', '*.3do')):
        ta3do[os.path.basename(p).lower()] = p
repo3do = {os.path.basename(p).lower(): p for p in glob.glob(os.path.join(REPO, 'objects3d', '*'))}

# ---- map units
mapping = []
for fname, (rid, d) in repo_units.items():
    tid = MANUAL.get(fname)
    how = 'manual'
    if not tid:
        c = by_name.get((str(d.get('side', '')).upper()[:3], str(d.get('name', '')).lower()), [])
        tid = c[0] if len(c) == 1 else None
        how = 'name'
    model = ''
    if tid:
        a = ta3do.get(str(ta_units[tid].get('objectname', tid)).lower() + '.3do')
        b = repo3do.get(str(d.get('objectname', '')).lower() + ('' if str(d.get('objectname', '')).lower().endswith(('.s3o', '.3do')) else '.3do'))
        if a and b:
            model = 'identical' if open(a, 'rb').read() == open(b, 'rb').read() else 'differs'
        elif b and b.endswith('.s3o'):
            model = 's3o'
        else:
            model = 'n/a'
    mapping.append((fname, rid, tid, how, model))

os.makedirs(OUT, exist_ok=True)
with open(os.path.join(OUT, 'unit_mapping.csv'), 'w', newline='') as f:
    w = csv.writer(f)
    w.writerow(['repo_file', 'repo_unitname', 'ta_id', 'matched_by', 'model_vs_ta'])
    w.writerows(mapping)

# ---- unit diffs
unit_rows, wpairs = [], {}
for fname, rid, tid, how, model in mapping:
    if not tid:
        continue
    rd = repo_units[fname][1]
    td = ta_units[tid]
    rws = [x.get('name', x.get('def', '')) if isinstance(x, dict) else x for x in (rd.get('weapons') or [])]
    rws = [str(x).lower() for x in rws]
    rd_flat = dict(rd)
    for i, wn in enumerate(rws[:3]):
        rd_flat['weapon%d' % (i + 1)] = wn
    for group, keys in UNIT_KEYS:
        for k in keys:
            tv, rv = norm(td.get(k)), norm(rd_flat.get(k))
            if k in ('weapon1', 'weapon2', 'weapon3', 'explodeas', 'selfdestructas', 'corpse'):
                if tv is not None or rv is not None:
                    pair = (str(rv or ''), str(tv or ''))
                    if k != 'corpse':
                        wpairs.setdefault(pair, set()).add(fname)
                    if (tv or '') != (rv or ''):
                        unit_rows.append([fname, tid, group, k, fmt(tv), fmt(rv), 'renamed/different', ''])
                continue
            if tv == rv or (tv is None and rv in (0, None)) or (rv is None and tv in (0, None)):
                continue
            pct = ''
            if isinstance(tv, float) and isinstance(rv, float) and tv:
                pct = round((rv - tv) / tv * 100, 1)
            status = 'missing in repo' if rv is None else ('not in TA' if tv is None else 'changed')
            unit_rows.append([fname, tid, group, k, fmt(tv), fmt(rv), status, pct])

with open(os.path.join(OUT, 'unit_diff.csv'), 'w', newline='') as f:
    w = csv.writer(f)
    w.writerow(['repo_unit', 'ta_id', 'group', 'tag', 'ta_3.1c', 'repo', 'status', 'pct_change'])
    w.writerows(unit_rows)

# ---- weapon diffs
weap_rows = []
seen = set()
for (rw, tw), users in sorted(wpairs.items()):
    if (rw, tw) in seen:
        continue
    seen.add((rw, tw))
    rd = repo_weaps.get(rw)
    td = ta_weaps.get(tw)
    note = ''
    if not rw:
        note = 'TA weapon has no repo slot'
    elif not tw:
        note = 'repo weapon has no TA slot'
    elif rd is None:
        note = 'repo weapon def not found'
    elif td is None:
        note = 'TA weapon def not found'
    if note:
        weap_rows.append([rw, tw, weap_file.get(rw, ''), '', '', '', note, '', ' '.join(sorted(users))])
        continue
    rtype = str(rd.get('weapontype', '')).lower()
    for k in WEAP_KEYS:
        if k == 'damage':
            tdm = td.get('damage', {}) if isinstance(td.get('damage'), dict) else {}
            rdm = rd.get('damage', {}) if isinstance(rd.get('damage'), dict) else {}
            for dk in sorted(set(tdm) | set(rdm)):
                tv, rv = norm(tdm.get(dk)), norm(rdm.get(dk))
                if tv != rv:
                    pct = round((rv - tv) / tv * 100, 1) if isinstance(tv, float) and isinstance(rv, float) and tv else ''
                    weap_rows.append([rw, tw, weap_file.get(rw, ''), 'damage.' + dk, fmt(tv), fmt(rv),
                                      'missing in repo' if rv is None else ('not in TA' if tv is None else 'changed'),
                                      pct, ' '.join(sorted(users))])
            continue
        tv, rv = norm(td.get(k)), norm(rd.get(k))
        if tv == rv or (tv is None and rv in (0, None)) or (rv is None and tv in (0, None)):
            continue
        pct = round((rv - tv) / tv * 100, 1) if isinstance(tv, float) and isinstance(rv, float) and tv else ''
        status = 'missing in repo' if rv is None else ('not in TA' if tv is None else 'changed')
        if k == 'weaponvelocity' and (td.get('ballistic') in ('1', 1) or rtype == 'cannon' or rd.get('ballistic') in (1, '1')):
            status += ' (overridden at load by BOTA gravity post-processing)'
        weap_rows.append([rw, tw, weap_file.get(rw, ''), k, fmt(tv), fmt(rv), status, pct, ' '.join(sorted(users))])

with open(os.path.join(OUT, 'weapon_diff.csv'), 'w', newline='') as f:
    w = csv.writer(f)
    w.writerow(['repo_weapon', 'ta_weapon', 'repo_file', 'tag', 'ta_3.1c', 'repo', 'status', 'pct_change', 'used_by'])
    w.writerows(weap_rows)

print('units mapped', sum(1 for m in mapping if m[2]), 'of', len(mapping))
print('unmapped', [m[0] for m in mapping if not m[2]])
from collections import Counter
print('models', Counter(m[4] for m in mapping))
print('unit diff rows', len(unit_rows), 'weapon pairs', len(seen), 'weapon diff rows', len(weap_rows))
