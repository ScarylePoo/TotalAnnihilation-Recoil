#!/usr/bin/env python3
"""Turn compare.py output into clean, classified diff tables.

Usage: finalize.py REPO TA_OUT TA_MERGED CMPDIR
"""
import csv, json, os, re, sys
import lupa

REPO, TAOUT, TAM, CMP = sys.argv[1:5]
sys.path.insert(0, os.path.dirname(__file__))
from tadump import parse_tdf, read  # noqa: E402

lua = lupa.LuaRuntime()


def conv(v):
    if lupa.lua_type(v) == 'table':
        ks = list(v.keys())
        if ks and all(isinstance(k, (int, float)) for k in ks):
            return [conv(v[k]) for k in sorted(ks)]
        return {str(k).lower(): conv(v[k]) for k in ks}
    return v


def num(v):
    try:
        return float(v)
    except (TypeError, ValueError):
        return None


def fmtn(v):
    f = num(v)
    if f is None:
        return v
    return int(f) if f == int(f) else round(f, 4)


# ---- movement classes, effective values
ta_moves = {d['name'].lower(): d for d in parse_tdf(read(os.path.join(TAM, 'gamedata', 'moveinfo.tdf'))).values()
            if isinstance(d, dict) and 'name' in d}
repo_moves = {str(d['name']).lower(): d for d in conv(lua.execute(open(os.path.join(REPO, 'gamedata', 'movedefs.lua')).read()))}
MOVE_KEYS = ['footprintx', 'footprintz', 'maxslope', 'maxwaterdepth', 'minwaterdepth', 'maxwaterslope']

ta_units = {k: {kk.lower(): vv for kk, vv in v['stats'].items()} for k, v in json.load(open(os.path.join(TAOUT, 'units.json'))).items()}
mapping = {r['repo_file']: r for r in csv.DictReader(open(os.path.join(CMP, 'unit_mapping.csv')))}
repo_units = {}
for f in mapping:
    t = conv(lua.execute('Shared = setmetatable({}, {__index=function() return {} end})\n' +
                         open(os.path.join(REPO, 'units', f + '.lua'), encoding='latin-1').read()))
    repo_units[f] = list(t.values())[0]


def eff_move(unit, moves):
    mc = str(unit.get('movementclass') or '').lower()
    md = moves.get(mc)
    out = {}
    for k in MOVE_KEYS:
        v = md.get(k) if md else None
        if v is None:
            v = unit.get(k)
        out[k] = num(v)
    return mc, out


# ---- classification
NAMING = {'corpse', 'weapon1', 'weapon2', 'weapon3', 'explodeas', 'selfdestructas'}
MOVE_FBI = {'movementclass', 'footprintx', 'footprintz', 'maxslope', 'maxwaterdepth', 'minwaterdepth'}
ENGINE_DEFAULT_TRUE = {'canattack', 'canreclamate', 'canrepair'}
LABEL = {
    'buildcostmetal': 'Metal cost', 'buildcostenergy': 'Energy cost', 'buildtime': 'Build time',
    'workertime': 'Build power', 'builddistance': 'Build range', 'energymake': 'Energy produced',
    'metalmake': 'Metal produced', 'energyuse': 'Energy upkeep', 'makesmetal': 'Metal converted',
    'extractsmetal': 'Metal extraction', 'windgenerator': 'Wind output', 'tidalgenerator': 'Tidal output',
    'energystorage': 'Energy storage', 'metalstorage': 'Metal storage', 'cloakcost': 'Cloak cost (still)',
    'cloakcostmoving': 'Cloak cost (moving)', 'mincloakdistance': 'Decloak distance',
    'maxdamage': 'Hit points', 'damagemodifier': 'Armored damage modifier', 'maxvelocity': 'Max speed',
    'acceleration': 'Acceleration', 'brakerate': 'Brake rate', 'turnrate': 'Turn rate',
    'sightdistance': 'Sight range', 'radardistance': 'Radar range', 'sonardistance': 'Sonar range',
    'radardistancejam': 'Radar jam range', 'sonardistancejam': 'Sonar jam range', 'cruisealt': 'Cruise altitude',
    'waterline': 'Waterline', 'idleautoheal': 'Idle regen', 'idletime': 'Idle time before regen',
    'transportcapacity': 'Transport capacity', 'transportsize': 'Transport size',
}


def unit_kind(tag, status):
    if tag in ('idleautoheal', 'idletime') or status == 'not in TA':
        return 'Recoil-only tag'
    if tag in ('activatewhenbuilt', 'onoffable') or (tag in ENGINE_DEFAULT_TRUE and status == 'missing in repo'):
        return 'Convention'
    return 'Balance'


unit_rows = []
for r in csv.DictReader(open(os.path.join(CMP, 'unit_diff.csv'))):
    tag = r['tag']
    if tag in NAMING or tag in MOVE_FBI:
        continue
    if tag in ('energymake', 'energyuse'):
        s = ta_units[r['ta_id']]
        if num(s.get('energymake')) == num(s.get('energyuse')) and not repo_units[r['repo_unit']].get('energymake') \
                and not repo_units[r['repo_unit']].get('energyuse'):
            continue  # TA make == use, net zero; repo has neither, same result
    kind = unit_kind(tag, r['status'])
    unit_rows.append(dict(unit=r['repo_unit'], ta_id=r['ta_id'], group=r['group'], stat=LABEL.get(tag, tag), tag=tag,
                          ta=r['ta_3.1c'], repo=r['repo'], status=r['status'], pct=r['pct_change'], kind=kind))

