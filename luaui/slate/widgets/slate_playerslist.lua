-- Part of Slate, a game-neutral RmlUi interface for Total Annihilation style
-- games on the Recoil engine. Derived from the Bastion HUD in Splinter
-- Faction (same author, GPL v2+).

function widget:GetInfo()
	return {
		name    = "Slate Players List",
		desc    = "Players by alliance with resources, cpu/ping and fps; spectators; alliance offers; click an ally to share, spectator click-to-follow",
		author  = "Scary le Poo",
		date    = "2026-10-24",
		license = "GNU GPL, v2 or later",
		layer   = -4,
		enabled = true,
	}
end

--------------------------------------------------------------------------------
--  At the bottom right: game time, speed and fps; then every player grouped
--  by alliance, with their team's metal and energy bars (for teams you may
--  see), cpu and ping, and fps; then the spectators, folded away until their
--  header is clicked.
--
--  Click an ally to open the share window for that team. With dynamic
--  alliances on, each enemy row has a square: click it to offer or withdraw
--  an alliance. A spectator clicks a player to watch through that player's
--  camera. Hovering the cpu/ping cells shows the player's system.
--
--  The fps, system and camera of the other players come from Slate Broadcast
--  (WG.SlateBroadcast), so they only show for players running Slate.
--------------------------------------------------------------------------------

--------------------------------------------------------------------------------
-- config
--------------------------------------------------------------------------------

local DOCUMENT_PATH = "playerslist.rml"

-- must match playerslist.rml (all in dp)
local PANEL_WIDTH = 336
local CHROME      = 20  -- borders and padding, top and bottom
local TOPBAR      = 24
local ROW         = 19
local GROUP_GAP   = 7
local SPEC_HEADER = 20
local SPEC_ROW    = 16

local POPUP_GAP = 8

local LAYOUT_NAME = "slate_playerslist"

-- Rejoin/lag detection: the engine exposes no explicit "catching up" flag to
-- LuaUI, but a rejoining client's reported ping is its time-behind while it
-- replays the demo -- it sits at multiple seconds until caught up. So:
-- huge ping + recent disconnect->connect transition = rejoining; huge ping
-- without one = plain lagging. Clears itself once ping normalizes.
local REJOIN_PING_S  = 2.0    -- seconds behind => catching up / lagging
local REJOIN_GRACE_S = 120    -- how long after reconnect we call it "rejoining"

-- camera-lock behavior
local lockcameraHideEnemies = true
local lockcameraLos         = true
local transitionTime        = 0.6
local listTime              = 14   -- seconds since their last camera to still count a player as broadcasting

--------------------------------------------------------------------------------
-- locals
--------------------------------------------------------------------------------

local spGetPlayerInfo      = Spring.GetPlayerInfo
local spGetPlayerList      = Spring.GetPlayerList
local spGetTeamInfo        = Spring.GetTeamInfo
local spGetTeamColor       = Spring.GetTeamColor
local spGetTeamList        = Spring.GetTeamList
local spGetAllyTeamList    = Spring.GetAllyTeamList
local spGetTeamResources   = Spring.GetTeamResources
local spGetMyTeamID        = Spring.GetMyTeamID
local spGetMyAllyTeamID    = Spring.GetMyAllyTeamID
local spGetMyPlayerID      = Spring.GetMyPlayerID
local spGetSpectatingState = Spring.GetSpectatingState
local spAreTeamsAllied     = Spring.AreTeamsAllied
local spGetGaiaTeamID      = Spring.GetGaiaTeamID
local spGetGameFrame       = Spring.GetGameFrame
local spGetGameSpeed       = Spring.GetGameSpeed
local spGetFPS             = Spring.GetFPS
local spGetCameraState     = Spring.GetCameraState
local spSetCameraState     = Spring.SetCameraState
local spGetMapDrawMode     = Spring.GetMapDrawMode
local spSendCommands       = Spring.SendCommands
local spGetAIInfo          = Spring.GetAIInfo

