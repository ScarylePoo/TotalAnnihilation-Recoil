function gadget:GetInfo()
	return {
		name    = "Bomber Orders",
		desc    = "Bombers refuse attack orders on aircraft (their bombs cannot hit them; they would circle forever)",
		author  = "TA:Recoil",
		date    = "2026-11-14",
		license = "GNU GPL v2",
		layer   = 0,
		enabled = true,
	}
end

-- Recoil lets a bomber take an attack order on an airborne plane: its bombs never get a release window (BombDropper
-- needs the target below and ahead), so it chases the plane until told otherwise, which reads as an ignored order.
-- BAR blocks the same (luarules/gadgets/unit_bomber_no_air_target.lua). Landed aircraft can still be bombed.

if not gadgetHandler:IsSyncedCode() then
	return
end

local CMD_ATTACK = CMD.ATTACK
local CMD_INSERT = CMD.INSERT
local spGetUnitDefID = Spring.GetUnitDefID
local spValidUnitID = Spring.ValidUnitID
local spGetUnitPosition = Spring.GetUnitPosition
local spGetGroundHeight = Spring.GetGroundHeight

local isBomber = {}
for udid, ud in pairs(UnitDefs) do
	if ud.canFly and not ud.hoverAttack and ud.weapons[1] then
		local wd = WeaponDefs[ud.weapons[1].weaponDef]
		if wd and wd.type == "AircraftBomb" then
			isBomber[udid] = true
		end
	end
end
local isAircraft = {}
for udid, ud in pairs(UnitDefs) do
	if ud.canFly then
		isAircraft[udid] = true
	end
end

local function Airborne(targetID)
	if not spValidUnitID(targetID) or not isAircraft[spGetUnitDefID(targetID)] then
		return false
	end
	local x, y, z = spGetUnitPosition(targetID)
	return y - math.max(spGetGroundHeight(x, z), 0) > 20
end

function gadget:Initialize()
	if next(isBomber) == nil then
		gadgetHandler:RemoveGadget(self)
		return
	end
end

function gadget:AllowCommand(unitID, unitDefID, unitTeam, cmdID, cmdParams, cmdOptions)
	if not isBomber[unitDefID] or (cmdID ~= CMD_ATTACK and cmdID ~= CMD_INSERT) then
		return true
	end
	if cmdID == CMD_INSERT then
		if cmdParams[2] ~= CMD_ATTACK or #cmdParams ~= 4 then
			return true
		end
		return not Airborne(cmdParams[4])
	end
	if #cmdParams == 1 then
		return not Airborne(cmdParams[1])
	end
	return true
end
