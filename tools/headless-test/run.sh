#!/bin/bash
# Headless smoke test for TA:Recoil on a given Recoil engine build.
#
#   tools/headless-test/run.sh /path/to/recoil-engine-dir [timeout_s]
#   AIM=1 tools/headless-test/run.sh ...      instead runs only zz_walker_aim_probe (fire, hits and gun pitch of every armed unit)
#   SCRIPTP=1 tools/headless-test/run.sh ...  instead runs only zz_script_probe (poses, on/off, build, corpses, transports, pads, stockpile)
#   PADS=1 tools/headless-test/run.sh ...     instead runs only zz_pad_probe (air repair pads: luarules/gadgets/unit_air_pads.lua)
#   STARTP=duel|teams|ffa|boxes|lobby|lobbybox tools/headless-test/run.sh ...  instead runs only zz_start_probe: the pregame flow of
#                                             game_spawn.lua (faction choice, placement, spawn) with simulated players, see the probe
#   MAP=/path/map.sd7 MAPNAME="Map Name" ...  plays on that map instead of the generated blank one (e.g. one with start positions)
#   KEEPLOG=path saves the cleaned infolog there (for tools/s3okit/kit/compare_probe.py)
#   WATER=1 tools/headless-test/run.sh ...    instead runs only zz_water_probe (hover and ship transports at a shore, seaplane torpedoes, ship anti-air)
#   TORP=<depth> tools/headless-test/run.sh ... instead runs only zz_torpedo_probe (every torpedo weapon in water that deep; TORPKIND=ship,sub,moving,shore,land,air picks targets)
#   VISUAL=unit1,unit2 [VISUALZOOM=700 VISUALDIST=420 VISUALOUT=dir] tools/headless-test/run.sh ...  GRAPHICAL engine: lines the units up firing
#                                             at the ground and saves screenshots (weapon visuals check, zz_visual_probe)
#   VISUALCEG=ceg1,ceg2 [VISUALZOOM=...] tools/headless-test/run.sh ...  GRAPHICAL engine: those CEGs in a row on the ground, repeated
#   DUMP=<file> tools/headless-test/run.sh ... instead runs only zz_def_dump: every runtime UnitDef/WeaponDef to <file> (tools/ta-data/defdump.py -> JSON)
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
[ -n "$TORP" ] && sed -i "s/debugmode=1;/debugmode=1;\n\t\taimonly=1;\n\t\ttorpprobe=$TORP;\n\t\ttorpkind=${TORPKIND:-ship,sub,moving,shore};/; s/blank_map_x=24/blank_map_x=32/; s/blank_map_y=24/blank_map_y=32/" "$WD/script.txt"
[ -n "$GAP" ] && sed -i 's/debugmode=1;/debugmode=1;\n\t\tgaponly=1;/' "$WD/script.txt"
[ -n "$FLIGHT" ] && sed -i "s/debugmode=1;/debugmode=1;\n\t\taimonly=1;\n\t\tflightprobe=$FLIGHT;/" "$WD/script.txt"
[ -n "$DUMP" ] && sed -i 's/debugmode=1;/debugmode=1;\n\t\taimonly=1;\n\t\tdumponly=1;/' "$WD/script.txt"
[ -n "$VISUALCEG" ] && VISUAL=${VISUAL:-none}
[ -n "$VISUAL" ] && sed -i "s|debugmode=1;|debugmode=1;\n\t\taimonly=1;\n\t\tvisualceg=$VISUALCEG;\n\t\tvisualunits=$VISUAL;\n\t\tvisualzoom=${VISUALZOOM:-700};\n\t\tvisualdist=${VISUALDIST:-420};\n\t\tvisualkill=${VISUALKILL:-};\n\t\tvisualhold=${VISUALHOLD:-};\n\t\tvisualspacing=${VISUALSPACING:-};\n\t\tvisualtex=${VISUALTEX:-};|" "$WD/script.txt"
[ -n "$PADS" ] && sed -i 's/debugmode=1;/debugmode=1;\n\t\taimonly=1;\n\t\tpadonly=1;/' "$WD/script.txt" && sed -i 's/\[ALLYTEAM0\]/[TEAM2] { TeamLeader=0; AllyTeam=1; Side=ARM; StartPosX=300; StartPosZ=11800; }\n\t[TEAM3] { TeamLeader=0; AllyTeam=2; Side=ARM; StartPosX=1000; StartPosZ=11800; }\n\t[TEAM4] { TeamLeader=0; AllyTeam=3; Side=ARM; StartPosX=2000; StartPosZ=11800; }\n\t[TEAM5] { TeamLeader=0; AllyTeam=4; Side=ARM; StartPosX=3000; StartPosZ=11800; }\n\t[ALLYTEAM2] { NumAllies=0; }\n\t[ALLYTEAM3] { NumAllies=0; }\n\t[ALLYTEAM4] { NumAllies=0; }\n\t&/' "$WD/script.txt"
if [ -n "$STARTP" ]; then
  sed -i '/skippregame=1;/d' "$WD/script.txt"
  sed -i "s/debugmode=1;/debugmode=1;\n\t\taimonly=1;\n\t\tstartprobe=$STARTP;/" "$WD/script.txt"
  case "$STARTP" in
    teams) sed -i 's/\[ALLYTEAM0\]/[TEAM2] { TeamLeader=0; AllyTeam=0; Side=CORE; StartPosX=1000; StartPosZ=5000; }\n\t[TEAM3] { TeamLeader=0; AllyTeam=1; Side=ARM; StartPosX=5000; StartPosZ=1000; }\n\t&/' "$WD/script.txt" ;;
    ffa)   sed -i 's/\[ALLYTEAM0\]/[TEAM2] { TeamLeader=0; AllyTeam=2; Side=ARM; StartPosX=1000; StartPosZ=5000; }\n\t[TEAM3] { TeamLeader=0; AllyTeam=3; Side=CORE; StartPosX=5000; StartPosZ=1000; }\n\t[ALLYTEAM2] { NumAllies=0; }\n\t[ALLYTEAM3] { NumAllies=0; }\n\t&/' "$WD/script.txt" ;;
    boxes) sed -i 's/StartPosType=0;/StartPosType=2;/; s/\[ALLYTEAM0\] { NumAllies=0; }/[ALLYTEAM0] { NumAllies=0; StartRectLeft=0; StartRectTop=0; StartRectRight=0.3; StartRectBottom=1; }/; s/\[ALLYTEAM1\] { NumAllies=0; }/[ALLYTEAM1] { NumAllies=0; StartRectLeft=0.7; StartRectTop=0; StartRectRight=1; StartRectBottom=1; }/' "$WD/script.txt" ;;
    lobby) sed -i 's/StartPosType=0;/StartPosType=3;/' "$WD/script.txt" ;;
    lobbybox) sed -i 's/StartPosType=0;/StartPosType=3;/; s/\[ALLYTEAM0\] { NumAllies=0; }/[ALLYTEAM0] { NumAllies=0; StartRectLeft=0; StartRectTop=0; StartRectRight=0.3; StartRectBottom=1; }/; s/\[ALLYTEAM1\] { NumAllies=0; }/[ALLYTEAM1] { NumAllies=0; StartRectLeft=0.7; StartRectTop=0; StartRectRight=1; StartRectBottom=1; }/' "$WD/script.txt" ;;
  esac
