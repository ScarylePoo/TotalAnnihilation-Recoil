# HANDOFF: S3O remodel of the TA / Core Contingency / Battle Tactics units in XTA

Read this whole file before doing anything. It is written by me (Claude) for me in a new project. The user
is Scary le Poo (GitHub ScarylePoo), an experienced developer: be direct, no hand-holding.

## The job

Remodel and retexture every unit on the user's list (`unit_list_request.txt`, ~225 names: the original Total
Annihilation, Core Contingency and Battle Tactics units as they exist in XTA) as S3O, **including their wrecks**
(`_dead` models), plus a **generic scrap heap** representing a wreck pulverised into small broken bits (replaces
the TA `1x1a` ... `7x7d` heap models). The user sent S-Z later as an addendum; it is appended to
`unit_list_request.txt` and included in the manifest.

User's stated priorities:
1. **UV space efficiency is very important** so textures are the best quality possible.
2. **Contrast and shape**: units are viewed from fairly high up, so they must be recognisable at a glance.
3. Units keep working with their existing scripts (do not touch scripts unless asked) - **except walkers**, which
   get a new standard skeleton and a shared walk script (see "Walkers" below).

Game repo: `https://github.com/ScarylePoo/TotalAnnihilation-Recoil` (default branch **`main`**, no `master`). The user
owns it and the Claude GitHub app has push access. Attach it with `add_repo` (access `push`), clone with
`git clone --depth 1 https://github.com/ScarylePoo/totalannihilation-recoil /home/claude/totalannihilation-recoil` and a
~10 min timeout. **The kit lives in the repo at `tools/s3okit/kit/`** (this file is `tools/s3okit/`).
Splinter Faction (walk scripts, utilities to borrow): `git clone --depth 1 https://github.com/SplinterFaction/SplinterFaction
/home/claude/SplinterFaction` (2.2 GB, ~5 min). Work on **branches** and push them for
the user to test in game; do not push models straight to master unless asked. Commit messages explain the cause/why,
and end with the Co-Authored-By / Claude-Session lines the harness gives you. If git status says a pushed branch
has "no remote", it is the shallow clone's fetch refspec: `git config --add remote.origin.fetch
'+refs/heads/<b>:refs/remotes/origin/<b>' && git fetch && git branch -u origin/<b>`.

Already done: the Flash - regenerated with this kit (spec `units/arm_flash.py`, including its wreck), made in XTA as
`arm_flash.s3o` / `arm_flash_dead.s3o`; those files were carried into this repo's `objects3d/`. **Not wired up yet:**
`units/ARM_T1_VEH_Flash.lua` still points at BOTA's `ARM_T1_VEH_Flash.3do`. The BOTA Flash COB uses exactly the kit
Flash's 7 pieces (base, turret, sleeves, barrel1/2, flare1/2); BOTA's 3DO has an extra `sleeves2` the COB never turns,
so its second gun never elevates. To redo it under the new name: copy `arm_flash.py` to `ARM_T1_VEH_Flash.py` with
`ref` = `objects3d/arm_flash.3do` (XTA's model, still in the repo) or rebuild against BOTA's 3DO. After seeing it in game the user called the
contrast-reworked version "absolutely perfect": the current kit defaults (palettes, VALUE, readability rules) are
the approved look. A test heap (`2x2a`, size 2) was generated but not installed. A walker test
(`units/arm_peewee.py`: standard legs + original TA torso/arms as blockout) proves the skeleton path end to end.

## Setup in a fresh session

```
pip install --break-system-packages bpy lupa    # Blender 5.2 as a Python module (~5 min, Python 3.13) + Lua for the defs
python3 -c "import bpy, lupa, numpy, PIL, matplotlib, scipy"   # the others are usually present
cd /home/claude/totalannihilation-recoil/tools/s3okit/kit
python3 run.py inspect flash                    # smoke test (the repo is found from the kit's location; XTA_REPO overrides)
python3 make_manifest.py                        # regenerate manifest/ from the Lua defs
```
No Blender GUI: everything is headless `bpy`. Cycles CPU only (2 cores here): a final 2048 bake is ~5-8 min per
model, so iterate with `--draft` and do final bakes once per model. Run long jobs with `run_in_background`.

## Repo layout (BOTA base, since 2026-10-25) - what the kit reads

The repo moved from XTA guts to the BOTA mod, renamed for findability, and every FBI/TDF became Lua (the SF way).
- **Names**: `<SIDE>_<TIER>_<CLASS>_<Name>` file stems, e.g. `ARM_T1_VEH_Flash`, `CORE_T2_BOT_Necro`, `ARM_Commander`.
  Classes: AIR BOT VEH HOV SEA SEAPL (seaplanes) LAB DEF ECO SEADEF SEAECO. **The stem is the kit's canonical unit
  name**: spec `units/<stem>.py`, `work/<stem>/`, outputs `<stem>.s3o`, `<stem>_1.png`, `<stem>_2.png`. Every command
  accepts any case, the def key or the display name (`run.py inspect flash`) and resolves it to the stem.
- **Unit defs**: `units/<stem>.lua` (`return { <key> = { objectname = "<stem>", corpse = "<stem>_dead", ... } }`),
  build lists via `Shared.buildList*` from `gamedata/unitdefs_pre.lua`. Read with `lupa` in a sandbox
  (`s3okit/xta.py: load_lua_defs`; unknown globals such as `Shared` become nil-like).
- **Features**: `Features/Corpses/<stem>_dead.lua` holds `<key>_dead` (object `<stem>_dead`) and `<key>_heap`
  (object `2x2c` etc.). Only one unit-specific level-2 wreck is left: `ARM_T2_DEF_Ambusher_dead2`.
- **Scripts**: 222 units have compiled `scripts/<stem>.COB` with **no BOS sources**; 44 (defences, eco, mines...) have
  Lua unit scripts `scripts/<stem>.lua`. `s3okit/cob.py` disassembles COB (opcodes/operand counts from Recoil's
  `CobOpCodes.h`/`CobThread.cpp`; validated on all 223 COBs, some have dead data after the last `return`) and
  `xta.script_summary` gives the same per-piece usage report for COB and LUS. Checked: no script references a piece its
  model lacks (all 266 units). To port a COB's logic to LUS, read `cob.read(path)['scripts']` (instruction lists).
- **Install** (`run.py install`): copies into `objects3d/` and `unittextures/`, sets `objectname = "<stem>.s3o"` in the
  unit Lua and `object = "<x>.s3o"` in the corpse's feature table (explicit extension: without it the engine picks
  .3do/.s3o arbitrarily). `install-heap` rewrites every `object = "<heap>"` under `Features/`.
- Data-format notes for the whole repo (engine fixes, Lua conversions, headless test): project doc
  `claude/recoil-compat-notes.md`.

## Kit layout

```
run.py                 CLI (stages below)
make_manifest.py       user's list -> unit defs/models/scripts/corpse chains -> manifest/manifest.{md,json}
s3okit/common.py       paths, MATS (material slots)
s3okit/threedo.py      3DO reader (engine coords), bbox, real faces, TA texture -> material guess
s3okit/geom.py         Unit/Builder modelling API, visibility culling, UV unwrap/pack, mirrors, clones, shading
s3okit/bake.py         Cycles emission bakes of helper maps -> .npz
s3okit/compose.py      numpy texture synthesis from the maps; faction PALETTES; unit / wreck / heap modes
s3okit/s3o.py          S3O writer (emit vertices preserved) and reader
s3okit/wreck.py        corpse generator from the built unit (level 1 = _dead, level 2 = unit-specific _dead2)
s3okit/heap.py         generic scrap heap generator (per footprint size + seed)
s3okit/preview.py      renders the exported S3O (via our own reader) + RTS-height readability thumbnail
s3okit/xta.py          Lua unit/feature def reading (lupa), script piece usage (COB/LUS), install (Lua edits)
s3okit/cob.py          compiled COB reader/disassembler (pieces, scripts, per-piece usage)
units/<unitname>.py    one spec per unit (arm_flash.py is the worked example)
work/<unitname>/       unit.blend, maps.npz, out/ (s3o + pngs), prev/ (renders, uv_layout.png), build_report.json
```

## Commands

```
python3 run.py inspect <unitname>     # prints unitdef essentials, corpse chain, piece table (engine coords),
                                      # what the BOS does to each piece; writes work/<u>/prev/ref3do.png;
                                      # scaffolds units/<u>.py (blockout = original TA polygons) if missing
