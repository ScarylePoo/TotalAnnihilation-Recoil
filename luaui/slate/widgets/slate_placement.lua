-- Part of Slate, a game-neutral RmlUi interface for Total Annihilation style
-- games on the Recoil engine. Derived from the Bastion HUD in Splinter
-- Faction (same author, GPL v2+).

function widget:GetInfo()
	return {
		name    = "Slate Start Placement",
		desc    = "Pregame start position choice; sends the choice to the game_spawn gadget",
		author  = "Scary le Poo; SplinterFaction Team",
		date    = "2026-11-06",
		license = "GNU GPL, v2 or later",
		layer   = 1900, -- below the faction chooser (2000)
		enabled = true,
	}
end

--------------------------------------------------------------------------------
--  After the faction choice, each player picks a start spot and confirms it.
--  The map's spots are shown as numbered markers over the ground and again on
--  the minimap; both can be clicked. A panel at the bottom says what to do,
--  counts down, and holds the confirm button. The markers over the ground and
--  the panel are RmlUi; the minimap markers are drawn with gl inside the
--  engine's minimap, where RmlUi cannot draw.
--
--  The widget also owns the pregame as a whole:
--    * before the game starts it takes the engine's start-position screen
--      (the GameSetup call-in): the player is readied at once, since the spot
--      is picked in game, and the engine's "Choose start pos" text and Ready
--      box are replaced by this panel showing the engine's state ("Waiting
--      for players...").
--    * WG.SlatePregame is set for the whole flow (faction choice included),
--      which hides the rest of the HUD (hud.FollowGuiHidden); the minimap
--      stays (it sets hud.showInPregame), since spots can be picked on it.
--
--  WHAT A GAME MUST PROVIDE
--
--  A gadget (game_spawn.lua + game_start_spots.lua in this game) that sets
--  these game rules params:
--    "phase"                   "faction" | "placement" | "done"
--    "placementDeadlineFrame"  frame number of the placement deadline
--    "spotCount"               total number of spots
--    "isFFA"                   1 = all spots open to all, 0 = sided
--    "spot_N_x", "spot_N_z"    world position of spot N (1-based)
--    "spot_N_at"               allyteam owner (-1 = all in FFA)
--  and these team rules params, allied-only: "selectedSpot", "claimedSpot",
--  "confirmedSpot" (spot index), and private to the team "refusedSpot" and
--  "refusedCount" (a selection refused because an opponent holds the spot;
--  the count goes up by one each time). It listens with RecvLuaMsg for
--    SELECT_BYTE .. spotIndex   tentative selection
--    CONFIRM_BYTE               confirm the selection
--  Without the "phase" param the widget only does the GameSetup part and
--  leaves once the game has started.
--------------------------------------------------------------------------------

local DOCUMENT_PATH = "placement.rml"

-- must match game_spawn.lua
local SELECT_BYTE  = "\139"
local CONFIRM_BYTE = "\140"

-- must match #placement in placement.rml
local PANEL_WIDTH  = 560
local PANEL_HEIGHT = 88

local MARKER_SIZE = 48 -- must match .spot in placement.rml

local MMARK_SIZE     = 7    -- half-size of a minimap marker, in dp
local MMARK_PICK_PAD = 1.75 -- click and hover reach on the minimap, as a multiple of that

local COUNTDOWN_BEEP_AT = 10
local PLACEMENT_SECONDS = 30 -- seconds the full bar stands for

local LAYOUT_NAME = "slate_placement"

local MINIMAP_FONT = LUAUI_DIRNAME .. "slate/fonts/Saira_SemiCondensed-Bold.ttf"

--------------------------------------------------------------------------------
-- minimap marker colors, by the same states as the markers over the ground
-- (the palette of theme.rcss)
--------------------------------------------------------------------------------