fi
if [ -n "$MAP" ]; then
  mkdir -p "$WD/maps"
  ln -s "$MAP" "$WD/maps/$(basename "$MAP")"
  sed -i "/InitBlank=1;/d; s/MapName=blank_test;/MapName=${MAPNAME:?set MAPNAME to the name in the map mapinfo.lua};/" "$WD/script.txt"
fi
set +e
if [ -n "$VISUAL" ] && [ -z "$VISUALHEADLESS" ]; then
  # graphical engine; libraries it needs but the system lacks can live in $ENGINE/../libs (see tools/ta-data/HANDOFF.md)
  LIBS="$ENGINE/../libs/root/usr/lib/x86_64-linux-gnu"
  export LD_LIBRARY_PATH="$LIBS:$LIBS/sdl2-classic:$LIBS/pulseaudio${LD_LIBRARY_PATH:+:$LD_LIBRARY_PATH}"
  # WSL2: render on the GPU through Mesa's D3D12 driver; the llvmpipe software fallback skips projectile sprites
  [ -e /dev/dxg ] && export GALLIUM_DRIVER="${GALLIUM_DRIVER:-d3d12}" LD_LIBRARY_PATH="/usr/lib/wsl/lib:$LD_LIBRARY_PATH"
  printf 'XResolutionWindowed = %s\nYResolutionWindowed = %s\nFullscreen = 0\nsnd_volmaster = 0\nMaxSounds = 0\n' "${VISUALW:-1600}" "${VISUALH:-900}" > "$WD/vis.cfg"
  timeout "${2:-600}" "$ENGINE/spring" --window --config "$WD/vis.cfg" --isolation --isolation-dir "$ENGINE" --write-dir "$WD" "$WD/script.txt" > "$WD/stdout.log" 2>&1
else
  timeout "${2:-1800}" "$ENGINE/spring-headless" --isolation --isolation-dir "$ENGINE" --write-dir "$WD" "$WD/script.txt" > "$WD/stdout.log" 2>&1
fi
echo "engine exit: $?   (infolog: $WD/infolog.txt)"
sed 's/^\[t=[^]]*\]\(\[f=[^]]*\]\)\? //' "$WD/infolog.txt" > "$WD/clean.log"
[ -n "$GAP" ] && grep -v "GAPD " "$WD/clean.log" > "$WD/clean2.log" && mv "$WD/clean2.log" "$WD/clean.log"
[ -n "$DUMP" ] && sed -n 's/^.*DEFDUMP //p' "$WD/clean.log" > "$DUMP" && echo "--- def dump: $DUMP ($(wc -l < "$DUMP") lines)" && grep -v "DEFDUMP " "$WD/clean.log" > "$WD/clean2.log" && mv "$WD/clean2.log" "$WD/clean.log"
[ -n "$KEEPLOG" ] && cp "$WD/clean.log" "$KEEPLOG"
[ -n "$VISUAL" ] && mkdir -p "${VISUALOUT:-$WD/shots}" && cp "$WD"/screenshots/* "${VISUALOUT:-$WD/shots}/" 2>/dev/null; [ -n "$VISUAL" ] && echo "--- screenshots: ${VISUALOUT:-$WD/shots}" && grep "\[VISUAL\]" "$WD/clean.log"
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
