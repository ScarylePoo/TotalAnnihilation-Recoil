#!/usr/bin/env bash
# Regenerate the TA 3.1c vs TA:Recoil stat review from the original Cavedog archives.
#
#   tools/ta-data/run_all.sh <dir with TA archives> [out dir]
#
# <dir with TA archives> must contain (names are matched case-insensitively):
#   totala1.hpi  ccdata.ccx  btdata.ccx  rev31.gp3  and the Cavedog downloadables .ufo
#   (optional: totala4.hpi, ccmiss.ccx; the map/campaign archives carry no unit data)
# Output (default ~/ta-data-out): x/<archive>/ extracted layers, merged/, out/ (TA stats as CSV/JSON),
# cmp/ (diffs vs this repo) and TA_vs_Recoil_stat_review.xlsx.
# Needs: python3, lupa, openpyxl  (pip install --user lupa openpyxl)
set -euo pipefail
here="$(cd "$(dirname "$0")" && pwd)"
repo="$(cd "$here/../.." && pwd)"
src="${1:?usage: run_all.sh <dir with TA archives> [out dir]}"
out="${2:-$HOME/ta-data-out}"
mkdir -p "$out/x" "$out/merged"

find_one() {  # case-insensitive lookup of an archive in $src
	find -L "$src" -maxdepth 1 -type f -iname "$1" | head -1
}

# Canonical layer names, in override order (later wins). The tools key on these names.
declare -A LAYER=(
	[totala1.hpi]="totala1.hpi" [totala4.hpi]="totala4.hpi" [ccmiss.ccx]="ccmiss.ccx"
	[ccdata.ccx]="ccdata.ccx" [btdata.ccx]="btdata.ccx" [cavedog.ufo]="*.ufo" [rev31.gp3]="rev31.gp3"
)
ORDER=(totala1.hpi totala4.hpi ccmiss.ccx ccdata.ccx btdata.ccx cavedog.ufo rev31.gp3)

for name in "${ORDER[@]}"; do
	f="$(find_one "${LAYER[$name]}")"
	if [[ -z "$f" ]]; then
		echo "skip $name (not found in $src)"
		continue
	fi
	if [[ ! -d "$out/x/$name" ]]; then
		echo "extract $(basename "$f") -> x/$name"
		python3 -I "$here/hpi.py" "$f" "$out/x/$name"
	fi
	cp -r "$out/x/$name/." "$out/merged/"
done

python3 -I "$here/tadump.py" "$out/x" "$out/out"
python3 "$here/compare.py" "$repo" "$out/out" "$out/x" "$out/cmp"
python3 "$here/finalize.py" "$repo" "$out/out" "$out/merged" "$out/cmp"
python3 "$here/compare_aim.py" "$repo" "$out/out" "$out/x" "$out/cmp"
TA_REPO_REV="$(git -C "$repo" log -1 --format='%h (%ad)' --date=short 2>/dev/null || echo unknown)" python3 "$here/build_xlsx.py" "$out/cmp" "$out/TA_vs_Recoil_stat_review.xlsx"
echo "done: $out/TA_vs_Recoil_stat_review.xlsx (open in Excel/LibreOffice; formulas calculate on open)"
