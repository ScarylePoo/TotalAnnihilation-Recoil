-- Part of Slate, a game-neutral RmlUi interface for Total Annihilation style
-- games on the Recoil engine. Derived from the Bastion HUD in Splinter
-- Faction (same author, GPL v2+).

function widget:GetInfo()
	return {
		name    = "Slate Core",
		desc    = "Shared theme, game config and settings for the Slate panels. /slate opacity <0-1>, /slate tint <name>, /slate wind, /slate tidal",
		author  = "Scary le Poo",
		date    = "2026-10-24",
		license = "GNU GPL, v2 or later",
		layer   = -99998,   -- after Slate Layout (-99999), before every panel
		enabled = true,
		handler = true,
	}
end

--------------------------------------------------------------------------------
-- WHAT THIS IS
--
-- Every Slate panel is a widget that draws itself with RmlUi (the documents
-- in luaui/slate/rml/) and asks this one for:
--
--   WG.Slate.theme    colours, opacity, sizes   (luaui/slate/configs/slate_theme.lua)
--   WG.Slate.game     what the game looks like  (luaui/slate/configs/slate_game.lua)
--   WG.Slate.Get/Set  the player's settings (opacity, tint, size...), kept in
--                     the engine config so they survive between games
--   WG.Slate.ThemeRules()  the RCSS the settings add on top of theme.rcss;
--                     luaui/slate/rml/core.lua appends it to every document
--   WG.Slate.OnChange a way to hear about a changed setting
--
-- so no panel hardcodes a colour, and a game that adopts Slate edits the two
-- config files and nothing else.
--
-- TO USE SLATE IN ANOTHER GAME
--
--   copy  the luaui/slate/ folder
--   add   luaui/slate/widgets/ to the widget handler's search (HANDLER.md)
--   edit  a copy of slate_game.lua (and slate_theme.lua to taste) placed in
--         the game's own luaui/configs/, which is read in preference
--
-- Nothing else in the game refers to these files.
--------------------------------------------------------------------------------

local SLATE_DIR = LUAUI_DIRNAME .. "slate/"
-- A game's own copy in luaui/configs/ wins, so the slate folder can be
-- replaced with a newer one without losing the game's settings.
local CONFIG_DIRS = { LUAUI_DIRNAME .. "configs/", SLATE_DIR .. "configs/" }

local spEcho  = Spring.Echo
local floor   = math.floor
local max     = math.max
local min     = math.min

local S = {}

--------------------------------------------------------------------------------
-- Config
--------------------------------------------------------------------------------