python3 run.py build <u> [--draft]    # spec -> cull hidden faces -> unwrap/pack -> mirrors/clones -> unit.blend
python3 run.py bake <u> [--draft]     # helper maps (id, pos, nrm, edge, ao near/far) at bake_res
python3 run.py compose <u>            # -> out/<u>_1.png, out/<u>_2.png at res
python3 run.py export <u>             # -> out/<u>.s3o
python3 run.py wreck <u> [--draft]    # -> out/<corpse>.s3o (+ level 2 if the chain has a unit-specific _dead2)
python3 run.py preview <u>            # -> prev/sheet.png (views + colour/grey thumbnail top-right)
python3 run.py all <u> [--draft]      # all of the above in order
python3 run.py heap 2x2a --size 2 --seed 3   # generic heap model named exactly like the TA heap it replaces
python3 run.py install <u>            # copy out/ into repo, unit Lua objectname="<stem>.s3o", corpse object="<x>.s3o"
python3 run.py install-heap 2x2a      # copy + rewrite every `object = "2x2a"` under Features/ to "2x2a.s3o"
```
Always look at `prev/sheet.png` and `prev/uv_layout.png` (Read tool) before installing. Send the user the sheet.

## Per-unit workflow

1. `inspect`. Read the reference sheet and the piece/script table. Note: pivots (piece origins), what turns/moves
   on which axis and how far (recoil distances!), which pieces are hidden/shown (nano lathes, build plates,
   folded wings), and which pieces are emit points (flares, nano points, smoke points).
2. Write `units/<u>.py` (start from the scaffold or copy a similar unit). Keep every piece name, its origin and the
   hierarchy exactly as the 3DO (the kit reads them from the 3DO; you only add geometry to pieces). Empty pieces stay
   empty. Model each piece's geometry around its own origin so rotations look right.
3. `build --draft` -> check `build_report.json` (tris, uv_coverage, culled faces; `mirror_asymmetry` and `script_pieces_missing` must be
   empty) and `uv_layout.png`. Then `bake --draft`, `compose`, `export`, `preview`. Iterate on shape first.
4. Final: `all <u>` (final bakes). Check the sheet again. `install <u>`, commit on a branch, push, tell the user.
   Batch several units per branch once the user is happy with the look.

## Modelling API (geom.py)

Coordinates are **engine coordinates, global** (X right, Y up, Z forward = the direction the unit drives/faces).
`k.P[name]` is a piece's global origin; `b = k.piece(name)`; `b.at(x, y, z)` converts piece-relative to global.
Shapes: `hull(points)` (convex hull - the workhorse), `box(lo, hi)`, `prism(x0, x1, [(z, y), ...])` (side profile
extruded along X), `plan(y0, y1, [(x, z), ...], top_inset=)` (plan outline extruded up with sloped sides),
`cyl(p0, p1, r, segs, r2=, rot=)`, `sphere(c, r, scale=)`, `from_3do(piece, mat=)` (original TA polygons).
Common options: `mat` (see materials), `bevel` (chamfer width; 0.05-0.15 typical; it is what catches light and
gives the edge-wear mask something to find), `seg`, `mirror=True`.
- **mirror=True** builds the given part on one side and a mirrored twin across global X=0 that **shares the same
  UV space** (halves texture use for symmetric units). Only on pieces whose origin x == 0. Never on a part that
  crosses x = 0 (build those whole, unmirrored). Asymmetric details (antennae, single hatches) unmirrored.
- **k.clone('barrel2', 'barrel1', mirror_x=False)** gives a piece the same local geometry AND UVs as another
  (identical barrels, legs, wheels as separate pieces). `mirror_x=True` for left/right handed copies.
- Convex hulls: anything concave = several hulls. `dissolve_limit` merges coplanar triangles before bevelling.

## Materials (common.MATS) and what compose does with them

`paint` faction camo + panel seams/rivets + edge wear | `paint2` secondary solid tone (use for big contrasting
masses: decks, armour bands - helps reading from above) | `dark` gunmetal mechanical parts | `tread` tracks (link
pattern from Z position) | `steel` barrels/pistons, brushed, reflective | `team` team colour (tex1 alpha 0.9) |
`lightw` / `lightc` / `lightr` self-illuminated lights (white / cyan / red; Core palette shifts these warmer) |
`black` bores, grilles | `hazard` faction accent with diagonal warning stripes | `glass` canopies |
`rust`, `ash` (wrecks/heaps).

Palettes live in `compose.PALETTES`: **ARM** = cool light blue-grey 3-tone camo, hazard yellow; **CORE** = warm dark
gunmetal, ochre/orange accent, warmer lights; **SCRAP** = neutral for heaps. The factions must separate at a glance
(Arm light/cool, Core dark/warm). Tweak there, not per unit; per-unit overrides would need a new parameter.

## Readability rules (user priority 2) - learned from the user's in-game screenshot

At normal zoom a 2x2 unit is only ~30-35 px wide on a 2000 px screen. The first Flash (light camo, thin team
stripes, thin guns) read as a single blue-grey lozenge; camo, panel seams and rivets average away completely.
The user stressed this: similar colours blend at distance, so **contrast between areas is what matters**.
- Value comes from big blocks, not texture detail. Plan each unit as 3-4 value groups seen from above: light
  main armour (`paint`), dark recesses/secondary masses (`paint2`: lower decks, gun pods, engine decks, joints),
  near-black mechanics (`dark`, `tread`, `black`), and team colour.
- compose.VALUE paints lighting in: tops x1.12, sides x0.72, undersides x0.45, light rims on convex edges, strong
  crevice AO, weak seams (0.22), team alpha 0.97. Camo tones are deliberately close together (texture interest
  up close, no mush at distance). Tune these globally, not per unit.
- Team colour: wide flat bands/plates on top-facing surfaces, ~15-25 % of the top view (Flash: fender bands
  2.5 elmo wide, turret roof, gun-pod tops). Side-only team colour is invisible from the game camera.
- Silhouette: guns, legs, wings, masts exaggerated in thickness (Flash barrels went 0.34 -> 0.46 radius) and kept
  dark against light armour (or light against dark for Core).
- No detail below ~0.4 elmo except lights.
- **Check `prev/sheet.png` top-right**: the game-distance render (camera 430 elmos away, 65 deg pitch, sandy
  ground, NOT scaled to the model: big units should look big), enlarged 3x with nearest-neighbour, in colour and
  greyscale. If the unit's parts don't separate in the greyscale one, fix value blocks before anything else.
  `examples/flash_distance_before_after.png` shows the change on the Flash.

## UV efficiency (user priority 1) - what the kit does

1. `visibility_cull`: deletes faces buried inside their own piece's solids (rays from the centre AND near every
   corner mostly hit back faces) and flat undersides sitting on the ground (land units only); `ash` is never
   culled. Records each face's sky exposure.
2. Smart UV project (55°), `average_islands_scale` (uniform texel density), then `split_poor_islands` cuts islands
   with fill < 45 % (chamfer rings, slivers) into per-face islands laid flat along their longest edge.
3. Importance scaling: islands shrink by low exposure (hidden-ish faces), downward-facing (land units), and material
   (`tread` 0.6, `black` 0.4, ...). Tune `geom.IMPORTANCE` and the curve in `unwrap`.
4. Minimum island size: islands are grown so their long side reaches `MIN_PX` (6) texels and short side
   `MIN_PX_THIN` (2.5) at the final resolution (an island smaller than a texel gets no baked texels and shows
   its neighbours' colours).
5. Pack: concave shapes, any rotation, 3 px margin at the final resolution (bake at 2x then downsample).
6. Mirrors and clones are added after packing, so they cost no UV space.
Result on the Flash: plain smart-project + pack covered 43 % of the texture; the kit gets ~63-67 %, with mirroring
and the barrel clone on top (~1.3x more effective density). Scrap heap: ~71 %.
Further ideas if wanted: a second packing pass with `pack_islands(merge_overlap=True)`, grouping tiny islands of
uniform materials (black/dark bolts) into a shared swatch, unit-family texture atlases.

## Engine facts (verified in the Recoil source; do not re-derive)

- The engine loads 3DO with **Z negated** (`3DOParser.cpp`: `v.z = -v.z`, `offset.z = -Z`), scale 1/65536.
  The kit writes S3O in the same engine frame, so piece offsets copied from the 3DO keep COB scripts working
  unchanged (turns, moves, recoil, explode). COB axis handling is the same for 3DO and S3O.
- S3O: triangles (primitiveType 0); winding with `cross(b-a, c-a)` along the normal (CCW, as Blender);
  `texv = 1 - v` for PNG (non-DDS loads with upper-left origin, `Bitmap.cpp`). DDS has its own flip: keep PNG.
- Textures: tex1 RGB diffuse, **A = team colour** mixed before lighting; tex2 **R = self-illum, G = reflectivity**
  (`specular *= G*4`, reflection mix by G), B unused, **A must be 255** (it is the one-bit transparency mask).
  `ModelFragProg.glsl`. XTA has no custom unit shader; the engine default applies.
- **Emit points**: `S3DModelPiece::GetEmitPos/Dir`: 0 verts -> pos 0, dir +Z; 1 vert -> pos 0, dir v0; 2+ -> pos v0,
  dir v1-v0. 3DO is the same. Weapons fire from and `emit-sfx` uses these. The exporter prepends the 3DO piece's
  first vertices (unreferenced by triangles) to every piece so behaviour matches the original exactly.
- Feature defs use `object = "name"` **without extension**; the engine then picks whichever registered format it
  finds first (map order, effectively arbitrary). `install` therefore writes `object = "<name>.s3o"` explicitly, and
  the unit def gets `objectname = "<stem>.s3o"`. The old .3do files can stay.
- PIL resizes RGBA premultiplied: resizing a team-colour texture blackens RGB where alpha = 0. compose resizes
  channels separately - keep it that way.
- Bake AO uses `only_local` so moving pieces don't bake shadows onto each other.
- **Never bake with a Cycles margin when several objects share one image**: each object's margin is painted
  over the other objects' texels (cost me a scrambled texture: treads came out as turret paint). bake.py bakes
  with margin 0 and compose.py dilates with scipy's distance transform from the coverage mask.
- bmesh `bevel` replaces the faces it bevels and only copies their data: tag material/mirror flags *before*
  bevelling (geom.py does). Anything you add to Builder must follow that.
- `dissolve_limit`'s `region` output contains only the faces it merged; hull triangles it did not touch are
  separate. Builder.hull tags both (a past bug left some hull triangles as default `paint`, unmirrored).
  After any Builder change, check per-material/per-mirror face counts are symmetric (sides 1 and 2 equal).
- Overlay plates/decals (team stripes, hazard plates) must sit >= 0.05 elmo above the surface they cover, or they
  z-fight differently on the two mirrored sides.

## Walkers (user requirement, 2026-10-24) - READ BEFORE ANY LEGGED UNIT

The user's words: "If you make them with the pieces that they have now and the walk animations that they have
now it's going to look dumb." All legged units get a **uniform piece hierarchy** so ONE walk script drives every
biped and ONE drives every quadruped, and **backwards (digitigrade) legs like Splinter Faction's Federation
walkers**.

- **Bipeds** (exactly the user's hierarchy):
  ```
  pelvis
  └ legs
    ├ rthigh └ rleg └ rfoot
    └ lthigh └ lleg └ lfoot
  ```
  `r` is the -X side (as in SF). Everything else of the unit (torso, arms, guns, flares, head...) hangs off
  `pelvis` (or off the new leg piece if it used to hang off an old leg).
- **Quadrupeds** (names confirmed by the user): `pelvis > legs > {rf,lf,rb,lb}thigh > ..leg > ..foot`
  (f = front, b = back, r = -X side).
- **6-legged units (Roach, Scarab) keep their legs, like the Spider** (user's decision): same style of hierarchy.
- **Exceptions**: **The Can and the Sumo
  get tracks, not legs** (tracked lower hull; their scripts must change too). The Sumo was missing from the list
  by accident; the user confirmed it is in scope (added to `unit_list_request.txt`).
- **Proportions = SF Federation rig, scaled by pelvis height H** (measured from fedbear/fedgoliath/fedstriker):
  legs = pelvis + (0, -0.013H, 0); thigh = legs + (+-hipx, 0, 0); knee (`leg` piece) = thigh + (0, -0.32H, -0.325H)
  i.e. BEHIND the hip; ankle (`foot` piece) = knee + (0, -0.49H, +0.49H), ending ~0.17H above ground. SF's shared
  walk is keyframed on that rig, so identical ratios are what lets one script fit every walker. Fed walkers use
  hipx ~ 0.66H; the kit defaults hipx to the TA model's thigh spacing (override with `skeleton_opts`).
- **SF reference** (clone `https://github.com/SplinterFaction/SplinterFaction`, sparse): Lua unit scripts, e.g.
  `Scripts/fed/hbot/fedbear_lus.lua`, call `common.WalkScript()` from `Scripts/headers/common_includes_lus.lua`
  (generated with Beherith's Skeletor_S3O from `2_legged_walk_animation_vb1.blend`); it animates pelvis
  (y bob, x/y sway), `lthigh/lleg/lfoot`, `rthigh/rleg/rfoot` (x/y/z turns). Models: `Objects3D/fed*.s3o`.
  SF also has a `dirt` emit piece at ground level under pelvis; not in the user's hierarchy - don't add unless asked.

**Kit support** (`s3okit/skeleton.py`):
- `UNIT = dict(skeleton='biped' | 'quad', skeleton_opts=dict(height=H, hipx=..., hipz=..., drop=[...], keep=[...]))`.
  The original model's leg pieces are dropped (name match: thigh/leg/shin/calf/knee/foot/boot/toe/hip, minus
  flare/gun/barrel/...), the standard skeleton is generated, all other pieces keep their global position and are
  re-parented. H defaults to the original `pelvis` height.
