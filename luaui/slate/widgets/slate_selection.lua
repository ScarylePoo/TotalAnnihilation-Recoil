-- Part of Slate, a game-neutral RmlUi interface for Total Annihilation style
-- games on the Recoil engine. Derived from the Bastion HUD in Splinter
-- Faction (same author, GPL v2+).

function widget:GetInfo()
	return {
		name    = "Slate Selection Panel",
		desc    = "Shows the selected unit or group, the unit under the cursor, or what a build or order button does. Replaces the engine tooltip.",
		author  = "Scary le Poo",
		date    = "2026-10-24",
		license = "GNU GPL, v2 or later",
		layer   = 2,
		enabled = true,
	}
end

--------------------------------------------------------------------------------
--  One panel at the bottom centre, shown only when there is something to
--  say, in this order of preference: the build tile or order button under the
--  mouse (from WG.Slate.hover), a hint from another Slate panel
--  (WG.Slate.TipAt), the selection (one unit with its live health, income and
--  stats from slate_game.lua, or a group as a row of type icons with counts),
--  or else the unit or wreck under the cursor.
--
--  In the group view a type icon is a button: left click keeps only that
--  type selected, Alt + click a single unit of it, Ctrl + click every unit of
--  that type you own (Shift adds them instead).
--------------------------------------------------------------------------------

local DOCUMENT_PATH = "selection.rml"
local UPDATE_INTERVAL = 0.15
local MAX_GROUP_ICONS = 9

-- must match #selection in selection.rml
local WIDTH, HEIGHT = 760, 128
local LAYOUT_NAME = "slate_selection"

local spGetSelectedUnits       = Spring.GetSelectedUnits
local spGetSelectedUnitsCounts = Spring.GetSelectedUnitsCounts
local spGetSelectedUnitsSorted = Spring.GetSelectedUnitsSorted
local spGetUnitDefID           = Spring.GetUnitDefID
local spGetUnitHealth          = Spring.GetUnitHealth
local spGetUnitResources       = Spring.GetUnitResources
local spGetMouseState          = Spring.GetMouseState
local spTraceScreenRay         = Spring.TraceScreenRay
local spGetCurrentTooltip      = Spring.GetCurrentTooltip
local spGetTeamUnitsByDefs     = Spring.GetTeamUnitsByDefs
local spGetMyTeamID            = Spring.GetMyTeamID
local spSelectUnitArray        = Spring.SelectUnitArray
local spGetModKeyState         = Spring.GetModKeyState

local min, max, floor = math.min, math.max, math.floor
local format = string.format

local hud, S
local document
local view
local SetText, SetClass, SetStyle
local lastUpdate
local lastHover
local shown                 -- the view currently on screen: "unit", "group", "text" or nil
local shownCells, shownTypes -- what the dynamic markup was made from
local groupTypes = {}       -- { defID =, count = } shown as icons; icon i has data-t="i"

--------------------------------------------------------------------------------
-- deciding what to show
--------------------------------------------------------------------------------

