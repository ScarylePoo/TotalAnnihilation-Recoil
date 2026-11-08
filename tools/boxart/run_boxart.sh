#!/bin/bash
# Box-art style renders of a commander with the WINDOWS Recoil engine (see tools/headless-test/run_win_visual.sh for
# the setup), staged by tartest.sdd/luarules/gadgets/zz_boxart_probe.lua.
#
#   SIDE=arm|core MAP=/path/map.sd7 MAPNAME="Name Version" [W=3840 H=2160 PAUSE=4 CAMS="name:dist:height:side:look/..."
#   BUILD=<unit> BANGLE=-45 PROGRESS=0.5 (build instead of the D-Gun)  FOV=40 AIMCAM=<preset> AIMDEG=12 AIMX=-0.2 TEAMCOLOR="r g b" BOXX= BOXZ= OUT=dir CFG=<extra config lines>] tools/boxart/run_boxart.sh
# Screenshots land in OUT (default "$WINROOT/run/boxart"), one per camera preset.
set -e
HERE=$(cd "$(dirname "$0")" && pwd)
GAME=$(cd "$HERE/../.." && pwd)
TEST="$GAME/tools/headless-test"
WINROOT=${WINROOT:-"/mnt/i/Claude Space/recoil-win"}
ENGINE="$WINROOT/engine-2026.09.01"
RUN="$WINROOT/run"
mkdir -p "$RUN/games"
rsync -a --delete --exclude=.git --exclude=tools "$GAME/" "$RUN/games/tar.sdd/"
rsync -aL --delete "$TEST/tartest.sdd/" "$RUN/games/tartest.sdd/"
rm -rf "$RUN/screenshots" "$RUN/infolog.txt"
cp "$TEST/script.txt" "$RUN/script.txt"
sed -i "s|debugmode=1;|debugmode=1;\n\t\taimonly=1;\n\t\tboxart=${SIDE:-arm};\n\t\tboxpause=${PAUSE:-4};\n\t\tboxcams=${CAMS:-};\n\t\tboxfov=${FOV:-};\n\t\tboxx=${BOXX:-};\n\t\tboxaimx=${AIMX:-};\n\t\tboxaimcam=${AIMCAM:-};\n\t\tboxaimdeg=${AIMDEG:-};\n\t\tboxoff=${OFF:-};\n\t\tboxbuild=${BUILD:-};\n\t\tboxbangle=${BANGLE:-};\n\t\tboxprogress=${PROGRESS:-};\n\t\tboxsunoff=${SUNOFF:-};\n\t\tboxlight=${LIGHT:-};\n\t\tboxz=${BOXZ:-};|" "$RUN/script.txt"
# empty options would read as set: drop them
sed -i '/box[a-z]*=;/d' "$RUN/script.txt"
# team colour: TA's Arm blue / Core red unless TEAMCOLOR="r g b"
case "${SIDE:-arm}" in core) TC=${TEAMCOLOR:-"0.85 0.08 0.05"} ;; *) TC=${TEAMCOLOR:-"0.05 0.25 1.0"} ;; esac
sed -i "0,/AllyTeam=0;/s//AllyTeam=0;\n\t\tRGBColor=$TC;/" "$RUN/script.txt"
rm -rf "$RUN/maps"
if [ -n "$MAP" ]; then
  mkdir -p "$RUN/maps" && cp "$MAP" "$RUN/maps/"
  sed -i "/InitBlank=1;/d; s/MapName=blank_test;/MapName=${MAPNAME:?set MAPNAME to the name and version in the map mapinfo.lua};/" "$RUN/script.txt"
fi
printf 'XResolutionWindowed = %s\nYResolutionWindowed = %s\nFullscreen = 0\nsnd_volmaster = 0\nMaxSounds = 0\n%s' "${W:-1600}" "${H:-900}" "${CFG:-}" > "$RUN/vis.cfg"
set +e
timeout "${TIMEOUT:-300}" "$ENGINE/spring.exe" --window --config "$(wslpath -w "$RUN/vis.cfg")" --isolation \
  --isolation-dir "$(wslpath -w "$ENGINE")" --write-dir "$(wslpath -w "$RUN")" "$(wslpath -w "$RUN/script.txt")" > /dev/null 2>&1
echo "engine exit: $?   (infolog: $RUN/infolog.txt)"
OUT=${OUT:-$RUN/boxart}
mkdir -p "$OUT" && cp "$RUN"/screenshots/* "$OUT/" 2>/dev/null
echo "--- screenshots: $OUT ($(ls "$RUN/screenshots" 2>/dev/null | wc -l) new)"
grep -a "\[BOXART\]\|Error" "$RUN/infolog.txt" | grep -v "RmlUi\|TART.lua\|beep1" | cut -c1-400 | head -30