local MINIMAP_COLOR = {
	free = {0.66, 0.74, 0.82, 0.95}, -- accent
	hot  = {0.76, 0.83, 0.89, 1.00}, -- bright accent
	mine = {0.95, 0.76, 0.19, 1.00}, -- warn
	done = {0.61, 0.91, 0.66, 1.00}, -- good
	mate = {0.55, 0.57, 0.60, 0.80}, -- dimmer
	foe  = {1.00, 0.70, 0.65, 0.45}, -- bad
}
local MINIMAP_INNER = {0.05, 0.055, 0.063, 0.80}

--------------------------------------------------------------------------------
-- speedups and state
--------------------------------------------------------------------------------

local spGetViewGeometry    = Spring.GetViewGeometry
local spGetMouseState      = Spring.GetMouseState
local spSendLuaRulesMsg    = Spring.SendLuaRulesMsg
local spGetGameRulesParam  = Spring.GetGameRulesParam
local spGetTeamRulesParam  = Spring.GetTeamRulesParam
local spWorldToScreenCoords = Spring.WorldToScreenCoords
local spGetGroundHeight    = Spring.GetGroundHeight
local spTraceScreenRay     = Spring.TraceScreenRay
local spIsAboveMiniMap     = Spring.IsAboveMiniMap
local spGetMiniMapGeometry = Spring.GetMiniMapGeometry
local spGetMiniMapRotation = Spring.GetMiniMapRotation   -- nil on older engines

local mapSizeX = Game.mapSizeX
local mapSizeZ = Game.mapSizeZ

local hud
local document
local view

local vsx, vsy    = spGetViewGeometry()
local widgetScale = 1             -- pixels per dp
local active      = false         -- true once the placement phase has begun
local gameStarted = false
local setupState  = nil           -- the engine's pregame state text, before the game starts

local myTeamID     = Spring.GetMyTeamID()
local myAllyTeamID = Spring.GetMyAllyTeamID()
local isSpectator  = false
local isFFA        = false

local spots     = {}   -- i -> {x, z, allyteam}
local spotCount = 0

local claimCount   = {}   -- i -> number of allied teams claiming spot i (0/nil = none visible)
local claimMine    = {}   -- i -> true if my own team claims spot i
local hoveredSpot  = nil  -- index or nil; under the mouse over the ground or on the minimap
local markerHover  = nil  -- index of the ground marker under the mouse (told by RmlUi)
local lastHoveredSpot = nil
local mySelected   = nil  -- server-acknowledged selected spot index
local myConfirmed  = nil  -- server-acknowledged confirmed spot index
local shareMode    = false -- true when no free same-side spots remain (overflow)
local confirmed    = false -- the player has confirmed a spot

local refused        = {}  -- i -> true: tried, and an opponent holds it
local refusedSeen    = 0   -- the gadget's refusedCount last seen
local noticeUntil    = 0   -- os.clock() until which the notice shows
local noticeText     = nil
local NOTICE_SECONDS = 3

local secondsLeft    = PLACEMENT_SECONDS
local lastBeepSecond = nil

-- a plain gl font for the numbers on the minimap markers
local minimapFont

--------------------------------------------------------------------------------
-- the game's state
--------------------------------------------------------------------------------

local function ValidSpot(v)
	return v and v >= 1 and math.floor(v) or nil
end

local function LoadSpots()
	spotCount = math.floor(spGetGameRulesParam("spotCount") or 0)
	isFFA     = (spGetGameRulesParam("isFFA") or 0) == 1

	spots = {}
	for i = 1, spotCount do
		local x  = spGetGameRulesParam("spot_" .. i .. "_x")
		local z  = spGetGameRulesParam("spot_" .. i .. "_z")
		local at = spGetGameRulesParam("spot_" .. i .. "_at")
		if x and z then
			spots[i] = { x = x, z = z, allyteam = at or -1 }
		end
	end
end

