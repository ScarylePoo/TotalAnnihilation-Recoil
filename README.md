# Total Annihilation: Recoil

**The 1997 classic, rebuilt for the Recoil engine.** Every Arm and Core unit from Total Annihilation, The Core
Contingency and Battle Tactics, with new models and animations, modern effects and an up-to-date interface. The
numbers underneath are still Total Annihilation's.

Arm and Core have fought for four thousand years over a galaxy that is now mostly rubble. Pick a side, put your
Commander down, and build the war machine that finishes it.

## What you get

- **266 units, Arm and Core.** Kbots, vehicles, hovercraft, ships, submarines, aircraft and seaplanes, defences,
  economy and the Krogoth, all from the original game and both expansions.
- **TA 3.1c balance.** Costs, build times, hit points, speeds, sight and radar ranges, and every weapon's range, reload,
  damage and area are taken from the Cavedog 3.1c data. TA's per-target damage tables are reproduced too: AA hits
  aircraft hard, the Immolator burns light units, the Stunner only stuns Core.
  The few places where the game deliberately differs from TA, and why, are listed in
  [tools/ta-data/DEVIATIONS.md](tools/ta-data/DEVIATIONS.md).
- **Every unit remodelled.** New high-detail S3O models and textures, made to read clearly from a top-down camera,
  with wrecks and scrap heaps to match.
- **New animations.** Lua unit scripts with proper walk cycles, aiming, recoil and launch sequences.
- **Modern effects.** Engine exhaust from each aircraft's real nozzles, missile trails, explosions, distortion and
  volumetric fog.
- **Aircraft that do what you tell them.** Bombers fly to where you send them and drop a full stream of bombs on each pass. An attack run on a target that ducks out of sight
  is finished on the last place you saw it.
- **A modern interface** (Slate): build menus, resource bar and economy graph, player list, chat, minimap, rebindable
  hotkeys and an options menu.
- **Skirmish AIs:** AdaptiveAI, which adjusts its difficulty to stay a step ahead of you, plus SimpleAI and
  SimpleDefenderAI.

## How to play

You need the [Recoil engine](https://github.com/beyond-all-reason/RecoilEngine). This release is built for
**Recoil 2026.09.01**.

**From a lobby:** in a Recoil lobby such as Coilbox, choose *Total Annihilation: Recoil* from the game list. The
lobby downloads it for you.

**By hand:**
1. Download the `.sdz` file from the latest
   [release](https://github.com/ScarylePoo/TotalAnnihilation-Recoil/releases/latest).
2. Put it in the `games` folder of your Recoil data directory.
3. Start a game from your lobby, with any map you like.

## Game options

The lobby's game options let you set:
- **How a game ends:** when a player's Commander dies, when every Commander on a team dies, or when every enemy unit
  is gone.
- **Economy and limits:** starting metal and energy (for each player or team), the unit limit, and diminishing returns
  on metal makers.
- **Rules:** a D-Gun that only works near your start position, ghosts of enemy buildings you have spotted, fixed
  alliances, and limits on game speed.
- **Unit movement:** speed, turn rate and acceleration of land and sea units, as a multiple of TA's.

## For developers

The game runs straight from a clone of this repository, so you can play the latest commit without building anything.
Clone it into your Recoil `games` folder as a `.sdd` directory, for example `games/TotalAnnihilation-Recoil.sdd`. A
checkout shows up as version `$VERSION`.

Layout:
- `units/`, `Weapons/`, `gamedata/` hold the unit and weapon definitions. `gamedata/alldefs_post.lua` applies the game-wide rules.
- `scripts/` holds the Lua unit animations. `objects3d/` and `unittextures/` hold the models and textures.
- `luarules/` holds the game logic gadgets, and `luaui/` holds the interface.
- `tools/` holds the toolchain:
  - `ta-data/`: TA 3.1c data extraction, armor classes and the deviation list.
  - `s3okit/`: model export and remodel tooling.
  - `headless-test/`: an automated headless test harness with probes for aiming, flight, water, AI and more.

**Releases** are built by GitHub Actions. Publish a GitHub release tagged with a version number such as `1.2.0`, and
the workflow attaches `TotalAnnihilation-Recoil_1.2.0.sdz` with that version stamped into `modinfo.lua`. The
repository itself always keeps `$VERSION`.

## Credits

- **Cavedog Entertainment**, for Total Annihilation, The Core Contingency and Battle Tactics: the units, the
  design and the war this game is about.
- **Scary le Poo**: project lead.
- Built using **BOTA** (Balanced Original Total Annihilation) as a starting point.
- **Splinter Faction** and **Beyond All Reason**, whose interface, effects, gadgets and hard-won Recoil know-how this
  game borrows from.
- The **Recoil engine** developers.

Total Annihilation is a trademark of its respective owners. This is a free, non-commercial fan project and is not
affiliated with or endorsed by them. Licence texts for the code and content are in [Licences/](Licences/).
