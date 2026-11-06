#!/usr/bin/env python3
"""Compare aim turn speeds (deg/s) in TA COB scripts vs TA:Recoil unit scripts."""
import csv, glob, json, os, re, sys
sys.path.insert(0, os.path.dirname(__file__))
from aimspeeds import cob_aim, lua_aim

REPO, TAOUT, TAX, CMP = sys.argv[1:5]
LAYERS = ['totala1.hpi', 'ccdata.ccx', 'btdata.ccx', 'cavedog.ufo', 'rev31.gp3']

ta_cob = {}
for L in LAYERS:
    for p in glob.glob(os.path.join(TAX, L, 'scripts', '*.cob')):
        ta_cob[os.path.basename(p)[:-4].lower()] = p
repo_scripts = {os.path.basename(p).lower(): p for p in glob.glob(os.path.join(REPO, 'scripts', '*'))}
ta_units = json.load(open(os.path.join(TAOUT, 'units.json')))
mapping = list(csv.DictReader(open(os.path.join(CMP, 'unit_mapping.csv'))))


def slot(fn):
    f = fn.lower()
    for k, n in (('primary', 1), ('secondary', 2), ('tertiary', 3)):
        if k in f:
            return n
    m = re.search(r'(\d+)$', f)
    return int(m.group(1)) if m else 1


def summarize(entries):
    """{(slot, axis): {'pieces': set, 'speeds': list}} ignoring zero/'expr' noise kept separately."""
    out = {}
    for fn, piece, axis, sp in entries:
        k = (piece, axis)
        e = out.setdefault(k, {'pieces': set(), 'speeds': [], 'raw': []})
        e['pieces'].add(piece)
        e['raw'].append('%s:%s' % (piece, sp))
        if isinstance(sp, float):
            e['speeds'].append(sp)
    return out


rows, status_rows = [], []
for m in mapping:
    f, tid = m['repo_file'], m['ta_id']
    src = open(os.path.join(REPO, 'units', f + '.lua'), encoding='latin-1').read()
    sm = re.search(r'\bscript\s*=\s*"([^"]+)"', src)
    on = re.search(r'objectname\s*=\s*"([^"]+)"', src).group(1)
    rname = sm.group(1) if sm else re.sub(r'\.(s3o|3do)$', '', on, flags=re.I) + '.cob'
    rpath = repo_scripts.get(rname.lower())
    tobj = str(ta_units[tid]['stats'].get('objectname', tid)).lower()
    tpath = ta_cob.get(tobj) or ta_cob.get(tid)
    if not rpath or not tpath:
        status_rows.append([f, tid, rname, 'script missing (%s)' % ('repo' if not rpath else 'TA'), '', ''])
        continue
    same = rpath.lower().endswith('.cob') and open(rpath, 'rb').read() == open(tpath, 'rb').read()
    ta = summarize(cob_aim(tpath))
    rp = summarize(lua_aim(rpath) if rpath.endswith('.lua') else cob_aim(rpath))
    kind = 'Lua' if rpath.endswith('.lua') else 'COB'
    status_rows.append([f, tid, os.path.basename(rpath), kind, 'identical to TA' if same else 'differs', len(ta)])
    if same:
        continue
    for k in sorted(set(ta) | set(rp)):
        a, b = ta.get(k), rp.get(k)
        sa = max(a['speeds']) if a and a['speeds'] else None
        sb = max(b['speeds']) if b and b['speeds'] else None
        if sa == sb:
            continue
        pct = round((sb - sa) / sa * 100, 1) if sa and sb is not None else ''
        rows.append(dict(unit=f, ta_id=tid, script=kind, piece=k[0],
                         axis={'y': 'y (traverse)', 'x': 'x (elevation)', 'z': 'z (roll/spin)'}.get(k[1], k[1]),
                         ta_pieces=' '.join(sorted(a['pieces'])) if a else '',
                         repo_pieces=' '.join(sorted(b['pieces'])) if b else '',
                         ta_speed=sa if sa is not None else ('(no constant speed)' if a else '(none)'),
                         repo_speed=sb if sb is not None else ('(no constant speed)' if b else '(none)'),
                         pct=pct, ta_detail=' '.join(a['raw']) if a else '', repo_detail=' '.join(b['raw']) if b else ''))

with open(os.path.join(CMP, 'aim_diff.csv'), 'w', newline='') as fh:
    w = csv.DictWriter(fh, fieldnames=list(rows[0].keys()))
    w.writeheader(); w.writerows(rows)
with open(os.path.join(CMP, 'aim_scripts.csv'), 'w', newline='') as fh:
    w = csv.writer(fh)
    w.writerow(['repo_unit', 'ta_id', 'repo_script', 'type', 'vs_TA', 'aim_axes_in_TA'])
    w.writerows(status_rows)
from collections import Counter
print('scripts', Counter((r[3], r[4]) for r in status_rows))
print('aim diff rows', len(rows), 'units', len({r['unit'] for r in rows}))
