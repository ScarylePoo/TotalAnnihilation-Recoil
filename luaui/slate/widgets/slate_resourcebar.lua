-- Part of Slate, a game-neutral RmlUi interface for Total Annihilation style
-- games on the Recoil engine. Derived from the Bastion HUD in Splinter
-- Faction (same author, GPL v2+).

function widget:GetInfo()
	return {
		name    = "Slate Resource Bar",
		desc    = "Metal and energy with storage, income, drain and a draggable share level. Optional wind and tidal read-outs.",
		author  = "Scary le Poo",
		date    = "2026-10-24",
		license = "GNU GPL, v2 or later",
		layer   = 1,
		enabled = true,
	}
end

--------------------------------------------------------------------------------
--  One strip at the top centre, a cell per resource in slate_game.lua
--  (metal and energy by default): stored / storage, net change, income and
--  pull, and a storage bar. Click or drag on a storage bar to set the share
--  level: stock above the marker is shared with allies.
--
--  The wind and tidal read-outs sit at the right end of the same strip when
--  switched on (settings, or /slate wind and /slate tidal); tidal only shows
--  on maps with water.
--------------------------------------------------------------------------------

local DOCUMENT_PATH   = "resourcebar.rml"
local UPDATE_INTERVAL = 0.1 -- seconds between refreshes

-- must match #resbar in resourcebar.rml
local CELL_WIDTH  = 340   -- per resource
local WIND_WIDTH  = 150
local TIDAL_WIDTH = 90
local BAR_HEIGHT  = 64

local LAYOUT_NAME = "slate_resourcebar"

local DEFAULT_SHARE_LEVEL = 0.8

local spGetMyTeamID        = Spring.GetMyTeamID
local spGetTeamResources   = Spring.GetTeamResources
local spGetSpectatingState = Spring.GetSpectatingState
local spSetShareLevel      = Spring.SetShareLevel
local spGetWind            = Spring.GetWind

local floor = math.floor
local format = string.format

local hud, S
local document
local view
local SetText, SetClass, SetStyle
local lastUpdate

local resources = {}      -- from slate_game.lua
local shareLevel = {}     -- key -> 0..1
local dragging            -- resource key while a share marker is being dragged
local hasWater = false
local showWind, showTidal = false, false
local barWidth = 0

--------------------------------------------------------------------------------
-- helpers
--------------------------------------------------------------------------------

local function Signed(value)
	-- the rounding is done first so that -0.04 reads "+0.0", not "-0.0"
	value = floor(value * 10 + 0.5) / 10
	if value >= 0 then
		return format("+%.1f", value)
	end
	return format("%.1f", value)
end

local function Percent(fraction)
	if fraction < 0 then
		fraction = 0
	elseif fraction > 1 then
		fraction = 1
	end
	-- half-percent steps: about one pixel of bar, and no restyle for less
	return format("%.1f%%", floor(fraction * 200 + 0.5) / 2)
end

--------------------------------------------------------------------------------
-- markup: one cell per resource
--------------------------------------------------------------------------------

local function CellRML(i, res)
	local key = res.key
	local icon = ""
	if res.icon and res.icon ~= "" then
		icon = format('<img class="icon" src="/%s%s"/>', hud.IMAGE_DIR, res.icon)
	end
	return table.concat({
		(i > 1) and '<div class="divider"/>' or "",
		format('<div id="cell-%s" class="cell">', key),
		'<div class="line head">', icon,
		format('<div class="label">%s</div>', hud.Escape(res.label or key)),
		'<div class="grow"/>',
		format('<div id="%s-net" class="net good">+0.0</div>', key),
		'</div>',
		'<div class="line figures">',
		format('<div id="%s-cur" class="value" style="color: %s;">0</div>', key, res.color or "#f4f5f7"),
		format('<div id="%s-max" class="sub">/ 0</div>', key),
		'<div class="grow"/>',
		format('<div id="%s-in" class="flow good">+0.0</div>', key),
		'<div class="slash">/</div>',
		format('<div id="%s-out" class="flow bad">-0.0</div>', key),
		'</div>',
		format('<div id="%s-grab" class="grab">', key),
		'<div class="bar">',
		format('<div id="%s-fill" class="bar-fill" style="background-color: %s;"/>', key, res.color or "#a9bdd0"),
		format('<div id="%s-share" class="share"/>', key),
		'</div></div></div>',
	})
end

--------------------------------------------------------------------------------
-- refreshing
--------------------------------------------------------------------------------

