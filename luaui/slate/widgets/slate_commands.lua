-- Part of Slate, a game-neutral RmlUi interface for Total Annihilation style
-- games on the Recoil engine. Derived from the Bastion HUD in Splinter
-- Faction (same author, GPL v2+).

function widget:GetInfo()
	return {
		name    = "Slate Build and Order Menu",
		desc    = "Build grid with category filters and paging, plus the order and unit-state buttons. Replaces the engine's command menu.",
		author  = "Scary le Poo",
		date    = "2026-10-24",
		license = "GNU GPL, v2 or later",
		layer   = 0,
		enabled = true,
		handler = true, -- the real widgetHandler: this widget takes over the command layout
	}
end

--------------------------------------------------------------------------------
--  Two panels at the bottom left. The orders panel holds the selected units'
--  commands (move, attack...) five to a row, and under them the unit states
--  (fire at will, hold fire...), each naming the state it is in with a row
--  of pips showing which one of how many. The build panel stands on the
--  orders panel: a header with the builder's name and the page, a row of
--  category chips from slate_game.lua, and a grid of build tiles with the
--  metal cost, the hotkey and how many are queued.
--
--  Left click gives the command, right click on a build tile takes one off
--  the queue, and the modifier keys work as they do everywhere else. The
--  mouse wheel over the build panel turns the page.
--
--  The selection panel is told what the mouse is over (WG.Slate.hover), and
--  the hotbind widget which action a Ctrl+Insert would bind
--  (WG.Slate.hoverAction). WG.SlateCommands gives other widgets the hovered
--  command and the panels' rectangles.
--------------------------------------------------------------------------------

local DOCUMENT_PATH = "commands.rml"
local QUEUE_INTERVAL = 0.25

-- must match #build and #orders in commands.rml
local PANEL_WIDTH  = 300
local BUILD_HEIGHT = 452
local PAD          = 10
local BORDER       = 1  -- .panel border in theme.rcss; inside the border-box width
local GAP          = 6
-- the width the rows of tiles have to fit in
local INNER_WIDTH  = PANEL_WIDTH - PAD * 2 - BORDER * 2
local HEADER_H     = 28
local CHIP_H       = 30
local ORDER_HEAD_H = 22
local ORDER_H      = 38
local STATE_H      = 44
local ORDER_MIN_H  = 264

local LAYOUT_BUILD = "slate_buildmenu"
local LAYOUT_ORDER = "slate_ordermenu"

local spGetActiveCmdDescs = Spring.GetActiveCmdDescs
local spGetActiveCommand  = Spring.GetActiveCommand
local spGetCmdDescIndex   = Spring.GetCmdDescIndex
local spSetActiveCommand  = Spring.SetActiveCommand
local spGetModKeyState    = Spring.GetModKeyState
local spGetSelectedUnits  = Spring.GetSelectedUnits
local spGetUnitDefID      = Spring.GetUnitDefID
local spGetFullBuildQueue = Spring.GetFullBuildQueue
local spGetActionHotKeys  = Spring.GetActionHotKeys
local spForceLayoutUpdate = Spring.ForceLayoutUpdate
local spGetMouseState     = Spring.GetMouseState

local floor, ceil = math.floor, math.ceil
local min, max = math.min, math.max
local concat = table.concat

local hud, S
local document
local view

local dirty = true
local builds, orders, states = {}, {}, {}
local filtered = {}                 -- builds after the category filter
local chips = {}                    -- { label, cat } ; cat == nil is "All"
local filter = nil                  -- selected category table, nil = All
local page, pageCount = 1, 1
local buildSignature = ""           -- which builder: a change resets filter and page
local builderName = ""
local queued = {}                   -- unitDefID -> count in the selected factory's queue
local queueTimer = 0
local activeCmdID
local showBuild, showOrders = false, false

local shownGrid, shownChips, shownOrders, shownStates -- what the markup was made from
local pageCards = {}                -- build cmds on the current page; tile i has data-b="i"
local hovered                       -- { kind = "build"|"order"|"state", cmd = } while the mouse is on a button
local buildRect, orderRect          -- {x1, y1, x2, y2} in screen pixels, y up
local orderHeight = ORDER_MIN_H

