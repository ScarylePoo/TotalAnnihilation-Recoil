#!/bin/bash
# Weapon/effect screenshots with the WINDOWS Recoil engine, run from WSL (native GPU drivers; the WSL D3D12 bridge
# blends particles wrongly, so colours of effects can only be judged this way).
#
#   VISUAL=unit1,unit2 | VISUALCEG=ceg1,ceg2  [VISUALZOOM= VISUALDIST= VISUALOUT=dir] tools/headless-test/run_win_visual.sh
#
# WINROOT (default "/mnt/i/Claude Space/recoil-win") holds engine-2026.09.01/ (the release's amd64-windows.7z unpacked)
# and run/ (write dir; the game is rsynced to run/games/tar.sdd, the probe mod to run/games/tartest.sdd).
set -e
HERE=$(cd "$(dirname "$0")" && pwd)
GAME=$(cd "$HERE/../.." && pwd)
WINROOT=${WINROOT:-"/mnt/i/Claude Space/recoil-win"}
ENGINE="$WINROOT/engine-2026.09.01"
RUN="$WINROOT/run"
mkdir -p "$RUN/games"
rsync -a --delete --exclude=.git --exclude=tools "$GAME/" "$RUN/games/tar.sdd/"
rsync -a --delete "$HERE/tartest.sdd/" "$RUN/games/tartest.sdd/"
rm -rf "$RUN/screenshots" "$RUN/infolog.txt"
cp "$HERE/script.txt" "$RUN/script.txt"
[ -n "$VISUALCEG" ] && VISUAL=${VISUAL:-none}
sed -i "s|debugmode=1;|debugmode=1;\n\t\taimonly=1;\n\t\tvisualceg=$VISUALCEG;\n\t\tvisualunits=$VISUAL;\n\t\tvisualzoom=${VISUALZOOM:-700};\n\t\tvisualdist=${VISUALDIST:-420};\n\t\tvisualkill=${VISUALKILL:-};\n\t\tvisualhold=${VISUALHOLD:-};\n\t\tvisualspacing=${VISUALSPACING:-};\n\t\tvisualtex=${VISUALTEX:-};\n\t\tvisualselect=${VISUALSELECT:-};\n\t\tvisualhurt=${VISUALHURT:-};|" "$RUN/script.txt"
printf 'XResolutionWindowed = %s\nYResolutionWindowed = %s\nFullscreen = 0\nsnd_volmaster = 0\nMaxSounds = 0\n%s' "${VISUALW:-1600}" "${VISUALH:-900}" "${VISUALCFG:-}" > "$RUN/vis.cfg"
set +e
timeout "${1:-600}" "$ENGINE/spring.exe" --window --config "$(wslpath -w "$RUN/vis.cfg")" --isolation \
  --isolation-dir "$(wslpath -w "$ENGINE")" --write-dir "$(wslpath -w "$RUN")" "$(wslpath -w "$RUN/script.txt")" > /dev/null 2>&1
echo "engine exit: $?   (infolog: $RUN/infolog.txt)"
OUT=${VISUALOUT:-$RUN/shots}
mkdir -p "$OUT" && cp "$RUN"/screenshots/* "$OUT/" 2>/dev/null
echo "--- screenshots: $OUT ($(ls "$OUT" | wc -l))"
grep -a "\[VISUAL\] draw\|GL renderer\|Error\|error" "$RUN/infolog.txt" | grep -v "RmlUi\|TART.lua" | head -15
