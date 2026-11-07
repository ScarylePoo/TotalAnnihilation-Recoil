function gadget:GetInfo()
	return {
		name    = "Nano Effects",
		desc    = "Splinter Faction's nano-animated CEG from every nano piece while a builder or factory sprays",
		author  = "TA:Recoil",
		license = "GPL v2 or later",
		layer   = 0,
		enabled = true,
	}
end

-- SF emits "nano-animated" from its builders' nano pieces every 425 ms while they build (in each unit script).
-- Here one gadget does it for every unit with build power, whatever it is doing with the nanolathe (build, repair,
-- reclaim, resurrect, capture), from the pieces the engine sprays nano particles from (Spring.GetUnitNanoPieces:
-- the script's QueryNanoPiece answers, cached by the engine once the unit has sprayed). The engine's own nanospray
-- stays on.

if not gadgetHandler:IsSyncedCode() then
	return
end

local CEG = "nano-animated"
local PERIOD = 13 -- sim frames between puffs (~433 ms; SF: 425 ms)

local GetUnitWorkerTask = Spring.GetUnitWorkerTask
local GetUnitNanoPieces = Spring.GetUnitNanoPieces
local GetUnitCurrentBuildPower = Spring.GetUnitCurrentBuildPower
local GetUnitPiecePosDir = Spring.GetUnitPiecePosDir
local SpawnCEG = Spring.SpawnCEG

local isBuilder = {}
for unitDefID, ud in pairs(UnitDefs) do
	if (ud.buildSpeed or 0) > 0 then
		isBuilder[unitDefID] = true
	end
end

local builders = {}

function gadget:UnitFinished(unitID, unitDefID)
	if isBuilder[unitDefID] then
		builders[unitID] = true
	end
end

function gadget:UnitDestroyed(unitID)
	builders[unitID] = nil
end

function gadget:Initialize()
	for _, unitID in ipairs(Spring.GetAllUnits()) do
		local _, _, _, _, buildProgress = Spring.GetUnitHealth(unitID)
		if buildProgress and buildProgress >= 1 then
			gadget:UnitFinished(unitID, Spring.GetUnitDefID(unitID))
		end
	end
end

function gadget:GameFrame(n)
	if n % PERIOD ~= 0 then
		return
	end
	for unitID in pairs(builders) do
		if GetUnitWorkerTask(unitID) and (not GetUnitCurrentBuildPower or (GetUnitCurrentBuildPower(unitID) or 0) > 0) then
			local pieces = GetUnitNanoPieces(unitID)
			if pieces then
				for i = 1, #pieces do
					SpawnCEG(CEG, GetUnitPiecePosDir(unitID, pieces[i]))
				end
			end
		end
	end
end