- `k.standard_legs(thigh=, shin=, foot=, joint=, width=1.4, armour=True)` builds a Fed-style leg once and clones it
  to every other leg (mirrored for the left side), so ALL legs share one UV set. Customise per unit by building the
  leg pieces yourself instead (build `r*`/`rf*` pieces, then `k.clone` the rest).
- `inspect` detects legged models, prints the remap (dropped / re-parented pieces) and writes the scaffold with
  `skeleton=` and `k.standard_legs()`. Its biped/quad guess is a heuristic - check the reference sheet.
- `build` saves the final piece table to `work/<u>/pieces.json` and the remap to `build_report.json['skeleton']`;
  export and wreck use pieces.json (never re-read the reference model for walkers).
- `manifest/manifest.md` has a "Legged units" table (heuristic: e.g. Solar Collector/Geothermal "legs" are
  structure, not walkers; Talon/Lost units slipped in where they share a name).

**Scripts (decided): walkers get Lua unit scripts (LUS)**, SF style: one `<unit>_lus.lua` per walker plus one
shared walk include for bipeds and one for quads. Port each unit's weapon/aim/build logic from its COB (no BOS sources in this repo:
disassemble with `s3okit/cob.py`; weapon and aim piece names are kept, so it maps across) and point the unitdef at the
new script. The user answered "yes lus" to "LUS, and will you write the walk or port SF's?": the format is settled;
confirm who writes the shared walk at the first walker. Default plan: port SF's `common.WalkScript` (it already
matches the skeleton proportions) and derive the quad walk from it.

