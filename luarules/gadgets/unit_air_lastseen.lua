function gadget:GetInfo()
	return {
		name    = "Air Attack Last Seen",
		desc    = "Aircraft whose attack target slips out of sight and radar finish the run on where it was last seen",
		author  = "TA:Recoil",
		date    = "2026-11-14",
		license = "GNU GPL v2",
		layer   = 0,
		enabled = true,
	}
end

-- Recoil drops an attack-unit order about 2 s after a mobile target leaves both LOS and radar (CommandAI
-- UpdateTargetLostTimer), so a bomber sent at something that ducks out of sight simply gives up mid-run.
-- Here, when the target is lost, the order becomes an attack-ground on the LAST POSITION THE OWNER'S ALLYTEAM SAW:
-- the true position if it was in LOS, the radar dot (true position + the same radar error the player is shown) if
-- it was only on radar. Nothing about where the target went afterwards is used, so the plane leaks nothing.
--   * target seen again (LOS or radar) before the run is over -> back to the attack-unit order
--   * the plane fires on the spot -> the order finishes RUN_AFTER_SHOT later (one pass, not bombing it forever)
--   * it never gets to fire -> the order finishes after GIVE_UP
-- Not touched: immobile targets (the engine never loses those), aircraft in the air (no blind fire at the sky),
-- and attack orders whose target was never seen by this gadget (it has no last position to use).

if not gadgetHandler:IsSyncedCode() then
	return
end

local CMD_ATTACK = CMD.ATTACK
local CMD_INSERT = CMD.INSERT
local CMD_REMOVE = CMD.REMOVE

local POLL = 5                  -- frames; the engine gives up after 4 slow updates (64 frames)
local RUN_AFTER_SHOT = 90       -- frames the run continues after the first shot at the spot (bomb streams)
local GIVE_UP = 30 * 30         -- frames without a shot before the blind order is dropped

local spGetUnitCurrentCommand = Spring.GetUnitCurrentCommand
local spGetUnitPosition = Spring.GetUnitPosition
local spGetUnitAllyTeam = Spring.GetUnitAllyTeam
local spGetUnitLosState = Spring.GetUnitLosState
local spGetUnitPosErrorParams = Spring.GetUnitPosErrorParams
local spGetRadarErrorParams = Spring.GetRadarErrorParams
local spGetUnitDefID = Spring.GetUnitDefID
local spValidUnitID = Spring.ValidUnitID
local spGetGroundHeight = Spring.GetGroundHeight
local spGetUnitWeaponState = Spring.GetUnitWeaponState
local spGiveOrderToUnit = Spring.GiveOrderToUnit

local isAircraft, isImmobile, numWeapons = {}, {}, {}
for udid, ud in pairs(UnitDefs) do
	if ud.canFly then
		isAircraft[udid] = true
		if ud.canAttack and #ud.weapons > 0 then
			numWeapons[udid] = #ud.weapons
		end
	end
	if ud.isImmobile or (ud.speed or 0) == 0 then
		isImmobile[udid] = true
	end
end

local planes = {}      -- unitID -> { def, run = nil | { target, x, y, z, since, shot } }
local lastSeen = {}    -- allyTeam -> targetID -> { x, y, z }

-- where allyTeam sees targetID now, or nil if it is out of LOS and radar
local function SeenAt(targetID, allyTeam)
	local los = spGetUnitLosState(targetID, allyTeam)
	if not los or not (los.los or los.radar) then
		return nil
	end
	local x, y, z = spGetUnitPosition(targetID)
	if not los.los then
		local ex, ey, ez, _, _, _, _, bit = spGetUnitPosErrorParams(targetID, allyTeam)
		local size = spGetRadarErrorParams(allyTeam) or 0
		if ex and bit then
			x, y, z = x + ex * size, y + ey * size, z + ez * size
		end
	end
	return x, y, z
end