local math_floor = math.floor
local math_max   = math.max
local math_min   = math.min
local osclock    = os.clock

local hud, S
local document
local view

--------------------------------------------------------------------------------
-- state
--------------------------------------------------------------------------------

local myTeamID, myAllyTeam, myPlayerID
local mySpecStatus, fullView
local drawAllyButton = false

local groups        = {}    -- ordered: { allyTeam, isEnemy, teams={ {teamID,...,rows={...}} } }
local specs         = {}    -- { {id, name} }
local rows          = {}    -- the player and AI rows, flat, in the order shown; row i has the id "r<i>"
local specsExpanded = false

local panelRect = {x1=0, y1=0, x2=0, y2=0}   -- screen pixels, y up

-- connection tracking (disconnect / rejoin)
local wasConnected  = {}   -- playerID -> last seen 'active' state
local reconnectTime = {}   -- playerID -> os.clock() of last false->true flip

-- camera lock state
local lockPlayerID
local appliedCamera        -- the camera state table last passed on to the engine
local myLastCameraState
local sceduledSpecFullView
local desiredLosmode
local desiredLosmodeChanged = 0

local contentDirty = true  -- set by the camera lock when the locked player changes
local refreshTimer = 0
local listSignature        -- what the rows' markup was made from
local specSignature
local shownHeight          -- the panel's height in dp, as last set
local hover                -- {kind = "ally" or "net", index = row, name = whose} while the mouse is on one

--------------------------------------------------------------------------------
-- helpers (carried over unchanged)
--------------------------------------------------------------------------------

-- Dark team colors are made readable by hud.ReadableColor; RefreshPlayers
-- still records which ones were dark.
local function IsDarkColor(r, g, b)
	return ((r or 1)*0.299 + (g or 1)*0.587 + (b or 1)*0.114) < 0.36
end

local function GetCpuLvl(c)
	if c < 0.15 then return 1 elseif c < 0.30 then return 2
	elseif c < 0.45 then return 3 elseif c < 0.65 then return 4 else return 5 end
end

local function GetPingLvl(p)
	if p < 0.15 then return 1 elseif p < 0.30 then return 2
	elseif p < 0.70 then return 3 elseif p < 1.50 then return 4 else return 5 end
end

-- Dynamic-alliance direction. Verified against engine behavior: issuing
-- "ally <theirAllyTeam> 1" (our outgoing offer) makes AreTeamsAllied(theirTeam, myTeam)
-- become true -- i.e. AreTeamsAllied(A, B) reports whether B has allied A. So:
--   our alliance toward team T  = AreTeamsAllied(T, myTeam)
--   their alliance toward us    = AreTeamsAllied(myTeam, T)
local function WeAllied(teamID)   return spAreTeamsAllied(teamID, myTeamID) end
local function TheyAllied(teamID) return spAreTeamsAllied(myTeamID, teamID) end

--------------------------------------------------------------------------------
-- what the other players' Slate told us (slate_broadcast.lua)
--------------------------------------------------------------------------------

local function Broadcast()
	return WG.SlateBroadcast
end

local function PlayerFps(playerID)
	local b = Broadcast()
	return b and tonumber(b.fps[playerID]) or nil
end

-- a table of lines, or nil
local function PlayerSystem(playerID)
	local b = Broadcast()
	return b and b.system[playerID] or nil
end

-- the newest camera state sent by this player, or nil
local function PlayerCamera(playerID)
	local b = Broadcast()
	local entry = b and b.camera[playerID]
	return entry and entry.state or nil
end

-- A player counts as broadcasting while their last camera is recent: only
-- those can be followed, so only their rows are offered to a spectator.
local function IsBroadcasting(playerID)
	local b = Broadcast()
	local entry = b and b.camera[playerID]
	return entry ~= nil and (b.now() - entry.time) <= listTime
end

--------------------------------------------------------------------------------
-- camera lock (a port from AdvPlayersList)
--------------------------------------------------------------------------------

