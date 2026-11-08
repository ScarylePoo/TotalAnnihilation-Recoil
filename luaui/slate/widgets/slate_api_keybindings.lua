-- Part of Slate, a game-neutral RmlUi interface for Total Annihilation style
-- games on the Recoil engine. Derived from gui_sf_keybindings.lua in Splinter
-- Faction (same author, GPL v2+).

function widget:GetInfo()
	return {
		name      = "Slate Keybindings",
		desc      = "Owns the key bindings: discards the engine-loaded uikeys.txt, then applies the game's <game>_keys.txt, the engine defaults behind them, and the player's in-game rebinds (<game>_uikeys.txt) on top.",
		author    = "Scary le Poo",
		date      = "2026-10-24",
		license   = "GNU GPL, v2 or later",
		layer     = -1000, -- first to Initialize, so widgets that bind keys in their own Initialize land on top
		enabled   = true,
	}
end

--------------------------------------------------------------------------------
-- WHY THIS REPLACES uikeys.txt INSTEAD OF LAYERING ON IT
--
-- Many players run one Recoil install for several games, and uikeys.txt in the
-- write dir is shared between them. Whatever another game left there (or an
-- "unbindall" at its top) used to win, because per keyset the engine runs the
-- first-bound action that is available, and uikeys.txt is bound at startup
-- before LuaUI exists.
--
-- So the bind table is rebuilt from scratch, in priority order:
--
--   1. unbindall                         drops everything, including uikeys.txt
--   2. luaui/configs/<game>_keys.txt     the game's binds, from the game archive
--                                        only (optional)
--   3. slate/configs/engine_default_keys.txt
--                                        the engine's built-in binds (generated
--                                        from the engine source), as fallbacks
--   4. <game>_uikeys.txt (write dir)     the player's rebinds from the Keybinds
--                                        window; its unbind lines remove what it
--                                        replaces, so it wins conflicts
--
-- <game> is the game's short name in lower case, so several games on one
-- install each keep their own rebinds. The engine's "keydefaults" is not a
-- registered console action, so it cannot be sent from Lua; that is why the
-- defaults are shipped as a file. uikeys.txt is never read or written; a
-- player who runs /keyreload gets it back until the next /slatekeys.
--
-- Widgets that bind keys at runtime (the settings window's F10, say) do so
-- in their own Initialize, after this one. A later re-apply (/slatekeys)
-- would wipe those binds, so they register with
-- WG.SlateKeybindings.AddReapplyHook and are re-run after every re-apply.
--
-- (From Splinter Faction's gui_sf_keybindings.lua.)
--------------------------------------------------------------------------------

local shortName = (Game.gameShortName or Game.modShortName or "game"):lower():gsub("[^%w_]", "")
local GAME_KEYS_FILE = "luaui/configs/" .. shortName .. "_keys.txt"
local USER_KEYS_FILE = shortName .. "_uikeys.txt"
-- the engine's defaults, shipped with Slate; archive only as well
local ENGINE_KEYS_FILE = LUAUI_DIRNAME .. "slate/configs/engine_default_keys.txt"

-- "/slatekeys" re-applies the files (e.g. after a /keyreload)
local ACTION_NAME = "slatekeys"

local spSendCommands = Spring.SendCommands
local spEcho         = Spring.Echo

local reapplyHooks = {} -- ordered {name = , fn = }

-- True if the path exists on the raw filesystem (not inside an archive).
local function RawFileExists(path)
	if VFS.RAW_ONLY and VFS.FileExists(path, VFS.RAW_ONLY) then
		return true
	end
	local f = io.open(path, "r")
	if f then
		f:close()
		return true
	end
	return false
end

-- Command lines of a uikeys-format file: comments and blank lines dropped.
local function ReadKeyLines(text, out)
	for line in text:gmatch("[^\r\n]+") do
		line = line:gsub("//.*$", "")
		line = line:match("^%s*(.-)%s*$")
		if line ~= "" then
			out[#out + 1] = line
		end
	end
	return out
end

local function AppendArchiveKeyFile(path, cmds, what, required)
	-- read from the archive only, so a loose copy in the write dir can never stand in for it
	local text = VFS.FileExists(path, VFS.ZIP) and VFS.LoadFile(path, VFS.ZIP)
	if text then
		ReadKeyLines(text, cmds)
	elseif required then
		spEcho("[Slate Keybindings] missing " .. path .. " -- no " .. what .. " applied")
	end
end

local function BuildCommands()
	local cmds = { "unbindall" }
	AppendArchiveKeyFile(GAME_KEYS_FILE, cmds, "game binds", false)   -- a game may have none
	AppendArchiveKeyFile(ENGINE_KEYS_FILE, cmds, "engine default binds", true)
	if RawFileExists(USER_KEYS_FILE) then
		-- raw on purpose: this file lives in the write dir
		cmds[#cmds + 1] = "keyload " .. USER_KEYS_FILE
	end
	return cmds
end

local function ApplyKeys(verbose)
	spSendCommands(BuildCommands())
	for i = 1, #reapplyHooks do
		local hook = reapplyHooks[i]
		local ok, err = pcall(hook.fn)
		if not ok then
			spEcho("[Slate Keybindings] reapply hook '" .. tostring(hook.name) .. "' failed: " .. tostring(err))
		end
	end
	if verbose then
		spEcho("[Slate Keybindings] key files re-applied")
	end
end

-- fn is called after every re-apply, so a widget's own runtime binds survive.
-- Registering again under the same name replaces the earlier hook.
local function AddReapplyHook(name, fn)
	if type(name) ~= "string" or type(fn) ~= "function" then return end
	for i = 1, #reapplyHooks do
		if reapplyHooks[i].name == name then
			reapplyHooks[i].fn = fn
			return
		end
	end
	reapplyHooks[#reapplyHooks + 1] = { name = name, fn = fn }
end

local function RemoveReapplyHook(name)
	for i = #reapplyHooks, 1, -1 do
		if reapplyHooks[i].name == name then
			table.remove(reapplyHooks, i)
		end
	end
end

local function ReloadAction(_, _, _, _, _, release)
	if release then
		return true
	end
	ApplyKeys(true)
	return true
end

function widget:Initialize()
	widgetHandler:AddAction(ACTION_NAME, ReloadAction, nil, "p")

	-- Shared with the Keybinds window and every widget that binds keys itself
	WG.SlateKeybindings = {
		Apply             = function() ApplyKeys(false) end,
		AddReapplyHook    = AddReapplyHook,
		RemoveReapplyHook = RemoveReapplyHook,
		gameFile          = GAME_KEYS_FILE,
		userFile          = USER_KEYS_FILE,
		engineFile        = ENGINE_KEYS_FILE,
		shortName         = shortName,
	}

	-- Applied here rather than on the first Update: this widget is layer -1000,
	-- so it initializes before every widget that adds its own binds.
	ApplyKeys(false)
end

function widget:Shutdown()
	widgetHandler:RemoveAction(ACTION_NAME, "p")
	WG.SlateKeybindings = nil
end
