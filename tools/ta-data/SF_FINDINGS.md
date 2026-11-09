# Things found while porting Splinter Faction code into TA:Recoil

For whoever is working on Splinter Faction (SF). These are bugs or suspect spots noticed in SF files while
bringing them into TA:Recoil (2026-11). Each was confirmed in TA:Recoil's copy; whether it bites in SF depends
on SF's own layout, so each entry says what to check. File paths are SF's unless noted. Engine: Recoil 2026.09.01.

## Confirmed bugs (same code in SF)

1. **Auto team colours are invisible to enemies.** `game_auto_teamcolors` publishes the palette colours with
   ally-only rules params, so a player only sees the recoloured teams on their own side; enemies keep their lobby
   colours. Making the params public fixed it. Check: the `SetTeamRulesParam` / `SetGameRulesParam` calls in the
   synced half, their visibility argument.

2. **Unit lights never show (Deferred Lights GL4).** `api_unit_tracker_gl4.lua` loads at layer -828888, after
   `gfx_deferred_rendering_gl4.lua` (-99999990) and `gfx_distortion_gl4.lua` (-999999999). Both look for the
   tracker in `Initialize` and find nothing, so per-unit lights (and unit distortions) are silently off. Fix: give
   the tracker a lower layer than both (TA:Recoil uses -2000000000).

3. **Muzzle flames draw the whole sprite sheet as one quad.** The engine's `CBitmapMuzzleFlame` reads
   `animParams1` / `animParams2`, not `animParams`. 11 SF muzzle-flame CEGs set `animParams`, so the sheet is not
   animated and the full atlas tile is drawn flat. Fix: set `animParams1` (and `animParams2` for the second texture)
   in those `gamedata/explosions/*` files.

4. **`bitmaps/default/circles.tga` is 260x260.** The seismic/ground ring texture is not a power of two, which broke
   the groundFX atlas build in 2026.09.01 (error at load, ring missing). Resized to 256x256 here.

5. **Reclaim Field Highlight and Initial Settings load a font from the wrong folder.** `gui_reclaim_field_highlight`
   and `gui_initial_settings` ask for `fonts/Saira_SemiCondensed-SemiBold.ttf`. If that path is not in the archive
   (it was not in the files we copied), `gl.LoadFont` returns nil and every reclaim-field label errors on any map
   with wrecks. Check that `fonts/` actually ships the file in SF's build, or load it from where SF keeps its fonts.

6. **LUPS shield hit path is wired to a class that does not exist.** `lups_shield.lua` (ZK lineage) feeds
   `hitData` / `GetShieldHitPositions` to a LUPS class `ShieldSphereColorHQ` that SF's `lups/` does not have, and
   `lups_shield_fxs.lua` never sets the `shieldPos` / `shieldRadius` fields that path needs. At high quality this
   errors; `gfx_shields_gl4` draws the impacts anyway. Either add the class and fields or drop the HQ branch
   (TA:Recoil forces `highEnoughQuality = false` and always registers the sync action for the GL4 widget).

7. **`unit_plane_stop.lua` is unfinished.** It tracks no units (the table it reads is never filled) and the MoveCtrl
   freeze path never runs. Not ported.

8. **Enemy deaths leak out of `api_unit_tracker_gl4` (engine crash after ~20 minutes).** A player's LuaUI receives
   `UnitDestroyed` / `RenderUnitDestroyed` only for its own ally team (EventHandler.h, `CanReadAllyTeam`) and
   `UnitLeftLos` only on a LOS change, so an enemy that dies in view produces no event. The tracker keeps it in
   `visibleUnits`, and Deferred Lights, headlights, health bars keep their instances for a dead (later recycled) unit
   id: "Found invalid unit/featureID ... while resizing", "ZOMBIE instanceID" in the log. BAR's tracker has the same
   structure. Fix: sweep `visibleUnits` every few frames with `isValidLivingSeenUnit` (and handle
   `RenderUnitDestroyed`).

