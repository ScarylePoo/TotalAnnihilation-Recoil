function gadget:GetInfo()
	return {
		name    = "Air Repair Pads",
		desc    = "Damaged aircraft fly to a friendly pad or carrier, land on a free landing point, get repaired and carry on",
		author  = "Claude, for TA:Recoil",
		date    = "2026-11-02",
		license = "Public domain",
		layer   = 0,
		enabled = true,
	}
end

--------------------------------------------------------------------------------
--  Recoil took air bases out of its aircraft code. What is left: the unit def
--  tag (ignored; unitdefs_post.lua copies it to customParams.isairbase), the
--  scripts' QueryLandingPads (never called) and the "Repair level" state
--  (CMD.AUTOREPAIRLEVEL: LandAt 0/30/50/80 on every aircraft, which Spring.GetUnitStates
--  reads back but nothing acts on). This gadget supplies the behaviour and keeps
--  that state button as TA's "Land at". Slate's order menu lists it on its own.
--
--  A trip is a command at the front of the aircraft's queue (inserted, so what
--  the aircraft was doing stays behind it, or given by right-clicking a pad):
--
--    fly           engine flight towards a reserved landing point
--    wait          all points taken: a gunship hovers on a ring around the pad; an
--                  airplane cannot (the engine flies it in turns over 1000 elmos
--                  wide, off the map if it must), so MoveCtrl holds it in a
--                  stacked orbit. No progress for a minute and it gives up.
--    land          MoveCtrl glides it down onto the point
--    deck          MoveCtrl keeps it on the point (a carrier moves), repairing
--    lift          MoveCtrl lifts it off, then the engine has it back
--
--  Any other order puts something else at the front of the queue, which is
--  how a trip gets cancelled. The aircraft then ignores its repair level for a
--  while: a player who sends a damaged plane back in means it.
--
--  Repair goes at the builder's rate: repairSpeed (workertime) / buildTime of
--  max health per second. It is not done by giving the pad a real CMD.REPAIR
--  because a carrier would stop for it and a pad builds no further than 38
--  elmos. It costs what engine repair costs: repairEnergyCostFactor of the
--  plane's energy cost per part repaired, which is 0 in this game (free).
--------------------------------------------------------------------------------

local CMD_PAD_REPAIR = 33791

local isPad, isAir = {}, {}
for unitDefID, ud in pairs(UnitDefs) do
	if ud.customParams.isairbase then
		isPad[unitDefID] = true
	end
	if ud.canFly then
		isAir[unitDefID] = true
	end
end

if not gadgetHandler:IsSyncedCode() then

	local spGetUnitDefID        = Spring.GetUnitDefID
	local spGetUnitHealth       = Spring.GetUnitHealth
	local spGetSelectedUnits    = Spring.GetSelectedUnits
	local spIsUnitAllied        = Spring.IsUnitAllied
	local spGetUnitIsBeingBuilt = Spring.GetUnitIsBeingBuilt

	function gadget:Initialize()
		Spring.SetCustomCommandDrawData(CMD_PAD_REPAIR, "Repair", {0.3, 1, 0.4, 0.8}, true)
	end

	-- right click on a friendly pad with a damaged aircraft selected
	function gadget:DefaultCommand(targetType, id)
		if targetType ~= "unit" or not isPad[spGetUnitDefID(id)] or not spIsUnitAllied(id) or spGetUnitIsBeingBuilt(id) then
			return
		end
		local selected = spGetSelectedUnits()
		for i = 1, #selected do
			if isAir[spGetUnitDefID(selected[i])] then
				local health, maxHealth = spGetUnitHealth(selected[i])
				if health and health < maxHealth then
					return CMD_PAD_REPAIR
				end
			end
		end
	end

	return
end

--------------------------------------------------------------------------------
-- Synced
--------------------------------------------------------------------------------

