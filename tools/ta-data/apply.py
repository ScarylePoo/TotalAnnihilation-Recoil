#!/usr/bin/env python3
"""Write TA 3.1c values into the TA:Recoil Lua defs (text edits: key order and comments are kept).

  apply.py REPO TA_OUT CMP [--dry]

Reads the classified diff (finalize.py output in CMP) and the TA stats (tadump.py output in TA_OUT).
Every changed line gets a trailing comment "-- TA 3.1c (was <old>)". Prints a report of what it did and what it
skipped, and writes CMP/apply_report.json.
What is deliberately NOT applied (see DEVIATIONS.md): waterline, footprints, movement slopes, upright,
Recoil-only tags, weapon type tags, beam duration (visual, handled by the laser pass).
"""
import csv, json, os, re, sys
from collections import Counter, defaultdict

if __name__ == '__main__':
    REPO, TAOUT, CMP = sys.argv[1:4]
    DRY = '--dry' in sys.argv
else:   # imported for its helpers (split_weapons.py)
    REPO, TAOUT, CMP = sys.argv[1:4]
    DRY = True

UNIT_TAGS = {
    'buildcostmetal', 'buildcostenergy', 'buildtime', 'workertime', 'builddistance', 'energymake', 'metalmake',
    'energyuse', 'extractsmetal', 'energystorage', 'metalstorage', 'cloakcost', 'cloakcostmoving',
    'mincloakdistance', 'maxdamage', 'damagemodifier', 'maxvelocity', 'acceleration', 'brakerate', 'turnrate',
    'sightdistance', 'radardistance', 'sonardistance', 'radardistancejam', 'sonardistancejam', 'cruisealt',
    'transportcapacity', 'transportsize', 'kamikazedistance', 'makesmetal',
}
WEAP_TAGS = {
    'range', 'reloadtime', 'areaofeffect', 'edgeeffectiveness', 'weaponvelocity', 'startvelocity',
    'weaponacceleration', 'turnrate', 'flighttime', 'weapontimer', 'energypershot', 'metalpershot', 'accuracy',
    'sprayangle', 'tolerance', 'burst', 'burstrate', 'projectiles', 'paralyzetime', 'coverage',
}

report = defaultdict(list)


def fmt(v):
    try:
        f = float(v)
    except ValueError:  # TA data typos such as "13O" (letter O) for 130
        f = float(str(v).strip().upper().replace('O', '0'))
        report['notes'].append('TA value %r read as %s' % (v, f))
    if f == int(f):
        return str(int(f))
    return repr(round(f, 4))


# ------------------------------------------------------------------ Lua text editing
LINE = r'^(?P<ind>[ \t]+)(?P<key>%s)(?P<eq>\s*=\s*)(?P<val>[^,\n]*?)(?P<comma>\s*,)(?P<rest>[^\n]*)$'


def set_in_block(lines, start, end, tag, value, indent, insert_before=None):
    """Set `tag = value` among lines[start:end] at exactly `indent`. Returns (old value or None, new lines)."""
    rx = re.compile(LINE % re.escape(tag), re.I)
    for i in range(start, end):
        m = rx.match(lines[i])
        if m and m.group('ind') == indent:
            old = m.group('val').strip()
            if old == value:
                return old, lines
            comment = '  -- TA 3.1c (was %s)' % old
            rest = m.group('rest')
            rest = re.sub(r'\s*--\s*TA 3\.1c \(was [^)]*\)', '', rest)
            lines[i] = '%s%s%s%s,%s%s' % (m.group('ind'), m.group('key'), m.group('eq'), value, comment, rest)
            return old, lines
    # insert
    pos = end
    if insert_before:
        for i in range(start, end):
            if re.match(r'^%s%s\b' % (re.escape(indent), insert_before), lines[i], re.I):
                pos = i
                break
    lines.insert(pos, '%s%s = %s,  -- TA 3.1c (was unset)' % (indent, tag, value))
    return None, lines


def find_block(lines, name, indent):
    """Lines of `name = {` ... matching close at `indent`. Returns (start, end) exclusive of braces or None."""
    rx = re.compile(r'^%s(?:%s|\[["\']%s["\']\])\s*=\s*\{\s*$' % (re.escape(indent), re.escape(name), re.escape(name)), re.I)
    for i, l in enumerate(lines):
        if rx.match(l):
            for j in range(i + 1, len(lines)):
                if re.match(r'^%s\}' % re.escape(indent), lines[j]):
                    return i + 1, j
    return None


# ------------------------------------------------------------------ units
def apply_units():
    rows = [r for r in csv.DictReader(open(os.path.join(CMP, 'units_final.csv'))) if r['kind'] == 'Balance']
    by_unit = defaultdict(list)
    for r in rows:
        tag = r['tag'].split(' ')[0]
        if tag in UNIT_TAGS and r['status'] in ('changed', 'missing in repo') and r['ta'] != '':
            by_unit[r['unit']].append((tag, r['ta']))
        elif r['kind'] == 'Balance':
            report['unit_skipped'].append('%s %s %s->%s' % (r['unit'], r['tag'], r['ta'], r['repo']))
    n = 0
    for unit, items in sorted(by_unit.items()):
        path = os.path.join(REPO, 'units', unit + '.lua')
        lines = open(path, encoding='latin-1').read().split('\n')
        blk = find_block(lines, unit.lower(), '\t')
        if not blk:
            report['errors'].append('no def block in ' + path)
            continue
        for tag, val in items:
            s, e = find_block(lines, unit.lower(), '\t')
            old, lines = set_in_block(lines, s, e, tag, fmt(val), '\t\t', insert_before='-- movement')
            n += 1
            report['unit_changes'].append('%s %s %s -> %s' % (unit, tag, old, fmt(val)))
        if not DRY:
            open(path, 'w', encoding='latin-1').write('\n'.join(lines))
    print('unit values set:', n, 'in', len(by_unit), 'units')