local function LockCamera(playerID)
	if playerID and playerID ~= myPlayerID and playerID ~= lockPlayerID then
		if lockcameraHideEnemies and not select(3, spGetPlayerInfo(playerID, false)) then
			spSendCommands("specteam " .. select(4, spGetPlayerInfo(playerID, false)))
			if not fullView then
				sceduledSpecFullView = 1
				spSendCommands("specfullview")
			else
				sceduledSpecFullView = 2
				spSendCommands("specfullview")
			end
			if lockcameraLos and mySpecStatus and spGetMapDrawMode() ~= "los" then
				desiredLosmode = 'los'
				desiredLosmodeChanged = osclock()
			end
		elseif lockcameraHideEnemies and select(3, spGetPlayerInfo(playerID, false)) then
			if not fullView then
				spSendCommands("specfullview")
			end
			desiredLosmode = 'normal'
			desiredLosmodeChanged = osclock()
		end
		lockPlayerID = playerID
		myLastCameraState = myLastCameraState or spGetCameraState()
		appliedCamera = PlayerCamera(lockPlayerID)
		if appliedCamera then
			spSetCameraState(appliedCamera, transitionTime)
		end
	else
		if myLastCameraState then
			spSetCameraState(myLastCameraState, transitionTime)
			myLastCameraState = nil
		end
		if lockcameraHideEnemies and lockPlayerID and not select(3, spGetPlayerInfo(lockPlayerID, false)) then
			if not fullView then
				spSendCommands("specfullview")
			end
			if lockcameraLos and mySpecStatus and spGetMapDrawMode() == "los" then
				desiredLosmode = 'normal'
				desiredLosmodeChanged = osclock()
			end
		end
		lockPlayerID = nil
		appliedCamera = nil
	end
	contentDirty = true
end

-- Every frame while locked: pass on each new camera state as it arrives
-- (Slate Broadcast makes a new table per message, so a change of table is a
-- new state), and let go of a player who stopped broadcasting.
local function FollowCamera()
	if not lockPlayerID then
		return
	end
	if not IsBroadcasting(lockPlayerID) then
		LockCamera()
		return
	end
	local state = PlayerCamera(lockPlayerID)
	if state and state ~= appliedCamera then
		appliedCamera = state
		spSetCameraState(state, transitionTime)
	end
end

--------------------------------------------------------------------------------
-- reading the players (carried over unchanged)
--------------------------------------------------------------------------------

local function GetTeamDisplayName(teamID, leader, isAI)
	if isAI then
		local _, botID, _, shortName = spGetAIInfo(teamID)
		if botID then return tostring(botID) .. " (" .. tostring(shortName) .. ")" end
		return "AI " .. teamID
	end
	local name = spGetPlayerInfo(leader, false)
	return name or ("Team " .. teamID)
end