## Flare pieces (user requirement, 2026-10-25)

Many TA 3DOs have "flare" pieces (`flare`, `flare1`, `lfire`, `rfire`, `muzzle`...) carrying polygons that in 1998
stood in for the muzzle flash (scripts `show` them for a frame when firing). **That geometry is removed: never
model or keep it.** The muzzle flash is the weapon's CEG/explosion generator.
- Keep the **piece itself** (empty): scripts query it (`QueryWeapon`/`AimFrom`), `emit-sfx` from it, and
  hide/show it. Deleting the piece breaks the script.
- The exporter still prepends the 3DO piece's first two vertices as unreferenced emit vertices, so the weapon's
  fire position and direction stay exactly what the game used (no visible geometry).
- `inspect` lists flare pieces that have polygons and leaves them out of the scaffold; just never call
  `from_3do()` or build shapes on them. Show/hide calls on them in the old scripts become harmless; drop them
  when porting a script to LUS.
- Flare-like pieces on unit bodies that are real geometry (rare, e.g. a gun named `*fire*`) are the exception:
  check the reference sheet before discarding.

## Wrecks and heaps

Corpse chain per unit (from fbi `corpse=` and tdf `featuredead=`): unit -> `<u>_dead` (level-1 wreck, our S3O) ->
heap. Heaps are the generic `NxN?` models (1x1a ... 7x7d, 30 referenced incl. 4x4f), plus one unit-specific level-2
wreck, `ARM_T2_DEF_Ambusher_dead2` (made by `run.py wreck`). `rock_teeth` is left alone.
- `wreck.make`: poses turret/guns, drops `drop` pieces beside the hull, removes `remove`, deletes some small loose
  parts, jitters others, crumples, dents, punches a few holes, tilts and sinks. Same UVs as the unit, rebaked,
  burnt texture (no team colour, no lights) at `wreck_res` = res/2. Spec: `UNIT['wreck'] = dict(seed, pose, drop, remove)`.