local function UpdateClaimCache()
	-- Only read claims for teams on our own side.  Claim params are allied-only,
	-- so opponents' claims are invisible here, in FFA too, which is the desired
	-- behaviour; all sharers of a spot are allied, so the counts built here are
	-- the true occupancy of every spot we can know about.  A spot an opponent
	-- holds is learnt only by trying it (see UpdateRefused).
	claimCount = {}
	claimMine  = {}
	local allyTeams = Spring.GetTeamList(myAllyTeamID) or {}
	for _, tID in ipairs(allyTeams) do
		local claimed = ValidSpot(spGetTeamRulesParam(tID, "claimedSpot"))
		if claimed then
			claimCount[claimed] = (claimCount[claimed] or 0) + 1
			if tID == myTeamID then claimMine[claimed] = true end
		end
	end

	-- Sharing becomes available once no same-side spot is free.
	if isSpectator then
		shareMode = false
	else
		local free = 0
		for i, spot in pairs(spots) do
			if (isFFA or spot.allyteam == myAllyTeamID) and not claimCount[i] and not refused[i] then
				free = free + 1
			end
		end
		shareMode = (free == 0)
	end
end

local function UpdateServerState()
	mySelected  = ValidSpot(spGetTeamRulesParam(myTeamID, "selectedSpot"))
	myConfirmed = ValidSpot(spGetTeamRulesParam(myTeamID, "confirmedSpot"))
	if myConfirmed then
		confirmed = true
	end
end

-- The gadget refused a selection: an opponent holds that spot. Say so, and
-- show the spot as taken from now on.
local function UpdateRefused()
	local count = spGetTeamRulesParam(myTeamID, "refusedCount") or 0
	if count > refusedSeen then
		refusedSeen = count
		local i = ValidSpot(spGetTeamRulesParam(myTeamID, "refusedSpot"))
		if i then
			refused[i] = true
			noticeText = "Spot " .. i .. " is taken. Pick another."
			noticeUntil = os.clock() + NOTICE_SECONDS
		end
	end
end

local function SpotOnMySide(i)
	local spot = spots[i]
	return spot ~= nil and (isFFA or spot.allyteam == myAllyTeamID)
end

local function SpotSelectable(i)
	if not SpotOnMySide(i) or refused[i] then return false end
	-- Selectable when: unclaimed, already mine, or (share mode) any same-side
	-- spot even if a teammate holds it.
	local occupied = (claimCount[i] or 0) > 0
	return (not occupied) or claimMine[i] or shareMode
end

local function TrySelectSpot(i)
	if SpotSelectable(i) then
		hud.Sound("click")
		spSendLuaRulesMsg(SELECT_BYTE .. i)
	end
end

--------------------------------------------------------------------------------
-- minimap
--------------------------------------------------------------------------------

-- World (x,z) -> minimap pixel coords (origin bottom-left) for use inside
-- DrawInMiniMap, whose default transform is minimap pixels.  Handles engine
-- minimap rotation when the query API exists: exact for 0 and 180 degrees;
-- 90/270 use the same rotate-around-center math and are best-effort (clicks
-- are unaffected either way, see MinimapPickSpot).
local function WorldToMinimapPx(wx, wz, sx, sy)
	local u = wx / mapSizeX
	local v = wz / mapSizeZ
	local rot = spGetMiniMapRotation and spGetMiniMapRotation() or 0
	if rot ~= 0 then
		local cu, cv = u - 0.5, v - 0.5
		local c, s   = math.cos(rot), math.sin(rot)
		u = 0.5 + c * cu - s * cv
		v = 0.5 + s * cu + c * cv
	end
	return math.floor(u * sx), math.floor(sy - v * sy)
end

