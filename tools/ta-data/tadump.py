#!/usr/bin/env python3
"""Parse TA FBI/TDF data from extracted archive layers into JSON + CSV.

Usage: tadump.py XDIR OUTDIR   (XDIR holds one extracted folder per archive)
"""
import csv, glob, json, os, re, sys

LAYERS = ['totala1.hpi', 'totala4.hpi', 'ccmiss.ccx', 'ccdata.ccx', 'btdata.ccx', 'cavedog.ufo', 'rev31.gp3']


def parse_tdf(text):
    text = re.sub(r'//[^\n]*', '', text)
    text = re.sub(r'/\*.*?\*/', '', text, flags=re.S)
    root = {}
    stack = [root]
    pending = None
    for tok in re.finditer(r'\[([^\]]*)\]|\{|\}|([^=;{}\[\]\n]+?)\s*=\s*([^;\n]*);?', text):
        if tok.group(1) is not None:
            pending = tok.group(1).strip().lower()
        elif tok.group(0) == '{':
            d = {}
            stack[-1][pending or ''] = d
            stack.append(d)
            pending = None
        elif tok.group(0) == '}':
            if len(stack) > 1:
                stack.pop()
        else:
            stack[-1][tok.group(2).strip().lower()] = tok.group(3).strip()
    return root


def read(p):
    with open(p, 'rb') as f:
        return f.read().decode('latin-1')


def num(v):
    try:
        f = float(v)
        return int(f) if f == int(f) else f
    except (TypeError, ValueError):
        return v


def collect(xdir, sub, ext, pattern=None):
    """Return {name: {'data':..., 'source': layer, 'history': {layer: data}}}."""
    out = {}
    for layer in LAYERS:
        for p in glob.glob(os.path.join(xdir, layer, sub, pattern or '*.' + ext)):
            try:
                parsed = parse_tdf(read(p))
            except Exception as e:
                print('parse fail', p, e, file=sys.stderr)
                continue
            for sec, d in parsed.items():
                if not isinstance(d, dict):
                    continue
                key = (d.get('unitname') or sec).lower() if ext == 'fbi' else sec
                rec = out.setdefault(key, {'history': {}})
                rec['history'][layer] = d
                rec['data'] = d
                rec['source'] = layer
                rec['file'] = os.path.relpath(p, os.path.join(xdir, layer))
    return out


UNIT_COLS = ['unitname', 'side', 'name', 'description', 'source', 'buildcostmetal', 'buildcostenergy',
             'buildtime', 'workertime', 'maxdamage', 'maxvelocity', 'acceleration', 'brakerate',
             'turnrate', 'sightdistance', 'radardistance', 'sonardistance', 'radardistancejam',
             'energymake', 'metalmake', 'energyuse', 'makesmetal', 'extractsmetal', 'windgenerator',
             'tidalgenerator', 'energystorage', 'metalstorage', 'cloakcost', 'cloakcostmoving',
             'builddistance', 'canfly', 'cruisealt', 'movementclass', 'footprintx', 'footprintz',
             'maxwaterdepth', 'minwaterdepth', 'maxslope', 'damagemodifier', 'weapon1', 'weapon2',
             'weapon3', 'explodeas', 'selfdestructas', 'corpse', 'category', 'tedclass', 'changed_by']

WEAP_COLS = ['id', 'name', 'source', 'range', 'reloadtime', 'damage_default', 'areaofeffect',
             'weaponvelocity', 'startvelocity', 'weaponacceleration', 'energypershot',
             'metalpershot', 'accuracy', 'tolerance', 'burst', 'burstrate', 'sprayangle',
             'edgeeffectiveness', 'turnrate', 'flighttime', 'model', 'beamweapon', 'lineofsight',
             'ballistic', 'dropped', 'vlaunched', 'selfprop', 'tracks', 'guidance', 'commandfire',
             'stockpile', 'paralyzer', 'noautorange', 'toairweapon', 'changed_by']


def diff_layers(hist):
    """Which later layers changed values versus the earliest version."""
    layers = [l for l in LAYERS if l in hist]
    changes = []
    for a, b in zip(layers, layers[1:]):
        da, db = hist[a], hist[b]
        keys = {k for k in set(da) | set(db) if not isinstance(da.get(k, ''), dict)}
        n = sum(1 for k in keys if str(da.get(k, '')).lower() != str(db.get(k, '')).lower())
        if n:
            changes.append('%s(%d)' % (b.split('.')[0], n))
    return ' '.join(changes)


def main():
    xdir, outdir = sys.argv[1], sys.argv[2]
    os.makedirs(outdir, exist_ok=True)
    units = collect(xdir, 'units', 'fbi')
    weaps = collect(xdir, 'gamedata', 'tdf', 'weapons.tdf')
    weaps.update(collect(xdir, 'weapons', 'tdf'))

    with open(os.path.join(outdir, 'units.json'), 'w') as f:
        json.dump({k: {'source': v['source'], 'file': v['file'],
                       'stats': {kk: num(vv) for kk, vv in v['data'].items()},
                       'history': v['history']} for k, v in sorted(units.items())}, f, indent=1)
    with open(os.path.join(outdir, 'weapons.json'), 'w') as f:
        json.dump({k: {'source': v['source'], 'file': v['file'], 'stats': v['data'],
                       'history': v['history']} for k, v in sorted(weaps.items())}, f, indent=1)

    with open(os.path.join(outdir, 'units.csv'), 'w', newline='') as f:
        w = csv.writer(f)
        w.writerow(UNIT_COLS)
        for k, v in sorted(units.items()):
            d = v['data']
            row = []
            for c in UNIT_COLS:
                if c == 'source':
                    row.append(v['source'].split('.')[0])
                elif c == 'changed_by':
                    row.append(diff_layers(v['history']))
                else:
                    row.append(num(d.get(c, '')))
            w.writerow(row)

    with open(os.path.join(outdir, 'weapons.csv'), 'w', newline='') as f:
        w = csv.writer(f)
        w.writerow(WEAP_COLS)
        for k, v in sorted(weaps.items()):
            d = v['data']
            row = []
            for c in WEAP_COLS:
                if c == 'id':
                    row.append(k)
                elif c == 'source':
                    row.append(v['source'].split('.')[0])
                elif c == 'changed_by':
                    row.append(diff_layers(v['history']))
                elif c == 'damage_default':
                    dmg = d.get('damage', {})
                    row.append(num(dmg.get('default', '')) if isinstance(dmg, dict) else '')
                else:
                    row.append(num(d.get(c, '')))
            w.writerow(row)

    # Per-target damage overrides as a separate long table.
    with open(os.path.join(outdir, 'weapon_damage.csv'), 'w', newline='') as f:
        w = csv.writer(f)
        w.writerow(['weapon', 'target', 'damage'])
        for k, v in sorted(weaps.items()):
            dmg = v['data'].get('damage', {})
            if isinstance(dmg, dict):
                for t, val in dmg.items():
                    w.writerow([k, t, num(val)])

    print('units', len(units), 'weapons', len(weaps))
    from collections import Counter
    print('unit sources', Counter(v['source'] for v in units.values()))
    print('weapon sources', Counter(v['source'] for v in weaps.values()))


if __name__ == '__main__':
    main()