- `heap.make(size, seed)`: scorched ash mound + broken plates, beams, pipes, chunks, wheels, bent panels.
  Generate each TA heap name with its footprint size: `heap 3x3c --size 3 --seed 3` etc. (the letter variants = seeds).

## Manifest

`manifest/manifest.md` maps every requested name to unit file stems, model, piece count, script, corpse model and
heap; it also lists **unit defs no request names**. Notes (2026-10-25, BOTA base):
- 223 of 227 requests match 254 defs / 228 distinct models. Aliases for BOTA display names are in `make_manifest.py`
  (Fusion Reactor = ARM fusion, Cloakable Fusion Reactor, Mobile Artillery = Pillager, Resurrection Kbot = Necro,
  Defender - NS = ARM_T1_SEADEF_Defender, L.L.T).
- Unmatched, not in BOTA: Galactic Gate, Implosion Device, Scorpion, Sea Serpent.
- Unrequested BOTA units (the S-Z addendum stops short): Warrior, Swatter, Wombat, Tornado, Turtle, Typhoon, Voodoo,
  Thunderbolt, Viper, Vulcan, Stunner, Toaster, Vulture, Voyeur, both Targeting Facilities, both Decoy commanders,
  underwater energy/metal storages, extractors and fusion plants, and 12 mines. Ask the user whether they are in scope.