-- Screen (x,y) -> nearest spot index when the mouse is over the minimap and
-- within pick range of a spot, else nil.  TraceScreenRay(useMinimap=true)
-- lets the engine do the minimap->world mapping.
local function MinimapPickSpot(x, y)
	if not (spIsAboveMiniMap and spIsAboveMiniMap(x, y)) then return nil end
	local _, coords = spTraceScreenRay(x, y, true, true)
	if type(coords) ~= "table" then return nil end
	local wx, wz = coords[1], coords[3]

	-- Pick radius: the marker's on-minimap pixel size converted to world units.
	local _, _, mmW, mmH = spGetMiniMapGeometry()
	if not mmW or mmW <= 0 or not mmH or mmH <= 0 then return nil end
	local worldPerPx = math.max(mapSizeX / mmW, mapSizeZ / mmH)
	local radius     = math.floor(MMARK_SIZE * widgetScale) * MMARK_PICK_PAD * worldPerPx

	local best, bestD2 = nil, radius * radius
	for i, spot in pairs(spots) do
		local dx, dz = spot.x - wx, spot.z - wz
		local d2 = dx * dx + dz * dz
		if d2 <= bestD2 then best, bestD2 = i, d2 end
	end
	return best
end

--------------------------------------------------------------------------------
-- the rest of the HUD
--------------------------------------------------------------------------------

-- WG.SlatePregame hides every Slate panel that follows hud.FollowGuiHidden.
-- WG.SlatePlacement tells the faction chooser that this widget owns the flag,
-- so it does not clear it on its way out between the two phases.
local function SetPregame(on)
	WG.SlatePregame = on or nil
	WG.SlatePlacement = on or nil
end

--------------------------------------------------------------------------------
-- showing
--------------------------------------------------------------------------------

-- What a spot is to the local player: "done", "mine", "mate", "free" or
-- "foe", and whether it is lit by the mouse. Shared by the markers over the
-- ground and the ones on the minimap.
local function SpotState(i)
	local spot   = spots[i]
	local count  = claimCount[i] or 0
	local mySide = isFFA or spot.allyteam == myAllyTeamID
	local hot    = (hoveredSpot == i)
	if myConfirmed and myConfirmed == i then
		return "done", false
	elseif claimMine[i] then
		return "mine", false
	elseif refused[i] then
		-- an opponent holds it (we know only because we tried it)
		return "foe", false
	elseif count > 0 then
		-- Taken by a teammate. In share mode it is still a valid target
		-- (overflow players may stack onto it), so it lights up.
		return "mate", hot and mySide and shareMode
	elseif mySide and not isSpectator then
		return "free", hot
	elseif mySide then
		return "free", false
	end
	-- the other side's: shown for reference, no claim state revealed
	return "foe", false
end

local STATES = {"done", "mine", "mate", "free", "foe"}

local function SpotsRML()
	local parts = {}
	for i = 1, spotCount do
		if spots[i] then
			parts[#parts + 1] = string.format(
				'<div id="s%d" class="spot hidden" data-spot="%d">%d<div id="s%d-ring" class="ring hidden"/><div id="s%d-n" class="count hidden"/></div>',
				i, i, i, i, i)
		end
	end
	return table.concat(parts)
end

local function RefreshSpots()
	local canPick = not confirmed and not isSpectator
	local margin = MARKER_SIZE * widgetScale
	for i, spot in pairs(spots) do
		local id = "s" .. i
		local gy = spGetGroundHeight(spot.x, spot.z) or 0
		local sx, sy, sz = spWorldToScreenCoords(spot.x, math.max(gy, 0) + 8, spot.z)
		local visible = sx and (not sz or sz < 1) and sx > -margin and sx < vsx + margin and sy > -margin and sy < vsy + margin
		view.SetClass(id, "hidden", not visible)
		if visible then
			view.SetStyle(id, "left", math.floor(sx) .. "px")
			view.SetStyle(id, "top", math.floor(vsy - sy) .. "px")
			local state, hot = SpotState(i)
			for _, name in ipairs(STATES) do
				view.SetClass(id, name, state == name)
			end
			view.SetClass(id, "hot", hot)
			view.SetClass(id, "can", canPick and SpotSelectable(i))
			view.SetClass(id .. "-ring", "hidden", state ~= "done")
			local count = claimCount[i] or 0
			view.SetClass(id .. "-n", "hidden", count < 2)
			if count >= 2 then
				view.SetText(id .. "-n", "x" .. count)
			end
		end
	end
