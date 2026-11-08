#!/usr/bin/env python3
"""Audit the game's runtime weapon damage and stats against TA 3.1c.

  DUMP=dump.txt tools/headless-test/run.sh <engine>; defdump.py dump.txt dump.json
  audit_damage.py dump.json ~/ta-data-out/out ~/ta-data-out/cmp

Pairs each runtime weapon with its TA weapon (weapon_diff.csv pairs, same name, or the unit's TA weapon slot), then
for every repo unit compares the damage the game really deals it (damages[unit armorType]) with TA's per-unit list
(or TA's default). Also range, reload, area of effect, projectile speed and burst. Expected rows: the 10 aircraft TA's
anti-air lists predate (DEVIATIONS.md, "Aircraft armor") and projectile speeds raised on purpose (SLOW_SHOT).
"""
import csv, json, sys
from collections import defaultdict
DUMP, OUT, CMP = sys.argv[1:4]
d = json.load(open(DUMP))
W, U = d['W'], d['U']
taw = {k.lower(): v['stats'] for k, v in json.load(open(OUT + '/weapons.json')).items()}
tau = {k.lower(): {kk.lower(): vv for kk, vv in v['stats'].items()} for k, v in json.load(open(OUT + '/units.json')).items()}
umap = {r['repo_file'].lower(): r['ta_id'].lower() for r in csv.DictReader(open(CMP + '/unit_mapping.csv'))}
pairs = defaultdict(set)
for r in csv.DictReader(open(CMP + '/weapon_diff.csv')):
    if r['repo_weapon'] and r['ta_weapon'].lower() in taw:
        pairs[r['repo_weapon'].lower()].add(r['ta_weapon'].lower())
for w in W:
    if w in taw and w not in pairs:
        pairs[w].add(w)
# unit slots: repo weapon id -> name
byid = {v['id']: n for n, v in W.items()}
slotpairs = defaultdict(set)
for u, ta in umap.items():
    if u not in U or ta not in tau: continue
    for i in (1, 2, 3):
        tw = tau[ta].get('weapon%d' % i)
        rid = U[u].get('weapons.%d.weaponDef' % i)
        if tw and rid in byid:
            slotpairs[byid[rid]].add(tw.lower())
def f(x):
    try: return float(x)
    except: return None
issues = []
for rw in sorted(set(pairs) | set(slotpairs)):
    tws = pairs.get(rw) or slotpairs.get(rw)
    if rw not in W: continue
    if slotpairs.get(rw) and pairs.get(rw) and slotpairs[rw] != pairs[rw]:
        issues.append(('PAIRING', rw, 'name/diff pair %s vs unit slot %s' % (sorted(pairs[rw]), sorted(slotpairs[rw]))))
    for tw in sorted(tws):
        t = taw[tw]; dmg = {k.lower(): v for k, v in (t.get('damage') or {}).items()}
        dflt = f(dmg.get('default'))
        rd = W[rw].get('dmg.default')
        if dflt is not None and rd is not None and abs(rd - dflt) > 0.51:
            issues.append(('DEFAULT', rw, 'TA %s=%s, game %s' % (tw, dflt, rd)))
        # per target unit
        bad = defaultdict(list)
        for u, ta in umap.items():
            if u not in U: continue
            want = f(dmg.get(ta, dflt))
            got = W[rw].get('damages.%d' % U[u]['armorType'])
            if want is not None and got is not None and abs(got - want) > 0.51:
                bad[(want, got)].append(u)
        for (want, got), us in sorted(bad.items()):
            issues.append(('TARGET', rw, 'vs %d units TA %s game %s: %s' % (len(us), want, got, ', '.join(sorted(us)[:6]) + (' ...' if len(us) > 6 else ''))))
        for tag, rk, scale in (('range', 'range', 1), ('reloadtime', 'reload', 1), ('areaofeffect', 'damageAreaOfEffect', 2), ('weaponvelocity', 'projectilespeed', 30), ('burst', 'salvoSize', 1)):
            tv = f(t.get(tag)); gv = W[rw].get(rk)
            if tv and gv is not None and not (tag == 'reloadtime' and W[rw].get('stockpile')) and abs(gv * scale - tv) > max(0.02 * tv, 0.6):
                issues.append(('STAT', rw, '%s TA %s game %s' % (tag, tv, round(gv * scale, 2))))
for i in issues: print(*i, sep=' | ')
print(len(issues), 'issues;', len(set(pairs) | set(slotpairs)), 'weapons checked')
unp = [w for w in W if w not in pairs and w not in slotpairs]
print('unpaired runtime weapons:', len(unp), unp)
