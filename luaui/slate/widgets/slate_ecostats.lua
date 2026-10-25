-- Part of Slate, a game-neutral RmlUi interface for Total Annihilation style
-- games on the Recoil engine. Derived from the Bastion HUD in Splinter
-- Faction (same author, GPL v2+).

function widget:GetInfo()
	return {
		name    = "Slate Eco Stats",
		desc    = "For spectators: every team's economy side by side, with totals per alliance. Hidden while you are playing.",
		author  = "Scary le Poo",
		date    = "2026-10-24",
		license = "GNU GPL, v2 or later",
		layer   = 7,
		enabled = true,
	}
end

--------------------------------------------------------------------------------
--  One panel at the top right, under the menu button, for spectators only.
--  Each alliance is a group: a head with the alliance's total income per
--  resource and a bar comparing it with the strongest alliance, then a row
--  per team with its colour, name, income and stored amount per resource,
--  and a bar comparing its income with the strongest team.
--
--  The markup is rebuilt only when the set of teams changes; the figures are
--  restated twice a second through the view, which only touches what moved.
--------------------------------------------------------------------------------

local DOCUMENT_PATH = "ecostats.rml"
local UPDATE_INTERVAL = 0.5
local LAYOUT_NAME = "slate_ecostats"

-- must match ecostats.rml: #ecostats width, and the heights that add up
local PANEL_WIDTH = 340
local PAD_Y       = 10    -- top and bottom padding of #ecostats
local HEAD_H      = 42    -- an alliance head (.ghead)
local ROW_H       = 24    -- a team row (.trow)
local GROUP_GAP   = 8     -- below each group (.group margin-bottom)
local MENU_CLEARANCE = 30 -- the menu button sits in the corner above this panel

local spGetTeamResources = Spring.GetTeamResources
local spGetTeamInfo      = Spring.GetTeamInfo
local spGetTeamColor     = Spring.GetTeamColor
local spGetAllyTeamList  = Spring.GetAllyTeamList
local spGetTeamList      = Spring.GetTeamList
local spGetGaiaTeamID    = Spring.GetGaiaTeamID
local spGetSpectatingState = Spring.GetSpectatingState

local format = string.format
local max = math.max

local hud, S
local document
local view
local SetText, SetClass, SetStyle
local lastUpdate
local active = false     -- a spectator is looking: the panel is on screen
local resources = {}     -- from WG.Slate.game.resources: { key, label, color }
local groups = {}        -- { ally, teams = { { teamID, name, color, dead } } }
local shownKey           -- the team set the markup was built from
local shownHeight

--------------------------------------------------------------------------------
-- teams
--------------------------------------------------------------------------------

local function TeamName(teamID)
	local _, leader, _, isAI = spGetTeamInfo(teamID, false)
	if isAI then
		local _, aiName, _, shortName = Spring.GetAIInfo(teamID)
		return (aiName and aiName ~= "" and aiName ~= "UNKNOWN") and aiName or shortName or "AI"
	end
	return Spring.GetPlayerInfo(leader or -1, false) or ("Team " .. teamID)
end