end

local function RefreshPanel()
	local title, quiet
	if isSpectator then
		title = "Players are choosing start positions"
	elseif confirmed then
		title = "Waiting for the others..."
	elseif noticeText and os.clock() < noticeUntil then
		title = noticeText
	elseif mySelected then
		title = "Spot " .. mySelected .. " selected. Confirm when ready."
	elseif shareMode then
		-- more players than spots on this side: all are taken, so one may
		-- be shared
		title = "All spots on your side are taken. Click one to share it."
	else
		title, quiet = "Click a highlighted spot to start there", true
	end
	view.SetText("title", hud.Escape(title))
	view.SetClass("title", "quiet", quiet)

	local urgent = secondsLeft <= COUNTDOWN_BEEP_AT
	view.SetClass("timer", "hidden", false)
	view.SetClass("timer-bar", "hidden", false)
	view.SetText("timer", secondsLeft .. "s")
	view.SetClass("timer", "urgent", urgent)
	view.SetClass("timer-fill", "urgent", urgent)
	local fraction = math.max(0, math.min(1, secondsLeft / PLACEMENT_SECONDS))
	view.SetStyle("timer-fill", "width", string.format("%.1f%%", fraction * 100))

	view.SetClass("confirm", "hidden", isSpectator)
	view.SetClass("confirm", "done", confirmed)
	view.SetClass("confirm", "disabled", not confirmed and not mySelected)
	view.SetText("confirm", confirmed and "Confirmed" or "Confirm")
end

-- before the game starts: only the engine's state, in the panel
local function RefreshSetup()
	view.SetClass("root", "hidden", false)
	view.SetText("title", hud.Escape(setupState))
	view.SetClass("title", "quiet", true)
	view.SetClass("timer", "hidden", true)
	view.SetClass("timer-bar", "hidden", true)
	view.SetClass("confirm", "hidden", true)
end

local function Refresh()
	view.SetClass("root", "hidden", not active)
	if active then
		RefreshSpots()
		RefreshPanel()
	end
end

--------------------------------------------------------------------------------
-- widget api
--------------------------------------------------------------------------------

local function DefaultOrigin(sizeX, sizeY, w, h, scale)
	return (sizeX - w) * 0.5, hud.Margin() * 2 * scale
end

local function Place()
	vsx, vsy = spGetViewGeometry()
	widgetScale = hud.GetScale()
	hud.PlacePanel(view.Element("placement"), LAYOUT_NAME, PANEL_WIDTH, PANEL_HEIGHT, DefaultOrigin)
	view.ForgetStyles()
end

local function LoadMinimapFont()
	if minimapFont then
		gl.DeleteFont(minimapFont)
		minimapFont = nil
	end
	if gl.LoadFont then
		local size = math.max(10, math.floor(16 * widgetScale))
		minimapFont = gl.LoadFont(MINIMAP_FONT, size, math.max(2, math.floor(size * 0.18)), 1.8)
	end
end

local function Leave()
	widgetHandler:RemoveWidget(widget)
end

