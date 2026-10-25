# Slate

A game-neutral in-game interface for Total Annihilation style games on the
Recoil engine, drawn with the engine's RmlUi: dark translucent panels with
soft corners, no faction styling, an optional colour tint. Derived from the
Bastion HUD in Splinter Faction (same author, GPL v2 or later).

## What is in it

Everything Slate needs is in this one folder (`luaui/slate/`). Nothing in it
names the game it sits in.

| Path | Purpose |
|---|---|
| `widgets/slate_api_core.lua` | Loads the two config files, keeps the player's settings (engine config `slate_*`), builds the tint rules, and publishes `WG.Slate` |
| `widgets/slate_api_layout.lua` | Tweak mode (Ctrl+F11): drag panels; positions are saved and resolution-independent |
| `widgets/slate_api_keybindings.lua` | Applies the per-game key files (see below) and `/slatekeys` |
| `widgets/slate_resourcebar.lua` | Metal and energy with storage, income, drain and a draggable share level; wind and tidal read-outs at the right end |
| `widgets/slate_commands.lua` | Build grid (category filters, paging, queue counts, hotkeys) and the order and state buttons; replaces the engine's menu |
| `widgets/slate_selection.lua` | Selected unit or group, unit under the cursor, build/order descriptions; replaces the engine tooltip |
| `widgets/slate_playerslist.lua` | Every player by alliance: resources, cpu/ping, fps; spectators; click an ally to share, or as a spectator click a player to follow their camera |
| `widgets/slate_broadcast.lua` | Sends your fps, system and camera to other players' Slate (needed for the fps column and camera following) |
| `widgets/slate_chat.lua` | On-screen chat with team-coloured names and a colour per channel |
| `widgets/slate_log.lua` | Scrollback window with Chat / Console / All tabs |
| `widgets/slate_menu.lua` | The MENU handle: settings, graphs, share, log, key bindings, widgets, pause, resign, quit |
| `widgets/slate_minimap.lua` | Frames the engine minimap top left; size from the settings |
| `widgets/slate_options.lua` | Settings window (F10): interface, graphics, sound; tabs are data files in `configs/options/` |
| `widgets/slate_widgetselector.lua` | Widget list (F11) |
| `widgets/slate_econgraph.lua` | Where metal or energy is going, over time |
| `widgets/slate_endgraph.lua` | End-of-game statistics, a line per team; replaces the engine's |
| `widgets/slate_ecostats.lua` | Spectators only: every team's economy side by side with alliance totals |
| `widgets/slate_keybinds.lua` | See and change key bindings; changes go to a per-game file |
| `widgets/slate_hotbind.lua` | Hover a build or order button, Ctrl+Insert binds a key to it, Ctrl+Delete removes it |
| `widgets/slate_select.lua` | The `slateselect` action used by custom selection binds |
| `widgets/slate_share.lua` | Give resources or selected units to an ally (H) |
| `widgets/slate_pause.lua` | Pause overlay |
| `widgets/slate_vote.lua` | Vote panel |
| `widgets/slate_replay.lua` | Replay speed buttons under the resource bar |
| `widgets/slate_desync.lua` | Desync alert |
| `widgets/slate_music.lua` | Music player (tracks under `music/<artist>/`); controls in the menu and settings |
| `widgets/slate_factionchooser.lua` | Pregame faction choice; needs a game-side gadget (see the file header), inactive otherwise |
| `widgets/slate_ranks.lua` | Cosmetic rank tracks; needs a game-side gadget (see the file header), inactive otherwise |
| `rml/*.rml`, `rml/theme.rcss` | The documents and the shared theme |
| `rml/core.lua` | Shared helpers every widget includes (documents, placement, views, formatting) |
| `configs/slate_game.lua` | Everything specific to the game |
| `configs/slate_theme.lua` | The settings' defaults and the colours a tint is computed from |
| `configs/options/*.lua` | One settings tab per file |
| `configs/slate_keybind_actions.lua` | Vocabulary of the custom-bind editor |
| `fonts/`, `images/` | Saira SemiCondensed (SIL OFL) and the premultiplied-alpha icons |

## Using it in another game

1. Copy the `luaui/slate/` folder into the game.
2. Make the game's widget handler load widgets from `luaui/slate/widgets/` as
   well. It is two small edits; [HANDLER.md](HANDLER.md) has them line for line.
3. Copy `configs/slate_game.lua` to the game's own `luaui/configs/` and edit it
   there: resources, build categories, hidden commands, unit stats, sounds, menu
   entries. Do the same with `slate_theme.lua` to change the defaults. A file in
   `luaui/configs/` is read in preference to the one in this folder, so the
   folder can later be swapped for a newer Slate without losing the game's
   settings. Extra settings tabs go in `luaui/configs/slate_options/`.
4. Disable or remove any widgets that draw the same things (resource bar, build
   menu, tooltip, console, player list, minimap frame, pause screen, replay
   buttons).

To take Slate out again, delete the folder and the lines from step 2.

Slate needs the stock LuaUI widget handler, an engine with RmlUi (Recoil 2024
or later) and nothing else from the game.

## The look

`rml/theme.rcss` is the theme; each document adds its own layout in a `<style>`
block. The player's opacity and colour tint are turned into a few rules at run
time (`WG.Slate.ThemeRules()` in `slate_api_core.lua`) and appended to every
document's stylesheet, so a panel that uses the shared classes (`.panel`,
`.tile`, `.title`, `.accent`...) follows the settings for free.

## In-game commands

| Command | Effect |
|---|---|
| F10 | Settings (also in the Menu) |
| F11 | Widget list |
| H | Share window (also in the Menu, or click an ally in the players list) |
| Ctrl+F11 | Tweak mode: drag panels, right-click one to reset it |
| `/resetlayout` | Put every panel back in its default place |
| `/slate opacity 0.6` | Panel opacity, 0.1 to 1 |
| `/slate tint Blue` | Colour tint (`/slate tint` lists them) |
| `/slate scale 1.1` | Interface size |
| `/slate wind`, `/slate tidal` | Toggle the read-outs (tidal only shows on maps with water) |
| `/slate broadcast` | Toggle sending your fps, system and camera |
| `/slatekeys` | Re-apply the key files (after a `/keyreload`) |
| Ctrl+Insert | While hovering a build or order button: bind it to the next key pressed |
| Ctrl+Delete | While hovering a build or order button: remove its key |

Settings are kept in the engine config as `slate_*` variables, so they are
shared by every game on the install. Colour tints are listed in
`configs/slate_theme.lua` (`tints`); add or change entries there.

## Key binding files

Slate never writes to the player's `uikeys.txt`. Bindings are layered:

1. the engine defaults and the player's own `uikeys.txt`;
2. `luaui/configs/<game>_keys.txt` in the game archive, if the game ships one;
3. `<game>_uikeys.txt` in the player's Recoil folder, holding changes made in
   game as plain `bind` / `unbind` lines.

`<game>` is the game's short name in lower case (`xta_uikeys.txt` here), so
several games on one install keep separate changes.