local function Remember(targetID, allyTeam)
	local x, y, z = SeenAt(targetID, allyTeam)
	if x then
		lastSeen[allyTeam] = lastSeen[allyTeam] or {}
		lastSeen[allyTeam][targetID] = { x, y, z }
		return true
	end
	return false
end

local function Airborne(targetID)
	if not isAircraft[spGetUnitDefID(targetID)] then
		return false
	end
	local x, y, z = spGetUnitPosition(targetID)
	return y - math.max(spGetGroundHeight(x, z), 0) > 20
end

local function Replace(unitID, tag, params)
	spGiveOrderToUnit(unitID, CMD_INSERT, { 0, CMD_ATTACK, 0, unpack(params) }, CMD.OPT_ALT)
	spGiveOrderToUnit(unitID, CMD_REMOVE, { tag }, 0)
end

local function FiredSince(unitID, def, frame)
	for w = 1, numWeapons[def] do
		local reload = spGetUnitWeaponState(unitID, w, "reloadState")
		local fired = reload and spGetUnitWeaponState(unitID, w, "reloadTime")
		-- reloadState is the frame the weapon is ready again; it moves forward when the weapon fires
		if reload and fired and reload - fired * 30 >= frame - 1 then
			return true
		end
	end
	return false
end

local function Update(unitID, p, frame)
	local cmdID, _, tag, a1, a2, a3, a4 = spGetUnitCurrentCommand(unitID)
	local run = p.run
	if cmdID ~= CMD_ATTACK then
		p.run = nil
		return
	end
	local ally = spGetUnitAllyTeam(unitID)

	if a2 == nil then
		-- attack unit
		p.run = nil
		local t = a1
		if not spValidUnitID(t) or isImmobile[spGetUnitDefID(t)] or Airborne(t) then
			return
		end
		if Remember(t, ally) then
			return
		end
		local seen = lastSeen[ally] and lastSeen[ally][t]
		if seen then
			local x, z = seen[1], seen[3]
			local y = spGetGroundHeight(x, z)
			p.run = { target = t, x = x, y = y, z = z, since = frame }
			Replace(unitID, tag, { x, y, z })
		end
		return
	end

	-- attack ground: only ours
	if not run or math.abs(a1 - run.x) > 1 or math.abs(a3 - run.z) > 1 or a4 ~= nil then
		p.run = nil
		return
	end
	if spValidUnitID(run.target) and Remember(run.target, ally) then
		p.run = nil
		Replace(unitID, tag, { run.target })
		return
	end
	if not run.shot and FiredSince(unitID, p.def, run.since) then
		run.shot = frame
	end
	if (run.shot and frame - run.shot >= RUN_AFTER_SHOT) or (not run.shot and frame - run.since >= GIVE_UP) then
		p.run = nil
		spGiveOrderToUnit(unitID, CMD_REMOVE, { tag }, 0)
	end
end

function gadget:GameFrame(frame)
	if frame % POLL ~= 0 then
		return
	end
	for unitID, p in pairs(planes) do
		Update(unitID, p, frame)
	end
end

-- remember where a target was when the order was given, for attack orders queued behind others
function gadget:UnitCommand(unitID, unitDefID, unitTeam, cmdID, cmdParams)
	if numWeapons[unitDefID] and cmdID == CMD_ATTACK and #cmdParams == 1 and spValidUnitID(cmdParams[1]) then
		Remember(cmdParams[1], spGetUnitAllyTeam(unitID))
	end
end

function gadget:UnitCreated(unitID, unitDefID)
	if numWeapons[unitDefID] then
		planes[unitID] = { def = unitDefID }
	end
end

function gadget:UnitDestroyed(unitID)
	planes[unitID] = nil
	for _, seen in pairs(lastSeen) do
		seen[unitID] = nil
	end
end

function gadget:Initialize()
	if next(numWeapons) == nil then
		gadgetHandler:RemoveGadget(self)
		return
	end
	for _, unitID in ipairs(Spring.GetAllUnits()) do
		gadget:UnitCreated(unitID, spGetUnitDefID(unitID))
	end
end