function widget:Initialize()
	if not WG.Slate then
		widgetHandler:RemoveWidget(widget)
		return
	end
	local helpers = include("slate/rml/core.lua")
	local result, reason = helpers.LoadDocument(DOCUMENT_PATH, widget)
	if not result then
		Spring.Echo("[Slate Start Placement] " .. tostring(reason))
		widgetHandler:RemoveWidget(widget)
		return
	end
	hud = helpers
	document = result
	gameStarted = Spring.GetGameFrame() > 0

	isSpectator  = Spring.GetSpectatingState()
	myTeamID     = Spring.GetMyTeamID()
	myAllyTeamID = Spring.GetMyAllyTeamID()

	view = hud.NewView(document)
	view.Assume("root", "hidden", true) -- set in the markup

	-- the markers over the ground
	local container = view.Element("spots")
	container:AddEventListener("mousedown", function(event)
		local i = hud.EventAttribute(event, "data-spot")
		if i and active and not confirmed and not isSpectator
			and event.parameters and event.parameters.button == 0 then
			TrySelectSpot(i)
		end
	end)
	container:AddEventListener("mouseover", function(event)
		markerHover = hud.EventAttribute(event, "data-spot")
	end)
	container:AddEventListener("mouseout", function()
		markerHover = nil
	end)

	hud.OnClick(view, "confirm", function()
		if active and not isSpectator and not confirmed and mySelected then
			hud.Sound("click")
			spSendLuaRulesMsg(CONFIRM_BYTE)
			confirmed = true
			Refresh()
		end
	end)

	hud.RegisterPanel(LAYOUT_NAME, "Start Placement", Place, function() return active end)
	hud.OnChange(LAYOUT_NAME, Place)
	Place()
	LoadMinimapFont()
	hud.ShowPassive(document)
end

function widget:Shutdown()
	-- whatever removes this widget (phase end, luaui reload, disabling it),
	-- the rest of the HUD must come back
	SetPregame(false)
	if hud then
		hud.UnregisterPanel(LAYOUT_NAME)
		hud.OffChange(LAYOUT_NAME)
		hud.CloseDocument(document)
		document = nil
	end
	if minimapFont then
		gl.DeleteFont(minimapFont)
		minimapFont = nil
	end
end

function widget:ViewResize()
	if hud and document then
		hud.UpdateScale()
		Place()
		LoadMinimapFont()
	end
end

-- The engine's start-position screen (shown when start positions are chosen
-- in game): this widget draws instead, and readies the player at once. The
-- spot is picked after the faction, in game.
function widget:GameSetup(state, ready, playerStates)
	setupState = state
	return true, true
end

function widget:GameStart()
	isSpectator  = Spring.GetSpectatingState()
	myTeamID     = Spring.GetMyTeamID()
	myAllyTeamID = Spring.GetMyAllyTeamID()
end

function widget:PlayerChanged()
	isSpectator  = Spring.GetSpectatingState()
	myTeamID     = Spring.GetMyTeamID()
	myAllyTeamID = Spring.GetMyAllyTeamID()
end

function widget:Update()
	if not document then
		return
	end
	if not gameStarted then
		if Spring.GetGameFrame() > 0 then
			gameStarted = true
			view.SetClass("root", "hidden", true)
		elseif setupState then
			RefreshSetup()
			return
		else
			return
		end
	end

	local newPhase = spGetGameRulesParam("phase")
	if newPhase == nil then
		-- no spawn gadget with phases: nothing to do once the game runs
		Leave()
		return
	end

	-- Keep the rest of the HUD hidden for the whole pregame flow (faction pick
	-- included) and bring it back the moment the flow is over.
	SetPregame(newPhase == "faction" or newPhase == "placement")

	if newPhase ~= "placement" then
		-- once the placement phase has ended, this widget is done
		if newPhase ~= "faction" then
			Leave()
		end
		return
	end

	-- first frame of the placement phase: load the spots and make a marker each
	if not active then
		active = true
		LoadSpots()
		view.Element("spots").inner_rml = SpotsRML()
		view.Forget()
		Place()
	end

	-- deadline (shrinks when all confirm)
	local deadlineFrame = spGetGameRulesParam("placementDeadlineFrame") or 0
	local frame         = Spring.GetGameFrame()
	local framesLeft    = math.max(0, deadlineFrame - frame)
	local gameSpeed     = Spring.GetGameSpeed() or 1
	secondsLeft         = math.ceil(framesLeft / (30 * gameSpeed))

	if secondsLeft <= COUNTDOWN_BEEP_AT and secondsLeft ~= lastBeepSecond and secondsLeft > 0 then
		hud.Sound("hover", 0.6)
		lastBeepSecond = secondsLeft
	end

	-- the server acknowledges our selection; allies' claims change too
	UpdateServerState()
	UpdateClaimCache()
	UpdateRefused()

	-- The spot under the mouse: a marker over the ground (RmlUi says which),
	-- or else one on the minimap. Either lights up both.
	-- (a marker that stops taking the mouse while under it, because an ally
	-- claimed it or the player confirmed, sends no "mouseout")
	if markerHover and (confirmed or isSpectator or not spots[markerHover] or not SpotSelectable(markerHover)) then
		markerHover = nil
	end
	hoveredSpot = markerHover
	if not hoveredSpot and not isSpectator then
		local mx, my = spGetMouseState()
		hoveredSpot = MinimapPickSpot(mx, my)
	end
	if hoveredSpot ~= lastHoveredSpot then
		if hoveredSpot then hud.Sound("hover") end
		lastHoveredSpot = hoveredSpot
	end

	Refresh()
