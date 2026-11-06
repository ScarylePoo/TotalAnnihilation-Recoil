#!/usr/bin/env python3
"""Runtime def dump (tools/headless-test/run.sh DUMP=<file>) -> JSON, and before/after diffs.

  defdump.py DUMP.txt OUT.json            parse
  defdump.py --diff BEFORE.txt AFTER.txt  print changed fields per def (U = unit, W = weapon)
"""
import json, sys
from collections import defaultdict


def parse(path):
    defs = {'U': defaultdict(dict), 'W': defaultdict(dict)}
    for line in open(path, encoding='latin-1'):
        parts = line.rstrip('\n').split(' ', 2)
        if len(parts) < 3 or parts[0] not in defs or '=' not in parts[2]:
            continue
        k, v = parts[2].split('=', 1)
        try:
            v = float(v)
            v = int(v) if v == int(v) else round(v, 6)
        except ValueError:
            pass
        defs[parts[0]][parts[1]][k] = v
    return {k: dict(v) for k, v in defs.items()}


def main():
    if sys.argv[1] == '--diff':
        a, b = parse(sys.argv[2]), parse(sys.argv[3])
        for kind in 'UW':
            for name in sorted(set(a[kind]) | set(b[kind])):
                da, db = a[kind].get(name, {}), b[kind].get(name, {})
                ch = [(k, da.get(k), db.get(k)) for k in sorted(set(da) | set(db)) if da.get(k) != db.get(k)]
                if ch:
                    print('%s %s: %s' % (kind, name, '; '.join('%s %s -> %s' % c for c in ch)))
        return
    json.dump(parse(sys.argv[1]), open(sys.argv[2], 'w'), indent=1, sort_keys=True)


if __name__ == '__main__':
    main()