local WAIT_TIMEOUT = 60 * 30    -- frames beside a full pad before giving up
local RETRY_DELAY  = 30 * 30    -- frames a cancelled or given-up aircraft ignores its repair level
local LAND_DECEL   = 1 / 60     -- of the entry speed, per frame: the glide takes about two seconds
local FLARE        = 12         -- elmos above the point where the glide ends and the plane sets down
local LIFT_HEIGHT  = {airplane = 70, gunship = 30}
local CLEAR_DIST   = 220        -- how far an aircraft with no orders moves off the pad
local FAR_PAD      = 2500       -- how much further a free pad may be than a full one
local PATIENCE     = 30 * 30    -- frames waiting before a free pad at any distance will do
local HOLD_RADIUS  = 320        -- airplanes waiting: the orbit around the pad
local HOLD_HEIGHT  = 170        -- above the pad, plus HOLD_STACK per place in the queue
local HOLD_STACK   = 35

local spGetUnitPosition       = Spring.GetUnitPosition
local spGetUnitPiecePosDir    = Spring.GetUnitPiecePosDir
local spGetUnitVelocity       = Spring.GetUnitVelocity
local spGetUnitRotation       = Spring.GetUnitRotation
local spGetUnitHealth         = Spring.GetUnitHealth
local spSetUnitHealth         = Spring.SetUnitHealth
local spGetUnitTeam           = Spring.GetUnitTeam
local spGetUnitStates         = Spring.GetUnitStates
local spGetUnitIsStunned      = Spring.GetUnitIsStunned
local spGetUnitIsBeingBuilt   = Spring.GetUnitIsBeingBuilt
local spGetUnitTransporter    = Spring.GetUnitTransporter
local spGetUnitIsTransporting = Spring.GetUnitIsTransporting
local spGetUnitCurrentCommand = Spring.GetUnitCurrentCommand
local spGetUnitCommands       = Spring.GetUnitCommands
local spGiveOrderToUnit       = Spring.GiveOrderToUnit
local spSetUnitMoveGoal       = Spring.SetUnitMoveGoal
local spSetUnitVelocity       = Spring.SetUnitVelocity
local spAreTeamsAllied        = Spring.AreTeamsAllied
local spGetGameFrame          = Spring.GetGameFrame
local mc                      = Spring.MoveCtrl

local sqrt, min, max, abs, atan2, sin, cos = math.sqrt, math.min, math.max, math.abs, math.atan2, math.sin, math.cos
local PI = math.pi

local energyFactor = Game.repairEnergyCostFactor or 0

local pads = {}      -- padID -> { id, points = { {piece =, plane =} ... }, rate = per second of workertime }
local planes = {}    -- finished aircraft: unitID -> unitDefID
local trips = {}     -- unitID -> trip
local retryAt = {}   -- unitID -> first frame its repair level counts again
local waiters = {}   -- trips in wait state, longest wait first
local newTrips = {}  -- started by CommandFallback, which can run inside an order given while walking trips
local moveKind = {}  -- unitDefID -> "airplane" | "gunship"

GG.AirPads = {pads = pads, trips = trips, CMD = CMD_PAD_REPAIR}

local padCmdDesc = {
	id      = CMD_PAD_REPAIR,
	type    = CMDTYPE.ICON_UNIT,
	name    = "Repair at pad",
	action  = "padrepair",
	cursor  = "Repair",
	tooltip = "Land on this repair pad or carrier and get repaired",
	hidden  = true, -- right click on a pad; no button
}

local function CallScript(unitID, name)
	local env = Spring.UnitScript.GetScriptEnv(unitID)
	if env and env.script[name] then
		Spring.UnitScript.CallAsUnit(unitID, env.script[name])
	end
end