local function StatCells(ud, res)
	local cells = {}
	local defs = S.game.unitStats or {}
	for i = 1, #defs do
		local ok, value = pcall(defs[i].value, ud, res)
		if ok and value then
			cells[#cells + 1] = { label = defs[i].label, value = value }
		end
	end
	return cells
end

local function UnitView(unitID, defID)
	local ud = UnitDefs[defID]
	if not ud then return nil end
	local health, maxHealth = spGetUnitHealth(unitID)
	local mm, mu, em, eu = spGetUnitResources(unitID)
	local res = mm and { mm, mu or 0, em or 0, eu or 0 } or nil
	return {
		kind = "unit", defID = defID, title = hud.UnitName(ud), blurb = hud.UnitBlurb(ud),
		health = health, maxHealth = maxHealth,
		cells = StatCells(ud, res),
	}
end

local function Decide()
	local hover = S.hover
	if hover and hover.unitDefID and UnitDefs[hover.unitDefID] then
		local ud = UnitDefs[hover.unitDefID]
		local cells = StatCells(ud, nil)
		cells[#cells + 1] = { label = "Build time", value = hud.Number(ud.buildTime or 0) }
		return { kind = "unit", defID = hover.unitDefID, title = hud.UnitName(ud), blurb = hud.UnitBlurb(ud), cells = cells }
	elseif hover and (hover.title or hover.text) then
		return { kind = "text", title = hover.title or "", text = hover.text or "" }
	end

	-- a hint from whichever Slate panel the mouse is over
	local mx, my = spGetMouseState()
	local tipTitle, tipText = S.TipAt(mx, my)
	if tipTitle then
		return { kind = "text", title = tipTitle, text = tipText or "" }
	end

	local sel = spGetSelectedUnits() or {}
	if #sel == 1 then
		return UnitView(sel[1], spGetUnitDefID(sel[1]))
	elseif #sel > 1 then
		local counts = spGetSelectedUnitsCounts() or {}
		local types = {}
		for defID, n in pairs(counts) do
			if type(defID) == "number" and UnitDefs[defID] then
				types[#types + 1] = { defID = defID, count = n }
			end
		end
		table.sort(types, function(a, b)
			if a.count ~= b.count then return a.count > b.count end
			return a.defID < b.defID
		end)
		local health, maxHealth = 0, 0
		for i = 1, min(#sel, 300) do
			local h, m = spGetUnitHealth(sel[i])
			if h and m then health = health + h ; maxHealth = maxHealth + m end
		end
		return { kind = "group", total = #sel, types = types, health = health, maxHealth = maxHealth }
	end

	-- Nothing selected: describe what the cursor is on, if anything.
	local what, id = spTraceScreenRay(mx, my)
	if what == "unit" then
		local defID = spGetUnitDefID(id)
		if defID then return UnitView(id, defID) end
	end
	if what == "unit" or what == "feature" then
		local tip = spGetCurrentTooltip()
		if tip and tip ~= "" then
			local title, rest = tip:match("^([^\r\n]*)[\r\n]*(.*)$")
			return { kind = "text", title = title or "", text = rest or "" }
		end
	end
	return nil
end

--------------------------------------------------------------------------------
-- showing it
--------------------------------------------------------------------------------

local function Percent(fraction)
	fraction = max(0, min(1, fraction or 0))
	return format("%.1f%%", floor(fraction * 200 + 0.5) / 2)
end

local function ShowView(kind)
	if shown ~= kind then
		shown = kind
		SetClass("unit", "hidden", kind ~= "unit")
		SetClass("group", "hidden", kind ~= "group")
		SetClass("text", "hidden", kind ~= "text")
		SetClass("selection", "hidden", kind == nil)
	end
end

local function ShowUnit(v)
	local picEl = view.Element("unit-pic")
	local pic = hud.UnitPictureRML(v.defID, "pic")
	if picEl and view.lastPic ~= pic then
		view.lastPic = pic
		picEl.inner_rml = pic
	end
	SetText("unit-name", hud.Escape(v.title))
	SetText("unit-blurb", hud.Escape(v.blurb))
	local live = v.health and v.maxHealth
	SetClass("unit-health", "hidden", not live)
	if live then
		SetStyle("unit-fill", "width", Percent(v.maxHealth > 0 and v.health / v.maxHealth or 0))
		SetText("unit-hp", hud.Number(v.health) .. " / " .. hud.Number(v.maxHealth))
	end
	local parts = {}
	for i = 1, min(#v.cells, 6) do
		local c = v.cells[i]
		parts[i] = format('<div class="cell"><div class="label">%s</div><div class="figure">%s</div></div>',
			hud.Escape(c.label), hud.Escape(c.value))
	end
	local cells = table.concat(parts)
	if cells ~= shownCells then
		shownCells = cells
		view.Element("unit-cells").inner_rml = cells
	end
end

local function ShowGroup(v)
	SetText("group-name", v.total .. " units selected")
	SetClass("group-health", "hidden", v.maxHealth <= 0)
	if v.maxHealth > 0 then
		SetStyle("group-fill", "width", Percent(v.health / v.maxHealth))
		SetText("group-hp", hud.Number(v.health) .. " / " .. hud.Number(v.maxHealth))
	end
	groupTypes = v.types
	local parts = {}
	for i = 1, min(#v.types, MAX_GROUP_ICONS) do
		local e = v.types[i]
		parts[#parts + 1] = format('<div class="type" data-t="%d">%s<div class="count">%d</div></div>',
			i, hud.UnitPictureRML(e.defID, "pic"), e.count)
	end
	local types = table.concat(parts)
	if types ~= shownTypes then
		shownTypes = types
		view.Element("types").inner_rml = types
	end
end

local function ShowText(v)
	SetText("text-title", hud.Escape(v.title))
	SetText("text-body", (hud.Escape(v.text):gsub("\r?\n", "<br/>")))
end

local function Refresh()
	local v = Decide()
	if not v then
		ShowView(nil)
		return
	end
	ShowView(v.kind)
	if v.kind == "unit" then ShowUnit(v)
	elseif v.kind == "group" then ShowGroup(v)
	else ShowText(v) end
end

--------------------------------------------------------------------------------
-- group icons: select by type
--------------------------------------------------------------------------------

local function OnTypeClick(event)
	if event.parameters and event.parameters.button ~= 0 then return end
	local index = hud.EventAttribute(event, "data-t")
	local e = index and groupTypes[index]
	if not e then return end
	local alt, ctrl, _, shift = spGetModKeyState()
	local units
	if ctrl then
		units = spGetTeamUnitsByDefs(spGetMyTeamID(), e.defID) or {}
	else
		local sorted = spGetSelectedUnitsSorted() or {}
		units = sorted[e.defID] or {}
		if alt and units[1] then units = { units[1] } end
	end
	hud.Sound("click")
	spSelectUnitArray(units, shift and ctrl)
end

--------------------------------------------------------------------------------
-- placement
--------------------------------------------------------------------------------

local function DefaultOrigin(vsx, vsy, w, h, scale)
	return (vsx - w) * 0.5, hud.Margin() * scale
end

local function Place()
	hud.PlacePanel(view.Element("selection"), LAYOUT_NAME, WIDTH, HEIGHT, DefaultOrigin)
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
		Spring.Echo("[Slate Selection] " .. tostring(reason))
		widgetHandler:RemoveWidget()
		return
	end
	hud = helpers
	document = result
	view = hud.NewView(document)
	SetText, SetClass, SetStyle = view.SetText, view.SetClass, view.SetStyle
	view.Assume("selection", "hidden", true)
	view.Assume("unit", "hidden", true)
	view.Assume("group", "hidden", true)
	view.Assume("text", "hidden", true)

	view.Element("types"):AddEventListener("mousedown", OnTypeClick)

	Spring.SendCommands("tooltip 0")
	if Spring.SetDrawSelectionInfo then Spring.SetDrawSelectionInfo(false) end

	hud.RegisterPanel(LAYOUT_NAME, "Selection", Place, function() return shown ~= nil end)
	hud.OnChange(LAYOUT_NAME, Place)
	Place()
	Refresh()
	hud.ShowPassive(document)
	lastUpdate = Spring.GetTimer()
end

function widget:Shutdown()
	Spring.SendCommands("tooltip 1")
	if Spring.SetDrawSelectionInfo then Spring.SetDrawSelectionInfo(true) end
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

function widget:Update()
	if not document then return end
	if hud.FollowGuiHidden(document) then return end
	-- hover changes should feel instant; everything else can wait a moment
	local now = Spring.GetTimer()
	if S.hover ~= lastHover or Spring.DiffTimers(now, lastUpdate) >= UPDATE_INTERVAL then
		lastHover = S.hover
		lastUpdate = now
		Refresh()
	end
end