# Effective movement comparison.
for f, m in mapping.items():
    tu, ru = ta_units[m['ta_id']], repo_units[f]
    tmc, te = eff_move(tu, ta_moves)
    rmc, re_ = eff_move(ru, repo_moves)
    if tu.get('canfly') in ('1', 1):
        continue
    for k in MOVE_KEYS:
        a, b = te[k], re_[k]
        if k == 'maxwaterslope':
            continue
        if (a or 0) == (b or 0):
            continue
        pct = round((b - a) / a * 100, 1) if a and b is not None else ''
        unit_rows.append(dict(unit=f, ta_id=m['ta_id'], group='Movement',
                              stat={'footprintx': 'Footprint X', 'footprintz': 'Footprint Z', 'maxslope': 'Max slope',
                                    'maxwaterdepth': 'Max water depth', 'minwaterdepth': 'Min water depth'}[k],
                              tag='%s (%s -> %s)' % (k, tmc or '-', rmc or '-'), ta=fmtn(a) if a is not None else '',
                              repo=fmtn(b) if b is not None else '', status='changed' if a is not None and b is not None else
                              ('missing in repo' if b is None else 'not in TA'), pct=pct, kind='Balance'))

# ---- weapons
TYPE_TAGS = {'lineofsight', 'ballistic', 'dropped', 'vlaunch', 'selfprop', 'tracks', 'guidance', 'beamweapon',
             'twophase', 'noautorange', 'toairweapon', 'turret', 'minbarrelangle', 'pitchtolerance', 'cruise'}
wrows_raw = list(csv.DictReader(open(os.path.join(CMP, 'weapon_diff.csv'))))
ta_weaps = {k: v['stats'] for k, v in json.load(open(os.path.join(TAOUT, 'weapons.json'))).items()}
weapon_rows = []
per_target_done = set()
WL = {'range': 'Range', 'reloadtime': 'Reload time', 'damage.default': 'Damage', 'areaofeffect': 'Area of effect',
      'edgeeffectiveness': 'Edge effectiveness', 'weaponvelocity': 'Projectile speed', 'startvelocity': 'Start speed',
      'weaponacceleration': 'Acceleration', 'turnrate': 'Turn rate (guided)', 'flighttime': 'Flight time',
      'weapontimer': 'Weapon timer', 'energypershot': 'Energy per shot', 'metalpershot': 'Metal per shot',
      'accuracy': 'Accuracy', 'sprayangle': 'Spray angle', 'tolerance': 'Aim tolerance', 'burst': 'Burst',
      'burstrate': 'Burst rate', 'duration': 'Beam duration', 'paralyzetime': 'Paralyze time', 'coverage': 'Coverage'}
for r in wrows_raw:
    tag = r['tag']
    if not tag:
        weapon_rows.append(dict(weapon=r['repo_weapon'], ta_weapon=r['ta_weapon'], file=r['repo_file'], stat='(pairing)',
                                tag='', ta='', repo='', status=r['status'], pct='', kind='Note', used_by=r['used_by']))
        continue
    if tag.startswith('damage.') and tag != 'damage.default':
        key = (r['repo_weapon'], r['ta_weapon'])
        if key in per_target_done:
            continue
        per_target_done.add(key)
        tdm = ta_weaps[r['ta_weapon']].get('damage', {})
        targets = {k: num(v) for k, v in tdm.items() if k != 'default'}
        vals = sorted(set(targets.values()))
        # find repo per-class damage
        rd = None
        for p in [os.path.join(REPO, 'Weapons', r['repo_file'])]:
            t = conv(lua.execute(open(p, encoding='latin-1').read()))
            rd = {k.lower(): v for k, v in t.items()}.get(r['repo_weapon'], {}).get('damage', {})
        rclasses = {k: v for k, v in rd.items() if k != 'default'}
        weapon_rows.append(dict(
            weapon=r['repo_weapon'], ta_weapon=r['ta_weapon'], file=r['repo_file'], stat='Per-target damage',
            tag='damage.<units>',
            ta='default %s; vs %d listed units: %s' % (fmtn(tdm.get('default', '')), len(targets),
                                                       '/'.join(str(fmtn(v)) for v in vals)) if targets else
               'default %s only' % fmtn(tdm.get('default', '')),
            repo='default %s; %s' % (fmtn(rd.get('default', '')),
                                     ', '.join('%s=%s' % (k, fmtn(v)) for k, v in rclasses.items()) or 'no per-class damage'),
            status='TA lists per unit; repo uses armor classes', pct='', kind='Balance', used_by=r['used_by']))
        continue
    if tag in TYPE_TAGS or tag == 'interceptor':
        kind = 'Convention'
    elif r['status'].startswith('not in TA'):
        kind = 'Recoil-only tag'
    else:
        kind = 'Balance'
    weapon_rows.append(dict(weapon=r['repo_weapon'], ta_weapon=r['ta_weapon'], file=r['repo_file'],
                            stat=WL.get(tag, tag), tag=tag, ta=r['ta_3.1c'], repo=r['repo'], status=r['status'],
                            pct=r['pct_change'], kind=kind, used_by=r['used_by']))

for name, rows in (('units_final.csv', unit_rows), ('weapons_final.csv', weapon_rows)):
    with open(os.path.join(CMP, name), 'w', newline='') as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(rows)

from collections import Counter
print('units', len(unit_rows), Counter(r['kind'] for r in unit_rows))
print('weapons', len(weapon_rows), Counter(r['kind'] for r in weapon_rows))
