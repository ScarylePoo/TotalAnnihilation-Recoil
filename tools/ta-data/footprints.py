# Model bounding box vs engine footprint for mobile units: footprints.py DUMP.json [SF_fpdump.txt]
# (DUMP= tools/headless-test/run.sh -> tools/ta-data/defdump.py -> JSON; the SF dump is a "FPDUMP name|xsize|zsize|speed|canFly|isBuilding|minx|maxx|minz|maxz" list)
import sys, json, statistics
# records: name, xsize, zsize (heightmap squares, 8 elmos), speed, canfly, isbuilding, minx, maxx, minz, maxz
def load_tar(p):
    d = json.load(open(p))['U']; out = []
    for n, u in d.items():
        try:
            out.append((n, int(u['xsize']), int(u['zsize']), float(u['speed']), str(u['canFly']).lower()=='true', str(u['isBuilding']).lower()=='true',
                        float(u['model.minx']), float(u['model.maxx']), float(u['model.minz']), float(u['model.maxz'])))
        except Exception as e: pass
    return out
def load_sf(p):
    out = []
    for ln in open(p):
        f = ln.rstrip('\n').split('|')
        if len(f) < 10 or f[0]=='done': continue
        try: out.append((f[0], int(f[1]), int(f[2]), float(f[3]), f[4]=='true', f[5]=='true', float(f[6]), float(f[7]), float(f[8]), float(f[9])))
        except: pass
    return out
def report(rows, label):
    rows = [r for r in rows if r[3] > 0 and not r[4] and not r[5]]
    res = []
    for n, xs, zs, sp, fly, bld, minx, maxx, minz, maxz in rows:
        w, l = maxx-minx, maxz-minz
        fw, fl = xs*8, zs*8
        if fw <= 0 or w <= 0: continue
        res.append((n, xs//2, zs//2, w, l, w/fw, l/fl))
    rw = [r[5] for r in res]; rl = [r[6] for r in res]; mx = [max(r[5], r[6]) for r in res]
    print(f"== {label}: {len(res)} mobile ground/sea units")
    print(f"   model width  / footprint width : median {statistics.median(rw):.2f}   model length / footprint length: median {statistics.median(rl):.2f}")
    print(f"   larger axis ratio: median {statistics.median(mx):.2f}; model pokes out of footprint (>1.0): {sum(1 for v in mx if v>1)}; footprint >= 1.25x model (<=0.8): {sum(1 for v in mx if v<=0.8)}")
    hist = {}
    for v in mx:
        b = min(round(v*4)/4, 3.0); hist[b] = hist.get(b,0)+1
    print("   histogram of larger-axis ratio:", '  '.join(f"{k:.2f}:{v}" for k,v in sorted(hist.items())))
    fp = {}
    for r in res: fp[(r[1],r[2])] = fp.get((r[1],r[2]),0)+1
    print("   footprints used:", '  '.join(f"{a}x{b}:{c}" for (a,b),c in sorted(fp.items())))
    res.sort(key=lambda r: -max(r[5], r[6]))
    print("   most oversized models / typical / most undersized (name fp modelW modelL ratioW ratioL):")
    for r in res[:6] + res[len(res)//2-2:len(res)//2+2] + res[-4:]:
        print(f"     {r[0]:<30} {r[1]}x{r[2]}  {r[3]:6.1f} {r[4]:6.1f}   {r[5]:.2f} {r[6]:.2f}")
    return res
if __name__ == '__main__':
    report(load_tar(sys.argv[1]), 'TA:Recoil')
    if len(sys.argv) > 2: report(load_sf(sys.argv[2]), 'Splinter Faction')
