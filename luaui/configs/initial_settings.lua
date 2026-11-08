--------------------------------------------------------------------------------
--  Recommended engine settings, written on a player's first run (TA:Recoil; system and code from Splinter Faction).
--
--  Used in two places:
--    LuaIntro/Addons/initial_settings.lua  writes them while the match loads,
--        before the engine reads most of them, so they take effect in the
--        very first match, multiplayer included, with no restart.
--    LuaUI/Widgets/gui_initial_settings.lua  restarts a single-player match
--        once if the loading screen had to change a setting the engine may
--        already have read (see RELOAD_FIXES).
--
--  Bump VERSION to make everyone apply the list again on their next launch.
--------------------------------------------------------------------------------

local M = {}

M.VERSION     = 4   -- 2: TeamNanoSpray, 3: deferred rendering, 4: GrassDetail
M.MARKER_KEY  = "TARInitialSettingsVersion"   -- VERSION, once the list has been written
M.PENDING_KEY = "TARInitialSettingsReload"    -- 1: the loading screen changed a RELOAD_FIXES setting

--------------------------------------------------------------------------------
-- Settings. Ordered list so application order is deterministic.
--   integer number -> SetConfigInt
--   fractional     -> SetConfigFloat
--   boolean        -> SetConfigInt (1/0)
--   string         -> SetConfigString
--------------------------------------------------------------------------------

local settings = {
	-- One 8192x8192 page for the effect textures (Splinter Faction's, ~41 megapixels). At the engine default of
	-- 4096 they need several pages, and effects that mix textures from different pages draw as flat garbled
	-- rectangles (engine 2026.09.01).
	{ "MaxTextureAtlasSizeX",        8192 },
	{ "MaxTextureAtlasSizeY",        8192 },
	-- Nanospray and the frames of units being built in the unit's nano colour, not team colour. The modrule
	-- (nanospray.allow_team_colors) is no longer read by the engine; this player setting is what decides now.
	-- The engine (2026.09) reads it at process start, so the spray turns green from the next launch; the CUS GL4
	-- build effect reads it when the match starts, so that one is green at once. Applied once per VERSION.
	{ "TeamNanoSpray",               0 },
	-- Deferred G-buffers for maps and models: the dynamic lights (gfx_deferred_rendering_gl4) and bloom need them.
	{ "AllowDeferredMapRendering",   1 },
	{ "AllowDeferredModelRendering", 1 },
	-- Engine grass off: the Map Grass GL4 widget draws the grass (both at once would double it).
	{ "GrassDetail",                 0 },
}

--------------------------------------------------------------------------------
-- Read while the match loads (MaxSounds excepted: the sound system starts with
-- the process, and only a reload restarts it). The loading screen runs before the engine
-- creates the texture atlases, the shadow map and the deferred buffers, so
-- writing them there normally takes effect at once. With multithreaded
-- loading the engine has started loading a moment earlier, so it is not
-- guaranteed; a reload rebuilds all of them for certain.
--------------------------------------------------------------------------------

local RELOAD_FIXES = {
	AllowDeferredMapRendering   = true,
	AllowDeferredModelRendering = true,
	MaxSounds                   = true,
	MaxTextureAtlasSizeX        = true,
	MaxTextureAtlasSizeY        = true,
	ShadowMapSize               = true,
}

--------------------------------------------------------------------------------
-- Read once at process start (CGlobalRendering). Neither the loading screen
-- nor a reload changes these; they apply on the next launch.
--------------------------------------------------------------------------------

local PROCESS_ONLY = {
	LoadingMT = true,
	MSAALevel = true,
	TeamNanoSpray = true,   -- engine 2026.09: read once at start (later engines apply it live)
}

M.settings     = settings
M.RELOAD_FIXES = RELOAD_FIXES
M.PROCESS_ONLY = PROCESS_ONLY

--------------------------------------------------------------------------------
-- Writing. Spring is passed in, so this file needs nothing from the
-- environment it is loaded into.
--------------------------------------------------------------------------------

-- Writes every setting. Returns applied, failed, reloadDirty, processDirty:
-- reloadDirty / processDirty say whether a setting in RELOAD_FIXES /
-- PROCESS_ONLY actually changed. log(text), if given, is told about those.
function M.Apply(Spring, log)
	local spGetConfigString = Spring.GetConfigString
	local spSetConfigInt    = Spring.SetConfigInt
	local spSetConfigFloat  = Spring.SetConfigFloat
	local spSetConfigString = Spring.SetConfigString

	local function encode(value)
		local t = type(value)
		if t == "boolean" then
			return "int", (value and 1 or 0)
		elseif t == "number" then
			if value % 1 == 0 then
				return "int", value
			end
			return "float", value
		end
		return "string", tostring(value)
	end

	local function setValue(key, kind, value)
		if kind == "int" then
			spSetConfigInt(key, value, false)
		elseif kind == "float" then
			if spSetConfigFloat then
				spSetConfigFloat(key, value, false)
			else
				spSetConfigString(key, tostring(value), false)
			end
		else
			spSetConfigString(key, value, false)
		end
	end

	local function currentAsString(key)
		local ok, v = pcall(spGetConfigString, key, "")
		if ok and v ~= nil and v ~= "" then
			return tostring(v)
		end
		return nil
	end

	local applied, failed = 0, 0
	local reloadDirty, processDirty = false, false

	for i = 1, #settings do
		local key = settings[i][1]
		local kind, value = encode(settings[i][2])
		local before = currentAsString(key)

		local ok = pcall(setValue, key, kind, value)
		if ok then
			applied = applied + 1
			if before ~= tostring(value) then
				if RELOAD_FIXES[key] then reloadDirty  = true end
				if PROCESS_ONLY[key] then processDirty = true end
				if log and (RELOAD_FIXES[key] or PROCESS_ONLY[key]) then
					log(key .. ": " .. tostring(before) .. " -> " .. tostring(value))
				end
			end
		else
			failed = failed + 1
			if log then log("failed to set: " .. tostring(key)) end
		end
	end

	return applied, failed, reloadDirty, processDirty
end

return M