-- Every alliance with at least one team, each team with its name and
-- colour. Also returns a key that changes when the set of teams does
-- (a team dying changes its row's look, so it is part of the key).
local function GatherTeams()
	local gaia = spGetGaiaTeamID()
	local list, keyParts = {}, {}
	for _, ally in ipairs(spGetAllyTeamList() or {}) do
		local group = { ally = ally, teams = {} }
		for _, teamID in ipairs(spGetTeamList(ally) or {}) do
			if teamID ~= gaia then
				local _, _, isDead = spGetTeamInfo(teamID, false)
				local r, g, b = spGetTeamColor(teamID)
				group.teams[#group.teams + 1] = {
					teamID = teamID, name = TeamName(teamID),
					color = { r or 1, g or 1, b or 1 }, dead = isDead and true or false,
				}
				keyParts[#keyParts + 1] = teamID .. (isDead and "d" or "")
			end
		end
		if #group.teams > 0 then
			list[#list + 1] = group
			keyParts[#keyParts + 1] = "|"
		end
	end
	return list, table.concat(keyParts, ",")
end

--------------------------------------------------------------------------------
-- markup: built once per team set
--------------------------------------------------------------------------------

-- ids: g<ally>-<key> total, g<ally>-<key>-fill bar; t<team>-<key>-inc,
-- t<team>-<key>-cur, t<team>-<key>-fill
local function PanelRML()
	local parts = {}
	for gi, group in ipairs(groups) do
		parts[#parts + 1] = '<div class="group">'
		parts[#parts + 1] = format('<div class="ghead"><div class="gtop"><div class="label">Alliance %d</div>', gi)
		for _, res in ipairs(resources) do
			parts[#parts + 1] = format('<div class="col"><div id="g%d-%s" class="strong gtotal"/></div>', group.ally, res.key)
		end
		parts[#parts + 1] = '</div><div class="gbars"><div class="name"/>'
		for _, res in ipairs(resources) do
			parts[#parts + 1] = format('<div class="col"><div class="bar"><div id="g%d-%s-fill" class="bar-fill" style="background-color: %s;"/></div></div>',
				group.ally, res.key, res.color or "#a9bdd0")
		end
		parts[#parts + 1] = '</div></div>'
		for _, team in ipairs(group.teams) do
			local c = team.color
			parts[#parts + 1] = format('<div class="trow%s"><div class="name"><div class="sw" style="background-color: %s;"/><div class="tname" style="color: %s;">%s</div></div>',
				team.dead and " dead" or "", hud.Rgb(c[1], c[2], c[3]), hud.ReadableColor(c[1], c[2], c[3]), hud.Escape(team.name))
			for _, res in ipairs(resources) do
				parts[#parts + 1] = format(
					'<div class="col"><div class="figures"><div id="t%d-%s-inc" class="inc"/><div id="t%d-%s-cur" class="sub cur"/></div>'
					.. '<div class="bar"><div id="t%d-%s-fill" class="bar-fill" style="background-color: %s;"/></div></div>',
					team.teamID, res.key, team.teamID, res.key, team.teamID, res.key, res.color or "#a9bdd0")
			end
			parts[#parts + 1] = '</div>'
		end
		parts[#parts + 1] = '</div>'
	end
	return table.concat(parts)
end

local function PanelHeight()
	local height = PAD_Y * 2
	for _, group in ipairs(groups) do
		height = height + HEAD_H + #group.teams * ROW_H + GROUP_GAP
	end
	return height
end

--------------------------------------------------------------------------------
-- placement
--------------------------------------------------------------------------------

local function DefaultOrigin(vsx, vsy, w, h, scale)
	local margin = hud.Margin() * scale
	return vsx - margin - w, vsy - margin - MENU_CLEARANCE * scale - hud.Gap() * scale - h
end

local function Place()
	local height = PanelHeight()
	if height ~= shownHeight then
		shownHeight = height
		view.Element("ecostats").style["height"] = height .. "dp"
	end
	hud.PlacePanel(view.Element("ecostats"), LAYOUT_NAME, PANEL_WIDTH, height, DefaultOrigin)
end

--------------------------------------------------------------------------------
-- refresh
--------------------------------------------------------------------------------

local function Percent(fraction)
	return format("%d%%", math.floor(max(0, math.min(1, fraction)) * 100 + 0.5))
end

local function Refresh()
	local spec = spGetSpectatingState() and true or false
	if spec ~= active then
		active = spec
		SetClass("ecostats", "hidden", not active)
	end
	if not active then return end

	local list, key = GatherTeams()
	if key ~= shownKey then
		shownKey = key
		groups = list
		view.Element("rows").inner_rml = PanelRML()
		view.Forget()
		view.Assume("ecostats", "hidden", false)
		Place()
	end

	-- income and stored amount per team, totals and bests per resource
	local income, current, totals = {}, {}, {}
	local bestTeam, bestAlly = {}, {}
	for _, res in ipairs(resources) do
		local k = res.key
		bestTeam[k], bestAlly[k] = 0, 0
		for _, group in ipairs(groups) do
			local total = 0
			for _, team in ipairs(group.teams) do
				local cur, _, _, inc = spGetTeamResources(team.teamID, k)
				inc = (not team.dead and inc) or 0
				income[team.teamID .. k] = inc
				current[team.teamID .. k] = cur or 0
				total = total + inc
				if inc > bestTeam[k] then bestTeam[k] = inc end
			end
			totals[group.ally .. k] = total
			if total > bestAlly[k] then bestAlly[k] = total end
		end
	end

	for _, group in ipairs(groups) do
		for _, res in ipairs(resources) do
			local k = res.key
			local total = totals[group.ally .. k]
			SetText("g" .. group.ally .. "-" .. k, "+" .. hud.Short(total))
			SetStyle("g" .. group.ally .. "-" .. k .. "-fill", "width", Percent(bestAlly[k] > 0 and total / bestAlly[k] or 0))
		end
		for _, team in ipairs(group.teams) do
			for _, res in ipairs(resources) do
				local k = res.key
				local id = "t" .. team.teamID .. "-" .. k
				local inc = income[team.teamID .. k]
				SetText(id .. "-inc", "+" .. hud.Short(inc))
				SetText(id .. "-cur", hud.Short(current[team.teamID .. k]))
				SetStyle(id .. "-fill", "width", Percent(bestTeam[k] > 0 and inc / bestTeam[k] or 0))
			end
		end
	end
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
	resources = S.game.resources or {}
	if #resources == 0 then
		Spring.Echo("[Slate Eco Stats] no resources in slate_game.lua")
		widgetHandler:RemoveWidget()
		return
	end
	local helpers = include("slate/rml/core.lua")
	local result, reason = helpers.LoadDocument(DOCUMENT_PATH, widget)
	if not result then
		Spring.Echo("[Slate Eco Stats] " .. tostring(reason))
		widgetHandler:RemoveWidget()
		return
	end
	hud = helpers
	document = result
	view = hud.NewView(document)
	SetText, SetClass, SetStyle = view.SetText, view.SetClass, view.SetStyle
	view.Assume("ecostats", "hidden", true)

	S.SetTip(LAYOUT_NAME, function(mx, my)
		if not active then return nil end
		local panel = view.Element("ecostats")
		local ok, left, top, w, h = pcall(function()
			return panel.absolute_left, panel.absolute_top, panel.offset_width, panel.offset_height
		end)
		if not ok or not w then return nil end
		local _, vsy = Spring.GetViewGeometry()
		local y = vsy - my
		if mx >= left and mx <= left + w and y >= top and y <= top + h then
			return "Eco stats", "Income per second and stored amount for every team. The bar under each alliance compares its total with the strongest alliance; the bar beside each team compares it with the strongest team."
		end
		return nil
	end)

	hud.RegisterPanel(LAYOUT_NAME, "Eco Stats", Place, function() return active end)
	hud.OnChange(LAYOUT_NAME, Place)
	Place()
	Refresh()
	hud.ShowPassive(document)
	lastUpdate = Spring.GetTimer()
end

function widget:Shutdown()
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

function widget:PlayerChanged()
	-- becoming a spectator (resign, /spectator) shows the panel right away
	if document then Refresh() end
end

function widget:Update()
	if not document then return end
	if hud.FollowGuiHidden(document) then return end
	local now = Spring.GetTimer()
	if Spring.DiffTimers(now, lastUpdate) >= UPDATE_INTERVAL then
		lastUpdate = now
		Refresh()
	end
end
