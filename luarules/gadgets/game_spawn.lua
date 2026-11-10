--------------------------------------------------------------------------------
--------------------------------------------------------------------------------
--
--  file:    game_spawn.lua
--  brief:   pre-game phases: faction choice → start position placement → spawn
--  author:  Tobi Vollebregt (original spawn gadget); phases ported from
--           game_spawn.lua in Splinter Faction (same author, GPL v2+)
--
--  Copyright (C) 2010.
--  Licensed under the terms of the GNU GPL, v2 or later.
--
--  The game starts with no units. Each player first picks a faction (the
--  Slate faction chooser), then a start spot (the Slate placement widget),
--  and only then is each team's commander created at its spot.
--
--  Phases, broadcast in the game rules param "phase":
--    "faction"    until "factionDeadlineFrame" (30 s, cut to 3 s once every
--                 human team has chosen). A team that has not chosen by then
--                 gets a faction at random; an AI team takes its lobby side.
--    "placement"  until "placementDeadlineFrame" (the same timings). The
--                 spots come from game_start_spots.lua (GG.StartSpots). AI
--                 teams are placed at once; a human team that has not
--                 confirmed by the deadline keeps the spot it selected, or is
--                 given the best free one on its side.
--    "done"       commanders created, start resources set.
--  With no usable spots the placement phase is skipped and each team starts
--  at its engine start position (its start box centre when that position is
--  unset or a box corner).
--
--  Messages (Spring.SendLuaRulesMsg), from a player of the team:
--    "\138" .. unitDefID   faction choice: the commander of one of the sides
--                          in gamedata/sidedata.lua
--    "\139" .. spotIndex   tentative spot selection
--    "\140"                confirm the selected spot
--  Team rules params "selectedSpot", "claimedSpot", "confirmedSpot" (allied
--  only: teammates and spectators) tell the placement widget what is taken.
--  A selection of a spot an opponent holds (FFA) is refused; only that team is
--  told, through the private params "refusedSpot" (the spot) and
--  "refusedCount" (goes up by one per refusal).
--
--  Start positions chosen in the lobby (startpostype 3): the placement phase
--  is skipped and each team starts at its lobby position, unless the game has
--  start boxes (an ally team with players whose box is not the whole map).
--
--  Changes from Splinter Faction: the factions are read from sidedata (no
--  commander upgrade, no Survival AI); AI teams keep their lobby side; start
--  resources are set right after each team's commander is created, as this
--  game always did; spectators' messages are ignored; a team that selected a
--  spot but did not confirm it keeps that spot.
--
--  Mod options (modoptions.lua) turn each phase off on its own:
--    factionchoice=0   no faction phase: every team takes its lobby side (a
--                      random faction when the side is not one), and the game
--                      goes straight to placement, or to the spawn.
--    startplacement=0  no placement phase: every team starts at its engine
--                      start position (FallbackPos), as with no usable spots.
--  Both off: the commanders are created at GameStart.
--
--  The headless test harness (tools/headless-test) sets the mod option
--  skippregame=1: start units are then created at GameStart at the engine
--  start positions, as before this gadget had phases.
--
--------------------------------------------------------------------------------
--------------------------------------------------------------------------------

function gadget:GetInfo()
	return {
		name      = "Spawn",
		desc      = "Pre-game faction + placement phases, then spawns start units and sets storage levels",
		author    = "Tobi Vollebregt; Scary le Poo; SplinterFaction Team",
		date      = "2026-11-06",
		license   = "GNU GPL, v2 or later",
		layer     = 0,
		enabled   = true
	}
end

--------------------------------------------------------------------------------
--------------------------------------------------------------------------------

if (not gadgetHandler:IsSyncedCode()) then
	return false
end

--------------------------------------------------------------------------------
-- Factions: one per side in gamedata/sidedata.lua
--------------------------------------------------------------------------------

local factions = {}       -- i → {side = "ARM", startUnit = "arm_commander", defID = n}
local factionByDefID = {}  -- commander unitDefID → faction
local factionBySide  = {}  -- lower-case side name → faction

