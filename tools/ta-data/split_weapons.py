#!/usr/bin/env python3
"""Undo BOTA's weapon merges where TA had different weapons with different values.

  split_weapons.py REPO TA_OUT CMP [--dry]

BOTA points several units at one weapon def (e.g. commander_laser for both commanders) where TA gave each unit its
own weapon with its own numbers (armcomlaser 60 dmg, corcomlaser 70). For every unit slot (weapon1-3, explodeas,
selfdestructas) whose repo weapon pairs with more than one, differing, TA weapon, the unit is pointed at a def named
like the TA weapon: an existing def of that name, or a copy of the merged def (inserted right after it, same file).
apply.py then writes the TA values into each def. Run compare.py again in between.
"""
import csv, json, os, re, sys
from collections import defaultdict
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import apply as A  # noqa: E402  (reuses its Lua helpers; apply.py only runs its main when executed)

REPO, TAOUT, CMP = sys.argv[1:4]
DRY = '--dry' in sys.argv
SLOTS = ['weapon1', 'weapon2', 'weapon3', 'explodeas', 'selfdestructas']
VALUE_TAGS = sorted(A.WEAP_TAGS)

ta_w = {k: v['stats'] for k, v in json.load(open(os.path.join(TAOUT, 'weapons.json'))).items()}
ta_u = {k.lower(): {kk.lower(): vv for kk, vv in v['stats'].items()} for k, v in json.load(open(os.path.join(TAOUT, 'units.json'))).items()}
mapping = {r['repo_file']: r['ta_id'].lower() for r in csv.DictReader(open(os.path.join(CMP, 'unit_mapping.csv')))}


def sig(t):
    d = ta_w[t]
    dm = d.get('damage') if isinstance(d.get('damage'), dict) else {}
    return tuple(str(d.get(k, '')).lower() for k in VALUE_TAGS) + tuple(sorted((k, str(v)) for k, v in dm.items()))


def unit_slots(stem):
    """{slot: (repo weapon lowercase, line index)} from the unit Lua text."""
    lines = open(os.path.join(REPO, 'units', stem + '.lua'), encoding='latin-1').read().split('\n')
    out = {}
    for i, l in enumerate(lines):
        m = re.match(r'^\t\t(explodeas|selfdestructas)\s*=\s*"([^"]+)"', l, re.I)
        if m:
            out[m.group(1).lower()] = (m.group(2).lower(), i)
    wb = A.find_block(lines, 'weapons', '\t\t')
    if wb:
        n = 0
        for i in range(*wb):
            m = re.match(r'^\t\t\t(?:\[(\d+)\]\s*=\s*)?\{', lines[i])
            if m:
                n = int(m.group(1)) if m.group(1) else n + 1
                for j in range(i + 1, wb[1]):
                    mm = re.match(r'^\t\t\t\tname\s*=\s*"([^"]+)"', lines[j], re.I)
                    if mm:
                        if n <= 3:
                            out['weapon%d' % n] = (mm.group(1).lower(), j)
                        break
                    if re.match(r'^\t\t\t\}', lines[j]):
                        break
    return out, lines


def main():
    files = A.weapon_files()
    pairs = defaultdict(lambda: defaultdict(list))   # rw -> t -> [(stem, slot)]
    slots = {}
    for stem, tid in mapping.items():
        s, _ = unit_slots(stem)
        slots[stem] = s
        for slot in SLOTS:
            if slot in s and ta_u[tid].get(slot):
                t = str(ta_u[tid][slot]).lower()
                if t in ta_w:
                    pairs[s[slot][0]][t].append((stem, slot))
    changes = []
    for rw, tmap in sorted(pairs.items()):
        if len(tmap) < 2 or len({sig(t) for t in tmap}) < 2:
            continue
        for t, uses in sorted(tmap.items()):
            if t == rw:
                continue
            if t not in files:
                if rw not in files:
                    print('cannot clone missing def', rw)
                    continue
                for f in files[rw]:
                    path = os.path.join(REPO, 'Weapons', f)
                    lines = open(path, encoding='latin-1').read().split('\n')
                    s, e = A.find_block(lines, rw, '\t')
                    block = lines[s - 1:e + 1]
                    block[0] = re.sub(r'^(\t)(?:[A-Za-z0-9_\-]+|\[["\'][^"\']+["\']\])', r'\g<1>%s' % t, block[0])
                    block.insert(1, '\t\t-- TA 3.1c weapon %s (BOTA used %s for it as well)' % (t, rw))
                    lines[e + 1:e + 1] = block
                    if not DRY:
                        open(path, 'w', encoding='latin-1').write('\n'.join(lines))
                files[t] = files[rw]
                changes.append('clone %s -> %s (%s)' % (rw, t, ', '.join(files[rw])))
            for stem, slot in uses:
                path = os.path.join(REPO, 'units', stem + '.lua')
                s, lines = unit_slots(stem)
                i = s[slot][1]
                lines[i] = re.sub(r'"[^"]+"', '"%s"' % t.upper(), lines[i], count=1)
                if not DRY:
                    open(path, 'w', encoding='latin-1').write('\n'.join(lines))
                changes.append('%s %s: %s -> %s' % (stem, slot, rw, t))
    print('\n'.join(changes))
    print(len(changes), 'changes')


if __name__ == '__main__':
    main()