-- Bar colours carry a meaning: red below 20% (stalling), amber above 85%
-- (about to waste it). Energy above 80% is green: plenty.
local function RefreshResource(team, res, spectating)
	local name = res.key
	local current, storage, pull, income = spGetTeamResources(team, name)
	current, storage, pull, income = current or 0, storage or 0, pull or 0, income or 0

	local fraction = (storage > 0) and (current / storage) or 0
	local net = income - pull

	SetText(name .. "-cur", hud.Number(current))
	SetText(name .. "-max", "/ " .. hud.Number(storage))
	SetText(name .. "-net", Signed(net))
	SetClass(name .. "-net", "good", net >= -0.05)
	SetClass(name .. "-net", "bad", net < -0.05)
	SetText(name .. "-in", "+" .. hud.Short(income))
	SetText(name .. "-out", "-" .. hud.Short(pull))

	-- an inline colour would beat the state classes, so the fill's own colour
	-- is restated only while no state applies
	local low = fraction < 0.2
	local high = fraction > 0.85 and name ~= "energy"
	local plenty = fraction > 0.8 and name == "energy"
	SetStyle(name .. "-fill", "width", Percent(fraction))
	SetStyle(name .. "-fill", "background-color",
		(low and "#ffb3a6") or (high and "#f2c230") or (plenty and "#9be7a8") or res.color or "#a9bdd0")

	-- a spectator cannot set anyone's share level
	SetClass(name .. "-share", "hidden", spectating)
	SetClass(name .. "-grab", "live", not spectating)
	SetStyle(name .. "-share", "left", Percent(shareLevel[name] or DEFAULT_SHARE_LEVEL))
	SetClass(name .. "-share", "dragging", dragging == name)
end

local function RefreshAddons()
	if showWind then
		local _, _, _, strength = spGetWind()
		SetText("wind-cur", format("%.1f", strength or 0))
		SetText("wind-range", format("(%d - %d)", Game.windMin or 0, Game.windMax or 0))
	end
	if showTidal then
		SetText("tidal-cur", format("%.1f", Game.tidal or 0))
	end
end

local function Refresh()
	local team = spGetMyTeamID()
	if not team then
		return
	end
	local spectating = spGetSpectatingState() and true or false
	for i = 1, #resources do
		RefreshResource(team, resources[i], spectating)
	end
	RefreshAddons()
end

--------------------------------------------------------------------------------
-- share level
--------------------------------------------------------------------------------

local function SetShare(name, level)
	if level < 0 then
		level = 0
	elseif level > 1 then
		level = 1
	end
	level = floor(level * 100 + 0.5) / 100
	if shareLevel[name] ~= level then
		shareLevel[name] = level
		spSetShareLevel(name, level)
	end
end

local function StartDrag(name)
	if spGetSpectatingState() then
		return
	end
	dragging = name
	local level = hud.MouseFraction(view.Element(name .. "-grab"))
	if level then
		SetShare(name, level)
	end
	Refresh()
end

-- called every frame while a marker is held
local function FollowDrag()
	local name = dragging
	local level = hud.MouseFraction(view.Element(name .. "-grab"))
	if level then
		SetShare(name, level)
	end
	Refresh()
end

local function EndDrag()
	if dragging then
		dragging = nil
		Refresh()
	end
end

--------------------------------------------------------------------------------
-- placement
--------------------------------------------------------------------------------

local function DefaultOrigin(vsx, vsy, w, h, scale)
	return (vsx - w) * 0.5, vsy - h - hud.Margin() * scale
end