for _, sd in ipairs(Spring.GetSideData() or {}) do
	local unitName = sd.startUnit and string.lower(sd.startUnit)
	local def = unitName and UnitDefNames[unitName]
	if def then
		local f = { side = sd.sideName, startUnit = unitName, defID = def.id }
		factions[#factions + 1] = f
		factionByDefID[def.id] = f
		factionBySide[string.lower(sd.sideName or "")] = f
	end
end

local PRIVATE = { private = true }
-- Spot selection / confirmation is visible to teammates and spectators only,
-- in FFA too: an opponent's spot is never shown. A player who tries a spot an
-- opponent holds is refused and told so (the private "refusedSpot" below), so
-- only spots a player actually tried are given away.
local ALLIED  = { allied = true }
local CLAIM_ACCESS = ALLIED

--------------------------------------------------------------------------------
-- Phase constants
--------------------------------------------------------------------------------

local CHOICE_TIMEOUT_FRAMES    = 900   -- 30 s
local PLACEMENT_TIMEOUT_FRAMES = 900   -- 30 s
local ADVANCE_FRAMES           = 90    -- 3 s once every human team is done

local FACTION_BYTE = "\138"
local SELECT_BYTE  = "\139"
local CONFIRM_BYTE = "\140"

local SHARE_RADIUS = 96   -- elmos between a shared spot's centre and each commander
local EDGE_MIN     = 128  -- elmos; a start position nearer the map edge than this is moved in (as game_start_spots.lua does with map spots)

--------------------------------------------------------------------------------
-- Phase state
--------------------------------------------------------------------------------

local modOptions = Spring.GetModOptions() or {}
local SKIP_PREGAME = (tonumber(modOptions.skippregame) or 0) ~= 0

-- A bool mod option, as a lobby or a script may spell it (true/false, 1/0).
local function Flag(key, default)
	local v = modOptions[key]
	if v == nil or v == "" then return default end
	if v == true or v == 1 or v == "1" or v == "true" then return true end
	if v == false or v == 0 or v == "0" or v == "false" then return false end
	return default
end
local FACTION_CHOICE  = Flag("factionchoice", true)
local START_PLACEMENT = Flag("startplacement", true)

local phase             = nil   -- nil (before GameStart) | "faction" | "placement" | "done"
local factionDeadline   = 0
local placementDeadline = 0

local humanTeams      = {}   -- teams with at least one human player
local allNonGaiaTeams = {}   -- every non-gaia team
local isHuman         = {}   -- teamID → true

local factionChosen           = {}    -- teamID → true once a faction is set
local pendingFactionAdvance   = false
local placementConfirmed      = {}    -- teamID → true once its spot is confirmed
local pendingPlacementAdvance = false

-- claimedSpots is spotIdx → { [teamID]=true, ... } (a set of claiming teams).
-- Normally each spot has at most one claimer (first-claim-wins).  When a side
-- has more players than spots, overflow players are allowed to *share* an
-- already-claimed same-side spot, so a spot may hold more than one team.
-- The key is removed entirely when the last claim is released, so a nil value
-- still means "unclaimed".
local claimedSpots   = {}   -- spotIdx → set of teamIDs
local selectedSpots  = {}   -- teamID → spotIdx (this team's one tentative selection)
local confirmedSpots = {}   -- teamID → spotIdx (this team's one confirmed selection)

local mapSpots     = {}    -- spotIdx (1-based) → {x, z, allyteam}  (from GG.StartSpots)
local usePlacement = false -- true when mapSpots has valid data
local refusedCount = {}    -- teamID → selections refused because an opponent held the spot
local isFFA        = false

-- For the headless test harness's probe (tools/headless-test, STARTP=1): it
-- has one real player, so it marks other teams as human here (before
-- GameStart) and sends their messages through Receive.
GG.SpawnFlow = { treatAsHuman = {} }

-- ── Claim-set helpers ────────────────────────────────────────────────────────

local function ClaimAdd(spotIdx, teamID)
	local c = claimedSpots[spotIdx]
	if not c then c = {}; claimedSpots[spotIdx] = c end
	c[teamID] = true
end

local function ClaimRemove(spotIdx, teamID)
	local c = claimedSpots[spotIdx]
	if c then
		c[teamID] = nil
		if next(c) == nil then claimedSpots[spotIdx] = nil end
	end
end

local function ClaimHas(spotIdx, teamID)
	local c = claimedSpots[spotIdx]
	return c ~= nil and c[teamID] == true
end

local function ClaimCount(spotIdx)
	local c = claimedSpots[spotIdx]
	if not c then return 0 end
	local n = 0
	for _ in pairs(c) do n = n + 1 end
	return n
end

local function AllyTeamOf(teamID)
	return select(6, Spring.GetTeamInfo(teamID, false))
end

-- True when a team other than an ally of allyID claims the spot.
local function ClaimedByOpponent(spotIdx, allyID)
	local c = claimedSpots[spotIdx]
	if not c then return false end
	for t in pairs(c) do
		if AllyTeamOf(t) ~= allyID then return true end
	end
	return false
end

-- Count same-side spots that this team could take without sharing: either
-- genuinely unclaimed, or claimed only by this team itself.  Used to decide
-- whether the sharing fallback is allowed (it is only when this returns 0).
local function FreeSameSideSpots(allyID, forTeamID)
	local n = 0
	for i, spot in ipairs(mapSpots) do
		if isFFA or spot.allyteam == allyID then
			local c = claimedSpots[i]
			if not c or (c[forTeamID] and ClaimCount(i) == 1) then
				n = n + 1
			end
		end
	end
	return n
end

--------------------------------------------------------------------------------
-- Teams
--------------------------------------------------------------------------------

-- A team is human when a player who is not a spectator plays it. AI teams
-- (skirmish AIs, Lua AIs, and teams nobody plays) are handled automatically.
local function IsTeamHuman(teamID)
	if GG.SpawnFlow.treatAsHuman[teamID] then return true end
	local _, _, _, isAiTeam = Spring.GetTeamInfo(teamID, false)
	if isAiTeam then return false end
	local luaAI = Spring.GetTeamLuaAI(teamID)
	if luaAI and luaAI ~= "" then return false end
	for _, playerID in ipairs(Spring.GetPlayerList(teamID) or {}) do
		local _, _, spectator, playerTeam = Spring.GetPlayerInfo(playerID, false)
		if not spectator and playerTeam == teamID then
			return true
		end
	end
	return false
end

local function RandomFaction()
	return factions[math.random(1, #factions)]
end

-- The lobby's side for the team, when it is one of the factions.
local function LobbyFaction(teamID)
	local side = select(5, Spring.GetTeamInfo(teamID, false))
	return side and factionBySide[string.lower(side)] or nil
end

local function SetFaction(teamID, faction)
	Spring.SetTeamRulesParam(teamID, "startUnit", faction.defID, PRIVATE)
	factionChosen[teamID] = true
end

--------------------------------------------------------------------------------
-- Spot selection helpers
--------------------------------------------------------------------------------

-- Pick the best unclaimed spot for a team: for sided games, the spot on their
-- side farthest from any enemy-side spot.  For FFA, farthest from any claimed spot.
local function AutoSelectSpot(teamID)
	local allyID = AllyTeamOf(teamID)
	local bestSpot, bestScore = nil, -1

	for i, spot in ipairs(mapSpots) do
		local available = isFFA or (spot.allyteam == allyID)
		if available and not claimedSpots[i] then
			local score

			if isFFA then
				-- Score: min distance to any claimed spot (maximize separation)
				local minDist = math.huge
				local anyClaimed = false
				for j in pairs(claimedSpots) do
					anyClaimed = true
					local es = mapSpots[j]
					if es then
						local dx = spot.x - es.x
						local dz = spot.z - es.z
						local d  = dx * dx + dz * dz
						if d < minDist then minDist = d end
					end
				end
				score = anyClaimed and minDist or 0
			else
				-- Score: min squared distance to any enemy-side spot (maximize)
				local minDist = math.huge
				for _, eSpot in ipairs(mapSpots) do
					if eSpot.allyteam ~= allyID then
						local dx = spot.x - eSpot.x
						local dz = spot.z - eSpot.z
						local d  = dx * dx + dz * dz
						if d < minDist then minDist = d end
					end
				end
				score = (minDist == math.huge) and 0 or minDist
			end

			if score > bestScore then
				bestScore = score
				bestSpot  = i
			end
		end
	end

	if bestSpot then return bestSpot end

	-- ── Sharing fallback ──────────────────────────────────────────────────────
	-- No unclaimed same-side spot remains (more players than spots on this side).
	-- Share the least-crowded same-side spot so this team still lands on its own
	-- side rather than at an arbitrary engine position. Never one an opponent
	-- holds (FFA): with none left, the team starts at FallbackPos.
	local fewest = math.huge
	for i, spot in ipairs(mapSpots) do
		local available = (isFFA or (spot.allyteam == allyID)) and not ClaimedByOpponent(i, allyID)
		if available then
			local n = ClaimCount(i)
			if n < fewest then
				fewest   = n
				bestSpot = i
			end
		end
	end

	return bestSpot
end

-- Claim and confirm a spot for a team, updating all relevant state.
local function AssignSpot(teamID, spotIdx)
	local prev = selectedSpots[teamID]
	if prev and ClaimHas(prev, teamID) then
		ClaimRemove(prev, teamID)
	end

	ClaimAdd(spotIdx, teamID)
	selectedSpots[teamID]  = spotIdx
	confirmedSpots[teamID] = spotIdx
	placementConfirmed[teamID] = true

	Spring.SetTeamRulesParam(teamID, "claimedSpot",   spotIdx, CLAIM_ACCESS)
	Spring.SetTeamRulesParam(teamID, "selectedSpot",  spotIdx, CLAIM_ACCESS)
	Spring.SetTeamRulesParam(teamID, "confirmedSpot", spotIdx, CLAIM_ACCESS)

	Spring.Echo("[Game Spawn] Assigned spot " .. spotIdx .. " to team " .. teamID ..
		" (now " .. ClaimCount(spotIdx) .. " claim(s))")
end

local function CheckAllFactionChosen()
	for _, tID in ipairs(humanTeams) do
		if not factionChosen[tID] then return false end
	end
	return true
end

local function CheckAllPlacementConfirmed()
	for _, tID in ipairs(humanTeams) do
		if not placementConfirmed[tID] then return false end
	end
	return true
end

--------------------------------------------------------------------------------
-- Spawning
--------------------------------------------------------------------------------

-- Where a team starts when it has no spot: its engine start position, unless
-- that is unset (0, 0) or the corner of its start box (where the engine puts
-- a player who readied without placing), in which case the middle of its
-- start box, spread out for teammates.
local function FallbackPos(teamID)
	local x, _, z = Spring.GetTeamStartPosition(teamID)
	local allyID = AllyTeamOf(teamID)
	local bx1, bz1, bx2, bz2 = Spring.GetAllyTeamStartBox(allyID)
	bx1, bz1 = bx1 or 0, bz1 or 0
	bx2, bz2 = bx2 or Game.mapSizeX, bz2 or Game.mapSizeZ
	local unset = (not x) or (x <= 0 and z <= 0) or (math.abs(x - bx1) < 1 and math.abs(z - bz1) < 1)
	if not unset then
		-- a position hard against the edge (the engine's fixed positions on a
		-- generated map are at 20, 20) leaves no room to build: move it in
		local cx = math.max(EDGE_MIN, math.min(Game.mapSizeX - EDGE_MIN, x))
		local cz = math.max(EDGE_MIN, math.min(Game.mapSizeZ - EDGE_MIN, z))
		if cx ~= x or cz ~= z then
			Spring.Echo(string.format("[Game Spawn] Team %d's start position (%.0f, %.0f) is against the map edge, moved to (%.0f, %.0f)", teamID, x, z, cx, cz))
		end
		return cx, cz
	end
	local mates = Spring.GetTeamList(allyID) or { teamID }
	local k, n = 1, #mates
	for i, t in ipairs(mates) do
		if t == teamID then k = i end
	end
	local cx, cz = (bx1 + bx2) / 2, (bz1 + bz2) / 2
	if n > 1 then
		local r = math.min(bx2 - bx1, bz2 - bz1) * 0.25
		local ang = (k - 1) / n * 2 * math.pi
		cx, cz = cx + r * math.cos(ang), cz + r * math.sin(ang)
	end
	Spring.Echo(string.format("[Game Spawn] Team %d has no usable start position — starting it at (%.0f, %.0f)", teamID, cx, cz))
	return cx, cz
end

local function StartUnitName(teamID)
	local defID = Spring.GetTeamRulesParam(teamID, "startUnit")
	local f = defID and factionByDefID[defID]
	if not f then
		f = LobbyFaction(teamID) or (#factions > 0 and RandomFaction())
	end
	return f and f.startUnit, f and f.side
end

-- This game's start resources: storage and amount from the team's or the mod
-- options, set right after the start unit is created (the unit's own storage
-- would otherwise be added on top).
local function SetStartResources(teamID)
	local teamOptions = select(8, Spring.GetTeamInfo(teamID, true)) or {}
	local m = teamOptions.startmetal  or modOptions.startmetal  or 1000
	local e = teamOptions.startenergy or modOptions.startenergy or 1000

	-- SetTeamResource gets rid of any existing resource without affecting stats;
	-- AddTeamResource adds the starting resource and counts it as income
	if (m and tonumber(m) ~= 0) then
		Spring.SetTeamResource(teamID, "ms", tonumber(m))
		Spring.SetTeamResource(teamID, "m", 0)
		Spring.AddTeamResource(teamID, "m", tonumber(m))
	end
	if (e and tonumber(e) ~= 0) then
		Spring.SetTeamResource(teamID, "es", tonumber(e))
		Spring.SetTeamResource(teamID, "e", 0)
		Spring.AddTeamResource(teamID, "e", tonumber(e))
	end
end

--   spawnX, spawnZ: the team's spot, or nil for FallbackPos
local function SpawnStartUnit(teamID, spawnX, spawnZ)
	local startUnit, side = StartUnitName(teamID)
	if startUnit and startUnit ~= "" then
		local x, z = spawnX, spawnZ
		if not (x and z) then
			x, z = FallbackPos(teamID)
		end

		-- Voidwater maps: never spawn in empty space.
		if GG.StartSpots and GG.StartSpots.SafeSpawnPos then
			x, z = GG.StartSpots.SafeSpawnPos(x, z)
		end

		-- keep on the map, snap to the 16x16 grid
		x = math.max(16, math.min(Game.mapSizeX - 16, x))
		z = math.max(16, math.min(Game.mapSizeZ - 16, z))
		x = 16 * math.floor((x + 8) / 16)
		z = 16 * math.floor((z + 8) / 16)
		local y = Spring.GetGroundHeight(x, z)

		-- facing toward map center
		local facing = math.abs(Game.mapSizeX / 2 - x) > math.abs(Game.mapSizeZ / 2 - z)
			and ((x > Game.mapSizeX / 2) and "west" or "east")
			or  ((z > Game.mapSizeZ / 2) and "north" or "south")

		local unitID = Spring.CreateUnit(startUnit, x, y, z, facing, teamID)
		Spring.SetTeamRulesParam(teamID, "faction", side or startUnit)
		Spring.Echo(string.format("[Game Spawn] Team %d: %s at (%d, %d)%s", teamID, startUnit, x, z,
			unitID and "" or " — CreateUnit FAILED"))
	end
	SetStartResources(teamID)
end

local function Finish()
	phase = "done"
	Spring.SetGameRulesParam("phase", "done")
	Spring.Echo("[Game Spawn] Phase: done")
end

-- Every team at its spot; teams sharing a spot stand on a small ring around
-- it so the commanders do not stack. Teams without a spot use FallbackPos.
local function SpawnAll()
	local spotTeams   = {}   -- spotIdx → { teamID, ... }
	local noSpotTeams = {}
	for _, teamID in ipairs(allNonGaiaTeams) do
		local spotIdx = confirmedSpots[teamID]
		if spotIdx and mapSpots[spotIdx] then
			local list = spotTeams[spotIdx]
			if not list then list = {}; spotTeams[spotIdx] = list end
			list[#list + 1] = teamID
		else
			noSpotTeams[#noSpotTeams + 1] = teamID
		end
	end

	for spotIdx = 1, #mapSpots do
		local teamList = spotTeams[spotIdx]
		if teamList then
			local spot = mapSpots[spotIdx]
			if #teamList == 1 then
				SpawnStartUnit(teamList[1], spot.x, spot.z)
			else
				local r = SHARE_RADIUS + 24 * (#teamList - 2)   -- widen slightly for 3+
				for k, teamID in ipairs(teamList) do
					local ang = (k - 1) / #teamList * 2 * math.pi
					SpawnStartUnit(teamID, spot.x + r * math.cos(ang), spot.z + r * math.sin(ang))
				end
			end
		end
	end

	for _, teamID in ipairs(noSpotTeams) do
		SpawnStartUnit(teamID, nil, nil)
	end
	Finish()
end

--------------------------------------------------------------------------------
-- Game start
--------------------------------------------------------------------------------

-- The game has start boxes when an ally team with players has a box that is
-- not the whole map (the engine reports the whole map for "no box").
local function HasStartBoxes()
	local gaiaTeamID = Spring.GetGaiaTeamID()
	for _, atID in ipairs(Spring.GetAllyTeamList()) do
		local players = false
		for _, t in ipairs(Spring.GetTeamList(atID) or {}) do
			if t ~= gaiaTeamID then players = true end
		end
		local x1, z1, x2, z2 = Spring.GetAllyTeamStartBox(atID)
		if players and x1 and not (x1 <= 1 and z1 <= 1 and x2 >= Game.mapSizeX - 1 and z2 >= Game.mapSizeZ - 1) then
			return true
		end
	end
	return false
end

local StartPlacement   -- the phase clock, below

function gadget:GameStart()
	-- only activate if engine didn't already spawn units (compatibility)
	if #Spring.GetAllUnits() > 0 then
		Spring.SetGameRulesParam("phase", "done")
		phase = "done"
		return
	end

	local gaiaTeamID = Spring.GetGaiaTeamID()
	for _, teamID in ipairs(Spring.GetTeamList()) do
		if teamID ~= gaiaTeamID then
			allNonGaiaTeams[#allNonGaiaTeams + 1] = teamID
			if IsTeamHuman(teamID) then
				humanTeams[#humanTeams + 1] = teamID
				isHuman[teamID] = true
			end
		end
	end

	-- The harness, or a game with nothing to choose: start as before.
	if SKIP_PREGAME or #factions == 0 then
		for _, teamID in ipairs(allNonGaiaTeams) do
			SpawnStartUnit(teamID, nil, nil)
		end
		Finish()
		return
	end

	-- AI teams take their lobby side (a random one when it is not a faction).
	for _, teamID in ipairs(allNonGaiaTeams) do
		if not isHuman[teamID] then
			SetFaction(teamID, LobbyFaction(teamID) or RandomFaction())
		end
	end

	-- Fetch the (already validated and partitioned) start spots before
	-- broadcasting the phase, so the game rules params are ready when widgets
	-- first read them.
	if not START_PLACEMENT then
		Spring.Echo("[Game Spawn] Start placement is off (mod option) — no placement phase")
	elseif Game.startPosType == 3 and not HasStartBoxes() then
		-- the players chose their start positions in the lobby
		Spring.Echo("[Game Spawn] Start positions chosen in the lobby — no placement phase")
	elseif GG.StartSpots then
		local spots, ffa = GG.StartSpots.Get()
		if spots and #spots > 0 then
			mapSpots     = spots
			isFFA        = ffa
			usePlacement = true
		end
	else
		Spring.Echo("[Game Spawn] GG.StartSpots missing (game_start_spots.lua not loaded?) — skipping placement phase")
	end

	Spring.SetGameRulesParam("factionDeadlineFrame",   0)
	Spring.SetGameRulesParam("placementDeadlineFrame", 0)

	if not FACTION_CHOICE then
		-- No faction phase: the human teams take their lobby side too.
		Spring.Echo("[Game Spawn] Faction choice is off (mod option) — every team takes its lobby side" ..
			"  human teams=" .. #humanTeams .. "  AI teams=" .. (#allNonGaiaTeams - #humanTeams) ..
			"  spots=" .. #mapSpots .. "  FFA=" .. tostring(isFFA))
		for _, teamID in ipairs(allNonGaiaTeams) do
			if not factionChosen[teamID] then
				SetFaction(teamID, LobbyFaction(teamID) or RandomFaction())
			end
		end
		if usePlacement then
			StartPlacement(Spring.GetGameFrame())
		else
			SpawnAll()
		end
		return
	end

	phase = "faction"
	factionDeadline = Spring.GetGameFrame() + CHOICE_TIMEOUT_FRAMES
	Spring.SetGameRulesParam("factionDeadlineFrame", factionDeadline)
	Spring.SetGameRulesParam("phase",                "faction")

	Spring.Echo("[Game Spawn] Phase: faction  deadline=" .. factionDeadline ..
		"  human teams=" .. #humanTeams .. "  AI teams=" .. (#allNonGaiaTeams - #humanTeams) ..
		"  spots=" .. #mapSpots .. "  FFA=" .. tostring(isFFA))

	if CheckAllFactionChosen() then
		pendingFactionAdvance = true
	end
end

--------------------------------------------------------------------------------
-- Messages
--------------------------------------------------------------------------------

local function Receive(msg, teamID)
	local firstByte = msg:sub(1, 1)

	if firstByte == FACTION_BYTE then
		if phase ~= "faction" then return end
		local f = factionByDefID[tonumber(msg:sub(2)) or -1]
		if not f then return end
		SetFaction(teamID, f)
		Spring.Echo("[Game Spawn] Team " .. teamID .. " chose " .. f.startUnit)
		if CheckAllFactionChosen() then
			pendingFactionAdvance = true
		end

	elseif firstByte == SELECT_BYTE then
		if phase ~= "placement" then return end
		local spotIdx = tonumber(msg:sub(2))
		if not spotIdx or not mapSpots[spotIdx] then return end
		if placementConfirmed[teamID] then return end   -- already locked

		local allyID = AllyTeamOf(teamID)
		local spot = mapSpots[spotIdx]

		-- no crossing into enemy territory
		if not isFFA and spot.allyteam ~= allyID then return end

		-- Claim rules:
		--   • A free spot can always be claimed.
		--   • A spot already claimed by this team is a no-op re-select.
		--   • A spot an opponent holds (FFA) is refused, and only this team is
		--     told: its own claims are all it can otherwise see.
		--   • A spot claimed by an ally is refused (first claim wins) unless
		--     this team has no free same-side spot left, in which case sharing
		--     is permitted so overflow players aren't stranded.
		if ClaimedByOpponent(spotIdx, allyID) then
			refusedCount[teamID] = (refusedCount[teamID] or 0) + 1
			Spring.SetTeamRulesParam(teamID, "refusedSpot", spotIdx, PRIVATE)
			Spring.SetTeamRulesParam(teamID, "refusedCount", refusedCount[teamID], PRIVATE)
			return
		end
		if not ClaimHas(spotIdx, teamID) and ClaimCount(spotIdx) > 0 then
			if FreeSameSideSpots(allyID, teamID) > 0 then return end
		end

		local prev = selectedSpots[teamID]
		if prev and ClaimHas(prev, teamID) then
			ClaimRemove(prev, teamID)
		end

		ClaimAdd(spotIdx, teamID)
		selectedSpots[teamID] = spotIdx
		Spring.SetTeamRulesParam(teamID, "claimedSpot",  spotIdx, CLAIM_ACCESS)
		Spring.SetTeamRulesParam(teamID, "selectedSpot", spotIdx, CLAIM_ACCESS)

	elseif firstByte == CONFIRM_BYTE then
		if phase ~= "placement" then return end
		if placementConfirmed[teamID] then return end
		local spotIdx = selectedSpots[teamID]
		if not spotIdx then return end   -- must select before confirming

		confirmedSpots[teamID] = spotIdx
		placementConfirmed[teamID] = true
		Spring.SetTeamRulesParam(teamID, "confirmedSpot", spotIdx, CLAIM_ACCESS)
		Spring.Echo("[Game Spawn] Team " .. teamID .. " confirmed spot " .. spotIdx)

		if CheckAllPlacementConfirmed() then
			pendingPlacementAdvance = true
		end
	end
end

GG.SpawnFlow.Receive = Receive

function gadget:RecvLuaMsg(msg, playerID)
	local firstByte = msg:sub(1, 1)
	if firstByte ~= FACTION_BYTE and firstByte ~= SELECT_BYTE and firstByte ~= CONFIRM_BYTE then
		return false
	end
	local _, _, spectator, teamID = Spring.GetPlayerInfo(playerID, false)
	if not spectator and teamID then
		Receive(msg, teamID)
	end
	return true
end

--------------------------------------------------------------------------------
-- Phase clock
--------------------------------------------------------------------------------

function StartPlacement(n)
	phase = "placement"
	placementDeadline = n + PLACEMENT_TIMEOUT_FRAMES
	Spring.SetGameRulesParam("placementDeadlineFrame", placementDeadline)
	Spring.SetGameRulesParam("phase", "placement")
	Spring.Echo("[Game Spawn] Phase: placement  deadline=" .. placementDeadline)

	-- AI teams: placed and confirmed at once
	for _, teamID in ipairs(allNonGaiaTeams) do
		if not isHuman[teamID] then
			local spotIdx = AutoSelectSpot(teamID)
			if spotIdx then
				AssignSpot(teamID, spotIdx)
			end
			placementConfirmed[teamID] = true
		end
	end

	if CheckAllPlacementConfirmed() then
		pendingPlacementAdvance = true
	end
end

function gadget:GameFrame(n)
	if phase == "faction" then
		if pendingFactionAdvance then
			pendingFactionAdvance = false
			local target = n + ADVANCE_FRAMES
			if target < factionDeadline then
				factionDeadline = target
				Spring.SetGameRulesParam("factionDeadlineFrame", factionDeadline)
				Spring.Echo("[Game Spawn] All factions chosen — new deadline: frame " .. factionDeadline)
			end
		end

		if n >= factionDeadline then
			for _, teamID in ipairs(allNonGaiaTeams) do
				if not factionChosen[teamID] then
					local f = RandomFaction()
					Spring.Echo("[Game Spawn] Team " .. teamID .. " timed out — random faction " .. f.startUnit)
					SetFaction(teamID, f)
				end
			end

			if usePlacement then
				StartPlacement(n)
			else
				SpawnAll()
			end
		end

	elseif phase == "placement" then
		if pendingPlacementAdvance then
			pendingPlacementAdvance = false
			local target = n + ADVANCE_FRAMES
			if target < placementDeadline then
				placementDeadline = target
				Spring.SetGameRulesParam("placementDeadlineFrame", placementDeadline)
				Spring.Echo("[Game Spawn] All placements confirmed — new deadline: frame " .. placementDeadline)
			end
		end

		if n >= placementDeadline then
			-- a human team that did not confirm keeps the spot it selected, or
			-- gets the best free one
			for _, teamID in ipairs(humanTeams) do
				if not placementConfirmed[teamID] then
					local spotIdx = selectedSpots[teamID] or AutoSelectSpot(teamID)
					Spring.Echo("[Game Spawn] Team " .. teamID .. " placement timed out — " ..
						(selectedSpots[teamID] and "keeping its selected spot" or "auto-placing"))
					if spotIdx then
						AssignSpot(teamID, spotIdx)
					end
					placementConfirmed[teamID] = true
				end
			end
			SpawnAll()
		end
	end
end

--------------------------------------------------------------------------------
-- Player ready states (choose-in-game start positions), for widgets
--------------------------------------------------------------------------------

-- readyState: 0 unready, 1 ready, 2 game force-started & player not ready,
-- 3 force-started & player absent
function gadget:AllowStartPosition(playerID, teamID, readyState, cx, cy, cz, rx, ry, rz)
	if Game.startPosType == 2 then
		Spring.SetGameRulesParam("player_" .. playerID .. "_readyState", readyState)
	end
	return true
end
