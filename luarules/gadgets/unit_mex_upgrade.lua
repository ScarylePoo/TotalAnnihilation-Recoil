function gadget:GetInfo()
	return {
		name    = "Mex Upgrade",
		desc    = "A moho mine finished on top of a basic mex makes the mex vanish (no explosion, no wreck)",
		author  = "Scary le Poo (after Floris's Mex Upgrade Reclaimer in Beyond All Reason)",
		date    = "2026-11-08",
		license = "GNU GPL, v2 or later",
		layer   = 0,
		enabled = true,
	}
end

--------------------------------------------------------------------------------
-- Moho mines have a stackable yardmap ("s": buildable on top of blocked ground, gamedata/alldefs_post.lua), so one
-- can be placed over a basic mex, which keeps producing while the moho is built. When a mex with a higher
-- customparams.metal_spot_mult finishes, every lower one under it is removed as if reclaimed (DestroyUnit with
-- reclaimed = true: no death explosion, no corpse). Only mexes can stand on a metal spot (building mask), so the
-- stacking never applies to anything else.
--------------------------------------------------------------------------------

if not gadgetHandler:IsSyncedCode() then
	return
end

local tier = {}
for unitDefID, ud in pairs(UnitDefs) do
	local m = ud.customParams and tonumber(ud.customParams.metal_spot_mult)
	if m then
		tier[unitDefID] = m
	end
end

local SEARCH = 24   -- elmos: a mex under a moho shares its spot centre

function gadget:UnitFinished(unitID, unitDefID)
	local t = tier[unitDefID]
	if not t then
		return
	end
	local x, _, z = Spring.GetUnitPosition(unitID)
	for _, other in ipairs(Spring.GetUnitsInCylinder(x, z, SEARCH)) do
		local ot = tier[Spring.GetUnitDefID(other)]
		if other ~= unitID and ot and ot < t then
			Spring.DestroyUnit(other, false, true)   -- not self-destruct, reclaimed: no explosion, no wreck
		end
	end
end
