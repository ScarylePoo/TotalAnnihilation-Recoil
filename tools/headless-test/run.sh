#!/bin/bash
# Headless smoke test for TA:Recoil on a given Recoil engine build.
#
#   tools/headless-test/run.sh /path/to/recoil-engine-dir [timeout_s]
#   AIM=1 tools/headless-test/run.sh ...      instead runs only zz_walker_aim_probe (fire, hits and gun pitch of every armed unit)
#   SCRIPTP=1 tools/headless-test/run.sh ...  instead runs only zz_script_probe (poses, on/off, build, corpses, transports, pads, stockpile)
#   PADS=1 tools/headless-test/run.sh ...     instead runs only zz_pad_probe (air repair pads: luarules/gadgets/unit_air_pads.lua)
#   KEEPLOG=path saves the cleaned infolog there (for tools/s3okit/kit/compare_probe.py)
#   WATER=1 tools/headless-test/run.sh ...    instead runs only zz_water_probe (hover and ship transports at a shore, seaplane torpedoes, ship anti-air)
#   GAP=1 tools/headless-test/run.sh ...      instead runs only zz_piece_gap_probe (piece matrices of every unit def in action); it prints the path of
#                                             gapdata.txt, which tools/s3okit/kit/piece_gaps.py turns into a report of pieces floating off the unit
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
# several runs at once (other worktrees too) need their own UDP port
sed -i "s/IsHost=1;/IsHost=1;\n\tHostPort=$((20000 + RANDOM % 30000));/" "$WD/script.txt"
[ -n "$AIM" ] && sed -i 's/debugmode=1;/debugmode=1;\n\t\taimonly=1;/' "$WD/script.txt"
[ -n "$SCRIPTP" ] && sed -i 's/debugmode=1;/debugmode=1;\n\t\taimonly=1;\n\t\tscriptonly=1;/' "$WD/script.txt"
[ -n "$WATER" ] && sed -i 's/debugmode=1;/debugmode=1;\n\t\taimonly=1;\n\t\twaterprobe=1;/' "$WD/script.txt"
[ -n "$GAP" ] && sed -i 's/debugmode=1;/debugmode=1;\n\t\tgaponly=1;/' "$WD/script.txt"
[ -n "$PADS" ] && sed -i 's/debugmode=1;/debugmode=1;\n\t\taimonly=1;\n\t\tpadonly=1;/' "$WD/script.txt" && sed -i 's/\[ALLYTEAM0\]/[TEAM2] { TeamLeader=0; AllyTeam=1; Side=ARM; StartPosX=300; StartPosZ=11800; }\n\t[TEAM3] { TeamLeader=0; AllyTeam=2; Side=ARM; StartPosX=1000; StartPosZ=11800; }\n\t[TEAM4] { TeamLeader=0; AllyTeam=3; Side=ARM; StartPosX=2000; StartPosZ=11800; }\n\t[TEAM5] { TeamLeader=0; AllyTeam=4; Side=ARM; StartPosX=3000; StartPosZ=11800; }\n\t[ALLYTEAM2] { NumAllies=0; }\n\t[ALLYTEAM3] { NumAllies=0; }\n\t[ALLYTEAM4] { NumAllies=0; }\n\t&/' "$WD/script.txt"
set +e
timeout "${2:-1800}" "$ENGINE/spring-headless" --isolation --isolation-dir "$ENGINE" --write-dir "$WD" "$WD/script.txt" > "$WD/stdout.log" 2>&1
echo "engine exit: $?   (infolog: $WD/infolog.txt)"
sed 's/^\[t=[^]]*\]\(\[f=[^]]*\]\)\? //' "$WD/infolog.txt" > "$WD/clean.log"
[ -n "$GAP" ] && grep -v "GAPD " "$WD/clean.log" > "$WD/clean2.log" && mv "$WD/clean2.log" "$WD/clean.log"
[ -n "$KEEPLOG" ] && cp "$WD/clean.log" "$KEEPLOG"
grep "\[HARNESS\]\|^\[SP\]" "$WD/clean.log" | grep -v ", spawn, "
echo "--- spawn failures: $(grep -c 'SPAWN FAIL' "$WD/clean.log")"
grep "\[PROBE\]" "$WD/clean.log" | cut -c1-300
if [ -n "$GAP" ]; then
  sed -n 's/^.*GAPD //p' "$WD/infolog.txt" > "$WD/gapdata.txt"
  echo "--- gap data: $WD/gapdata.txt ($(du -h "$WD/gapdata.txt" | cut -f1))"
fi
echo "--- problems (grouped):"
grep -i "error\|warn\|fail\|deprecat\|unknown\|invalid\|missing\|not found\|couldn\|bad \|nil value" "$WD/clean.log" \
  | grep -v "UDPListener\|GPU memory\|LuaIntro\] Loading" | sed -E 's/[0-9]+/N/g' | sort | uniq -c | sort -rn