-- Taking over the menu makes the engine flag every command as hidden, so the
-- commands the game itself hides are noted before that happens.
local reallyHidden = {}

--------------------------------------------------------------------------------
-- Command list
--------------------------------------------------------------------------------

local function CleanName(name)
	name = (name or ""):gsub("\255...", ""):gsub("[\r\n]+", " ")
	return name
end

local function HotKey(action)
	if not action or action == "" or not spGetActionHotKeys then return nil end
	local keys = spGetActionHotKeys(action)
	local k = keys and keys[1]
	if not k then return nil end
	k = k:gsub("^[Aa]ny%+", ""):gsub("sc_", ""):upper()
	if #k > 5 then return nil end
	return k
end

local function Refresh()
	dirty = false
	builds, orders, states = {}, {}, {}
	local hidden = S.game.hiddenCommands or {}
	local descs = spGetActiveCmdDescs() or {}

	for i = 1, #descs do
		local cmd = descs[i]
		local t = cmd.type
		if not reallyHidden[cmd.id] and t ~= CMDTYPE.PREV and t ~= CMDTYPE.NEXT and not hidden[cmd.action or ""] then
			if cmd.id < 0 then
				if UnitDefs[-cmd.id] then
					cmd.slateKey = HotKey(cmd.action)
					builds[#builds + 1] = cmd
				end
			elseif t == CMDTYPE.ICON_MODE and cmd.params and #cmd.params > 1 then
				cmd.slateKey = HotKey(cmd.action)
				states[#states + 1] = cmd
			elseif (cmd.name and cmd.name ~= "") or (cmd.texture and cmd.texture ~= "") then
				cmd.slateLabel = CleanName(cmd.name)
				cmd.slateKey = HotKey(cmd.action)
				orders[#orders + 1] = cmd
			end
		end
	end

	-- A different builder: back to the first page of "All".
	local sig = #builds .. ":" .. (builds[1] and builds[1].id or 0) .. ":" .. (builds[#builds] and builds[#builds].id or 0)
	if sig ~= buildSignature then
		buildSignature = sig
		filter, page = nil, 1
	end

	chips = { { label = "All" } }
	local cats = S.game.buildCategories or {}
	for c = 1, #cats do
		local cat = cats[c]
		for i = 1, #builds do
			if cat.match(UnitDefs[-builds[i].id]) then
				chips[#chips + 1] = { label = cat.label, cat = cat }
				break
			end
		end
	end
	if #chips <= 2 then chips = {} ; filter = nil end   -- one category is no choice

	filtered = {}
	for i = 1, #builds do
		if not filter or filter.match(UnitDefs[-builds[i].id]) then
			filtered[#filtered + 1] = builds[i]
		end
	end

	local perPage = (S.game.buildColumns or 4) * (S.game.buildRows or 5)
	pageCount = max(1, ceil(#filtered / perPage))
	page = min(max(1, page), pageCount)

	local sel = spGetSelectedUnits() or {}
	local firstDef, same = nil, true
	for i = 1, #sel do
		local d = spGetUnitDefID(sel[i])
		if firstDef == nil then firstDef = d elseif d ~= firstDef then same = false ; break end
	end
	if #sel == 0 then
		builderName = ""
	elseif same and firstDef and UnitDefs[firstDef] then
		builderName = hud.UnitName(UnitDefs[firstDef])
	else
		builderName = #sel .. " units"
	end

	showBuild = #builds > 0
	showOrders = (#orders + #states) > 0
end

local function RefreshQueue()
	queued = {}
	if #builds == 0 or not spGetFullBuildQueue then return end
	local sel = spGetSelectedUnits() or {}
	for i = 1, #sel do
		local ud = UnitDefs[spGetUnitDefID(sel[i]) or -1]
		if ud and ud.isFactory then
			local q = spGetFullBuildQueue(sel[i]) or {}
			for j = 1, #q do
				for defID, count in pairs(q[j]) do
					queued[defID] = (queued[defID] or 0) + count
				end
			end
			return
		end
	end
end

--------------------------------------------------------------------------------
-- Engine menu takeover
--------------------------------------------------------------------------------

local function HideEngineMenu()
	local function layoutHandler(xIcons, yIcons, cmdCount, commands)
		reallyHidden = {}
		for i = 1, cmdCount do
			local c = commands[i]
			if c and c.hidden then reallyHidden[c.id] = true end
		end
		widgetHandler.commands = commands
		widgetHandler.commands.n = cmdCount
		widgetHandler:CommandsChanged()
		local customCmds = widgetHandler.customCommands
		return "", xIcons, yIcons, {}, customCmds, {}, {}, {}, {}, {}, { [1337] = 9001 }
	end
	widgetHandler:ConfigLayoutHandler(layoutHandler)
	spForceLayoutUpdate()
end

--------------------------------------------------------------------------------
-- Markup
--------------------------------------------------------------------------------

local function TileSize()
	local cols = S.game.buildColumns or 4
	local rows = S.game.buildRows or 5
	local w = floor((INNER_WIDTH - GAP * (cols - 1)) / cols)
	local avail = BUILD_HEIGHT - PAD * 2 - BORDER * 2 - HEADER_H - GAP - ((#chips > 0) and (CHIP_H + GAP) or 0)
	local h = floor((avail - GAP * (rows - 1)) / rows)
	return cols, rows, w, min(w, h)
end

local function ShowChips()
	local parts = {}
	for i = 1, #chips do
		local c = chips[i]
		parts[i] = string.format('<div class="chip tile%s%s" data-c="%d">%s</div>',
			(c.cat == filter) and " active" or "", (i == #chips) and " last" or "", i, hud.Escape(c.label))
	end
	local signature = concat(parts)
	if signature ~= shownChips then
		shownChips = signature
		view.Element("chips").inner_rml = signature
	end
	view.SetClass("chips", "hidden", #chips == 0)
end

local function ShowGrid()
	local cols, rows, w, h = TileSize()
	local first = (page - 1) * cols * rows
	pageCards = {}
	local parts = {}
	for i = 1, cols * rows do
		local cmd = filtered[first + i]
		if not cmd then break end
		pageCards[i] = cmd
		local defID = -cmd.id
		local ud = UnitDefs[defID]
		local last = (i % cols == 0) and " last" or ""
		parts[#parts + 1] = string.format('<div id="b%d" class="card tile%s" data-b="%d" style="width: %ddp; height: %ddp;">', i, last, i, w, h)
		parts[#parts + 1] = hud.UnitPictureRML(defID, "pic")
		parts[#parts + 1] = string.format('<div class="cost">%s</div>', hud.Cost(ud.metalCost or 0))
		if cmd.slateKey then
			parts[#parts + 1] = string.format('<div class="key">%s</div>', hud.Escape(cmd.slateKey))
		end
		parts[#parts + 1] = string.format('<div id="b%d-q" class="queue hidden"/>', i)
		parts[#parts + 1] = '</div>'
	end
	local signature = concat(parts)
	if signature ~= shownGrid then
		shownGrid = signature
		view.Element("grid").inner_rml = signature
		view.Forget()
		hovered = nil
	end
	view.SetText("builder", hud.Escape(builderName))
	view.SetClass("pager", "hidden", pageCount <= 1)
	view.SetText("pageno", page .. " / " .. pageCount)
	view.SetClass("prev", "off", page <= 1)
	view.SetClass("next", "off", page >= pageCount)
end

local function ShowOrders()
	local oCols = S.game.orderColumns or 5
	local sCols = S.game.stateColumns or 4
	local ow = floor((INNER_WIDTH - GAP * (oCols - 1)) / oCols)
	local sw = floor((INNER_WIDTH - GAP * (sCols - 1)) / sCols)

	local parts = {}
	for i = 1, #orders do
		local cmd = orders[i]
		local last = (i % oCols == 0) and " last" or ""
		parts[#parts + 1] = string.format('<div id="o%d" class="order tile%s%s" data-o="%d" style="width: %ddp;">', i, last, cmd.disabled and " disabled" or "", i, ow)
		if cmd.slateLabel ~= "" then
			parts[#parts + 1] = string.format('<div class="cap">%s</div>', hud.Escape(cmd.slateLabel))
		elseif cmd.texture and cmd.texture ~= "" then
			parts[#parts + 1] = string.format('<img class="oicon" src="/%s"/>', cmd.texture)
		end
		if cmd.slateKey then
			parts[#parts + 1] = string.format('<div class="okey">%s</div>', hud.Escape(cmd.slateKey))
		end
		parts[#parts + 1] = '</div>'
	end
	local signature = concat(parts)
	if signature ~= shownOrders then
		shownOrders = signature
		view.Element("order-grid").inner_rml = signature
		view.Forget()
		hovered = nil
	end

	parts = {}
	for i = 1, #states do
		local cmd = states[i]
		local cur = tonumber(cmd.params[1]) or 0
		local count = #cmd.params - 1
		local label = CleanName(cmd.params[cur + 2] or cmd.name)
		-- pips: how far along the options this state is (on/off shows one pip)
		local pips = (count == 2) and 1 or count
		local lit = (count == 2) and cur or (cur + 1)
		local pipW = min(14, floor((sw - 10 - (pips - 1) * 2) / max(1, pips)))
		local last = (i % sCols == 0) and " last" or ""
		parts[#parts + 1] = string.format('<div id="s%d" class="state tile%s%s" data-s="%d" style="width: %ddp;">', i, last, cmd.disabled and " disabled" or "", i, sw)
		parts[#parts + 1] = string.format('<div class="cap">%s</div><div class="pips">', hud.Escape(label))
		for p = 1, pips do
			parts[#parts + 1] = string.format('<div class="pip%s" style="width: %ddp;"/>', (p <= lit) and " lit" or "", pipW)
		end
		parts[#parts + 1] = '</div></div>'
	end
	signature = concat(parts)
	if signature ~= shownStates then
		shownStates = signature
		view.Element("state-grid").inner_rml = signature
		view.Forget()
		hovered = nil
	end

	-- the panel is as tall as its rows need
	local oRows, sRows = ceil(#orders / oCols), ceil(#states / sCols)
	local h = PAD * 2 + BORDER * 2 + ORDER_HEAD_H + GAP + oRows * (ORDER_H + GAP) + sRows * (STATE_H + GAP)
	return max(ORDER_MIN_H, h)
end

-- everything about a tile that changes without the list changing
local function RefreshTiles()
	for i = 1, #pageCards do
		local cmd = pageCards[i]
		local n = queued[-cmd.id] or 0
		local id = "b" .. i
		if n > 0 then
			view.SetText(id .. "-q", tostring(n))
		end
		view.SetClass(id .. "-q", "hidden", n <= 0)
		view.SetClass(id, "disabled", cmd.disabled and true or false)
		view.SetClass(id, "active", cmd.id == activeCmdID)
	end
	for i = 1, #orders do
		view.SetClass("o" .. i, "active", orders[i].id == activeCmdID)
	end
	view.SetClass("build", "hidden", not showBuild)
	view.SetClass("orders", "hidden", not showOrders)
end

--------------------------------------------------------------------------------
-- Placement
--------------------------------------------------------------------------------

local Place

local function OrderOrigin(vsx, vsy, w, h, scale)
	return hud.Margin() * scale, hud.Margin() * scale
end

-- the build menu stands on the orders menu and follows it if it is moved, so
-- it stays put whatever shape the minimap takes
local function BuildOrigin(vsx, vsy, w, h, scale)
	if orderRect then
		return orderRect[1], orderRect[4] + hud.Gap() * scale
	end
	return hud.Margin() * scale, (hud.Margin() + ORDER_MIN_H + hud.Gap()) * scale
end

Place = function()
	local ordersEl = view.Element("orders")
	ordersEl.style["height"] = orderHeight .. "dp"
	local x, y, w, h = hud.PlacePanel(ordersEl, LAYOUT_ORDER, PANEL_WIDTH, orderHeight, OrderOrigin)
	orderRect = x and { x, y, x + w, y + h }
	x, y, w, h = hud.PlacePanel(view.Element("build"), LAYOUT_BUILD, PANEL_WIDTH, BUILD_HEIGHT, BuildOrigin)
	buildRect = x and { x, y, x + w, y + h }
end

local function InRect(rect, x, y)
	return rect and x >= rect[1] and x <= rect[3] and y >= rect[2] and y <= rect[4]
end

--------------------------------------------------------------------------------
-- Rebuilding
--------------------------------------------------------------------------------

local function Rebuild()
	Refresh()
	RefreshQueue()
	ShowChips()
	ShowGrid()
	local h = ShowOrders()
	if h ~= orderHeight then
		orderHeight = h
		Place()
	end
	RefreshTiles()
end

--------------------------------------------------------------------------------
-- Hover and clicks
--------------------------------------------------------------------------------

local function SetHover(kind, cmd)
	if cmd and kind == "build" then
		local ud = UnitDefs[-cmd.id]
		S.hover = { unitDefID = -cmd.id }
		S.hoverAction = (cmd.action and cmd.action ~= "") and { action = cmd.action, label = hud.UnitName(ud) } or nil
	elseif cmd then
		S.hover = { title = CleanName(cmd.name), text = cmd.tooltip }
		S.hoverAction = (cmd.action and cmd.action ~= "") and { action = cmd.action, label = CleanName(cmd.name) } or nil
	elseif hovered then
		S.hover = nil
		S.hoverAction = nil
	end
	hovered = cmd and { kind = kind, cmd = cmd } or nil
end

local function Apply(cmd, button)
	local index = spGetCmdDescIndex(cmd.id)
	if not index then return end
	local alt, ctrl, meta, shift = spGetModKeyState()
	spSetActiveCommand(index, button, button == 1, button == 3, alt, ctrl, meta, shift)
end

-- RmlUi numbers the buttons left 0, right 1, middle 2; the engine 1, 3, 2
local ENGINE_BUTTON = { [0] = 1, [1] = 3, [2] = 2 }

local function Listen(containerId, attribute, kind, list)
	local container = view.Element(containerId)
	if not container then return end
	container:AddEventListener("mousedown", function(event)
		local index = hud.EventAttribute(event, attribute)
		local cmd = index and list()[index]
		local button = ENGINE_BUTTON[event.parameters and event.parameters.button]
		if not cmd or not button then return end
		-- a click while the hotbind prompt is up cancels the prompt and does
		-- nothing else, so a mis-triggered capture never eats a build order
		local hotbind = WG.SlateHotbind
		if hotbind and hotbind.IsCapturing and hotbind.IsCapturing() then
			hotbind.Cancel()
			return
		end
		if cmd.disabled then return end
		hud.Sound("click")
		Apply(cmd, button)
		dirty = true
	end)
	container:AddEventListener("mouseover", function(event)
		local index = hud.EventAttribute(event, attribute)
		local cmd = index and list()[index]
		if cmd then
			if not hovered or hovered.cmd ~= cmd then
				hud.Sound("hover")
			end
			SetHover(kind, cmd)
		else
			SetHover(kind, nil)
		end
	end)
	container:AddEventListener("mouseout", function()
		SetHover(kind, nil)
	end)
end

local function TurnPage(delta)
	local p = min(pageCount, max(1, page + delta))
	if p ~= page then
		page = p
		dirty = true
	end
end

--------------------------------------------------------------------------------
-- Widget callins
--------------------------------------------------------------------------------

function widget:Initialize()
	S = WG.Slate
	if not S then
		widgetHandler:RemoveWidget(self)
		return
	end
	local helpers = include("slate/rml/core.lua")
	local result, reason = helpers.LoadDocument(DOCUMENT_PATH, widget)
	if not result then
		Spring.Echo("[Slate Build Menu] " .. tostring(reason))
		widgetHandler:RemoveWidget(self)
		return
	end
	hud = helpers
	document = result
	view = hud.NewView(document)
	view.Assume("build", "hidden", true) -- set in the markup
	view.Assume("orders", "hidden", true)
	view.Assume("chips", "hidden", true)
	view.Assume("pager", "hidden", true)

	Listen("grid", "data-b", "build", function() return pageCards end)
	Listen("order-grid", "data-o", "order", function() return orders end)
	Listen("state-grid", "data-s", "state", function() return states end)

	local chipsEl = view.Element("chips")
	chipsEl:AddEventListener("mousedown", function(event)
		if event.parameters and event.parameters.button ~= 0 then return end
		local index = hud.EventAttribute(event, "data-c")
		local chip = index and chips[index]
		if chip then
			hud.Sound("click")
			filter = chip.cat
			page = 1
			dirty = true
		end
	end)
	hud.OnClick(view, "prev", function() hud.Sound("click") ; TurnPage(-1) end)
	hud.OnClick(view, "next", function() hud.Sound("click") ; TurnPage(1) end)
	view.Element("build"):AddEventListener("mousescroll", function(event)
		local delta = event.parameters and (event.parameters.wheel_delta_y or event.parameters.wheel_delta)
		if delta and delta ~= 0 then
			TurnPage((delta > 0) and 1 or -1)
		end
	end)

	WG.SlateCommands = {
		-- the command under the mouse and whether it is disabled, or nil
		GetHovered = function()
			local cmd = hovered and hovered.cmd
			if not cmd then return nil end
			local visible = (hovered.kind == "build" and showBuild) or (hovered.kind ~= "build" and showOrders)
			if not visible then return nil end
			return cmd, (cmd.disabled and true or false)
		end,
		-- the panels' rectangles in screen pixels (y up)
		GetOrderRect = function()
			if orderRect then return orderRect[1], orderRect[2], orderRect[3], orderRect[4] end
		end,
		GetBuildRect = function()
			if buildRect then return buildRect[1], buildRect[2], buildRect[3], buildRect[4] end
		end,
		-- nil while the mouse is off both panels; otherwise the tooltip of the
		-- command under it, or "" between the buttons
		GetTooltip = function()
			if not document or Spring.IsGUIHidden() then return nil end
			local mx, my = spGetMouseState()
			if not ((showOrders and InRect(orderRect, mx, my)) or (showBuild and InRect(buildRect, mx, my))) then
				return nil
			end
			local cmd = hovered and hovered.cmd
			return cmd and (cmd.tooltip or "") or ""
		end,
	}

	hud.RegisterPanel(LAYOUT_ORDER, "Orders", Place)
	hud.RegisterPanel(LAYOUT_BUILD, "Build menu", Place)
	hud.OnChange(LAYOUT_BUILD, function() Place() ; dirty = true end)
	Place()

	HideEngineMenu()
	Rebuild()
	hud.ShowPassive(document)
end

function widget:Shutdown()
	widgetHandler:ConfigLayoutHandler(true)
	spForceLayoutUpdate()
	WG.SlateCommands = nil
	if S and hovered then
		S.hover = nil
		S.hoverAction = nil
	end
	if hud then
		hud.UnregisterPanel(LAYOUT_ORDER)
		hud.UnregisterPanel(LAYOUT_BUILD)
		hud.OffChange(LAYOUT_BUILD)
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

function widget:CommandsChanged()  dirty = true end
function widget:SelectionChanged() dirty = true end

function widget:Update(dt)
	if not document then return end
	if hud.FollowGuiHidden(document) then
		SetHover(nil, nil)
		return -- hidden with the rest of the GUI (F5)
	end
	local _, cmdID = spGetActiveCommand()
	queueTimer = queueTimer + dt
	if dirty then
		activeCmdID = cmdID
		queueTimer = 0
		Rebuild()
	elseif queueTimer > QUEUE_INTERVAL then
		queueTimer = 0
		activeCmdID = cmdID
		RefreshQueue()
		RefreshTiles()
	elseif cmdID ~= activeCmdID then
		activeCmdID = cmdID
		RefreshTiles()
	end
end