local function RefreshPlayers()
	myTeamID    = spGetMyTeamID()
	myAllyTeam  = spGetMyAllyTeamID()
	myPlayerID  = spGetMyPlayerID()
	mySpecStatus, fullView = spGetSpectatingState()
	-- the engine only takes "ally" commands with the fixedallies mod option
	-- switched off (it is on when the game does not set it)
	local fixedallies = tostring(Spring.GetModOptions().fixedallies or "1"):lower()
	drawAllyButton = (fixedallies == "0" or fixedallies == "false") and not mySpecStatus
	local gaia = spGetGaiaTeamID and spGetGaiaTeamID() or -1

	-- human players grouped by team
	local teamPlayers = {}
	specs = {}
	for _, pid in ipairs(spGetPlayerList() or {}) do
		local name, active, spec, teamID, _, ping, cpu = spGetPlayerInfo(pid, false)
		-- disconnect -> reconnect transition marks a rejoin in progress
		if wasConnected[pid] == false and active then
			reconnectTime[pid] = osclock()
		end
		wasConnected[pid] = active or false
		if spec then
			-- disconnected specs stay in GetPlayerList with active=false; hide them
			if active then
				specs[#specs+1] = {id = pid, name = name or ("Player " .. pid)}
			end
		else
			-- disconnected players also stay in the list; keep their row, tag it
			teamPlayers[teamID] = teamPlayers[teamID] or {}
			teamPlayers[teamID][#teamPlayers[teamID]+1] = {
				id = pid, name = name or ("Player "..pid),
				ping = ping or 0, cpu = cpu or 0, connected = active or false,
			}
		end
	end

	-- ordered allyteams: own first (if a player), then ascending, skipping gaia-only
	local allyList = spGetAllyTeamList() or {}
	local order = {}
	local seen = {}
	local function addAlly(at)
		if at ~= nil and not seen[at] then seen[at] = true ; order[#order+1] = at end
	end
	if not mySpecStatus then addAlly(myAllyTeam) end
	for _, at in ipairs(allyList) do addAlly(at) end

	groups = {}
	for _, allyTeam in ipairs(order) do
		local teamsInAlly = spGetTeamList(allyTeam) or {}
		local groupTeams = {}
		for _, teamID in ipairs(teamsInAlly) do
			if teamID ~= gaia then
				local _, leader, isDead, isAI = spGetTeamInfo(teamID, false)
				local r, g, b = spGetTeamColor(teamID)
				local color = {r or 1, g or 1, b or 1}
				local dark = IsDarkColor(r, g, b)

				-- resources (gated: spec sees all; player sees own + anyone we're
				-- allied with, including dynamic allies). The nil-check below still
				-- guards if the engine declines a given team.
				local readable = mySpecStatus or spAreTeamsAllied(myTeamID, teamID)
				local mCur, mMax, eCur, eMax
				if readable then
					local m, ms = spGetTeamResources(teamID, "metal")
					local e, es = spGetTeamResources(teamID, "energy")
					if m then mCur, mMax = m, math_max(ms or 1, 1) end
					if e then eCur, eMax = e, math_max(es or 1, 1) end
				end

				local teamRows = {}
				local plist = teamPlayers[teamID]
				if plist and #plist > 0 then
					for _, p in ipairs(plist) do
						teamRows[#teamRows+1] = {
							kind = "player", playerID = p.id, name = p.name,
							ping = p.ping, cpu = p.cpu, isAI = false,
							connected = p.connected,
						}
					end
				elseif isAI then
					teamRows[#teamRows+1] = {
						kind = "ai", playerID = nil, name = GetTeamDisplayName(teamID, leader, true), isAI = true,
					}
				end

				if #teamRows > 0 then
					groupTeams[#groupTeams+1] = {
						teamID = teamID, allyTeam = allyTeam, color = color, dark = dark, dead = isDead,
						readable = readable, mCur = mCur, mMax = mMax, eCur = eCur, eMax = eMax,
						rows = teamRows,
					}
				end
			end
		end
		if #groupTeams > 0 then
			groups[#groups+1] = {
				allyTeam = allyTeam,
				isEnemy  = (not mySpecStatus) and (allyTeam ~= myAllyTeam),
				teams    = groupTeams,
			}
		end
	end
end

--------------------------------------------------------------------------------
-- markup
--------------------------------------------------------------------------------

-- The rows in the order they are shown, with their team's data on each.
local function FlattenRows()
	rows = {}
	for _, group in ipairs(groups) do
		for _, team in ipairs(group.teams) do
			for _, r in ipairs(team.rows) do
				rows[#rows + 1] = {
					kind = r.kind, playerID = r.playerID, name = r.name,
					ping = r.ping, cpu = r.cpu, connected = r.connected,
					team = team, isEnemy = group.isEnemy,
				}
			end
		end
	end
end

local function RowRML(i, row)
	local color = row.team.color
	local parts = {string.format('<div id="r%d" class="prow" data-r="%d">', i, i)}
	if drawAllyButton and row.isEnemy then
		parts[#parts + 1] = string.format('<div id="r%d-ally" class="ally" data-ally="%d"/>', i, i)
	end
	parts[#parts + 1] = string.format('<div class="pname" style="color: %s;">%s</div><div id="r%d-tag" class="ptag"/><div class="grow"/>',
		hud.ReadableColor(color[1], color[2], color[3]), hud.Escape(row.name), i)
	if row.team.readable then
		parts[#parts + 1] = string.format(
			'<div class="res"><div class="track"><div id="r%d-m" class="fill metal"/></div>'
			.. '<div class="track"><div id="r%d-e" class="fill energy"/></div></div>', i, i)
	end
	if row.kind == "player" then
		parts[#parts + 1] = string.format(
			'<div class="net" data-net="%d"><div id="r%d-cpu" class="cell top">CPU</div><div id="r%d-ping" class="cell">PING</div></div>'
			.. '<div class="fpsbox" data-net="%d"><div class="chip">FPS</div><div id="r%d-fps" class="fps"/></div>', i, i, i, i, i)
	else
		-- an AI has no cpu, ping or fps: keep its bars in line with the others'
		parts[#parts + 1] = '<div class="nonet"/>'
	end
	parts[#parts + 1] = '</div>'
	return table.concat(parts)
end

-- Rebuilds the rows' markup when the people in it have changed; everything
-- that changes while they stay is restated by ShowRows instead.
local function ShowList()
	FlattenRows()
	local signature = {drawAllyButton and "a" or "-"}
	local parts = {}
	local index = 0
	for _, group in ipairs(groups) do
		parts[#parts + 1] = group.isEnemy and '<div class="group enemy">' or '<div class="group">'
		signature[#signature + 1] = "|" .. tostring(group.allyTeam) .. (group.isEnemy and "e" or "")
		for _, team in ipairs(group.teams) do
			for _ = 1, #team.rows do
				index = index + 1
				local row = rows[index]
				parts[#parts + 1] = RowRML(index, row)
				signature[#signature + 1] = table.concat({row.kind, tostring(row.playerID), row.name, team.teamID,
					team.readable and "r" or "", hud.Rgb(team.color[1], team.color[2], team.color[3])}, ",")
			end
		end
		parts[#parts + 1] = '</div>'
	end
	signature = table.concat(signature, "\n")
	if signature ~= listSignature then
		listSignature = signature
		view.Element("list").inner_rml = table.concat(parts)
		view.Forget()
		specSignature = nil -- Forget covers the spectators too
		-- the mouse has not moved: keep the popup if its row is still the same one
		local row = hover and rows[hover.index]
		if not (row and row.name == hover.name and (hover.kind ~= "ally" or (drawAllyButton and row.isEnemy))) then
			hover = nil
		end
	end

	local names = {}
	if specsExpanded then
		for i, spec in ipairs(specs) do
			names[i] = '<div class="srow">' .. hud.Escape(spec.name) .. '</div>'
		end
	end
	local specMarkup = table.concat(names)
	if specMarkup ~= specSignature then
		specSignature = specMarkup
		view.Element("speclist").inner_rml = specMarkup
	end
	view.SetText("spechdr", (specsExpanded and "-" or "+") .. "  Spectators (" .. #specs .. ")")
end

-- what a row says about the player's connection: tag text and whether it is "dc"
local function StatusTag(row)
	if row.kind ~= "player" then
		return nil
	end
	if not row.connected then
		return "dc"
	end
	if (row.ping or 0) >= REJOIN_PING_S then
		local rejoined = reconnectTime[row.playerID]
		if rejoined and (osclock() - rejoined) < REJOIN_GRACE_S then
			return "rejoining"
		end
		return "lagging"
	end
	return nil
end

local function Percent(current, max)
	if not current or not max or max <= 0 then
		return "0%"
	end
	return string.format("%d%%", math_floor(math_max(0, math_min(1, current / max)) * 100 + 0.5))
end

local function ShowRows()
	for i, row in ipairs(rows) do
		local id = "r" .. i
		local team = row.team
		local tag = StatusTag(row)

		view.SetText(id .. "-tag", tag or "")
		view.SetClass(id .. "-tag", "dc", tag == "dc")
		view.SetClass(id, "dim", team.dead or tag == "dc")
		view.SetClass(id, "locked", row.playerID ~= nil and row.playerID == lockPlayerID)
		view.SetClass(id, "watchable", mySpecStatus and row.playerID ~= nil and IsBroadcasting(row.playerID))
		-- a player can click an ally to share with them
		view.SetClass(id, "shareable", not mySpecStatus and not row.isEnemy and team.teamID ~= myTeamID and not team.dead)

		if drawAllyButton and row.isEnemy then
			local weToThem, themToUs = WeAllied(team.teamID), TheyAllied(team.teamID)
			view.SetClass(id .. "-ally", "mutual", weToThem and themToUs)
			view.SetClass(id .. "-ally", "offered", weToThem and not themToUs)
			view.SetClass(id .. "-ally", "asked", themToUs and not weToThem)
		end

		if team.readable then
			view.SetStyle(id .. "-m", "width", Percent(team.mCur, team.mMax))
			view.SetStyle(id .. "-e", "width", Percent(team.eCur, team.eMax))
		end

		if row.kind == "player" then
			local cpu = row.connected and GetCpuLvl(row.cpu) or 0
			local ping = row.connected and GetPingLvl(row.ping) or 0
			for level = 1, 5 do
				view.SetClass(id .. "-cpu", "l" .. level, cpu == level)
				view.SetClass(id .. "-ping", "l" .. level, ping == level)
			end
			local fps = row.connected and PlayerFps(row.playerID) or nil
			view.SetText(id .. "-fps", fps and tostring(math_min(999, math_floor(fps))) or "")
		end
	end
end

local function ShowTopBar()
	local frame = spGetGameFrame()
	local minutes = math_floor(frame / 30 / 60)
	local seconds = math_floor(frame / 30) % 60
	local _, speed = spGetGameSpeed()
	view.SetText("tb-time", string.format("%d:%02d", minutes, seconds))
	view.SetText("tb-speed", string.format("%.2f", speed or 1))
	view.SetText("tb-fps", tostring(spGetFPS()))
end

--------------------------------------------------------------------------------
-- placement: the panel is as tall as its rows, and grows upward
--------------------------------------------------------------------------------

local function PanelHeight()
	local height = CHROME + TOPBAR + SPEC_HEADER
	for _, group in ipairs(groups) do
		for _, team in ipairs(group.teams) do
			height = height + #team.rows * ROW
		end
		height = height + GROUP_GAP
	end
	if specsExpanded then
		height = height + #specs * SPEC_ROW
	end
	return height
end

local function DefaultOrigin(vsx, vsy, w, h, scale)
	local margin = hud.Margin() * scale
	return vsx - margin - w, margin
end

local function Place()
	local height = PanelHeight()
	if height ~= shownHeight then
		shownHeight = height
		view.Element("players").style["height"] = height .. "dp"
	end
	local x, y, w, h = hud.PlacePanel(view.Element("players"), LAYOUT_NAME, PANEL_WIDTH, height, DefaultOrigin)
	if x then
		panelRect = {x1 = x, y1 = y, x2 = x + w, y2 = y + h}
	end
end

--------------------------------------------------------------------------------
-- the popup beside the list
--------------------------------------------------------------------------------

local function SystemLines(row)
	local pid = row.playerID
	local fps = PlayerFps(pid)
	-- (runs of spaces collapse in RML, so the figures are set apart by dots)
	local dot = " \194\183 "
	local second = "FPS " .. (fps and tostring(math_floor(fps)) or "?") .. dot .. "CPU " .. math_floor((row.cpu or 0) * 100) .. "%"
	second = second .. dot .. "Ping " .. math_floor((row.ping or 0) * 1000) .. " ms"

	local lines = {row.name, second}
	local system = PlayerSystem(pid)
	if system then
		for i = 1, #system do
			lines[#lines + 1] = system[i]
		end
	else
		lines[#lines + 1] = "(not running Slate: no system details)"
	end
	return lines
end

local function AllyStateTip(weToThem, themToUs)
	if weToThem and themToUs then return "Allied \194\183 click to break" end
	if weToThem then              return "Alliance offered \194\183 click to withdraw" end
	if themToUs then              return "They offered alliance \194\183 click to accept" end
	return "Not allied \194\183 click to offer alliance"
end

local function ShowPopup()
	local row = hover and rows[hover.index]
	local anchor = row and view.Element("r" .. hover.index)
	if not anchor then
		view.SetClass("popup", "hidden", true)
		return
	end

	local lines
	if hover.kind == "ally" then
		lines = {AllyStateTip(WeAllied(row.team.teamID), TheyAllied(row.team.teamID))}
	else
		lines = SystemLines(row)
	end
	local parts = {}
	for i, line in ipairs(lines) do
		parts[i] = string.format('<div class="%s">%s</div>', (i == 1) and "first" or ((i == 2) and "second" or ""), hud.Escape(line))
	end
	view.SetText("popup", table.concat(parts))

	-- beside the list, on whichever side has the room; its bottom level with
	-- the row's, since the list sits at the bottom of the screen
	local vsx, vsy = Spring.GetViewGeometry()
	local gap = math_floor(POPUP_GAP * hud.GetScale())
	local rowBottom = (anchor.absolute_top or 0) + (anchor.offset_height or 0)
	view.SetStyle("popup", "bottom", string.format("%dpx", math_max(0, math_floor(vsy - rowBottom))))
	if (panelRect.x1 + panelRect.x2) * 0.5 >= vsx * 0.5 then
		view.SetStyle("popup", "left", "auto")
		view.SetStyle("popup", "right", string.format("%dpx", vsx - panelRect.x1 + gap))
	else
		view.SetStyle("popup", "right", "auto")
		view.SetStyle("popup", "left", string.format("%dpx", panelRect.x2 + gap))
	end
	view.SetClass("popup", "hidden", false)
end

--------------------------------------------------------------------------------
-- refreshing
--------------------------------------------------------------------------------

local function Refresh()
	RefreshPlayers()
	ShowList()
	ShowRows()
	ShowTopBar()
	Place()
	ShowPopup()
	contentDirty = false
end

--------------------------------------------------------------------------------
-- input
--------------------------------------------------------------------------------

local function OnListMouseDown(event)
	if not (event.parameters and event.parameters.button == 0) then
		return
	end
	-- the alliance square: offer or withdraw OUR alliance toward them
	local index = hud.EventAttribute(event, "data-ally")
	local row = index and rows[index]
	if row then
		if drawAllyButton then
			spSendCommands("ally " .. row.team.allyTeam .. (WeAllied(row.team.teamID) and " 0" or " 1"))
			hud.Sound("click")
		end
		return
	end
	index = hud.EventAttribute(event, "data-r")
	row = index and rows[index]
	if not row then
		return
	end
	-- a spectator clicks a player to follow their camera, and again to let go
	if mySpecStatus then
		if row.playerID and (IsBroadcasting(row.playerID) or row.playerID == lockPlayerID) then
			hud.Sound("click")
			if row.playerID == lockPlayerID then
				LockCamera()
			else
				LockCamera(row.playerID)
			end
			ShowRows()
		end
		return
	end
	-- a player clicks an ally to share with that team
	local share = WG.SlateShare
	if share and not row.isEnemy and row.team.teamID ~= myTeamID and not row.team.dead then
		hud.Sound("click")
		if share.Open then
			share.Open(row.team.teamID)
		elseif share.Toggle then
			share.Toggle()
		end
	end
end

local function OnListMouseOver(event)
	local previous = hover
	local index = hud.EventAttribute(event, "data-ally")
	if index and rows[index] then
		hover = {kind = "ally", index = index, name = rows[index].name}
	else
		index = hud.EventAttribute(event, "data-net")
		hover = (index and rows[index]) and {kind = "net", index = index, name = rows[index].name} or nil
	end
	if hover and hover.kind == "ally" and not (previous and previous.kind == "ally" and previous.index == hover.index) then
		hud.Sound("hover")
	end
	ShowPopup()
end

local function OnListMouseOut()
	hover = nil
	ShowPopup()
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
		Spring.Echo("[Slate Players List] " .. tostring(reason))
		widgetHandler:RemoveWidget()
		return
	end
	hud = helpers
	document = result

	view = hud.NewView(document)
	view.Assume("popup", "hidden", true) -- set in the markup

	-- this list replaces the engine's own player list (/info)
	spSendCommands("info 0")

	-- the top bar shows these, so the engine need not
	spSendCommands("fps 0")
	spSendCommands("clock 0")
	spSendCommands("speed 0")

	local list = view.Element("list")
	list:AddEventListener("mousedown", OnListMouseDown)
	list:AddEventListener("mouseover", OnListMouseOver)
	list:AddEventListener("mouseout", OnListMouseOut)
	hud.OnClick(view, "spechdr", function()
		specsExpanded = not specsExpanded
		hud.Sound("click")
		Refresh()
	end)
	-- erases every map mark and drawing
	hud.OnClick(view, "tb-marks", function()
		hud.Sound("click")
		spSendCommands("clearmapmarks")
	end)
	view.Element("spechdr"):AddEventListener("mouseover", function()
		hud.Sound("hover")
	end)

	-- Other widgets may hang off this panel. The rectangle is the live one,
	-- including changes of height while the game runs. The camera lock is
	-- offered for a spectator tool that picks whom to follow.
	WG.SlatePlayersList = {
		GetRect = function()
			return panelRect.x1, panelRect.y1, panelRect.x2, panelRect.y2
		end,
		GetLockPlayerID = function() return lockPlayerID end,
		SetLockPlayerID = LockCamera,
	}

	hud.RegisterPanel(LAYOUT_NAME, "Players List", Refresh)
	hud.OnChange(LAYOUT_NAME, Refresh)
	Refresh()
	hud.ShowPassive(document)
end

function widget:Shutdown()
	if hud then
		hud.UnregisterPanel(LAYOUT_NAME)
		hud.OffChange(LAYOUT_NAME)
	end
	if document then
		hud.CloseDocument(document)
		document = nil

		WG.SlatePlayersList = nil

		spSendCommands("info 1")
		spSendCommands("fps 1")
		spSendCommands("clock 1")
		spSendCommands("speed 1")
	end
end

function widget:ViewResize()
	if hud and document then
		hud.UpdateScale()
		Refresh()
	end
end

-- These fire on connect, disconnect and spectator changes: refresh at once
-- rather than waiting for the 1s poll, so dc/rejoin tags appear without delay.
function widget:PlayerChanged(playerID)
	if document then
		Refresh()
	end
end

function widget:PlayerAdded(playerID)
	if document then
		Refresh()
	end
end

function widget:PlayerRemoved(playerID, reason)
	wasConnected[playerID]  = nil
	reconnectTime[playerID] = nil
	if document then
		Refresh()
	end
end

function widget:Update(dt)
	if not document then
		return
	end
	mySpecStatus, fullView = spGetSpectatingState()

	-- deferred specfullview re-apply (minimap/world refresh)
	if sceduledSpecFullView ~= nil then
		spSendCommands("specfullview")
		sceduledSpecFullView = sceduledSpecFullView - 1
		if sceduledSpecFullView == 0 then sceduledSpecFullView = nil end
	end

	-- deferred LOS toggle (within 1s of a lock change)
	if lockcameraLos then
		if desiredLosmodeChanged + 1 > osclock() then
			if lockPlayerID ~= nil then
				if desiredLosmode ~= spGetMapDrawMode() then
					spSendCommands("togglelos")
				end
			elseif mySpecStatus and spGetMapDrawMode() == 'los' then
				spSendCommands("togglelos")
			end
		end
	end

	FollowCamera()

	if hud.FollowGuiHidden(document) then
		hover = nil
		return -- hidden with the rest of the GUI (F5); the camera lock above still runs
	end

	refreshTimer = refreshTimer + dt
	if refreshTimer >= 1.0 or contentDirty then
		refreshTimer = 0
		Refresh()
	end
end