local function AddPad(unitID, unitDefID)
	local env = Spring.UnitScript.GetScriptEnv(unitID)
	local query = env and env.script.QueryLandingPads
	local list = query and Spring.UnitScript.CallAsUnit(unitID, query)
	if not list then
		return
	end
	local points, seen = {}, {}
	for i = 1, #list do
		local piece = list[i]
		if piece and piece > 0 and not seen[piece] then
			seen[piece] = true -- the OTA scripts name their one pad twice
			points[#points + 1] = {piece = piece}
		end
	end
	if #points > 0 then
		pads[unitID] = {id = unitID, points = points, rate = UnitDefs[unitDefID].repairSpeed}
	end
end

local function PadUsable(padID, teamID)
	return pads[padID] and spAreTeamsAllied(spGetUnitTeam(padID), teamID) and not spGetUnitIsBeingBuilt(padID)
end

local function PointPosition(padID, piece)
	return spGetUnitPiecePosDir(padID, piece)
end

-- nearest free point, unless that is much further than a full pad (it will come free before the
-- plane has flown across the map, after which it may well have to wait there too); failing that the nearest full pad
local function FindPad(unitID, wanted, patient)
	local teamID = spGetUnitTeam(unitID)
	local x, _, z = spGetUnitPosition(unitID)
	local freePad, freeDist, freePoint, fullPad, fullDist
	for padID, pad in pairs(pads) do
		if (not wanted or padID == wanted) and PadUsable(padID, teamID) and not spGetUnitIsStunned(padID) then
			local px, _, pz = spGetUnitPosition(padID)
			local d = (px - x)^2 + (pz - z)^2
			local point
			for i = 1, #pad.points do
				if not pad.points[i].plane then
					point = pad.points[i]
					break
				end
			end
			if point then
				if not freeDist or d < freeDist then
					freePad, freeDist, freePoint = pad, d, point
				end
			elseif not fullDist or d < fullDist then
				fullPad, fullDist = pad, d
			end
		end
	end
	if freeDist and fullDist and patient and sqrt(freeDist) > sqrt(fullDist) + FAR_PAD then
		return nil, nil, fullPad
	end
	return freePad, freePoint, fullPad
end

local function AnyPad(teamID)
	for padID in pairs(pads) do
		if PadUsable(padID, teamID) then
			return true
		end
	end
	return false
end

--------------------------------------------------------------------------------
-- Leaving and ending
--------------------------------------------------------------------------------

local function ReleasePoint(trip)
	if trip.point then
		trip.point.plane = nil
		trip.point = nil
	end
	trip.pad = nil
end

local function LeaveWaiters(trip)
	for i = 1, #waiters do
		if waiters[i] == trip then
			table.remove(waiters, i)
			return
		end
	end
end

local function RemoveCommand(trip)
	local queue = spGetUnitCommands(trip.unit, -1)
	for i = 1, #queue do
		if queue[i].tag == trip.tag then
			spGiveOrderToUnit(trip.unit, CMD.REMOVE, {trip.tag}, 0)
			return
		end
	end
end

local function LetGo(trip)
	if trip.grabbed then
		trip.grabbed = false
		mc.Disable(trip.unit)
		spSetUnitVelocity(trip.unit, trip.vx, trip.vy, trip.vz)
	end
end

local function EndTrip(trip, retryDelay)
	LetGo(trip)
	ReleasePoint(trip)
	LeaveWaiters(trip)
	trips[trip.unit] = nil
	if retryDelay then
		retryAt[trip.unit] = spGetGameFrame() + retryDelay
	end
	RemoveCommand(trip)
end

local StartLanding

local function Search(trip)
	local unitID = trip.unit
	if trip.wanted and not PadUsable(trip.wanted, spGetUnitTeam(unitID)) then
		trip.wanted = nil
	end
	local waited = trip.waitSince and spGetGameFrame() - trip.waitSince or 0
	local pad, point, fullPad = FindPad(unitID, trip.wanted, waited < PATIENCE)
	if point then
		-- the queue moved: the others' minute starts again
		local wasWaiting = trip.waitSince
		LeaveWaiters(trip)
		if wasWaiting then
			for i = 1, #waiters do
				waiters[i].waitSince = spGetGameFrame()
			end
		end
		point.plane = unitID
		trip.pad, trip.point, trip.state = pad, point, "fly"
		trip.waitSince = nil
		trip.waitPad = nil
		local x, _, z = spGetUnitPosition(unitID)
		local px, _, pz = PointPosition(pad.id, point.piece)
		local d = sqrt((px - x)^2 + (pz - z)^2)
		local ud = UnitDefs[planes[unitID]]
		trip.deadline = spGetGameFrame() + 900 + 2 * d / max(ud.speed / 30, 1)
		trip.goalAt = nil
		if trip.grabbed then
			if d < HOLD_RADIUS * 2 then
				StartLanding(trip)
			else
				LetGo(trip)
			end
		end
	elseif fullPad then
		if trip.state ~= "wait" then
			trip.state = "wait"
			trip.waitSince = trip.waitSince or spGetGameFrame()
			if not trip.slot or waiters[trip.slot] ~= trip then
				LeaveWaiters(trip)
				waiters[#waiters + 1] = trip
				trip.slot = #waiters
			end
		end
		trip.waitPad = fullPad.id
	else
		-- nothing left to land on: back to its orders; the repair level counts as soon as a pad turns up
		EndTrip(trip)
	end
end

--------------------------------------------------------------------------------
-- Scripted flight
--------------------------------------------------------------------------------

local function Grab(trip)
	local unitID = trip.unit
	local x, y, z = spGetUnitPosition(unitID)
	local vx, vy, vz = spGetUnitVelocity(unitID)
	local pitch, yaw, roll = spGetUnitRotation(unitID)
	trip.x, trip.y, trip.z = x, y, z
	trip.vx, trip.vy, trip.vz = vx, vy, vz
	trip.pitch, trip.yaw, trip.roll = pitch, yaw, roll
	if not trip.grabbed then
		trip.grabbed = true
		mc.Enable(unitID)
		mc.SetNoBlocking(unitID, true)
		mc.SetGravity(unitID, 0)
		mc.SetCollideStop(unitID, false)
		mc.SetLimitsStop(unitID, false)
	end
end

local function Place(trip)
	local unitID = trip.unit
	mc.SetPosition(unitID, trip.x, trip.y, trip.z)
	mc.SetVelocity(unitID, trip.vx, trip.vy, trip.vz)
	mc.SetRotation(unitID, trip.pitch, trip.yaw, trip.roll)
end

local function Lift(trip, why)
	local unitID = trip.unit
	if trip.state ~= "land" and trip.state ~= "deck" then
		return
	end
	if why == "cancel" then
		trip.cancelled = true
		retryAt[unitID] = spGetGameFrame() + RETRY_DELAY
	end
	trip.state = "lift"
	trip.liftFrom = trip.y
	trip.liftSpeed = max(trip.vy, 0.3)
	-- out of the plane it came down in
	local ud = UnitDefs[planes[unitID]]
	trip.forward = 0
	trip.maxForward = moveKind[planes[unitID]] == "airplane" and ud.speed / 30 * 0.5 or 0
	trip.baseVx, trip.baseVz = trip.vx, trip.vz
	CallScript(unitID, "Activate")
	CallScript(unitID, "StartMoving")
end

local function Release(trip)
	local unitID = trip.unit
	LetGo(trip)
	if trip.research then
		-- its pad went: find another
		trip.research = nil
		ReleasePoint(trip)
		trip.state = "search"
		return
	end
	EndTrip(trip)
	-- nothing to go back to: do not sit in the way of the next plane
	if #spGetUnitCommands(unitID, 1) == 0 then
		if moveKind[planes[unitID]] == "airplane" then
			-- Lift already carried it clear. A Stop sets it down where it is; the Move a gunship gets would
			-- end at once, an airplane's Move being over within its turn radius of the goal, and leave it circling
			spGiveOrderToUnit(unitID, CMD.STOP, {}, 0)
		else
			spGiveOrderToUnit(unitID, CMD.MOVE, {
				max(min(trip.x - sin(trip.yaw) * CLEAR_DIST, Game.mapSizeX), 0), 0,
				max(min(trip.z + cos(trip.yaw) * CLEAR_DIST, Game.mapSizeZ), 0)}, 0)
		end
	end
end

local function PadYaw(padID)
	local _, yaw = spGetUnitRotation(padID)
	return yaw
end

local function WrapAngle(a)
	return (a + PI) % (2 * PI) - PI
end

local function StepLand(trip)
	local pad = trip.pad
	local tx, ty, tz = PointPosition(pad.id, trip.point.piece)
	local padVx, _, padVz = spGetUnitVelocity(pad.id)
	local dx, dz = tx - trip.x, tz - trip.z
	local d = sqrt(dx * dx + dz * dz)
	trip.landFrames = trip.landFrames + 1

	local speed = min(trip.entrySpeed, sqrt(2 * trip.entrySpeed * LAND_DECEL * d) + 0.4)
	local k = trip.landFrames > 240 and 1 or 0.12
	local wantVx, wantVz = padVx, padVz
	if d > 0.5 then
		wantVx = padVx + dx / d * speed
		wantVz = padVz + dz / d * speed
	end
	trip.vx = trip.vx + (wantVx - trip.vx) * k
	trip.vz = trip.vz + (wantVz - trip.vz) * k
	if d < 1 + speed then
		trip.vx, trip.vz = padVx, padVz
		trip.x, trip.z = tx, tz
		d = 0
	else
		trip.x = trip.x + trip.vx
		trip.z = trip.z + trip.vz
	end

	-- glide to just above the point, then set down
	local heightGoal, vy = ty + trip.hoverOffset
	if d > 4 then
		heightGoal = heightGoal + FLARE
		local frames = max(d / max(speed, 0.5), 1)
		vy = (heightGoal - trip.y) / frames
		vy = max(min(vy, 6), -6)
	else
		-- a plane that came in high drops fast at first and sets down at one elmo a frame
		local h = heightGoal - trip.y
		local rate = max(1, abs(h) * 0.08)
		vy = max(min(h, rate), -rate)
	end
	trip.y = trip.y + vy
	trip.vy = vy

	-- face the way it is going over the pad, wings level
	local relVx, relVz = trip.vx - padVx, trip.vz - padVz
	if d > 20 and relVx * relVx + relVz * relVz > 0.25 then
		local turn = WrapAngle(atan2(-relVx, relVz) - trip.yaw)
		trip.yaw = trip.yaw + max(min(turn, 0.05), -0.05)
	end
	trip.pitch = trip.pitch * 0.93
	trip.roll = trip.roll * 0.93

	if d == 0 and abs(heightGoal - trip.y) < 0.2 then
		trip.state = "deck"
		trip.yawOffset = trip.yaw - PadYaw(pad.id)
		trip.nextRepair = spGetGameFrame() + 5
		trip.pitch, trip.roll = 0, 0
	end
	Place(trip)
end

local function StepDeck(trip, frame)
	local pad, unitID = trip.pad, trip.unit
	local tx, ty, tz = PointPosition(pad.id, trip.point.piece)
	ty = ty + trip.hoverOffset
	-- a velocity that matches the deck, so the plane is drawn smoothly between frames
	trip.vx, trip.vy, trip.vz = tx - trip.x, ty - trip.y, tz - trip.z
	trip.x, trip.y, trip.z = tx, ty, tz
	trip.yaw = PadYaw(pad.id) + trip.yawOffset
	Place(trip)

	if frame >= trip.nextRepair then
		trip.nextRepair = frame + 5
		if not spGetUnitIsStunned(pad.id) and not spGetUnitIsBeingBuilt(pad.id) then
			local health, maxHealth = spGetUnitHealth(unitID)
			local ud = UnitDefs[planes[unitID]]
			local part = pad.rate / ud.buildTime * 5 / 30
			local pays = energyFactor <= 0 or Spring.UseTeamResource(spGetUnitTeam(pad.id), "energy", ud.energyCost * part * energyFactor)
			if pays then
				health = min(health + part * maxHealth, maxHealth)
				spSetUnitHealth(unitID, health)
			end
			if health >= maxHealth then
				Lift(trip)
			end
		end
	end
end

local function StepLift(trip)
	local height = trip.y - trip.liftFrom
	trip.liftSpeed = min(trip.liftSpeed + 0.08, 3)
	trip.forward = min(trip.forward + trip.maxForward / 45, trip.maxForward)
	-- it keeps the deck's way until it is clear
	trip.vx = trip.baseVx - sin(trip.yaw) * trip.forward
	trip.vz = trip.baseVz + cos(trip.yaw) * trip.forward
	trip.vy = trip.liftSpeed
	trip.x, trip.y, trip.z = trip.x + trip.vx, trip.y + trip.vy, trip.z + trip.vz
	Place(trip)
	if height >= LIFT_HEIGHT[moveKind[planes[trip.unit]]] then
		Release(trip)
	end
end

StartLanding = function(trip)
	Grab(trip)
	local unitID = trip.unit
	trip.state = "land"
	trip.landFrames = 0
	trip.entrySpeed = max(sqrt(trip.vx * trip.vx + trip.vz * trip.vz), 1.5)
	-- cargo hangs under a transport: stay above the pad with it
	trip.hoverOffset = 0
	local cargo = spGetUnitIsTransporting(unitID)
	if cargo and cargo[1] then
		for i = 1, #cargo do
			trip.hoverOffset = max(trip.hoverOffset, UnitDefs[Spring.GetUnitDefID(cargo[i])].height + 8)
		end
	end
	CallScript(unitID, "Deactivate")
	CallScript(unitID, "StopMoving")
end

--------------------------------------------------------------------------------
-- Engine flight
--------------------------------------------------------------------------------

local function StepFly(trip, frame)
	local unitID = trip.unit
	local pad = trip.pad
	if frame > trip.deadline then
		EndTrip(trip, RETRY_DELAY)
		return
	end
	local tx, ty, tz = PointPosition(pad.id, trip.point.piece)
	local x, _, z = spGetUnitPosition(unitID)
	local d = sqrt((tx - x)^2 + (tz - z)^2)
	local vx, _, vz = spGetUnitVelocity(unitID)
	if d < max(120, 30 * sqrt(vx * vx + vz * vz)) then
		StartLanding(trip)
		return
	end
	if not trip.goalAt or frame >= trip.goalAt then
		trip.goalAt = frame + 30
		spSetUnitMoveGoal(unitID, tx, ty, tz, 8)
	end
end

local function StepHold(trip)
	local px, py, pz = spGetUnitPosition(trip.waitPad)
	if not px then
		return
	end
	trip.holdAngle = trip.holdAngle + trip.holdSpeed / HOLD_RADIUS
	local tx = px + sin(trip.holdAngle) * HOLD_RADIUS
	local tz = pz + cos(trip.holdAngle) * HOLD_RADIUS
	local ty = py + HOLD_HEIGHT + HOLD_STACK * trip.slot
	-- steers for its place on the circle, so it joins and changes height smoothly
	trip.vx = trip.vx + (tx - trip.x - trip.vx * 15) * 0.004
	trip.vz = trip.vz + (tz - trip.z - trip.vz * 15) * 0.004
	local speed = sqrt(trip.vx * trip.vx + trip.vz * trip.vz)
	if speed > trip.holdSpeed * 1.3 then
		trip.vx, trip.vz = trip.vx / speed * trip.holdSpeed * 1.3, trip.vz / speed * trip.holdSpeed * 1.3
	end
	trip.vy = max(min((ty - trip.y) * 0.03, 2), -2)
	trip.x, trip.y, trip.z = trip.x + trip.vx, trip.y + trip.vy, trip.z + trip.vz
	if speed > 0.5 then
		local turn = WrapAngle(atan2(-trip.vx, trip.vz) - trip.yaw)
		turn = max(min(turn, 0.05), -0.05)
		trip.yaw = trip.yaw + turn
		trip.roll = trip.roll + (turn * 6 - trip.roll) * 0.05
	end
	trip.pitch = trip.pitch * 0.95
	Place(trip)
end

local function StepWait(trip, frame, slot)
	local unitID = trip.unit
	trip.slot = slot
	if frame - trip.waitSince > WAIT_TIMEOUT then
		EndTrip(trip, RETRY_DELAY)
		return
	end
	Search(trip)
	if trips[unitID] ~= trip or trip.state ~= "wait" then
		return
	end
	local px, py, pz = spGetUnitPosition(trip.waitPad)
	if moveKind[planes[unitID]] == "airplane" then
		if not trip.grabbed then
			local x, _, z = spGetUnitPosition(unitID)
			if (x - px)^2 + (z - pz)^2 < (HOLD_RADIUS + 200)^2 then
				Grab(trip)
				trip.holdAngle = atan2(x - px, z - pz)
				trip.holdSpeed = min(UnitDefs[planes[unitID]].speed / 30 * 0.6, 6)
			else
				spSetUnitMoveGoal(unitID, px, py, pz, 8)
			end
		end
	else
		-- a spot of its own on a ring around the pad
		local a = slot * 2.4
		local r = 160 + 30 * slot
		spSetUnitMoveGoal(unitID, px + sin(a) * r, py, pz + cos(a) * r, 16)
	end
end

local function PadGone(trip)
	if trip.state == "land" or trip.state == "deck" then
		trip.research = true
		Lift(trip)
		ReleasePoint(trip)
	elseif trip.state == "lift" then
		local health, maxHealth = spGetUnitHealth(trip.unit)
		trip.research = not trip.cancelled and health < maxHealth
		ReleasePoint(trip)
	else
		ReleasePoint(trip)
		trip.state = "search"
	end
end

--------------------------------------------------------------------------------
-- Call-ins
--------------------------------------------------------------------------------

local function FinishUnit(unitID, unitDefID)
	if isPad[unitDefID] then
		AddPad(unitID, unitDefID)
	end
	if isAir[unitDefID] then
		planes[unitID] = unitDefID
		if not moveKind[unitDefID] then
			moveKind[unitDefID] = Spring.GetUnitMoveTypeData(unitID).name
		end
	end
end

function gadget:Initialize()
	gadgetHandler:RegisterCMDID(CMD_PAD_REPAIR)
	-- /luarules reload: the states are still set, the rest is not
	local units = Spring.GetAllUnits()
	for i = 1, #units do
		local unitID = units[i]
		local unitDefID = Spring.GetUnitDefID(unitID)
		gadget:UnitCreated(unitID, unitDefID)
		if not spGetUnitIsBeingBuilt(unitID) then
			FinishUnit(unitID, unitDefID)
		end
	end
end

function gadget:Shutdown()
	for unitID, trip in pairs(trips) do
		if trip.grabbed then
			mc.Disable(unitID)
		end
	end
end

function gadget:UnitCreated(unitID, unitDefID)
	if isAir[unitDefID] then
		Spring.InsertUnitCmdDesc(unitID, padCmdDesc)
	end
end

function gadget:UnitFinished(unitID, unitDefID)
	FinishUnit(unitID, unitDefID)
	if isAir[unitDefID] then
		-- the button starts on LandAt 30 but the state behind it on 0
		spGiveOrderToUnit(unitID, CMD.AUTOREPAIRLEVEL, {1}, 0)
	end
end

function gadget:UnitDestroyed(unitID, unitDefID)
	newTrips[unitID] = nil
	local trip = trips[unitID]
	if trip then
		ReleasePoint(trip)
		LeaveWaiters(trip)
		trips[unitID] = nil
	end
	planes[unitID] = nil
	retryAt[unitID] = nil
	if pads[unitID] then
		pads[unitID] = nil
		for _, t in pairs(trips) do
			if (t.pad and t.pad.id == unitID) or t.waitPad == unitID then
				PadGone(t)
			end
		end
	end
end

function gadget:UnitGiven(unitID)
	retryAt[unitID] = nil
end

function gadget:AllowCommand(unitID, unitDefID, teamID, cmdID, cmdParams)
	if cmdID ~= CMD_PAD_REPAIR then
		return true
	end
	if not isAir[unitDefID] then
		return false
	end
	local padID = cmdParams[1]
	if padID and not PadUsable(padID, teamID) then
		return false
	end
	local health, maxHealth = spGetUnitHealth(unitID)
	return health < maxHealth
end

function gadget:CommandFallback(unitID, unitDefID, teamID, cmdID, cmdParams, cmdOptions, cmdTag)
	if cmdID ~= CMD_PAD_REPAIR then
		return false
	end
	if trips[unitID] or newTrips[unitID] then
		return true, false
	end
	local health, maxHealth = spGetUnitHealth(unitID)
	if not planes[unitID] or health >= maxHealth then
		return true, true
	end
	newTrips[unitID] = {unit = unitID, tag = cmdTag, wanted = cmdParams[1], state = "search"}
	return true, false
end

-- an aircraft whose repair level says it should go
local function CheckPlane(unitID, frame)
	if trips[unitID] or (retryAt[unitID] and frame < retryAt[unitID]) then
		return
	end
	local level = spGetUnitStates(unitID).autorepairlevel or 0
	if level <= 0 then
		return
	end
	local health, maxHealth = spGetUnitHealth(unitID)
	if health >= maxHealth * level or spGetUnitIsStunned(unitID) or spGetUnitTransporter(unitID) then
		return
	end
	if spGetUnitCurrentCommand(unitID) == CMD_PAD_REPAIR or not AnyPad(spGetUnitTeam(unitID)) then
		return
	end
	spGiveOrderToUnit(unitID, CMD.INSERT, {0, CMD_PAD_REPAIR, CMD.OPT_INTERNAL}, CMD.OPT_ALT)
end

function gadget:GameFrame(frame)
	for unitID, trip in pairs(newTrips) do
		trips[unitID] = trip
		newTrips[unitID] = nil
	end
	if frame % 15 == 0 then
		local slot = 1
		while waiters[slot] do
			local trip = waiters[slot]
			StepWait(trip, frame, slot)
			if waiters[slot] == trip then
				slot = slot + 1
			end
		end
	end
	for unitID, trip in pairs(trips) do
		local state = trip.state
		-- the trip's command is still the one it is doing?
		if state ~= "lift" and (frame + unitID) % 8 == 0 then
			local cmdID, _, cmdTag = spGetUnitCurrentCommand(unitID)
			if cmdID ~= CMD_PAD_REPAIR or cmdTag ~= trip.tag then
				if state == "land" or state == "deck" then
					Lift(trip, "cancel")
				else
					EndTrip(trip, RETRY_DELAY)
				end
				state = nil
			elseif trip.pad and not PadUsable(trip.pad.id, spGetUnitTeam(unitID)) then
				PadGone(trip)
				state = nil
			end
		end
		if state == "land" then
			StepLand(trip)
		elseif state == "deck" then
			StepDeck(trip, frame)
		elseif state == "lift" then
			StepLift(trip)
		elseif state == "search" then
			Search(trip)
		elseif state == "wait" and trip.grabbed then
			StepHold(trip)
		elseif state == "fly" and (frame + unitID) % 4 == 0 then
			StepFly(trip, frame)
		end
	end
	if frame % 30 == 0 then
		for unitID in pairs(planes) do
			CheckPlane(unitID, frame)
		end
	end
end
