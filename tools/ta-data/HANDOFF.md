# HANDOFF: translating original TA 3.1c unit, weapon and economy values into TA:Recoil

Read this whole file before doing anything. It was written by Claude (cloud session, 2026-10-31 .. 11-06) for the
next Claude session (Claude Code in WSL2 on the user's Windows PC). The user is Scary le Poo (GitHub ScarylePoo),
an experienced developer: be direct, no hand-holding.

## Status (2026-11-06, branch `ta-values`)

The conversion is done: TA 3.1c values are in the defs, scripts and gamedata. Read DEVIATIONS.md (what differs from
TA and why) and BALANCE_NOTES.md (suggestions, none applied) first. New tools since the first handoff:
`apply.py` (writes TA values into the Lua, text edits with `-- TA 3.1c (was X)` comments), `split_weapons.py` (undoes
BOTA's weapon merges), `armor.py` (TA per-unit damage -> armor classes, writes gamedata/ArmorDefs.lua), `defdump.py`
(runtime def dumps from `DUMP=<file> tools/headless-test/run.sh`, `--diff` before/after). Rerun order after a data
change: run_all.sh, then split_weapons.py, compare.py + finalize.py, apply.py, armor.py.
Def post-processing is laid out like Splinter Faction's: every unit/weapon tweak lives in `gamedata/alldefs_post.lua`
(`UnitDef_Post`, `WeaponDef_Post`); `unitdefs_post.lua`/`weapondefs_post.lua` only run the engine's base pass and call
those. Cannons carry SF's trail (`plasmacannontrail` CEG + 20-stage fading tail). All effects are Splinter Faction's now:
see the Effects section of DEVIATIONS.md (impacts, death explosions, damage smoke, nano, the atlas-size fix).
The graphical check: `VISUAL=unit1,unit2 [VISUALZOOM= VISUALDIST= VISUALOUT=] tools/headless-test/run.sh <engine>`
(screenshots of the units firing at the ground). On this WSL machine the graphical engine needs SDL2/SDL3/OpenAL
and audio libs that are not installed system-wide: they are unpacked (apt-get download + dpkg-deb -x, no root) into
~/engine/libs/root, and run.sh adds them plus Mesa's D3D12 GPU driver (GALLIUM_DRIVER=d3d12) itself. The software
renderer (llvmpipe) does not draw projectile sprites, so always render on the GPU.

## The job

The user's goal, in his words: "pull stats and unit characteristics from the original game, and translate those as
close as possible to this game. Including economy, like how much things cost, etc etc."

Done so far (all reproducible with the tools in this folder):
1. Extracted the Cavedog archives and layered them into the final TA 3.1c values (units, weapons, features).
2. Matched every one of the repo's 266 units to its TA unit (all 266 matched, one-to-one, verified).
3. Diffed every gameplay stat, every weapon, and every turret aim speed against the repo, and classified each
   difference (real balance change vs. the same thing written the Recoil way).
4. Built a review workbook, `TA_vs_Recoil_stat_review.xlsx`, with a Decision dropdown per row (Revert to TA /
   Keep repo / Custom value / Not applicable). The user has it (sent in the cloud chat); regenerate it with
   `run_all.sh` if needed.

**Not done yet (your job):** apply the user's decisions to the Lua defs and scripts. The user has not filled in
decisions yet. He may instead give blanket rules ("revert all sight and range to TA, keep the movement changes"):
then fill the Decision column from those rules and show him before applying. Do not change balance values without
his decision. Work on a branch, push, let him test.

Related project docs (claude.ai project "Total Annihilation: Recoil"; the user can paste them if you need them):
`claude/recoil-compat-notes.md` (Lua def conversion, headless test, engine fixes) and `s3o-remodel-handoff.md`
(the S3O remodel effort, which also turned every unit script into Lua).

## Setup in WSL

```
cd ~/TotalAnnihilation-Recoil            # keep the clone in the Linux filesystem, not /mnt/c
git fetch origin && git checkout ta-stat-review
pip install --user --break-system-packages lupa openpyxl     # python3.11+; lupa = Lua runtime for reading the defs
tools/ta-data/run_all.sh /mnt/c/<your TA install folder> ~/ta-data-out
```
`run_all.sh` needs these archives in one folder (names case-insensitive): `totala1.hpi`, `ccdata.ccx`,
`btdata.ccx`, `rev31.gp3` and the Cavedog downloadables `.ufo` (the user's file is `Cavedog_units.ufo`; the
script takes the first `*.ufo` it finds, so point it at a folder with only that one). `totala4.hpi` and `ccmiss.ccx`
are optional (campaign data). It extracts once (cached in `~/ta-data-out/x/`), takes ~4 min on 2 cores, and writes:

```
~/ta-data-out/x/<archive>/              each archive extracted (lowercased paths)
~/ta-data-out/merged/                   all layers overlaid in override order
~/ta-data-out/out/units.{csv,json}      final TA values per unit; JSON has every tag + per-archive history
~/ta-data-out/out/weapons.{csv,json}    same for weapons (weapons/*.tdf + gamedata/weapons.tdf explosions)
~/ta-data-out/out/weapon_damage.csv     per-target damage lists
~/ta-data-out/out/features.csv          wreck/heap metal, energy, HP
~/ta-data-out/cmp/unit_mapping.csv      repo unit -> TA id
~/ta-data-out/cmp/unit_diff.csv, weapon_diff.csv      raw diffs
~/ta-data-out/cmp/units_final.csv, weapons_final.csv  classified diffs (what the workbook shows)
~/ta-data-out/cmp/aim_diff.csv, aim_scripts.csv       turret speed diffs
~/ta-data-out/TA_vs_Recoil_stat_review.xlsx
```
The Cavedog data and the outputs stay out of git (the repo is public; the archives are Cavedog's). Only the
tools live in the repo.

## Tools (tools/ta-data/)

| File | What it does |
|---|---|
| `hpi.py ARCHIVE OUTDIR [--list] [--filter s]` | HPI/UFO/CCX/GP3 extractor (header key XOR obfuscation, SQSH chunks: LZ77 = method 1, zlib = 2, per-chunk byte encryption) |
| `tadump.py XDIR OUT` | parses FBI/TDF (`parse_tdf`), layers archives in `LAYERS` order, writes out/ |
| `compare.py REPO OUT XDIR CMP` | loads the repo's Lua defs with lupa, maps units (`MANUAL` overrides + side/name), checks models against TA 3DOs, diffs every tag, pairs weapons through unit slots |
| `finalize.py REPO OUT MERGED CMP` | classifies rows (Balance / Convention / Recoil-only tag), compares effective movement (resolves both sides' movement classes), folds per-target damage lists into one row |
| `aimspeeds.py` | aim turn speeds: `cob_aim()` = stack interpreter over COB bytecode; `lua_aim()` = `Turn()` calls in Lua unit scripts |
| `compare_aim.py REPO OUT XDIR CMP` | turret speed diff per (piece, axis) |
| `build_xlsx.py CMP OUT.xlsx` | review workbook (env `TA_REPO_REV` labels the commit) |
| `pieces.py` | 3DO piece-tree reader (skeleton comparisons) |
| `run_all.sh` | everything above in order |

Python note: run anything that reads extracted archive content with `python3 -I` (the extracted tree is untrusted
data; `-I` keeps a stray `json.py` in it from shadowing modules).

## The archives (what is where)

TA's data lives in HPI-format archives regardless of extension. Override order (later wins; the game's own rule is
roughly .gp3 > .ccx > .ufo > .hpi):
`totala1.hpi` -> `totala4.hpi` -> `ccmiss.ccx` -> `ccdata.ccx` -> `btdata.ccx` -> `Cavedog_units.ufo` -> `rev31.gp3`.

Findings:
- Unit/weapon data is only in `totala1.hpi` (157 FBIs), `ccdata.ccx` (266), `btdata.ccx` (203), the `.ufo` (6) and
  `rev31.gp3` (189). `totala2/3.hpi`, `ccmaps.ccx` are maps/installer; `totala4.hpi`, `ccmiss.ccx` are campaigns.
- The user's `ccdata.ccx` is already the patched v3.0 build (`gamedata/version.tdf` says `GPFVersion=v3.0`).
  3.1c (`rev31.gp3`) differs from it in only 6 unit files and 7 weapon files (EMP, Sniper, York, Sentinel, Shark,
  Tron...). CC replaces every base-game FBI.
- Battle Tactics adds nothing: its 197 shared FBIs are byte-identical to CC; its 6 others are the ones 3.1c has.
- `Cavedog_units.ufo` = the 6 downloadables: Flea `armflea`, FARK `armfark`, Scarab `armscab`, Hedgehog `cormabm`,
  Immolator `corplas`, Necro `cornecro` ("Resurrection Kbot").
- Final set: 278 TA units, 197 weapons (incl. explosions from `gamedata/weapons.tdf`), 1632 features.
- 13 TA units have no repo unit, all campaign/props: Galactic Gates, Implosion Devices, Alien Beacons, Scorpion,
  Sea Serpent (both sides each), Hydration Plant, Truck.
- Original data bugs: three FBIs reference explosions that do not exist anywhere (`big_building`,
  `big_buildingex`, `medium_unitex`; Leveler, seaplanes, Moho metal makers...). TA ignored them; the repo maps them
  to `large_building(ex)` / `big_unitex`. Keep the repo's choice unless the user says otherwise.
- `totala1.hpi/units/allunits.xls` + `more.txt` are Cavedog's own balance sheet: cross-reference only, the FBIs are
  what the game loaded.
- `totala1.hpi/scripts/*.bos`: 157 BOS sources for the base units (CC/BT/patch units are COB only). Handy to
  read intent; the COB in the highest layer is authoritative.

## Unit mapping (repo stem -> TA id)

Repo stems are `<SIDE>_<TIER>_<CLASS>_<Name>`; TA ids are `armpw` etc. Match = side + display name, then these
hand overrides (`compare.py MANUAL`), all verified:
- Fusion plants: `*_T2_ECO_FusionPowerplant` = `armfus`/`corfus`, `*_CloakableFusion` = `armckfus`/`corckfus`,
  `*_SEAECO_UWFusionPowerplant` = `armuwfus`/`coruwfus` (TA: "Fusion Reactor" names).
- `CORE_T2_BOT_Necro` = `cornecro`; `CORE_T2_VEH_Pillager` = `cormart` (TA "Mobile Artillery");
  `*_T2_BOT_DecoyCommander` = `armdecom`/`cordecom`.
- `ARM_T1_SEADEF_Defender` = `armfrt` ("Defender - NS"). Name matching alone paired it with land `armrl`.
- Mines by NUMBER: `*_T1_DEF_MineN` = `armmineN`/`cormineN`. BOTA renamed Core mines (Mine2 is called "M-303",
  Mine3 a second "M-515"), so name matching scrambles them. With this rule every mine 3DO is byte-identical to TA's.
Check after any change: no TA id used twice (compare prints duplicates when you check `unit_mapping.csv`).
At the compared commit 173/266 repo 3DOs were byte-identical to TA's; on current main every unit is an S3O remodel,
so model identity can no longer confirm the mapping: keep the overrides.

## TA -> Recoil: how values translate

Verified in the Recoil source at tag 2026.09.01 (`rts/Sim/Units/UnitDef.cpp`, `rts/Sim/Weapons/WeaponDef.cpp`,
`rts/Sim/Units/Unit.cpp`, `rts/Sim/Misc/ModInfo.cpp`). Recoil reads TA's FBI tag names (case-insensitive) and was
built to TA's conventions, so most values copy across 1:1. The repo's unit Lua still uses TA tag names; keep them.

### Units

| TA tag | Recoil reads it as | Translation |
|---|---|---|
| buildcostmetal / buildcostenergy | cost | 1:1 |
| buildtime, workertime | `buildTime`, `buildSpeed` | 1:1. Seconds to build = buildtime / workertime (`CUnit::AddBuildPower`: step = power/buildTime, builder power = workertime per second). Resources drain in proportion to progress. As far as known TA uses the same formula; quick in-game check: Arm Commander (workertime 300) builds a Solar Collector (buildtime 2495) in ~8.3 s |
| builddistance | `buildDistance` (default 128) | 1:1 elmos (TA pixels = elmos) |
| maxdamage | `health` | 1:1 |
| maxvelocity | `speed` = maxvelocity x 30 | 1:1: both are distance per sim frame at 30 frames/s |
| acceleration / brakerate | `maxAcc` / `maxDec` | 1:1 per-frame units |
| turnrate | `turnRate` | 1:1 (COB angle units: 65536 = 360 deg) |
| sightdistance, radardistance, sonardistance, radardistancejam, sonardistancejam | LOS/radar radii | 1:1 elmos. Recoil rounds to its LOS grid (`losMipLevel`); TA's LOS was height-based, Recoil's is height-aware too but not identical |
| energymake, metalmake | unconditional income | 1:1 per second |
| energyuse | `energyUpkeep` | 1:1, but **only charged while the unit is activated** |
| makesmetal, extractsmetal, windgenerator | conditional | **only while activated** (`CUnit::SlowUpdate`). Wind: output = min(current wind, windgenerator). Extraction: `extractsmetal` x metal-map values in the extractor radius, so it depends on the map conversion; check against a known TA map |
| tidalgenerator | unconditional | x map tidal strength |
| energystorage / metalstorage | 1:1 | |
| cloakcost / cloakcostmoving / mincloakdistance | 1:1 | per second / elmos |
| damagemodifier | `armoredMultiple` | 1:1 (damage multiplier while armored/closed) |
| cruisealt | `cruiseAlt` | 1:1 |
| footprintx/z, maxslope, maxwaterdepth, minwaterdepth | movedef | the unit's movementclass decides; compare **effective** values (finalize.py does) |

Activation: `activatewhenbuilt = 1` in the def, or the unit script setting `COB.ACTIVATION` (the wind generator
scripts do this in `Create()`), or the player toggling `onoffable` units. Any unit you give upkeep, metal making,
extraction or wind output must be activated one of those ways or it produces nothing. finalize.py classes
`activatewhenbuilt` rows as Convention; re-check them if you touch an eco unit.

### Weapons

| TA tag | Recoil | Translation |
|---|---|---|
| range | elmos | 1:1 (Recoil cannons also use `heightMod`, default 0.8, and `cylinderTargeting`: range vs height differs from TA) |
| reloadtime | seconds | 1:1 |
| damage {default, <unit>=} | per hit | 1:1; see per-target damage below |
| areaofeffect | diameter (engine halves it internally) | 1:1 |
| edgeeffectiveness | 1:1 | but see BOTA post-processing |
| weaponvelocity / startvelocity | elmos per second | 1:1 |
| weaponacceleration | elmos/s^2 | 1:1 |
| turnrate (guided) | COB angle units per second | 1:1 |
| flighttime, weapontimer, burstrate | seconds | 1:1 |
| burst, projectiles | counts | 1:1 |
| tolerance, sprayangle, accuracy | TA angle units | 1:1 |
| energypershot / metalpershot | per shot | 1:1 |
| lineofsight / ballistic / dropped / vlaunch / beamweapon / selfprop / guidance / tracks / twophase | weapon type | the repo now writes native `weapontype` etc. (see compat notes); these show as "Convention" rows, not balance |

### Per-target damage (important)

TA lists damage per unit name; Recoil uses armor classes from `gamedata/ArmorDefs.lua`, which in the repo has one
class, `planes` (all aircraft). Almost every TA anti-air weapon does ~2x its default against each aircraft
(missile ship: 57 default, 108 vs 20 aircraft). The repo kept only `default` on most AA weapons, so **AA does about
half its TA damage to aircraft**. Only `armflak_gun`, `corflak_gun`, `armrl_missile`, `corrl_missile`,
`corfrt_missile` have `damage.planes`. To revert: `damage = { default = <TA default>, planes = <TA per-aircraft
value> }` (TA uses one value for all aircraft on almost every AA weapon). Weapons whose per-unit lists target
non-aircraft (EMP/stunner vs ~149 units, Tron, sniper, torpedoes, mines, Immolator) need new armor classes or a
judgement call: ask the user. Workbook rows: Weapons sheet, Stat = "Per-target damage".

### BOTA post-processing that changes what the numbers mean (`gamedata/weapondefs_post.lua`)

- **Cannons**: `weaponvelocity` is overwritten at load: `sqrt(range * gravity * 900 / sin(2 * 30 deg))` with
  `mygravity = 0.25` (modoption `gravity`) and `heightboostfactor = 0.04` (all Cannon types except the Tornado's
  `armsfig_weapon`). So the def's velocity is dead; reverting a cannon's **range** changes its projectile speed. To
  get TA's ballistics, the user must decide whether to drop this post-processing (gameplay change; ask).
- **Explosive weapons** with `edgeeffectiveness > 0` and AoE < 145: AoE becomes `min(AoE / (1 - edge), 160)` and
  edge becomes 0.
- `cratermult`/`craterboost` x 0.4; inertialess weapons get `impulsefactor = 0`.

### Engine and rule defaults that differ from TA (no unit tag needed to change them)

- `idleAutoHeal` defaults to **10 HP/s** after `idleTime` 600 frames. TA has no idle regeneration. BOTA sets 0.5 /
  2200 on 261 units ("Recoil-only tag" rows); any unit that lacks it heals 10 HP/s.
- `gamedata/modrules.lua` (repo): `featurevisibility = 2`, flanking `defaultmode = 0` (off), `reclaimmethod = 0`
  (gradual), `losmiplevel = 3`. **`airlosmiplevel`, `losmul`, `airlosmul` are not read by Recoil 2026.09.01**
  (the engine reads `sensors.los.airMipLevel` and `radarMipLevel`; air LOS is at the default 1). Fix only with the
  user's OK.
- Not set in the repo and different from TA (verify TA behaviour before changing): construction decay is **on**
  (unfinished buildings decay after 6.66 s at 3 %/s; TA nanoframes did not decay); `repair` costs nothing;
  resurrect costs 0.5 x energy; `transportShip = false`; `fireAtKilled = false`.

### What lived in TA's executable or maps (not in the archives)

Damage-armor interaction beyond per-unit lists, projectile physics and inaccuracy models, aircraft flight model,
veterancy, metal extractor yield vs. map metal, wind range and tidal strength (map `.ota`). These cannot be
copied, only matched by testing.

## Findings (balance rows on main @ d06fed81, 2026-11-06; identical to 7c805bd)

1,394 unit-stat differences, 566 weapon-stat differences; every unit has at least one. BOTA's pattern vs TA 3.1c:

| Stat | Rows | Typical repo change |
|---|---|---|
| Sight range | 238 units | +75 % |
| Weapon range | 125 weapons | +45 % |
| Weapon damage | 113 weapons | +33 % |
| Max speed | 100 units | +20 % |
| Acceleration | 67 units | +70 % |
| Area of effect | 53 weapons | +75 % |
| Metal cost | 97 units | +14 % (67 up, 30 down) |
| Energy cost | 86 units | +7 % (48 up, 38 down) |
| Build time | 80 units | -5 % |
| Hit points | 76 units | +15 % |
| Build range | 23 units | ~2x |
| Max slope (effective) | 91 units | +33 % |

Plus:
- **Builders and commanders lost their energy production** (51 rows): TA Commander makes 25 E, Construction
  Aircraft 11, Advanced Construction Aircraft 24, etc. Early-game economy changes.
- **AA vs aircraft halved** (per-target damage, above).
- The Commander's D-Gun (`arm_disintegrator`/`core_disintegrator`) is in TA weapon slot 3; the repo has one shared
  `disintegrator` (pairing note rows).

## Turret aim speeds

Speeds of the `turn ... speed` commands inside each unit's aim functions. COB speeds are COB angle units per second
(65536 = 360 deg, so deg/s = value / 182.044) in both TA and Recoil. Lua `Turn(piece, axis, angle, speed)` takes
radians per second. Note the COBWTF sign rule from the S3O handoff (z-axis turns and x-axis moves are negated by the
engine for COB; Lua ports negate them by hand) - it affects angles, not speeds.

How `cob_aim` works: COB pushes the **speed first, then the target**, then `TURN piece axis` (opcode 0x10002000,
two inline operands). A pattern match on the preceding push picks the target, which is wrong. `cob_aim` runs a small
stack interpreter over each `Aim*` function using the opcode table in `aimspeeds.OPS` (operand counts and stack
effects from Recoil's `CobOpCodes.h`), folding constant arithmetic. Validated against the BOS sources (Peewee torso
150 / arms 200, Goliath 70 / 50, HLT 200 / 200).

On current main every unit runs a Lua script, most generated by `tools/s3okit/kit/cob2lus.py` from the repo's COB
(speeds written as `rad(44.99)`; `lua_aim` understands `rad` and `math.rad`). They use one
`script.AimWeapon(num, heading, pitch)` for all weapons, so the comparison is per (piece, axis), not per weapon slot.

Result (main @ d06fed81): 56 real speed differences on 29 units, 51 rows where a piece was renamed/moved by the
remodels (e.g. Goliath `turret`/`sleeve` -> `turret1`/`sleeve1`, Reaper `sleeves` -> `sleeve1/2`, AK arms ->
`lshoulder/rshoulder`; pair them by hand), 3 rows where a script computes its speed (commanders).
- Hand-written Lua towers use one generic 5 rad/s (286.5 deg/s) instead of TA's per-tower speed: LLT, Sentinel,
  Defender (land + NS), Pulverizer, Stinger, Flakker (TA 700/550), torpedo launchers (TA 80), Stingray (171.9 vs
  150). Guardian/Punisher are slower (20 vs TA 30/45). Big Bertha 5.2 vs TA 5/2.
- BOTA-modified COBs (carried into the cob2lus ports): Penetrator 50 vs TA 8/4; Doomsday 10->50, 300->200, 200->300;
  Annihilator 25/20 vs 50/50; Weasel 200 vs 90; Instigator 180 vs 90; AK torso 225 vs 90; Pyro 2x; Reaper, Crock,
  Goliath faster; Leveler traverse 90 vs 170; Slasher elevation 60 vs 150; Pillager 35 vs 50; commander arms 90 vs 45.
- Values like 300 -> 299.9 are recompiler rounding; ignored (< 1 %).
- Not covered: barrel spin speeds, restore-to-idle speeds (only aim functions are read).

## Applying decisions (next step: write `tools/ta-data/apply.py`)

Input: the workbook's Decision/Notes columns (Units, Weapons, Turret Speeds sheets). Plan:
1. Read rows with Decision = "Revert to TA" (value = TA column) or "Custom value" (value = Notes).
2. Units: edit `units/<stem>.lua` **as text**, replacing the `<tag> = <value>,` line in place (keep the FBI key
   order, comments and the `-- old//values` comment style BOTA uses; add missing tags next to their group, e.g. an
   energymake line under the costs block). Do not regenerate files from lupa output: that loses comments/order.
3. Weapons: weapons are defined in `Weapons/*.lua` (some, e.g. `emg`, `coax_torpedo`, exist in two files as
   identical copies: change both). A weapon shared by several units changes all of them: the workbook's "Used by"
   column lists them; warn the user when a unit-specific decision hits a shared weapon.
4. Movement rows: the value lives in `gamedata/movedefs.lua` (shared by every unit of that class). Changing one
   unit's slope means moving it to another class or making a new one: ask.
5. Per-target damage: write `damage.planes` (and add armor classes in `ArmorDefs.lua` only with the user's OK).
6. Turret speeds: edit the `Turn(...)` speed in `scripts/<stem>.lua` (`rad(<deg>)`). If a script is generated by
   cob2lus, check whether the S3O work regenerates it (its header says "generated by ... cob2lus.py"; a
   regeneration would overwrite hand edits: change the source COB or the generator's input instead, ask).
7. Verify: rerun `run_all.sh` (applied rows must disappear from the diff), then the headless test
   (`tools/headless-test/run.sh <engine dir>`, see compat notes) and the def dump diff method from the compat notes
   (dump runtime UnitDefs/WeaponDefs before/after: only the intended tags may change).
8. One commit per logical change set, messages say why; push the branch; the user tests in game.

## Open questions for the user (ask when relevant, not all at once)

- Blanket rules or row-by-row decisions?
- Keep BOTA's cannon gravity post-processing, or restore TA ballistics (velocity from the def)?
- AA vs non-aircraft per-unit damage: add armor classes (e.g. commanders, ships) or approximate?
- Builder/commander energy production: restore TA's?
- idleAutoHeal: TA had none; keep BOTA's 0.5 HP/s?
- Construction decay and the ignored modrules keys (`airlosmiplevel` -> `airMipLevel`).
- Turret speeds: revert the generic 286.5 deg/s Lua towers to TA's per-tower speeds?

## Gotchas

- Run `run_all.sh` from the branch you are changing; it compares against the checkout it lives in.
- lupa loads unit defs with a `Shared` stub (build lists); a def that errors in lupa errors in the engine too.
- Unit keys in the Lua are lowercase stems (`arm_t1_bot_peewee`); file stems keep case.
- Repo explosions were renamed (`commander_blast` -> `commander_explosion`, `big_building` -> `large_building`);
  `unit_diff.csv` lists them as renamed, they are not balance changes.
- `weapon_diff.csv` "pairing" notes: `arm/core_disintegrator` (TA slot 3) vs the repo's shared `disintegrator`;
  TA's nonexistent explosions (data bugs above).
- The workbook's "Median change" column on the Read Me sheet is static (computed at build time).
- Generated at: cloud session 2026-11-06, repo main @ d06fed81.

## Normal maps (for CUS GL4)

`unittextures/<tex1 stem>_normals.dds`, one per S3O texture (541: units, wrecks, heaps), generated from the diffuse
by `tools/textures/normalmaps.py` (numpy + Pillow; its own DXT5 encoder: Pillow's tilted flat areas ~3 degrees).
Layout as BAR's CUS GL4 reads it: RGB tangent-space normal (red = image right, green = image down, measured on BAR's
own Arm textures), alpha = height. Capped at 1024. Units point at theirs with `customparams.normaltex`
(`UnitDef_Post`); features need nothing (CUS finds `<tex1>_normals.dds` itself). Re-run the script after changing a
diffuse texture (it skips up-to-date ones; `--force` redoes all, `--preview DIR` writes lit before/after images).

## Custom Unit Shaders GL4

Installed from https://github.com/Spring-Helper-Projects/Custom-Unit-Shaders-GL4 (see
`modelmaterials_gl4/README-TAR.txt`; our changes are marked "TA:Recoil"). Settings in `luarules/configs/cus_defs.lua`:
- Units and wrecks use our own option `OPTION_TEX2_SPECULAR`: our texture2s are classic Recoil ones (red = glow,
  green = specular, blue unused; read as PBR, blue 0 would make every unit a mirror). Glow stays; green sets
  metalness (x 0.6) and roughness (0.9 - 1.4 x green), in `cus_gl4.frag.glsl`.
- `brightnessFactor` 1.6 for units and wrecks (was 1.1 / 1.3): the PBR path darkens our older textures.
- Without GL4 (headless, servers) the gadget removes itself (was ~2300 errors per test run).
- Features get `customParams.normaltex` in `gamedata/featuredefs_post.lua` (which keeps the base content's own
  processing); this CUS has no naming fallback.
In game: `/luarules disablecusgl4`, `/luarules reloadcusgl4`; config `cus2 = 0` turns it off.

## LuaUI widget handler (from Splinter Faction)

`luaui/widgets.lua` is SF's `LuaUI/widgets_custom.lua` and `luaui/main.lua` its `main_custom.lua` (replacing the
XTA/stock handler), plus `luaui/cache.lua`. Our one addition (marked "TA:Recoil"): it also loads the Slate UI suite
from `LuaUI/Slate/Widgets/`. What SF's brings: the `SelectionChanged` call-in (Slate's commands widget and the fancy
selection widget use it; the old handler never called it), game files always before loose ones, and loose user
widgets only with the `allowuserwidgets` modoption (off). Saved widget settings: `LuaUI/Config/TART_data.lua`.
`luaui/widgets/gui_fancy_selected_units.lua`: SF's selection rings, unchanged.

## Graphics widgets from Splinter Faction (batch 1)

Unchanged SF files ("From Splinter Faction" header), toggles in the Slate graphics options:
`luaui/widgets/` gfx_deferred_rendering_gl4 (dynamic lights; with api_unit_tracker_gl4 and the gadget
`luarules/gadgets/gfx_explosion_lights.lua`), gfx_bloom_mipchain, gfx_tonemap, gfx_ground_ao_gl4,
gui_healthbars_gl4, gui_range_overview_gl4, gfx_orders_gl4, gfx_build_footprint_gl4, gui_reclaim_field_highlight.
Support: `luaui/widgets/include/` (SF's LuaShader etc.), `luaui/shaders/*.glsl`, `luaui/images/` (health bar atlas,
noise), `luaui/configs/DeferredLightsGL4*.lua`, `luarules/configs/customcmds.h.lua`. Weapon lights are assigned to
every weapon by type/colour automatically; the per-unit lamp table in DeferredLightsGL4config.lua is SF's (keyed by
SF unit names, so it matches nothing here yet). Initial settings v3 turns on AllowDeferredMap/ModelRendering
(the lights and bloom need the G-buffers).

## Unit lights (generated)

`luaui/configs/DeferredLightsGL4unitLights.lua` is generated by `tools/textures/unitlights.py`: for each unit, the
glow painted in texture2's red channel is mapped onto the S3O geometry (texture V as is), clustered per piece, and
each cluster becomes a point light just off the surface in the painted colour (up to 4 per unit; 242 units). Re-run
after changing a model or its textures. Hand-made lights go in `DeferredLightsGL4config.lua` `unitLights` (a unit
listed there keeps those instead). `api_unit_tracker_gl4` is moved to layer -999999999 so it loads before the
lights widget (SF's order left unit lights off).

## Weather and unit headlights (from Splinter Faction)

`luaui/widgets/gfx_timecyclesweathereffects_weather.lua` (day/night cycle, war-weariness tint, rain fog, heat waves,
lightning on big explosions; drives sun and atmosphere, publishes WG.weather) with the synced gadget
`luarules/gadgets/weather_seed.lua` (per-match seed so every player sees the same weather), and
`luaui/widgets/gfx_unit_headlights.lua` (mobile units switch on cone headlights at dusk or in heavy storms, through
the deferred lights widget; `/luaui headlights on|off|auto`). Unchanged SF files. Per-unit options: customparams
`headlights = "0"` (none) or `headlight_pieces = "a,b"` (default: an automatic front-centre spot). The effect widgets
it drives are in too: `gfx_timecyclesweathereffects_fog.lua` (ground fog), `_rain.lua` (rain streaks, splashes, falling
ash), `_heat.lua` (heat-haze shimmer).

## Distortion GL4 (from Splinter Faction)

`luaui/widgets/gfx_distortion_gl4.lua`: screen-space shockwaves and heat ripples at weapon impacts, explosions and
muzzles (needs the deferred G-buffers, like the lights). Distortions are assigned to every weapon by type and size in
`luaui/configs/DistortionGL4WeaponsConfig.lua`; `DistortionGL4Config.lua` has SF's per-unit table (SF unit names,
matches nothing here). Shaders in `luaui/shaders/`. The unit tracker is now at layer -2000000000 so it loads before
both this and the lights widget.

## Map Grass GL4 (from Splinter Faction)

`luaui/widgets/map_grass_gl4.lua`: instanced 3D grass blades, swaying in the wind, coloured from the map, burnt down
by explosions. Grows where the map's own grass map says (or a map's `mapinfo.custom.grassconfig` /
`[map]_grassDist.tga`; `/editgrass`, `/savegrass` to paint one). Blade textures (0 A.D., CC-BY-SA 3.0) in
`luaui/images/luagrass/`, shaders in `luaui/shaders/`, `luaui/include/grassPatches.lua`. Initial settings v4:
`GrassDetail = 0` (engine grass off, or both would draw). Off by default on weak GPUs (Intel, under 1.8 GB).
Test on a real map: `VISUALMAP=/mnt/e/EvoDev/xxxmaps/altair_crossing_v3.sd7 VISUALMAPNAME=Altair_Crossing_v3`.

