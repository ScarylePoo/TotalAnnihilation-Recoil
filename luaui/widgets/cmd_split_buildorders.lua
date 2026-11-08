function widget:GetInfo()
	return {
		name = "Build Order Splitter",
		desc = "Shift-queued buildings are shared out between the selected builders instead of every builder queueing all of them",
		author = "Splinter Faction; TA:Recoil rework by Scary le Poo",
		date = "2026-11-08",
		license = "GPLv2",
		layer = 0,
		enabled = true
	}
end

--------------------------------------------------------------------------------
-- With two or more builders selected, each shift-queued building (a click, or every building of a dragged line) goes
-- to the one builder that can make it and has the fewest buildings queued, so a row of buildings is built in
-- parallel. Without shift, or with Space held (CommandInsert), orders are left alone (every builder takes the order, as usual). Factories never take
-- part: they have no build positions.
--------------------------------------------------------------------------------

local spGetSelectedUnits = Spring.GetSelectedUnits
local spGetUnitDefID     = Spring.GetUnitDefID
local spGetUnitCommands  = Spring.GetUnitCommands
local spGiveOrderToUnit  = Spring.GiveOrderToUnit

local canBuild = {}   -- builder unitDefID -> { [built unitDefID] = true }
for udid, ud in pairs(UnitDefs) do
	if ud.isBuilder and not ud.isFactory and ud.buildOptions and #ud.buildOptions > 0 then
		local set = {}
		for _, o in ipairs(ud.buildOptions) do
			set[o] = true
		end
		canBuild[udid] = set
	end
end

-- orders handed out that the unit's queue does not show yet (a round trip to the simulation, longer with ping; a
-- dragged line of buildings gives them all in one frame); UnitCommand says when one arrived
local pending = {}

local function QueuedBuildings(unitID)
	local n = pending[unitID] or 0
	for _, cmd in ipairs(spGetUnitCommands(unitID, -1) or {}) do
		if cmd.id < 0 then
			n = n + 1
		end
	end
	return n
end

function widget:CommandNotify(cmdID, cmdParams, cmdOpts)
	if cmdID >= 0 or not cmdOpts.shift or not cmdParams or #cmdParams < 3 then
		return false
	end
	if cmdOpts.meta or select(3, Spring.GetModKeyState()) then
		return false   -- Space+Shift is CommandInsert's
	end
	local defID = -cmdID
	local builders = {}
	for _, unitID in ipairs(spGetSelectedUnits()) do
		local set = canBuild[spGetUnitDefID(unitID)]
		if set and set[defID] then
			builders[#builders + 1] = unitID
		end
	end
	if #builders < 2 then
		return false
	end
	local best, bestN
	for _, unitID in ipairs(builders) do
		local n = QueuedBuildings(unitID)
		if not bestN or n < bestN then
			best, bestN = unitID, n
		end
	end
	spGiveOrderToUnit(best, cmdID, cmdParams, cmdOpts.coded)
	pending[best] = (pending[best] or 0) + 1
	return true
end

function widget:UnitCommand(unitID, unitDefID, unitTeam, cmdID)
	local p = pending[unitID]
	if p and cmdID < 0 then
		pending[unitID] = (p > 1) and (p - 1) or nil
	end
end

function widget:UnitDestroyed(unitID)
	pending[unitID] = nil
end