- Several names map to an Arm and a Core def (Shipyard, Metal Extractor, ...): both need models.
- Count distinct models, not names, when estimating work: many units share wrecks/heaps.

## Timings (2-core container)

build ~10 s; draft bake (1024, low samples) ~30 s; final bake (2048) ~7.5 min; compose ~20 s; preview ~1-2 min;
heap draft ~1.5 min. Budget ~12-15 min of machine time per finished unit + wreck, plus the modelling.

## Decisions (2026-10-25, user)

- **Scope**: every BOTA unit (266 defs), including the ones the request list missed (Warrior, Swatter, Wombat, Tornado,
  Turtle, Typhoon, Voodoo, Thunderbolt, Viper, Vulcan, Stunner, Toaster, Vulture, Voyeur, Targeting Facilities, Decoy
  commanders, underwater eco, mines). **Third-party S3O remodels are redone too** (model to their piece layout: the
  COB drives those pieces).
- **Textures: DDS**, per unit (`<stem>_1.dds` DXT5, `<stem>_2.dds` DXT1, full mips, written unflipped; S3O UVs unflipped).
  A per-side atlas (user allowed up to 8192^2) was considered and rejected: one 8192^2 = 67 M texels vs ~348 M per side
  for per-unit 1024/2048 textures + wrecks, i.e. ~1/5 of the planned detail. Revisit only for per-family atlases.
