-- Damage smoke, as Splinter Faction's common SmokeUnit: below 90 % health the unit trails black smoke and small
-- burning puffs from random pieces (CEGs blacksmokesmall and burnblacksmall, gamedata/explosions), more often the
-- lower its health.
-- Use: include "smokeunit.lua", then StartThread(SmokeUnit, { piece "base", ... }) in script.Create().

local random = math.random
local SpawnCEG = Spring.SpawnCEG
local GetUnitPiecePosDir = Spring.GetUnitPiecePosDir

local function Emit(p, ceg)
	SpawnCEG(ceg, GetUnitPiecePosDir(unitID, p))
end

function SmokeUnit(smokePieces)
	local n = #smokePieces
	while (GetUnitValue(COB.BUILD_PERCENT_LEFT) ~= 0) do
		Sleep(1000)
	end
	while true do
		local health = GetUnitValue(COB.HEALTH)
		if (health <= 90) then
			Emit(smokePieces[random(1, n)], "blacksmokesmall")
			Emit(smokePieces[random(1, n)], "burnblacksmall")
		end
		Sleep(20 * health + 200)
	end
end
