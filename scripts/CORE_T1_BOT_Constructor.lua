-- Construction Kbot (CORE_T1_BOT_Constructor): Lua unit script for the remodelled walker (standard biped skeleton).
-- Ported from TA's CORE_T1_BOT_Constructor.COB: Go slides the end cap off (guncover x -2.35), swings the nano cannon
-- up and round (nanogun z -90 then -180, gunclamp y +90, all 600 deg/s), telescopes the nozzle 9.6 elmo and turns the
-- torso to the build heading before setting INBUILDSTANCE; Stop reverses it. Same RequestState queue, QueryNanoPiece
-- = nanospray2, SweetSpot = torso, same death table and corpse types. COB negates turn-z and move-x destinations
-- (Recoil CobInstance.h "COBWTF"), so those values are sign-flipped here. The walk is the shared one.

pelvis, legs, rthigh, rleg, rfoot, lthigh, lleg, lfoot = piece('pelvis', 'legs', 'rthigh', 'rleg', 'rfoot', 'lthigh', 'lleg', 'lfoot')
ground, torso, gunclamp, nanogun, nozzle, nanospray2, guncover =
	piece('ground', 'torso', 'gunclamp', 'nanogun', 'nozzle', 'nanospray2', 'guncover')

include "smokeunit.lua"
local walk = include("headers/walk.lua")
walk.Biped()

local rad = math.rad
local SPD = rad(599.85)
local buildHeading = 0

local function Go()
	Move(guncover, x_axis, 0)
	Move(guncover, x_axis, 2.35, 50)
	Sleep(200)
	Turn(nanogun, z_axis, rad(89.99), SPD)
	Sleep(200)
	Turn(gunclamp, y_axis, rad(89.99), SPD)
	Sleep(200)
	Turn(nanogun, z_axis, rad(179.99), SPD)
	Sleep(200)
	Move(nozzle, x_axis, 9.625, 50)
	Sleep(400)
	Turn(torso, y_axis, buildHeading, SPD)
	WaitForTurn(torso, y_axis)
	SetUnitValue(COB.INBUILDSTANCE, 1)
end

local function Stop()
	SetUnitValue(COB.INBUILDSTANCE, 0)
	Turn(torso, y_axis, 0, SPD)
	WaitForTurn(torso, y_axis)
	Move(guncover, x_axis, 2.35)
	Move(nozzle, x_axis, 9.625)
	Move(nozzle, x_axis, 0, 50)
	Turn(gunclamp, x_axis, 0)
	Turn(gunclamp, y_axis, rad(89.99))
	Turn(nanogun, z_axis, rad(179.99))
	Sleep(200)
	Turn(nanogun, z_axis, rad(89.99), SPD)
	Sleep(200)
	Turn(gunclamp, y_axis, 0, SPD)
	Sleep(200)
	Turn(nanogun, z_axis, 0, SPD)
	Sleep(200)
	Move(guncover, x_axis, 0, 50)
	Sleep(400)
end

-- COB RequestState: one worker runs Go/Stop until the requested state stops changing (0 = open, 1 = closed)
local wanted, current, busy = 1, 1, false
local function RequestState(state)
	wanted = state
	if busy then return end
	busy = true
	while wanted ~= current do
		current = wanted
		if current == 0 then Go() else Stop() end
	end
	busy = false
end

function script.Create()
	StartThread(SmokeUnit, {torso, pelvis})
end

function script.Activate()
	StartThread(RequestState, 0)
end

function script.Deactivate()
	StartThread(RequestState, 1)
end

function script.StartBuilding(heading, pitch)
	buildHeading = heading
	StartThread(RequestState, 0)
end

function script.StopBuilding()
	StartThread(RequestState, 1)
end

function script.QueryNanoPiece()
	return nanospray2             -- COB: piece 1
end

function script.SweetSpot(num)
	return torso                  -- COB: piece 0
end

local DEATH = {ground, gunclamp, guncover, lfoot, lleg, lthigh, nanogun, nanospray2, nozzle, rfoot, rleg, rthigh}

function script.Killed(recentDamage, maxHealth)
	local severity = recentDamage / maxHealth * 100
	Explode(torso, SFX.NONE)
	if severity <= 25 then
		for _, p in ipairs(DEATH) do Explode(p, SFX.NONE) end
		Explode(pelvis, SFX.NONE)
		return 1
	elseif severity <= 50 then
		for _, p in ipairs(DEATH) do Explode(p, SFX.FALL) end
		Explode(pelvis, SFX.SHATTER)
		return 2
	end
	local f = SFX.FALL + SFX.SMOKE + SFX.FIRE + SFX.EXPLODE_ON_HIT
	for _, p in ipairs(DEATH) do Explode(p, f) end
	Explode(pelvis, SFX.SHATTER + ((severity > 99) and SFX.EXPLODE_ON_HIT or 0))
	return 3
end