- **Core palette** settled on the Instigator: warm dark gunmetal (~35 % value), light steel guns, ochre hazard.
- Commit to the repo at intervals (per unit or small batch) so work is never lost.

## Batch workflow (one agent per family, each on its own branch)

Branches: the shared base is `s3o-remodel` (kit + Flash + Instigator). Each family batch works on
`s3o-<family>` (e.g. `s3o-t1-veh`) created from `origin/s3o-remodel`, commits **after every finished unit** (spec +
installed files) and pushes at least every few units. The coordinator merges family branches into `s3o-remodel`.
Do not change kit-wide look parameters (`compose.PALETTES`, `VALUE`, `REFLECT`, `geom.IMPORTANCE`): propose changes in
the report instead. Kit bug fixes are fine if small, isolated and explained in the commit message.

Per unit:
1. `python3 run.py inspect <stem>`; Read `work/<stem>/prev/ref3do.png`; note the script piece table (what turns/moves,
   hide/show frames, emit/query pieces).
2. Write `units/<stem>.py` (copy the closest finished spec: `ARM_T1_VEH_Flash.py` = Arm vehicle,
   `CORE_T1_VEH_Instigator.py` = Core vehicle with frame-cycled tracks). Keep every piece and origin; geometry around
   each piece's own origin; flare/firepoint pieces stay empty. Readability rules above are the quality bar.