local function Place()
	showWind = S.Get("wind")
	showTidal = S.Get("tidal") and hasWater
	barWidth = CELL_WIDTH * math.max(1, #resources) + (showWind and WIND_WIDTH or 0) + (showTidal and TIDAL_WIDTH or 0)
	local bar = view.Element("resbar")
	bar.style["width"] = barWidth .. "dp"
	SetClass("wind", "hidden", not showWind)
	SetClass("wind-divider", "hidden", not showWind)
	SetClass("tidal", "hidden", not showTidal)
	SetClass("tidal-divider", "hidden", not showTidal)
	view.ForgetStyles()
	hud.PlacePanel(bar, LAYOUT_NAME, barWidth, BAR_HEIGHT, DefaultOrigin)
end

local function InPanel(mx, my)
	local layout = WG.SlateLayout
	if not layout then return false end
	local x1, y1, x2, y2 = layout.GetRect(LAYOUT_NAME)
	return x1 and mx >= x1 and mx <= x2 and my >= y1 and my <= y2
end

-- The screen rectangle of an element, y up, or nil.
local function ElementRect(element)
	if not element or not element.absolute_left then return nil end
	local _, vsy = Spring.GetViewGeometry()
	local x1 = element.absolute_left
	local top = vsy - element.absolute_top
	return x1, top - element.offset_height, x1 + element.offset_width, top
end

--------------------------------------------------------------------------------
-- widget api
--------------------------------------------------------------------------------

function widget:Initialize()
	S = WG.Slate
	if not S then
		widgetHandler:RemoveWidget()
		return
	end
	local helpers = include("slate/rml/core.lua")
	local result, reason = helpers.LoadDocument(DOCUMENT_PATH, widget)
	if not result then
		Spring.Echo("[Slate Resource Bar] " .. tostring(reason))
		widgetHandler:RemoveWidget()
		return
	end
	hud = helpers
	document = result

	resources = S.game.resources or {}
	local lowest = Spring.GetGroundExtremes()
	hasWater = (lowest or 0) < 0

	view = hud.NewView(document)
	SetText, SetClass, SetStyle = view.SetText, view.SetClass, view.SetStyle

	local parts = {}
	for i = 1, #resources do
		parts[i] = CellRML(i, resources[i])
	end
	view.Element("cells").inner_rml = table.concat(parts)
	view.Forget()
	view.Assume("wind", "hidden", true)
	view.Assume("wind-divider", "hidden", true)
	view.Assume("tidal", "hidden", true)
	view.Assume("tidal-divider", "hidden", true)

	Spring.SendCommands("resbar 0") -- this bar replaces the engine's

	for i = 1, #resources do
		local key = resources[i].key
		shareLevel[key] = shareLevel[key] or DEFAULT_SHARE_LEVEL
		spSetShareLevel(key, shareLevel[key])
		hud.OnDrag(view, key .. "-grab", function() StartDrag(key) end, EndDrag)
		view.Assume(key .. "-net", "good", true)
	end

	hud.RegisterPanel(LAYOUT_NAME, "Resources", Place)
	hud.OnChange(LAYOUT_NAME, Place)
	Place()

	S.SetTip(LAYOUT_NAME, function(mx, my)
		if Spring.IsGUIHidden() or not InPanel(mx, my) then return nil end
		for i = 1, #resources do
			local x1, y1, x2, y2 = ElementRect(view.Element(resources[i].key .. "-grab"))
			if x1 and mx >= x1 and mx <= x2 and my >= y1 - 4 and my <= y2 + 4 then
				return (resources[i].label or resources[i].key) .. " share level",
					"Drag the marker along the bar. When your storage is fuller than the marker, the excess goes to your allies."
			end
		end
		local ax1 = ElementRect(view.Element(showWind and "wind" or "tidal"))
		if (showWind or showTidal) and ax1 and mx >= ax1 then
			return "Wind and tide", "Wind changes constantly within the range shown for this map; wind generators produce in step with it. Tidal strength is fixed for the map."
		end
		return "Resources", "Stored and storage on the left. On the right, income (+) and what your builders are asking for (-), per second."
	end)

	Refresh()
	hud.ShowPassive(document)
	lastUpdate = Spring.GetTimer()
end

function widget:Shutdown()
	Spring.SendCommands("resbar 1")
	if S then
		S.SetTip(LAYOUT_NAME, nil)
	end
	if hud then
		hud.UnregisterPanel(LAYOUT_NAME)
		hud.OffChange(LAYOUT_NAME)
		hud.CloseDocument(document)
		document = nil
	end
end

function widget:ViewResize()
	if hud and document then
		hud.UpdateScale()
		Place()
	end
end

function widget:Update(dt)
	if not document then
		return
	end
	if hud.FollowGuiHidden(document) then
		dragging = nil
		return -- hidden with the rest of the GUI (F5)
	end
	if dragging then
		FollowDrag()
		return
	end
	local now = Spring.GetTimer()
	if Spring.DiffTimers(now, lastUpdate) >= UPDATE_INTERVAL then
		lastUpdate = now
		Refresh()
	end
end

-- the share levels are the player's choice: keep them across sessions
function widget:GetConfigData()
	return { shareLevel = shareLevel }
end

function widget:SetConfigData(data)
	if type(data) ~= "table" or type(data.shareLevel) ~= "table" then
		return
	end
	for key, level in pairs(data.shareLevel) do
		if type(level) == "number" then
			shareLevel[key] = math.max(0, math.min(1, level))
		end
	end
end