## Graphics widgets from Splinter Faction (the rest)

Unchanged SF files (toggles in the Slate graphics options): Contrast Adaptive Sharpen, Outline (deferred), SSAO,
Depth of Field (off), Darken Map, GUI Shader (+ API Screencopy Manager), Attack AoE, Highlight Unit, Highlight Selected
Units (off), Aircraft Trails GL4, Altitude Lines GL4, Airjets GL4, Under construction gfx, Ground Texture Highlight
(power range), Mouse FX, Mapmarks FX, Build ETA, Self-Destruct icons, Given Units, Start Boxes, Start Radius, Snow,
Building Grid GL4 (off), and LUPS (wrapper widget + gadget, LupsManager, Units on Fire, cloak FX, shockwaves).
`lups/` is now SF's (newer) LUPS library (BOTA's extra thundairjet class kept). Support files: `luaui/widgets/shaders/`,
`luaui/images/` (mapmarksfx, snow, glow), the Saira fonts copied into `luaui/fonts/` (SF widgets load them from
there). Not ported (not for TA): shields, disruption electricity; SF's World Labels (replaced, below).

Aircraft thruster flames: `luaui/configs/lupsunitfxs_ta.lua`, generated by `tools/textures/airjets.py` from each
aircraft's exhaust pieces (thrust/jet/exhaust...; hovering aircraft blow down, planes backward; Arm blue-white, Core
orange), merged into SF's `lupsunitfxs.lua` (its own entries are SF units).