# ------------------------------------------------------------------ weapons
def weapon_files():
    """lowercased weapon name -> list of files defining it (some weapons exist in two files)."""
    out = defaultdict(list)
    for p in sorted(os.listdir(os.path.join(REPO, 'Weapons'))):
        if not p.endswith('.lua'):
            continue
        for l in open(os.path.join(REPO, 'Weapons', p), encoding='latin-1'):
            m = re.match(r'^\t(?:([A-Za-z0-9_\-]+)|\[["\']([^"\']+)["\']\])\s*=\s*\{\s*$', l)
            if m:
                out[(m.group(1) or m.group(2)).lower()].append(p)
    return out


def ta_air_ids():
    tu = json.load(open(os.path.join(TAOUT, 'units.json')))
    return {k.lower() for k, v in tu.items() if str(v['stats'].get('canfly', '0')) == '1'}


def apply_weapons():
    ta_w = {k: v['stats'] for k, v in json.load(open(os.path.join(TAOUT, 'weapons.json'))).items()}
    rows = list(csv.DictReader(open(os.path.join(CMP, 'weapon_diff.csv'))))
    pairs = defaultdict(set)   # repo weapon -> set of TA weapons
    users = {}
    for r in rows:
        if r['repo_weapon'] and r['ta_weapon'] and r['ta_weapon'] in ta_w:
            pairs[r['repo_weapon']].add(r['ta_weapon'])
            users[r['repo_weapon']] = r['used_by']
    # weapons whose values all agree with TA are absent from the diff: fine, nothing to do.
    files = weapon_files()
    air = ta_air_ids()
    n = 0
    for rw, tws in sorted(pairs.items()):
        if rw not in files:
            report['errors'].append('repo weapon %s not found in Weapons/' % rw)
            continue
        # pick values; if several TA weapons pair with one repo weapon, they must agree
        want = {}
        for tag in WEAP_TAGS:
            vals = {fmt(ta_w[t][tag]) for t in tws if ta_w[t].get(tag) not in (None, '')}
            if len(vals) == 1:
                want[tag] = vals.pop()
            elif len(vals) > 1:
                report['weapon_conflicts'].append('%s %s TA %s: %s' % (rw, tag, sorted(tws), sorted(vals)))
        dmg = {}
        defaults = {fmt(ta_w[t]['damage']['default']) for t in tws if isinstance(ta_w[t].get('damage'), dict) and 'default' in ta_w[t]['damage']}
        if len(defaults) == 1:
            dmg['default'] = defaults.pop()
        elif defaults:
            report['weapon_conflicts'].append('%s damage.default TA %s: %s' % (rw, sorted(tws), sorted(defaults)))
        # per-target damage vs aircraft -> armor class "planes"
        vs_air, vs_other = Counter(), Counter()
        for t in tws:
            d = ta_w[t].get('damage') or {}
            for k, v in d.items():
                if k == 'default':
                    continue
                (vs_air if k in air else vs_other)[fmt(v)] += 1
        if vs_air:
            dmg['planes'] = vs_air.most_common(1)[0][0]
            if len(vs_air) > 1:
                report['notes'].append('%s: TA damage vs aircraft varies %s; used the most common' % (rw, dict(vs_air)))
        if vs_other:
            report['per_unit_damage_not_applied'].append('%s (%s): TA damage vs %d non-aircraft units %s' % (
                rw, users.get(rw, ''), sum(vs_other.values()), dict(vs_other)))
        for f in files[rw]:
            path = os.path.join(REPO, 'Weapons', f)
            lines = open(path, encoding='latin-1').read().split('\n')
            for tag, val in sorted(want.items()):
                s, e = find_block(lines, rw, '\t')
                old, lines = set_in_block(lines, s, e, tag, val, '\t\t', insert_before='damage')
                if old != val:
                    n += 1
                    report['weapon_changes'].append('%s %s %s -> %s' % (rw, tag, old, val))
            s, e = find_block(lines, rw, '\t')
            ds = find_block(lines[s:e], 'damage', '\t\t')
            if ds is None:
                report['errors'].append('%s: no damage table in %s' % (rw, f))
            else:
                for k, val in dmg.items():
                    s, e = find_block(lines, rw, '\t')
                    ds = find_block(lines[s:e], 'damage', '\t\t')
                    old, lines = set_in_block(lines, s + ds[0], s + ds[1], k, val, '\t\t\t')
                    if old != val:
                        n += 1
                        report['weapon_changes'].append('%s damage.%s %s -> %s' % (rw, k, old, val))
            if not DRY:
                open(path, 'w', encoding='latin-1').write('\n'.join(lines))
    print('weapon values set:', n, 'over', len(pairs), 'weapons')


if __name__ != '__main__':
    pass
else:
  apply_units()
  apply_weapons()
  json.dump(report, open(os.path.join(CMP, 'apply_report.json'), 'w'), indent=1)
  for k, v in report.items():
      print('%s: %d' % (k, len(v)))
  for k in ('errors', 'weapon_conflicts'):
      for x in report.get(k, []):
          print('  ', k, x)