local function LoadTable(file, fallback)
	local path
	for i = 1, #CONFIG_DIRS do
		if VFS.FileExists(CONFIG_DIRS[i] .. file) then
			path = CONFIG_DIRS[i] .. file
			break
		end
	end
	if not path then
		spEcho("[Slate] missing " .. CONFIG_DIRS[#CONFIG_DIRS] .. file)
		return fallback
	end
	local ok, result = pcall(VFS.Include, path)
	if not ok or type(result) ~= "table" then
		spEcho("[Slate] could not load " .. path .. ": " .. tostring(result))
		return fallback
	end
	return result
end

--------------------------------------------------------------------------------
-- Settings
--
-- Each setting is an engine config variable (slate_<key>) whose default is the
-- value in slate_theme.lua or slate_game.lua. The options window reads and
-- writes them through S.Get and S.Set; so do the /slate commands.
--------------------------------------------------------------------------------

-- key -> { kind = "float"|"int"|"bool"|"string", config = name, default = fn, lo =, hi = }
local SETTINGS = {
	opacity      = { kind = "float",  lo = 0.1, hi = 1,   default = function() return S.theme.opacity or 0.6 end },
	scale        = { kind = "float",  lo = 0.7, hi = 1.5, default = function() return S.theme.scale or 1 end },
	minimapSize  = { kind = "float",  lo = 0.5, hi = 2.5, default = function() return S.theme.minimapSize or 1 end },
	tint         = { kind = "string",                     default = function() return S.theme.tint or "None" end },
	tintStrength = { kind = "float",  lo = 0,   hi = 1,   default = function() return S.theme.tintStrength or 0.5 end },
	wind         = { kind = "bool",                       default = function() return (S.game.addons or {}).wind and true or false end },
	tidal        = { kind = "bool",                       default = function() return (S.game.addons or {}).tidal and true or false end },
	broadcast    = { kind = "bool",                       default = function() return S.theme.broadcast ~= false end },
}

local function ConfigName(key)
	return "slate_" .. key:lower()
end

function S.Get(key)
	local def = SETTINGS[key]
	if not def then
		return nil
	end
	local name = ConfigName(key)
	local fallback = def.default()
	if def.kind == "float" then
		local v = Spring.GetConfigFloat(name, fallback)
		if v == nil then v = fallback end
		return min(def.hi, max(def.lo, v))
	elseif def.kind == "bool" then
		return (Spring.GetConfigInt(name, fallback and 1 or 0) or 0) > 0
	elseif def.kind == "string" then
		return Spring.GetConfigString(name, fallback) or fallback
	end
	return Spring.GetConfigInt(name, fallback)
end

local NotifyAll -- defined below

function S.Set(key, value)
	local def = SETTINGS[key]
	if not def then
		return
	end
	local name = ConfigName(key)
	if def.kind == "float" then
		Spring.SetConfigFloat(name, min(def.hi, max(def.lo, tonumber(value) or def.default())))
	elseif def.kind == "bool" then
		Spring.SetConfigInt(name, value and 1 or 0)
	elseif def.kind == "string" then
		Spring.SetConfigString(name, tostring(value))
	else
		Spring.SetConfigInt(name, floor((tonumber(value) or 0) + 0.5))
	end
	NotifyAll()
end

-- The tints the settings offer, from slate_theme.lua.
function S.TintNames()
	local names = {}
	for _, t in ipairs(S.theme.tints or {}) do
		names[#names + 1] = t.name
	end
	return names
end

local function TintColor(name)
	for _, t in ipairs(S.theme.tints or {}) do
		if t.name == name then
			return t.color
		end
	end
	return nil
end

--------------------------------------------------------------------------------
-- The theme the settings produce
--
-- theme.rcss holds the default look. The player's opacity and tint are turned
-- into a few RCSS rules here, which core.lua appends to every document's
-- stylesheet (appended rules win over the file's). Only the classes listed
-- here respond to the settings, so a panel widget that wants its glass tinted
-- uses .panel, its tiles .tile and its headings .title or .accent.
--------------------------------------------------------------------------------

local function Mix(a, b, t)
	return a * (1 - t) + b * t
end

local function Rgb(r, g, b)
	return string.format("rgb(%d,%d,%d)", floor(r * 255 + 0.5), floor(g * 255 + 0.5), floor(b * 255 + 0.5))
end

local function Rgba(r, g, b, a)
	return string.format("rgba(%d,%d,%d,%d)", floor(r * 255 + 0.5), floor(g * 255 + 0.5), floor(b * 255 + 0.5), floor(a * 255 + 0.5))
end

-- The colours a tint changes, resolved for the current settings.
function S.Colors()
	local t = S.theme
	local tint = TintColor(S.Get("tint"))
	local s = tint and S.Get("tintStrength") or 0
	tint = tint or { 0, 0, 0 }
	local panel, border, accent = {}, {}, {}
	for i = 1, 3 do
		local light = tint[i] * 0.55 + 0.45
		-- the glass stays dark enough for text at any strength
		panel[i]  = Mix(t.panel[i], tint[i] * 0.38, s)
		border[i] = Mix(t.border[i], light, s)
		accent[i] = Mix(t.accent[i], light, s)
	end
	return {
		panel = panel,
		border = border,
		borderAlpha = t.border[4] or 0.14,
		accent = accent,
		opacity = S.Get("opacity"),
	}
end

function S.ThemeRules()
	local c = S.Colors()
	local p, b, a = c.panel, c.border, c.accent
	local opacity = c.opacity
	local borderRgba = Rgba(b[1], b[2], b[3], c.borderAlpha)
	local firmRgba = Rgba(b[1], b[2], b[3], min(1, c.borderAlpha * 1.7))
	local accentRgb = Rgb(a[1], a[2], a[3])
	local accentDim = Rgb(a[1] * 0.85, a[2] * 0.85, a[3] * 0.85)
	local accentBright = Rgb(min(1, a[1] * 1.15), min(1, a[2] * 1.15), min(1, a[3] * 1.15))
	local rules = {
		".panel { background-color: " .. Rgba(p[1], p[2], p[3], opacity) .. "; border-color: " .. borderRgba .. "; }",
		".panel.window { background-color: " .. Rgba(p[1], p[2], p[3], max(opacity, 0.88)) .. "; }",
		".popup { background-color: " .. Rgba(p[1], p[2], p[3], max(opacity, 0.94)) .. "; }",
		".raised, .tile, .close, .tab, .button { border-color: " .. borderRgba .. "; }",
		".divider { background-color: " .. borderRgba .. "; }",
		".window-head { border-bottom-color: " .. borderRgba .. "; }",
		".tile.active, .tab.active, .button:active, .button.quiet:hover { border-color: " .. accentRgb .. "; }",
		".tab.active { border-bottom-color: " .. accentRgb .. "; }",
		".title, .accent, .signal { color: " .. accentRgb .. "; }",
		".accent-line { background-color: " .. Rgba(a[1], a[2], a[3], 0.47) .. "; }",
		".bar-fill, .pip.lit { background-color: " .. accentRgb .. "; }",
		".button.primary { background-color: " .. accentRgb .. "; border-color: " .. accentRgb .. "; }",
		".button.primary:hover { background-color: " .. accentBright .. "; border-color: " .. accentBright .. "; }",
		".button.primary:active { background-color: " .. accentDim .. "; border-color: " .. accentDim .. "; }",
		"scrollbarvertical sliderbar:hover { background-color: " .. accentRgb .. "; }",
		".firm { border-color: " .. firmRgba .. "; }",
	}
	return table.concat(rules, "\n")
end

-- The accent as an RCSS colour, for widgets that set colours from Lua.
function S.AccentColor()
	local a = S.Colors().accent
	return Rgb(a[1], a[2], a[3])
end

--------------------------------------------------------------------------------
-- Shared hover state: the build/order menu writes it, the selection panel
-- reads it. { unitDefID = n } or { title = "...", text = "..." } or nil.
-- S.hoverAction is the keybind action of the hovered button, for hotbind.
--------------------------------------------------------------------------------

S.hover = nil
S.hoverAction = nil

--------------------------------------------------------------------------------
-- Panel hints. A panel registers a function (mx, my) -> title, text that
-- answers only while the mouse is over it; the selection panel shows the
-- answer. (The engine tooltip is switched off, so hints have to travel here.)
--------------------------------------------------------------------------------

local tipProviders = {}
function S.SetTip(owner, fn) tipProviders[owner] = fn end

function S.TipAt(mx, my)
	for _, fn in pairs(tipProviders) do
		local ok, title, text = pcall(fn, mx, my)
		if ok and title then return title, text end
	end
end

--------------------------------------------------------------------------------
-- Change listeners. Panels register a function that re-places their panels;
-- it runs after any setting changes. core.lua wraps it so the documents are
-- restyled first.
--------------------------------------------------------------------------------

S.version = 0

local listeners = {}
function S.OnChange(owner, fn) listeners[owner] = fn end
function S.OffChange(owner) listeners[owner] = nil end

NotifyAll = function()
	S.version = S.version + 1
	for owner, fn in pairs(listeners) do
		local ok, err = pcall(fn)
		if not ok then spEcho("[Slate] " .. tostring(owner) .. ": " .. tostring(err)) end
	end
end
S.Notify = NotifyAll

--------------------------------------------------------------------------------
-- Widget callins
--------------------------------------------------------------------------------

function widget:Initialize()
	S.theme = LoadTable("slate_theme.lua", nil)
	S.game  = LoadTable("slate_game.lua", nil)
	if not S.theme or not S.game then
		spEcho("[Slate] config missing - Slate is disabled")
		widgetHandler:RemoveWidget()
		return
	end
	S.dir = SLATE_DIR

	-- Line-of-sight view on at the start of a game, if the game asks for it.
	-- Only before the game starts, so a player who turns it off keeps it off
	-- when the interface is reloaded.
	if S.game.losView and (Spring.GetGameFrame() or 0) <= 0 and Spring.GetMapDrawMode() ~= "los" then
		Spring.SendCommands("togglelos")
	end

	WG.Slate = S
end

function widget:Shutdown()
	if WG.Slate == S then WG.Slate = nil end
end

function widget:ViewResize()
	if S.theme then
		NotifyAll()
	end
end

function widget:TextCommand(command)
	if command:sub(1, 5) ~= "slate" then return false end
	local arg1, arg2 = command:match("^slate%s+(%S+)%s*(.*)")
	if arg1 == "opacity" then
		local v = tonumber(arg2)
		if v then
			S.Set("opacity", v)
			spEcho("[Slate] panel opacity " .. S.Get("opacity"))
		else
			spEcho("[Slate] usage: /slate opacity 0.6")
		end
	elseif arg1 == "tint" then
		local name = (arg2 or ""):match("^%s*(.-)%s*$")
		if TintColor(name) or name:lower() == "none" then
			S.Set("tint", TintColor(name) and name or "None")
			spEcho("[Slate] colour tint " .. S.Get("tint"))
		else
			spEcho("[Slate] tints: " .. table.concat(S.TintNames(), ", "))
		end
	elseif arg1 == "wind" or arg1 == "tidal" or arg1 == "broadcast" then
		S.Set(arg1, not S.Get(arg1))
		spEcho("[Slate] " .. arg1 .. " " .. (S.Get(arg1) and "on" or "off"))
	elseif arg1 == "scale" then
		local v = tonumber(arg2)
		if v then
			S.Set("scale", v)
			spEcho("[Slate] interface size " .. S.Get("scale"))
		else
			spEcho("[Slate] usage: /slate scale 1.0")
		end
	else
		return false
	end
	return true
end