end

--------------------------------------------------------------------------------
-- input on the minimap. (Clicks on the markers over the ground and on the
-- panel go to RmlUi and are handled in Initialize.)
--------------------------------------------------------------------------------

-- Take the press on a minimap marker, so the minimap does not also treat it
-- as a camera move. Clicks elsewhere on the minimap fall through and pan the
-- camera as usual.
function widget:MousePress(x, y, button)
	if not active or button ~= 1 or confirmed or isSpectator then return false end
	local mmSpot = MinimapPickSpot(x, y)
	return (mmSpot and SpotOnMySide(mmSpot)) and true or false
end

function widget:MouseRelease(x, y, button)
	if not active or button ~= 1 or confirmed or isSpectator then return false end
	local mmSpot = MinimapPickSpot(x, y)
	if mmSpot and SpotOnMySide(mmSpot) then
		TrySelectSpot(mmSpot)
		return true
	end
	return false
end

--------------------------------------------------------------------------------
-- minimap markers
--
-- Plain gl, inside the engine's minimap: RmlUi cannot draw there. A dozen
-- quads a frame for the half minute this lasts.
--------------------------------------------------------------------------------

function widget:DrawInMiniMap(sx, sy)
	if not active then return end

	local ms = math.max(4, math.floor(MMARK_SIZE * widgetScale))
	for i, spot in pairs(spots) do
		local px, py = WorldToMinimapPx(spot.x, spot.z, sx, sy)
		local state, hot = SpotState(i)
		local col = MINIMAP_COLOR[hot and "hot" or state]
		if state == "done" then
			-- outer ring, as on the marker over the ground
			local r = ms + math.max(2, math.floor(ms * 0.35))
			gl.Color(col[1], col[2], col[3], 0.55)
			gl.Rect(px - r, py - r, px + r, py + r)
		end
		gl.Color(col[1], col[2], col[3], col[4])
		gl.Rect(px - ms, py - ms, px + ms, py + ms)
		local inr = math.max(1, math.floor(ms * 0.3))
		gl.Color(MINIMAP_INNER[1], MINIMAP_INNER[2], MINIMAP_INNER[3], MINIMAP_INNER[4])
		gl.Rect(px - ms + inr, py - ms + inr, px + ms - inr, py + ms - inr)
	end
	gl.Color(1, 1, 1, 1)

	-- the numbers, so "Spot 3 selected" in the panel can be found here too
	if minimapFont and ms >= 6 then
		local lsz = math.floor(ms * 1.3)
		minimapFont:Begin()
		for i, spot in pairs(spots) do
			local px, py = WorldToMinimapPx(spot.x, spot.z, sx, sy)
			minimapFont:Print("\255\244\245\247" .. i, px, py - math.floor(lsz * 0.35), lsz, "con")
		end
		minimapFont:End()
	end
end