9. **`modules/graphics/instancevbotable.lua` corrupts itself when a resize drops dead entries.** SF's copy predates two
   BAR fixes: `resizeInstanceVBOTable` copies each surviving element from `new_usedElements * step` (its new place)
   instead of `(i - 1) * step` (its old place), and `pushElementInstance` keeps the `endOffset` it computed before the
   resize, so the new element is written past the compacted data and leaves a hole. From then on `#instanceData`
   stops at the hole, every `Upload` in `popElementInstance` throws "Invalid luaStartIndex", and because that upload
   happens half-way through the bookkeeping each failure leaves `usedElements` one too high ("We somehow have a nil
   element at the back of the array") until the engine access-violates in the next upload. Take BAR's current
   `instancevbotable.lua`, and consider finishing the Lua bookkeeping in `popElementInstance` before the GPU calls
   (TA:Recoil does, with the upload in a pcall). Together with the tracker leak above this is a guaranteed crash in any long game.

## Adaptive AI (SimpleAI Enhanced) findings

10. **Reclaim sends builders to the enemy base.** The single reclaim rung at the bottom of the chain area-reclaims
   around the nearest enemy position rather than around home or a wreck field. Since SF's economy leans on wrecks,
   this is worth a look. TA:Recoil replaced it with a wreck grid scan plus a small reclaim crew near home.

11. **A rung that picks something the builder cannot make eats the builder's turn, every tick.** Lists are per faction
   and tech; when a builder cannot build the picked def, the order fails silently and the selector does not fall
   through to the next rung, so that builder idles until the list changes. In SF most builders can build most of a
   list so it is rarer, but any builder with a narrow build list will show it. Fix: cut each list to the builder's
   own `buildOptions` before picking, and skip empty lists. Same for the factory `F.con` rung: when the factory
   cannot make a constructor it should fall through to combat production instead of failing each tick.

12. **No affordability check.** `TryBuild`-style picks take any def on the list; in a slower economy that is a Guardian
    or an advanced lab at minute three and the builder stands on it for ten minutes. Gating a pick to bank plus ~2
    minutes of income (and falling back to the cheapest) made a large difference here.

13. **`Spring.GetTeamStartPosition` used as "home".** Observed thousands of elmos from where the commander actually
    stood (depends on start-box handling). The team's first commander position is a safer anchor.

14. **The construction selector is at Lua 5.1's 60-upvalue limit.** `SimpleConstructionProjectSelection` in
    `b_construction.lua` hits "function has more than 60 upvalues" with one or two more locals captured. SF already
    keeps constants in `STOR` for this reason; anyone extending it will hit the wall at once. Worth bundling the
    remaining loose upvalues into a table now.

15. **Paralyzer-only units are counted as full combat strength.** `NonDirectClass` / role weights treat EMP-only
    units like damage dealers, so wave composition can be mostly stunners. (May be fine in SF if no such units
    exist; TA:Recoil caps them.)

## Deprecated API use (works today, warns or breaks later)

16. **`Spring.GetCommandQueue(unitID, 0)` in `unit_target_on_the_move.lua`**: deprecated form; use
    `Spring.GetUnitCommandCount(unitID)`.

17. **`KEYSYMS.*` in `gui_group_recall_fix`, `gui_con_locater`, `cmd_queue_copypasta`**: the KEYSYMS table is the old
    key-code path; `Spring.GetKeyCode("name")` is the current one and survives keyboard-layout changes.

18. **`gui_select_and_center.lua` only works in some camera modes.** It sets the camera state directly; using
    `Spring.SetCameraTarget` works in every camera mode.

## Rendering: worth checking rather than confirmed

19. **Custom Unit Shaders GL4 and classic texture2.** Stock CUS GL4 reads a unit's tex2 as PBR: red = emissive,
    green = metalness, blue = roughness. Classic Recoil/Spring tex2 is red = self-illumination, green =
    specular/reflectivity, blue unused (0). On such textures blue = 0 means roughness 0: every unit renders as a
    mirror and reads darker than before. TA:Recoil added an `OPTION_TEX2_SPECULAR` path (green drives both
    metalness x0.6 and roughness 0.9 - 1.4 x green) and raised `brightnessFactor` to 1.6 to compensate for the PBR
    darkening. If any SF models still use classic tex2 (older or borrowed assets), they will look wrong in the same
    way. Also useful: an `albedoFactor` uniform that scales the base colour before lighting, which is what people
    actually mean by "make the unit brighter" (`brightnessFactor` scales the lit result, glow included).

20. **Projectile texture atlas pages.** SF's own fix (Initial Settings sets `MaxTextureAtlasSizeX/Y = 8192`) is
    needed because ~41 megapixels of effect textures overflow a 4096 page, and effects spanning pages draw as flat
    rectangles. Still true in 2026.09.01; a player's very first match in multiplayer can still show rectangles
    because the config is written during loading and only single player reloads. Trimming the effect set or making
    the first-run write happen before the first match would remove the gap.

21. **Headless engine segfaults.** Running two Lua AIs headless at high speed, `spring-headless` 2026.09.01 crashed
    twice in a worker thread at different frames, not reproducible with the same seed. Looks like an engine issue
    rather than game code, but SF's headless CI would see it too.

## Not bugs, but differences you may want

- Stockpile limit: SF's gadget (BAR lineage) fills every new silo to the cap and replaces each fired missile.
  TA:Recoil caps the queue only.
- `unit_transportee_hider` hides cargo at `UnitLoaded`; crane-style transports (lift animation) make the unit vanish
  mid-lift.
- Set Target's default key Y collides with other binds in some layouts; TA:Recoil only binds it when Y is free.
