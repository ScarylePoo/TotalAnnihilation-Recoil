#!/bin/bash
# Headless smoke test for TA:Recoil on a given Recoil engine build.
#
#   tools/headless-test/run.sh /path/to/recoil-engine-dir [timeout_s]
#
# Loads the game on a generated blank map (the engine's InitBlank map
# generator, no map download), spawns every unitdef for two enemy teams, lets
# them build and fight, self-destructs everything, clears the wrecks, quits.
# Prints every error/warning from the infolog, grouped.
#
# Known lines on headless that are not game problems:
#   "Could not finalize groundFX texture atlas"   headless has no GPU texture limit
#   "[RmlUi] Could not load texture"               headless has no GL
#   "atmosphere.skyDir ... deprecated"             from the generated blank map
#   "Vote failed: ... white flag"                  team 1 has no player, so game_end offers a surrender vote
#   "cannot open LuaUI/Config/TART.lua"            first run in a fresh write dir
set -e
ENGINE=${1:?engine directory (the one containing spring-headless)}
HERE=$(cd "$(dirname "$0")" && pwd)
GAME=$(cd "$HERE/../.." && pwd)
WD=$(mktemp -d)
mkdir -p "$WD/games"
ln -s "$GAME" "$WD/games/tar.sdd"
ln -s "$HERE/tartest.sdd" "$WD/games/tartest.sdd"
cp "$HERE/script.txt" "$WD/script.txt"
set +e
timeout "${2:-1800}" "$ENGINE/spring-headless" --isolation --isolation-dir "$ENGINE" --write-dir "$WD" "$WD/script.txt" > "$WD/stdout.log" 2>&1
echo "engine exit: $?   (infolog: $WD/infolog.txt)"
sed 's/^\[t=[^]]*\]\(\[f=[^]]*\]\)\? //' "$WD/infolog.txt" > "$WD/clean.log"
grep "\[HARNESS\]" "$WD/clean.log" | grep -v ", spawn, "
echo "--- spawn failures: $(grep -c 'SPAWN FAIL' "$WD/clean.log")"
grep "\[PROBE\]" "$WD/clean.log" | cut -c1-300
echo "--- problems (grouped):"
grep -i "error\|warn\|fail\|deprecat\|unknown\|invalid\|missing\|not found\|couldn\|bad \|nil value" "$WD/clean.log" \
  | grep -v "UDPListener\|GPU memory\|LuaIntro\] Loading" | sed -E 's/[0-9]+/N/g' | sort | uniq -c | sort -rn
