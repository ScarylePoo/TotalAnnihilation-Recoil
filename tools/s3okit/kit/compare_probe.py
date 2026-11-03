#!/usr/bin/env python3
"""Diff two logs of tools/headless-test probes (KEEPLOG=... AIM=1 / SCRIPTP=1 run.sh), typically a COB run against a Lua run.

    python3 compare_probe.py aim  cob.log lua.log     shots and hits per weapon, poses at the end of the far and near phases
    python3 compare_probe.py sp   cob.log lua.log     poses per state, spinning pieces, activation/armor/resources, corpses, factories, specials

Poses: a piece differing by more than 0.15 in rotation or 1.5 elmo is listed. Spinners and things mid-animation legitimately differ."""
import re
import sys
from collections import defaultdict


def poses(path):
    out = {}
    for ln in open(path, errors='replace'):
        if not ln.startswith('[POSE] '):
            continue
        _, unit, tag, *parts = ln.split()
        d = {}
        for p in parts:
            n, v = p.split('=')
            d[n] = [float(x) for x in v.split(',')]
        out[(unit, tag)] = d
    return out


def pose_diff(a, b):
    res = []
    for n in a:
        if n not in b:
            continue
        rot = max(abs(x - y) for x, y in zip(a[n][:9], b[n][:9]))
        pos = max(abs(x - y) for x, y in zip(a[n][9:], b[n][9:]))
        if rot > 0.15 or pos > 1.5:
            res.append((n, round(rot, 2), round(pos, 1)))
    return res


def compare_poses(pa, pb, moving_ok=()):
    bad = defaultdict(list)
    n = 0
    for k in sorted(pa):
        if k not in pb:
            continue
        n += 1
        d = pose_diff(pa[k], pb[k])
        if d:
            bad[k[0]].append((k[1], d))
    print(f'poses compared: {n}, units with a difference: {len(bad)}')
    for u, rows in sorted(bad.items()):
        for tag, d in rows:
            print(f'  POSE {u} {tag}: ' + ' '.join(f'{p}(r{r},p{q})' for p, r, q in d[:8]) + (' ...' if len(d) > 8 else ''))


def spinners(p, unit):
    a, b = p.get((unit, 'move1')), p.get((unit, 'move2'))
    if not a or not b:
        return None
    return {n for n in a if n in b and max(abs(x - y) for x, y in zip(a[n][:9], b[n][:9])) > 0.02}


def aim(path):
    out = {}
    for ln in open(path, errors='replace'):
        if '[HARNESS] waim' not in ln:
            continue
        m = re.search(r'waim, (\S+), (w\d+), (\S+), (\S+), .*?shots ([\d/]+) hits ([\d/]+)(.*)$', ln)
        if m:
            sh = [int(x) for x in m.group(5).split('/')]
            hi = [int(x) for x in m.group(6).split('/')]
            out[(m.group(1), m.group(2))] = (m.group(3), m.group(4), sh, hi, m.group(7))
    return out


def main():
    mode, fa, fb = sys.argv[1:4]
    if mode == 'aim':
        a, b = aim(fa), aim(fb)
        print(f'weapons: {len(a)} / {len(b)}')
        worse = same = better = 0
        for k in sorted(set(a) | set(b)):
            if k not in a or k not in b:
                print('  ONLY IN ONE', k)
                continue
            sa, sb = sum(a[k][2]), sum(b[k][2])
            ha, hb = sum(a[k][3]), sum(b[k][3])
            tag = ''
            if (sa > 0 and sb == 0) or (ha > 0 and hb == 0) or sb < sa * 0.6 or hb < ha * 0.6:
                tag = 'WORSE'
                worse += 1
            elif (sa == 0 and sb > 0) or (ha == 0 and hb > 0) or sb > sa * 1.6 or hb > ha * 1.6:
                tag = 'better'
                better += 1
            else:
                same += 1
            if tag:
                print(f'  {tag} {k[0]} {k[1]} {a[k][0]} {a[k][1]}: shots {a[k][2]} -> {b[k][2]} hits {a[k][3]} -> {b[k][3]}')
        print(f'same {same}, better {better}, worse {worse}')
        flags = defaultdict(list)
        for k, v in b.items():
            for fl in ('NOFIRE', 'NOHIT', 'NOPITCH', 'OFFAXIS', 'NOBARREL'):
                if fl in v[4]:
                    flags[fl].append(f'{k[0]}:{k[1]}')
        for fl, us in sorted(flags.items()):
            print(f'{fl} ({len(us)}): ' + ' '.join(us))
        compare_poses(poses(fa), poses(fb))
        return
    pa, pb = poses(fa), poses(fb)
    compare_poses(pa, pb)
    units = {k[0] for k in pa}
    for u in sorted(units):
        sa, sb = spinners(pa, u), spinners(pb, u)
        if sa is not None and sb is not None and sa != sb:
            print(f'  SPIN {u}: cob-only {sorted(sa - sb)} lua-only {sorted(sb - sa)}')

    def sp(path):
        rows = {}
        for ln in open(path, errors='replace'):
            if ln.startswith('[SP]'):
                t = ln.strip()
                key = ' '.join(t.split(',')[:3])
                rows.setdefault(key, []).append(t)
        return rows
    a, b = sp(fa), sp(fb)
    for k in sorted(set(a) | set(b)):
        if a.get(k) != b.get(k):
            print(f'  DIFF\n    cob {a.get(k)}\n    lua {b.get(k)}')


if __name__ == '__main__':
    main()
