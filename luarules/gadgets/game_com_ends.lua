function gadget:GetInfo()
	return {
		name    = "Commander Ends",
		desc    = "Game end modes 'commander' (a team dies with its commander) and 'comends' (an alliance dies with its last commander)",
		author  = "KDR_11k (David Becker), Floris, Jools; reworked for TA:Recoil",
		date    = "2026-10-25",
		license = "Public domain",
		layer   = 1,
		enabled = true,
	}
end

-- Commanders are the unitdefs with customParams.iscommander (set in gamedata/unitdefs_post.lua).
-- game_end.lua does the rest of the bookkeeping (dead teams, winners, surrender votes).

if not gadgetHandler:IsSyncedCode() then
	return
end

local MODE = (Spring.GetModOptions() or {}).mode or "comends" -- same default as modoptions.lua
local OWN_COM  = (MODE == "commander")
local TEAM_COM = (MODE == "comends")

local spGetTeamInfo  = Spring.GetTeamInfo
local spGetTeamList  = Spring.GetTeamList
local spGetTeamUnits = Spring.GetTeamUnits
local spDestroyUnit  = Spring.DestroyUnit
local spKillTeam     = Spring.KillTeam

local gaiaTeamID = Spring.GetGaiaTeamID()

local isCommander = {}
for unitDefID, unitDef in pairs(UnitDefs) do
	if unitDef.customParams.iscommander then
		isCommander[unitDefID] = true
	end
end

local teamComs = {}    -- teamID -> alive commanders
local allyComs = {}    -- allyTeamID -> alive commanders
local queue = {}       -- teamIDs to check next frame (a commander may be given before it is taken)

local function AllyTeamOf(teamID)
	return select(6, spGetTeamInfo(teamID, false))
end

local function IsDead(teamID)
	return select(3, spGetTeamInfo(teamID, false))
end

local function Eliminate(teamID)
	if IsDead(teamID) then
		return
	end
	-- as in TA: the commander takes the rest of the base with it
	local units = spGetTeamUnits(teamID)
	for i = 1, #units do
		spDestroyUnit(units[i], false)
	end
	spKillTeam(teamID)
end

local function Add(teamID, delta)
	if teamID == gaiaTeamID then
		return
	end
	local allyTeamID = AllyTeamOf(teamID)
	teamComs[teamID] = (teamComs[teamID] or 0) + delta
	allyComs[allyTeamID] = (allyComs[allyTeamID] or 0) + delta
	if delta < 0 then
		queue[teamID] = true
	end
end

function gadget:GameFrame()
	for teamID in pairs(queue) do
		queue[teamID] = nil
		if OWN_COM and teamComs[teamID] <= 0 then
			Eliminate(teamID)
		elseif TEAM_COM then
			local allyTeamID = AllyTeamOf(teamID)
			if allyComs[allyTeamID] <= 0 then
				local teams = spGetTeamList(allyTeamID)
				for i = 1, #teams do
					Eliminate(teams[i])
				end
			end
		end
	end
end

function gadget:UnitCreated(unitID, unitDefID, teamID)
	if isCommander[unitDefID] then Add(teamID, 1) end
end

function gadget:UnitGiven(unitID, unitDefID, newTeamID)
	if isCommander[unitDefID] then Add(newTeamID, 1) end
end

function gadget:UnitTaken(unitID, unitDefID, oldTeamID)
	if isCommander[unitDefID] then Add(oldTeamID, -1) end
end

function gadget:UnitDestroyed(unitID, unitDefID, teamID)
	if isCommander[unitDefID] then Add(teamID, -1) end
end

function gadget:Initialize()
	if not (OWN_COM or TEAM_COM) or next(isCommander) == nil then
		gadgetHandler:RemoveGadget(self)
		return
	end
	-- luarules reload: count what is already on the map
	local units = Spring.GetAllUnits()
	for i = 1, #units do
		local unitID = units[i]
		gadget:UnitCreated(unitID, Spring.GetUnitDefID(unitID), Spring.GetUnitTeam(unitID))
	end
end