3. `build --draft`: `mirror_asymmetry` and `script_pieces_missing` must be empty; Read `prev/uv_layout.png`.
4. `bake --draft`, `compose`, `export`, `preview`; Read `prev/sheet.png`. Fix shape/value problems; the greyscale
   thumbnail must separate into 3-4 value blocks + team colour.
5. `all <stem>` (final). Read the sheet again (including the wreck view). `install <stem>`. Commit:
   `units/<stem>.py`, `objects3d/<stem>*.s3o`, `unittextures/<stem>*.dds`, `units/<stem>.lua`, the corpse feature Lua.
   Never commit `work/` or PNGs.
Skip legged walkers (standard skeleton + LUS walk: handled separately, see "Walkers"), but do the Spider/Roach/Scarab
only if told to. Air units: `air` is automatic from `canfly`. Ships/hovers: check `floater`/`waterline`; underwater
parts are seen from above through water. Report at the end: units done, units skipped and why, problems, proposals.

## Suggested order of work

1. Get the user's in-game verdict on the Flash; adjust the kit globally.
2. Do one Core unit early (e.g. Core's counterpart tank, the Instigator `core_instigator`) to settle the CORE palette.
3. Then by family so specs can be copied: T1 vehicles, T1 kbots, aircraft (set `air`), ships/hovers (check
   `floater`/`waterline`; underwater parts are seen from above through water), T2 of each, buildings/factories
   (big footprints -> 2048 textures; nano/build pieces from the BOS), then defences, economy, experimentals.
4. Heaps once (29 models, `heap <name> --size N --seed <letter index>`), installed with `install-heap`.
5. One branch per batch (e.g. `s3o-arm-t1-vehicles`), pushed for the user to test; merge only when they say so.
Regenerate the manifest after pulling: `python3 make_manifest.py $XTA_REPO unit_list_request.txt manifest`.

## Units that are already S3O

Some units already use third-party S3O remodels (MRD/Smoth/ZK/CA carried over from XTA, renamed: e.g.
`CORE_T1_VEH_Instigator.s3o`, `CORE_T1_VEH_Raider.s3o`, `CORE_T2_VEH_Goliath.s3o`, `ARM_T1_ECO_SolarCollector.s3o`;
34 S3O files in `objects3d/`, the manifest's model column shows them). The kit uses whatever model the unitdef
points at as the reference (`threedo.load_any` reads .3do and .s3o), because the script was written against that
model's pieces. Those remodels can differ from the TA layout, e.g. the Instigator animates its treads by cycling
`tracks1..4` with hide/show: every such frame piece needs its own geometry (vary the tread texture per frame by
offsetting the link pattern, or by small geometry shifts). Ask the user whether these already-remodelled units
should be redone too, or skipped.

## Open questions to ask the user when relevant

- Texture format/size budget: PNG 1024 RGBA is ~1-2 MB each; ~250 units x (2 + wreck 2) textures adds a lot to the
  repo. Options: DDS (BC3/BC1 with mips, smaller + faster loading, but mind the DDS flip), or per-family atlases.
- Walkers: who writes the shared walk (default: port SF's), The Can / Sumo tracked layout and their new scripts.
- Whether the already-S3O third-party remodels are redone with the kit (recommended: one look) or skipped.
- Whether the unrequested BOTA units (see Manifest) are in scope.
- 6-legged units (Spider, Roach, Scarab) now get "the same style of hierarchy" (user's edit of this file): agree the
  hexapod piece names (e.g. `pelvis > legs > {rf,lf,rm,lm,rb,lb}thigh > ..leg > ..foot`) and whether one shared
  hexapod walk drives all three, before the first of them.
