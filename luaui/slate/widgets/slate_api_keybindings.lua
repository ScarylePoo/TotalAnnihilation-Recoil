-- Part of Slate, a game-neutral RmlUi interface for Total Annihilation style
-- games on the Recoil engine. Derived from gui_sf_keybindings.lua in Splinter
-- Faction (same author, GPL v2+).

function widget:GetInfo()
	return {
		name      = "Slate Keybindings",
		desc      = "Owns the per-game key binding files: applies <game>_keys.txt from the game archive and the player's in-game rebinds (<game>_uikeys.txt) on top of the engine's bindings.",
		author    = "Scary le Poo",
		date      = "2026-10-24",
		license   = "GNU GPL, v2 or later",
		layer     = -1000, -- first to Initialize, so widgets that bind keys in their own Initialize land on top
		enabled   = true,
	}
end

--------------------------------------------------------------------------------
-- WHERE BINDINGS LIVE
--
--   1. the engine's defaults and the player's own uikeys.txt   - never touched
--   2. luaui/configs/<game>_keys.txt inside the game archive   - the game's
--      defaults (optional)
--   3. <game>_uikeys.txt in the player's Recoil folder         - changes made
--      in the Keybinds window, as plain bind / unbind lines
--
-- Each later file is loaded on top of the earlier ones. Because file 3 is
-- named after the game, several games on one install each keep their own
-- changes and never see each other's. <game> is the game's short name in
-- lower case.
--
-- Widgets that bind keys at runtime (the settings window's F10, say) do so
-- in their own Initialize, after this one. A later re-apply (/slatekeys)
-- would put the files' binds in front of those again, so they register with
-- WG.SlateKeybindings.AddReapplyHook and are re-run after every re-apply.
--------------------------------------------------------------------------------

local shortName = (Game.gameShortName or Game.modShortName or "game"):lower():gsub("[^%w_]", "")
local GAME_KEYS_FILE = "luaui/configs/" .. shortName .. "_keys.txt"
local USER_KEYS_FILE = shortName .. "_uikeys.txt"

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

local function BuildCommands()
	local cmds = {}
	-- the game's own defaults, read from the archive only so a loose copy in
	-- the write dir can never stand in for them
	local text = VFS.FileExists(GAME_KEYS_FILE, VFS.ZIP) and VFS.LoadFile(GAME_KEYS_FILE, VFS.ZIP)
	if text then
		ReadKeyLines(text, cmds)
	end
	if RawFileExists(USER_KEYS_FILE) then
		-- raw on purpose: this file lives in the write dir
		cmds[#cmds + 1] = "keyload " .. USER_KEYS_FILE
	end
	return cmds
end

local function ApplyKeys(verbose)
	local cmds = BuildCommands()
	if #cmds > 0 then
		spSendCommands(cmds)
	end
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