Commander name tags: `luaui/slate/widgets/slate_nametags.lua` + `luaui/slate/rml/nametags.rml`, a Slate pill (.panel:
the player's opacity and tint) with a team-colour dot and the owner's name under every visible commander; decoy
commanders get their owner's tag too (a tag-less commander would give a decoy away).

## Shields (for modders; TA has none)

From Splinter Faction, inert unless a unit has a shield: `luaui/widgets/gfx_shields_gl4.lua` (instanced bubbles,
impact ripples, intersection glow, charge state), `luarules/gadgets/lups_shield.lua` (+ `luarules/configs/
lups_shield_fxs.lua`, `luarules/gadgets/include/IterableMap.lua`), `unit_shield_onoffable.lua` (the unit's on/off
switches its shield), `unit_protoss_style_shields.lua` and `unit_deflect_aoe_damage_to_shield.lua`.
To give a unit a shield: a weapon with `weapontype = "Shield"` and a `shield = { power, powerregen, radius, ... }`
table, and `customparams.shield_radius = <radius>` (the bubble visuals key on it). Optional:
`customparams.isshieldedunit = "1"` (+ `shield_max_strength`, `shield_regeneration_delay`,
`shield_regeneration_rate`) for a personal Protoss-style shield, `customparams.shield_deflect_damage = 1` to route all
damage to the shield first (TA:Recoil made this opt-in; the gadget unloads if no unit uses it). Test unit:
`tools/headless-test/tartest.sdd/units/zz_test_shield.lua` (probe mod only).

LuaRules now loads `init.lua` (Common/: table.copy, Spring.Utilities...) and SF's `luarules/utilities/`
tablefunctions + unitTypeChecker before the gadget handler, like LuaUI; SF gadgets, configs and LUPS expect them.


## Mexes and geovents (SF-style metal spots)
- luarules/gadgets/game_metal_spots.lua: one spot per metal patch (peaks of the box-blurred metal map, refined to the
  patch's metal-weighted centre, snapped to a square centre where odd-footprint buildings sit), stamps building mask 4,
  publishes GG.metalMakerSpots and GameRulesParams metalSpot_count / _<i>_x / _z / metalSpot_value / metalSpot_players.
- game_metal_spot_output.lua: SetUnitResourcing cmm/cue on finished mexes (value x customparams.metal_spot_mult,
  customparams.mex_energy), off when switched off; calls the script's ExtractionRateChanged so the arms spin.
- unit_mex_upgrade.lua: a higher-tier mex finishing removes lower ones under it (DestroyUnit reclaimed).
- game_geovent_spots.lua: map geoThermal features -> GG.customGeoventSpots + customGeovent_* params.
- gamedata/alldefs_post.lua: names ending metalextractor / _mohomine get extractsmetal 0, buildingmask 4,
  energyuse 0 (moved to customparams.mex_energy), onoffable, moho yardmap all "s".
- Widgets from SF: game_metal_spot_loader, game_metal_spot_minimap_drawer, game_metal_maker_placement_snapping
  (TA:Recoil changes: picks highest tier, allows moho over own mex, right-click geovent), game_geovent_spot_loader,
  _minimap_drawer, _highlight (all map vents). Own: game_metal_spot_rings.lua (F4 replacement).
- Test: MEXPROBE=1 MAP=... MAPNAME=... tools/headless-test/run.sh (zz_mex_probe.lua).

## Unit control widgets from Splinter Faction
- cmd_customformations2.lua (right-drag to draw a formation line; images/formationDot.dds),
  cmd_line_move_spread.lua (a single-click move spreads the group into a line abreast facing the travel direction),
  unit_auto_group.lua (Alt+0-9 sets an autogroup for the selected unit types; new units of that type join it;
  Alt+` removes), unit_auto_group_com.lua (commander into group 1 at game start), gui_select_and_center.lua
  (selects and centres on the commander at game start; TA:Recoil uses SetCameraTarget so any camera mode works).
  gui_group_recall_fix.lua (pressing a group number again only centres the camera on a quick double press).

## HD cursors
- tools/cursors/cursors.py redraws TA's cursor set (plus fight, manual fire and wait) as anti-aliased vector art
  with smooth animation, in 32/48/64/96 px sets: anims/hd/<size>/<cursor>_<i>.png + <cursor>.txt spec files
  (per-frame lengths, hotspot). anims/<cursor>.txt = the 48 px set (the engine reads spec files first).
  `--preview DIR` writes an animated GIF of the whole set. The old TA .bmp frames were removed (in git history).
- luaui/widgets/gui_cursor_size.lua swaps in the set nearest 48 px per 1080 lines (or config TARCursorSize).

## Set Target (from Splinter Faction)
- luarules/gadgets/unit_target_on_the_move.lua: Set Target / Cancel Target commands (Zero-K IDs 34922-34925, as in
  luarules/configs/customcmds.h.lua, so orders GL4 and CustomFormations2 know them). A unit keeps its target while
  moving and fires at it whenever it is in range. Cursor "settarget" = cursorsettarget (tools/cursors/cursors.py,
  assigned by gui_cursor_size.lua). luaui/widgets/cmd_set_target_key.lua binds Y (SF's key) unless Y is taken.
- Probe: MEXPROBE also checks a set-target order locks on (units must be on dry land: weapons can't test
  underwater targets).

## Key bindings (SF's overhaul, in Slate)
- luaui/slate/widgets/slate_api_keybindings.lua rebuilds the binds from scratch: unbindall, then
  luaui/configs/tar_keys.txt (game binds, archive only), then luaui/slate/configs/engine_default_keys.txt (the
  engine's built-in binds, generated from KeyBindings.cpp, identical to 2026.09.02; archive only), then the
  player's tar_uikeys.txt from the Keybinds window. The shared uikeys.txt is never used (other games' binds).
- tar_keys.txt: Alt+S/D/X split / swap / recombine selection (luaui/widgets/gui_split_selection.lua), Y / Ctrl+Y set /
  cancel target, Ctrl+P pause, F11 / Ctrl+F11 widget selector / tweak mode. Runtime binds belong in a reapply hook
  (WG.SlateKeybindings.AddReapplyHook) or, better, in tar_keys.txt.
- The Keybinds window reads its action vocabulary from the archive only (VFS.ZIP) as SF does.
- Test: KEYPROBE=1 run.sh writes a stale uikeys.txt and logs "[PROBE] keys ..." for a few keys. The test mod's
  short name is TART, so tartest.sdd/luaui/configs/tart_keys.txt links to tar_keys.txt.

## Loading screen (LuaIntro, from Splinter Faction)
- LuaIntro/main.lua + config.lua (SF; the handler is the engine's base content LuaHandler). Addons:
  loadprogress.lua (SF: per-map load timing), bg_texture.lua (a random picture from bitmaps/loadpictures/, cropped to
  fill the screen; start1.jpg for now), main.lua (SF's panel drawn as a Slate window: rounded glass, a head with the card kind and map, the card sized to
  its text, a LOADING label / percentage / rounded bar; follows the player's Slate tint and opacity config),
  music.lua (plays LuaIntro/Configs/loadscreen.lua's music, TA's Intro.ogg, at snd_volmusic; names it in config
  music_loadscreen_track), bg_logo.lua (a disabled stub shadowing the engine's spinning logo), initial_settings.lua.
- Cards (tips, unit notes with pictures, quotes) and the track are data in LuaIntro/Configs/loadscreen.lua.
- Slate Music picks up the running stream, shows/remembers it as that track, then plays on through the playlist.
  music/Total Annihilation OST/artist.txt gives the folder its display name (VFS lower-cases folder names).
- To see the loading screen in a test, gl.SaveImage(0, 0, vsx, vsy, "x.png") inside DrawLoadScreen works (the
  screenshot command doesn't run while loading).

## Unit outline
- luaui/widgets/gfx_outline_shader.lua (SF's, unchanged) is on in every Slate graphics preset but Lowest (was High
  and Ultra only). It pauses itself below 15 fps.

## Quality-of-life widgets and gadgets from Splinter Faction (batch of 2026-11-08)
- Orders: gui_commandinsert (Space+click puts an order at the front of the queue, Space+Shift+click where it fits
  best), cmd_split_buildorders (rewritten: each shift-queued building goes to the selected builder that can build it
  with the fewest buildings queued, counting orders still on their way; clicks only, orders a widget gives through
  Spring.GiveOrder don't reach CommandNotify), cmd_queue_copypasta (Space+Alt+N copies queues, Space+N pastes; no
  longer saved between games), cmd_stop_selfd, cmd_state_reverse_toggle (right-click steps 3+ state buttons back; the
  engine sends state+1 with the right flag), unit_load_own_moving, unit_immobile_buider (on; TA has no immobile
  builders today, so idle).
- Building: unit_showbuilderqueue (on: ghosts of every queued building), cmd_persistent_build_spacing,
  gui_buildspacing (mouse side buttons, only while placing), autofirstbuildfacing, gui_reclaiminfo (own font; SF used
  its font API), gui_con_locater (hold Space).
- Team / spectators: gui_ally_cursors + luarules/gadgets/cmd_mouse_pos_broadcast.lua, gui_allySelectedUnits +
  cmd_selected_units.lua, gui_spectate_selected, camera_player_tv, cmd_stall_assist (off by default: it gives energy
  away). Player-TV and Ally Selected Units talk to WG['advplayerlist_api'], which slate_playerslist.lua now publishes
  (as SF's Bastion list does) next to WG.SlatePlayersList.
- camera_shake (big explosions shake the camera).
- Gadgets: unit_priority (Low / Normal / High construction priority button on builders and factories, CMD 34220),
  unit_stockpile_limit (caps only: 10 nukes, 20 anti-nukes, 10 EMP missiles, by weapon name; a silo starts empty and a
  fired missile is not replaced, as in TA; BAR's version fills silos to the cap), game_prevent_excessive_share,
  game_block_nanoframe_reclaim, factory_anti_slacker (new units are non-blocking for 12 s), unit_shared_preserve_orders
  (units given to an ally keep their queues; slate_share.lua sends each queue first, as SF's Bastion share does;
  checks the sender owns the unit; options sent as options.coded), cmd_luaui_reload (/luarules reloadluaui).
- game_auto_teamcolors (SF's, Interface > "Auto team colours" + palette, off by default, config AutoTeamColors /
  AutoTeamColorsPalette): the synced half makes every palette with synced random, so everyone on the same palette sees
  the same colours. Fixed: the params are now public (SF's were ally-only, so enemies kept lobby colours).
- Not brought over: unit_plane_stop (SF's is unfinished: no units tracked, MoveCtrl freeze), unit_transportee_hider
  (TA's ship/hover transports lift cargo onto the deck with a crane; UnitLoaded fires when the crane grabs it, so the
  unit would vanish mid-lift).
- Also: KEYSYMS -> Spring.GetKeyCode in gui_group_recall_fix / gui_con_locater / copypasta; unit_target_on_the_move
  uses GetUnitCommandCount (GetCommandQueue(id, 0) is deprecated).
- Test: PORTPROBE=1 run.sh (zz_port_probe + luaui zz_port_widget_probe; team 2 is an ally) logs "[PROBE] port ...":
  priority button, nanoframe reclaim, factory blocking, stockpile cap, splitter, preserved orders on share, team colour
  params readable by LuaUI. PORTCOLORS=1 also switches Auto team colours on (Red vs Blue). LuaUI orders reach the
  simulation ~30 frames later on headless; the probe steps are 40 frames apart.

## Commander box art (tools/boxart)
- run_boxart.sh renders 4K in-engine "box art" of a commander with the Windows engine (run_win_visual.sh setup),
  staged by tartest.sdd/luarules/gadgets/zz_boxart_probe.lua: a flat spot, a base behind, the scene turned toward
  the sun, a lighting preset (LIGHT=arm|core: sun angle, key/ambient colours, haze), then either the D-Gun fired
  toward a camera (AIMCAM) or a nanoframe built (BUILD=<unit>), paused, one screenshot per camera preset
  (CAMS="name:dist:height:side:look/..."), interface hidden, LuaUI graphics widgets kept.
- Useful config: CFG=$'HardwareCursor = 1\nMaxNanoParticles = 0\nWindowBorderless = 1\nWindowPosX = 0\nWindowPosY = 0\n'
  with W=3840 H=2160 (the borderless window gives the full 2160 rows; the engine's square nano particles are huge up
  close). The Initial Settings widget restarts a fresh-config match: the probe turns it off.
- The red tint on close-up commanders was their own glow lights (DeferredLightsGL4unitLights): DeferredLightsGL4config
  drops them when the boxart modoption is set. Gameplay is unaffected.
- grade.py arm|core in out: contrast, faction split tone, sky gradient, bloom, vignette, grain.
- Results of 2026-11-08: I:\Claude Space\Commander Box Art (Arm on Painted Badlands, Core on Incandescence).

## Footprints from movement classes (2026-11-09)
- As in Splinter Faction: `movedefs_tags.lua` lists footprintX/Z, so `movedefs_post.lua` copies each class's footprint
  into its units; `movedefs_classes.lua` sizes every class so its largest model fits (one step above TA's: kbots 3,
  tanks 3/4, hovers 4, HOVERBIG 6 for Turtle/Bear, ships 5/7/9 by beam, subs 5, commander 3, Krogoth 4). Why: TA's
  footprints came from the old models; 88 of 117 mobile units stuck out of theirs (clumping). Analysis script:
  `DUMP=` run.sh + `tools/ta-data/footprints.py <dump.json> [<SF fpdump>]` (model bounds vs engine xsize/zsize).
- Consequences handled: factory exit lanes at least as wide as the units (Arm kbot lab 4, Core vehicle plant 5, hover
  platforms 6); transports `transportsize` 4 and capacity x1.5 (Atlas/Valkyrie 4 = one unit; the Valkyrie's TA
  capacity 1 carried nothing). Death-explosion size (UnitSizeLevel) and SimpleAI placement use footprints of
  buildings only. Units define no collision volumes, so hitboxes are unchanged (model radius).

## Movement modoptions
- modoptions.lua section "Movement": movespeed, moveturn (multipliers, default 1.25), moveaccel, movebrake (multipliers
  since 2026-11-09, default 1.5 after play-testing, 1 = TA's; they were floors in elmos/frame^2 with 0 = TA's). Applied in
  gamedata/alldefs_post.lua UnitDef_Post to every def with a speed that can't fly. Walk cadence follows UnitDefs speed
  (scripts/headers/walk.lua), so legs keep pace. Checked with DUMP=1 run.sh at the defaults, at TA values
  (movespeed=1 moveturn=1) and at moveaccel=2 movebrake=2 (Peewee 0.1/0.19 -> 0.2/0.38, Stumpy 0.016/0.01 -> 0.032/0.02).
- moveturninplace (degrees, default 90) -> turnInPlaceAngleLimit. The engine's default 0 cuts a ground unit's target
  speed for ANY turn (to turnRate/angle of top speed, at least 10 %); with the braking floor that was a dead stop
  before every turn. TURNPROBE=1 run.sh measures it: 60 degree turn 100 % speed at 90, 10 % at 0.

## hideDamage
- Only the commanders hide their health from enemies (TA: HideDamage=1 in armcom.fbi / corcom.fbi only). The FBI ->
  Lua conversion had put hidedamage = 1 on every unit, so enemy health bars never showed and Slate saw no enemy
  damage. Decoy commanders show theirs, as in TA. Check: DUMP=1 run.sh, grep "hideDamage=true".

## Damage audit and slow projectiles (2026-11-08)
- `tools/ta-data/audit_damage.py DUMP.json TA_OUT CMP` checks the runtime defs (from a `DUMP=` run + `defdump.py`) against
  TA 3.1c: for every weapon and every unit, the damage the game deals that unit (`damages[armorType]`) vs TA's per-unit
  list or default; plus range, reload, area of effect (runtime stores the radius), projectile speed, burst.
  Result on ta-values @ 5e78d3a2: all 173 paired weapons match TA. The only damage rows are the deliberate aircraft
  deviation (10 aircraft TA's AA lists predate take the side's aircraft bonus), the only stat rows the speeds below.
  The Crasher and the Core decoy commander fire from slot 3/4 (NOWEAPON before): the audit's PAIRING row for
  `noweapon` is that, not a missing weapon.
- Slow projectiles (modoptions `shotspeed` 1-2, default 1.5 (1.25 until 2026-11-09), and `shotspeedcutoff` 0-1000 elmos/s, default 300; Movement
  section): `WeaponDef_Post` multiplies `weaponvelocity` (and `startvelocity`, `weaponacceleration`) by
  `SLOW_SHOT_MULT` = 1.25 for every weapon at or under `SLOW_SHOT` = 300 elmos/s except bombs: all torpedoes and depth
  charges, light cannons (170), medium cannons (210/220: Hammer, Thud, Bulldog, Reaper, Triton, Gimp, Crock), Pyro
  flamethrower (188), D-Gun (200), Goliath (250), Rocko/Storm rockets (250), Snapper (260), Leveler (280), Morty (290),
  E.M.G.s and the Crusader/Enforcer guns (300). Fastest untouched: Luger/Pillager/Immolator at 310. Death explosions
  and mines carry a dummy 250 that also scales (never fired; no effect). Damage, range and gravity unchanged; cannon
  arcs are flatter. AIM=1 probe: all still fire and hit as before. Checked with def dumps: defaults = the hard-coded
  version, `shotspeed=1` = TA exactly. `MODOPTS='\\n\\t\\tkey=value;' run.sh` passes modoptions to any probe.

## Range modoptions (2026-11-08)
- `buildrange` (1-3, default 1.5, 2026-11-09): builders' `builddistance` x mult (`UnitDef_Post`; only defs that set
  it, i.e. TA's 40-100 elmos; factories keep the engine's 128). Asked for after the footprint change: with units one
  footprint step bigger, TA's reach often could not start a building. Checked with DUMP=: commander 60 -> 90,
  constructors 40 -> 60.
- `weaponrange` (1-2, default 1.25 since 2026-11-09, user decision): every weapon's range x mult (`WeaponDef_Post`). Set missile `flighttime` scales too
  (others derive lifetime from range); Cannons get `weaponvelocity` x sqrt(mult) so v^2/g keeps its margin over the
  range (applied after the slow-shot boost, whose cutoff reads TA's speed). Anti-nuke `coverage` unchanged.
- `sightrange` (1-2, default 1.25): `sightdistance` x mult (`UnitDef_Post`); air sight follows (engine 1.5x sight).
  Radar/sonar/jammers unchanged.
- User's reason: short TA ranges make fights clump (only the front ranks are in range, the rest crowd forward).
- Checked: defaults give identical def dumps; at 1.25/1.25 only range/sight (+ derived maxWeaponRange, LOS radii,
  cannon speeds, set flight times) change; AIM=1 probe at 1.25 has no new NOFIRE/NOHIT.

## Radar icons (tools/icons, 2026-11-08)
- `tools/icons/make_icons.py [REPO] [--sheet out.png]` draws every icon (Pillow, 4x supersampled, 128 px), writes
  `Icons/*.png` (replaces the folder's PNGs), `gamedata/icontypes.lua` and `gamedata/unit_icons.lua` (unit -> icon type);
  `UnitDef_Post` applies the map, the unit files carry no `icontype` any more. Edit the `UNITS` table and rerun; the
  script refuses to run if a unit is missing from it.
- Design: frame = domain (kbot circle, vehicle box, hover lens, ship hull, sub dome, aircraft delta, seaplane delta +
  wave, amphibious = frame + wave, building square, defence shield, factory double box with the domain it builds,
  commander star, mine, wall), black glyph = role (chevrons 1/2/3 = light/assault/heavy, dot = artillery, ringed dot =
  long range, arrow = rockets, arc = anti-air, gantry = builder, ring = scout, arcs = radar/sonar, zigzag = jammer,
  cradle = transport, triangle = bomber, torpedo, starburst = crawling bomb, half disc = spy, bolt = EMP/energy,
  M/E = metal/energy (ring = maker, bar = storage), trefoil = nuke, rings = anti-nuke, crosshair = sniper/targeting,
  cross = repair pad), pips = tech level. White takes the team colour. Decoy commanders use the commander icon.
- Runtime check: `DUMP=` now also lists `iconType` (unsynced-only in UnitDefs) from zz_def_dump's unsynced half.

## Slate fixes (2026-11-08)
- Name tags (`slate_nametags.lua`) only for commanders in line of sight: IsUnitVisible also counted radar blips,
  whose positions carry radar error, so a tag floated near an enemy commander that had left sight (and showed on
  cloaked ones). `GetUnitLosState` returns a table for widgets (raw bits need full read).
- Hover info (`slate_selection.lua`): features get their own view (name, metal, energy); the engine tooltip's colour
  codes (\255 r g b, \b) are stripped before escaping (they showed as junk characters).

## Order lines with many units (2026-11-09)
- gfx_orders_gl4.lua: a big selection turned the ground into string. The rebuild now counts the queues it draws
  (selected + echoed units) and above TUNE.crowdFrom (8) scales every line's resting alpha by crowdFrom/n down to
  crowdMin (0.25 of restAlpha), thins the ribbons toward half width and shrinks the marks to 3/4; one unit's path
  is unchanged. WG.orders.get/setCrowdFrom, saved in the config. Checked with the new harness mode
  `VISUALMOVE=1` (every unit gets a two-leg move order at frame 60; camera on the path), 20 Peewees on
  Altair Crossing: faint but readable lines.

## Command colours (2026-11-09, from Splinter Faction)
- `cmdcolors_mod.txt` (game root) + `luaui/widgets/gfx_mod_cmdcolors.lua`: the widget feeds the file to
  Spring.LoadCmdColorsConfig at start and reloads the engine's `cmdcolors.txt` when disabled. The engine itself only
  ever reads `cmdcolors.txt` (Game.cpp, at load). Effects: engine unit selection boxes off (Fancy Selected Units draws
  them), the engine's queue lines at alpha 0.1 under the Orders GL4 marks (which gfx_orders_gl4.lua's header always
  assumed), queue icons half size, range rings alpha 0.5.

## Slate fixes (2026-11-09, from play-testing)
- Widget Selector (F11) "unloaded itself": its layer was -math.huge, so it initialised before Slate Core, found no
  WG.Slate and removed itself (its Shutdown then bound F11 to the engine's selector). Layer -99990 now.
- Graph windows (economy, end graph) drew their gl plot faint: core.lua appends the theme rules scoped under the
  body id ("#slate-themed .panel.window {...}"), which outranks the window's own "#econgraph { background: clear }"
  rule, so the glass covered the plot after all. The theme now carries ".panel.window.hole { clear }" and both
  windows have class "hole" (ThemeRules in slate_api_core.lua). Rule of thumb: nothing in a document's own
  stylesheet can beat the appended theme rules except with another class on top of the theme's selector.
- Orders panel: labels wrap onto a second line (long ones in 11dp), and the engine's own names that fit nowhere are
  relabelled (LABELS in slate_commands.lua: ManualFire -> Manual Fire, LoadUnits -> Load...). Tile widths keep 2dp
  spare so dp-to-px rounding cannot wrap the last tile of a row (at 900p a 4-column grid became 3 columns and
  overflowed the orders header).
- Build panel: the mouse wheel no longer turns pages (arrows only).
- Minimap: a real Slate frame (1dp light line, 6dp glass band in the theme's panel colour and opacity, 1dp inner
  line; minimap.rml + slate_minimap.lua). The engine draws the minimap before RmlUi and does not bend to the UI, so
  the frame is hollow and re-wraps the minimap's geometry every frame; the minimap is inset by the frame plus 4px.
  (The old frame was a 2dp dark line that vanished against the map.) The frame's colour follows opacity/tint
  (OnSettings, which was referenced but never defined before).
- The small dark pill in the screen's top-left corner was a hidden commander name tag: the theme's .hidden
  (display: none) lost to the tag's own display: flex (same specificity, the file's rule wins), so hidden tags
  parked at 0,0 as empty pills. nametags.rml now has .tag.hidden { display: none }. Same lesson as the graphs: a
  document's own rule outranks theme.rcss at equal specificity.
- Checks: run_win_visual.sh with VISUALSELECT=1 (keeps LuaUI), VISUALCMD="luaui econgraph" opens the economy graph,
  screenshots zoomed with tools/ta-data/pngcrop.py (pure Python; no PIL on this machine).

## Faction pictures and emblems (2026-11-09)
- `tools/faction_logos.py` (Pillow + numpy, system python3) draws `luaui/slate/images/factions/arm.png` and `core.png`
  for the faction chooser at 1568x880 (4x the 392x220 dp shown, sharp to 8K) and the emblems alone as
  `arm_emblem.png` / `core_emblem.png` (1024x1024, transparent, PREMULTIPLIED as RmlUi needs). Arm: steel ring,
  blue arrow rising; Core: steel gear, red hexagonal reactor. New designs, not the TA marks. Shapes are drawn at 4x
  and scaled down; edit the script and re-run rather than the PNGs. The old placeholder script is gone.
- Seeing the chooser in the engine: `VISUALPREGAME=1 VISUALSELECT=1 VISUAL=arm_commander run_win_visual.sh` (the
  harness script.txt sets skippregame=1; VISUALPREGAME drops it, the faction phase lasts 900 frames and screenshots
  start at 195).

## Unit brightness (2026-11-09)
- CUS GL4 `albedoFactor` uniform (defaultunit bin, `luarules/configs/cus_defs.lua`): multiplies the unit's base colour
  right after the texture read (`cus_gl4.frag.glsl`, after albedoColor), so lighting, specular, glow (tex2 red adds
  albedo again), team colour and damage shading all apply on top. `brightnessFactor` (1.6) instead scales the final
  colour. Live: `/luarules unitbrightness <0.25-3>`; Slate Graphics > Unit brightness (0.5-2, engine config
  TARUnitBrightness, read again when CUS initialises). Checked on the Windows engine at 1.0 vs 1.6.
- tex2 in TA:Recoil (OPTION_TEX2_SPECULAR): red = self-illumination, green = specular (-> metalness/roughness), blue
  ignored. Stock CUS GL4 reads blue as roughness.

## Alternating barrels: flip the gun index AFTER the recoil starts (2026-11-09)
- The engine runs `FireWeapon` up to its first Sleep/WaitFor, THEN calls `QueryWeapon` for the muzzle piece and
  spawns the shot (Weapon.cpp: FireWeapon at the top of the fire branch; Shot -> UpdateWeaponPieces -> Fire in the
  projectile loop). A script that flipped its gun index before the recoil (Hammer, Jethro, Spider: `gun = 1` then
  Move) made the shot leave the other barrel from the one recoiling. The flip now comes after the recoil has
  started (as the Thud always did). Rule for new scripts: pick the barrel from the index, animate it, yield, then
  flip.

## Maverick did not fire; Windows sweep (2026-11-09)
- Holstered, the Maverick's flares (QueryWeapon) sit below ground; a Cannon has no line of fire from there, so it never
  aimed, never drew its pistols and never fired (ground attack and enemies in range alike). QueryWeapon now returns the
  shoulder until drawn (same fix as the Peewee). The headless AIM probe reported it firing: do not trust it alone for
  "does it fire"; use the Windows engine.
- `VISUALENEMY=<unit> run_win_visual.sh`: an enemy in range of each unit, no orders (fire at will); the [VISUAL] frame
  lines give shots per unit (and src/ground heights, lof). Sweep 2026-11-09: all 68 armed land units (minus AA-only and
  stockpile weapons) fire on the Windows engine; builders (commanders) need VISUALENEMY, the ground-attack mode gives
  them a build order.

## Deferred lights crash (2026-11-09)
A 25-minute skirmish (Comet Catcher, vs AdaptiveAI) ended in an engine access violation inside the Deferred Lights
GL4 widget's "Unit Point Light VBO". Two faults, both from Splinter Faction / BAR code, lined up:
- **Enemy deaths leak.** The engine sends `UnitDestroyed` and `RenderUnitDestroyed` to a player's LuaUI only for the
  player's own ally team (EventHandler.h `CanReadAllyTeam`); `UnitLeftLos` only fires on a LOS change. An enemy that
  dies in view produces no event at all, so `api_unit_tracker_gl4` kept it in `visibleUnits` and every listener kept
  its instances (the per-unit glow lights, headlights, health bars) for a unit id that was gone or recycled. Visible
  as "Found invalid unit/featureID N ... while resizing" and "ZOMBIE instanceID" lines. Fix: the tracker sweeps
  `visibleUnits` / `alliedUnits` every 10 frames (`isValidLivingSeenUnit`) and also handles `RenderUnitDestroyed`.
- **The instance table corrupted itself when it compacted those dead entries.** `modules/graphics/instancevbotable.lua`
  (SF's copy, older than BAR's): `resizeInstanceVBOTable` copied each surviving element from its *new* index instead
  of its old one (all data shifted by one element per dropped entry), and `pushElementInstance` kept the write offset
  computed *before* the resize, so the new element landed past the compacted data and left a hole; `#instanceData`
  then stopped at the hole (6119 = 211 x 29 in the log), every later `Upload` threw "Invalid luaStartIndex", and
  since `popElementInstance` uploaded half-way through its bookkeeping, each failure left `usedElements` one too high
  ("nil element at the back of the array") until the engine crashed in the next upload. Fixes: both offsets (as BAR
  has since done), and `popElementInstance` now finishes all Lua bookkeeping before any GPU call, with the upload in a
  pcall (a failed upload leaves a stale light, never a broken table).
- Tests: `VBOPROBE=1 run.sh` (zz_vbo_probe: the module against a fake GPU buffer that checks bounds like
  LuaVBOImpl::Upload; `VBOPROBE=old_instancevbotable.lua` style paths test another copy) and, on the Windows engine,
  `VISUAL=<units> VISUALENEMY=core_t1_bot_ak VISUALSELECT=1 VISUALFRAMES=2400 LIGHTSPROBE=1 run_win_visual.sh`
  (zz_lights_probe widget: dead units still in the light buffers / tracker, every 60 frames; must stay 0). Result
  2026-11-09, 12 Core AKs killed by 12 Arm units: fixed code 86 -> 50 lights, 0 leaked throughout; the old tracker +
  module (control) kept all 86 with 36 leaked point lights, 12 leaked headlights and 12 dead units in the tracker.
  The run dir keeps the widget on/off state (LuaUI/Config/TART_data.lua); LIGHTSPROBE runs delete it so the lights
  widget is on, and need VISUALCFG with AllowDeferredMap/ModelRendering = 1.

## AI: AdaptiveAI / SimpleAI (2026-11-09, ported from Splinter Faction)
Files: `LuaAI.lua` (the AIs the lobby offers: AdaptiveAI, SimpleAI, SimpleDefenderAI, Sandbox),
`luarules/gadgets/ai_simpleai.lua` (core: classification, counters, ctx, team tick), `luarules/configs/simpleai/lib.lua`
(queries: build lists, targets, placement, bricks, reachability), `luarules/configs/simpleai/behaviors/*.lua` (b_adaptive
difficulty controller, b_defense intel, b_construction economy, b_commander, b_throttle, b_strategic nukes, b_combat waves
and raids, b_surrender). SF's b_morph / b_upgrades / b_economy (morphs, research points, build boost) are not ported: TA
has none of that. Modoptions (section AI): `adaptiveai_start` (0..1, 0.5 = plain SimpleAI; default 0.6 since 2026-11-09),
`adaptiveai_edge` (2026-11-09: how far ahead the AI steers to stay, 0.15 default, 0 = even; SF's controller aimed for the
player slightly ahead, +0.10, and eased twice as fast as it hardened; TA:Recoil's hardens twice as fast as it eases,
3-minute warmup, build-speed knob up to 1.5x), `ai_neverstall` (150 M/E floor;
AdaptiveAI always has it), `aitrace` (decision trace to the infolog every 10 s).

`validais.lua` (2026-11-09, like SF's) names the AIs a lobby may offer: AdaptiveAI, Simple*AI (SimpleAI and
SimpleDefenderAI) and Sandbox; the engine's BARb and CircuitAI know only Beyond All Reason's units and are left out.
What differs from SF's AI (see each file's header):
- Factions from the unit name prefix (`arm_` / `core_`); a unit's tier from its name (`_t1_`..`_t3_`); a team's tech
  level = the highest tier any finished builder of its own can build (a T1 constructor builds an Advanced lab, so it is
  tech 2 at once; the cost gate keeps the lab for later). Commanders: `customparams.iscommander`.
- Classes TA needs: IsShip (smClass 3; ships fight on their own like aircraft), IsAssistant (FARK, Necro, mine layers:
  builders with no useful build list; they repair / finish nanoframes / guard factories), IsSilo / IsAntiNuke
  (stockpile weapons) and IsLRPC (range > 2000) are "strategic", not turrets. Mexes are recognised by
  `customparams.metal_spot_mult` (extractsMetal is 0 here). TA builders make energy: classify builders before generators.
- Energy: `lib.EnergyOutput` (energyMake, negative energyUpkeep = solar, wind capped by average wind, tidal x strength).
  Energy is the TA bottleneck (every unit costs several times its metal in E): rung P2 is URGENT (right after the opening
  mexes) when the bank is under 35 % or stalling; power is ordered in batches of up to 3 small plants; a new factory
  needs 80 + 50/factory E income; storage waits for 6 mexes and a healthy bank; metal makers are built when E brims and
  M is short, switched off (CMD.ONOFF) in an energy stall and back on when E recovers (`mm.off`/`mm.on` trace keys).
- Metal: `lib.FindMexSpot` returns spot + the cheapest basic extractor the engine accepts there (land / underwater);
  mex expansion (P6) comes right after the first factory, above power and storage (TA maps have dozens of spots);
  `lib.FindMexUpgrade` + rung MOHO put a moho over a basic mex (unit_mex_upgrade.lua removes the mex).
- Rungs REP (repair hurt friendlies, nothing shooting at them), AS (finish an unattended nanoframe), FB.assist (guard the
  busiest factory; the commander always does when idle), 6a (one turret per factory floor), ST (b_strategic's wanted
  silo / anti-nuke), MM (metal makers). Every list a rung picks from is cut to what THIS builder can make (`Mine`), so no
  rung fails and eats the turn; picks are cost-gated (bank + 120 s of metal income; factories 300 s).
- Combat: role weights from the radar icon roles (gamedata/unit_icons.lua glyphs); AA units x3 while enemy air is
  about; paralyzer-only units capped. Commander: D-Gun any enemy in range when E >= 1.1 x the shot (b_commander).
- Sea: buildings with minWaterDepth > 0 and sea factories only when `lib.WaterNear(teamID)` (4 % of the survey cells
  within 3000 of home below sea level). Walls, mines and decoy commanders are never on a build list.
- The selector (b_construction SimpleConstructionProjectSelection) is at Lua 5.1's 60-upvalue limit: new constants go in
  the `TA` table (SF's go in STOR).

Testing: `AIPROBE=1 AIBOTH=1 AIFRAMES=14400 MAP=/mnt/e/EvoDev/xxxmaps/altair_crossing_v3.sd7 MAPNAME=Altair_Crossing_v3
KEEPLOG=out.log tools/headless-test/run.sh <engine> 1700` (AI on team 1, AIBOTH: both; the player spectates, or the
server never starts). zz_ai_probe runs at 60x, echoes [AIPROBE] per team every 1800 frames (units by class, resources,
kills, losses, what each factory is doing, what has been built) and the AI's own traces ([SimpleAI] team N f=...; r=
rung tallies). run.sh pre-sets TARInitialSettingsVersion in the write dir, or the loading screen's Initial Settings
addon restarts the engine. Headless runs about 1.5x real time with two AIs.
Opening (from the runs, Altair Crossing 1v1, both AdaptiveAI): 3 mexes, first factory ordered at 0:31 and standing at
0:47 (P5 fires with 600 metal banked even if the energy bank is low; urgent power then follows), one LLT per factory
(rung 6a, above mex expansion), mex expansion to 14 (P6), factories by income (FAC_BASE 1 + one per 7 M/s; a T1 lab
eats ~7 M/s flat out; plus 80 + 50/factory E income), storage only after 6 mexes. At 8 minutes: ~9-11 mexes, 2
factories, 4-5 constructors, 300-550 E/s, 20-24 M/s, 6-9 combat units built; raids and waves are running by then and
in one run Arm had killed Core's factory by minute 6. TA T1 labs are slow (vehicle plant: Stumpy 24 s, constructor
50 s), so production scales with factories and assist, not with the bank: a full bank means "build another factory".
Self-play result (final tuning, same map): Arm killed Core's commander at 7:03 with a commander hunt
(lib.FindCommanderTarget), 14 kills to 4; the game ends there (comends) and gadget:GameOver removes the AI, so the
winner idles afterwards in the probe. Energy storage is capped low (TECH_CEIL e), metal makers come early when energy
floats (rung MM above the defence floor), and once two factories stand the next factory a builder starts is an Advanced
lab if it can make one (TA.HasTier2Factory).
Known: the headless engine segfaulted twice in a worker thread (f=11671, f=16200; stripped traces; not reproducible with
the same seed) (stripped trace; not reproducible with the
same seed), so a crashed run is rerun before it is blamed on the AI. Rung tallies "stuck" and "unreach" are builders
whose orders failed (dropped after 30 s). Not done: LRPC (Berthas) are never built; ships only hunt the nearest
enemy; no hover/sea muster; SimpleConstructorAI is not offered; no play-testing against a human yet.
